from tulip import tlp
import sys
import os

def list_subgraphs(g, indent=0):
    for sg in g.getSubGraphs():
        print("  " * indent + "- " + sg.getName())
        list_subgraphs(sg, indent + 1)


if __name__ == "__main__":
    
    print("\nPlugins:")
    print(tlp.getExportPluginsList())
    print("\nLayout Algorithms:")
    print(tlp.getLayoutAlgorithmPluginsList())    
    
    if len(sys.argv) != 3:
        print("Usage: python render_flat_graph.py <input.graphml> <output.svg>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_svg = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        sys.exit(1)
        
    ##########################################

    tlp.initTulipLib()
    tlp.loadPlugins()

    graph = tlp.loadGraph(input_file)
    if graph is None:
        print(f"Failed to load graph: {input_file}")
        sys.exit(1)
             
    ##########################################

    layout = graph.getLayoutProperty("viewLayout")
    graph.applyLayoutAlgorithm("FM^3 (OGDF)", layout)

    size = graph.getSizeProperty("viewSize")
    label = graph.getStringProperty("viewLabel")
    names = graph.getStringProperty("name")
    for node in graph.getNodes():
        size[node] = tlp.Size(10, 10, 0)
        label[node] = names[node]


    ##########################################
    
    params = tlp.getDefaultPluginParameters("SVG Export", graph)
    params["fileName"] = output_svg
    params["drawBackground"] = False
    params["textFontSize"] = 10

    success = tlp.exportGraph("SVG Export", graph, output_svg, params)  
    if not success:
        print("SVG export failed.")
        sys.exit(1)

    print(f"\nGraph successfully saved to: {output_svg}")
