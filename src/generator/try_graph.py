import dgl
import torch
import pandas as pd

# Read the CSV file and create a DataFrame
df = pd.read_csv('/Users/aaronsteiner/Documents/GitHub/BugPlusEngine/graphs_test.csv', sep=';')

print(df)

# Create an empty graph
G = dgl.graph((df['src'], df['dst']))

# Add edges to the graph with a specific edge type
G.edata['edge_type'] = torch.tensor(df['edge_type'])

# Add value attribute to Up, Down, and Out nodes
for i, row in df.iterrows():
    if row['src_port'] in ['UP', 'DOWN', 'OUT']:
        G.nodes[row['src']].data['value'] = row['value']
    if row['dst_port'] in ['UP', 'DOWN', 'OUT']:
        G.nodes[row['dst']].data['value'] = row['value']

# Access the value attribute
print(G.nodes[1].data['value'])
