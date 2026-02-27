from typing import List
import sympy
import numpy as np
import matplotlib.pyplot as plt
import cirq

import cirq_google
import networkx as nx

from cirq.contrib.svg import SVGCircuit

"""Test file for Google's implementation of QAOA on Sycamore."""

working_device = cirq_google.Sycamore
print(working_device)

# Random seed to determine problem instance
np.random.seed(seed=11)

# Identify working qubits
device_qubits = working_device.metadata.qubit_set
working_qubits = sorted(device_qubits)[:12]

# Populate networkx graph with nodes
working_graph = working_device.metadata.nx_graph.subgraph(working_qubits)


## Add random weights to edges of the graph.
## Each weight is a 2 decimal floating point between 0 and 5.

nx.set_edge_attributes(
    working_graph,
    {e: {"weight": np.random.randint(0, 500) / 100} for e in working_graph.edges}
)

# Draw the working_graph on a 2D grid
pos = {q: (q.col, -q.row) for q in working_graph.nodes()}

## Shape is a hexagon for fun. node_shape = "h"
nx.draw(working_graph, pos = pos, with_labels=True,node_shape = "h", node_size = 1000)
plt.show()


# Symbols for the rotation angles in the QAOA circuit.
alpha = sympy.Symbol("alpha")
beta = sympy.Symbol("beta")

qaoa_circuit = cirq.Circuit(
    # Prepare uniform superposition on working_qubits == working_graph.nodes
    cirq.H.on_each(working_graph.nodes()),
    # Do ZZ operations between neighbors u, v in the graph. Here, u is a qubit,
    # v is its neighboring qubit, and w is the weight between these qubits.
    (
        cirq.ZZ(u, v) ** (alpha * w["weight"])
        for (u, v, w) in working_graph.edges(data=True)
    ),
    # Apply X operations along all nodes of the graph. Again working_graph's
    # nodes are the working_qubits. Note here we use a moment
    # which will force all of the gates into the same line.
    cirq.Moment(cirq.X(qubit) ** beta for qubit in working_graph.nodes()),
    # All relevant things can be computed in the computational basis.
    (cirq.measure(qubit) for qubit in working_graph.nodes()),
)
SVGCircuit(qaoa_circuit)
print(qaoa_circuit)
