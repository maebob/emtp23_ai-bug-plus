import dgl
import torch
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import pickle

# Read the CSV file and create a DataFrame
df = pd.read_csv('graphs.csv', sep=';')

# get all node ids
node_ids = df['src'].unique().tolist() + df['dst'].unique().tolist()
node_ids = list(set(node_ids))

# Create an empty graph and add nodes
Graph = dgl.DGLGraph()
# Add the nodes to the graph
Graph.add_nodes(len(node_ids))

# Create the node features tensor
node_features = torch.full(
    (Graph.number_of_nodes(), 6), -999, dtype=torch.float)
# Set the node features for the graph
Graph.ndata['features'] = node_features

# Print the first node's feature
print(Graph.ndata['features'])


"""for i, row in df.iterrows():
    if row['src_value'] != "None":
        Graph.ndata[row["src_port"]][row['src'],
                                row['src_port']] = int(row['src_value'])
    if row['dst_value'] != "None":
        Graph.ndata[row['dst_value']][row['dst'],
                                row['dst_port']] = int(row['dst_value'])"""

print(Graph)
"""
# Add the ports to each node the value represents the value at a given port
num_ports = 6
node_features = torch.full(
    (Graph.number_of_nodes(), num_ports), -999, dtype=torch.int)
# Set the node features for the graph
Graph.ndata['features'] = {"Up": node_features[:, 0]}

print(Graph)
print(Graph.ndata['features'][0])"""

# Add edges to the graph with a specific edge type an to and from port
edge_type_map = {'Control': 0, 'Data': 1}
df['edge_type'] = df['edge_type'].map(edge_type_map)
# Map Ports to numbers
port_map = {'Up': 0, 'Down': 1, 'Right': 2, 'Left': 3, 'Out': 4, 'In': 5}
df['src_port'] = df['src_port'].map(port_map)
df['dst_port'] = df['dst_port'].map(port_map)

# Set the node features for the graph
for i, row in df.iterrows():
    if row['src_value'] != "None":
        # Set the node features for the graph
        port_value = int(row['src_value'])
        port_index = int(row["src_port"])
        # Set the value of the port to the value of the node
        Graph.ndata["features"][row['src']][port_index] = port_value

    if row['dst_value'] != "None":
        # Set the node features for the graph
        port_value = int(row['dst_value'])
        port_index = int(row["dst_port"])
        # Set the value of the port to the value of the node
        Graph.ndata["features"][row['dst']][port_index] = port_value

for i, row in df.iterrows():
    edge_data_tensor = torch.tensor([[row['src_port'], row['dst_port'], row['edge_type']]])
    Graph.add_edges(row['src'], row['dst'], data={"edge_features": edge_data_tensor})

print(Graph.ndata)
print(Graph.edata)


#G = Graph.to_networkx()
"""# Get node positions
pos = nx.spring_layout(G)

# Create node labels
node_labels = {}
for node in G.nodes():
    # Add the features to the node labels
    data = {}
    port_list = ['Up', 'Down', 'Right', 'Left', 'Out', 'In']
    for port in port_list:
        if Graph.ndata[port][node] != -999:
            data[port] = int(Graph.ndata[port][node])

    node_labels[node] = f'Node ID: {node}\nFeatures: {data}'

# Create edge labels
edge_labels = {}
for u, v, data in G.edges(data=True):
    # Add the features to the edge labels
    data = {}
    data['src_port'] = int(Graph.edges[u, v].data['src_port'])
    data['dst_port'] = int(Graph.edges[u, v].data['dst_port'])
    data['edge_type'] = int(Graph.edges[u, v].data['edge_type'])
    edge_labels[(u, v)] = f'Edge Features: {data}'"""


"""# Draw graph
nx.draw(G, pos, with_labels=True)
nx.draw_networkx_labels(G, pos, node_labels)
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_color='red')
print(edge_labels)
print(Graph.edata)
# Show plot
plt.show()"""
"""
# Visualize the graph using NetworkX and Matplotlib
pos = nx.kamada_kawai_layout(nx_g)
node_features = nx.get_node_attributes(nx_g, 'features')
edge_features = nx.get_edge_attributes(nx_g, 'edge_type')
nx.draw(nx_g, pos, with_labels=True, node_color=node_features, edge_color=edge_features)
plt.show()

plt.show()"""


"""# Delete one edge 
# store the graph and the deleted edge information in a list
graphs = []
deleted_edges = []


# Get all edges 
all_eids = Graph.edges()

# Convert the tensor to a list for easier iteration
all_eids = list(all_eids)

# Loop through all edge ids
for eid in range(len(all_eids[0])):
    # Get the source and destination node id
    u = all_eids[0][eid]
    v = all_eids[1][eid]
    # Append the edge to the deleted edges list
    deleted_edges.append((u, v, Graph.edges[u, v].data))
    print(Graph)
    # Remove the edge from the graph
    Graph = dgl.remove_edges(Graph, eid)    
    print(Graph)                    
    # Append the graph to the list
    graphs.append(Graph)
    # Add the edge back to the graph
    Graph = dgl.add_edges(Graph, u, v)

# Access the value attribute
print(Graph)

print(len(graphs), len(deleted_edges))
print(deleted_edges[0])"""
# Save the graphs and the edges to a file
# serialize the list to disk
with open('graphs_and_deleted_edges.pickle', 'wb') as f:
    pickle.dump((Graph), f)
