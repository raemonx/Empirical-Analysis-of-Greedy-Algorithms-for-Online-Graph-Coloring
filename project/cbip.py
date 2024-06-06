from project.models import Graph, GraphOutputs


def execute_cbip(g: Graph) -> GraphOutputs:
    if g.chromatic_number != 2:
        return GraphOutputs(g, {})
    graph = {}
    colors = {}

    for v in g.vertices:
        node = v.vertex_id
        graph[node] = set()
        for neighbour in v.neighbours:
            if neighbour in graph:
                graph[node].add(neighbour)
                graph[neighbour].add(node)

        partitions = [set() for _ in range(0, g.chromatic_number)]
        q_switch = 0
        qs = [[node], []]
        while True:
            current_q = qs[q_switch]
            if not current_q:
                break
            while current_q:
                current_node = current_q.pop(0)
                for current_node_neighbour in graph[current_node]:
                    in_any_partitions = False
                    for partition in partitions:
                        if current_node_neighbour in partition:
                            in_any_partitions = True
                            break
                    if not in_any_partitions:
                        partitions[1 - q_switch].add(current_node_neighbour)
                        qs[1 - q_switch].append(current_node_neighbour)
            q_switch = 1 - q_switch

        banned = {colors[b] for b in partitions[1]}
        color = 1
        while color in banned:
            color += 1
        colors[node] = color

    return GraphOutputs(g, colors)
