"""
45356
"""

from typing import Generator


class HandType:
    """
    Stores hand, determines hand type, and calculates rank.
    Implements __lt__ to allow sorting by rank and strength.
    """
    CARDS = 'AKQJT98765432'

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
        count = 6
        for count, is_hand_type in enumerate((
            self.five_of_a_kind,
            self.four_of_a_kind,
            self.full_house,
            self.three_of_a_kind,
            self.two_pair,
            self.one_pair,
        )):
            if is_hand_type():
                break
        else:
            return 0
        return 6 - count

    # The rules need to be evaluated from the highest rank.
    # Would need more complex logic otherwise.
    def five_of_a_kind(self) -> bool:
        return self.hand_set_len == 1

    def four_of_a_kind(self) -> bool:
        return 4 in self.counts.values()

    def full_house(self) -> bool:
        return 2 in self.counts.values() and 3 in self.counts.values()

    def three_of_a_kind(self) -> bool:
        return 3 in self.counts.values()

    def two_pair(self) -> bool:
        return self.hand_set_len == 3

    def one_pair(self) -> bool:
        return self.hand_set_len == 4

    # def high_card(self) -> bool:
    #     return self.hand_set_len == 5


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
