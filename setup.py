"""
Initialize the AMUSE simulation.

Authors: Qiushi Chris Tian
Updated: 2026-11-11
"""


def make_system():
    obj = new_solar_system()
    new_system = obj[
        (obj.name == "SUN") |
        (obj.name == "JUPITER") |
        (obj.name == "SATURN")
    ].copy()
    saturn = new_system[new_system.name == "SATURN"][0]

    #iapetus properties from solar_system_moons.py
    iapetus = Particle()
    iapetus.name = "IAPETUS"
    iapetus.mass = 1.81e21 | units.kg
    iapetus.radius = 746 | units.km

    #orbital parameters
    a = 3560854 | units.km
    e = 0.0293
    M = np.deg2rad(201.789)  #mean anomaly