import os

os.makedirs("subgraphs", exist_ok=True)

input_file = "cit-HepTh.txt"
output_file = "subgraphs/cite-phy.elist"

kept_edges = 0

with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
    for line in f_in:
        if line.startswith("#") or not line.strip():
            continue

        u_str, v_str = line.strip().split()[:2]
        u, v = int(u_str), int(v_str)

        if u % 2 != 0 and v % 2 != 0:
            f_out.write(f"{u}\t{v}\n")
            kept_edges += 1

print(f"Successfully saved {kept_edges} edges to {output_file}")
