"""
Processes a flattened GraphML file from MVIS and renders it as a PDF using the graph-tool Python module.
"""

import sys, os
from graph_tool.all import *

def main():
    if len(sys.argv) != 2:
        print("Usage: python render_flat_graph.py <filename.graphml>")
        sys.exit(1)
    filename = sys.argv[1]
    g = load_graph(filename)

    pos = sfdp_layout(g, K=1.5)
    output_path = os.path.splitext(filename)[0] + "_graph.pdf"

    graph_draw(
        g,
        pos=pos,
        vertex_text=g.vp.get('_graphml_vertex_id'),
        vertex_font_size=10,
        vertex_color="black",
        vertex_fill_color="white",
        edge_color="grey",
        output_size=(30000, 30000),
        output=output_path
    )
    
    print(f"Graph exported to: {output_path}")

if __name__ == "__main__":
    main()
