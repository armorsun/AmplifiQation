"""
Author: AmplifiQation

iQuHACK 2023
"""
from typing import Dict

import pandas
# import covalent as ct
import numpy as np
import sklearn
from sklearn.neighbors import DistanceMetric

from backend.hamiltonian_cycles import hamiltonian_cycle
from randomizer import RNG
from Typing import Dict

IBM_QUANTUM_TOKEN = '9e7bde2b4061405bfd573264c0b7782d144c344aaa91cd8632cd492dff71254520bdd5c5f5a1726e35d66f5e4cdc8d411698fc0424e3253436eabf817671f72d'


class DataManager:
    """
    Generates a dict of costs
    events: Pandas.DataFrame
        A pandas df of events
    """
    df: DataFrame
    rng: RNG

    def __init__(self, filepath: str):
        """
        Initialization of DataManager Class
        :param in_file: str
            string of file path
        """
        # TODO: Interface with Google maps
        self.df = pandas.read_csv(filepath)

    def _generate_data(self):
        """
        # Prepares data in a pandas DataFrame needed for other classes
        :return: None
        """
        print(self.df)
        df = self.df[['name', 'latitude', 'longitude']].copy()
        self.df_new = df

    def _convert_to_rad(self):
        """
        Converts long and lat coordinates to radians and adds an index column
        :return: None
        """
        self.df_new[['lat_radians', 'long_radians']] = (
                    np.radians(self.df_new.loc[:, ['latitude', 'longitude']]))
        self.df_new['index_col'] = self.df_new.index

    @ct.electron
    def _get_random_events(self, num_event: int):
        """
        Uses the Quantum RNG to generate a list of numbers which determine
        the events to pick up to <num_events>
        :param num_event: int
            number of events to generate
        :return: Pandas.DataFrame:
            Data frame of desired events

        """
        token = os.environ[IBM_QUANTUM_TOKEN]
        backend = 2
        self.rng = RNG(backend, token)
        binary_len = len(format(num_event, 'b'))

        if 2**binary_len - 1 > num_event:
            binary_len -= 1

        temp_lst = []
        for i in range(num_event):
            temp_lst.append(self.rng.randomizer_circuit(binary_len))

        temp_df = self.df_new.filter(items=temp_lst, axis=0)

        return temp_df

    @ct.electron
    def build_cost_matrix(self, num_event: int) -> List[List]:
        """
        Builds a matrix of all distances between any two events of size
        <num_events>
        :param num_event:
            Size of matrix to generate
        :return:
            Cost Matrix of desired size
        """
        self._generate_data()
        self._convert_to_rad()
        temp_df = self._get_random_events(num_event)
        dist = sklearn.neighbors.DistanceMetric.get_metric('haversine')
        d = dist.pairwise(temp_df[['lat_radians', 'long_radians']],
                          temp_df[['lat_radians', 'long_radians']])
        return d

    def build_hamiltonian_cycle_dict(self, n_events: int = 5) -> Dict[str, float]:
        """
        Build a dictionary of Hamiltonian cycles.

        :param n_events: int (optional; default is 5):
            The number of events to use.

        :return: dict:
            keyed by the Hamiltonian cycles (as strings)
            values are the costs (as floats)

        """
        cost_matrix = self.build_cost_matrix(n_events)
        # Generate Hamiltonian cycles in file
        hamiltonian_cycle(cost_matrix)

        # Read in Hamiltonian cycles from file
        import pathlib
        ham_cycle_in_dir = str(pathlib.Path().resolve().parent.resolve()) + "\\data"
        ham_cycle_in_file = ham_cycle_in_dir + "\\hamiltonian_cycles_temp.txt"

        my_file = open(ham_cycle_in_file, 'r')
        lines = my_file.readlines()

        # Build up an array of Hamiltonian cycles.
        hamiltonian_cycle_arr = []
        for line in lines:
            hamiltonian_cycle_arr.append(line.strip())  # Strip the newline characters.

        # Compute costs for each cycle.
        costs = [0] * len(hamiltonian_cycle_arr)
        for i, cycle in enumerate(hamiltonian_cycle_arr):
            stops = cycle.split(" ")
            len_stops = len(stops)

            for j, stop in enumerate(stops):
                if j < len_stops - 1:
                    costs[i] += cost_matrix[int(stops[j]), int(stops[j + 1])]

        # Build a dictionary.
        res = {}
        for key in hamiltonian_cycle_arr:
            for value in costs:
                res[key] = value
                costs.remove(value)
                break

        return res


if __name__ == "__main__":
    import pathlib
    in_dir = str(pathlib.Path().resolve().parent.resolve()) + "\\data"
    in_file = in_dir + '/out.csv'

    data_manager = DataManager(in_file)
    cost_matrix = data_manager.build_cost_matrix(7)
    print(np.round(cost_matrix, 5))

    res = data_manager.build_hamiltonian_cycle_dict()
    print(res)
