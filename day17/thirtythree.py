"""
--- 
"""

from itertools import product
from typing import Dict, Self

import pandas as pd


class BeamPath:
    """DFS ray tracing, recursive"""
    def __init__(self, layout: pd.DataFrame) -> None:
        self.layout = layout
        # self.energized_layout = layout.copy()
        self.visited: Dict[tuple, tuple] = {}  # {(row_idx, col_idx): (mode, count_idx))} map to keep track of visited cells

    def __call__(self, offset) -> Self:
        """Calculate beam path from top left corner"""
        self.horizontal(offset, 0, 'right', first_call=True)
        return self

    def horizontal(self, y_idx: int, offset: int, mode: str, first_call=False) -> None:
        """Horizontal ray tracing"""
        row = self.layout.iloc[y_idx, offset:] if mode == 'right' else reversed(self.layout.iloc[y_idx, :offset + 1])
        counts = range(offset, len(row) + offset) if mode == 'right' else reversed(range(offset + 1))
        for count_idx, (count, symbol) in enumerate(zip(counts, row)):
            if self.visited.get((y_idx, count)) == (mode, count_idx):
                return
            self.visited[(y_idx, count)] = (mode, count_idx)
            # self.energized_layout.iat[y_idx, count] = '#'
            if count_idx == 0 and not first_call:
                continue
            if symbol in ('.', '-'):
                continue
            if (symbol == '\\' and mode == 'right') or (symbol == '/' and mode == 'left'):
                self.vertical(count, y_idx, 'down')
                return
            if (symbol == '\\' and mode == 'left') or (symbol == '/' and mode == 'right'):
                self.vertical(count, y_idx, 'up')
                return
            if symbol == '|':
                self.vertical(count, y_idx, 'down')
                self.vertical(count, y_idx, 'up')
                return
            raise ValueError('Unknown symbol')

    # TODO I know the code for vertical and horizontal is almost identical
    # (transposition, I've made similar in previous days), but I'm too lazy to refactor it
    def vertical(self, x_idx: int, offset: int, mode: str, first_call=False) -> None:
        """Vertical ray tracing"""
        row = self.layout.iloc[offset:, x_idx] if mode == 'down' else reversed(self.layout.iloc[:offset + 1, x_idx])
        counts = range(offset, len(row) + offset) if mode == 'down' else reversed(range(offset + 1))
        for count_idx, (count, symbol) in enumerate(zip(counts, row)):
            if self.visited.get((count, x_idx)) == (mode, count_idx):
                return
            self.visited[(count, x_idx)] = (mode, count_idx)
            # self.energized_layout.iat[count, x_idx] = '#'
            if count_idx == 0 and not first_call:
                continue
            if symbol in ('.', '|'):
                continue
            if (symbol == '\\' and mode == 'down') or (symbol == '/' and mode == 'up'):
                self.horizontal(count, x_idx, 'right')
                return
            if (symbol == '\\' and mode == 'up') or (symbol == '/' and mode == 'down'):
                self.horizontal(count, x_idx, 'left')
                return
            if symbol == '-':
                self.horizontal(count, x_idx, 'left')
                self.horizontal(count, x_idx, 'right')
                return
            raise ValueError('Unknown symbol')


# Python program for Dijkstra's single
# source shortest path algorithm. The program is
# for adjacency matrix representation of the graph
class Graph:

    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for _ in range(vertices)]
                    for _ in range(vertices)]

    def printSolution(self, dist):
        print("Vertex \t Distance from Source")
        for node in range(self.V):
            print(node, "\t\t", dist[node])

    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minDistance(self, dist, sptSet):

        # Initialize minimum distance for next node
        min = 1e7

        # Search not nearest vertex not in the
        # shortest path tree
        for v in range(self.V):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v

        return min_index

    # Function that implements Dijkstra's single source
    # shortest path algorithm for a graph represented
    # using adjacency matrix representation
    def dijkstra(self, src):

        dist = [1e7] * self.V
        dist[src] = 0
        sptSet = [False] * self.V

        for _ in range(self.V):

            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # u is always equal to src in first iteration
            u = self.minDistance(dist, sptSet)

            # Put the minimum distance vertex in the
            # shortest path tree
            sptSet[u] = True

            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            for v in range(self.V):
                if (self.graph[u][v] > 0 and
                sptSet[v] == False and
                dist[v] > dist[u] + self.graph[u][v]):
                    dist[v] = dist[u] + self.graph[u][v]

        self.printSolution(dist)


# TODO dataclass
class Vertex:
    def __init__(self, node: tuple, last_direction: str, distance: int):
        self.node = node
        self.last_direction = last_direction
        self.distance = distance


class Graph:
    # example of adjacency list (or rather map)
    # adjacency_list = {
    # 'A': [('B', 1), ('C', 3), ('D', 7)],
    # 'B': [('D', 5)],
    # 'C': [('D', 12)]
    # }

    def __init__(self, adjacency_list, layout):
        self.adjacency_list = adjacency_list
        self.layout = layout
        self.stop_node = None

    def get_neighbors(self, v):
        if v.distance == 3:
            return self.adjacency_list[v.node]
        return self.adjacency_list[v.node]

    # heuristic function with equal values for all nodes
    def h(self, n):
        # H = {
        #     'A': 1,
        #     'B': 1,
        #     'C': 1,
        #     'D': 1
        # }
        # return H[n]
        # TODO should work with Manhattan distance
        return abs(n[0] - self.stop_node[0]) + abs(n[1] - self.stop_node[1])
        return 0
        return int(self.layout.iloc[*n])
        return {key: val for key, val in self.adjacency_list[n]}

    def a_star_algorithm(self, start_node, stop_node):
        # open_list is a list of nodes which have been visited, but who's neighbors
        # haven't all been inspected, starts off with the start node
        # closed_list is a list of nodes which have been visited
        # and who's neighbors have been inspected
        self.stop_node = stop_node
        start_node = Vertex(start_node, '', 0)
        open_list = set([start_node])
        closed_list = set()

        # g contains current distances from start_node to all other nodes
        # the default value (if it's not found in the map) is +infinity
        g = {}

        g[start_node.node] = 0

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[start_node.node] = start_node

        while len(open_list) > 0:
            n = None

            # find a node with the lowest value of f() - evaluation function
            for v in open_list:
                if n is None or g[v.node] + self.h(v.node) < g[n.node] + self.h(n.node):
                    n = v;

            if n is None:
                print('Path does not exist!')
                return None

            # if the current node is the stop_node
            # then we begin reconstructin the path from it to the start_node
            if n.node == stop_node:
                reconst_path = []

                while parents[n.node] != n:
                    reconst_path.append(n.node)
                    n = parents[n.node]

                reconst_path.append(start_node.node)

                reconst_path.reverse()

                # print('Path found: {}'.format(reconst_path))
                return reconst_path

            # for all neighbors of the current node do
            for direction_int, (m, weight) in enumerate(self.get_neighbors(n)):
                if m is None:
                    continue
                # if the current node isn't in both open_list and closed_list
                # add it to open_list and note n as it's parent
                if m not in open_list and m not in closed_list:
                    open_list.add(Vertex(m, direction_int, 0))
                    n.last_direction = direction_int
                    parents[m] = n
                    g[m] = g[n.node] + weight
                    continue

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                if not (g[m] > g[n] + weight):
                    continue
                last_direction = n.last_direction
                g[m] = g[n] + weight
                parents[m] = n

                if m in closed_list:
                    closed_list.remove(m)
                    open_list.add(m)

            # remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None


class Graph:
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)
        
    def construct_graph(self, nodes, init_graph):
        """
        This method makes sure that the graph is symmetrical.
        In other words, if there's a path from node A to B with a value V,
        there needs to be a path from node B to node A with a value V.
        """
        graph = {}
        for node in nodes:
            graph[node] = {}
        
        graph.update(init_graph)
        
        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value
                    
        return graph
    
    def get_nodes(self):
        """Returns the nodes of the graph."""
        return self.nodes
    
    def get_outgoing_edges(self, node):
        """Returns the neighbors of a node."""
        connections = []
        last_dir = node[1]
        length = node[2]
        node = node[0]
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False):
                if last_dir == out_node[1]:
                    if length == 3:
                        continue
                    connections.append(tuple([out_node[0], out_node[1], out_node[2] + 1]))
                else:
                    connections.append(out_node)
        return connections
    
    def value(self, node1, node2):
        """Returns the value of an edge between two nodes."""
        return self.graph[node1][node2][0]


def dijkstra_algorithm(graph: Graph, start_node):
    unvisited_nodes = list(graph.get_nodes())
 
    # We'll use this dict to save the cost of visiting each node and update it as we move along the graph   
    shortest_path = {}
 
    # We'll use this dict to save the shortest known path to a node found so far
    previous_nodes = {}
 
    # We'll use max_value to initialize the "infinity" value of the unvisited nodes   
    max_value = 1e7  # float('inf')
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    # However, we initialize the starting node's value with 0   
    shortest_path[start_node] = 0
    
    # The algorithm executes until we visit all nodes
    while unvisited_nodes:
        # The code block below finds the node with the lowest score
        current_min_node = None
        for node in unvisited_nodes:  # Iterate over the nodes
            if current_min_node is None or shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node
                
        # The code block below retrieves the current node's neighbors and updates their distances
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node
 
        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)
    
    return previous_nodes, shortest_path


def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node
    
    while node != start_node:
        path.append(node)
        node = previous_nodes[node]
 
    # Add the start node manually
    path.append(start_node)
    
    print("We found the following best path with a value of {}.".format(shortest_path[target_node]))
    print(list(reversed(path)))
    # print(" -> ".join(reversed(path)))


def main() -> int:
    """main"""
    with open('test_input.txt', 'r') as f_in:
        layout = pd.DataFrame(list(iter(row)) for row in f_in.read().splitlines())

    # # Driver program
    # g = Graph(9)
    # g.graph = [  # Distance matrix between all nodes. Duplicates information, could be reduced
    #     #0,  1, 2,  3,  4,  5, 6,  7, 8
    #     [0,  4, 0,  0,  0,  0, 0,  8, 0],  # 0
    #     [4,  0, 8,  0,  0,  0, 0, 11, 0],  # 1
    #     [0,  8, 0,  7,  0,  4, 0,  0, 2],  # 2
    #     [0,  0, 7,  0,  9, 14, 0,  0, 0],  # 3
    #     [0,  0, 0,  9,  0, 10, 0,  0, 0],  # 4
    #     [0,  0, 4, 14, 10,  0, 2,  0, 0],  # 5
    #     [0,  0, 0,  0,  0,  2, 0,  1, 6],  # 6
    #     [8, 11, 0,  0,  0,  0, 1,  0, 7],  # 7
    #     [0,  0, 2,  0,  0,  0, 6,  7, 0],  # 8
    # ]
    # print(g.dijkstra(0))

    adjacency = {}
    len_x, len_y = layout.shape
    for count, inner_count in product(range(len_x), range(len_y)):
        adjacency[(count, inner_count)] = []
        for loc in (
            [[count, inner_count + 1], 'R'],  # R
            [[count, inner_count - 1], 'L'],  # L
            [[count + 1, inner_count], 'D'],  # D
            [[count - 1, inner_count], 'U'],  # U
        ):
            direction = loc[1]
            loc = loc[0]
            try:
                if loc[0] >= 0 and loc[1] >= 0:
                    adjacency[(count, inner_count)].append(tuple([tuple(loc), int(layout.iloc[*loc]), direction, 0]))
            except IndexError:
                pass
                # adjacency[(count, inner_count)].append(tuple([None, None]))
        # adjacency[(count, inner_count)].append(((count, inner_count - 1), layout.iloc[count, inner_count - 1]))
        # adjacency[(count, inner_count)].append(((count + 1, inner_count), layout.iloc[count + 1, inner_count]))
        # adjacency[(count, inner_count)].append(((count - 1, inner_count), layout.iloc[count - 1, inner_count]))

    # adjacency = {
    #     'A': [('B', 1), ('C', 3), ('D', 7)],
    #     'B': [('D', 5)],
    #     'C': [('D', 12)]
    # }
    # TODO both A* and Dijkstra are capable to solve this. Need to edit the graph.
    # Keep track of the last direction and number of steps already passed this direction on edge.
    from pprint import pprint
    # pprint(adjacency)
    print()
    # graph1 = Graph(adjacency, layout)
    # condition = True
    # path = graph1.a_star_algorithm((0, 0), (len_x - 1, len_y - 1))
    graph = Graph([tuple([node, layout.iloc[*node], '', 0]) for node in adjacency.keys()], {key: {val[0]: tuple([val[1:]]) for val in outer_val} for key, outer_val in adjacency.items()})
    pprint(graph.get_nodes())
    previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=tuple([(0, 0), 2, 'R', 0]))
    print(len(shortest_path))
    # print_result(previous_nodes, shortest_path, ((0, 0), 0, 'R'), (len_x - 1, len_y - 1))

    # pokus o odstraneni rovnych cest. Musime ale upravit graf
    # while condition:
    #     for item1, item2, item3 in zip(path[:-2], path[1:-1], path[2:]):
    #         print(item1, item2, item3)
    #         condition = (
    #                (item1[0] == item2[0]) and (item2[0] == item3[0]) and (item1[1] == item2[1] + 1) and (item2[1] == item3[1] + 1)
    #             or (item1[1] == item2[1]) and (item2[1] == item3[1]) and (item1[0] == item2[0] + 1) and (item2[0] == item3[0] + 1)
    #             or (item1[0] == item2[0]) and (item2[0] == item3[0]) and (item1[1] == item2[1] - 1) and (item2[1] == item3[1] - 1)
    #             or (item1[1] == item2[1]) and (item2[1] == item3[1]) and (item1[0] == item2[0] - 1) and (item2[0] == item3[0] - 1)
    #         )
    #         if condition:
    #             print(True)
    #             # TODO create new graph with the next (4th) vertex in straight line removed
    #             path = graph1.a_star_algorithm(item3, (len_x - 1, len_y - 1))
    #             break

    # return sum(int(layout.iloc[*loc]) for loc in path)


if __name__ == '__main__':
    print(main())
