#CMD pip 
import matplotlib.pyplot as plt
import numpy as np

T_Kelvin_extended = np.arange(300, 6001, 50)  # Temperature range up to 6000 K

coefficients = {
    'Ti': [11.925, -24991, -1.3376, 0],
    'V': [9.744, -27132, -0.5501, 0],
    'Ta': [16.807, -41346, -3.2152, 0],
    'Cr': [6.8, -20733, 0.4391, 0],
    'W': [2.945, -44094, 1.3677, 0],
    'Re': [11.543, -40726, -1.1629, 0],
}

melting_boiling_points = {
    'Ti': {'melting': 1941, 'boiling': 3560},
    'V': {'melting': 2183, 'boiling': 3680},
    'Ta': {'melting': 3290, 'boiling': 5731},
    'Cr': {'melting': 2180, 'boiling': 2944},
    'W': {'melting': 3695, 'boiling': 5828},
    'Re': {'melting': 3459, 'boiling': 5869},
}

ambient_pressures = [10, 100, 1000]  # 10 Pa, 100 Pa, 1000 Pa

plt.figure(figsize=(12, 8))

for element, coeff in coefficients.items():
    A, B, C, D = coeff

    logP_atm = A + B / T_Kelvin_extended + C * np.log10(np.maximum(T_Kelvin_extended, 1)) + D * T_Kelvin_extended**3
    logP_atm[np.isinf(logP_atm) | np.isnan(logP_atm)] = -20  

    P_Pa = 10**logP_atm * 101325
    P_Pa[P_Pa < 1e-20] = 1e-20  # Cap negligible values

    plt.semilogy(T_Kelvin_extended, P_Pa, label=element, linewidth=2)
    
    melt_temp = melting_boiling_points[element]['melting']
    boil_temp = melting_boiling_points[element]['boiling']
    melt_pressure = 10**(A + B / melt_temp + C * np.log10(max(melt_temp, 1)) + D * melt_temp**3) * 101325
    boil_pressure = 10**(A + B / boil_temp + C * np.log10(max(boil_temp, 1)) + D * boil_temp**3) * 101325
    plt.scatter([melt_temp], [melt_pressure], color='blue', s=100, zorder=5, marker='o')
    plt.scatter([boil_temp], [boil_pressure], color='orange', s=100, zorder=5, marker='o')

for ambient_pressure in ambient_pressures:
    plt.axhline(ambient_pressure, linestyle='--', linewidth=1.5, 
                label=f'Ambient Pressure: {ambient_pressure} Pa', alpha=0.8)

plt.xlabel('Temperature (K)', fontsize=12)
plt.ylabel('Vapor Pressure (Pa)', fontsize=12)
plt.title('Vapor Pressure vs Temperature with Solutions to Reduce Evaporation', fontsize=14)
plt.ylim(1e-20, 1e10)
plt.legend(loc='best', fontsize=10, frameon=False)
plt.grid(which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()
