from dataclasses import dataclass
from typing import Tuple, Optional
from sys import maxsize


@dataclass
class Probe:
    position: Tuple[int, int]
    velocity: Tuple[int, int]
    highest_vertical_position = -maxsize

    def __hash__(self) -> int:
        return hash(self.velocity)

    def advance(self) -> None:
        (x, y) = self.position
        (x_velocity, y_velocity) = self.velocity
        new_y = y + y_velocity
        self.position = (x + x_velocity, new_y)
        self.highest_vertical_position = max(new_y, self.highest_vertical_position)
        if x_velocity > 0:
            x_velocity -= 1
        elif x_velocity < 0:
            x_velocity += 1
        y_velocity -= 1
        self.velocity = (x_velocity, y_velocity)

    def check_target(self, target: Tuple[int, int, int, int]) -> Tuple[bool, bool]:
        (x, y) = self.position
        (_, y_velocity) = self.velocity
        (x_start, x_end, y_start, y_end) = target
        is_within_target = x in range(x_start, x_end + 1) and y in range(
            y_start, y_end + 1
        )
        if x > x_end:  # probe is past the target in the horizontal axis
            return is_within_target, False
        if (
            y_velocity < 0 and y < y_start
        ):  # probe is already descending and the target is higher in the horizontal axis
            return is_within_target, False
        return is_within_target, True


def try_probe(
    velocity: Tuple[int, int], target_range: Tuple[int, int, int, int]
) -> Optional[Probe]:
    probe = Probe((0, 0), velocity)
    useful_probe = False
    while True:
        probe.advance()
        (is_within_target, can_reach_target) = probe.check_target(target_range)
        if is_within_target:
            useful_probe = True
        if not can_reach_target:
            break
    if useful_probe:
        return probe
    else:
        return None


def solve() -> int:
    input = open("input.txt", "r").readline().strip().split()
    x_range = [int(s) for s in input[2][2:-1].split("..")]
    y_range = [int(s) for s in input[3][2:].split("..")]

    target_range: Tuple[int, int, int, int] = (
        x_range[0],
        x_range[-1],
        y_range[0],
        y_range[-1],
    )
    max_value = max(
        abs(x_range[0]), abs(x_range[-1]), abs(y_range[0]), abs(y_range[-1])
    )
    useful_probes = 0

    for x_velocity in range(-max_value - 1, max_value + 1):
        for y_velocity in range(-max_value - 1, max_value + 1):
            probe = try_probe((x_velocity, y_velocity), target_range)
            if probe:
                useful_probes += 1

    return useful_probes


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
