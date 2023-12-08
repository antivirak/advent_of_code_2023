from thirteen_discriminant import HandType


class JokerHandType(HandType):
    """
    Overrides rank method to account for jokers.
    """
    JOKER = 'J'
    # Replace JOKER with space to have comparable card strengths between classes.
    CARDS = f"{'AKQJT98765432'.replace(JOKER, ' ')}{JOKER}"

    @property
    def rank(self) -> int:
        """Returns rank of hand with all jokers replaced by the most frequent card in hand"""
        if self.hand == self.JOKER * 5:
            return 6  # Edge case for 5 jokers
        counts = {key: val for key, val in self.counts.items() if key != self.JOKER}
        return HandType(self.hand.replace(self.JOKER, max(counts, key=counts.get)), self.bid).rank


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
