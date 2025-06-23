'''
import xml.etree.ElementTree as ET
import sys

def is_multi_part(string):
    parts = string.split(".")
    return len(parts) > 1

if len(sys.argv) < 2:
    print("Usage: python script.py <input_file.xml>")
    sys.exit(1)
xml_file = sys.argv[1]

tree = ET.parse(xml_file)
root = tree.getroot()

for component in root.findall(".//componentTypes"):
    key_value = component.get("key") 
    if is_multi_part(key_value):
        package = ".".join(key_value.split(".")[:-1])
    else:
        package = key_value
    value = component.find("./value")
    if value is not None:
        value.set("package", package)

updated_file = "updated_" + xml_file
tree.write(updated_file, encoding="ASCII", xml_declaration=True)
print(f"Updated XML saved to {updated_file}")
'''

from lxml import etree
import sys

def is_multi_part(string):
    parts = string.split(".")
    return len(parts) > 1

if len(sys.argv) < 2:
    print("Usage: python script.py <input_file.xml>")
    sys.exit(1)
xml_file = sys.argv[1]

parser = etree.XMLParser(remove_blank_text=True)
tree = etree.parse(xml_file, parser)
root = tree.getroot()

for component in root.xpath("//componentTypes"):
    value = component.find("./value")
    if value is not None:
        full_name = value.get("name")
        if is_multi_part(full_name):       
            package = ".".join(full_name.split(".")[:-1])
        else:
            package = full_name
        name = full_name.split(".")[-1]

        #print(value.get("name") + " | " + package + " : " + name)      
        value.set("package", package)
        value.set("name", name)

updated_file = xml_file
xml_string = etree.tostring(root, encoding="ASCII", xml_declaration=True, pretty_print=True)

with open(updated_file, "wb") as f:
    f.write(xml_string)

print(f"Updated XML saved to {updated_file}")
