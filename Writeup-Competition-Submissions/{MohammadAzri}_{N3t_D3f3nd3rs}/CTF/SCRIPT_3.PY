import itertools

# Input data
edges = [
    ("NodeA", "NodeC", 32324),
    ("NodeB", "NodeA", 26786),
    ("NodeC", "NodeB", 77458),
    ("NodeC", "NodeD", 19905),
    ("NodeC", "NodeG", 19455),
    ("NodeD", "NodeA", 64678),
    ("NodeD", "NodeE", 57878),
    ("NodeE", "NodeF", 29999),
    ("NodeE", "NodeA", 82356),
    ("NodeF", "NodeC", 77777),
    ("NodeF", "NodeA", 33333),
    ("NodeF", "NodeD", 88888),
    ("NodeF", "NodeG", 88888),
    ("NodeG", "NodeA", 1),
]

# Extract unique nodes
nodes = sorted(set(itertools.chain.from_iterable((edge[0], edge[1]) for edge in edges)))
node_indices = {node: idx for idx, node in enumerate(nodes)}

# Initialize adjacency matrix with 0s (no direct connection)
n = len(nodes)
adj_matrix = [[0] * n for _ in range(n)]

# Populate adjacency matrix with direct connections
for src, dst, cost in edges:
    src_idx, dst_idx = node_indices[src], node_indices[dst]
    adj_matrix[src_idx][dst_idx] = 1  # Mark direct connection

# Debugging: Print adjacency matrix
print("Adjacency Matrix:")
for row in adj_matrix:
    print(row)

# Flatten adjacency matrix and format as the flag
flattened_matrix = "".join(map(str, itertools.chain.from_iterable(adj_matrix)))
flag = f"STOUTCTF{{{flattened_matrix}}}"

# Output the flag
print("\nFlag:", flag)
