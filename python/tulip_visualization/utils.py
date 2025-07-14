from tulip import tlp
      
############### Misc. ###############    
                       
def has_meta_nodes(graph):
    for n in graph.getNodes():
        if graph.isMetaNode(n):
            return True
    return False
    
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
                  
def print_metagraph(graph):
    def quotient_hierarchy(graph, indent=0): 
        name = graph.getName() or "(unnamed)"
        graph_id = graph.getId()
        indent_str = "  " * indent
        print(f"{indent_str}- {name:<40} (ID: {graph_id:>3})")            
        if not graph.getName().startswith("quotient"):
            return       
        nodes = graph.getNodes()       
        for i in nodes:
            inner_graph = graph.getNodeMetaInfo(i)
            quotient_hierarchy(inner_graph, indent+1)    
      
    if not graph.getSubGraph("quotient of 0"):
        print("no recursive metagraph")  
    else:
        print("=" * 100)
        print("METAGRAPH")
        quotient_hierarchy(graph.getSubGraph("quotient of 0"))        
                 
def print_nodes_with_metanode_tags(graph):
    """
    Prints all nodes in the graph and indicates which ones are metanodes.
    If the graph contains subgraphs (metanodes), it recursively explores them.
    """
    def recurse_print(g, indent=0):
        for node in g.getNodes():
            prefix = "  " * indent
            if g.isMetaNode(node):
                print(f"{prefix}Node {node.id} [Metanode]")
                # Recursively print contents of the metanode
                recurse_print(g.getSubGraph(node), indent + 1)
            else:
                print(f"{prefix}Node {node.id}")

    print("Listing all nodes in the graph:")
    recurse_print(graph)
  
############### Properties ###############
    
def print_meta_node_properties(graph):
    property_names = list(graph.getProperties())
    meta_props = {}

    for node in graph.getNodes():
        if graph.isMetaNode(node):
            print(f"First meta-node found: ID {node.id}")
            for name in property_names:
                try:
                    prop = graph.getProperty(name)
                    meta_props[name] = prop[node]
                except:
                    continue
            for k, v in meta_props.items():
                print(f"  {k}: {v}")
            return meta_props

    print("No meta-node found in the graph.")
    return None
    
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

#####################################

def get_quotient(rootgraph, subgraph):
    '''Returns the quotient of the associated subgraph if it exists in root.'''
    for g in rootgraph.getSubGraphs():
        if g.getName() == "quotient of " + subgraph.getName():
            return g
    return None

def get_metanode_of_subgraph(rootgraph, subgraph):  
    if subgraph.getName() == "quotient of 0":
        return None
    if "quotient of" in subgraph.getName():
        name = subgraph.getName().replace("quotient of ", "")
        target = get_subgraph_name(rootgraph, name)
    else:
        target = subgraph
        
    quotient = get_quotient(rootgraph, target.getSuperGraph()) 
    for n in quotient.getNodes():
        if quotient.getNodeMetaInfo(n).getName().replace("quotient of ", "") == target.getName():
            return n               
    return None

def fit_metanode_around_subgraph(parent_graph, subgraph):
    metanode = get_metanode_of_subgraph(parent_graph, subgraph)
    if subgraph is None:
        raise ValueError("No metanode associated with this subgraph.")
    
    layout = parent_graph.getLayoutProperty('viewLayout')
    size = parent_graph.getSizeProperty('viewSize')
    
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
    
    # Optional: add padding
    padding = 10.0
    min_x -= padding
    max_x += padding
    min_y -= padding
    max_y += padding
    
    # Set metanode position and size
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    width = max_x - min_x
    height = max_y - min_y
    
    layout[metanode] = tlp.Coord(center_x, center_y, 0)
    size[metanode] = tlp.Size(width, height, 1)
    
def add_bounding_box_node_for_subgraph(parent_graph, subgraph):
    if subgraph is None:
        raise ValueError("Subgraph is None — cannot compute bounding box.")
    
    layout = parent_graph.getLayoutProperty('viewLayout')
    size = parent_graph.getSizeProperty('viewSize')
    
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
    max_y += padding
    
    # Compute bounding box center and dimensions
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    width = max_x - min_x
    height = max_y - min_y
    
    # Create a new node and assign position and size
    box_node = parent_graph.addNode()
    layout[box_node] = tlp.Coord(center_x, center_y, 0)
    size[box_node] = tlp.Size(width, height, 1)
    
    return box_node


def bounding_box(parent_graph, subgraph):
    if subgraph is None:
        raise ValueError("Subgraph is None — cannot compute bounding box.")

    layout = parent_graph.getLayoutProperty('viewLayout')
    size = parent_graph.getSizeProperty('viewSize')
    color = parent_graph.getColorProperty('viewColor')
    shape = parent_graph.getIntegerProperty('viewShape')

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
    max_y += padding

    # Compute bounding box center and dimensions
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    width = max_x - min_x
    height = max_y - min_y

    # Create a new node and assign position and size
    box_node = parent_graph.addNode()
    layout[box_node] = tlp.Coord(center_x, center_y, 0)
    size[box_node] = tlp.Size(width, height, 1)

    color[box_node] = tlp.Color(255, 0, 0, 100)
    shape[box_node] = tlp.NodeShape.Square

    return box_node

####################

def translate_subgraph_nodes(subgraph, dx, dy, dz=0):
    """
    Translates all nodes in the given subgraph by the specified (dx, dy, dz) offset.

    Parameters:
        subgraph (tlp.Graph): The subgraph to translate.
        dx (float): Translation in X-axis.
        dy (float): Translation in Y-axis.
        dz (float): Translation in Z-axis (optional, default is 0).
    """
    layout = subgraph.getLayoutProperty("viewLayout")
    translation_vector = tlp.Vec3f(dx, dy, dz)

    for node in subgraph.getNodes():
        layout.translate(node, translation_vector)
        
        
def print_subgraph_hierarchy_bottom_up(graph, indent=0, is_root=True, nodes=False):
    subgraphs = graph.getSubGraphs()
    subgraph_list = []
    while subgraphs.hasNext():
        subgraph_list.append(subgraphs.next())

    for subgraph in subgraph_list:
        print_subgraph_hierarchy_bottom_up(subgraph, indent + 1, is_root=False, nodes=nodes)

    name = graph.getName() or "(unnamed)"
    graph_id = graph.getId()
    num_nodes = graph.numberOfNodes()
    num_edges = graph.numberOfEdges()
    indent_str = "  " * indent

    label = f"{name} [ROOT]" if is_root else name
    print(f"{indent_str}- {label:<40} (ID: {graph_id:>3})  Nodes: {num_nodes:>4}  Edges: {num_edges:>4}")

    if nodes:
        names = graph.getProperty("viewLabel")
        indent_str = "  " * (indent + 1)
        for i in graph.getNodes():
            print(f"{indent_str}- {names[i].upper():<40}")
