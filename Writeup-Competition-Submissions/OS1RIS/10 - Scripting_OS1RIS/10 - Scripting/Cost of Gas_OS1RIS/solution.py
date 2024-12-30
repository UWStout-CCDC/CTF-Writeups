import numpy as np

edges = {
    'A': {'C': 32324},
    'B': {'A': 26786},
    'C': {'B': 77458, 'D': 19905, 'G': 19455},
    'D': {'A': 64678, 'E': 57878},
    'E': {'A': 82356, 'F': 29999},
    'F': {'C': 77777, 'A': 33333, 'D': 88888, 'G': 88888},
    'G': {'A': 1}
}

nodes = list(edges.keys())

n = len(nodes)
distance_matrix = np.full((n, n), float('inf'))

for i in range(n):
    distance_matrix[i][i] = 0

for src in edges:
    for dest in edges[src]:
        distance_matrix[nodes.index(src)][nodes.index(dest)] = edges[src][dest]

for k in range(n):
    for i in range(n):
        for j in range(n):
            if distance_matrix[i][j] > distance_matrix[i][k] + distance_matrix[k][j]:
                distance_matrix[i][j] = distance_matrix[i][k] + distance_matrix[k][j]

output = ""
for i in range(n):
    for j in range(n):
        output += str(int(distance_matrix[i][j]))

result = f"STOUTCTF{{{output}}}"
print(result)
