"""
Author: AmplifiQation

iQuHACK 2023

Gover search for minimization.

L. Grover, “A fast quantum mechanical algorithm for database search,” in
Proceedings of the twenty-eighth annual ACM symposium on theory of computing,
1996, pp. 212–219. doi: 10.1145/237814.237866.
"""

import math

import qiskit
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister, transpile
from qiskit.circuit.library import GroverOperator
from qiskit import Aer
from qiskit.visualization import plot_histogram

import matplotlib.pyplot as plt

from numpy import pi as pi
from typing import List

from qiskit_aer import AerSimulator

from qft import qft


def minimization_oracle(arr: List[int], x: int) -> QuantumCircuit:
    """
    Marking oracle that flips the sign of elements that satisfy the minimization
    condition.
        That is: mark states |i> (take |i> to -|i> if arr[i] < x).

    :param arr: List[int]
        The list we are searching.
    :param x: int
        Our current pivot element.
    :return: QuantumCircuit:
        A marking oracle.
    """
    # We need one wire in the data register for each element of arr.
    number_of_data_qubits_required = len(arr)
    data_register_q = QuantumRegister(number_of_data_qubits_required, 'data_q')

    # We need enough ancillary qubits to represent 0 -> sum(arr) or x, whichever is larger.
    #  Recall you can represent up to 2^n - 1 with n bits.
    number_ancillary_qubits_required = max(math.ceil(math.log(sum(arr) + 1, 2)), math.ceil(math.log(x + 1, 2)))
    ancillary_register_q = QuantumRegister(number_ancillary_qubits_required, 'ancillary_q')
    # Ancillary bits are just work bits, we won't need to measure them.

    oracle_circuit = QuantumCircuit(ancillary_register_q, data_register_q)

    # Conditionally load all the values in arr onto the axcillary register.
    oracle_circuit = load_values_in_arr(circuit=oracle_circuit,
                                        n_ancillary_qubits=number_ancillary_qubits_required,
                                        n_data_qubits=number_of_data_qubits_required, arr=arr)

    oracle_circuit_for_cleanup = oracle_circuit.inverse().copy()

    # Loop thorugh all integers in the range 1 to x-1. Notice we start at 1 because the all 0's state would always be
    #  marked. Anyway, in the TSP context arr should never contain any 0's. If we get a sum of elements on the
    #  ancillary wires that is < x, then there must be at least one element in arr that is less than x.
    for i in range(1, x):

        data_register_q_for_flip = QuantumRegister(number_of_data_qubits_required,
                                                   'data_q')
        ancillary_register_q_for_flip = QuantumRegister(number_ancillary_qubits_required,
                                                        'ancillary_q')

        sign_flip_circuit = QuantumCircuit(ancillary_register_q_for_flip,
                                           data_register_q_for_flip)

        binary_list = to_list(n=i, n_wires=number_ancillary_qubits_required)

        sign_flip_circuit.initialize(i, qubits=ancillary_register_q_for_flip)

        if binary_list[-1] == 0:
            sign_flip_circuit.x(ancillary_register_q_for_flip[-1])

        # Since we don't have a controlled Z-gate, use the identity HXH = Z.
        sign_flip_circuit.h(ancillary_register_q_for_flip[-1])
        sign_flip_circuit.mcx(control_qubits=ancillary_register_q_for_flip[:-1],
                              target_qubit=ancillary_register_q_for_flip[-1])
        sign_flip_circuit.h(ancillary_register_q_for_flip[-1])

        if binary_list[-1] == 0:
            sign_flip_circuit.x(ancillary_register_q_for_flip[-1])

        oracle_circuit = oracle_circuit.compose(sign_flip_circuit)

    oracle_circuit = oracle_circuit.compose(oracle_circuit_for_cleanup)  # Cleanup.
    return oracle_circuit


def load_values_in_arr(circuit: QuantumCircuit, n_ancillary_qubits: int,
                       n_data_qubits: int, arr: List[int]):
    """
    Conditionally load all the values in arr onto the axcillary register.

    :param circuit: QuantumCircuit
    :param n_ancillary_qubits: int
        The number of ancillary qubits.
    :param n_data_qubits: int
        The number of data qubits wires.
    :param arr: List[int]
        The list we are searching.
    :return: QuantumCircuit:
        The provided circuit, except with added gates to conditionally load all
        the values in arr onto the ancillary register
    """
    circuit_for_recovery = circuit.copy()

    # Perform a QFT, so we can add values in the Fourier basis.
    qft(circuit=circuit, n=n_ancillary_qubits)

    # Loop through each of the data wires, preforming controlled additions.
    for j in range(n_data_qubits):
        data_reg_q = QuantumRegister(n_data_qubits, 'data_q')
        ancillary_reg_q = QuantumRegister(n_ancillary_qubits, 'ancillary_q')

        k_addition_circuit = QuantumCircuit(ancillary_reg_q, data_reg_q)
        for n in range(n_ancillary_qubits):
            k_addition_circuit.crz(arr[j] * pi / (2 ** j), n_ancillary_qubits + j, n)

        circuit = circuit.compose(k_addition_circuit)

    # Return to the computational basis.
    adjoint_circuit = qft(circuit=circuit_for_recovery,
                          n=n_ancillary_qubits).inverse()
    circuit = circuit.compose(adjoint_circuit)

    return circuit


def to_list(n, n_wires):
    """
    This function is copy and pasted straight out of PennyLane!
    Convert an integer into a binary integer list

    Args:
        n (int): Basis state as integer
        n_wires (int): Numer of wires to transform the basis state
    Raises:
        ValueError: "cannot encode n with n wires "
    Returns:
        (array[int]): integer binary array
    """
    if n >= 2 ** n_wires:
        raise ValueError(f"cannot encode {n} with {n_wires} wires ")

    b_str = f"{n:b}".zfill(n_wires)
    bin_list = [int(i) for i in b_str]
    return bin_list


def minimization_circuit(arr: List[int], x: int) -> QuantumCircuit:
    """
    Build the complete quantum minimization circuit to find if there exists an
    element in arr < x.

    :param arr: List[int]
    :param x: int
    :return: QuantumCircuit
    """
    # We need one wire in the data register for each element of arr.
    number_of_data_qubits_required = len(arr)
    quantum_data_register = QuantumRegister(number_of_data_qubits_required,
                                            'data_q')

    # Measurment results from the quantum data register will be projected onto classical wires.
    classical_data_register = ClassicalRegister(number_of_data_qubits_required,
                                                "data_c")

    # We need enough ancillary qubits to represent 0 -> sum(arr) or x, whichever is larger.
    #  Recall you can represent up to 2^n - 1 with n bits.
    number_ancillary_qubits_required = max(math.ceil(math.log(sum(arr) + 1, 2)),
                                           math.ceil(math.log(x + 1, 2)))
    quantum_ancillary_register = QuantumRegister(number_ancillary_qubits_required,
                                                 'ancillary_q')
    # Ancillary bits are just work bits, we won't need to measure them.

    # Create a quantum circuit
    circuit = QuantumCircuit(quantum_ancillary_register, quantum_data_register,
                             classical_data_register)

    # Grover's Search, here we go..!
    # Step 1: Create an equal superposition by applying a Hadamard to each wire in the data register.
    for wire in quantum_data_register:
        circuit.h(wire)

    circuit.barrier(quantum_data_register)  # Just to ease of visulation.

    # The optimal number of iterations requires knowledge of the number of marked elements.
    # Alternatively, we could assume a minimum number of marked elements and work our way up.
    j = 2

    for _ in range(j):
        # Step 2: Get an oracle we can use to build quantum states.
        oracle = minimization_oracle(arr=arr, x=x)

        # Step 3: Apply the Grover operator to amplify the probability of getting the correct solution.
        grover_op = GroverOperator(oracle=oracle, insert_barriers=True)

        circuit = circuit.compose(grover_op)

    # Draw the minimization oracle
    oracle.draw(output='mpl')
    plt.show()

    circuit.barrier(quantum_data_register)  # Just to ease of visulation.
    circuit.measure(quantum_data_register, classical_data_register)
    return circuit


def grover_for_minimization(arr: List[int], x: int) -> bool:
    """
    Use Grover's search to check if arr contains an element < x.
    Important Precondition:
        arr must contain integer values > 0.
    :param arr: List[int]
        List of integers that the algorithm searches
    :param x:
        Element that the algorithm checks against
    :return: bool:
        True: We found an element in arr < x.
        False: otherwise.
    """
    circuit = minimization_circuit(arr=arr, x=x)

    # Execute the circuit on the qasm simulator.
    backend = Aer.get_backend('unitary_simulator')
    qc_compiled = transpile(circuit, backend)

    job_sim = backend.run(qc_compiled, shots=1024)

    # Grab the results from the job.
    result_sim = job_sim.result()

    counts = result_sim.get_counts(qc_compiled)
    print(counts)

    # # Draw the circuit
    # circuit.draw(output='mpl')
    # plt.show()

    # print("\nlen(values):")  # Four bits can encode 16 distinct characters
    # print(len(values))
    # print("\nvalues:")
    # print(values)
    # plt.rcParams["figure.figsize"] = [7.50, 6]
    # plt.rcParams["figure.autolayout"] = True
    # plt.bar(range(len(values)), values)
    # plt.xlabel("State", fontsize=25)
    # plt.ylabel("Probability", fontsize=25)
    # plt.xticks(fontsize=20)
    # plt.yticks(fontsize=20)
    #
    # plt.show()
    #
    # # The second device is for actully obtaining a sample.
    # device2 = qml.device("default.qubit", wires=data_register + ancillary_register, shots=1)
    # qnode2 = qml.qnode(func=minimization_circuit, device=device2)(
    #     data_register=data_register, ancillary_register=ancillary_register, arr=arr, x=x, ret="sample")
    #
    # sample = qnode2.__call__(data_register=data_register, ancillary_register=ancillary_register, arr=arr, x=x,
    #                          ret="sample")
    # print(sample)
    #
    # found_elements = [i for indx, i in enumerate(arr) if sample[indx] == 1]
    # print("Found elements: " + str(found_elements))
    #
    if len(found_elements) > 0:
        if found_elements[0] < x:
            # If the found value is actually less than result, great!
            return True

    # No such element exists.
    return False


if __name__ == "__main__":

    # arr_ = [18, 10, 6, 7]
    # arr_ = [3, 5, 4, 3]
    arr_ = [36, 5, 8, 14, 15, 2, 4, 16]
    x_ = 3

    found_number_smaller_than_x = grover_for_minimization(arr=arr_, x=x_)

    print("Found a number smaller than x: " + str(found_number_smaller_than_x))
