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
    Estimate the QAOA cost function from measurement samples.
    """
    
    cost_value = 0.0

    for u, v, w in edges:
        u_samples = samples[str(u)]
        v_samples = samples[str(v)]

        u_signs = (-1) ** u_samples
        v_signs = (-1) ** v_samples
        term_signs = u_signs * v_signs

        cost_value += np.mean(term_signs) * w

    return -cost_value

def run_qaoa(n, edges, grid_size = 5, repetitions=20000):
    """
    Run QAOA for Max-Cut, sweep over alpha and beta, and return
    the best cut partition found.
    """

    alpha = sympy.Symbol("alpha")
    beta = sympy.Symbol("beta")

    circuit = build_qaoa_circuit(n, edges, alpha, beta)
    sim = cirq.Simulator()

    # Sweep alpha and beta over [0, 2*pi]
    
    alpha_sweep = cirq.Linspace(alpha, 0, 2 *np.pi, grid_size)
    beta_sweep = cirq.Linspace(beta, 0, 2 * np.pi, grid_size)
    sweep = alpha_sweep * beta_sweep

    samples = sim.run_sweep(circuit, params = sweep, repetitions = repetitions)

    # Find the best parameters from sweep
    exp_values = np.array([
        estimate_cost(n, edges, s.data) for s in samples
    ])
    best_idx = np.argmax(exp_values)
    best_params = dict(list(sweep.param_tuples())[best_idx])

    # Sample candidate cuts at best parameters
    num_cuts = 100
    candidate_cuts = sim.sample(
        circuit,
        params = {alpha: best_params["alpha"], beta: best_params["beta"]},
        repetitions = num_cuts,
    )

    # Find best cut from candidates
    best_bitstring = None
    best_cut_val = -np.inf

    for i in range(num_cuts):
        candidate = candidate_cuts.iloc[i]
        bitstring = [int(candidate[str(q)]) for q in range(n)]

        cut_val = sum(
            w for u, v, w in edges
            if bitstring[u] != bitstring[v]
        )

        if cut_val > best_cut_val:
            best_cut_val = cut_val
            best_bitstring = bitstring
    
    return best_bitstring, best_cut_val
