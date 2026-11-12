"""
Helper functions.

Authors: Qiushi Chris Tian
Updated: 2026-11-11
"""

import contextlib
import io
import itertools
import sys
import threading
import time
from typing import Callable

from amuse.units.quantities import ScalarQuantity
from amuse.units import units, constants, nbody_system
from amuse.datamodel import Particle, Particles
from amuse.ext.solarsystem import new_solar_system
from amuse.ext.orbital_elements import rel_posvel_arrays_from_orbital_elements
from amuse.community.huayno.interface import Huayno


# See `amuse.ext.solarsystem.get_sun_and_planets`
AMUSE_ZERO_JD: ScalarQuantity = 2457099.500000000 | units.day


@contextlib.contextmanager
def spinner(message: str = 'Processing'):
    stop = threading.Event()
    stdout = sys.stdout  # Capture original stdout

    def animate():
        for char in itertools.cycle(
            "|/-\\"
            # ['.', '..', '...', '....', '.....']
        ):
            if stop.is_set():
                break
            stdout.write(f"\r{message}... {char}")
            stdout.flush()
            time.sleep(0.1)

        stdout.write(f"\r{message}... done!\n")
        stdout.flush()

    thread = threading.Thread(target=animate)
    thread.start()

    try:
        yield
    finally:
        stop.set()
        thread.join()


def get_abs_jd(delta_jd: ScalarQuantity):
    return AMUSE_ZERO_JD + delta_jd


def get_delta_jd(abs_jd: ScalarQuantity):
    return abs_jd - AMUSE_ZERO_JD


def get_time_jd(delta_jd: ScalarQuantity):
    """Alias for utils.get_abs_jd()."""
    return get_abs_jd(delta_jd)


def print_cyan(message, *args, **kwargs):
    print(f'\033[96m{message}\033[00m', *args, **kwargs)


def print_green(message, *args, **kwargs):
    print(f'\033[92m{message}\033[00m', *args, **kwargs)


# def run_with_spinner(message: str, func: Callable, *args, **kwargs):
#     stop, thread = _spinner(message)
#     try:
#         return func(*args, **kwargs)
#     finally:
#         stop.set()
#         thread.join()


# def silence(func: Callable, *args, **kwargs):
#     with contextlib.redirect_stdout(io.StringIO()):
#         return func(*args, **kwargs)


def orbital_radii(particles):
    moon = particles[0]
    debris = particles[1:]

    r = (
        (debris.x - moon.x)**2 +
        (debris.y - moon.y)**2 +
        (debris.z - moon.z)**2
    ).sqrt()

    return r.value_in(units.km)


def compare_radii(initial, final):
    r0 = orbital_radii(initial)
    r1 = orbital_radii(final)
    dr = r1 - r0

    print(f"Initial mean radius: {r0.mean():.3f} km")
    print(f"Final mean radius:   {r1.mean():.3f} km")
    print(f"Change in mean:      {dr.mean():.3f} km")
    print(f"Mean absolute change:{np.abs(dr).mean():.3f} km")
    print(f"Maximum change:      {np.abs(dr).max():.3f} km")
