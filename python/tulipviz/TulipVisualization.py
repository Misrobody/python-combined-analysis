from tulip import tlp
from TulipClusterGrouper import TulipClusterGrouper
from utils import *

class TulipVisualization:
    def __init__(self, input, output):
        self._grouper = TulipClusterGrouper()      
        self._input = input
        self._output = output
        self._fontsize = 8
        self._boxes = {}
                
        tlp.initTulipLib()
        tlp.loadPlugins()  
        
        #import 
        extension = self._input.split(".")[-1]
        if extension == "dot":
            self._graph = self._import_dot_graph()
        elif extension == "graphml":
            self._graph = self._import_graphml_graph()
        else:
            raise Exception("Wrong file type")
        
        # custom global properties
        self._alt = self._graph.getLayoutProperty("altLayout")
        self._bbox = self._graph.getBooleanProperty("isBoundingBox")
          
        # default global properties
        self._view = self._graph.getLayoutProperty("viewLayout")
        self._viewSize = self._graph.getProperty("viewSize")
        self._viewLabel = self._graph.getProperty("viewLabel")
        self._viewBorderWidth = self._graph.getProperty("viewBorderWidth")
        self._viewShape = self._graph.getProperty("viewShape")
        self._viewColor = self._graph.getProperty("viewColor")
        self._externLabel = self._graph.getProperty("externLabel")       
              
        # group graph
        self._style_graph()
        self._grouper.group_graph(self._graph)                          
        
        # layout
        self._bottom_up(self._graph)
        self._curve_edges(self._graph)
        self._edge_bundling(self._graph)
        self.set_bbox_labels(self._graph)
        
        # export
        self._export_graph()
        
    def _import_dot_graph(self):
        params = tlp.getDefaultPluginParameters('graphviz')
        params['filename'] = self._input
        return tlp.importGraph('graphviz', params)
    
    def _import_graphml_graph(self):
        params = tlp.getDefaultPluginParameters('GraphML')
        params['filename'] = self._input
        return tlp.importGraph('GraphML', params)
                  
    def _style_graph(self):
        for node in self._graph.getNodes():
            self._viewLabel[node] = self._viewLabel[node].replace("<<assembly component>>\n", "").strip('"').strip()
            self._viewSize[node] = tlp.Size((len(self._viewLabel[node])) * self._fontsize, 5 * self._fontsize, 0)
            self._viewBorderWidth[node] = 5.0
            self._viewShape[node] = tlp.NodeShape.Square
            if self._viewColor[node] != tlp.Color(255, 192, 255, 255):
                self._viewColor[node] = tlp.Color(255, 255, 255, 255)
    
        for edge in self._graph.getEdges():
            self._viewBorderWidth[edge] = 5.0
            self._viewColor[edge] = tlp.Color.Gray
      
    def _export_graph(self):
        params = tlp.getDefaultPluginParameters("SVG Export", self._graph)
        params['edge color interpolation'] = False
        params['edge size interpolation'] = False
        params['edge extremities'] = True
        params['no background'] = False
        params['makes SVG output human readable'] = False
        params['export edge labels'] = True
        params['export metanode labels'] = True
        tlp.exportGraph("SVG Export", self._graph, self._output, params)
                 
    def _bottom_up(self, graph):
        subgraphs = graph.getSubGraphs()
        subgraph_list = []
        while subgraphs.hasNext():
            subgraph_list.append(subgraphs.next())

        for subgraph in subgraph_list:
            self._bottom_up(subgraph)

        self._fm3(graph, self._alt)
        self._fast_overlap_removal(graph, self._alt)
        
        direct_children = self._grouper.direct_nodes(graph)
        for n in direct_children:
            self._view[n] = self._alt[n]
            
        for s in subgraph_list:
            if s in self._boxes.keys():
                box = self._boxes[s]
                diff = self._alt[box] - self._view[box]
                self._view[box] = self._alt[box]
                for n in s.getNodes():
                    self._view[n] += diff
                       
        if graph.getSuperGraph() != graph:           
            box_node = bounding_box(graph.getSuperGraph(), graph)
            self._boxes[graph] = box_node
            self._bbox[box_node] = True
     
    def set_bbox_labels(self, graph):       
        for node in graph.getNodes():
            if self._bbox[node]:
                label_node = self._graph.addNode()

                self._viewSize[label_node] = tlp.Size((len(self._externLabel[node])) * self._fontsize, 5 * self._fontsize, 0)
                self._viewColor[label_node] = tlp.Color(0, 0, 0, 0)
                self._viewShape[label_node] = tlp.NodeShape.Square
                self._viewLabel[label_node] = self._externLabel[node]
                
                tmp = self._view[node] + tlp.Coord(0, self._viewSize[node][1]/2 - 10, 0)
                self._view[label_node] = tmp
                                
    def _fm3(self, graph, property):
        params = tlp.getDefaultPluginParameters('FM^3 (OGDF)', graph)
        params['new initial layout'] = False
        graph.applyLayoutAlgorithm('FM^3 (OGDF)', property, params)
        
    def _fast_overlap_removal(self, graph, property):
        algorithm = "Fast Overlap Removal"
        params = tlp.getDefaultPluginParameters(algorithm, graph)
        params["initial layout"] = property
        params["x border"] = 10
        params["y border"] = 10
        graph.applyLayoutAlgorithm(algorithm, property, params)
        
    def _edge_bundling(self, graph):
        algorithm = "Edge bundling"
        params = tlp.getDefaultPluginParameters(algorithm, graph)
        graph.applyAlgorithm(algorithm, params)
        
    def _curve_edges(self, graph):
        algorithm = "Curve edges"
        params = tlp.getDefaultPluginParameters(algorithm, graph)
        graph.applyAlgorithm(algorithm, params)    