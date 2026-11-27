"""
Simulating Iapetus with AMUSE.

Authors: Qiushi Chris Tian
Updated: 2026-11-27
"""

from matplotlib import patches
from matplotlib.animation import ArtistAnimation
import matplotlib.pyplot as plt
import numpy as np

from amuse.plot import scatter, UnitlessArgs
from amuse.units import units

from utils import get_index_from_name


def animate(particlesets, times, figsize=(5, 5), interval=50):
    fig, ax = plt.subplots(figsize=figsize)
    l = []
    for p, t in zip(particlesets, times):
        l.append(get_artists_2d(p, t))

    return ArtistAnimation(fig=fig, artists=l, interval=interval)


def animate_3d(particle_set_list, radius, figsize=(5, 5), interval=50):
    fig = plt.figure(figsize=(5, 5), layout='constrained')
    ax = fig.add_subplot(projection='3d')

    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 20)
    x = radius * np.outer(np.cos(u), np.sin(v))
    y = radius * np.outer(np.sin(u), np.sin(v))
    z = radius * np.outer(np.ones_like(u), np.cos(v))

    iapetus_artist = ax.plot_wireframe(
        x, y, z,
        colors='navy', alpha=0.2
    )

    l = []
    for p in particle_set_list:
        l.append(get_artists_3d(p, ax))

    ax.set_aspect('equal')
    # ax.view_init(elev=90, azim=-90)

    return ArtistAnimation(fig=fig, artists=l, interval=50)


def get_artists_2d(particles, t=None):
    iap_x, iap_y = particles[2].x, particles[2].y
    # scatter(particles[0].x, particles[0].y, label='Sun')
    # scatter(particles[1].x, particles[1].y, label='Saturn')
    sca_iape = patches.Circle(
        (0, 0),
        radius=particles[2].radius.value_in(units.km),
        facecolor='r', linewidth=0, alpha=0.5
    )
    plt.gca().add_patch(sca_iape)
    sca_debr = scatter(
        particles[3:-1].x - iap_x, particles[3:-1].y - iap_y,
        label='Debris', c='b', s=1, marker='.',
        alpha=min(1, 2000 / len(particles))  # TODO need another alpha logic
    )
    # sca_test = scatter(
    #     particles[-1].x - iap_x, particles[-1].y - iap_y,
    #     label='Test particle', c='g'
    # )
    ti_artist = plt.text(-20, 150, f'{t.value_in(units.hour):.2f} hr')
    # lgd = plt.legend(bbox_to_anchor=[1.5, 0.6])
    return [
        sca_iape, sca_debr,
        # sca_test,
        ti_artist,
        # lgd
    ]


def get_artists_3d(particle_set, ax):
    index_iapetus = get_index_from_name(particle_set, 'iapetus')
    iapetus = particle_set[index_iapetus]

    disk_xyz = UnitlessArgs.strip(
        particle_set[index_iapetus :].x - iapetus.x,
        particle_set[index_iapetus :].y - iapetus.y,
        particle_set[index_iapetus :].z - iapetus.z,
    )
    disk_artist = ax.scatter(
        *UnitlessArgs.stripped_args,
        label='Debris', c='olive', s=1, marker='.',
        # TODO need another alpha logic
        alpha=min(1, 2000 / len(particle_set[index_iapetus :]))
    )
    
    text_artist = ax.text(
        0, 0, 0,
        f'{particle_set.get_timestamp().value_in(units.hour):.0f} hr',
        # transform=ax.transAxes
    )

    ax.set_xlabel(f'x {UnitlessArgs.x_label()}')
    ax.set_ylabel(f'y {UnitlessArgs.y_label()}')
    ax.set_zlabel(f'z {UnitlessArgs.z_label()}')

    return [disk_artist, text_artist]

##############################################################################

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
