from typing import Tuple, List, Dict


def calculate_points_between(
    origin: Tuple[int, int], destination: Tuple[int, int]
) -> List[Tuple[int, int]]:
    (origin_x, origin_y) = origin
    (destination_x, destination_y) = destination
    points: List[Tuple[int, int]] = []

    if origin_x == destination_x:
        for y in range(min(origin_y, destination_y), max(origin_y, destination_y) + 1):
            points.append((origin_x, y))
    elif origin_y == destination_y:
        for x in range(min(origin_x, destination_x), max(origin_x, destination_x) + 1):
            points.append((x, origin_y))

    return points


def solve() -> int:
    origin: Tuple[int, int]
    destination: Tuple[int, int]
    count: Dict[Tuple[int, int], int] = {}

    input = open("input.txt", "r")
    for line in input.readlines():
        splitted = line.strip().split(" -> ")
        origin_splitted = splitted[0].split(",")
        origin = (int(origin_splitted[0]), int(origin_splitted[-1]))
        destination_splitted = splitted[-1].split(",")
        destination = (int(destination_splitted[0]), int(destination_splitted[-1]))
        points = calculate_points_between(origin, destination)
        for point in points:
            if point in count:
                count[point] += 1
            else:
                count[point] = 1

    total_overlap = 0
    for point, times in count.items():
        if times >= 2:
            total_overlap += 1

    return total_overlap


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
