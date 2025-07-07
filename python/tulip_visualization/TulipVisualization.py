from tulip import tlp

from indent_svg import pretty_print_svg
from font_svg import update_font_size
from marker_svg import update_marker_size

from TulipClusterGrouper import TulipClusterGrouper
from utils import *

class TulipVisualization:
    def __init__(self, input, output):
        self._grouper = TulipClusterGrouper()      
        self._input = input
        self._output = output
        self._fontsize = 8
        self._markersize = 10
                
        tlp.initTulipLib()
        tlp.loadPlugins()   
        self._graph = self._import_dot_graph()
        self._process_nodes()
        self._grouper.group_graph(self._graph)
        print_subgraph_hierarchy(self._graph)
        print(has_meta_nodes(self._graph))
        self._set_metanodes()
        print(has_meta_nodes(self._graph))
        print_metagraph(self._graph)
        self._process_edges()                                   
        self._layout_graph()
        self._export_graph()
        self._process_svg()
                  
    def _format_label(self, label):
        return label.replace("<<assembly component>>\n", "").strip('"').strip()              
                  
    def _process_nodes(self):
        size = self._graph.getProperty("viewSize")
        label = self._graph.getProperty("viewLabel")
        border_width = self._graph.getProperty("viewBorderWidth")
        
        for node in self._graph.getNodes():
            label[node] = self._format_label(label[node])
            size[node] = tlp.Size((len(label[node])) * self._fontsize, 5 * self._fontsize, 0)
            border_width[node] = 5.0
            
    def _set_metanodes(self):
        algorithm = "Quotient Clustering"
        params = tlp.getDefaultPluginParameters(algorithm, self._graph)
        params['directed'] = True
        params['use name of subgraph'] = True
        params['recursive'] = True
        params['layout quotient graph(s)'] = True
        params['layout clusters'] = False
        params['edge cardinality'] = True 
        self._graph.applyAlgorithm(algorithm, params)  
            
    def _process_edges(self):
        border_width = self._graph.getProperty("viewBorderWidth")
        color = self._graph.getProperty("viewColor")
        for edge in self._graph.getEdges():
            border_width[edge] = 5.0
            color[edge] = tlp.Color.Gray
             
    def _import_dot_graph(self):
        params = tlp.getDefaultPluginParameters('graphviz')
        params['filename'] = self._input
        return tlp.importGraph('graphviz', params)
      
    def _export_graph(self):
        params = tlp.getDefaultPluginParameters("SVG Export", self._graph)
        params['edge color interpolation'] = False
        params['edge size interpolation'] = False
        params['edge extremities'] = True
        params['no background'] = True
        params['makes SVG output human readable'] = False
        params['export edge labels'] = True
        params['export metanode labels'] = True
        tlp.exportGraph("SVG Export", self._graph, self._output, params)
        
    def _process_svg(self):
        pretty_print_svg(self._output, self._output)
        update_font_size(self._output, self._output, self._fontsize)
        update_marker_size(self._output, self._output, self._markersize)
      
    def style_meta_nodes_light_gray(self, graph):
        viewColor = graph.getColorProperty("viewColor")
        light_gray = tlp.Color(211, 211, 211, 100)
        for node in graph.getNodes():
            if graph.isMetaNode(node):
                viewColor[node] = light_gray            
     
    def _layout_graph(self): 
        algorithm = "Quotient Clustering"
        params = tlp.getDefaultPluginParameters(algorithm, self._graph)
        params['directed'] = True
        params['use name of subgraph'] = True
        params['recursive'] = True
        params['layout quotient graph(s)'] = True
        params['layout clusters'] = False
        params['edge cardinality'] = True 
        self._graph.applyAlgorithm(algorithm, params)                      
        #self.recursive_metagraph(self._graph)