"""
--- Step Counter ---

You manage to catch the airship right as it's dropping someone else off on their all-expenses-paid trip to Desert Island! It even helpfully drops you off near the gardener and his massive farm.

"You got the sand flowing again! Great work! Now we just need to wait until we have enough sand to filter the water for Snow Island and we'll have snow again in no time."

While you wait, one of the Elves that works with the gardener heard how good you are at solving problems and would like your help. He needs to get his steps in for the day, and so he'd like to know which garden plots he can reach with exactly his remaining 64 steps.

He gives you an up-to-date map (your puzzle input) of his starting position (S), garden plots (.), and rocks (#). For example:

...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
The Elf starts at the starting position (S) which also counts as a garden plot. Then, he can take one step north, south, east, or west, but only onto tiles that are garden plots. This would allow him to reach any of the tiles marked O:

...........
.....###.#.
.###.##..#.
..#.#...#..
....#O#....
.##.OS####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
Then, he takes a second step. Since at this point he could be at either tile marked O, his second step would allow him to reach any garden plot that is one step north, south, east, or west of any tile that he could have reached after the first step:

...........
.....###.#.
.###.##..#.
..#.#O..#..
....#.#....
.##O.O####.
.##.O#...#.
.......##..
.##.#.####.
.##..##.##.
...........
After two steps, he could be at any of the tiles marked O above, including the starting position (either by going north-then-south or by going west-then-east).

A single third step leads to even more possibilities:

...........
.....###.#.
.###.##..#.
..#.#.O.#..
...O#O#....
.##.OS####.
.##O.#...#.
....O..##..
.##.#.####.
.##..##.##.
...........
He will continue like this until his steps for the day have been exhausted. After a total of 6 steps, he could reach any of the garden plots marked O:

...........
.....###.#.
.###.##.O#.
.O#O#O.O#..
O.O.#.#.O..
.##O.O####.
.##.O#O..#.
.O.O.O.##..
.##.#.####.
.##O.##.##.
...........
In this example, if the Elf's goal was to get exactly 6 more steps today, he could use them to reach any of 16 garden plots.

However, the Elf actually needs to get 64 steps today, and the map he's handed you is much larger than the example map.

Starting from the garden plot marked S on your map, how many garden plots could the Elf reach in exactly 64 steps?
"""

from itertools import product

START = 'S'
ROCK = '#'

with open('input.txt', 'r') as f_in:
    rows = [row.strip() for row in f_in.readlines()]  # TODO to class attributes
len_x = len(rows[0])
len_y = len(rows)


def get_adjacent(idx: tuple[int, int]) -> set:
    """Add adjacent locations to set"""
    new = set()
    # this would be ok with 8 directions
    # for i in range(idx[0] - 1, idx[0] + 2):
    #     for j in range(idx[1] - 1, idx[1] + 2):
    #         if i == idx[0] and j == idx[1]:
    #             continue
    for i, j in (
        (idx[0] - 1, idx[1]),
        (idx[0] + 1, idx[1]),
        (idx[0], idx[1] - 1),
        (idx[0], idx[1] + 1),
    ):
        if 0 <= i < len_x and 0 <= j < len_y:
            if rows[i][j] != ROCK:
                new.add((i, j))

    return new


def main() -> int:
    """main"""
    for idx in product(range(len_x), range(len_y)):
        if rows[idx[0]][idx[1]] == START:
            break
    else:
        raise ValueError('No starting point found')

    locations: set[tuple[int, int]] = set()
    new = get_adjacent(idx)
    for _ in range(64):
        for item in locations:
            new.update(get_adjacent(item))
        locations = new
        new = set()

    # for row_count, row in enumerate(rows):
    #     print(''.join([item if tuple([row_count, count]) not in locations else 'O' for count, item in enumerate(row)]))

    return len(locations)


if __name__ == '__main__':
    print(main())
