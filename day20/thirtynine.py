"""
14713
"""

from collections import deque
from math import prod
from typing import Iterable

FLIP = '%'
CONJUNCTION = '&'
START = 'broadcaster'


def construct_graph(modules: Iterable) -> dict:
    """Return dict of all modules adjacency"""
    adjacency = {}
    for module in modules:
        module = module.strip()
        module_name, next_items = (item.strip() for item in module.split('->'))
        module_type = module_name
        if module_name != START:
            module_type = module_name[0]
            module_name = module_name[1:]
        adjacency[module_name] = {
            'type': module_type,
            'state': False if module_type == FLIP else 'low',
            'next': [node.strip() for node in next_items.split(', ')]
        }
    # add default state for conjunctions
    for module, data in adjacency.items():
        if data['type'] == CONJUNCTION:
            data['state'] = {  # mutable, can assign right away
                ancestor: 'low' for ancestor in [
                    key for key, val in adjacency.items() if module in val['next']
                ]
            }

    return adjacency


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        modules = f_in.readlines()

    adjacency = construct_graph(modules)
    # Simulate button push. Could be recursive BFS, I'm going with iterative
    state_count = {'low': 0, 'high': 0}
    for _ in range(1000):  # TODO find loops (then lcm?) or cache results
        queue = deque(tuple([START, node]) for node in adjacency[START]['next'])
        states = deque(['low' for _ in queue])
        # add signal from button to broadcaster and from broadcaster to all adjacent nodes
        state_count['low'] += 1 + len(queue)
        while queue:
            prev_node, node = queue.popleft()
            state = states.popleft()
            if adjacency[node]['type'] == FLIP:
                if state == 'high':
                    continue  # high signal dies at flip-flop
                adjacency[node]['state'] = not adjacency[node]['state']
                if adjacency[node]['state']:
                    state = 'high'
            elif adjacency[node]['type'] == CONJUNCTION:
                # remember incoming signal
                adjacency[node]['state'][prev_node] = state
                state = 'low' if all(state_ == 'high' for state_ in adjacency[node]['state'].values()) else 'high'
            else:
                raise ValueError(f'Unknown type {adjacency[node]["type"]}')

            to_extend = adjacency[node]['next']
            state_count[state] += len(to_extend)
            # print('incrementing state ', state, ' from ', node, ' to ', to_extend)
            queue.extend(tuple([node, item]) for item in to_extend if item in adjacency)
            states.extend([state for item in to_extend if item in adjacency])

    return prod(state_count.values())


if __name__ == '__main__':
    print(main())
