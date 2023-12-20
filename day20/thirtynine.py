"""
--- 
"""

from collections import deque
from math import prod

FLIP = '%'
CONJUNCTION = '&'
START = 'broadcaster'


def main() -> int:
    """main"""
    with open('test_input2.txt', 'r') as f_in:
        modules = f_in.readlines()

    # construct dict of all modules adjacency
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
            'next': [node.strip() for node in next_items.split(', ')]  # reversed if we used LIFO stack, not FIFO queue
        }

    print(adjacency)
    # Simulate button push. Could be some kind of recursive BFS/DFS
    state_count = {'low': 0, 'high': 0}
    # state = 'low'
    for _ in range(1000):  # TODO find loops or cache results
        queue = deque(adjacency[START]['next'].copy())
        states = deque(['low' for _ in queue])
        # visited = set(queue)
        # visited = {node: 0 for node in adjacency.keys()}
        # for node in queue:
        #     visited[node] -= 1
        state_count['low'] += 1 + len(queue)  # or state?
        print('initial state: ', state_count)
        while queue:
            # print(queue)
            node = queue.popleft()
            state = states.popleft()
            # visited.add(node)
            # visited[node] += 1
            if adjacency[node]['type'] == FLIP:
                if state == 'high':
                    continue
                adjacency[node]['state'] = not adjacency[node]['state']
                if adjacency[node]['state']:
                    state = 'high'
            elif adjacency[node]['type'] == CONJUNCTION:
                adjacency[node]['state'] = state
                state = 'high' if state == 'low' else 'low'  # only invertor (1 input) for now
            else:
                raise ValueError(f'Unknown type {adjacency[node]["type"]}')
            state_count[state] += 1
            print('incrementing state ', state, ' from ', node, ' to ', adjacency[node]['next'])
            # to_extend = set(adjacency[node]['next']) - set(key for key, val in visited.items() if val > 0)
            to_extend = adjacency[node]['next']  # set() - visited
            queue.extend(item for item in to_extend if item in adjacency)
            states.extend([state for _ in to_extend])
        print(state_count)
        return prod(state_count.values())

    return prod(state_count.values())


if __name__ == '__main__':
    print(main())
