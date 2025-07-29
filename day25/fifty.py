from fortyeight_graph_viz import count_connected_vertices


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        nodes = {
            line.strip().split(': ')[0]: line.strip().split(': ')[1].split(' ')
            for line in f_in.readlines() if line
        }

    # print input for graphviz
    print('graph = {')
    for node, adjancent in nodes.items():
        adj_new = []
        for adj in adjancent:
            print(f'{node} -- {adj}')
    print('}')

    # Add nodes that are not in nodes keys
    to_add = set()
    for adjancent in nodes.values():
        for adj in adjancent:
            if adj not in nodes:
                to_add.add(adj)

    for node in to_add:
        nodes[node] = []
    # Add the edges from adj back to node
    for node in nodes:
        for key, value in nodes.items():
            if node in value:
                nodes[node].append(key)
                nodes[node] = list(set(nodes[node]))

    # create new graph and remove the 3 edges
    split_graph = nodes.copy()
    for node, adjancent in nodes.items():
        adj_new = []
        for adj in adjancent:
            # I got the edges to remove by examining the input visualization
            if (node == 'bvc' and adj == 'rsm') or (node == 'rsm' and adj == 'bvc'):
                continue
            if (node == 'bkm' and adj == 'ldk') or (node == 'ldk' and adj == 'bkm'):
                continue
            if (node == 'pgh' and adj == 'zmq') or (node == 'zmq' and adj == 'pgh'):
                continue
            adj_new.append(adj)
        split_graph[node] = adj_new

    # calculate number of nodes in each component
    subtotal = count_connected_vertices(split_graph, 'bvc')

    return subtotal * count_connected_vertices(split_graph, 'rsm')


if __name__ == '__main__':
    print(main())
