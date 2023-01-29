"""
Author: AmplifiQation

iQuHACK 2023

# TODO:
"""


import os
import qiskit as qt
from qiskit import QuantumCircuit, Aer
from qiskit import IBMQ
# import covalent as ct


class RNG:
    """
    # TODO
    """
    # _backend: 0 for local simulator, 1 for IBM sim, 2 for QC
    backend: str

    def __init__(self, backend: int, token) -> None:
        """
        # TODO
        :param backend:
        :param token:
        """
        IBMQ.save_account(token)
        IBMQ.load_account()
        provider = IBMQ.get_provider(hub='ibm-q')
        if backend == 0:
            self.backend = provider.get_backend('ibm_nairobi')
        elif backend == 1:
            self.backend = provider.get_backend('simulator_stabilizer')
        else:
            self.backend = Aer.get_backend('qasm_simulator')

    # @ct.electron
    def randomizer_circuit(self, num_qubits: int) -> int:
        """
        Returns a random integer based on the number of qubits available.
        :param num_qubits:
        :return:
        """
        circuit = QuantumCircuit(num_qubits, num_qubits)
        for i in range(num_qubits):
            circuit.h(i)
        for i in range(num_qubits):
            circuit.measure(i, i)

        job = qt.execute(circuit, backend=self.backend, shots=1)
        counts = job.result().get_counts()
        return int(list(counts)[0], 2)
