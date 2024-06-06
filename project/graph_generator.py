import random
from typing import List

from project.models import Graph, Vertex

GRAPH_ID = 0


def generate_graph(k: int, no_of_vertices: int) -> Graph:
    vertex_sets = [set() for _ in range(k)]
    for i in range(1, no_of_vertices + 1):
        vertex_sets[random.randint(0, k - 1)].add(Vertex(i, set()))
    for vertex_set in vertex_sets:
        for v1 in vertex_set:
            for vertex_set_2 in vertex_sets:
                if vertex_set_2 is vertex_set:
                    continue
                for v2 in vertex_set_2:
                    edge_probability = random.randint(1, 100) / 100
                    if random.random() < edge_probability:
                        v1.neighbours.add(v2.vertex_id)
                        v2.neighbours.add(v1.vertex_id)

    vertices = [v for vertex_set in vertex_sets for v in vertex_set]
    random.shuffle(vertices)
    global GRAPH_ID
    GRAPH_ID += 1
    return Graph(GRAPH_ID, k, vertices)


def generate_graphs(k: int, no_of_graphs: int, no_of_vertices: int) -> List[Graph]:
    global GRAPH_ID
    GRAPH_ID = 0
    return [generate_graph(k, no_of_vertices) for _ in range(no_of_graphs)]
