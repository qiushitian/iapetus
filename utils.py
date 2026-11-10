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