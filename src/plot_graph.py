import matplotlib.pyplot as plt
import numpy as np
from utils import get_datafilestring

with open(f'{get_datafilestring()}.csv', 'r') as f:
    data = [float(x.strip()) for x in f.readlines()]

    plt.plot(np.arange(0, len(data)), data)
    plt.grid()
    plt.savefig('temp_plot.png')
