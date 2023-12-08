from typing import Generator


class HandType:
    """
    Stores hand, determines hand type, and calculates rank.
    Implements __lt__ to allow sorting by rank and strength.
    Uses DISCRIMINANT to determine rank instead of set of rules.
    """
    CARDS = 'AKQJT98765432'
    DISCRIMINANT = {
        -4: 0,
        -2: 1,
        -1: 2,
        0: 3,
        1: 4,
        2: 5,
        4: 6,
    }

    def __init__(self, hand: str, bid: int) -> None:
        self.hand = hand
        self.bid = bid
        hand_set = set(hand)
        self.hand_set_len = len(hand_set)
        self.counts = {card: hand.count(card) for card in hand_set}

    def __getitem__(self, index: int) -> str:
        return self.hand[index]

    def __lt__(self, other: 'HandType') -> bool:
        if self.rank != other.rank:
            return self.rank < other.rank
        for self_card, other_card in zip(self.strength(), other.strength()):
            if self_card == other_card:
                continue
            return self_card < other_card

    def strength(self) -> Generator:
        """Generate card strength of each card in hand"""
        for card in self.hand:
            yield 15 - self.CARDS.index(card)

    @property
    def rank(self) -> int:
        """Return highest possible rank of hand"""
        return self.DISCRIMINANT[max(self.counts.values()) - self.hand_set_len]


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        lines = f_in.readlines()

    total = 0
    hands = [HandType(hand, int(bid)) for hand, bid in (line.strip().split() for line in lines)]
    hands.sort()
    for count, hand in enumerate(hands, start=1):
        total += count * hand.bid

    return total


if __name__ == '__main__':
    print(main())
