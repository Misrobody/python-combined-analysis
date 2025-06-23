import pydot, sys, re
from indent_dot import indent_dot
from termcolor import colored

class ContainedGraph:
    def __init__(self, input_file, color="#ffffff", colordiff=-15):
        self._graph = pydot.graph_from_dot_file(input_file)[0]
        self._nodes = self._graph.get_nodes()
        self._clusters = {}
        self._outgraph = pydot.Dot("GroupedGraph", graph_type="digraph", rankdir="LR")
        #self._outgraph.set('clusterrank', 'local')
        #self._outgraph.set_overlap("false")
        #self._outgraph.set_splines("true")
        #self._outgraph.set_sep("+30")  # spacing between clusters
        #self._outgraph.set_nodesep("0.5")
        #self._outgraph.set_ranksep("1.2 equally")  # vertical spacing
        self._colordiff = colordiff
        self._color = color
        self.group_clusters()
        self.add_edges()

    def group_clusters(self):

        for node in self._nodes:
            print("-----------")           
            l = (node.get_label() or "").replace("<<assembly component>>\npyparse.", "").strip("")
            
        

            node.set_label(l)
            name = node.get_name().strip('"')
            parts = name.split(".")
            if name == "node" or name == "edge":
                self._outgraph.add_node(node)
                continue
                   
            print(name)
            for i in range(len(parts) - 1):
                curpart = ".".join(parts[:i+1])
                print("cur: " + curpart)
                if curpart not in self._clusters:
                    level = i + 1
                    color = self.adjust_hex_color(self._color, self._colordiff * level)

                    cluster = pydot.Cluster(
                        curpart,
                        label=curpart,
                        style="filled",
                        color="black",
                        fillcolor=color,
                        fontsize="20"
                    )
                    print(colored("created: " + cluster.get_label(), "red"))
                    #cluster.set_graph_defaults(margin="20,20")
                    self._clusters[curpart] = cluster
                    parent_name = ".".join(parts[:i])
                    print(parent_name)
                    parent = self._clusters.get(parent_name, self._outgraph)
                    parent.add_subgraph(cluster)
                
            node_key = ".".join(parts[:-1])
            parent = self._clusters.get(node_key, self._outgraph)
            parent.add_node(node)
        #print(self._outgraph.get_subgraphs()[0].get_name())
        for cluster in self._clusters.values():
            #print(cluster.get_name())
            self._outgraph.add_subgraph(cluster)

    def add_edges(self):
        for edge in self._graph.get_edges():
            src = edge.get_source().strip('"')
            dst = edge.get_destination().strip('"')
            attrs = edge.get_attributes()
            #self._outgraph.add_edge(pydot.Edge(src, dst, **attrs, color="black", style="solid"))
            self._outgraph.add_edge(edge)

    def export(self):
        self._outgraph.write("bin/output.dot")
        indent_dot("bin/output.dot")
        #self._outgraph.write_pdf("bin/output.pdf")

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
    if len(sys.argv) < 2:
        print("Usage: python3 table.py <input.dot>")
        sys.exit(1)

    c = ContainedGraph(sys.argv[1])
    c.export()
