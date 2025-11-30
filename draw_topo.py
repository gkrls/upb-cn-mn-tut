from mininet.topo import Topo
import matplotlib.pyplot as plt
import networkx as nx

def draw_topology(topo):
    """
    topo: a Mininet Topo instance
    """
    g = nx.Graph()

    # Hosts and switches are just names
    hosts = topo.hosts()        # ['h1', 'h2', ...]
    switches = topo.switches()  # ['s1', 's2', ...]

    for h in hosts: g.add_node(h, type='host')
    for s in switches: g.add_node(s, type='switch')
    for n1, n2, info in topo.links(withInfo=True): g.add_edge(n1, n2)

    # Layout
    pos = nx.spring_layout(g)

    # Draw
    nx.draw_networkx_nodes(g, pos, nodelist=hosts, node_shape='o', node_color='lightblue')
    nx.draw_networkx_nodes(g, pos, nodelist=switches, node_shape='s', node_color='orange')
    nx.draw_networkx_edges(g, pos)
    nx.draw_networkx_labels(g, pos)
    plt.axis('off')
    plt.show()

import topo
draw_topology(topo.topos['star']())