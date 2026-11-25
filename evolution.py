"""
Functions AMUSE.

Authors: Qiushi Chris Tian
Updated: 2026-11-11
"""

import time

import numpy as np

from amuse.units import units


def evolve_to(time_days, particles):
    gravity = Huayno(converter, channel_type="sockets")
    try:
        gravity.particles.add_particles(particles)
        gravity.evolve_model(time_days | units.day)
        result = gravity.particles.copy()
    finally:
        gravity.stop()

    return result


def evolve_gravity(
    gravity,
    channels,
    particles,  # TODO get rid of? Figure out how to return particles from gravity
    duration=100 | units.hour,
    collision_detection=True
):
    # Record the wall-clock starting time to measure how long the calculation takes on the computer
    start = time.perf_counter()

    if collision_detection:
        collision_detection = gravity.stopping_conditions.collision_detection
        collision_detection.enable()
    else:
        raise NotADirectoryError("Collision detection must be enabled for now.")

    #EVOLVE GRAVITY
    #We ask Ph4 to evolve for one hour. However, because collision detection is enabled,Ph4 can stop BEFORE one hour if particles collide.
    # fig, ax = plt.subplots(figsize=(5, 5))
    particlesets = []
    times = []
    # artists = []
    simulation_time = 0 | units.hour
    dt = 1.0 | units.hour
    while simulation_time < duration:
        simulation_time += dt
        gravity.evolve_model(simulation_time)
        channels['from_gravity'].copy()

        if collision_detection.is_set():
            # print(f'Time is {simulation_time}')

            #Obtain the two groups of particles involvedin the detected collision pairs.
            first = collision_detection.particles(0)
            second = collision_detection.particles(1)

            #AMUSE gives every particle a unique key. We use these keys to verify that the collision involved Iapetus and artificial test particle.
            moon_key = a[2].key
            test_key = impact_test[0].key

            # Check both possible orders because Iapetus could appear in either collision group.
            expected = any((p.key == moon_key and q.key == test_key) or (p.key == test_key and q.key == moon_key) for p, q in zip(first, second))

            # #model_time gives the actual simulation time when Ph4 stopped, not the requested end time.
            # print('Collision detected at:', gravity.model_time.in_(units.minute))
            # print('Iapetus + artificial test tracer:', expected)

            # if not expected:
            #     print('WARNING: collision involved a different particle pair')

        # else:
        #     print(f'WARNING: collision detector did not trigger in {EVOLVE_DURATION}')

        # Plotting
        particlesets.append(particles.copy())
        times.append(simulation_time)

        # art_list = animate_particles(particles)
        # artists += art_list

        # artists.append([ax_scatter(particles.x, particles.y, ax)])

    #shut down the Ph4 worker
    gravity.stop()
    print(
        f'Evolved gravity only in wall time: '
        f'{time.perf_counter() - start:.2f} s'
    )

    return particlesets, times
