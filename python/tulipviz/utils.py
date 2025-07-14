from tulip import tlp
      
############### Hierarchy ###############
    
def print_subgraph_hierarchy(graph, indent=0, is_root=True, nodes=False):
    name = graph.getName() or "(unnamed)"
    graph_id = graph.getId()
    num_nodes = graph.numberOfNodes()
    num_edges = graph.numberOfEdges()
    indent_str = "  " * indent

    label = f"{name} [ROOT]" if is_root else name
    print(f"{indent_str}- {label:<40} (ID: {graph_id:>3})  Nodes: {num_nodes:>4}  Edges: {num_edges:>4}")

    if nodes:
        names = graph.getProperty("viewLabel")
        indent_str = "  " * (indent+1)
        for i in graph.getNodes():
            print(f"{indent_str}- {names[i].upper():<40}")

    subgraphs = graph.getSubGraphs()
    while subgraphs.hasNext():
        subgraph = subgraphs.next()
        print_subgraph_hierarchy(subgraph, indent + 1, is_root=False, nodes=nodes)      
                   
############### Properties ###############
    
def print_node_properties(graph, node_index=0):
    properties = graph.getNodePropertiesValues(graph.nodes()[node_index])
    max_key_length = max(len(key) for key in properties.getKeys())
    for key in properties.getKeys():
        print(f"{key:<{max_key_length}} : {properties[key]}")
            
def print_edge_properties(graph, edge_index=0):
    properties = graph.getEdgePropertiesValues(graph.edges()[edge_index])
    max_key_length = max(len(key) for key in properties.getKeys())
    for key in properties.getKeys():
        print(f"{key:<{max_key_length}} : {properties[key]}")
       
def print_graph_properties(graph):
    property_names = list(graph.getLocalProperties())
    max_key_length = max(len(key) for key in property_names) if property_names else 0
    for key in property_names:
        prop = graph.getProperty(key)
        print(f"{key:<{max_key_length}} : {prop}")
        
def print_graph_inherited_properties(graph):
    property_names = list(graph.getInheritedProperties())
    max_key_length = max(len(key) for key in property_names) if property_names else 0
    for key in property_names:
        prop = graph.getProperty(key)
        print(f"{key:<{max_key_length}} : {prop}")
         
def print_graph_property(graph, property):
    property_names = list(graph.getLocalProperties())
    if property not in property_names:
        print(f"No property named {property}")
        return         
    values = graph.getProperty(property)
    for node in graph.getNodes():
        print(values.getNodeValue(node))
        
def print_graph_inherited_property(graph, property):
    property_names = list(graph.getInheritedProperties())
    if property not in property_names:
        print(f"No property named {property}")
        return         
    values = graph.getProperty(property)
    for node in graph.getNodes():
        print(values.getNodeValue(node))        
        
############### Acces ###############
        
def get_subgraph(graph, target_id):
    '''get subgraph but recursive'''
    if graph.getId() == target_id:
        return graph

    subgraphs = graph.getSubGraphs()
    while subgraphs.hasNext():
        subgraph = subgraphs.next()
        result = get_subgraph(subgraph, target_id)
        if result is not None:
            return result

    return None

def get_subgraph_name(graph, target_name):
    '''get subgraph by name but recursive'''
    if graph.getName() == target_name:
        return graph

    subgraphs = graph.getSubGraphs()
    while subgraphs.hasNext():
        subgraph = subgraphs.next()
        result = get_subgraph_name(subgraph, target_name)
        if result is not None:
            return result

    return None

############### Bounding box ###############
  
def bounding_box(parent_graph, subgraph):
    '''
    creates a new node representing the bounding box of the subgraph
    puts it around the graph
    add it to the supplied parent graph
    '''
    if subgraph is None:
        raise ValueError("Subgraph is None — cannot compute bounding box.")
    
    label_name = parent_graph.getProperty("externLabel")
    layout = parent_graph.getLayoutProperty('viewLayout')
    size = parent_graph.getSizeProperty('viewSize')
    color = parent_graph.getColorProperty('viewColor')
    shape = parent_graph.getIntegerProperty('viewShape')
    border_width = parent_graph.getProperty("viewBorderWidth")

    # Compute bounding box of all nodes in the subgraph
    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')
    for n in subgraph.getNodes():
        pos = layout[n]
        sz = size[n]
        x0 = pos[0] - sz[0] / 2
        x1 = pos[0] + sz[0] / 2
        y0 = pos[1] - sz[1] / 2
        y1 = pos[1] + sz[1] / 2
        min_x = min(min_x, x0)
        max_x = max(max_x, x1)
        min_y = min(min_y, y0)
        max_y = max(max_y, y1)

    # Add optional padding
    padding = 10.0
    min_x -= padding
    max_x += padding
    min_y -= padding
    max_y += padding * 2

    # Compute bounding box center and dimensions
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    width = max_x - min_x
    height = max_y - min_y

    # Create a new node and style it
    box_node = parent_graph.addNode()
    layout[box_node] = tlp.Coord(center_x, center_y, 0)
    size[box_node] = tlp.Size(width, height, 1)
    border_width[box_node] = 5
    color[box_node] = tlp.Color(255, 0, 0, 15)
    shape[box_node] = tlp.NodeShape.Square
    label_name[box_node] = subgraph.getName()

    return box_node