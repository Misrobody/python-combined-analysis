import xml.etree.ElementTree as ET
import argparse

def update_marker_size(input_path, output_path, size):
    # Parse the SVG file
    tree = ET.parse(input_path)
    root = tree.getroot()

    # SVG namespace handling
    ns = {'svg': 'http://www.w3.org/2000/svg'}
    ET.register_namespace('', ns['svg'])

    # Find and update all <marker> elements
    for marker in root.findall('.//svg:marker', ns):
        marker.set('markerWidth', str(size))
        marker.set('markerHeight', str(size))

    # Write the updated SVG to output
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"Updated all marker sizes to {size} and saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set markerWidth and markerHeight in an SVG file.")
    parser.add_argument("-i", "--input", help="Path to the input SVG file")
    parser.add_argument("-o", "--output", help="Path to the output SVG file")
    parser.add_argument("-s", "--size", type=float, help="New size for markerWidth and markerHeight")

    args = parser.parse_args()
    update_marker_size(args.input, args.output, args.size)
