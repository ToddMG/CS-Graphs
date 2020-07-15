from graph import Graph

def earliest_ancestor(ancestors, starting_node):
    tree = Graph()

    for pair in ancestors:
        if pair[0] not in tree.vertices:
            tree.add_vertex(pair[0])
        if pair[1] not in tree.vertices:
            tree.add_vertex(pair[1])

        tree.add_edge(pair[0], pair[1])


    relations = []

    for parent in tree.vertices:
        path = tree.bfs(parent, starting_node)

        if path is not None:
            relations.append(path)

    if len(relations) > 1:

        oldest = relations[0]
        for path in relations:
            if len(path) > len(oldest):
                oldest = path
            if len(path) == len(oldest):
                if path[0] < oldest[0]:
                    oldest = path

        return oldest[0]
    else:
        return -1