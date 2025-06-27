#!/usr/bin/env python3

import argparse
import os
import requests
import time
from py2cytoscape import cyrest

CYREST_BASE = "http://localhost:1234/v1"

def main(input_file, output_file):
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' not found.")

    # Upload the GraphML file to Cytoscape
    files = {'file': open(input_file, 'rb')}
    response = requests.post(f"{CYREST_BASE}/networks?format=graphml", files=files)
    response.raise_for_status()
    network_suid = response.json()['networkSUID']

    # Apply layout via py2cytoscape
    cy = cyrest.cyclient()
    cy.layout.apply(name="force-directed", network=network_suid)

    # Optional: pause to ensure layout finishes
    time.sleep(2)

    # Export to PDF
    cy.export.render(file=output_file, type='pdf', options={'network': network_suid})
    print(f"✅ Successfully exported to {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import GraphML, visualize with Cytoscape, and export to PDF (CLI only).')
    parser.add_argument('input', help='Path to input .graphml file')
    parser.add_argument('output', help='Path to output .pdf file')
    args = parser.parse_args()

    main(args.input, args.output)
