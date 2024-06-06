from project.models import GraphOutputs, Graph


def execute_first_fit(g: Graph) -> GraphOutputs:
    graph = {}
    colors = {}
    for v in g.vertices:
        node = v.vertex_id
        if node not in graph:
            graph[node] = set()
        for neighbour in v.neighbours:
            if neighbour in graph:
                graph[node].add(neighbour)
                graph[neighbour].add(node)

        banned = {colors[neighbour] for neighbour in graph[node]}
        color = 1
        while color in banned:
            color += 1
        colors[node] = color

    return GraphOutputs(g, colors)
