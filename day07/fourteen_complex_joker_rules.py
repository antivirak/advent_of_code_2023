"""
To make things a little more interesting, the Elf introduces one additional rule. Now, J cards are jokers - wildcards that can act like whatever card would make the hand the strongest type possible.

To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

J cards can pretend to be whatever card is best for the purpose of determining hand type; for example, QJJQ2 is now considered four of a kind. However, for the purpose of breaking ties between two hands of the same type, J is always treated as J, not the card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

Now, the above example goes very differently:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
32T3K is still the only one pair; it doesn't contain any jokers, so its strength doesn't increase.
KK677 is now the only two pair, making it the second-weakest hand.
T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3, QQQJA gets rank 4, and KTJJT gets rank 5.
With the new joker rule, the total winnings in this example are 5905.

Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?
"""

from typing import Generator

from thirteen import HandType


class JokerHandType(HandType):
    """
    Inherits from HandType and overrides rules methods to account for jokers.
    """
    JOKER = 'J'
    CARDS = f"{'AKQJT98765432'.replace(JOKER, ' ')}{JOKER}"

    @property
    def joker_count(self) -> int:
        return self.counts.get(self.JOKER, 0)

    def strength(self) -> Generator:
        """Generate card strength of each card in hand"""
        for card in self.hand:
            yield 15 - self.CARDS.index(card)

    def _of_a_kind(self, num: int) -> bool:
        """This seems too complex"""
        max_count, second_max, *_ = sorted(self.counts.values(), reverse=True)
        if self.joker_count == max_count:
            return second_max > num - 1 - self.joker_count
        return num - self.joker_count in self.counts.values()

    def five_of_a_kind(self) -> bool:
        return self.hand_set_len < 3

    def four_of_a_kind(self) -> bool:
        return self._of_a_kind(4)

    def full_house(self) -> bool:
        return self.hand_set_len < 4

    def three_of_a_kind(self) -> bool:
        return self._of_a_kind(3)

    def two_pair(self) -> bool:
        return self.hand_set_len < 5

    def one_pair(self) -> bool:
        return True


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        lines = f_in.readlines()

    total = 0
    hands = [JokerHandType(hand, int(bid))
             if JokerHandType.JOKER in hand
             else HandType(hand, int(bid))
             for hand, bid in (line.strip().split() for line in lines)]
    hands.sort()
    for count, hand in enumerate(hands, start=1):
        total += count * hand.bid

    return total


if __name__ == '__main__':
    print(main())
