"""
Initialize the AMUSE simulation.

Authors: Qiushi Chris Tian
Updated: 2026-11-12
"""

import contextlib
import io

from amuse.ic.solar_system_moons import get_moons_for_planet
from amuse.units.quantities import ScalarQuantity
from amuse.units import units
from amuse.ext.solarsystem import solar_system_in_time

from utils import get_delta_jd, spinner


def make_system(jd: ScalarQuantity = 2457099.5 | units.day):
    """
    Creates a Sun–Saturn–Iapetus system with Jupiter.

    Parameters
    ----------
    jd : :class:`~amuse.units.quantities.ScalarQuantity`
        Julian date of the solar system.
        Must be in :class:`~amuse.units.units.day`.

    Returns
    -------
    system : :class:`~amuse.datamodel.particles.ParticlesSubset`
        A particle set object of the system containing the Sun, Jupiter, 
        Saturn, and Iapetus.
    """
    # Create solar system with Sun, Jupiter, and Saturn
    with spinner('Creating solar system'):
        system = solar_system_in_time(jd)

    # Keep only Sun, Jupiter, and Saturn
    system = system[
        [n in ('Sun', 'Jupiter', 'Saturn') for n in system.name]
    ]

    # Set types
    system[0].type = 'star'
    system[1:].type = 'planet'

    # Get all moons for Saturn
    with spinner('Adding Iapetus'):
        with contextlib.redirect_stdout(io.StringIO()):
            saturn_moons = get_moons_for_planet(
                system[system.name == 'Saturn'][0],
                delta_JD=get_delta_jd(jd)
            )
    
    system.add_particle(
        saturn_moons[saturn_moons.name == b'Iapetus'][0]
    )
    system.move_to_center()

    return system
