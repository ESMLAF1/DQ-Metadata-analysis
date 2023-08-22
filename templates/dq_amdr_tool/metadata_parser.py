import pandas as pd
import yaml

class MetadataParser:
    def __init__(self, input_file_path, kme_definitions_file_path, mapping_tab_name_file):
        self.input_file_path = input_file_path
        self.kme_definitions = {}
        self.load_kme_definitions(kme_definitions_file_path)

        with open(mapping_tab_name_file, "r") as mapping_file:
            self.tab_to_kme_mapping = yaml.safe_load(mapping_file)

    def parse_metadata(self):
        # Step 1: Parse the metadata from the input Excel file.
        df = pd.read_excel(self.input_file_path, sheet_name=None)

        # Step 2: Process each tab and create a dictionary to store the metadata.
        self.metadata = {}
        for sheet_name, data in df.items():
            # Convert the data to a list of dictionaries (one for each row).
            records = data.to_dict('records')
            self.metadata[sheet_name] = records

        return self.metadata

    def load_kme_definitions(self, kme_definitions_file_path):
        # Step 3: Load the KME definitions from the YAML file.
        with open(kme_definitions_file_path, 'r') as file:
            self.kme_definitions = yaml.safe_load(file)

        return self.kme_definitions

    def get_metadata(self):
        return self.metadata

    def get_kme_definitions(self):
        return self.kme_definitions

    def validate_application_system_nodes(self):
        if self.metadata is None or self.tab_to_kme_mapping is None:
            raise ValueError(
                "Metadata or tab_to_kme_mapping not loaded. Call parse_metadata() and load_tab_to_kme_mapping() first.")

        for mapping_name, sheet_name in self.tab_to_kme_mapping['tabs_to_kme_mapping'].items():
            if mapping_name not in self.kme_definitions:
                print(f"Error: Invalid KME definition key '{mapping_name}'.")
                continue

            kme_definition_list = self.kme_definitions[mapping_name]
            if not isinstance(kme_definition_list, list):
                print(f"Error: Invalid KME definition format for key '{mapping_name}'.")
                continue

            for kme_definition in kme_definition_list:
                if not isinstance(kme_definition, dict):
                    print(f"Error: Invalid KME definition format for key '{mapping_name}'.")
                    continue

                kme_key_name = kme_definition.get('name')
                kme_data_type = kme_definition.get('data_type')

                if kme_key_name is None or kme_data_type is None:
                    print(
                        f"Error: Missing '{kme_key_name}' or '{kme_data_type}'in KME definition for mapping '{mapping_name}'.")
                    continue

                if sheet_name not in self.metadata:
                    print(f"Warning: No matching sheet found for mapping '{mapping_name}'.")
                    continue

                records = self.metadata[sheet_name]

                for record in records:
                    for key, value in record.items():
                        if key == kme_key_name:  # Check if the keys match
                            excel_data_type = None

                            if pd.notna(value):  # Check if the cell value is not empty
                                try:
                                    excel_data_type = pd.api.types.infer_dtype(value, skipna=True)
                                except TypeError:
                                    # If the value is not iterable (e.g., 'float'), skip data type inference
                                    pass

                            if excel_data_type is not None and excel_data_type != kme_data_type:
                                print(f"Error: Data type mismatch for key '{key}' in sheet '{sheet_name}'. "
                                      f"KME data type: '{kme_data_type}', Excel data type: '{excel_data_type}'.")

def main():
    input_file_path = "../data/Atradius_Metadata_Repository_for_test.xlsx"
    kme_definitions_file_path = "../kme_definitions.yaml"
    mapping_tab_name_file = "../mapping_tab_sheet_name.yaml"

    metadata_parser = MetadataParser(input_file_path, kme_definitions_file_path, mapping_tab_name_file)
    metadata_parser.parse_metadata()

    metadata = metadata_parser.get_metadata()
    print("Parsed Metadata:")
    print(metadata)

    kme_definitions = metadata_parser.get_kme_definitions()
    print("\nLoaded KME Definitions:")
    print(kme_definitions)

    # Validate application system nodes
    metadata_parser.validate_application_system_nodes()

if __name__ == "__main__":
    main()
