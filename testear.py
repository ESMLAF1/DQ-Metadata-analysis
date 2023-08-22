import pandas as pd
import yaml
from pyvis.network import Network
import networkx as nx

input_file_path = "data/Atradius_Metadata_Repository_for_DQ.xlsx"
kme_definitions_file_path = "kme_definitions.yaml"
mapping_tab_name_file = "mapping_tab_sheet_name.yaml"
catalog_color_mapping_name_file = "mapping_catalog_style.yaml"

kme_definitions = {}
load_kme_definitions(kme_definitions_file_path)

with open(mapping_tab_name_file, "r") as mapping_file:
    self.tab_to_kme_mapping = yaml.safe_load(mapping_file)

parse_metadata()

def load_kme_definitions(kme_definitions_file_path):
    # Step 3: Load the KME definitions from the YAML file.
    with open(kme_definitions_file_path, 'r') as file:
        kme_definitions = yaml.safe_load(file)

def parse_metadata():
    # Step 1: Parse the metadata from the input Excel file.
    df = pd.read_excel(input_file_path, sheet_name=None)

    # Step 2: Process each tab and create a dictionary to store the metadata.
    metadata = {}
    for sheet_name, data in df.items():
        # Convert the data to a list of dictionaries (one for each row).
        records = data.to_dict('records')
        metadata[sheet_name] = records



print("Hecho!")