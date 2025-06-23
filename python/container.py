import pydot, sys
from indent_dot import indent_dot
from termcolor import colored

class ContainedGraph:
    def __init__(self, input_file, output_file, color="#ffffff", colordiff=-15):
        self._graph = pydot.graph_from_dot_file(input_file)[0]
        self._nodes = self._graph.get_nodes()
        self._clusters = {}
        self._outgraph = pydot.Dot("GroupedGraph", graph_type="digraph")
        self._outgraph.set('clusterrank', 'local')
        self._outgraph.set_overlap("prism")
        self._outgraph.set_splines("true")
        self._outgraph.set_sep("+15")
        self._outgraph.set_nodesep("0.5")
        self._outgraph.set_ranksep("1.2 equally")
        self._outgraph.set_concentrate("true")
        self._colordiff = colordiff
        self._color = color
        self.group_clusters()
        self.add_edges()
        
        self._output_file = output_file

    def group_clusters(self):
        for node in self._nodes:   
            l = (node.get_label() or "").replace("<<assembly component>>\npyparse.", "").strip('"').strip()
            node.set_label(l)
            name = node.get_name().strip('"')
            parts = name.split(".")
                   
            for i in range(len(parts) - 1):
                curpart = ".".join(parts[:i+1])
                if curpart not in self._clusters:
                    level = i + 1
                    color = self.adjust_hex_color(self._color, self._colordiff * level)
                    cluster = pydot.Cluster(
                        curpart,
                        label=curpart,
                        style="filled",
                        color="black",
                        fillcolor=color,
                        fontsize="20",
                        rank="same"
                    )
                    cluster.set_graph_defaults(margin="20,20")
                    self._clusters[curpart] = cluster
                    parent_name = ".".join(parts[:i])                   
                    parent = self._clusters.get(parent_name, self._outgraph)
                    parent.add_subgraph(cluster)              
            node_key = ".".join(parts[:-1])
            parent = self._clusters.get(node_key, self._outgraph)
            if name != "":            
                parent.add_node(node)

    """
    def add_edges(self):
        for edge in self._graph.get_edges():           
            self._outgraph.add_edge(edge)
    """
    
    def add_edges(self):
        node_to_cluster = {}

        # Map each node name to the cluster (subgraph) it belongs to
        for cluster_name, cluster in self._clusters.items():
            for node in cluster.get_nodes():
                node_name = node.get_name().strip('"')
                node_to_cluster[node_name] = cluster.get_name()

        # Reconstruct edges using cluster heads and tails if applicable
        for edge in self._graph.get_edges():
            src = edge.get_source().strip('"')
            dst = edge.get_destination().strip('"')

            new_edge = pydot.Edge(src, dst)

            # Set ltail and lhead if nodes are inside clusters
            if src in node_to_cluster:
                new_edge.set_ltail(f"cluster_{node_to_cluster[src]}")
            if dst in node_to_cluster:
                new_edge.set_lhead(f"cluster_{node_to_cluster[dst]}")

            # Copy styling attributes
            if edge.get_label():
                new_edge.set_label(edge.get_label())
            if edge.get_style():
                new_edge.set_style(edge.get_style())
            if edge.get_color():
                new_edge.set_color(edge.get_color())

            self._outgraph.add_edge(new_edge)


    def export(self):
        self._outgraph.write(self._output_file)
        indent_dot(self._output_file)

    def adjust_hex_color(self, hex_color, offset):
        if not hex_color.startswith('#') or len(hex_color) != 7:
            raise ValueError("Color must be in format '#RRGGBB'")

        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)

        r_new = max(0, min(255, r + offset))
        g_new = max(0, min(255, g + offset))
        b_new = max(0, min(255, b + offset))

        return f'#{r_new:02X}{g_new:02X}{b_new:02X}'

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 table.py <input.dot> <output-name>")
        sys.exit(1)

    c = ContainedGraph(sys.argv[1], sys.argv[2])
    c.export()



