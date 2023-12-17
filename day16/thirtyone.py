"""
--- The Floor Will Be Lava ---

With the beam of light completely focused somewhere, the reindeer leads you deeper still into the Lava Production Facility. At some point, you realize that the steel facility walls have been replaced with cave, and the doorways are just cave, and the floor is cave, and you're pretty sure this is actually just a giant cave.

Finally, as you approach what must be the heart of the mountain, you see a bright light in a cavern up ahead. There, you discover that the beam of light you so carefully focused is emerging from the cavern wall closest to the facility and pouring all of its energy into a contraption on the opposite side.

Upon closer inspection, the contraption appears to be a flat, two-dimensional square grid containing empty space (.), mirrors (/ and \), and splitters (| and -).

The contraption is aligned so that most of the beam bounces around the grid, but each tile on the grid converts some of the beam's light into heat to melt the rock in the cavern.

You note the layout of the contraption (your puzzle input). For example:

.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
The beam enters in the top-left corner from the left and heading to the right. Then, its behavior depends on what it encounters as it moves:

If the beam encounters empty space (.), it continues in the same direction.
If the beam encounters a mirror (/ or \), the beam is reflected 90 degrees depending on the angle of the mirror. For instance, a rightward-moving beam that encounters a / mirror would continue upward in the mirror's column, while a rightward-moving beam that encounters a \ mirror would continue downward from the mirror's column.
If the beam encounters the pointy end of a splitter (| or -), the beam passes through the splitter as if the splitter were empty space. For instance, a rightward-moving beam that encounters a - splitter would continue in the same direction.
If the beam encounters the flat side of a splitter (| or -), the beam is split into two beams going in each of the two directions the splitter's pointy ends are pointing. For instance, a rightward-moving beam that encounters a | splitter would split into two beams: one that continues upward from the splitter's column and one that continues downward from the splitter's column.
Beams do not interact with other beams; a tile can have many beams passing through it at the same time. A tile is energized if that tile has at least one beam pass through it, reflect in it, or split in it.

In the above example, here is how the beam of light bounces around the contraption:

>|<<<\....
|v-.\^....
.v...|->>>
.v...v^.|.
.v...v^...
.v...v^..\
.v../2\\..
<->-/vv|..
.|<<<2-|.\
.v//.|.v..
Beams are only shown on empty tiles; arrows indicate the direction of the beams. If a tile contains beams moving in multiple directions, the number of distinct directions is shown instead. Here is the same diagram but instead only showing whether a tile is energized (#) or not (.):

######....
.#...#....
.#...#####
.#...##...
.#...##...
.#...##...
.#..####..
########..
.#######..
.#...#.#..
Ultimately, in this example, 46 tiles become energized.

The light isn't energizing enough tiles to produce lava; to debug the contraption, you need to start by analyzing the current situation. With the beam starting in the top-left heading right, how many tiles end up being energized?
"""

from typing import Dict, Self

import pandas as pd

# TODO mode enum


class BeamPath:
    """DFS ray tracing, recursive"""
    def __init__(self, layout: pd.DataFrame) -> None:
        self.layout = layout
        # self.energized_layout = layout.copy()
        self.visited: Dict[tuple, tuple] = {}  # {(row_idx, col_idx): (mode, count_idx))} map to keep track of visited cells

    def __call__(self, offset) -> Self:
        """Calculate beam path from top left corner"""
        self.horizontal(offset, 0, 'right', first_call=True)
        return self

    def horizontal(self, y_idx: int, offset: int, mode: str, first_call=False) -> None:
        """Horizontal ray tracing"""
        row = self.layout.iloc[y_idx, offset:] if mode == 'right' else reversed(self.layout.iloc[y_idx, :offset + 1])
        counts = range(offset, len(row) + offset) if mode == 'right' else reversed(range(offset + 1))
        for count_idx, (count, symbol) in enumerate(zip(counts, row)):
            if self.visited.get((y_idx, count)) == (mode, count_idx):
                return
            self.visited[(y_idx, count)] = (mode, count_idx)
            # self.energized_layout.iat[y_idx, count] = '#'
            if count_idx == 0 and not first_call:
                continue
            if symbol in ('.', '-'):
                continue
            if (symbol == '\\' and mode == 'right') or (symbol == '/' and mode == 'left'):
                self.vertical(count, y_idx, 'down')
                return
            if (symbol == '\\' and mode == 'left') or (symbol == '/' and mode == 'right'):
                self.vertical(count, y_idx, 'up')
                return
            if symbol == '|':
                self.vertical(count, y_idx, 'down')
                self.vertical(count, y_idx, 'up')
                return
            raise ValueError('Unknown symbol')

    # TODO I know the code for vertical and horizontal is almost identical
    # (transposition, I've made similar in previous days), but I'm too lazy to refactor it
    def vertical(self, x_idx: int, offset: int, mode: str, first_call=False) -> None:
        """Vertical ray tracing"""
        row = self.layout.iloc[offset:, x_idx] if mode == 'down' else reversed(self.layout.iloc[:offset + 1, x_idx])
        counts = range(offset, len(row) + offset) if mode == 'down' else reversed(range(offset + 1))
        for count_idx, (count, symbol) in enumerate(zip(counts, row)):
            if self.visited.get((count, x_idx)) == (mode, count_idx):
                return
            self.visited[(count, x_idx)] = (mode, count_idx)
            # self.energized_layout.iat[count, x_idx] = '#'
            if count_idx == 0 and not first_call:
                continue
            if symbol in ('.', '|'):
                continue
            if (symbol == '\\' and mode == 'down') or (symbol == '/' and mode == 'up'):
                self.horizontal(count, x_idx, 'right')
                return
            if (symbol == '\\' and mode == 'up') or (symbol == '/' and mode == 'down'):
                self.horizontal(count, x_idx, 'left')
                return
            if symbol == '-':
                self.horizontal(count, x_idx, 'left')
                self.horizontal(count, x_idx, 'right')
                return
            raise ValueError('Unknown symbol')


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        layout = pd.DataFrame(list(iter(row)) for row in f_in.read().splitlines())

    beam = BeamPath(layout)
    return len(beam(0).visited)


if __name__ == '__main__':
    print(main())
