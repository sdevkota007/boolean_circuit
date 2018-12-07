import itertools
from collections import deque, namedtuple






# we'll use infinity as a default distance to nodes.
inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')
INPUT_FILE = 'inputs/compute2.cir'


def make_edge(start, end, cost=1):
  return Edge(start, end, cost)



def write_to_file(content, filename):
    with open(filename, 'w') as f:
        f.write(content)

def read_from_file(filename):
    with open(filename) as in_file:
        content = in_file.readlines()
    return content

def create_tables(variables):
    n = len(variables)
    # table = list(itertools.product([False, True], repeat=n))
    table = list(itertools.product([1, 2], repeat=n))
    return table


class Graph:
    def __init__(self, edges):
        # let's check that the data is right
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]
        if wrong_edges:
            raise ValueError('Wrong edges data: {}'.format(wrong_edges))

        self.edges = [make_edge(*edge) for edge in edges]

    @property
    def vertices(self):
        return set(
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )

    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs

    def remove_edge(self, n1, n2, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)

    def add_edge(self, n1, n2, cost=1, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.edges.append(Edge(start=n1, end=n2, cost=cost))
        if both_ends:
            self.edges.append(Edge(start=n2, end=n1, cost=cost))

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours

    def dijkstra(self, source, dest):
        assert source in self.vertices, 'Such source node doesn\'t exist'
        distances = {vertex: inf for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()

        while vertices:
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == inf:
                break
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        return path


# # graph = Graph([
# #     ("a", "b", 7),  ("a", "c", 9),  ("a", "f", 14), ("b", "c", 10),
# #     ("b", "d", 15), ("c", "d", 11), ("c", "f", 2),  ("d", "e", 6),
# #     ("e", "f", 9)])

graph = Graph([
    ("1", "2", 1),  ("1", "3", 1),  ("1", "6", 1), ("2", "3", 1),
    ("2", "4", 1), ("3", "4", 1), ("3", "6", 1),  ("4", "5", 1),
    ("5", "6", 1)])
#
print(graph.dijkstra("1", "2"))




lines = read_from_file(INPUT_FILE)
number_of_registers = int(lines[0].strip('\n'))
edges = [x.split() for x in lines[1:]]
print("edges: ", edges)
nodes = set((itertools.chain.from_iterable([[x[1], x[2]] for x in edges])))
print("nodes: ", nodes)
variables = list(set([x[0].replace('!', '') for x in edges]))
print(variables)

# for node in nodes:
#     graph.add_node(str(node))

table = create_tables(variables)
# print(table)


for i, row in enumerate(table):
    # print(row)
    graph_list = []
    for edge in edges:
        variable = edge[0].replace('!', '')
        pos_variable = variables.index(variable)
        # print(pos_variable, edge[0])
        bool_value = row[pos_variable]
        if '!' in edge[0]:

            # bool_value = not bool_value
            # graph.add_edge(edge[1], edge[2], bool_value)
            graph_list.append((edge[1], edge[2], bool_value))
            # print(edge[1], edge[2], bool_value)
        else:
            # graph.add_edge(edge[1], edge[2], bool_value)
            graph_list.append((edge[1], edge[2], bool_value))
            # print(edge[1], edge[2], bool_value)

    print("graph_list: ",graph_list)
    graph = Graph(graph_list)

    print(graph.dijkstra('0', '1'))
