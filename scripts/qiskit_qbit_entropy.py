"""
Fetch real q-bit measurements from IBM Quantum using Qiskit.
- Requires: pip install qiskit
- You must set your IBM Quantum API token as the environment variable IBM_QUANTUM_TOKEN
"""
import os
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_provider import IBMProvider

# Get your IBM Quantum API token from environment
API_TOKEN = os.getenv("IBM_QUANTUM_TOKEN")
if not API_TOKEN:
    raise RuntimeError("Set IBM_QUANTUM_TOKEN environment variable with your IBM Quantum API token.")

# Initialize provider
provider = IBMProvider(token=API_TOKEN)

# Pick the least busy backend with real q-bits
backends = provider.backends(simulator=False, operational=True)
backend = sorted(backends, key=lambda b: b.status().pending_jobs)[0]
print(f"Using backend: {backend.name}")

# Create a simple circuit: Hadamard on q0, then measure
qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

# Transpile and run
job = backend.run(transpile(qc, backend), shots=1)
result = job.result()
counts = result.get_counts()

# Output the measurement (0 or 1)
print(f"Qubit measurement result: {counts}")
