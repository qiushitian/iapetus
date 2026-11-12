"""
The single file you need to run to make all outputs.

Authors: Qiushi Chris Tian, Audrey Whitmer
Updated: 2026-11-12
"""

from pathlib import Path
import sys

import astropy
import numpy as np
import matplotlib
import amuse

from initialize import make_system
from utils import print_cyan, print_green  # , spinner


SAVE_DIR = Path('outputs/')


if __name__ == '__main__':
    SAVE_DIR.mkdir(exist_ok=True)

    print(f'Python {sys.version}')
    print(
        f'AMUSE {amuse.__version__}, Astropy {astropy.__version__}, '
        f'Matplotlib {matplotlib.__version__}, Numpy {np.__version__}'
    )

    print()
    print_cyan('Can the Equatorial Ridge on Iapetus Form from a Debris Disk?')
    print('  by Ankita Dasgupta, Audrey Whitmer, and Qiushi Chris Tian')
    print()

    # print(
    #     "Note:\tIt's normal that the progress spinner will appear dead\n"
    #     '\tfor a few minutes. It is still running.'
    # )
    # print()

    print_green('----- Initialization -----')

    # with spinner('Creating solar system'):
    system = make_system()

    print()

    print(system)  # TODO dev, remove
