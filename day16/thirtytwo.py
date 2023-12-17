from typing import Self

import pandas as pd
from numpy import rot90

from thirtyone import BeamPath


class BeamPathTop(BeamPath):
    """Start the beam from the top left corner going down"""
    def __call__(self, offset) -> Self:
        self.vertical(offset, 0, 'down', first_call=True)
        return self


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        layout = pd.DataFrame(list(iter(row)) for row in f_in.read().splitlines())

    totals = []
    for _ in range(4):
        beam = BeamPath(layout)
        totals.append(len(beam(0).visited))
        for offset in range(layout.shape[0]):
            beam = BeamPathTop(layout)
            totals.append(len(beam(offset).visited))
        layout = pd.DataFrame(rot90(layout))

    return max(totals)


if __name__ == '__main__':
    print(main())
