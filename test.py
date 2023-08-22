import tkinter as tk
from tkinter import ttk

# Sample dictionary
data = {
    'name': 'John',
    'age': 30,
    'city': 'New York'
}

# Function to execute query
def execute_query():
    query = query_entry.get()

    result_text.config(state=tk.NORMAL)
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, str(e))
    result_text.config(state=tk.DISABLED)

# Create main window
root = tk.Tk()
root.title("Dictionary Query Tool")

# Create query entry
query_entry = ttk.Entry(root)
query_entry.pack(padx=10, pady=10, fill=tk.X)

# Create execute button
execute_button = ttk.Button(root, text="Execute Query", command=execute_query)
execute_button.pack()

# Create result text widget
result_text = tk.Text(root, state=tk.DISABLED, wrap=tk.WORD)
result_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()