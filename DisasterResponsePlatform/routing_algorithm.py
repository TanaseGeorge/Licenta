import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
import MySQLdb

db = MySQLdb.connect(host="localhost", user="root", passwd="Sqluser1", db="disaster_response")
cursor = db.cursor()

cursor.execute("SELECT start_node, end_node, weight FROM road_network")
road_network_data = cursor.fetchall()

G = nx.DiGraph()

for edge in road_network_data:
    G.add_edge(edge[0], edge[1], weight=edge[2])

db.close()

def find_optimal_route(start_node, end_node):
    try:
        optimal_route = nx.shortest_path(G, start_node, end_node, weight='weight')
        return optimal_route
    except nx.NetworkXNoPath:
        return None

def plot_graph(graph, optimal_route):
    pos = nx.spring_layout(graph)  # or any layout
    nx.draw(graph, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=12, font_weight="bold", arrows=True)
    if optimal_route:
        edges = [(optimal_route[i], optimal_route[i + 1]) for i in range(len(optimal_route) - 1)]
        nx.draw_networkx_edges(graph, pos, edgelist=edges, width=2, edge_color='red')
    plt.show()

def find_and_plot_optimal_route():
    start_node = start_entry.get()
    end_node = end_entry.get()
    if start_node and end_node:
        optimal_route = find_optimal_route(start_node, end_node)
        if optimal_route:
            plot_graph(G, optimal_route)
        else:
            messagebox.showinfo("Error", "No route found.")
    else:
        messagebox.showinfo("Error", "Please enter both start and end nodes.")

root = tk.Tk()
root.title("Optimal Route Finder")

start_label = tk.Label(root, text="Start Node:")
start_label.grid(row=0, column=0, padx=10, pady=5)
start_entry = tk.Entry(root)
start_entry.grid(row=0, column=1, padx=10, pady=5)

end_label = tk.Label(root, text="End Node:")
end_label.grid(row=1, column=0, padx=10, pady=5)
end_entry = tk.Entry(root)
end_entry.grid(row=1, column=1, padx=10, pady=5)

find_button = tk.Button(root, text="Find Optimal Route", command=find_and_plot_optimal_route)
find_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

root.mainloop()
