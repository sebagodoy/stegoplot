#### Add clases for gaseous species
# V1.0, d8.03.23

import stego.thermo_base
import stego.promps
import numpy
from stego.item_types import SingleItem
from stego.parameters import kb, eV2J


class GasItem(SingleItem):
    def __init__(self, **kwargs):
        stego.item_types.SingleItem.__init__(self, **{**kwargs, 'type': 'Gas'})

    #######################################################
    #### ---- Partition functions

    def q_tras(self, T, P, Report=False, **_unused) -> 'float, Adim':
        try:
            out = stego.thermo_base.qTras(self.mass, T, P)
            stego.promps.report(Report, 'q_tras', out, self)  # report?
            return out
        except TypeError:
            stego.promps.errorreport('Something is missing to compute q_tras for ' + self.Name)

    def q_rot(self, T, Report=False, **_unused) -> 'float, Adim':
        try:
            out = stego.thermo_base.qRot(self.Geometry, self.RotTemp, T, self.RotSym)
            stego.promps.report(Report, 'q_rot', out, self)  # report?
            return out
        except TypeError:
            NameError('Something went wrong computing q_rot for ' + self.Name +
                      '\nbe sure it has a Geometry, Rotational Symmetry number and Rotational Temperature')

    def q_vib(self, T, Report=False, **_unused) -> 'float, Adim':
        # Check input
        try:
            out = stego.thermo_base.qVib(self.FreqR, T)
            stego.promps.report(Report, 'q_vib', out, self)  # report?
            return out
        except TypeError:
            NameError('Need a list of frea freqs[cm-1] and T[K] to compute qTras')

    def q_el(self, Report=False, **_unused):
        out = stego.thermo_base.qEl()
        stego.promps.report(Report, 'q_el', out, self)  # report?
        return out

    #######################################################
    #### ---- Thermo energy contributions

    def Etras(self, T=None, Report=False, **_unused) -> 'float, eV':
        try:
            out = stego.thermo_base.Etras(T)  # /[eV]
            stego.promps.report(Report, 'E. tras.', out, self)  # report?
            return out
        except TypeError:
            raise NameError('Needs T to compute E traslational')

    def Erot(self, T=None, Report=False, **_unused) -> 'float, eV':
        try:
            out = stego.thermo_base.Erot(self.Geometry, T=T)
            stego.promps.report(Report, 'E. rot.', out, self)  # report?
            return out
        except TypeError:
            raise NameError('Something is missing to compute E. rot. for ' + self.Name)

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
            raise NameError('Needs real frequencies to compute E vib.')

    def Eel(self, Report=False, **_unused):
        # Bottom of well reference
        # Negligible population of higher levels is assumed
        stego.promps.report(Report, 'E. el.', 0., self)  # report?
        return 0.

    #######################################################
    #### ---- Thermo entropy contributions
    def Stras(self, T=None, P=None, Report=False):

        try:
            out = kb * (numpy.log(self.q_tras(T=T, P=P)) + 5. / 2.) / eV2J  # /[eV/K]
            stego.promps.report(Report, 'S. tras.', out, self)  # report?
            return out
        except TypeError:
            raise NameError('Something is missing to compute S. tras. for ' + self.Name)

    def Srot(self, T, Report=False, **_unused):
        # Check input
        try:
            out = stego.thermo_base.Srot(self.Geometry, self.RotTemp, T, self.RotSym)
            stego.promps.report(Report, 'S. rot.', out, self)  # report?
            return out
        except TypeError:
            raise NameError('Something is missing to compute S. rot. for ' + self.Name)

    def Svib(self, T, Report=False, **_unused):
        # Check input
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
        # Eel = 0
        # Internal = E0 + Etras + Erot  + ZPVE + Evib
        out = self.E0 \
              + self.Etras(T=T) \
              + self.Erot(T=T) \
              + self.ZPVE() \
              + self.Evib(T=T)
        stego.promps.report(Report, 'Internal E.', out, self)  # report?
        return out

    def Enthalpy(self, T=None, Report=False, **_unused):
        # Includes pressure effect: H = U + kbT
        out = self.Internal(T=T) + kb * T / eV2J  # [eV]
        stego.promps.report(Report, 'Enthalpy', out, self)  # report?
        return out

    def Entropy(self, T=None, P=None, Report=False):
        # Svib = 0
        out = self.Stras(T, P) \
              + self.Srot(T) \
              + self.Svib(T)  # eV/K
        stego.promps.report(Report, 'Entropy', out, self)  # report?
        return out
