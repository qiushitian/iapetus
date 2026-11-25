"""
Initialize the AMUSE simulation.

Authors: Qiushi Chris Tian
Updated: 2026-11-25
"""

import contextlib
import io

import numpy as np

from amuse.community.ph4 import Ph4
from amuse.community.fi import Fi
from amuse.couple import bridge
from amuse.datamodel import Particles
from amuse.ic.solar_system_moons import get_moons_for_planet
from amuse.units.quantities import ScalarQuantity
from amuse.units import units, constants, nbody_system
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
        # with contextlib.redirect_stdout(io.StringIO()):
        saturn_moons = get_moons_for_planet(
            system[system.name == 'Saturn'][0],
            delta_JD=get_delta_jd(jd)
        )

    system.add_particle(
        saturn_moons[saturn_moons.name == b'Iapetus'][0]
    )
    system.move_to_center()

    return system


def make_system_anki(
    sun_mass,
    saturn_mass,
    iapetus_mass,
    sun_saturn_distance,
    saturn_iapetus_distance
):
    #CREATE SUN, SATURN AND IAPETUS
    a = Particles(3)
    a.name = ('sun'.casefold(), 'saturn'.casefold(), 'iapetus'.casefold())
    a.mass = (
        sun_mass.in_(units.kg),
        saturn_mass.in_(units.kg),
        iapetus_mass.in_(units.kg)
    )

    #Only Iapetus needs a physical radius for our surface-collision test using R_Iapetus = 735 km (Stickle & Roberts, 2018).
    #Sun and Saturn are treated as point particles for collision detection

    a.radius = [0, 0, 735] | units.km

    #Initially set all positions and velocities to zero

    a.position = [[0, 0, 0]] * 3 | units.km
    a.velocity = [[0, 0, 0]] * 3 | (units.km / units.s)

    #SUN-SATURN ORBIT
    # placing the Sun and Saturn in circular orbits around their common center of mass. using their relative circular orbital speed is: v = sqrt(G * (M1 + M2) / r). also divided that relative motion between the two bodies according to their masses.

    outer_speed = (constants.G * (sun_mass + saturn_mass) / sun_saturn_distance).sqrt()

    # positions along the x-axis, measured relative to the Sun-Saturn center of mass

    a[0].x = -sun_saturn_distance * saturn_mass / (sun_mass + saturn_mass)
    a[1].x = sun_saturn_distance * sun_mass / (sun_mass + saturn_mass)

    # vel are perpendicular to the separation, along the y-axis, producing an initially circular orbit. The two bodies move in opposite directions.

    a[0].vy = -outer_speed * saturn_mass / (sun_mass + saturn_mass)

    a[1].vy = outer_speed * sun_mass / (sun_mass + saturn_mass)

    #IAPETUS AROUND SATURN
    # we place Iapetus relative to Saturn. The position and velocity must include Saturn's own position and velocity around the Sun.
    # assume a circular, coplanar orbit and not yet using Iapetus's observed eccentricity and inclination from Chris's longer simulation.

    moon = a[2]
    moon.position = a[1].position + ([saturn_iapetus_distance.value_in(units.km), 0, 0]| units.km)

    #circular speed of Iapetus rel to Saturn = v = sqrt(G * (M_Saturn + M_Iapetus) / r)
    moon_speed = (constants.G * (saturn_mass + iapetus_mass) / saturn_iapetus_distance).sqrt()

    #Iapetus's velocity is Saturn's orbital velocity + its velocity around Saturn
    #This gives all bodies velocities in the same frame.

    moon.velocity = a[1].velocity + ([0, moon_speed.value_in(units.km / units.s), 0] | (units.km / units.s))

    return a


def add_debris_disk(particle_set: Particles, N: int, inclination: float = 0.0, seed: int = 42):
    iapetus = particle_set[particle_set.name == 'iapetus'][0]

    #DEBRIS RING
    #100 particles in circular orbits around Iapetus. The initial ring lies between 1000 and 1800 km from Iapetus's center
    #This range is approximately within the Roche-limit region discussed by Levison et al. (2011) and Dombard et al. (2012)
    debris_disk_particle_set = Particles(N)
    debris_disk_particle_set.name = [
        f'debris_{i}'.casefold() for i in range(N)
    ]

    rng = np.random.default_rng(seed)
    r = rng.uniform(1000, 1800, N) | units.km

    # Random orbital angle between 0 and 2*pi. This distributes the particles around the ring.
    theta = rng.uniform(0, 2 * np.pi, N)

    #Circular orbital velocity at each radius.
    v = (constants.G * iapetus.mass / r).sqrt()

    #Give particles very small gravitational masses. This is our numerical tracer approximation: the particles primarily respond to Iapetus's gravity instead of strongly perturbing each other.
    #These are NOT the physical masses of the debris. We will eventually assign separate represented masses for the ridge-deposition calculation.

    debris_disk_particle_set.mass = (1.81e21 * 1e-12 / N) | units.kg

    #Their physical sizes and mutual collisions are not yet included.
    debris_disk_particle_set.radius = 0 | units.km

    #Place particles around Iapetus in the XY plane. All particles initially have the same z as Iapetus. We assume this plane is Iapetus's equatorial plane.

    debris_disk_particle_set.x = iapetus.x + r * np.cos(theta)
    debris_disk_particle_set.y = iapetus.y + r * np.sin(theta)
    debris_disk_particle_set.z = iapetus.z

    # Velocity must be tangential to the circular orbit. Adding Iapetus's velocity puts the debris in the same reference frame as the other bodies.

    debris_disk_particle_set.vx = iapetus.vx - v * np.sin(theta)
    debris_disk_particle_set.vy = iapetus.vy + v * np.cos(theta)
    debris_disk_particle_set.vz = iapetus.vz

    # for now, initialize an inclination angle around the x-axis.
    debris_disk_particle_set.rotate(inclination, 0.0, 0.0)

    # COMBINE ALL PARTICLES
    particle_set.add_particles(debris_disk_particle_set)


def make_ph4(particles, conv_1=5.683e26 | units.kg, conv_2=3.56e6 | units.km):
    # INITIALIZE PH4
    # Convert physical SI units into the dimensionless N-body units used internally by the integrator

    converter = nbody_system.nbody_to_si(conv_1, conv_2)

    # start the Ph4 gravitational solver
    gravity = Ph4(converter)

    # Accuracy/timestep control for Ph4. timestep of 0.01 is a dimensionless integrator parameter

    # gravity.parameters.timestep_parameter = 0.01

    # copied the particles into the gravitational solver
    gravity.particles.add_particles(particles)

    channels = {}
    channels['to_gravity'] = particles.new_channel_to(gravity.particles)
    channels['from_gravity'] = gravity.particles.new_channel_to(particles)

    return gravity, channels


def make_huayno():
    pass


def make_fi(particles, n_gas=500, conv_1=5.683e26 | units.kg, conv_2=3.56e6 | units.km):
    converter = nbody_system.nbody_to_si(conv_1, conv_2)
    gas = new_plummer_gas_model(n_gas, converter)
    hydro = Fi(converter)
    hydro.particles.add_particles(gas)
    channels = {}
    channels['to_hydro'] = gas.new_channel_to(hydro.particles)
    channels['from_hydro'] = hydro.particles.new_channel_to(gas)
    return hydro, channels


def make_bridge(code_1, code_2):
    """
    Make a bridge between two codes.

    Args:
        code_1: The first code
        code_2: The second code

    Returns:
        The bridge
    """
    my_bridge = bridge.Bridge()
    my_bridge.add_system(code_1, (code_2))
    my_bridge.add_system(code_2, (code_1))
    return my_bridge
