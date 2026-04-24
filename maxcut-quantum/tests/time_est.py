"""
This serves as a time estimator for further n values of QAOA and Brute Force.
"""

import numpy as np

def format_time(seconds):
    ### Convert seconds to readable format
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.2f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.2f} hours"
    else:
        return f"{seconds/86400:.2f} days"
    
def estimate_from_multiple(measurements, target_sizes, label=""):
    """
    Estimate runtime using multiple measured data points.
    Fits a curve to the measurments for projection.
    """

    ns = np.array([m[0] for m in measurements])
    times = np.array([m[1] for m in measurements])

    # Fit log-linear model: log(time) = a*n + b
    log_times = np.log(times)
    coeffs = np.polyfit(ns, log_times, 1)
    a, b = coeffs

    print(f"\n === {label} Runtime Estimates (multi-point fit) ===")
    print(f"Known measurements:")
    for n, t in measurements:
        print(f"  n={n:>3}: {format_time(t)}")
    print(f"Fitted scaling base: {np.exp(a):.3f}x per additional node (theoretical: 2.000x)")
    print("-" * 45)
    for target_n in target_sizes:
        estimated = np.exp(a * target_n + b)
        print(f"n={target_n:>3}:  {format_time(estimated)}")


if __name__ == "__main__":
    TARGET_SIZES = [35, 40, 45, 50]

    # Plug in actual measured times here
    bf_measurements = [
        (4, 0.001),
        (6, 0.001),
        (8, 0.001),
        (10, 0.001),
        (15, 0.076),
        (20, 3.308),
        (25, 157.235),
        (30, 7058.681),
    ]

    qa_measurements = [
        (4, 0.936),   
        (6, 1.294),   
        (8, 2.054),   
        (10, 2.054),   
        (15, 3.374),   
        (20, 6.663),   
        (25, 131.803),
        (30, 6181.511),   
    ]

estimate_from_multiple(bf_measurements, TARGET_SIZES, label="Brute Force")
estimate_from_multiple(qa_measurements, TARGET_SIZES, label="QAOA")