def backup_paths(g, path):
    start = path[0]

    results = [[]]
    deep = 0

    if len(g.adj[start]) > 2:
        fork = True
    else:
        fork = False

    path.remove(start)
    visited, queue = path, [(start, [start], deep)]

    while queue:
        (node, search_path, level) = queue.pop(0)
        results.append(search_path)

        if node not in visited:
            visited.append(node)
            adjacent = g.adj[node]

            if fork == True:
                level += 1

            if len(adjacent) > 2:
                fork = True

            for neighbor in adjacent:
                print('ajdacents: {}, level {}'.format(str(neighbor), level))

                if neighbor not in visited and level <= 2:
                    results.append(neighbor)
                    queue.append((neighbor, search_path + [neighbor], level))

    return results
