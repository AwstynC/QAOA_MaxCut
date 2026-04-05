### Baseline comparison algorithms for maxcut problem.

from src.graph import cut_value, int_to_bitlist

def brut_force(n, edges):
    """
    Find the max cut by extensively checking all 2^n bitstrings.
    Practicality: Small graph of n <= 20.
    Returns: Best bitstring and its cut value.
    """
    best_bits = None
    best_val = -1

    for x in range(2 ** n):
        bits = int_to_bitlist(x, n)
        val = cut_value(bits, edges)
        if val > best_val:
            best_val= val
            best_bits = bits
    
    return best_bits, best_val

def greedy(n, edges):
    """
    Greedy max-cut heuristic. Assigns each node to the
    partition that maximizes the cut given current assignments
    Returns: bitstring and cut value.   
    """
    assignment = [0] * n
    
    for node in range(n):
        #Try node in partition 0 vs partition 1, keep the better
        assignment[node] = 0
        val0 = cut_value(assignment, edges)
        assignment[node] = 1
        val1 = cut_value(assignment, edges)
        
        if val0 >= val1:
            assignment[node] = 0
        else:
            assignment[node] = 1
    
    return assignment, cut_value(assignment, edges)