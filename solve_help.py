# library solve
import math

"""
    Contain some functions needed by snowymontreal.py
"""


def is_eulerian_cycle(num_vertices, edges_list, is_oriented, cycle):
    """
    Check whether the given cycle is an eulerian cycle in the given graph
    :param is_oriented:
    :param num_vertices:
    :param edges_list:
    :param cycle:
    :return:
    """

    def consume(begin, end, edges):
        for i in range(len(edges)):
            if begin == edges[i][0] and end == edges[i][1]:
                edges.pop(i)
                return True
            if not is_oriented and begin == edges[i][1] and end == edges[i][0]:
                edges.pop(i)
                return True
        return False

    len_cycle = len(cycle)
    if len(edges_list) != len_cycle:
        return False
    if len(edges_list) == 0:
        return True

    for i in range(len_cycle - 1):
        if not consume(cycle[i], cycle[i + 1], edges_list):
            return False
    if not consume(cycle[len_cycle - 1], cycle[0], edges_list):
        return False
    return edges_list == []


def odd_vertices_undirected(num_vertices, edges_list):
    """
    Check whether the vertices are odd
    :param num_vertices:
    :param edges_list:
    :return: list of odd vertices
    """
    deg = [0] * num_vertices
    for (a, b, _) in edges_list:
        deg[a] += 1
        deg[b] += 1
    return [a for a in range(num_vertices) if deg[a] % 2]

def test_vertices_eulerian(num_vertices, edges_list, is_oriented=False):
    """
    Check whether the vertices comply with an eulerian graph requirements
    if not is_oriented: Only even vertices
    if is_oriented: in_deg equals with out_deg for each vertex
    :param is_oriented:
    :param num_vertices:
    :param edges_list:
    :return: list
    """

    def in_out_deg_directed(num_vertices, edges_list):
        """
        :param num_vertices:
        :param edges_list:
        :return:
        """
        in_deg = [0] * num_vertices
        out_deg = [0] * num_vertices
        for (a, b, _) in edges_list:
            out_deg[a] += 1
            in_deg[b] += 1
        return [a for a in range(num_vertices) if in_deg[a] != out_deg[a]]

    if is_oriented:
        return len(in_out_deg_directed(num_vertices, edges_list)) == 0
    else:
        return len(odd_vertices_undirected(num_vertices, edges_list)) == 0


def is_connected(n, edges, is_oriented=False):
    if n == 0:
        return True
    # Convert to adjacency list
    succ = adjacency_list(n, edges, is_oriented)
    # DFS over the graph
    touched = [False] * n
    touched[0] = True
    todo = [0]
    while todo:
        s = todo.pop()
        for d in succ[s]:
            if not touched[d]:
                touched[d] = True
                todo.append(d)
    somme = sum(touched)
    if somme == n:
        return True
    return False


def is_edge_connected(num_vertices, edges_list, is_oriented=False):
    """
    Check whether is the graph is edge connected.
    A graph is edge connected if all edges can be visited from one
    :param is_oriented:
    :param num_vertices:
    :param edges_list:
    :return: true if the graph is connected, false otherwise
    """
    if num_vertices == 0 or len(edges_list) == 0:
        return True
    succ = adjacency_list(num_vertices, edges_list, is_oriented)
    seen = [False] * num_vertices
    init = edges_list[0][0]  # random vertex
    seen[init] = True
    todo = [init]
    while todo:
        s = todo.pop()
        for d in succ[s]:
            if not seen[d]:
                seen[d] = True
                todo.append(d)
    return all(seen[a] or not succ[a] for a in range(num_vertices))


def adjacency_list(num_vertices, edges_list, is_oriented=False):
    """
    :param num_vertices:
    :param edges_list:
    :param is_oriented:
    :return: adjacency list of the given graph
    """
    succ = [[] for _ in range(num_vertices)]
    for (a, b, _) in edges_list:
        succ[a].append(b)
        if not is_oriented:
            succ[b].append(a)
    return succ


def find_shortest_path(num_vertices, edges_list, src, dst, is_oriented=False):
    if not is_oriented:
        # Classic Bellman-Ford for undirected graphs
        dist = [math.inf] * num_vertices
        dist[src] = 0
        parent = list(range(num_vertices))
        for k in range(num_vertices - 1):
            for (s, d, w) in edges_list:
                if dist[d] > dist[s] + w:
                    parent[d] = (s, w)
                    dist[d] = dist[s] + w
                if not is_oriented and dist[s] > dist[d] + w:
                    parent[s] = (d, w)
                    dist[s] = dist[d] + w

        # src not connected to dst
        if dist[dst] == math.inf:
            return None

        # Extra loop to detect negative cycles
        for (s, d, w) in edges_list:
            if dist[d] > dist[s] + w or (not is_oriented and dist[s] > dist[d] + w):
                return None

        # Build the shortest-path from parents
        # In addition, store the cost
        sp = [(dst, 0)]
        while dst != src:
            dst, cost = parent[dst]
            sp.insert(0, (dst, cost))
        return sp