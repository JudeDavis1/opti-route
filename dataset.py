import csv
import time

from typing import List

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
        self.dataset: List[Dataset] = []
    
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


def test_loader():
    print('Compiling data...')
    
    start = time.time()
    ld = Loader(config.CSV_FILE)
    ld.compile()

    print(f'Compiled {len(ld.dataset)} rows in {(time.time() - start):.3f} seconds.')



if __name__ == '__main__':
    test_loader()