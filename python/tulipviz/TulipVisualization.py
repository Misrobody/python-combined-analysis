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
        self._boxes = {}
                
        tlp.initTulipLib()
        tlp.loadPlugins()   
        self._graph = self._import_dot_graph()
        self._process_nodes()
        self._process_edges()
        self._grouper.group_graph(self._graph) 
        self._grouper.print_nodes()                             
       
        print_subgraph_hierarchy(self._graph, nodes=False) 
      
        self._alt = self._graph.getLayoutProperty("altLayout")
        self._view = self._graph.getLayoutProperty("viewLayout")
        
        self._layout_graph()  
        
        self._export_graph()
        self._process_svg()
        
        print(self._boxes)
        
        #print_node_properties(self._graph)
        #print_graph_properties(self._graph)
        #print_graph_property(self._graph, "altLayout")
        print_node_properties(self._graph, node_index=3)
        
                  
    def _format_label(self, label):
        return label.replace("<<assembly component>>\n", "").strip('"').strip()              
                  
    def _process_nodes(self):
        size = self._graph.getProperty("viewSize")
        label = self._graph.getProperty("viewLabel")
        border_width = self._graph.getProperty("viewBorderWidth")
        shape = self._graph.getIntegerProperty('viewShape')
        
        for node in self._graph.getNodes():
            label[node] = self._format_label(label[node])
            size[node] = tlp.Size((len(label[node])) * self._fontsize, 5 * self._fontsize, 0)
            border_width[node] = 5.0
            shape[node] = tlp.NodeShape.Square
                     
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
          
    def _bounding_box(self, subgraph):
        box_node = bounding_box(self._graph, subgraph)
        self._boxes[subgraph] = box_node
        #self._graph.addNode(box_node)
        if subgraph.getSuperGraph() != subgraph:
            subgraph.getSuperGraph().addNode(box_node)
        
    def _bottom_up(self, graph):
        subgraphs = graph.getSubGraphs()
        subgraph_list = []
        while subgraphs.hasNext():
            subgraph_list.append(subgraphs.next())

        for subgraph in subgraph_list:
            self._bottom_up(subgraph)

        #print(len(list(graph.getNodes())))
        self._fm3(graph, self._alt)
        self._fast_overlap_removal(graph, self._alt)
        
        direct_children = self._grouper.direct_nodes(graph)
        for n in direct_children:
            self._view[n] = self._alt[n]
            
        for s in subgraph_list:
            #print(s)
            if s in self._boxes.keys():
                box = self._boxes[s]
                #print(self._view[box])
                #print(self._alt[box])
                diff = self._alt[box] - self._view[box]
                #print(diff)
                self._view[box] = self._alt[box]
                for n in s.getNodes():
                    self._view[n] += diff
                       
        if graph.getSuperGraph() != graph:     
            self._bounding_box(graph)
     
    def _layout_graph(self): 
        #g = get_subgraph(self._graph, 6)
        #self._graph.addNode()
        #self._fm3(g)
        #self._bounding_box(g)
        self._bottom_up(self._graph)
        self._curve_edges(self._graph)
        self._edge_bundling(self._graph)
        
           
    def _fm3(self, graph, property):
        params = tlp.getDefaultPluginParameters('FM^3 (OGDF)', graph)
        # params['edge length property'] = ...
        # params['node size'] = ...
        # params['unit edge length'] = ...
        params['new initial layout'] = False
        # params['fixed iterations'] = ...
        # params['threshold'] = ...
        # params['page format'] = ...
        # params['quality vs speed'] = ...
        # params['edge length measurement'] = ...
        # params['allowed positions'] = ...
        # params['tip over'] = ...
        # params['presort'] = ...
        # params['galaxy choice'] = ...
        # params['max iterations change'] = ...
        # params['initial layout'] = ...
        # params['force model'] = ...
        # params['repulsive force method'] = ...
        # params['initial layout forces'] = ...
        # params['reduced tree construction'] = ...
        # params['smallest cell finding'] = ...
        # graph.applyLayoutAlgorithm('FM^3 (OGDF)', params)

        graph.applyLayoutAlgorithm('FM^3 (OGDF)', property, params)
        print(f"layed out {graph.getName()}")
        
    def _fast_overlap_removal(self, graph, property):
        algorithm = "Fast Overlap Removal"
        params = tlp.getDefaultPluginParameters(algorithm, graph)
        params["initial layout"] = property
        params["x border"] = 10
        params["y border"] = 10
        graph.applyLayoutAlgorithm(algorithm, property, params)
        print(f"layed out {graph.getName()}")
        
    def _edge_bundling(self, graph):
        algorithm = "Edge bundling"
        params = tlp.getDefaultPluginParameters(algorithm, graph)
        graph.applyAlgorithm(algorithm, params)
        print(f"layed out {graph.getName()}")
        
    def _curve_edges(self, graph):
        algorithm = "Curve edges"
        params = tlp.getDefaultPluginParameters(algorithm, graph)
        graph.applyAlgorithm(algorithm, params)
        print(f"layed out {graph.getName()}")      