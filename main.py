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
from amuse.units import units

from evolution import evolve_gravity
from initialize import (
    make_system_anki, make_ph4, make_fi, make_bridge,
    add_debris_disk
)
from plotting import animate
from utils import print_cyan, print_green  # , spinner


SAVE_DIR = Path('outputs/')


if __name__ == '__main__':
    SAVE_DIR.mkdir(exist_ok=True)

    print(f'Python {sys.version}')
    print(
        f'AMUSE {amuse.__version__}, Astropy {astropy.__version__}, '
        f'Matplotlib {matplotlib.__version__}, Numpy {np.__version__}\n'
    )

    print_cyan('Can the Equatorial Ridge on Iapetus Form from a Debris Disk?')
    print('  by Ankita Dasgupta, Audrey Whitmer, and Qiushi Chris Tian')

    # print(
    #     "Note:\tIt's normal that the progress spinner will appear dead\n"
    #     '\tfor a few minutes. It is still running.'
    # )
    # print()

    print_green('\n----- Initialization -----')

    # with spinner('Creating solar system'):
    system = make_system_anki(
        #Masses of the 3 main gravitational bodies
        sun_mass = 1 | units.MSun,
        saturn_mass = 5.683e26 | units.kg,
        iapetus_mass = 1.81e21 | units.kg,
        #Approximate orbital distances. For simplicity, we start with circular orbits
        sun_saturn_distance = 9.5 | units.au,
        saturn_iapetus_distance = 3.56e6 | units.km
    )
    add_debris_disk(system, N=5)
    print(system)
    sys.exit(0)

    # Create n-body and hydro 
    gravity, gravity_channels = make_ph4(system)
    hydro, hydro_channels = make_fi(system)
    channels = {**gravity_channels, **hydro_channels}

    # Create bridge
    gravhydro = make_bridge(gravity, hydro)

    print_green('\n----- Evolving -----')

    particlesets, times = evolve_gravity(gravity, channels, particles=system)

    print_green('\n----- Visualization -----')

    movie_save_path = SAVE_DIR / 'disk_1k_100h.mp4'
    animate(particlesets, times).save(movie_save_path)
    print(f'Movie saved to {movie_save_path}')
