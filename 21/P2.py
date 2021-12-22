from typing import List, Tuple, Dict
from itertools import product


cache: Dict[Tuple[int, int, int, int], Tuple[int, int]] = {}


def count_games(
    player_1: int, player_2: int, score_1: int, score_2: int
) -> Tuple[int, int]:
    if score_1 >= 21:
        return (1, 0)
    if score_2 >= 21:
        return (0, 1)
    if (player_1, player_2, score_1, score_2) in cache:
        return cache[(player_1, player_2, score_1, score_2)]
    count = (0, 0)
    for (roll_1, roll_2, roll_3) in product([1, 2, 3], repeat=3):
        player_1_upd = sum([player_1, roll_1, roll_2, roll_3]) % 10
        score_1_upd = score_1 + player_1_upd + 1

        (p2_wins, p1_wins) = count_games(player_2, player_1_upd, score_2, score_1_upd)
        count = (count[0] + p1_wins, count[1] + p2_wins)
    cache[(player_1, player_2, score_1, score_2)] = count
    return count


def solve() -> int:
    input = open("input.txt", "r")
    players: List[int] = [
        int(input.readline().strip().split()[4]) - 1,
        int(input.readline().strip().split()[4]) - 1,
    ]

    wins = count_games(players[0], players[1], 0, 0)
    return max(wins)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
