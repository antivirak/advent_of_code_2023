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
    with open('input.txt', 'r') as f_in:
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
            'next': [node.strip() for node in next_items.split(', ')]
        }
    #for module, data in adjacency.items():
    #    if len(set(data['next'])) != len(data['next']):
    #        raise ValueError(f'Node {module} has duplicate next nodes')
    for module, data in adjacency.items():
        if data['type'] == CONJUNCTION:
            adjacency[module]['state'] = {
                ancestor: 'low' for ancestor in [
                    key for key, val in adjacency.items() if module in val['next']
                ]  # if ancestor != START
            }

    from pprint import pprint
    pprint(adjacency)
    # Simulate button push. Could be recursive BFS
    state_count = {'low': 0, 'high': 0}
    # state = 'low'
    for _ in range(1000):  # TODO find loops (then lcm?) or cache results
        queue = deque(tuple([START, node]) for node in adjacency[START]['next'])
        states = deque(['low' for _ in queue])
        # visited = set(queue)
        # visited = {node: 0 for node in adjacency.keys()}
        # for node in queue:
        #     visited[node] -= 1
        state_count['low'] += 1 + len(queue)
        # print('initial state: ', state_count)
        while queue:
            # print(queue)
            prev_node, node = queue.popleft()
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
                adjacency[node]['state'][prev_node] = state
                # print(adjacency[node]['state'])
                state = 'low' if all(state_ == 'high' for state_ in adjacency[node]['state'].values()) else 'high'
                # print(state)
            else:
                raise ValueError(f'Unknown type {adjacency[node]["type"]}')
            to_extend = adjacency[node]['next']  # set() - visited
            state_count[state] += len(to_extend)
            print('incrementing state ', state, ' from ', node, ' to ', adjacency[node]['next'])
            # to_extend = set(adjacency[node]['next']) - set(key for key, val in visited.items() if val > 0)
            queue.extend(tuple([node, item]) for item in to_extend if item in adjacency)
            states.extend([state for _ in to_extend])
            # for next_ in adjacency[node]['next']:
            #     if adjacency.get(next_, {}).get('type') == CONJUNCTION:
            #         adjacency[next_]['state'][node] = state  # TODO still does not work. Add "time" sync?
        #break
        #print(state_count)
        #if _ == 4:
        #    return prod(state_count.values())

    return prod(state_count.values())  # 688623195 too low
    #                                    688580648


if __name__ == '__main__':
    print(main())
