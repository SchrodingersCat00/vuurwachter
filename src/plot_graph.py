import matplotlib.pyplot as plt
import numpy as np
from utils import get_datafilestring
import sys

data_f = get_datafilestring() + '.csv' if len(sys.argv) == 1 else sys.argv[1]

with open(f'{data_f}', 'r') as f:
    data = [float(x.strip()) for x in f.readlines()]

    plt.plot(np.arange(0, len(data)), data)
    plt.grid()
    plt.savefig('temp_plot.png')
