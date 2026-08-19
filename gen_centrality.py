import os
import sys
from collections import deque
import networkx as nx

if len(sys.argv) < 2:
    print("Usage: python gen_centrality.py <subgraph_name>")
    sys.exit(1)

subgraph_name = sys.argv[1]
elist_path = os.path.join("subgraphs", subgraph_name)
os.makedirs("centralities", exist_ok=True)

G = nx.read_edgelist(elist_path, nodetype=int, create_using=nx.Graph())
nodes = list(G.nodes())
n = len(nodes)

# 1. Closeness
print("Calculating Closeness Centrality...")
closeness = {}
for u in nodes:
    visited = {u: 0}
    queue = deque([u])
    sum_dist = 0
    while queue:
        curr = queue.popleft()
        d = visited[curr]
        for neighbor in G.neighbors(curr):
            if neighbor not in visited:
                visited[neighbor] = d + 1
                sum_dist += d + 1
                queue.append(neighbor)
    closeness[u] = (n - 1) / sum_dist if sum_dist > 0 else 0.0

# 2. Betweenness (Brandes)
print("Calculating Betweenness Centrality...")
betweenness = {u: 0.0 for u in nodes}
for s in nodes:
    S = []
    P = {w: [] for w in nodes}
    sigma = {w: 0 for w in nodes}
    sigma[s] = 1
    d = {w: -1 for w in nodes}
    d[s] = 0
    
    Q = deque([s])
    while Q:
        v = Q.popleft()
        S.append(v)
        for w in G.neighbors(v):
            if d[w] < 0:
                Q.append(w)
                d[w] = d[v] + 1
            if d[w] == d[v] + 1:
                sigma[w] += sigma[v]
                P[w].append(v)
                
    delta = {w: 0.0 for w in nodes}
    while S:
        w = S.pop()
        for v in P[w]:
            delta[v] += (sigma[v] / sigma[w]) * (1.0 + delta[w])
        if w != s:
            betweenness[w] += delta[w]

norm_factor = 1.0 / ((n - 1) * (n - 2)) if n > 2 else 1.0
for u in nodes:
    betweenness[u] *= norm_factor

# 3. Eigenvector
print("Calculating Eigenvector Centrality...")
x = {u: 1.0 / n for u in nodes}
for _ in range(100):
    x_new = {u: sum(x[v] for v in G.neighbors(u)) for u in nodes}
    norm = (sum(val**2 for val in x_new.values())) ** 0.5
    if norm == 0:
        break
    x = {u: val / norm for u, val in x_new.items()}

eigenvector = x

# 4. Biased PageRank
print("Calculating Biased PageRank...")
alpha = 0.8
pref_nodes = [u for u in nodes if u % 3 == 0]
v_pref = {u: (1.0 / len(pref_nodes) if u % 3 == 0 else 0.0) for u in nodes}
pr = {u: 1.0 / n for u in nodes}
degrees = {u: G.degree(u) for u in nodes}

for _ in range(100):
    pr_new = {}
    for u in nodes:
        rank_sum = sum(pr[v] / degrees[v] for v in G.neighbors(u) if degrees[v] > 0)
        pr_new[u] = alpha * rank_sum + (1.0 - alpha) * v_pref[u]
    pr = pr_new

# Save outputs
metrics = [
    ("closeness.txt", closeness),
    ("betweenness.txt", betweenness),
    ("eigenvector.txt", eigenvector),
    ("pagerank.txt", pr)
]

for filename, data in metrics:
    sorted_items = sorted(data.items(), key=lambda item: item[1], reverse=True)
    with open(os.path.join("centralities", filename), "w") as f:
        for node, val in sorted_items:
            f.write(f"{node}\t{round(val, 6):.6f}\n")

print("Task 2 complete.")
