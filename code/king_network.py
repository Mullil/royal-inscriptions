
import process_corpus
import networkx as nx
import matplotlib.pyplot as plt

ED_kings = process_corpus.ED_kings()
OA_kings = process_corpus.OA_kings()
LagasII_kings = process_corpus.LagasII_kings()
UrIII_kings = process_corpus.UrIII_kings()

def all_periods(ED, OA, LagasII, UrIII):  # This function draws a network with kings from all periods
    G = nx.DiGraph()
    king_periods = {
        "ED": ED,
        "OA": OA,
        "LagasII": LagasII,
        "UrIII": UrIII
    }
    period_colors = {
        "ED": "red",
        "OA": "blue",
        "LagasII": "green",
        "UrIII": "yellow"
    }
    node_colors = {}
    
    for period, king_dict in king_periods.items():
        for king, deities in king_dict.items():
            node_colors[king] = period_colors[period] # each node has a color representing the period
            for deity in deities:
                G.add_edge(king, deity)

    king_projection = nx.Graph()
    kings = [node for node in G if G.in_degree(node) == 0]

    for i, king1 in enumerate(kings):
        for king2 in kings[i+1:]:
            deities_king1 = set(G.successors(king1))
            deities_king2 = set(G.successors(king2))
            shared_deities = deities_king1 & deities_king2 # intersection of two sets
            if len(shared_deities) >= 2: # if the kings mention two or more common gods they have an edge
                king_projection.add_edge(king1, king2, weight=len(shared_deities)) # The weight of the edge is assigned by the number of shared gods.

    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(king_projection, weight="weight", seed=42)

    node_sizes = [1000 for _ in king_projection.nodes()]
    edge_widths = [king_projection[u][v]["weight"] for u, v in king_projection.edges()]
    node_colors_list = [node_colors[node] for node in king_projection.nodes()]

    nx.draw(
        king_projection,
        pos,
        with_labels=True,
        node_size=node_sizes,
        node_color=node_colors_list,
        width=edge_widths,
        edge_color="gray",
        font_size=10,
    )
    plt.savefig('..figures/kings.png')

all_periods(ED_kings, OA_kings, LagasII_kings, UrIII_kings)


