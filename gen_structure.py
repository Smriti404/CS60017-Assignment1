import os
import sys
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

if len(sys.argv) < 2:
    print("Usage: python gen_structure.py <subgraph_name>")
    sys.exit(1)

subgraph_name = sys.argv[1]
elist_path = os.path.join("subgraphs", subgraph_name)
os.makedirs("plots", exist_ok=True)

G = nx.read_edgelist(elist_path, nodetype=int, create_using=nx.Graph())

# 1. Size
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
print(f"Number of nodes:{num_nodes}")
print(f"Number of edges:{num_edges}")

# 2. Degree Analysis
degrees = dict(G.degree())
max_degree = max(degrees.values())
max_deg_nodes = [str(node) for node, deg in degrees.items() if deg == max_degree]
print(f"Node id(s) with highest degree:{','.join(max_deg_nodes)}")

plt.figure()
plt.hist(list(degrees.values()), bins=30, edgecolor="black")
plt.title("Degree Distribution")
plt.xlabel("Degree")
plt.ylabel("Frequency")
plt.savefig(f"plots/deg_dist_{subgraph_name}.png")
plt.close()

# 3. Paths
sample_sizes = [10, 100, 1000]
diameters = []

for sample_size in sample_sizes:
    sampled_nodes = random.sample(list(G.nodes()), min(sample_size, num_nodes))
    max_sp = 0
    for node in sampled_nodes:
        lengths = nx.single_source_shortest_path_length(G, node)
        if lengths:
            max_sp = max(max_sp, max(lengths.values()))
    diameters.append(max_sp)
    print(f"Approximate full diameter by sampling {sample_size} nodes:{max_sp}")

mean_diam = round(float(np.mean(diameters)), 4)
var_diam = round(float(np.var(diameters)), 4)
print(f"Approximate full diameter (mean and variance):{mean_diam}, {var_diam}")

all_paths = []
sample_for_path = random.sample(list(G.nodes()), min(500, num_nodes))
for node in sample_for_path:
    lengths = nx.single_source_shortest_path_length(G, node)
    all_paths.extend(lengths.values())

plt.figure()
plt.hist(all_paths, bins=range(1, max(all_paths) + 2), edgecolor="black")
plt.title("Shortest Path Length Distribution")
plt.xlabel("Path Length")
plt.ylabel("Frequency")
plt.savefig(f"plots/shortest_path_{subgraph_name}.png")
plt.close()

# 4. Components
components = list(nx.connected_components(G))
lcc = max(components, key=len)
frac_lcc = round(len(lcc) / num_nodes, 4)
print(f"Fraction of nodes in largest connected component:{frac_lcc}")

print(f"Number of edge bridges:{len(list(nx.bridges(G)))}")
print(f"Number of articulation points:{len(list(nx.articulation_points(G)))}")

plt.figure()
plt.hist([len(c) for c in components], bins=30, edgecolor="black", log=True)
plt.title("Connected Component Sizes")
plt.xlabel("Component Size")
plt.ylabel("Frequency (log scale)")
plt.savefig(f"plots/connected_comp_{subgraph_name}.png")
plt.close()

# 5. Connectivity & Clustering
print(f"Average clustering coefficient:{round(nx.average_clustering(G), 4)}")

triads_dict = nx.triangles(G)
print(f"Number of triads:{sum(triads_dict.values()) // 3}")

rand_node = random.choice(list(G.nodes()))
print(f"Clustering coefficient of random node {rand_node}:{round(nx.clustering(G, rand_node), 4)}")
print(f"Number of triads random node {rand_node} participates:{triads_dict[rand_node]}")

edges_in_triads = sum(1 for u, v in G.edges() if set(G.neighbors(u)).intersection(set(G.neighbors(v))))
print(f"Number of edges that participate in at least one triad:{edges_in_triads}")

plt.figure()
plt.hist(list(nx.clustering(G).values()), bins=20, edgecolor="black")
plt.title("Clustering Coefficient Distribution")
plt.xlabel("Clustering Coefficient")
plt.ylabel("Frequency")
plt.savefig(f"plots/clustering_coeff_{subgraph_name}.png")
plt.close()
