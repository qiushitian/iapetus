"""
Simulating Iapetus with AMUSE.

Authors: Qiushi Chris Tian
Updated: 2026-11-11
"""

from matplotlib import patches
from matplotlib.animation import ArtistAnimation
import matplotlib.pyplot as plt
import numpy as np

from amuse.plot import scatter
from amuse.units import units


def plot_system(particles, t=None):
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


def animate(particlesets, times, figsize=(5, 5), interval=50):
    fig, ax = plt.subplots(figsize=figsize)
    l = []
    for p, t in zip(particlesets, times):
        l.append(plot_system(p, t))

    return ArtistAnimation(fig=fig, artists=l, interval=interval)


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
