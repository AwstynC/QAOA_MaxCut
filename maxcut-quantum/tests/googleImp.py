from typing import List
import sympy
import numpy as np
import matplotlib.pyplot as plt
import cirq

import cirq_google
import networkx as nx

from cirq.contrib.svg import SVGCircuit

## Blog point: implementation of pandas on 28 Feb 2026
import pandas as pd


"""Test file for Google's implementation of QAOA on Sycamore."""

working_device = cirq_google.Sycamore
# print(working_device)

# Set the seed to determine the problem instance.
np.random.seed(seed=11)

# Identify working qubits from the device.
device_qubits = working_device.metadata.qubit_set
working_qubits = sorted(device_qubits)[:12]

# Populate a networkx graph with working_qubits as nodes.
working_graph = working_device.metadata.nx_graph.subgraph(working_qubits)

# Add random weights to edges of the graph. Each weight is a 2 decimal floating point between 0 and 5.
nx.set_edge_attributes(
    working_graph,
    {e: {"weight": np.random.randint(0, 500) / 100} for e in working_graph.edges},
)

# Draw the working_graph on a 2d grid
pos = {q: (q.col, -q.row) for q in working_graph.nodes()}
nx.draw(working_graph, pos=pos, with_labels=True, node_size=1000)
#plt.show()


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


## Blog point coding: implementation of pandas on 28 Feb 2026
### Calculate the expected value of the QAOA cost Hamiltonion

def estimate_cost(graph: nx.Graph, samples: pd.DataFrame) -> float:
    """Estimate the cost function of the QAOA on the given graph using the
    provided computational basis bitstrings."""
    cost_value = 0.0

    # Loop over edge pairs and compute contribution.
    for u, v, w in graph.edges(data=True):
        u_samples = samples[str(u)]
        v_samples = samples[str(v)]

        # Determine if it was a +1 or -1 eigenvalue.
        u_signs = (-1) ** u_samples
        v_signs = (-1) ** v_samples
        term_signs = u_signs * v_signs

        # Add scaled term to total cost.
        term_val = np.mean(term_signs) * w["weight"]
        cost_value += term_val

    return -cost_value

alpha_value = np.pi / 4
beta_value = np.pi / 2
sim = cirq.Simulator()

sample_results = sim.sample( qaoa_circuit, params = {alpha: alpha_value, beta: beta_value}, repetitions = 20000)

print (f"Alpha = {round(alpha_value, 3)} Beta = {round(beta_value, 3)}")
print (f"Estimated cost: {estimate_cost(working_graph, sample_results)}")

"""Outer Loop Optimization"""

grid_size = 5

alpha_sweep = cirq.Linspace(alpha, 0, 2 * np.pi, grid_size)
beta_sweep = cirq.Linspace(beta, 0, 2 * np.pi, grid_size)
samples = sim.run_sweep(
    qaoa_circuit, params=alpha_sweep * beta_sweep, repetitions=20000
)

### Can increase the grid size to get more granularity and smoothness.
exp_values = np.reshape(samples, (-1, grid_size)).tolist()
estimate = np.vectorize(lambda s: estimate_cost(working_graph, s.data))
exp_values = estimate(exp_values)
par_tuples = [tuple(y[1] for y in x) for x in (alpha_sweep * beta_sweep).param_tuples()]
par_values = np.reshape(par_tuples, (-1, grid_size, 2))


plt.title("Heatmap of QAOA Cost Function Value")
plt.xlabel(r"$\alpha$")
plt.ylabel(r"$\beta$")
plt.imshow(exp_values)
plt.show()


"""Compare the cuts"""

def output_cut(s_partition: List[cirq.Qid]) -> None:
    """Plot and output the graph cut info."""

    # Generate the colors
    coloring = []
    for node in working_graph:
        if node in s_partition:
            coloring.append("blue")
        else:
            coloring.append("red")
    
    #Get weights
    edges = working_graph.edges(data=True)
    weights = [w["weight"] for (u, v, w) in edges]

    nx.draw_circular(
        working_graph,
        node_color = coloring,
        node_size = 1000,
        with_labels = True,
        width = weights,
    )
    plt.show()
    size = nx.cut_size(working_graph, s_partition, weight = "weight")
    print(f"Cut size: {size}")

#output_cut([])

best_exp_index = np.unravel_index(np.argmax(exp_values), exp_values.shape)
print(best_exp_index, type(best_exp_index))
best_parameters = par_values[best_exp_index]
print(f"Best control parameters: {best_parameters}")
