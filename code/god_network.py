import process_corpus
import networkx as nx
import matplotlib.pyplot as plt

ED_kings = process_corpus.ED_kings()
OA_kings = process_corpus.OA_kings()
LagasII_kings = process_corpus.LagasII_kings()
UrIII_kings = process_corpus.UrIII_kings()


def king_god_network(king_dict, filename):
    G = nx.DiGraph()
    for king, deities in king_dict.items():
        for deity in deities:
            G.add_edge(king, deity)

    in_degree_centrality = nx.in_degree_centrality(G)

    # The sizes of the nodes depend on the in-degree centrality of a node, meaning that the amount of directed edges arriving to a node makes the node larger.
    node_sizes = [5000 * in_degree_centrality[node] for node in G] 
    node_colors = ["blue" if G.in_degree(node) == 0 else "green" for node in G]

    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=node_sizes,
        node_color=node_colors,
        edge_color="gray",
        font_size=8,
        font_color="black",)
    plt.savefig(filename)

king_god_network(ED_kings, "../figures/ed_kings.png")
king_god_network(OA_kings, "../figures/oa_kings.png")
king_god_network(LagasII_kings, "../figures/lagasII_kings.png")
king_god_network(UrIII_kings, "../figures/urIII_kings.png")
