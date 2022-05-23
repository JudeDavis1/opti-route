import csv
import time
import numpy as np

from typing import *
from tqdm import tqdm

# Local
import config

from search import *


class Row:

    def __init__(self,
                 id: int,
                 coord: tuple,
                 postcode: str):
        self.id = id
        self.coord = coord
        self.postcode = postcode

    def __repr__(self):
        return f'Row(\n\tid: {self.id},\n\tlat: {self.lat},\n\tlong: {self.long},\n\tpostcode: {self.postcode}\n)'


class Loader:

    def __init__(self, filename):
        self.filename = filename
        self.nodes: List[Node] = []
        self.dataset: List[Row] = []
        self.csv_len = 0
        self.max_rows = 1000
    
    def compile(self):
        with open(self.filename) as f:
            reader = csv.DictReader(f)

            for row in reader:
                data = Row(
                    id=int(row['id']),
                    coord=(float(row['latitude']), float(row['longitude'])),
                    postcode=row['postcode'].strip()
                )

                self.csv_len += 1
                self.dataset.append(data)
                self.nodes.append(Node(data.postcode))

                if self.csv_len == self.max_rows:
                    break
    
    def build_graph(self) -> Graph:
        graph = Graph()

        try:
            assert len(self.dataset) == len(self.nodes)
        except AssertionError:
            raise ValueError('Length of dataset != length of nodes')
        
        for i, row1 in (t := tqdm(enumerate(self.dataset), desc='Building graph', total=len(self.dataset))):
            for j, row2 in enumerate(self.dataset):
                graph.add(Edge(
                    cost=self._euclid_distance(row1.coord, row2.coord),
                    from_to=(self.nodes[i], self.nodes[j])
                ))
            
            t.update(1)
        
        return graph
    
    def _euclid_distance(self, p1: Tuple, p2: Tuple) -> float:
        # Unpack points
        lat1, long1 = p1
        lat2, long2 = p2
        D = config.EARTH_DIA  # Approx. diameter of the earth

        d_lat = np.deg2rad(lat2 - lat1)
        d_long = np.deg2rad(long2 - long1)

        a = np.sin(d_lat / 2) ** 2\
            + np.cos(np.deg2rad(lat1)) * np.cos(np.deg2rad(lat2))\
            * np.sin(d_long / 2) ** 2

        d = D * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        
        if str(d) == 'nan':
            print('nan')

        return d


def test_loader():
    print('Compiling data...')
    
    start = time.time()
    ld = Loader(config.CSV_FILE)
    ld.compile()

    print(f'Compiled {len(ld.dataset)} rows in {(time.time() - start):.3f} seconds.')
    print(f"{ld._euclid_distance(ld.dataset[0].coord, ld.dataset[-1].coord):.3f}")

    graph = ld.build_graph()

    print('Compiling graph...')
    graph.compile()


if __name__ == '__main__':
    test_loader()
