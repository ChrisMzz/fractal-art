import sys
sys.path.insert(0, '.')
import numpy as np
import fractalize as frctl
import matplotlib.pyplot as plt
import os



EXPCE_NAME = 'test'
FUNC_PATH = fr'EXPCE\{EXPCE_NAME}\validated\functions'

funcs = []
for f in os.listdir(FUNC_PATH):
    funcs.append(np.load(fr'{FUNC_PATH}\{f}'))
    
for func in funcs:
    pred = frctl.julia_from_2Darray(func, (2048,2048))
    plt.imshow(pred)
    plt.show()

