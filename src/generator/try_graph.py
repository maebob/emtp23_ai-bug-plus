import dgl
import torch
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import pickle

# Read the CSV file and create a DataFrame
df = pd.read_csv('graphs.csv', sep=';')

#print(df)
node_ids = df['src'].unique().tolist() + df['dst'].unique().tolist()

# Create an empty graph
G = dgl.DGLGraph()
print(G.edges())

nx_g = G.to_networkx()

# Visualize the graph using NetworkX and Matplotlib
pos = nx.kamada_kawai_layout(nx_g)
nx.draw(nx_g, pos, with_labels=True, node_color='lightblue', edge_color='gray')

plt.show()

# Map "Control" to 0 and "Data" to 1
edge_type_map = {'Control': 0, 'Data': 1}
df['edge_type'] = df['edge_type'].map(edge_type_map)

# Map Ports to numbers
port_map = {'Up': 0, 'Down': 1, 'Right': 2, 'Left': 3, 'Out': 4, 'In': 5}
df['src_port'] = df['src_port'].map(port_map)
df['dst_port'] = df['dst_port'].map(port_map)

print(df)

# Add edges to the graph with a specific edge type
print(df['edge_type'].unique().tolist())
G.edata['edge_type'] = torch.tensor(df['edge_type'].values.tolist())

# Add the 6 ports to each node in the graph as a 2D tensor and fill it with the value None
G.ndata['port'] = torch.full((G.number_of_nodes(), len(port_map)), -999, dtype=torch.int)

# Loop through the DataFrame and set the port values
for i, row in df.iterrows():
    if row['src_value'] != "None":
        G.ndata['port'][row['src'], row['src_port']] = int(row['src_value'])
    if row['dst_value'] != "None":
        G.ndata['port'][row['dst'], row['dst_port']] = int(row['dst_value'])


# Delete one edge 
# store the graph and the deleted edge information in a list
graphs = []
deleted_edges = []


# Get all edges 
all_eids = G.edges()

# Convert the tensor to a list for easier iteration
all_eids = list(all_eids)

# Loop through all edge ids
for eid in range(len(all_eids[0])):
    # Get the source and destination node id
    u = all_eids[0][eid]
    v = all_eids[1][eid]
    # Append the edge to the deleted edges list
    deleted_edges.append((u, v))
    print(G)
    # Remove the edge from the graph
    G = dgl.remove_edges(G, eid)    
    print(G)                    
    # Append the graph to the list
    graphs.append(G)
    # Add the edge back to the graph
    G = dgl.add_edges(G, u, v)

# Access the value attribute
print(G)
# Convert the DGL graph to a NetworkX graph
nx_g = G.to_networkx()

# Visualize the graph using NetworkX and Matplotlib
pos = nx.kamada_kawai_layout(nx_g)
nx.draw(nx_g, pos, with_labels=True, node_color='lightblue', edge_color='gray')

plt.show()
print(len(graphs), len(deleted_edges))
# Save the graphs and the edges to a file
# serialize the list to disk
with open('graphs_and_deleted_edges.pickle', 'wb') as f:
    pickle.dump((graphs, deleted_edges), f)