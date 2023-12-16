from collections import OrderedDict

from twentynine import hash_alg


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        input_file = f_in.read().strip()

    boxes = {}
    for char_group in input_file.split(','):
        group_split = char_group.split('=')
        mode = '='
        if len(group_split) == 1:
            group_split = char_group.split('-')
            mode = '-'
        prefix, focal_len = group_split

        key = hash_alg(prefix)
        if mode == '-':
            if not boxes.get(key):
                continue
            boxes[key].pop(prefix, None)
        if mode == '=':
            boxes[key] = boxes.get(key, OrderedDict())
            boxes[key][prefix] = int(focal_len)

    total = 0
    # calculate focusing power
    for key, val in boxes.items():
        for count, (_, inner_val) in enumerate(val.items(), start=1):
            total += (key + 1) * inner_val * count

    return total


if __name__ == '__main__':
    print(main())
