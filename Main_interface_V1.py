import tkinter as tk
from tkinter import ttk
from tkinter import *
import webbrowser
from dq_amdr_tool.SharePointExcelReader import SharePointExcelReader
from dq_amdr_tool.metadata_parser import MetadataParser
from dq_amdr_tool.lineage_visualizer_V3 import LineageVisualizer
from dq_amdr_tool.ownership_matrix import OwnershipMatrix

class GUIApp:
    def __init__(self, root, full_node_list, metadata):
        self.root = root
        self.root.title("AMDR - Data Catalogue")
        self.full_node_list = full_node_list
        self.metadata = metadata

        # Create frames
        self.left_frame = tk.Frame(root, bg='white', width=300,height=600)
        self.right_frame = tk.Frame(root, bg='white', width=700,height=600)

        # Left Frame
        self.filter_entry = ttk.Entry(self.left_frame)
        self.filter_entry.pack(pady=10, padx=10, fill=tk.X)

        self.list_items = tk.Variable(value=self.full_node_list)
        self.listbox = tk.Listbox(self.left_frame, selectmode=tk.SINGLE, listvariable=self.list_items)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        self.button = tk.Button(self.left_frame, text="Open Network", command=self.open_network)
        self.button.pack(pady=10, padx=10, fill=tk.X)

        # Configure weights for resizing
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=7)
        self.root.rowconfigure(0, weight=1)

        # Add frames to root
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.right_frame.grid(row=0, column=1, sticky="nsew")

    def execute_graph(self,input_selected_item):
        self.input_selected_item = input_selected_item

        # Create graph and prepare for visualization
        self.lineage_visualizer = LineageVisualizer(self.metadata)
        self.nodes = self.lineage_visualizer.create_node_list(self.input_selected_item)
        self.lineage_graph = self.lineage_visualizer.create_graph(self.nodes)
        self.lineage_visualizer.create_html_file(self.lineage_graph)

        pass

    def open_network(self):
        # Get selected node
        self.selected_item = self.listbox.get(tk.ACTIVE)

        # Generate network
        self.execute_graph(self.selected_item)

        # Open the generated network in browser
        webbrowser.open_new_tab("lineage.html")

if __name__ == "__main__":
    # Inputs
    input_file_path = "data/Data_Quality_Management_Sytem.xlsx"
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

    # Step 2: Create Data Catalogue list
    lineage_visualizer = LineageVisualizer(metadata)
    full_node_list = lineage_visualizer.create_node_list("None")

    full_node_list = full_node_list["UID"].values.tolist()

    full_node_list.insert(0,"None")

    # Step 3: Initialize GUI app
    root = tk.Tk()
    root.state('zoomed')
    app = GUIApp(root,full_node_list,metadata)
    root.mainloop()