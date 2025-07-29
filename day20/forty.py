import json
from collections import deque

from thirtynine import construct_graph, FLIP, CONJUNCTION, START

END = 'rx'


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        modules = f_in.readlines()

    adjacency = construct_graph(modules)
    # Simulate button push. Could be recursive BFS, I'm going with iterative
    count = 1
    history = {}
    while True:  # TODO find loops (then lcm?) or cache results
        frozen_dict = hash(json.dumps(adjacency))
        if frozen_dict in history:
            print('loop detected', count)
        else:
            history[frozen_dict] = count
        queue = deque(tuple([START, node]) for node in adjacency[START]['next'])
        states = deque(['low' for _ in queue])
        # add signal from button to broadcaster and from broadcaster to all adjacent nodes
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
            if END in to_extend and state == 'low':
                return count  # TODO this should trigger when SINGLE low pulse reaches rx
            queue.extend(tuple([node, item]) for item in to_extend if item in adjacency)
            states.extend([state for item in to_extend if item in adjacency])
        count += 1
        if count % 1_000_000_000 == 0:
            print(count)


if __name__ == '__main__':
    print(main())  # 207_652_583_562_007
