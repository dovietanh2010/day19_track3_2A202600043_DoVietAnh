import networkx as nx
import matplotlib.pyplot as plt
import os
import sys

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.graph.neo4j_client import Neo4jClient

def visualize_graph():
    client = Neo4jClient()
    # Fetch all relationships from Neo4j
    query = "MATCH (n)-[r]->(m) RETURN n.name as start, type(r) as rel, m.name as end"
    results = client.query(query)
    
    G = nx.DiGraph()
    for res in results:
        G.add_edge(res["start"], res["end"], label=res["rel"])
    
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=0.5)
    
    nx.draw(G, pos, with_labels=True, node_color='skyblue', 
            node_size=2000, edge_color='gray', linewidths=1, font_size=10)
    
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    plt.title("Knowledge Graph Visualization")
    plt.savefig("graph_visualization.png")
    print("Graph visualization saved to graph_visualization.png")
    plt.show()

if __name__ == "__main__":
    visualize_graph()
