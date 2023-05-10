#### Add clase for clean surfaces
# V1.0, d8.03.23

import stego.promps
from stego.item_types import SingleItem


class CleanSurf(SingleItem):
    def __init__(self, **kwargs):
        # Get parent's properties and functions
        SingleItem.__init__(self, **{**kwargs, 'type': 'Clean Surface'})
        # Overwrite some things
        self.F_ID = None
        self.FreqR = None
        self.FreqI = None
        self.Species = None

    #### ---- Overwrite Partition functions
    def q_tras(self, Report=False, **_unused):
        # Surface as a whole does not rotate
        stego.promps.report(Report, 'q_tras', 1., self)
        return 1

    def q_vib(self, Report=False, **_unused):
        # Phonons are not considered
        stego.promps.report(Report, 'q_vib', 1., self)
        return 1

    def q_rot(self, Report=False, **_unused):
        stego.promps.report(Report, 'q_rot', 1., self)
        return 1.

    def q_el(self, Report=False, **_unused):
        stego.promps.report(Report, 'q_el', 1., self)
        return 1.

    #### ---- Thermo Energy functions
    def ZPVE(self, Report=False, **_unused):
        # Phonons are sistematically ignored
        out = 0.
        stego.promps.report(Report, 'ZPVE', 0., self)
        return out

    def Etras(self, Report=False, **_unused):
        # Surface does not move
        stego.promps.report(Report, 'E. tras.', 0., self)
        return 0

    def Erot(self, Report=False, **_unused):
        # Surface does not rotate
        stego.promps.report(Report, 'E. rot.', 0., self)
        return 0.

    def Evib(self, Report=False, **_unused):
        # Phonons are sistematically ignored
        stego.promps.report(Report, 'E. vib.', 0., self)
        return 0.

    def Eel(self, Report=False, **_unused):
        # Bottom of well reference
        # Negligible population of higher levels is assumed
        stego.promps.report(Report, 'E. el.(corr)', 0., self)
        return 0.

    #### ---- Overwrite Thermo Entropy functions
    def Stras(self, Report=False, **_unused):
        # Surface does not move
        stego.promps.report(Report, 'S. tras.', 0., self)
        return 0

    def Srot(self, Report=False, **_unused):
        # Surface does not rotate
        stego.promps.report(Report, 'S. tras.', 0., self)
        return 0.

    def Svib(self, Report=False, **_unused):
        # Phonons are sistematically ignored
        stego.promps.report(Report, 'S. vib.', 0., self)
        return 0.

    def Sel(self, Report=False, **_unused):
        # Bottom of well reference
        # Negligible population of higher levels is assumed
        stego.promps.report(Report, 'S. el.', 0., self)
        return 0.

    #### ---- Thermodynamic functions
    def Internal(self, Report=False, **_unused):
        # Etras = Erot = ZPVE = Evib = Eel = 0
        stego.promps.report(Report, 'S. tras.', self.E0, self)
        return self.E0

    def Enthalpy(self, Report=False, **_unused):
        # No pressure effect: do not include kbT (as in U+PV)
        out = self.Internal(Report=False, **_unused)
        stego.promps.report(Report, 'Enthalpy', out, self)
        return out

    def Entropy(self, Report=False, **_unused):
        # Only one state: Stras = Srot = Svib = Sel = 0
        stego.promps.report(Report, 'Entrophy', 0., self)
        return 0.
