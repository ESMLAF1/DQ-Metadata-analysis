import tkinter as tk
from tkinter import ttk
from pyvis.network import Network

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Application")

        self.left_frame = ttk.Frame(self.root, width=200)
        self.left_frame.pack(side="left", fill="y")

        self.right_frame = ttk.Frame(self.root)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # Call methods to populate the frames
        self.create_left_frame()
        self.create_right_frame()

    def create_left_frame(self):
        # Create widgets for the left frame (list, filter, button)
        self.object_list = tk.Listbox(self.left_frame)
        self.filter_entry = ttk.Entry(self.left_frame)
        self.update_button = ttk.Button(self.left_frame, text="Update Graph", command=self.update_graph)

        # Position widgets in the left frame
        self.object_list.pack(side="top", fill="both", expand=True)
        self.filter_entry.pack(side="top", fill="x")
        self.update_button.pack(side="bottom", fill="x")

        # Populate object list (you should replace this with your list of objects)
        objects = ["Object 1", "Object 2", "Object 3"]
        for obj in objects:
            self.object_list.insert("end", obj)

    def create_right_frame(self):
        # Create the pyvis network graph with specified dimensions
        graph_width = self.right_frame.winfo_width()  # Get the width of the right frame
        graph_height = self.right_frame.winfo_height()  # Get the height of the right frame
        self.graph = Network(graph_width, graph_height, notebook=True)
        self.graph.show("graph.html")  # Display the graph in an HTML file
        self.update_graph()  # Initial graph update

    def update_graph(self):
        # Clear the graph and add nodes/edges based on selected object
        #self.graph.clear()
        selected_object = self.object_list.get(tk.ACTIVE)  # Get selected object from the list
        # Add nodes and edges to the graph based on the selected object (replace with your logic)
        self.graph.add_node(selected_object)
        self.graph.show("graph.html")  # Update the graph

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()