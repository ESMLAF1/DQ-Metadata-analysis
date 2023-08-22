from dq_amdr_tool.SharePointExcelReader import SharePointExcelReader
from dq_amdr_tool.metadata_parser import MetadataParser
from dq_amdr_tool.lineage_visualizer import LineageVisualizer
from dq_amdr_tool.ownership_matrix import OwnershipMatrix

def main():
    # File path for the input Excel file containing the metadata and DQ information.

    input_file_path = "data/Atradius_Metadata_Repository_for_DQ.xlsx"
    kme_definitions_file_path = "kme_definitions.yaml"
    mapping_tab_name_file = "mapping_tab_sheet_name.yaml"
    catalog_color_mapping_name_file = "mapping_catalog_style.yaml"

    # Step 1: Parse the metadata from the input Excel file.
    metadata_parser = MetadataParser(input_file_path, kme_definitions_file_path, mapping_tab_name_file)
    metadata = metadata_parser.parse_metadata()
    kme_definitions = metadata_parser.get_kme_definitions()

    # this should return a list of the AMDR elements that are not passing the validations according to KME_definitions
    # as of now the ones that are not compliant are an output in the console
    metadata_parser.validate_application_system_nodes()

    # Step 2: Create visualization object, define graph elements, build and represent lineage network
    lineage_visualizer = LineageVisualizer(metadata,catalog_color_mapping_name_file)
    nodes = lineage_visualizer.create_node_list()
    lineage_graph = lineage_visualizer.create_graph(nodes)
    lineage_visualizer.show_graph(lineage_graph)

    # lineage_visualizer = LineageVisualizer(metadata)
    # lineage_visualizer.create_graph()
    # output_graph_path = "lineage_visualization.html"
    # lineage_visualizer.save_graph(output_graph_path)

    #  Create and save the ownership matrix table to an HTML file.
    # ownership_matrix = OwnershipMatrix(metadata)  # Pass the metadata to the OwnershipMatrix instance
    # ownership_matrix.create_matrix()

    # output_matrix_path = "ownership_matrix.html"
    # ownership_matrix.save_matrix_to_html(output_matrix_path)

if __name__ == "__main__":
    main()




