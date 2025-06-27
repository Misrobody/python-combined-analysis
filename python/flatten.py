import sys
import xml.etree.ElementTree as ET
import re

GRAPHML_NS = "http://graphml.graphdrawing.org/xmlns"
NS = {"g": GRAPHML_NS}
ET.register_namespace('', GRAPHML_NS)

# Remove numeric suffixes (e.g., module_0 --> module)
def strip_numeric_suffixes(name):
    parts = name.split(".")
    cleaned_parts = [re.sub(r'_\d+$', '', part) for part in parts]
    return ".".join(cleaned_parts)

# Keep only the module path + method name (e.g., drop return type)
def simplify_method_path(name):
    parts= name.split(" ")
    new = ".".join(parts[0].split(".")[:-1]) + "." + parts[2].split("(")[0]
    return new

# Combine both transformations
def normalize_id(name):
    base = strip_numeric_suffixes(name)
    if len(name.split(" ")) > 2:
        return simplify_method_path(base)
    return base

def flatten_graphml(filename, output_file):
    tree = ET.parse(filename)
    root = tree.getroot()
    top_graph = root.find(".//g:graph", NS)
    if top_graph is None:
        raise RuntimeError("No top-level <graph> found in GraphML.")

    collected_nodes = []
    collected_edges = []
    seen_node_ids = set()

    def recurse_extract(graph_elem):
        for node in list(graph_elem.findall("g:node", NS)):
            original_id = node.attrib["id"]
            clean_id = normalize_id(original_id)

            subgraph = node.find("g:graph", NS)
            if subgraph is not None:
                recurse_extract(subgraph)
                graph_elem.remove(node)
                continue

            if clean_id in seen_node_ids:
                graph_elem.remove(node)
                continue

            seen_node_ids.add(clean_id)
            node.attrib["id"] = clean_id
            collected_nodes.append(node)
            graph_elem.remove(node)

        for edge in list(graph_elem.findall("g:edge", NS)):
            for attr in ("source", "target"):
                if attr in edge.attrib:
                    edge.attrib[attr] = normalize_id(edge.attrib[attr])
            collected_edges.append(edge)
            graph_elem.remove(edge)

    recurse_extract(top_graph)

    for node in collected_nodes:
        top_graph.append(node)
    for edge in collected_edges:
        top_graph.append(edge)

    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"Fully normalized and flattened GraphML saved to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python flatten_graphml.py input.graphml output_flat.graphml")
        sys.exit(1)

    flatten_graphml(sys.argv[1], sys.argv[2])
