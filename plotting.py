"""
Simulating Iapetus with AMUSE.

Authors: Qiushi Chris Tian
Updated: 2026-11-11
"""

import numpy as np
import matplotlib.pyplot as plt

from amuse.units import units, constants, nbody_system
from amuse.datamodel import Particle, Particles
from amuse.ext.solarsystem import new_solar_system
from amuse.ext.orbital_elements import rel_posvel_arrays_from_orbital_elements
from amuse.community.huayno.interface import Huayno


def plot_disk(particles, time=None):
    moon = particles[0]
    debris = particles[1:]

    x = (debris.x - moon.x).value_in(units.km)
    y = (debris.y - moon.y).value_in(units.km)
    R = moon.radius.value_in(units.km)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(x, y, s=8, label="Debris")
    ax.add_patch(plt.Circle((0, 0), R, color="gray"))

    ax.set_aspect("equal")
    ax.set_xlabel("x rel to Iapetus(km)")
    ax.set_ylabel("y rel to Iapetus(km)")
    ax.set_title(f"Debris disk at t = {time} days" if time is not None
                 else "Debris disk")
    ax.legend()
    plt.show()
