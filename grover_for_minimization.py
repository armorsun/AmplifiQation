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
from qiskit.circuit.library import GroverOperator, HGate
from qiskit.providers.aer import QasmSimulator
from qiskit.visualization import plot_histogram

import matplotlib.pyplot as plt

from numpy import pi as pi
from typing import List

from qft import qft


def minimization_oracle(circuit: QuantumCircuit, data_register_q: QuantumRegister,
                        ancillary_register_q: QuantumRegister, arr: List[int], x: int) -> QuantumCircuit:
    """
    Marking oracle that flips the sign of elements that satisfy the minimization condition.
        That is: mark states |i> (take |i> to -|i> if arr[i] < x).

    :param circuit:
    :param data_register_q:
    :param ancillary_register_q:
    :param arr:
    :param x:
    :return:
    """
    # We need one wire in the data register for each element of arr.
    number_of_data_qubits_required = len(arr)
    data_register_q = QuantumRegister(number_of_data_qubits_required, 'data_q')

    # Measurment results from the data register will go here.
    data_register_c = ClassicalRegister(number_of_data_qubits_required, "data_c")

    # We need enough ancillary qubits to represent 0 -> sum(arr) or x, whichever is larger.
    #  Recall you can represent up to 2^n - 1 with n bits.
    number_ancillary_qubits_required = max(math.ceil(math.log(sum(arr) + 1, 2)), math.ceil(math.log(x + 1, 2)))
    ancillary_register_q = QuantumRegister(number_ancillary_qubits_required, 'ancillary_q')
    # Ancillary bits are just work bits, we won't need to measure them.

    print("Data Register:")
    print(data_register_q)
    print("Ancillary Register:")
    print(ancillary_register_q)

    oracle_circuit = QuantumCircuit(ancillary_register_q, data_register_q)
    oracle_circuit_for_cleanup = oracle_circuit.copy()

    # Conditionally load all the values in arr onto the axcillary register.
    oracle_circuit = load_values_in_arr(circuit=oracle_circuit, n_ancillary_qubits=number_ancillary_qubits_required,
                                        n_data_qubits=number_of_data_qubits_required, arr=arr)

    # Draw the circuit.
    oracle_circuit.draw(output='mpl')
    plt.show()




    # # Loop thorugh all integers in the range 1 to x-1. Notice we start at 1 because the all 0's state would always be
    # #  marked. Anyway, in the TSP context arr should never contain any 0's. If we get a sum of elements on the
    # #  ancillary wires that is < x, then there must be at least one element in arr that is less than x.
    # for i in range(1, x):
    #
    #     # qml.FlipSign(i, wires=ancillary_register)
    #     # # To improve sucess, we replace the phase inversion by a phase rotation through phi.
    #
    #     # Implement flip_sign in pauli primatives
    #     arr_bin = to_list(n=i, n_wires=len(ancillary_register))  # Turn i into a state.
    #
    #     if arr_bin[-1] == 0:
    #         qml.PauliX(wires=ancillary_register[-1])
    #
    #     qml.ctrl(qml.PauliZ, control=ancillary_register[:-1], control_values=arr_bin[:-1])(
    #                  wires=ancillary_register[-1])
    #
    #     if arr_bin[-1] == 0:
    #         qml.PauliX(wires=ancillary_register[-1])

    qml.adjoint(fn=load_values_in_arr)()  # Cleanup.


def load_values_in_arr(circuit: QuantumCircuit, n_ancillary_qubits: int, n_data_qubits: int, arr: List[int]):
    """
    Conditionally load all the values in arr onto the axcillary register.
    """
    circuit_for_recovery = circuit.copy()

    # Perform a QFT, so we can add values in the Fourier basis.
    qft(circuit=circuit, n=n_ancillary_qubits)

    # Loop through each of the data wires, preforming controlled additions.
    for j in range(n_data_qubits):
        print(j)
        data_reg_q = QuantumRegister(n_data_qubits, 'data_q')
        ancillary_reg_q = QuantumRegister(n_ancillary_qubits, 'ancillary_q')

        k_addition_circuit = QuantumCircuit(ancillary_reg_q, data_reg_q)
        for n in range(n_ancillary_qubits):
            k_addition_circuit.crz(arr[j] * pi / (2 ** j), n_ancillary_qubits + j, n)
        # custom_rotation = k_addition_circuit.to_gate().control(num_ctrl_qubits=1)
        circuit = circuit.compose(k_addition_circuit)

        # controlled_rotation = add_k_fourier(k=arr[j], wires=ancillary_register_q).control(2)
        # minimization_oracle.ctrl(op=add_k_fourier(k=arr[j], wires=ancillary_register_q), control=data_register_q[j])

    # Return to the computational basis.
    adjoint_circuit = qft(circuit=circuit_for_recovery, n=n_ancillary_qubits).inverse()
    circuit = circuit.compose(adjoint_circuit)

    return circuit


def add_k_fourier(circuit: QuantumCircuit, k: int, reg: QuantumRegister) -> None:
    """
    Add the integer value k to wires.
    :return: None, operation is done in place.
    """
    k_addition_circuit = QuantumCircuit(2)

    for j in reg.size():
        circuit.rz(phi=k * pi / (2 ** j), qubit=reg[j])
        to_gate().num_ctrl_qubits=1


def minimization_circuit(arr: List[int], x: int) -> QuantumCircuit:
    """
    Build a quantum minimization circuit.

    :param arr: list of ints.
    :param x: int.

    :return: Minimization circuit.
    """
    # We need one wire in the data register for each element of arr.
    number_of_data_qubits_required = len(arr)
    data_register_q = QuantumRegister(number_of_data_qubits_required, 'data_q')

    # Measurment results from the data register will go here.
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

    # Step 1: Create an equal superposition by applying a Hadamard to each wire in the data register.
    for wire in data_register_q:
        circuit.h(wire)

    circuit.barrier(data_register_q)

    # Upon measurment at the
    j = 1
    for _ in range(j):
        # Step 2: Use the oracle to mark solution states.
        oracle = minimization_oracle(circuit=circuit, data_register_q=data_register_q,
                                     ancillary_register_q=ancillary_register_q, arr=arr, x=x)

        grover_op = GroverOperator(oracle=oracle, insert_barriers=True)

        # Step 3: Apply the Grover operator to amplify the probability of getting the correct solution.
        circuit.GroverOperator(wires=data_register)

    circuit.measure(data_register_q, data_register_c)

    return circuit


def grover_for_minimization(arr: List[int], x: int) -> bool:
    """
    Use Grover's search to check if arr contains an element < x.

    Important Precondition:
        arr must contain integer values strickly > 0.

    :return: bool:
        True: We found an element in arr < x.
        False: otherwise.
    """
    circuit = minimization_circuit(arr=arr, x=x)

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
