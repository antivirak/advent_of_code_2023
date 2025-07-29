import json
import heapq

from thirtynine import construct_graph, FLIP, CONJUNCTION, START

END = 'rx'

# TODO try reverse with DP


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        modules = f_in.readlines()

    adjacency = construct_graph(modules)
    # Simulate button push. Could be recursive BFS, I'm going with iterative
    count = 1
    history: dict[str, int] = {}
    while True:  # TODO find loops (then lcm?) or cache results
        frozen_dict = hash(json.dumps(adjacency))
        if frozen_dict in history:
            print('loop detected', count)
        else:
            history[frozen_dict] = count
        queue: list[tuple[int, str, dict, str]] = []
        for node in adjacency[START]['next']:
            # TODO add int as first item in tuple to be the priority
            heapq.heappush(queue, (count, START, node, 'low'))
        # add signal from button to broadcaster and from broadcaster to all adjacent nodes
        while queue:
            _, prev_node, node, state = heapq.heappop(queue)
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
            for item in to_extend:
                if item in adjacency:
                    heapq.heappush(queue, (count, node, item, state))
        count += 1
        if count % 1_000_000_000 == 0:
            print(count)


if __name__ == '__main__':
    print(main())  # 207_652_583_562_007
