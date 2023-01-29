import scipy as sp
import covalent as ct
import numpy as np
import sklearn
import os
from sklearn.neighbors import DistanceMetric
from randomizer import RNG

class Hamiltonian:
    """
    Generates a dict of costs
    events: A pandas DataFrame
    """
    # df:
    # rng: RNG

    def __init__(self, df):
        self.df = df;

    def _generate_data(self):
        df = self.df[['name', 'latitude', 'longitude']].copy()
        self.df_new = df

    def _convert_to_rad(self):
        self.df_new[['lat_radians', 'long_radians']] = (
                    np.radians(self.df_new.loc[:, ['latitude', 'longitude']]))
        self.df_new['index_col'] = self.df_new.index

    @ct.electron
    def _get_random_events(self, num_event: int):
        token = os.environ["IBM_QUANTUM_TOKEN"]
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
    def get_distance_matrix(self, num_event: int):
        self._generate_data()
        self._convert_to_rad()
        temp_df = self._get_random_events(num_event)
        dist = sklearn.neighbors.DistanceMetric.get_metric('haversine')
        d = dist.pairwise(temp_df[['lat_radians', 'long_radians']],
                          temp_df[['lat_radians', 'long_radians']])
        return d


if __name__ == "__main__":
    pass
    #file = 'out.csv'
    #ham = Hamiltonian(file)
    #dist_matrix = ham.get_distance_matrix(4)
    #print(dist_matrix)



