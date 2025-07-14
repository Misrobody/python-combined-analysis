import xml.etree.ElementTree as ET
import argparse

def update_font_size(input_path, output_path, new_font_size):
    # Parse the SVG file
    tree = ET.parse(input_path)
    root = tree.getroot()

    # SVG namespace handling
    ns = {'svg': 'http://www.w3.org/2000/svg'}
    ET.register_namespace('', ns['svg'])

    # Update font-size attributes
    for elem in root.iter():
        if 'font-size' in elem.attrib:
            elem.set('font-size', str(new_font_size))

    # Write the updated SVG to output
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"Updated font-size to {new_font_size} and saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update font-size attributes in an SVG file.")
    parser.add_argument("-i", "--input", type=str, help="Path to the input SVG file")
    parser.add_argument("-o", "--output", type=str, help="Path to the output SVG file")
    parser.add_argument("-f", "--fontsize", type=int, help="New font-size value to apply")

    args = parser.parse_args()
    update_font_size(args.input, args.output, args.fontsize)
