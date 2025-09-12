class Node:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = None
        self.child = None
        self.left = self
        self.right = self
        self.mark = False

def create_heap():
    return {"min": None, "n": 0}

def insert(heap, key):
    node = Node(key)
    if heap["min"] is None:
        heap["min"] = node
    else:
        # Insert node into root list
        node.right = heap["min"].right
        node.left = heap["min"]
        heap["min"].right.left = node
        heap["min"].right = node

        if node.key < heap["min"].key:
            heap["min"] = node
    heap["n"] += 1

def find_min(heap):
    return heap["min"].key if heap["min"] else None

# Example
heap = create_heap()
for k in [7, 3, 17, 24]:
    insert(heap, k)
print("Minimum key:", find_min(heap))


≠====================



from collections import deque

def bfs(graph, source, sink, parent):
    visited = [False] * len(graph)
    queue = deque([source])
    visited[source] = True

    while queue:
        u = queue.popleft()
        for v, capacity in enumerate(graph[u]):
            if not visited[v] and capacity > 0:
                parent[v] = u
                visited[v] = True
                if v == sink:
                    return True
                queue.append(v)
    return False

def ford_fulkerson(graph, source, sink):
    parent = [-1] * len(graph)
    max_flow = 0

    while bfs(graph, source, sink, parent):
        # Find bottleneck capacity
        path_flow = float("inf")
        s = sink
        while s != source:
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]

        max_flow += path_flow

        # Update residual graph
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = parent[v]

    return max_flow

# Example graph
graph = [
    [0, 16, 13, 0, 0, 0],
    [0, 0, 10, 12, 0, 0],
    [0, 4, 0, 0, 14, 0],
    [0, 0, 9, 0, 0, 20],
    [0, 0, 0, 7, 0, 4],
    [0, 0, 0, 0, 0, 0]
]
print("The maximum possible flow is", ford_fulkerson(graph, 0, 5))



==================================

from collections import deque

def bfs(adj, s, t, parent):
    visited = [False] * len(adj)
    queue = deque([s])
    visited[s] = True

    while queue:
        u = queue.popleft()
        for v, cap in enumerate(adj[u]):
            if not visited[v] and cap > 0:
                parent[v] = u
                visited[v] = True
                if v == t:
                    return True
                queue.append(v)
    return False

def edmonds_karp(adj, names, s, t):
    max_flow = 0
    parent = [-1] * len(adj)

    while bfs(adj, s, t, parent):
        flow = float("inf")
        v = t
        while v != s:
            flow = min(flow, adj[parent[v]][v])
            v = parent[v]
        max_flow += flow

        v = t
        while v != s:
            u = parent[v]
            adj[u][v] -= flow
            adj[v][u] += flow
            v = parent[v]

        # Print path
        path = []
        v = t
        while v != -1:
            path.append(v)
            v = parent[v] if v != s else -1
        print("Path:", " -> ".join(names[i] for i in reversed(path)), ", Flow:", flow)

    return max_flow

# Example usage
n = 6
adj = [[0]*n for _ in range(n)]
names = ['s', 'v1', 'v2', 'v3', 'v4', 't']
edges = [(0,1,3),(0,2,7),(1,3,3),(1,4,4),(2,1,5),(2,4,3),(3,4,3),(3,5,2),(4,5,6)]
for u,v,c in edges:
    adj[u][v] = c

print("The maximum possible flow is", edmonds_karp(adj, names, 0, 5))
