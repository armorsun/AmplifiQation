import os
import qiskit as qt
from qiskit import QuantumCircuit, Aer
from qiskit.compiler import transpile
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import Estimator, QiskitRuntimeService, Session
from qiskit import IBMQ

class RNG:
    # _backend: 0 for local simulator, 1 for IBM sim, 2 for QC
    backend: str

    def __init__(self, token: str, backend: int) -> None:
        IBMQ.save_account(token)
        IBMQ.load_account()
        provider = IBMQ.get_provider(hub='ibm-q')
        if backend == 0:
            self.backend = provider.get_backend('ibm_nairobi')
        elif backend == 1:
            self.backend = provider.get_backend('simulator_stabilizer')
        else:
            self.backend = Aer.get_backend('qasm_simulator')

    def randomizer_circuit(self, num_qubits: int) -> int:
        """Returns a rand int based on num_qubits available"""
        circuit = QuantumCircuit(num_qubits, num_qubits)
        for i in range(num_qubits):
            circuit.h(i)
        for i in range(num_qubits):
            circuit.measure(i, i)

        job = qt.execute(circuit, backend=self.backend, shots=1)
        counts = job.result().get_counts()
        return int(list(counts)[0], 2)
