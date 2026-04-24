import numpy as np
import time
from src.graph import generate_random_graph, cut_value
from src.baselines import brute_force, greedy
from src.qaoa import run_qaoa
from src.viz import draw_graph, draw_cut

def run_experiment(n, edge_prob = 0.5, seed = None, grid_size = 5, repetitions = 20000):
    """
    Run all three methods on a single random graph and return results
    """
    # Generate weighted edges
    edges_unweighted = generate_random_graph(n, edge_prob = edge_prob, seed = seed)
    rng = np.random.default_rng(seed)
    edges = [(u, v, round(rng.uniform(0, 5), 2)) for u, v in edges_unweighted]

    print(f"\nGraph: {n} nodes, {len(edges)} edges")
    print(f"Edges: {edges}")

    # Brute Force
    print("\nRunning Brute Force...")
    bf_start = time.time()
    bf_bits, bf_val = brute_force(n, edges)
    bf_time = time.time() - bf_start
    print(f"Brute Force Cut Value: {bf_val} ({bf_time:.3f}s)")


    #Greedy
    print("\nRunning Greedy...")
    gr_start = time.time()
    gr_bits, gr_val = greedy(n, edges)
    gr_time = time.time() - gr_start
    print(f"Greedy Cut Value: {gr_val} ({gr_time:.3f}s)")

    # QAOA
    print("\nRunning QAOA...")
    qa_start = time.time()
    qa_bits, qa_val = run_qaoa(n, edges, grid_size = grid_size, repetitions = repetitions)
    qa_time = time.time() - qa_start
    print(f"QAOA Cut Value: {qa_val} ({qa_time:.3f}s)")

    # Approximation ratios relative to brute force optimal
    gr_ratio = gr_val / bf_val if bf_val > 0 else 0
    qa_ratio = qa_val / bf_val if bf_val > 0 else 0

    print(f"\n--- Results for n={n} ---")
    print(f"Brute Force (optimal): {bf_val}")
    print(f"Greedy: {gr_val} (ratio: {gr_ratio:.3f} time: {gr_time:.3f}s)")
    print(f"QAOA:   {qa_val} (ratio: {qa_ratio:.3f} time: {qa_time:.3f}s)")


    # Visualization of graph and cuts
    draw_graph(edges, n, title=f"Graph (n={n}")
    draw_cut(n, edges, bf_bits, title=f"Brute Force Cut - {bf_val:.2f}")
    draw_cut(n, edges, gr_bits, title=f"Greedy Cut - {gr_val:.2f}")
    draw_cut(n, edges, qa_bits, title=f"QAOA Cut - {qa_val:.2f}")

    return {
        "n": n,
        "edges": edges,
        "brute_force": {"bitstring": bf_bits, "cut_value": bf_val, "time": bf_time},
        "greedy":      {"bitstring": gr_bits, "cut_value": gr_val, "ratio": gr_ratio, "time": gr_time},
        "qaoa":        {"bitstring": qa_bits, "cut_value": qa_val, "ratio": qa_ratio, "time": qa_time}
    }

def run_scaling_experiment(node_sizes, edge_prob = 0.5, seed = 42, grid_size = 5, repetitions = 20000):
    """
    Run experiments for multiple graph sizes and summarize scaling behavior.
    """

    all_results = []

    for n in node_sizes:
        result = run_experiment(
            n,
            edge_prob = edge_prob,
            seed = seed,
            grid_size = grid_size,
            repetitions = repetitions
        )
        all_results.append(result)

    # Summary table
    print("\n\n=== Scaling Summary ===")
    print(f"{'n':>4}  {'Brute Force':>12}  {'Greedy':>8}  {'Greedy Ratio':>13}  {'QAOA':>8}  {'QAOA Ratio':>11}")
    print("-" * 65)
    for r in all_results:
        print(
            f"{r['n']:>4}  "
            f"{r['brute_force']['cut_value']:>12.3f}  "
            f"{r['brute_force']['time']:>7.3f}s  "
            f"{r['greedy']['cut_value']:>8.3f}  "
            f"{r['greedy']['ratio']:>13.3f}  "
            f"{r['greedy']['time']:>7.3f}s  "
            f"{r['qaoa']['cut_value']:>8.3f}  "
            f"{r['qaoa']['ratio']:>11.3f}"
            f"{r['qaoa']['time']:>7.3f}s"
        )
    
    return all_results

if __name__ == "__main__":
    run_scaling_experiment(node_sizes = [4, 6, 8, 10, 15])

