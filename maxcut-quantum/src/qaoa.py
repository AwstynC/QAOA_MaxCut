import sympy
import numpy as np
import cirq

def build_qaoa_circuit(n, edges, alpha, beta):
    """
    Build a p=1 QAOA circuit for Max-Cut on a graph with n nodes.
    n: number of nodes
    edges: [(u, v, w)] weighted edge list
    alpha: sympy.Symbol for cost layer angle
    beta: sympy.Symbol for mixer layer angle
    Return: cirq.Circuit
    """

    qubits = cirq.LineQubit.range(n)

    circuit = cirq.Circuit(
        #Prepare uniform superposition
        cirq.H.on_each(*qubits),
        #Cost layer: ZZ interactions weighted by edge weight
        (
            cirq.ZZ(qubits[u], qubits[v]) ** (alpha * w)
            for (u, v, w) in edges
        ),
        # Mixer layer: X rotations on all qubits
        cirq.Moment(cirq.X(q) ** beta for q in qubits),
        # Measure qubits
        (cirq.measure(q) for q in qubits)
    )
    return circuit

def estimate_cost(n, edges, samples):
    """
    Estimate the QAOA cost fucntion from measurement samples.
    """
    
    cost_value = 0.0

    for u, v, w in edges:
        u_samples = samples[str(u)]
        v_samples = samples[str(v)]

        u_signs = (-1) ** u_samples
        v_signs = (-1) ** v_samples
        term_signs = u_signs * v_signs

        cost_value += np.mean(term_signts) * w

    return -cost_value

