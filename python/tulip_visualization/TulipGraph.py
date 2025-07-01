from tulip import tlp
import sys

def list_subgraphs(g, indent=0):
    for sg in g.getSubGraphs():
        print("  " * indent + "- " + sg.getName())
        list_subgraphs(sg, indent + 1)

class TulipGraph():
    def __init__(self, input, output):   
        self._input = input
        self._output = output
        self._fontsize = 40
                
        tlp.initTulipLib()
        tlp.loadPlugins()
    
        match self._input.split(".")[-1]:
            case "dot":
                self._graph = self._import_dot_graph()
            case "graphml":
                self._graph = self._import_graphml_graph()
            case _:
                raise Exception("wrong filetype")
            
        self._process_nodes()
        self._process_edges()
        
        list_subgraphs(self._graph, indent=4)
        
        #self._print_edge_properties()
        self._layout_graph()
        self._export_graph()
                  
    def _process_nodes(self):
        size = self._graph.getProperty("viewSize")
        label = self._graph.getProperty("viewLabel")
        border_width = self._graph.getProperty("viewBorderWidth")
        font_size = self._graph.getProperty("viewFontSize")
        for node in self._graph.getNodes():
            label[node] = self._format_label(label[node])
            size[node] = tlp.Size(len(label[node]), 10, 0)
            border_width[node] = 5.0
            font_size[node] = self._fontsize
            
    def _process_edges(self):
        border_width = self._graph.getProperty("viewBorderWidth")
        color = self._graph.getProperty("viewColor")
        for edge in self._graph.getEdges():
            border_width[edge] = 5.0
            color[edge] = (133, 133, 133, 255)
             
    def _import_dot_graph(self):
        params = tlp.getDefaultPluginParameters('graphviz')
        params['filename'] = self._input
        return tlp.importGraph('graphviz', params)
    
    def _import_graphml_graph(self):
        params = tlp.getDefaultPluginParameters('GraphML')
        params['filename'] = self._input
        return tlp.importGraph('GraphML', params)
   
    def _export_graph(self):
        params = tlp.getDefaultPluginParameters("SVG Export", self._graph)
        # set any input parameter value if needed
        params['edge color interpolation'] = False
        params['edge size interpolation'] = False
        params['edge extremities'] = True
        params['no background'] = True
        params['makes SVG output human readable'] = True
        params['export edge labels'] = True
        params['export metanode labels'] = True

                
        tlp.exportGraph("SVG Export", self._graph, self._output, params)
        
    def _layout_graph(self):
        params = tlp.getDefaultPluginParameters('FM^3 (OGDF)', self._graph)
        #params['edge length property'] = self._graph.getSizeProperty("viewSize")
        #params['node size'] = self._graph.getSizeProperty("viewSize")
        params['unit edge length'] = 200
        params['new initial layout'] = False
        params['fixed iterations'] = 10
        params['threshold'] = 2
        params['page format'] = "portrait"
        # params['quality vs speed'] = ...
        params['edge length measurement'] = "midpoint"
        params['allowed positions'] = "all"
        params['tip over'] = "always"
        # params['presort'] = ...
        # params['galaxy choice'] = ...
        # params['max iterations change'] = ...
        # params['initial layout'] = ...
        # params['force model'] = ...
        params['repulsive force method'] = "grid approximation"
        # params['initial layout forces'] = ...
        params['reduced tree construction'] = "path by path"
        #params['smallest cell finding'] =

        resultLayout = self._graph.getLayoutProperty("viewLayout")
        self._graph.applyLayoutAlgorithm('FM^3 (OGDF)', resultLayout, params)
   
    def _format_label(self, label):
        return label.replace("<<assembly component>>\n", "").strip('"').strip()

    def _print_node_properties(self, node_index=0):
        properties = self._graph.getNodePropertiesValues(self._graph.nodes()[node_index])
        max_key_length = max(len(key) for key in properties.getKeys())
        for key in properties.getKeys():
            print(f"{key:<{max_key_length}} : {properties[key]}")
            
    def _print_edge_properties(self, edge_index=0):
        properties = self._graph.getEdgePropertiesValues(self._graph.edges()[edge_index])
        max_key_length = max(len(key) for key in properties.getKeys())
        for key in properties.getKeys():
            print(f"{key:<{max_key_length}} : {properties[key]}")
            
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python render_flat_graph.py <input.dot> <output.svg>")
        sys.exit(1)

    input = sys.argv[1]
    output = sys.argv[2]
    
    graph = TulipGraph(input, output)
    
    


