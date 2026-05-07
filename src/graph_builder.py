from collections import defaultdict
from itertools import combinations
import networkx as nx
from pathlib import Path
import matplotlib.pyplot as plt



def build_extension_graph(multi_extension_instructions):
    """
    Build a graph of extensions based on shared instructions.

    Args:
        multi_extension_instructions (dict):
            Mapping of instruction → list of extensions.

    Returns:
        dict:
            Extension → set of connected extensions.
    """

    graph = defaultdict(set)

    for _, extensions in multi_extension_instructions.items():
        for a, b in combinations(extensions, 2):
            graph[a].add(b)
            graph[b].add(a)

    return graph


def format_graph(graph):
    """
    Format the extension relationship graph into a list of strings.

    Args:
        graph (dict):
            Extension → set of connected extensions.

    Returns:
        list:
            Formatted strings representing the graph.
    """
    lines = []

    header = "Extension Relationships"
    separator = "-" * 40

    lines.append(header)
    lines.append(separator)

    for ext in sorted(graph.keys()):
        connections = ", ".join(sorted(graph[ext]))
        lines.append(f"{ext} -> {connections}")

    return lines


def plot_graph(graph):
    """
    Generate and save a visual graph of extension relationships.

    - Cleans extension names (removes rv32_/rv64_)
    - Uses spring layout for better spacing
    - Saves image to output/extension_graph.png

    Args:
        graph (dict):
            Extension → connected extensions.
    """

    G = nx.Graph()

    # Helper to clean extension names
    def clean_name(ext):
        return ext.replace("rv32_", "").replace("rv64_", "")

    # Build graph
    for node, neighbors in graph.items():
        node_clean = clean_name(node)

        for neighbor in neighbors:
            neighbor_clean = clean_name(neighbor)
            G.add_edge(node_clean, neighbor_clean)

    # Create layout
    pos = nx.spring_layout(G, k=1.2, seed=42)

    # Ensure output folder exists
    output_path = Path("output/extension_graph.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Plot
    plt.figure(figsize=(14, 10))

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=1500,
        font_size=7,
        edge_color="gray"
    )

    plt.title("RISC-V Extension Relationship Graph", fontsize=14)

    # Save image
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"\n\nGraph saved to: {output_path}\n")
