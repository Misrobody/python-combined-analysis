import sys
import networkx as nx

def convert_dot_to_graphml(dot_file, output_file):
    G = nx.drawing.nx_agraph.read_dot(dot_file)
    nx.write_graphml(G, output_file)
    print(f"Converted '{dot_file}' to '{output_file}' successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python dot_to_graphml.py input.dot output.graphml")
        sys.exit(1)
    dot_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_dot_to_graphml(dot_file, output_file)
