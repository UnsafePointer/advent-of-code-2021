from typing import Set, Tuple, Dict, List, FrozenSet
from collections import defaultdict
from sys import maxsize
from heapq import heappop, heappush
from copy import deepcopy
from os import linesep
from functools import reduce


def is_vertial_location_in_hallway(y: int) -> bool:
    return y == 4


def get_rooms_state(
    state: FrozenSet[Tuple[str, int, int]]
) -> Dict[int, Dict[str, int]]:
    rooms: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(lambda: 0))
    for (_type, x, y) in state:
        if is_vertial_location_in_hallway(y):
            continue
        rooms[x][_type] += 1
    return rooms


def get_possible_hallway_locations_for_room_exit(
    state: FrozenSet[Tuple[str, int, int]], x: int
) -> Set[Tuple[int, int]]:
    min_x = 0
    max_x = 10
    for (_, _x, _y) in state:
        if not is_vertial_location_in_hallway(_y):
            continue
        if _x < x:
            min_x = max(min_x, _x + 1)
        if _x > x:
            max_x = min(max_x, _x - 1)
    possible_locations: Set[Tuple[int, int]] = set()
    for _x in range(min_x, max_x + 1):
        if _x in [2, 4, 6, 8]:  # they can't be in front of the door
            continue
        possible_locations.add((_x, 4))
    return possible_locations


def calculate_energy_cost(_type: str, x1: int, y1: int, x2: int, y2: int) -> int:
    energy_cost: Dict[str, int] = {"A": 1, "B": 10, "C": 100, "D": 1000}
    if is_vertial_location_in_hallway(y1):
        return (abs(y1 - y2) + abs(x1 - x2)) * energy_cost[_type]
    else:
        return (abs(4 - y1) + abs(4 - y2) + abs(x1 - x2)) * energy_cost[_type]


target_room_per_type: Dict[str, int] = {"A": 2, "B": 4, "C": 6, "D": 8}


def can_enter_own_room(
    state: FrozenSet[Tuple[str, int, int]],
    ampiphod: Tuple[str, int, int],
    rooms_state: Dict[int, Dict[str, int]],
) -> bool:
    (_type, x, y) = ampiphod
    target_room = target_room_per_type[_type]

    # is there space?
    ampiphod_in_room = reduce(lambda x, y: x + y, rooms_state[target_room].values(), 0)
    if ampiphod_in_room >= 4:  # Room is full
        return False
    if (
        rooms_state[target_room][_type] != ampiphod_in_room
    ):  # Room is occupied by other type of ampiphod
        return False

    for other_ampiphod in state:
        (_, other_x, other_y) = other_ampiphod

        if other_x == x and other_y == y:  # Skip self
            continue

        if is_vertial_location_in_hallway(other_y):
            if other_x < x and other_x > target_room:
                return False
            elif other_x > x and other_x < target_room:
                return False

    return True


def can_exit_room(
    ampiphod: Tuple[str, int, int], rooms_state: Dict[int, Dict[str, int]]
) -> bool:
    (_, x, y) = ampiphod

    ampiphod_in_room = reduce(lambda x, y: x + y, rooms_state[x].values())
    if (y + 1) == ampiphod_in_room:  # If it's the first one
        return True

    return False


def generate_new_state(
    base_state: FrozenSet[Tuple[str, int, int]],
    to_remove: Tuple[str, int, int],
    to_add: Tuple[str, int, int],
) -> FrozenSet[Tuple[str, int, int]]:
    new_state = set(deepcopy(base_state))
    new_state.remove(to_remove)
    new_state.add(to_add)
    return frozenset(new_state)


def generarte_sub_states(
    state: FrozenSet[Tuple[str, int, int]]
) -> FrozenSet[Tuple[int, FrozenSet[Tuple[str, int, int]]]]:
    sub_states: Set[Tuple[int, FrozenSet[Tuple[str, int, int]]]] = set()
    rooms_state = get_rooms_state(state)
    for ampiphod in state:
        (_type, x, y) = ampiphod
        if is_vertial_location_in_hallway(y):
            if can_enter_own_room(state, ampiphod, rooms_state):
                target_room = target_room_per_type[_type]
                new_y = rooms_state[target_room][_type]
                sub_states.add(
                    (
                        calculate_energy_cost(_type, x, y, target_room, new_y),
                        generate_new_state(
                            state,
                            ampiphod,
                            (_type, target_room, new_y),
                        ),
                    )
                )
        else:
            if can_exit_room(ampiphod, rooms_state):
                if can_enter_own_room(state, ampiphod, rooms_state):
                    target_room = target_room_per_type[_type]
                    new_y = rooms_state[target_room][_type]
                    sub_states.add(
                        (
                            calculate_energy_cost(_type, x, y, target_room, new_y),
                            generate_new_state(
                                state,
                                ampiphod,
                                (_type, target_room, new_y),
                            ),
                        )
                    )
                for (
                    hallway_x,
                    hallway_y,
                ) in get_possible_hallway_locations_for_room_exit(state, x):
                    sub_states.add(
                        (
                            calculate_energy_cost(_type, x, y, hallway_x, hallway_y),
                            generate_new_state(
                                state,
                                ampiphod,
                                (_type, hallway_x, hallway_y),
                            ),
                        )
                    )

    return frozenset(sub_states)


def is_end_state(state: FrozenSet[Tuple[str, int, int]]) -> bool:
    rooms_state = get_rooms_state(state)
    at_home = (
        rooms_state[2]["A"]
        + rooms_state[4]["B"]
        + rooms_state[6]["C"]
        + rooms_state[8]["D"]
    )
    return at_home == 16


def state_repr(state: Set[Tuple[str, int, int]]) -> str:
    hallway = ["."] * 11
    rooms_1 = list("##.#.#.#.##")
    rooms_2 = list("##.#.#.#.##")
    rooms_3 = list("##.#.#.#.##")
    rooms_4 = list("##.#.#.#.##")
    for (_type, x, y) in state:
        if is_vertial_location_in_hallway(y):
            hallway[x] = _type
        elif y == 3:
            rooms_1[x] = _type
        elif y == 2:
            rooms_2[x] = _type
        elif y == 1:
            rooms_3[x] = _type
        elif y == 0:
            rooms_4[x] = _type

    rooms_2 = rooms_2[1:-1]
    rooms_3 = rooms_3[1:-1]
    rooms_4 = rooms_4[1:-1]
    s = ""
    s += "#############" + linesep
    s += "#" + "".join(hallway) + "#" + linesep
    s += "#" + "".join(rooms_1) + "#" + linesep
    s += "  " + "".join(rooms_2) + linesep
    s += "  " + "".join(rooms_3) + linesep
    s += "  " + "".join(rooms_4) + linesep
    s += "  #########" + linesep
    return s


def solve() -> int:
    input = open("input.txt", "r")
    input.readline()
    input.readline()

    initial_state: Set[Tuple[str, int, int]] = set()
    for idx, type in enumerate(input.readline()[3:-4].split("#")):
        initial_state.add((type, idx * 2 + 2, 3))
    for idx, type in enumerate(input.readline()[3:-2].split("#")):
        initial_state.add((type, idx * 2 + 2, 2))
    for idx, type in enumerate(input.readline()[3:-2].split("#")):
        initial_state.add((type, idx * 2 + 2, 1))
    for idx, type in enumerate(input.readline()[3:-2].split("#")):
        initial_state.add((type, idx * 2 + 2, 0))

    visited: Set[FrozenSet[Tuple[str, int, int]]] = set()
    energy_cost: Dict[FrozenSet[Tuple[str, int, int]], int] = defaultdict(
        lambda: maxsize
    )
    energy_cost[frozenset(initial_state)] = 0

    priority_queue: List[Tuple[int, FrozenSet[Tuple[str, int, int]]]] = []
    heappush(priority_queue, (0, frozenset(initial_state)))
    while priority_queue:
        (_, current_state) = heappop(priority_queue)
        if current_state in visited:
            continue

        sub_states = generarte_sub_states(current_state)
        for (sub_state_energy_cost, sub_state) in sub_states:
            sub_state_total_energy_cost = (
                energy_cost[current_state] + sub_state_energy_cost
            )
            frozen_sub_state = frozenset(sub_state)
            if sub_state_total_energy_cost < energy_cost[frozen_sub_state]:
                energy_cost[frozen_sub_state] = sub_state_total_energy_cost
                heappush(
                    priority_queue, (sub_state_total_energy_cost, frozen_sub_state)
                )
        visited.add(current_state)
        if is_end_state(current_state):
            break

    return energy_cost[current_state]


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
