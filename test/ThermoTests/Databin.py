# Testing thermodynamic functons for

import stegoplot.item_types as Model

# ----------------------------------------------------------------------------------------------------------------------
# Molecular information from RPBE-DFT and reference (McQuarrie & Simon)

CH4_g = Model.GasItem(Name='CH4', E0=-24.03491563, type='Gas',
                         G_ID='CH4.gas_Local_UltraHighRes_Box15', F_ID='freqs from McQuarrie & Simon',
                  FreqR=[3088.351691, 3086.406086, 3080.600334, 2967.887746, 1519.931601, 1516.585642,
                         1296.27073, 1295.587467, 1291.591103],
                  Geometry='Poliatomic', Mass=16.04,
                  RotT=[7.54, 7.54, 7.54], RotSymNum=12)

H2 = Model.GasItem(Name='H2-gas', E0=-6.98503949,
                   FreqR=[4354.140143],
                   Geometry='Diatomic homonuclear',
                   Mass=2.0,
                   RotT=85.3,
                   RotSymNum=2)

print('-'*20)

print(str(H2))
print(repr(H2))

print('-'*20)

H2.q_vib(T=300, Report=True)
H2.q_el(T=300, Report=True)
H2.q_tras(P=1, T=300, Report=True)
H2.q_rot(T=300, Report=True)

print('-'*20)

H2.Evib(T=300, Report=True)
H2.Erot(T=300, Report=True)
H2.Etras(T=300, Report=True)
H2.Eel(T=300, Report=True)

print('-'*20)

H2.Svib(T=300, Report=True)
H2.Srot(T=300, Report=True)
H2.Stras(T=300, P=1, Report=True)
H2.Sel(T=300, Report=True)

print('-'*20)

H2.Internal(T=300, P=123, Report=True) # P does not matter for internal energy
H2.E0ZPVE(Report=True)
H2.ZPVE(Report=True)
H2.Enthalpy(T=300, Report=True)
H2.Entropy(T=300, P=1., Report=True)
H2.Gibbs(T=300, P=1., Report='Detailed')

print('-'*20)

H2.GetThermo(ThermoType='E0', T=300, P=1, Report=True)
H2.GetThermo(ThermoType='Etras', T=300, P=1, Report=True)
H2.GetThermo(ThermoType='Erot', T=300, P=1, Report=True)
H2.GetThermo(ThermoType='Evib', T=300, P=1, Report=True)
H2.GetThermo(ThermoType='Eel', T=300, P=1, Report=True)
H2.GetThermo(ThermoType='Gibbs', T=300, P=1, Report=True)

H2.GetThermo(ThermoType='Internal', T=300, P=1, Report=True)
