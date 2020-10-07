
from numpy import isnan


def mass_energy_criteria(old_grid, new_grid):
    old_mass_t = 0
    old_mass_hw = 0
    for f in old_grid.Faces:
        s = f.area()
        assert ~isnan(f.T), 'NaN value of T'
        assert ~isnan(f.Hw), 'NaN value of Hw'
        old_mass_t += f.T * s
        old_mass_hw += f.Hw * s

    new_mass_t = 0
    new_mass_hw = 0
    for f in new_grid.Faces:
        s = f.area()
        assert ~isnan(f.T), 'NaN value of T'
        assert ~isnan(f.Hw), 'NaN value of Hw'
        new_mass_t += f.T * s
        new_mass_hw += f.Hw * s

    print('t: {}\nhw: {}'.format(new_mass_t - old_mass_t, new_mass_hw - old_mass_hw))
