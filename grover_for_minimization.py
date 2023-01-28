"""
Author: AmplifiQation

iQuHACK 2023

Gover search for minimization.

L. Grover, “A fast quantum mechanical algorithm for database search,” in Proceedings of the twenty-eighth annual ACM
 symposium on theory of computing, 1996, pp. 212–219. doi: 10.1145/237814.237866.
"""
import math

import numpy as np
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.providers.aer import QasmSimulator
from qiskit.visualization import plot_histogram

import matplotlib.pyplot as plt

from numpy import pi as pi
from typing import List


def minimization_oracle(data_register: List[int], ancillary_register: List[int], arr: List[int], x: int) -> None:
    """
    Marking oracle that flips the signs of those elements that satisfies the minimization condition.
        That is: mark states |i> (take |i> to -|i> if arr[i] < x).

    :param data_register: List of ints:
        Our main data qubits.
    :param ancillary_register: List of ints:
        Our helper qubits.
    :param arr: List of ints.
    :param x: int.

    :return: None, operation is done in place.
    """

    def add_k_fourier(k: int, wires: List[int]) -> None:
        """
        Add the integer value k to wires.
        :return: None, operation is done in place.
        """
        for j in range(len(wires)):
            circuit.rz(phi=k * pi / (2 ** j), wires=wires[j])

    def load_values_in_arr():
        """
        Conditionally load all the values in arr onto the axcillary register.
        """
        # Perform a QFT, so we can add values in the Fourier basis.
        qml.QFT(wires=ancillary_register)

        # Loop through each of the data wires, preforming controlled additions.
        for wire in data_register:
            qml.ctrl(op=add_k_fourier, control=wire)(k=arr[wire], wires=ancillary_register)

        # Return to the computational basis.
        qml.adjoint(fn=qml.QFT(wires=ancillary_register))

    load_values_in_arr()

    # Loop thorugh all integers in the range 1 to x-1. Notice we start at 1 because the all 0's state would always be
    #  marked. Anyway, in the TSP context arr should never contain any 0's. If we get a sum of elements on the
    #  ancillary wires that is < x, then there must be at least one element in arr that is less than x.
    for i in range(1, x):

        # qml.FlipSign(i, wires=ancillary_register)
        # # To improve sucess, we replace the phase inversion by a phase rotation through phi.

        # Implement flip_sign in pauli primatives
        arr_bin = to_list(n=i, n_wires=len(ancillary_register))  # Turn i into a state.

        if arr_bin[-1] == 0:
            qml.PauliX(wires=ancillary_register[-1])

        qml.ctrl(qml.PauliZ, control=ancillary_register[:-1], control_values=arr_bin[:-1])(
                     wires=ancillary_register[-1])

        if arr_bin[-1] == 0:
            qml.PauliX(wires=ancillary_register[-1])

    qml.adjoint(fn=load_values_in_arr)()  # Cleanup.


def minimization_circuit(data_register: List[int], ancillary_register: List[int], arr: List[int], x: int,
                         ret: str = "sample") -> list:
    """
    A quantum circuit to find a value in arr that is less than x.

    :param data_register: List of ints:
        Our main data qubits.
    :param ancillary_register: List of ints:
        Our helper qubits.
    :param arr: list of ints.
    :param x: int.
    :param ret: str (optional; default is "sample"):
        "sample": return sample.
        "probs": return probabilities.
    :return:
    """

    # Step 1: Create an equal superposition by applying a Hadamard to each wire in the data register.
    # Add a H gate on qubit 0
    circuit.h(0)
    for wire in data_register:
        qml.Hadamard(wires=wire)

    # Compute some of the parameters defined in Long et al.
    beta = math.asin(1 / math.sqrt(len(arr)))
    j_op = math.floor((pi / 2 - beta) / (2 * beta))
    j = j_op + 1
    phi = 2 * math.asin(math.sin(pi / (4 * j + 6)) / math.sin(beta))

    print("phi: " + str(phi))
    print("j_op: " + str(j_op))
    print("j: " + str(j))
    print("beta: " + str(beta))

    # Upon measurment at the (J + 1)th iteration, the marked state is obtained with quasi-certainty.
    for _ in range(j + 1):
        # Step 2: Use the oracle to mark solution states.
        minimization_oracle(data_register=data_register, ancillary_register=ancillary_register, arr=arr, x=x, phi=pi)

        # Step 3: Apply the Grover operator to amplify the probability of getting the correct solution.
        qml.GroverOperator(wires=data_register)

    if ret == "probs":
        return qml.probs(wires=data_register)
    else:
        return qml.sample(wires=data_register)


def grover_for_minimization(arr: List[int], x: int) -> bool:
    """
    Use Grover's search to check if arr contains an element < x.

    Important Precondition:
        arr must contain integer values strickly > 0.

    :return: bool:
        True: We found an element in arr < x.
        False: otherwise.
    """
    # We need one wire in the data register for each element of arr.
    number_of_data_qubits_required = len(arr)
    data_register_q = QuantumRegister(number_of_data_qubits_required, 'data_q')

    # We will need to project measurements from
    data_register_c = ClassicalRegister(number_of_data_qubits_required, "data_c")

    # We need enough ancillary qubits to represent 0 -> sum(arr) or x, whichever is larger.
    #  Recall you can represent up to 2^n - 1 with n bits.
    number_ancillary_qubits_required = max(math.ceil(math.log(sum(arr) + 1, 2)), math.ceil(math.log(x + 1, 2)))
    ancillary_register_q = QuantumRegister(number_ancillary_qubits_required, 'ancillary_q')
    # Ancillary bits are just work bits, we won't need to measure them.

    print(data_register_q)
    print(ancillary_register_q)

    # Create a Quantum Circuit
    circuit = QuantumCircuit(data_register_q, ancillary_register_q, data_register_c)

    circuit.measure(data_register_q, data_register_c)

    # Draw the circuit
    circuit.draw(output='mpl')
    plt.show()

    # # Execute the circuit on Aer's qasm_simulator
    # simulator = QasmSimulator()
    # job = simulator.run(compiled_circuit, shots=1000)
    #
    # # Grab results from the job
    # result = job.result()
    #
    # # Returns counts
    # counts = result.get_counts(compiled_circuit)
    #

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
    # if len(found_elements) > 0:
    #     if found_elements[0] < x:
    #         # If the found value is actually less than result, great!
    #         return True
    #
    # # No such element exists.
    return False


if __name__ == "__main__":

    arr_ = [18, 10, 6, 7]
    # arr_ = [3, 5, 4, 3]
    # arr_ = [36, 5, 8, 14, 15, 2, 4, 16]
    x_ = 3

    found_number_smaller_than_x = grover_for_minimization(arr=arr_, x=x_)

    print("Found a number smaller than x: " + str(found_number_smaller_than_x))
