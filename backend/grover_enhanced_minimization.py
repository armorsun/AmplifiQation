"""
Author: AmplifiQation

iQuHACK 2023

Find the minimum value in a list using the Durr & Hoyer Quantum algorithm for minimzation:
C. Durr and P. Hoyer, “A Quantum Algorithm for Finding the Minimum,” 1996, doi: 10.48550/arxiv.quant-ph/9607014.
"""

from grover_for_minimization import grover_for_minimization

def grover_enhanced_minimization(arr: list[int], _lower_bound: int = 0, _upper_bound: int = None,
                                 verbose: bool = False) -> int:
    """
    Use the Durr & Hoyer Quantum algorithm for minimization to find the minimum
    value in arr.
    This algorithm is basically just binary search on-top of Grover's search.
    Query complexity:
        Let m = initial_upper_bound - initial_lower_bound = arr[0] - 0
        Let n = len(arr)
        Binary search: O(log(m))
        Grover: O(sqrt(n))
        Total: O(log(m) * sqrt(n))
    # TODO: Expand functionality to encompase all comparable types.
    :param arr: list of positive ints:
        A list of input values >= 0. We are searching for the minimum.
    :param verbose: bool (optional; default is False):
        Print our extra information - useful for debugging.
    :return: int:
        The smallest value in arr.
    """

    if _upper_bound is None:
        # First iteration. For an initial upper bound, just use the first element in arr. Worst case, this is the
        #  biggest element.
        _upper_bound = arr[0]
        if _lower_bound > _upper_bound:
            raise Exception("Error: The initial_bound must be less than arr[0].")

    if verbose:
        print("\nLower bound: " + str(_lower_bound))
        print("Upper bound: " + str(_upper_bound))

    # We keep going till the upper and lower bounds cross.
    if _upper_bound >= _lower_bound:
        middle = (_upper_bound + _lower_bound) // 2

        # Using Grover, check if there is an element smaller than the middle value.
        # smaller_element_exists = grover_for_minimization_classical(arr=arr, x=middle)
        smaller_element_exists = grover_for_minimization(arr=arr, x=middle)

        if smaller_element_exists:
            # There is at least one element smaller than middle, lower our upper bound.
            if verbose:
                print("Smaller element found, lowering our upper bound...")
            return grover_enhanced_minimization(arr, _lower_bound=_lower_bound,
                                                _upper_bound=middle - 1,
                                                verbose=verbose)

        else:
            # There are no elements smaller than middle, raise the lower bound.
            if verbose:
                print("No smaller element found, raising our lower bound...")
            return grover_enhanced_minimization(arr, _lower_bound=middle + 1,
                                                _upper_bound=_upper_bound,
                                                verbose=verbose)

    else:
        # Bounds have crossed, return the solution.
        return _upper_bound


def grover_for_minimization_classical(arr: list[int], x: int) -> bool:
    """
    This is a classical function that performs the same function as
    grover_for_minimization(). That is, check if arr contains an element < x.
    This is just used for testing to make sure the classical
    grover_enhanced_minimization() overhead is working as expected.
    :return: bool:
        True: We found an element in arr < x.
        False: otherwise.
    """
    for i in range(len(arr)):
        if arr[i] < x:
            return True  # We have found a smaller value!

    return False  # No element in list > middle


if __name__ == "__main__":

    # test_array = [27, 15, 17, 16, 3, 45, 9]
    test_array = list(range(0, 100000))
    test_array.reverse()  # Engineer the worst case scenario - when the first element in the list is the largest.

    # print(test_array)
    grover_enhanced_minimization(arr=test_array, verbose=False)

    #
    # results = [0] * 100
    # for i in range(100):
    #     results[i] = grover_enhanced_minimization(arr=test_array, verbose=True)
    #     print("###")
    #     print("MIN: " + str(results[i]))
    #     print("###")
    #
    # print(results)
