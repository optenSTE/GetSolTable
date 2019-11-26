import hyperion
import numpy as np

# instrumant ip
# ip = '217.74.248.42'
ip = '10.0.0.50'
# Index of Refraction
n = 1.4682

h1 = hyperion.Hyperion(ip)

wl_start = 1566
wl_finish = 1626

wls = list()
distances = list()
shifts = list()
for wl in range(wl_start, wl_finish, 2):
    wls.append(wl)

    for distance in [50000]:
        num_of_attempts = 10
        cur_shifts = list()
        for _ in range(num_of_attempts):
            time_of_flight = int(2 * distance / 299792458 * n * 1e+9)
            wl_shifted = h1.shift_wavelength_by_offset(wl, time_of_flight)
            shift = (wl_shifted - wl)
            cur_shifts.append(shift)

        shift = np.mean(cur_shifts)
        shift_std = np.std(cur_shifts)

        print(distance, wl, shift, shift_std, sep='\t')

        shifts.append(shift)
        if distance not in distances:
            distances.append(distance)

with open('sol_table2.txt', 'w') as f:
    f.write('\t'.join(['WL[nm] / Distence[m]'] + list(map(str, distances))) + '\n')
    for wl in wls:
        f.write(str(wl) + '\t')
        for distance in distances:
            f.write(str(shifts[0]) + '\t')
            shifts.pop(0)
        f.write('\n')
