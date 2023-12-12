"""
--- Cosmic Expansion ---

You continue following signs for "Hot Springs" and eventually come across an observatory. The Elf within turns out to be a researcher studying cosmic expansion using the giant telescope here.

He doesn't know anything about the missing machine parts; he's only visiting for this research project. However, he confirms that the hot springs are the next-closest area likely to have people; he'll even take you straight there once he's done with today's observation analysis.

Maybe you can help him with the analysis to speed things up?

The researcher has collected a bunch of data and compiled the data into a single giant image (your puzzle input). The image includes empty space (.) and galaxies (#). For example:

...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies. However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the observatory.

Due to something involving gravitational effects, only some space expands. In fact, the result is that any rows or columns that contain no galaxies should all actually be twice as big.

In the above example, three columns and two rows contain no galaxies:

   v  v  v
 ...#......
 .......#..
 #.........
>..........<
 ......#...
 .#........
 .........#
>..........<
 .......#..
 #...#.....
   ^  ^  ^
These rows and columns need to be twice as big; the result of cosmic expansion therefore looks like this:

....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......
Equipped with this expanded universe, the shortest path between every pair of galaxies can be found. It can help to assign every galaxy a unique number:

....1........
.........2...
3............
.............
.............
........4....
.5...........
............6
.............
.............
.........7...
8....9.......
In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't matter. For each pair, find any shortest path between the two galaxies using only steps that move up, down, left, or right exactly one . or # at a time. (The shortest path between two galaxies is allowed to pass through another galaxy.)

For example, here is one of the shortest paths between galaxies 5 and 9:

....1........
.........2...
3............
.............
.............
........4....
.5...........
.##.........6
..##.........
...##........
....##...7...
8....9.......
This path has length 9 because it takes a minimum of nine steps to get from galaxy 5 to galaxy 9 (the eight locations marked # plus the step onto galaxy 9 itself). Here are some other example shortest path lengths:

Between galaxy 1 and galaxy 7: 15
Between galaxy 3 and galaxy 6: 17
Between galaxy 8 and galaxy 9: 5
In this example, after expanding the universe, the sum of the shortest path between all 36 pairs of galaxies is 374.

Expand the universe, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?
"""

import numpy as np
import pandas as pd

GALAXY = '#'


def expand_universe(space_map: pd.DataFrame, increment: int) -> pd.DataFrame:
    """Add int(increment)-filled row and col next to every empty row and col"""
    df = space_map.copy()
    length = len(df.columns)
    to_expand = []
    for idx, col in df.items():
        if all(col == '.'):
            to_expand.append(idx)

    for count, idx in enumerate(reversed(to_expand)):  # reversed, because the index increments
        # increment index
        for col_name in reversed(range(idx, length + count)):
            df = df.rename(columns={col_name: col_name + 1})
        # insert col
        df[idx] = [increment] * length
    length += len(to_expand)
    df = df.reindex(columns=range(length))

    # the same for rows
    to_expand = []
    for idx, row in space_map.iterrows():
        if all(row == '.'):
            to_expand.append(idx)

    space_map = df.copy()
    for idx in reversed(to_expand):
        line = pd.DataFrame(dict(zip(range(length), [increment] * length)), index=[idx])
        space_map = pd.concat([space_map.iloc[:idx], line, space_map.iloc[idx:]]).reset_index(drop=True)

    return space_map


def main() -> int:
    """main"""
    space_map = pd.DataFrame(list(iter(row[1][0])) for row in pd.read_csv(
        'input.txt', dtype=str, header=None,
    ).iterrows())

    space_map = expand_universe(space_map, 1)
    # verify_map = pd.DataFrame(list(iter(row[1][0])) for row in pd.read_csv(
    #     'verify_expansion.txt', dtype=str, header=None,
    # ).iterrows())
    # for idx, row in space_map.iterrows():
    #     assert (row == verify_map.iloc[idx]).all()
    galaxies = np.where(space_map == GALAXY)
    indices = list(zip(*galaxies))
    total = 0
    for count, (row, col) in enumerate(indices):
        for inner_row, inner_col in indices[count + 1:]:
            # vector norm in discrete squared space
            total += abs(row - inner_row) + abs(col - inner_col)

    return total


if __name__ == '__main__':
    print(main())
