import networkx as nx
import yaml
from pyvis.network import Network
import networkx as nx
import pandas as pd
import math
from numpy import nan
import matplotlib.pyplot as plt

class LineageVisualizer:
    def __init__(self, metadata):
        self.metadata = metadata
        self.lineage_nx_graph = nx.DiGraph(directed = True)

        # Declaration of node color mapping
        self.data_catalogue_colors = pd.DataFrame(data={"Type":['Business Term','Conceptual Term','Application','System','Table','Data Element','Control'],"Color":['firebrick','silver','lightcoral','forestgreen','lightsteelblue','black','gold']})

        # Declaration of node color mapping
        self.data_catalogue_shapes = pd.DataFrame(data={
            "Type": ['Business Term', 'Conceptual Term', 'Application', 'System', 'Table', 'Data Element', 'Control'],
            "Shape": ['dot', 'dot', 'dot', 'diamond', 'square', 'square', 'triangleDown']})

    def create_graph(self,node_list):
        # Implement logic to create the lineage visualization graph using the pyvis library.
        # Add nodes and edges to the graph based on the extracted metadata.

        self.nodes = node_list

        #self.lineage_data = self.metadata["Lineage - Component Mapping"]

        self.nodes = self.nodes.to_dict('records')

        # Node creation
        for item in self.nodes:
            self.lineage_nx_graph.add_node(item["UID"],color=item["Color"],value=item["Weight"],shape=item["Shape"])

        # Edge creation
        if (len(self.dependencies)>=1):
            for index,item in self.dependencies.iterrows():
                if (item["Source Component"] != "") and (item["Source Component"] != "nan") and (item["Target Component"] != "") and (item["Target Component"] != "nan"):
                    self.lineage_nx_graph.add_edge(item["Source Component"],item["Target Component"],title=item["Mapping Type"])

        return self.lineage_nx_graph

    def create_html_file(self,lineage_graph):
        # Runs the visualization of the previously created graph

        self.lineage_graph = lineage_graph

        # Plot with pyvis
        self.graph_network = Network(directed=True, filter_menu=True, select_menu=True)
        #self.graph_network.show_buttons()  # Show part 3 in the plot (optional)
        self.graph_network.from_nx(self.lineage_graph)  # Create directly from nx graph
        #self.graph_network.show('lineage.html',notebook=False)
        self.graph_network.save_graph("lineage.html")

        pass

    def create_node_list(self,input_node):
        # Creates node list from the AMDR data dictionary

        self.input_node = input_node

        if (self.input_node == "None"):

            self.lineage_data = self.metadata["Lineage - Component Mapping"]

            self.dependencies = pd.DataFrame.from_dict(self.lineage_data)

            # Extracts every element from the data dictionary Excel sheets and converts them to dataframes
            self.business_terms = self.metadata["Data C - Business term"]
            self.business_terms = pd.DataFrame.from_dict(self.business_terms)
            self.data_catalogue = self.business_terms[["UID", "Type of Asset"]]
            self.data_element = self.metadata["Data C - Data Element"]
            self.data_element = pd.DataFrame.from_dict(self.data_element)
            self.data_element = self.data_element[["UID", "Type of Asset"]]
            self.application_system = self.metadata["Data C - Application & System"]
            self.application_system = pd.DataFrame.from_dict(self.application_system)
            self.application_system = self.application_system[["UID", "Type of Asset"]]
            self.table = self.metadata["Data C - Table"]
            self.table = pd.DataFrame.from_dict(self.table)
            self.table = self.table[["UID", "Type of Asset"]]
            self.control = self.metadata["DQ - Business Rule & control"]
            self.control = pd.DataFrame.from_dict(self.control)
            self.control = self.control[["UID", "Type of Asset"]]

            # Concatenates all the dataframes to build a unique data catalogue list
            self.data_catalogue = pd.concat([self.data_catalogue, self.data_element])
            self.data_catalogue = pd.concat([self.data_catalogue, self.application_system])
            self.data_catalogue = pd.concat([self.data_catalogue, self.table])
            self.data_catalogue = pd.concat([self.data_catalogue, self.control])

            # Drop NaN, empty and null values
            self.data_catalogue = self.data_catalogue.dropna(subset=["UID"])

            # Merge with color mapping
            self.data_catalogue = self.data_catalogue.merge(self.data_catalogue_colors, left_on='Type of Asset',right_on='Type', how='left')

            self.data_catalogue = self.data_catalogue.drop(["Type"], axis=1)

            self.data_catalogue = self.data_catalogue.merge(self.data_catalogue_shapes, left_on='Type of Asset',right_on='Type', how='left')

            self.data_catalogue = self.data_catalogue.drop(["Type of Asset", "Type"], axis=1)

            # *** Node weight computing ***
            # Extract Lineage Exce sheet and convert it to Dataframe
            self.lineage_data = self.metadata["Lineage - Component Mapping"]

            self.lineage_data_df = pd.DataFrame.from_dict(self.lineage_data)

            # Separate source and target components
            self.components = self.lineage_data_df[["Source Component"]]

            self.targets = self.lineage_data_df[["Target Component"]]

            # Rename and concatenate both component Dataframes in order to get a unique component list
            self.targets = self.targets.rename(columns={"Target Component": "Source Component"})

            self.components = pd.concat([self.components, self.targets])

            # Drop NaN, empty and null values
            self.components = self.components.dropna(subset=["Source Component"])

            # Reset index (Necessary after concatenation)
            self.components = self.components.reset_index(drop=True)

            # Group and count number of apparances of every component in order to define node weights
            self.components = self.components.groupby(["Source Component"])["Source Component"].count().reset_index(name="Weight")

            # ***

            # Weight mapping and delivery
            self.data_catalogue = self.data_catalogue.merge(self.components, left_on='UID', right_on='Source Component',how='left')

            self.data_catalogue = self.data_catalogue.drop(["Source Component"], axis=1)

            self.data_catalogue["Weight"] = self.data_catalogue["Weight"].fillna(1)

            self.data_catalogue["Weight"] = self.data_catalogue["Weight"].astype(int)

        else:
            self.data_catalogue = []
            self.data_catalogue.append(self.input_node)

            self.lineage_data = self.metadata["Lineage - Component Mapping"]

            self.lineage_data_df = pd.DataFrame.from_dict(self.lineage_data)

            self.dependencies = self.lineage_data_df

            self.dependencies["Remove"] = ""

            self.data_catalogue_aux = self.data_catalogue

            self.aux = 0

            while (self.aux < 2):
                self.data_catalogue_aux = self.data_catalogue

                for index,row in self.lineage_data_df.iterrows():
                    for y in self.data_catalogue_aux:
                        if (y == row["Source Component"]):
                            if (row["Target Component"] not in self.data_catalogue_aux):
                                self.data_catalogue.append(row["Target Component"])
                            #self.dependencies = pd.concat([self.dependencies,self.lineage_data_df.iloc[index]],ignore_index = True)
                            self.dependencies.loc[index, 'Remove'] = "X"
                        elif (y == row["Target Component"]):
                            if (row["Source Component"] not in self.data_catalogue_aux):
                                self.data_catalogue.append(row["Source Component"])
                            #self.dependencies = pd.concat([self.dependencies,self.lineage_data_df.iloc[index]],ignore_index = True)
                            self.dependencies.loc[index, 'Remove'] = "X"

                if(len(self.data_catalogue_aux) == len(self.data_catalogue)):
                    self.aux = self.aux + 1

            self.data_catalogue = pd.DataFrame(self.data_catalogue, columns=['UID'])
            print(self.data_catalogue)

            self.dependencies.drop(self.dependencies[self.dependencies["Remove"] != "X"].index, inplace=True)

            self.dependencies.drop(["Remove"], axis=1)

            print(self.dependencies)

            # Drop NaN, empty and null values
            self.data_catalogue = self.data_catalogue.dropna(subset=["UID"])

            # Extracts every element from the data dictionary Excel sheets and converts them to dataframes
            self.business_terms = self.metadata["Data C - Business term"]
            self.business_terms = pd.DataFrame.from_dict(self.business_terms)
            self.data_catalogue_total = self.business_terms[["UID", "Type of Asset"]]
            self.data_element = self.metadata["Data C - Data Element"]
            self.data_element = pd.DataFrame.from_dict(self.data_element)
            self.data_element = self.data_element[["UID", "Type of Asset"]]
            self.application_system = self.metadata["Data C - Application & System"]
            self.application_system = pd.DataFrame.from_dict(self.application_system)
            self.application_system = self.application_system[["UID", "Type of Asset"]]
            self.table = self.metadata["Data C - Table"]
            self.table = pd.DataFrame.from_dict(self.table)
            self.table = self.table[["UID", "Type of Asset"]]
            self.control = self.metadata["DQ - Business Rule & control"]
            self.control = pd.DataFrame.from_dict(self.control)
            self.control = self.control[["UID", "Type of Asset"]]

            # Concatenates all the dataframes to build a unique data catalogue list
            self.data_catalogue_total = pd.concat([self.data_catalogue_total, self.data_element])
            self.data_catalogue_total = pd.concat([self.data_catalogue_total, self.application_system])
            self.data_catalogue_total = pd.concat([self.data_catalogue_total, self.table])
            self.data_catalogue_total = pd.concat([self.data_catalogue_total, self.control])

            self.data_catalogue_total = self.data_catalogue_total.rename(columns={"UID": "UID_y"})

            # Merge to get type of asset
            self.data_catalogue = self.data_catalogue.merge(self.data_catalogue_total[["UID_y","Type of Asset"]], left_on='UID',right_on='UID_y', how='left')

            self.data_catalogue = self.data_catalogue.drop(["UID_y"], axis=1)

            # Merge with color mapping
            self.data_catalogue = self.data_catalogue.merge(self.data_catalogue_colors, left_on='Type of Asset',right_on='Type', how='left')

            self.data_catalogue = self.data_catalogue.drop(["Type"], axis=1)

            self.data_catalogue = self.data_catalogue.merge(self.data_catalogue_shapes, left_on='Type of Asset',right_on='Type', how='left')

            self.data_catalogue = self.data_catalogue.drop(["Type of Asset", "Type"], axis=1)

            # *** Node weight computing ***
            # Separate source and target components
            self.components = self.lineage_data_df[["Source Component"]]

            self.targets = self.lineage_data_df[["Target Component"]]

            # Rename and concatenate both component Dataframes in order to get a unique component list
            self.targets = self.targets.rename(columns={"Target Component": "Source Component"})

            self.components = pd.concat([self.components, self.targets])

            # Drop NaN, empty and null values
            self.components = self.components.dropna(subset=["Source Component"])

            # Reset index (Necessary after concatenation)
            self.components = self.components.reset_index(drop=True)

            # Group and count number of apparances of every component in order to define node weights
            self.components = self.components.groupby(["Source Component"])["Source Component"].count().reset_index(name="Weight")
            # ***

            # Weight mapping and delivery
            self.data_catalogue = self.data_catalogue.merge(self.components, left_on='UID', right_on='Source Component',how='left')

            self.data_catalogue = self.data_catalogue.drop(["Source Component"], axis=1)

            self.data_catalogue["Weight"] = self.data_catalogue["Weight"].fillna(1)

            self.data_catalogue["Weight"] = self.data_catalogue["Weight"].astype(int)

        return self.data_catalogue

    def save_graph(self, output_path):
        # Implement logic to save the graph to a file in the specified output_path.

        pass
