"""
Functions AMUSE.

Authors: Qiushi Chris Tian
Updated: 2026-11-11
"""

import numpy as np

from amuse.units import units, constants, nbody_system
from amuse.datamodel import Particle, Particles
from amuse.ext.solarsystem import new_solar_system
from amuse.ext.orbital_elements import rel_posvel_arrays_from_orbital_elements
from amuse.community.huayno.interface import Huayno


def evolve_to(time_days, particles):
    gravity = Huayno(converter, channel_type="sockets")
    try:
        gravity.particles.add_particles(particles)
        gravity.evolve_model(time_days | units.day)
        result = gravity.particles.copy()
    finally:
        gravity.stop()

    return result