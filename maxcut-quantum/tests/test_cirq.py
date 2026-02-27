import cirq

q = cirq.LineQubit(0)
circuit = cirq.Circuit(cirq.H(q), cirq.measure(q, key="m"))

sim = cirq.Simulator()
result = sim.run(circuit, repetitions=10)

print("Circuit:")
print(circuit)
print("\nResults:")
print(result)