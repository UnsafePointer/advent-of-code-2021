from __future__ import annotations

from dataclasses import dataclass, field
from math import sqrt
from typing import List, Optional, Tuple, Set, Dict
from itertools import combinations, permutations
from collections import defaultdict
from heapq import heappush, heappop
from copy import deepcopy


@dataclass
class Beacon:
    x: int
    y: int
    z: int
    scanner: int

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z, self.scanner))

    def distance(self, another: Beacon) -> float:
        return round(
            sqrt(
                pow(another.x - self.x, 2)
                + pow(another.y - self.y, 2)
                + pow(another.z - self.z, 2)
            ),
            10,
        )

    def dimensions(self) -> List[int]:
        return [self.x, self.y, self.z]


@dataclass
class Scanner:
    identifier: int
    beacons: Set[Beacon] = field(default_factory=set)

    def distances(self) -> Dict[float, Tuple[Beacon, Beacon]]:
        distances: Dict[float, Tuple[Beacon, Beacon]] = {}
        for (a, b) in combinations(self.beacons, 2):
            distance = a.distance(b)
            distances[distance] = (a, b)
        return distances

    def common_beacons(self, another: Scanner) -> List[Tuple[Beacon, Beacon]]:
        d0 = self.distances()
        d1 = another.distances()
        r = set(d0.keys()) & set(d1.keys())
        beacons: Dict[Beacon, Set[Beacon]] = {}
        for distance in r:
            (a, b) = d0[distance]
            if a in beacons:
                beacons[a] &= set(d1[distance])
            else:
                beacons[a] = set(d1[distance])

            if b in beacons:
                beacons[b] &= set(d1[distance])
            else:
                beacons[b] = set(d1[distance])
        beacon_mapping: List[Tuple[Beacon, Beacon]] = []
        for k, v in beacons.items():
            if len(v) == 1:
                beacon_mapping.append((k, v.pop()))
        return beacon_mapping

    def add_beacons(
        self,
        another: Scanner,
        signs: Tuple[int, int, int],
        ref: Tuple[int, int, int],
        indices: Tuple[int, int, int],
    ) -> None:
        (x_sign, y_sign, z_sign) = signs
        (x_ref, y_ref, z_ref) = ref
        (i, j, k) = indices
        for beacon in another.beacons:
            dims = beacon.dimensions()
            x = (dims[i] * (x_sign * -1)) + x_ref
            y = (dims[j] * (y_sign * -1)) + y_ref
            z = (dims[k] * (z_sign * -1)) + z_ref
            new_beacon = Beacon(x, y, z, self.identifier)
            self.beacons.add(new_beacon)
        return


def find_position_relative_to_common_beacons(
    beacon_mapping: List[Tuple[Beacon, Beacon]]
) -> Optional[Tuple[Tuple[int, int, int], Tuple[int, int, int], Tuple[int, int, int]]]:
    previous_ref: Optional[Tuple[int, int, int]]
    for (i, j, k) in permutations(range(3)):
        for x_sign in [-1, 1]:
            for y_sign in [-1, 1]:
                for z_sign in [-1, 1]:
                    found = True
                    previous_ref = None
                    for (point_0, point_1) in beacon_mapping:
                        dims = point_1.dimensions()
                        ref = (
                            point_0.x + (dims[i] * x_sign),
                            point_0.y + (dims[j] * y_sign),
                            point_0.z + (dims[k] * z_sign),
                        )
                        if previous_ref == None:
                            previous_ref = ref
                        else:
                            if previous_ref != ref:
                                found = False
                                break
                    if found:
                        return ((x_sign, y_sign, z_sign), previous_ref, (i, j, k))
    return None


def get_path_to_zero(
    current: int,
    current_path: List[int],
    known_paths: List[List[int]],
    mapping: Dict[int, Set[int]],
) -> Optional[List[int]]:
    if current == 0 and current_path not in known_paths:
        return current_path
    for option in mapping[current]:
        if option in current_path:
            continue
        option_path = current_path.copy()
        option_path.append(option)
        result = get_path_to_zero(option, option_path, known_paths, mapping)
        if result != None:
            return result
    return None


def solve() -> int:
    input = open("input.txt", "r")

    scanners: List[Scanner] = []
    current_scanner: Scanner
    for line in [s.strip() for s in input.readlines()]:
        if line.startswith("---"):
            identifier = int(line.split()[2])
            current_scanner = Scanner(identifier=identifier)
            scanners.append(current_scanner)
        elif line == "":
            continue
        else:
            (x, y, z) = tuple([int(s) for s in line.split(",")])
            beacon = Beacon(x, y, z, current_scanner.identifier)
            current_scanner.beacons.add(beacon)

    scanner_mapping: Dict[int, Set[int]] = defaultdict(lambda: set())
    for (a, b) in combinations(scanners, 2):
        beacon_mapping = a.common_beacons(b)
        if len(beacon_mapping) >= 12:
            scanner_mapping[a.identifier].add(b.identifier)
            scanner_mapping[b.identifier].add(a.identifier)

    priority_queue: List[Tuple[int, List[int]]] = []
    for idx in range(len(scanners)):
        known_paths = []
        while True:
            path = get_path_to_zero(idx, [idx], known_paths, scanner_mapping)
            if path:
                known_paths.append(path)
            else:
                break
        for known_path in known_paths:
            heappush(priority_queue, (len(known_path), (idx, known_path)))

    solved_count: Set[int] = set()
    solution_beacons: Set[Beacon] = set(scanners[0].beacons)
    while priority_queue:
        (_, (idx, path)) = heappop(priority_queue)
        if idx in solved_count:
            continue
        if len(path) == 1:
            continue
        scanners_copy = deepcopy(scanners)
        for i, j in zip(path, path[1:]):
            b = scanners_copy[i]
            a = scanners_copy[j]
            beacon_mapping = a.common_beacons(b)
            positions = find_position_relative_to_common_beacons(beacon_mapping)
            (signs, beacon_relative, indices) = positions
            a.add_beacons(b, signs, beacon_relative, indices)

        for beacon in scanners_copy[0].beacons:
            solution_beacons.add(beacon)
        solved_count.add(idx)

    return len(solution_beacons)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
