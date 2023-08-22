import tkinter as tk
import pandas as pd
from pandastable import Table
import duckdb
from tkinter import ttk
from tkinter import *
import webbrowser
from dq_amdr_tool.metadata_parser import MetadataParser
from dq_amdr_tool.lineage_visualizer_V3 import LineageVisualizer
from dq_amdr_tool.ownership_matrix import OwnershipMatrix

class GUIApp:
    def __init__(self, root, full_node_list, metadata):
        self.root = root
        self.root.title("DQMS Analytics")
        self.full_node_list = full_node_list
        self.metadata = metadata

        # Create frames
        self.top_frame = tk.Frame(root, bg='#dc0028', width=1000, height=10)
        self.left_frame = tk.Frame(root, bg='white', width=300,height=590)
        self.right_frame = tk.Frame(root, bg='white', width=700,height=590)

        self.dqms_Label = tk.Label(self.top_frame, text="Data Quality Management System - Analytics", bg="#dc0028")
        #self.dqms_Label.pack()
        self.dqms_Label.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.dqms_Label.config(font=('Arial', 40))  # Cambiar tipo y tamaño de fuente
        self.dqms_Label.config(fg="white")  # Cambiar color del texto

        # Left Frame
        #self.filter_entry = ttk.Entry(self.left_frame)
        #self.filter_entry.pack(pady=10, padx=10, fill=tk.X)

        self.button = ttk.Button(self.left_frame, text="Open Network", command=self.open_network)
        self.button.pack()

        self.list_items = tk.Variable(value=self.full_node_list)
        self.listbox = tk.Listbox(self.left_frame, selectmode=tk.SINGLE, listvariable=self.list_items)
        self.scroll_list = ttk.Scrollbar(self.left_frame, orient=VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self.scroll_list.set)
        self.listbox.pack(side="left", fill="both", expand=True)
        self.scroll_list.pack(side="right", fill="both")

        # Right Frame

        # Create text box
        self.textbox = tk.Text(self.right_frame, height=7, width=140, font='Helvetica 10 bold')
        self.textbox.insert(tk.END,"Queriable tables:\n - business_terms\n - data_elements\n - application_systems\n - tables\n - controls\n - lineage")
        self.textbox.pack()

        # Create query entry
        self.query_entry = ttk.Entry(self.right_frame)
        self.query_entry.pack(padx=100, pady=10, fill=tk.X)

        # Create execute button
        self.execute_button = ttk.Button(self.right_frame, text="Execute Query", command=self.execute_query)
        self.execute_button.pack()

        # Create tree view
        self.tree = ttk.Treeview(self.right_frame)
        self.tree['show'] = 'headings'
        self.scroll = ttk.Scrollbar(self.right_frame, orient=HORIZONTAL, command=self.tree.xview)
        self.scroll_y = ttk.Scrollbar(self.right_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(xscrollcommand=self.scroll.set)
        self.tree.configure(yscrollcommand=self.scroll_y.set)

        self.right_frame.pack_propagate(0)
        self.scroll.pack(side="bottom", fill="x")
        self.scroll_y.pack(side="right", fill="y")
        self.tree.pack(side="top", fill="both", expand=True)

        # Configure weights for resizing
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=7)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Add frames to root
        self.top_frame.grid(row=0,columnspan=2, sticky="nsew")
        self.left_frame.grid(row=1, column=0, sticky="nsew")
        self.right_frame.grid(row=1, column=1, sticky="nsew")

    # Function to execute query
    def execute_query(self):
        self.query = self.query_entry.get()

        for i in self.tree.get_children():
            self.tree.delete(i)

        self.cols = []

        self.tree["columns"] = self.cols
        for i in self.cols:
            self.tree.column(i, anchor="w")
            self.tree.heading(i, text=i, anchor='w')

        self.query_df = duckdb.query(self.query).df()

        self.cols = list(self.query_df.columns)

        self.tree["columns"] = self.cols
        for i in self.cols:
            self.tree.column(i, anchor="w")
            self.tree.heading(i, text=i, anchor='w')

        for index, row in self.query_df.iterrows():
            self.tree.insert("", 0, text=index, values=list(row))

    def execute_graph(self,input_selected_item):
        self.input_selected_item = input_selected_item

        # No element selected, represent complete AMDR lineage
        self.lineage_visualizer = LineageVisualizer(self.metadata)
        self.nodes = self.lineage_visualizer.create_node_list(self.input_selected_item)
        self.lineage_graph = self.lineage_visualizer.create_graph(self.nodes)
        self.lineage_visualizer.create_html_file(self.lineage_graph)

        pass

    def open_network(self):
        self.selected_item = self.listbox.get(tk.ACTIVE)
        # Replace with your pyvis network code to generate the visualization

        print("Selected node:"+self.selected_item)

        # Generate network
        self.execute_graph(self.selected_item)

        # For demonstration, let's just open a dummy URL
        webbrowser.open_new_tab("lineage.html")

if __name__ == "__main__":
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

    # Step 2: Turn AMDR tabs to dataframes to allow pandasql queries
    # Extracts every element from the data dictionary Excel sheets and converts them to dataframes
    business_terms = metadata["Data C - Business term"]
    business_terms = pd.DataFrame.from_dict(business_terms)
    business_terms.columns = business_terms.columns.str.replace(' ', '_')
    data_elements = metadata["Data C - Data Element"]
    data_elements = pd.DataFrame.from_dict(data_elements)
    data_elements.columns = data_elements.columns.str.replace(' ', '_')
    application_systems = metadata["Data C - Application & System"]
    application_systems = pd.DataFrame.from_dict(application_systems)
    application_systems.columns = application_systems.columns.str.replace(' ', '_')
    tables = metadata["Data C - Table"]
    tables = pd.DataFrame.from_dict(tables)
    tables.columns = tables.columns.str.replace(' ', '_')
    controls = metadata["DQ - Business Rule & control"]
    controls = pd.DataFrame.from_dict(controls)
    controls.columns = controls.columns.str.replace(' ', '_')
    lineage = metadata["Lineage - Component Mapping"]
    lineage = pd.DataFrame.from_dict(lineage)
    lineage.columns = lineage.columns.str.replace(' ', '_')

    lineage_visualizer = LineageVisualizer(metadata)
    full_node_list = lineage_visualizer.create_node_list("None")

    full_node_list = full_node_list["UID"].values.tolist()

    print(full_node_list)

    full_node_list.insert(0,"None")

    root = tk.Tk()
    root.state('zoomed')
    app = GUIApp(root,full_node_list,metadata)
    root.mainloop()