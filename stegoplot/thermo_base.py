# Packages

from stegoplot.parameters import Nav, kb, hh, cc, eV2J
from numpy import pi, exp, prod, log


########################################################################################################################
# Partition functions

def qTras(inM: 'float, Mass, [AMU=g/mol]',
          inT: 'float, Temperature, [K]',
          inP: 'float, Pressure, [bar]') -> 'float, part.fun. adim.':
    inP = inP * 100000  # bar -> Pa
    inM = inM / (Nav * 1000)  # g/mol -> kG/particle
    frac1 = 2 * pi * inM * kb * inT / (hh ** 2.)
    frac2 = kb * inT / inP
    return frac2 * (frac1 ** (3. / 2.))  # /[Adim]


def qRot(Geom: 'str, Geometry',
         RotT: 'Rot. temp., float or float-list in [K]',
         Tin: 'float, Temp., [K]',
         SymmNum: 'int, Rot. symmetry number') -> 'float, part.fun. adim.':
    # Rotational partition function [Adim.]
    # Geometry = 'Diatomic homonuclear', 'Diatomic Heteronuclear' or 'Poliatomic'
    # RotT	=	Rotational temperature or list if poliatomic /[K]
    # Tin =		Temperature /[K]
    # SymmNum = Rotational symmetry number (HCl:1, H2/O2/Cl2=2, NH3:3, CH4:12)

    # Check geometry
    if 'Diatomic' in Geom:
        # Diatomic, Symmnumber = 1 or 2, len(RotT) = 1
        return Tin / (SymmNum * RotT)
    elif 'Poliatomic' in Geom:
        if not len(RotT) == 3:
            raise NameError('Poliatomic molecule needs three rotational temperatures to compute qRot')
        return (pi * (Tin ** 3) / ((SymmNum ** 2) * prod(RotT))) ** 0.5  # /adim
    else:
        raise NameError('Geometry not recognized')


def qVib(FreqIn: 'list, Real frequencies, [cm-1]',
         Tin: 'float, Temperature, [K]') -> 'float, part.fun. adim.':
    qV = 1
    for iF in FreqIn:
        vibTemp = hh * cc * iF * 100. / kb  # /[Adim.]
        fracUp = exp(-vibTemp / (2. * Tin))
        fracDown = 1. - exp(-vibTemp / Tin)
        qV *= fracUp / fracDown
    return qV  # /[Adim.]


def qEl() -> 'float, part.fun. adim.':
    # Electronic partition function [Adim.]
    # Assumes excited states in such high energy that are inaccessible
    # and spin multiplicity of ground state = 1
    return 1.


########################################################################################################################
# Energetic contributions by partition
# default output in eV

def Etras(inT: 'float, temp [K]') -> 'float, energy [eV]':
    # Translational energy [eV]
    # inT = Temperature		/[K]
    return (3. / 2.) * (kb * inT / eV2J)  # /(eV)


def ZPVE(FreqIn: 'list, real freqs, [cm-1]') -> 'float, energy [eV]':
    # Zero Point Vibrational Energy, ZPVE [eV]
    # FreqIn = [real freqs list]	/[cm-1]
    sZPVE = 0.
    for iF in FreqIn:
        sZPVE += (hh * cc * iF * 100) / (2 * eV2J)
    return sZPVE  # /(eV)


def Evib(FreqIn: 'list, real freqs., [cm-1]',
         Tin: 'float, temp. [K]') -> 'float, energy [eV]':
    # Vibrational energy [eV]
    # FreqIn = [real freqs list]	/[cm-1]
    # Tin = Temperature				/[K]
    Ev = 0.
    for iF in FreqIn:
        vibTemp = hh * cc * iF * 100. / kb  # /[Adim.]
        Ev += vibTemp / (exp(vibTemp / Tin) - 1.)
    return Ev * (kb / eV2J)  # /[eV]


def Erot(Geometry: 'str, molecular geometry',
         T: 'float, temp. [K]') -> 'float, energy [eV]':
    # Rotational energy [eV]
    # Geometry =	'Diatomic homonuclear'
    #               'Diatomic Heteronuclear'
    #               'Polyatomic'
    # Tin = Temperature  /[K]
    if "Diatomic" in Geometry:
        return kb * T / eV2J  # /[eV]
    elif 'Poliatomic' in Geometry:
        return (3. / 2.) * kb * T / eV2J  # /[eV]
    else:
        raise NameError('Geometry option not recognized, must be \
        Diatomic homonuclear, Diatomic heteronuclear or Polyatomic')


########################################################################################################################
# Entropic contributions by partition
# default output in eV/K

def Stras(iinM: "float, molec. mass [g/mol]",
          iinT: "float, temp [K]",
          iinP: "float, pressure, [bar]") -> 'float, entropy, [eV/K]':
    # Translational entropy [eV/K]
    # inM = Masa			/[AMU = g/mol]
    # inT = Temperature		/[K]
    # inP = Pressure		/[bar]
    qT = qTras(iinM, iinT, iinP)
    return kb * (log(qT) + 5. / 2.) / eV2J  # /[eV/K]


def Srot(Geom: "str, molec geometru",
         RotT: "float 4 diatomic, [3xfloat] polyatomic, rot. temp [K]",
         Tin: "float, temp. [K]",
         SymmNum: "int, Rot. symmetry number") -> 'float, entropy, [eV/K]':
    # Rotational entropy [eV/K]
    # Geom	=	'Diatomic homonuclear', 'Diatomic Heteronuclear' or 'Poliatomic'
    # RotT	=	Rotational temperature / K, 1float for diatomics list[3] for everything else.
    # Tin	=	Temperature / K
    # SymmNum =	Rotational symmetry number (1 for HCl, 2 for H2, 3 for NH3, 12 for CH4)
    # print("Rot Sym number = " + str(SymmNum))
    qR = qRot(Geom, RotT, Tin, SymmNum)
    if 'Diatomic' in Geom:
        return kb * (log(qR) + 1.) / eV2J  # /[eV/K]
    elif Geom == 'Poliatomic':
        return kb * (log(qR) + 3. / 2.) / eV2J  # /[eV/K]


def Svib(FreqIn: "list[floats], real freqs. [cm-1]", Tin: "float, temp. [K]") -> 'float, entropy, [eV/K]':
    # Vibrational entropy [eV/K]
    # FreqIn = [Real fres list]	/[cm-1]
    # Tin = Temperature			/[K]
    Sv = 0
    for iFq in FreqIn:
        rotTonT = hh * cc * iFq * 100. / (kb * Tin)  # /[Adim.]
        # print('(Rot T)/T = ' + str(rotTonT))
        frac = rotTonT / (exp(rotTonT) - 1.)  # /[Adim.]
        lo = log(1. - exp(-rotTonT))  # /[Adim.]
        Sv += kb * (frac - lo) / eV2J  # /[eV/K]
    return Sv  # /[eV/K]


def Sel() -> 'float, entropy, [eV/K]':
    return 0.
