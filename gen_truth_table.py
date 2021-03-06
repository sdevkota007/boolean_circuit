from __future__ import print_function
from collections import defaultdict, deque
import itertools

INPUT_FILE = 'inputs/compute1.cir'

input_files = ['inputs/compute1.cir',
               'inputs/compute2.cir',
               'inputs/compute3.cir',
               'inputs/compute5.cir',
               'inputs/compute4.cir',
               # 'inputs/EXTRA1.cir',
               # 'inputs/EXTRA2.cir'
                ]



class Graph(object):
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance



def write_to_file(content, filename):
    with open(filename, 'w') as f:
        f.write(content)

def read_from_file(filename):
    with open(filename) as in_file:
        content = in_file.readlines()
    return content


def dijkstra(graph, initial):
    visited = {initial: 0}
    path = {}

    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node
        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge in graph.edges[min_node]:
            try:
                weight = current_weight or graph.distances[(min_node, edge)]
            except:
                continue
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    return visited, path


def shortest_path(graph, origin, destination):
    visited, paths = dijkstra(graph, origin)
    full_path = deque()
    _destination = paths[destination]

    while _destination != origin:
        full_path.appendleft(_destination)
        _destination = paths[_destination]

    full_path.appendleft(origin)
    full_path.append(destination)

    return visited[destination], list(full_path)


def create_tables(variables):
    n = len(variables)
    table = list(itertools.product([False, True], repeat=n))
    return table

def main(input_file):
    lines = read_from_file(input_file)
    # number_of_registers = int(lines[0].strip('\n'))
    edges = [x.split() for x in lines[1:]]
    # print("edges: ", edges)
    nodes = set((itertools.chain.from_iterable([[x[1], x[2]] for x in edges])))
    # print("nodes: ", nodes)
    variables = list(set([x[0].replace('!', '') for x in edges]))
    # print(variables)
    content = '\t'.join(variables) + '\n'
    # for node in nodes:
    #     graph.add_node(str(node))

    table = create_tables(variables)

    for i, row in enumerate(table):
        # print(row)
        graph = Graph()
        for node in nodes:
            graph.add_node(str(node))

        for edge in edges:
            variable = edge[0].replace('!', '')
            pos_variable = variables.index(variable)
            # print(pos_variable, edge[0])
            bool_value = row[pos_variable]
            if edge[1] == '1': edge[1], edge[2] = edge[2], edge[1]
            if '!' in edge[0]:
                bool_value = not bool_value
                graph.add_edge(edge[1], edge[2], bool_value)
                # print(edge[1], edge[2], bool_value)
            else:
                graph.add_edge(edge[1], edge[2], bool_value)
                # print(edge[1], edge[2], bool_value)

        output = shortest_path(graph, '0', '1')[0]

        row = [str(int(elem)) for elem in row]
        content += '\t'.join(row) + '\t' + str(int(output)) + '\n'

    output_file = 'outputs/' + input_file.split('/')[1] + '.out'
    print(output_file)
    write_to_file(content, output_file)


if __name__ == '__main__':
    for input_file in input_files:
        main(input_file)