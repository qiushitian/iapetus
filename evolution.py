"""
Functions AMUSE.

Authors: Qiushi Chris Tian
Updated: 2026-11-27
"""

from amuse.units import units
from amuse.units.quantities import ScalarQuantity


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
    duration: ScalarQuantity = 100 | units.hour,
    n_frames: int = 100,
    detect_collision: bool = False
):
    """
    Evolve gravity only.
    
    Args:
        gravity: gravity object
        channels: channels object
        particles: particles object
        duration: duration of evolution
        n_frames: number of frames
        detect_collision: whether to detect collision
    
    Returns:
        particle_set_list: list of particle sets at each frame
    """
    if detect_collision:
        collision_detection = gravity.stopping_conditions.collision_detection
        collision_detection.enable()

    particle_set_list = []
    simulation_time = 0 | units.hour
    dt = duration / n_frames
    while simulation_time < duration:
        simulation_time += dt
        gravity.evolve_model(simulation_time)
        channels['from_gravity'].copy()

        if detect_collision and collision_detection.is_set():
            # print(f'Time is {simulation_time}')

            #Obtain the two groups of particles involvedin the detected collision pairs.
            first = collision_detection.particles(0)
            second = collision_detection.particles(1)

            # #AMUSE gives every particle a unique key. We use these keys to verify that the collision involved Iapetus and artificial test particle.
            # moon_key = a[2].key
            # test_key = impact_test[0].key

            # # Check both possible orders because Iapetus could appear in either collision group.
            # expected = any((p.key == moon_key and q.key == test_key) or (p.key == test_key and q.key == moon_key) for p, q in zip(first, second))

            # #model_time gives the actual simulation time when Ph4 stopped, not the requested end time.
            # print('Collision detected at:', gravity.model_time.in_(units.minute))
            # print('Iapetus + artificial test tracer:', expected)

            # if not expected:
            #     print('WARNING: collision involved a different particle pair')

        # else:
        #     print(f'WARNING: collision detector did not trigger in {EVOLVE_DURATION}')

        # Plotting
        particle_set_list.append(particles.savepoint(simulation_time))

    gravity.stop()
    return particle_set_list
