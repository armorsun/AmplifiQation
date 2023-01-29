"""
Author: AmplifiQation

iQuHACK 2023

Sourced from https://qiskit.org/textbook/ch-algorithms/quantum-fourier-transform.html#generalqft.
"""
from math import pi


def qft_rotations(circuit, n):
    """
    Performs qft on the first n qubits in circuit (without swaps)
    :param circuit:
    :param n: int:
        Number of qubits.
    :return: None. Operation is done in place.
    """
    if n == 0:
        return circuit
    n -= 1
    circuit.h(n)
    for qubit in range(n):
        circuit.cp(pi/2**(n-qubit), qubit, n)
    # At the end of our function, we call the same function again on
    # the next qubits (we reduced n by one earlier in the function)
    qft_rotations(circuit, n)


def swap_registers(circuit, n):
    """
    Performs the swaps
    :param circuit:
    :param n: int:
        Swaps are performed on the first n qubits.
    :return: The transformed circuit.
    """
    for qubit in range(n//2):
        circuit.swap(qubit, n-qubit-1)
    return circuit


def qft(circuit, n):
    """
    QFT on the first n qubits in circuit.
    :param circuit:
    :param n:
        QFT is performed on the first n qubits
    :return: The transformed circuit.
    """
    circuit = circuit.copy()
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit
