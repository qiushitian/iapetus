"""
The single file you need to run to make all outputs.

Authors: Qiushi Chris Tian, Audrey Whitmer
Updated: 2026-11-27
"""

from pathlib import Path
import sys
import time

import astropy
import numpy as np
import matplotlib

import amuse
from amuse.units import units

from evolution import evolve_gravity
from initialize import (
    make_bridge,
    make_debris_disk,
    add_particles_centered_on,
    make_ph4,
    make_system_anki
)
from plotting import animate_3d, get_artists_3d
from utils import get_particle, print_cyan, print_green, spinner


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
    debris_disk = make_debris_disk(10000, np.pi / 4)
    add_particles_centered_on(system, 'iapetus', debris_disk)

    # Create n-body
    gravity, gravity_channels = make_ph4(system, n_workers=32)
    channels = {**gravity_channels}

    # Create bridge
    # gravhydro = make_bridge(gravity, hydro)

    print_green('\n----- Evolving -----')
    start_time = time.perf_counter()
    with spinner():
        particle_set_list = evolve_gravity(
            gravity, gravity_channels,
            particles=system, detect_collision=False,
            duration=10 | units.yr,
            n_frames=100
        )
    print(
        f'Evolved ph4 in wall time: '
        f'{(time.perf_counter() - start_time) / 60:.1f} min'
    )

    print_green('\n----- Visualization -----')
    movie_save_path = SAVE_DIR / '10k_10yr_45deg.mp4'
    animate_3d(
        particle_set_list,
        get_particle(system, 'iapetus').radius.value_in(units.km)
    ).save(movie_save_path)
    print(movie_save_path)
