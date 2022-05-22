import csv
import time
import numpy as np

from typing import *

# Local
import config


class Row:

    def __init__(self,
                 id: int,
                 lat: float,
                 long: float,
                 postcode: str):
        self.id = id
        self.lat = lat
        self.long = long
        self.postcode = postcode

    def __repr__(self):
        return f'Row(\n\tid: {self.id},\n\tlat: {self.lat},\n\tlong: {self.long},\n\tpostcode: {self.postcode}\n)'


class Loader:

    def __init__(self, filename):
        self.filename = filename
        self.dataset: List[Row] = []
    
    def compile(self):
        with open(self.filename) as f:
            reader = csv.DictReader(f)

            for i, row in enumerate(reader):
                data = Row(
                    id=int(row['id']),
                    lat=float(row['latitude']),
                    long=float(row['longitude']),
                    postcode=row['postcode']
                )

                self.dataset.append(data)
    
    def build_graph(self):
        raise NotImplementedError
    
    def _euclid_distance(self, p1: Tuple, p2: Tuple):
        # Unpack points
        lat1, long1 = p1
        lat2, long2 = p2
        R = config.EARTH_RAD  # Approx. radius of the earth

        d_lat = np.deg2rad(lat2 - lat1)
        d_long = np.deg2rad(long2 - long1)

        d = 2 * R * np.arcsin(np.sqrt(
            np.sin(d_lat / 2) ** 2
            + np.cos(lat1) * np.cos(lat2)
            * np.sin(d_long / 2) ** 2
        ))

        return d


def test_loader():
    print('Compiling data...')
    
    start = time.time()
    ld = Loader(config.CSV_FILE)
    ld.compile()

    print(f'Compiled {len(ld.dataset)} rows in {(time.time() - start):.3f} seconds.')



if __name__ == '__main__':
    test_loader()