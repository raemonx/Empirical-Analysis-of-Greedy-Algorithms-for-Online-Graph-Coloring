import base64
import io
import math
import random
from typing import Dict, Set, List

import matplotlib.pyplot as plt
import networkx as nx


class Vertex:
    vertex_id: int = 0
    neighbours: Set[int] = set()

    def __init__(self, vertex_id: int, neighbours: Set[int]):
        self.vertex_id = vertex_id
        self.neighbours = neighbours


class Graph:
    graph_id: int = 0
    chromatic_number: int = 0
    vertices: List[Vertex] = []

    def __init__(self, graph_id: int, chromatic_number: int, vertices: List[Vertex]):
        self.graph_id = graph_id
        self.chromatic_number = chromatic_number
        self.vertices = vertices


class GraphOutputs:
    graph: Graph
    vertex_to_color: Dict[int, int] = dict()

    def __init__(self, graph: Graph, vertex_to_color: Dict[int, int]):
        self.graph = graph
        self.vertex_to_color = vertex_to_color

    def get_color_count(self):
        return len({color for color in self.vertex_to_color.values()})

    def get_competitive_ratio(self) -> float:
        return self.get_color_count() / self.graph.chromatic_number

    def draw(self):
        vertex_id_to_index = {v.vertex_id: idx for idx, v in enumerate(self.graph.vertices)}
        index_to_color = {idx: self.vertex_to_color[v.vertex_id] for idx, v in enumerate(self.graph.vertices)}

        # Create an undirected graph
        G = nx.Graph()

        # Add nodes to the graph with assigned colors
        for vertex in self.graph.vertices:
            G.add_node(vertex_id_to_index[vertex.vertex_id], color=self.vertex_to_color[vertex.vertex_id])

        # Add edges between adjacent vertices
        for vertex in self.graph.vertices:
            for neighbour in vertex.neighbours:
                G.add_edge(vertex_id_to_index[vertex.vertex_id], vertex_id_to_index[neighbour])

        cmap = plt.cm.get_cmap("Set3", self.get_color_count())

        # Draw the graph with grid layout
        n = int(math.sqrt(len(G.nodes)))
        pos = {node: (node % n, n - node // n - 1) for node in G.nodes()}
        node_colors = [G.nodes[v]['color'] for v in G.nodes]

        # Set the figure size to be wider
        fig, ax = plt.subplots(figsize=(15, 6))
        nx.draw(G, pos, node_color=node_colors, cmap=cmap, with_labels=True, font_weight='bold', ax=ax)

        # Add text labels to each node
        for node_id, coords in pos.items():
            x, y = coords
            label = f"\nColor: {index_to_color[node_id]}"
            plt.text(x, y, label, ha='center', va='top', fontsize=10)

        # Convert the PNG image to a binary string
        img_data = io.BytesIO()
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

        # f"{vertex_id_to_index[vertex.vertex_id]}/{self.vertex_to_color[vertex.vertex_id]}"
        plt.savefig(img_data, format='png')
        img_data.seek(0)
        img_binary = base64.b64encode(img_data.getvalue()).decode()

        plt.clf()
        return img_binary

