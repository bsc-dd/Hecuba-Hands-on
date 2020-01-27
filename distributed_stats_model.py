import random
import string
import numpy as np

from hecuba import config, StorageDict


class Data(StorageDict):
    '''
    @TypeSpec dict<<key:int>, val1:str, val2:float, val3:bool>
    '''


def gen_random_data(name, rows):
    config.session.execute(f"DROP TABLE IF EXISTS {name}")

    data = Data(name)

    normal = np.random.normal(loc=50.0, scale=15.0, size=rows)
    for i in range(rows):
        N = random.randint(0, 15)
        val1 = ''.join(random.choice(string.ascii_lowercase) for _ in range(N))
        val2 = normal[i]
        val3 = (i % 3 == 0)

        data[i] = [val1, val2, val3]
