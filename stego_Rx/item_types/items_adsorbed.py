#### Add clases for Adsorbed Surfaces
# V1.0, d8.03.23

import stego.thermo_base
import stego.promps
from stego.item_types import SingleItem


class AdsItem(SingleItem):
    def __init__(self, **kwargs):
        stego.item_types.SingleItem.__init__(self, **{**kwargs, 'type': 'Adsorbed'})

    #######################################################
    #### ---- Partition functions

    def q_tras(self, Report=False, **_unused) -> 'float, Adim':
        # Surface as a whole does not move
        stego.promps.report(Report, 'q_tras', 1., self)
        return 1

    def q_rot(self, T, Report=False, **_unused) -> 'float, Adim':
        # Surface as a whole does not rotate
        stego.promps.report(Report, 'q_tras', 1., self)
        return 1

    def q_vib(self, T, Report=False, **_unused) -> 'float, Adim':
        try:
            out = stego.thermo_base.qVib(self.FreqR, T)
            stego.promps.report(Report, 'q_vib', out, self)
            return out
        except TypeError:
            NameError('Need a list of frea freqs[cm-1] and T[K] to compute qTras')

    def q_el(self, Report=False, **_unused):
        # Bottom of the weel reference, n contribution for higher energies
        stego.promps.report(Report, 'q_el', 1., self)
        return 1

    #######################################################
    #### ---- Thermo energy contributions

    def Etras(self, T=None, Report=False, **_unused):
        # Surface does not move
        stego.promps.report(Report, 'E. tras.', 0., self)
        return 0

    def Erot(self, T=None, Report=False, **_unused) -> 'float, eV':
        # Surface does not rotate
        stego.promps.report(Report, 'E. rot.', 0., self)
        return 0.

    def ZPVE(self, Report=False, **_unused):
        # Check input
        try:
            out = stego.thermo_base.ZPVE(self.FreqR)  # /[eV]
            stego.promps.report(Report, 'ZPVE', out, self)  # report?
            return out
        except TypeError:
            raise NameError('Can\'t compute ZPVE without freqs.')

    def Evib(self, T=None, Report=False, **_unused):
        # Check input
        try:
            out = stego.thermo_base.Evib(self.FreqR, T)
            stego.promps.report(Report, 'E. vib', out, self)  # report?
            return out
        except TypeError:
            raise NameError('Needs real frequencies and T to compute E vib.')

    def Eel(self, Report=False, **_unused):
        # Bottom of well reference
        # Negligible population of higher levels is assumed
        stego.promps.report(Report, 'E. el.', 0., self)  # report?
        return 0.

    #######################################################
    #### ---- Thermo entropy contributions
    def Stras(self, T=None, P=None, Report=False):
        # Surface does not move
        stego.promps.report(Report, 'S. tras.', 0., self)
        return 0

    def Srot(self, T, Report=False, **_unused):
        # Surface does not rotate
        stego.promps.report(Report, 'S. tras.', 0., self)
        return 0.

    def Svib(self, T, Report=False, **_unused):
        try:
            out = stego.thermo_base.Svib(self.FreqR, T)  # /[eV/K]
            stego.promps.report(Report, 'S. vib.', out, self)  # report?
            return out
        except TypeError:
            raise NameError('Need real frequencies list [cm-1] and T [K] to compute Svib')

    def Sel(self, Report=False, **_unused):
        # Bottom of well reference
        # Negligible population of higher levels is assumed
        stego.promps.report(Report, 'S. el.', 0., self)  # report?
        return 0

    #### ---- Thermodynamic functions
    def Internal(self, T=None, Report=False, **_unused):
        # Etras = Erot = ZPVE = Evib = Eel = 0
        # Internal = E0 + ZPVE + Evib
        out = self.E0 \
              + self.ZPVE() \
              + self.Evib(T=T)
        stego.promps.report(Report, 'Internal E.', out, self)  # report?
        return out

    def Enthalpy(self, T=None, Report=False):
        # No pressure effect: do not include kbT (as in U+PV)
        out = self.Internal(T=T)  # [eV]
        stego.promps.report(Report, 'Enthalpy', out, self)  # report?
        return out

    def Entropy(self, T=None, P=None, Report=False):
        # Stras = Srot = Sel = 0
        out = self.Svib(T)  # eV/K
        stego.promps.report(Report, 'Entropy', out, self)  # report?
        return out
