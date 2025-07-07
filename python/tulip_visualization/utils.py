from tulip import tlp
      
############### Misc. ###############    
                       
def has_meta_nodes(graph):
    for n in graph.getNodes():
        if graph.isMetaNode(n):
            return True
    return False
    
############### Hierarchy ###############
    
def print_subgraph_hierarchy(graph, indent=0, is_root=True):
    name = graph.getName() or "(unnamed)"
    graph_id = graph.getId()
    num_nodes = graph.numberOfNodes()
    num_edges = graph.numberOfEdges()
    indent_str = "  " * indent

    label = f"{name} [ROOT]" if is_root else name
    print(f"{indent_str}- {label:<40} (ID: {graph_id:>3})  Nodes: {num_nodes:>4}  Edges: {num_edges:>4}")

    subgraphs = graph.getSubGraphs()
    while subgraphs.hasNext():
        subgraph = subgraphs.next()
        print_subgraph_hierarchy(subgraph, indent + 1, is_root=False)      
                  
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
    quotient_hierarchy(graph.getSubGraph("quotient of 0"))        
          
    
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
            
def print_graph_property(graph, property):
    property_names = list(graph.getLocalProperties())
    if property not in property_names:
        print(f"No property named {property}")
        return         
    values = graph.getProperty(property)
    for node in graph.getNodes():
        print(values.getNodeValue(node))