from stegoplot.parameters import kb, hh, cc


# ---- molecular thermodynamics
# frequecy conversions
def freq__cm1_to_s1(in_fq: "float or list[floats], freqs cm-1") -> "float or list[floats] freqs s-1":
    # transforms vibrational frequencies from cm-1 to s-1
    if isinstance(in_fq, float) or isinstance(in_fq, int):
        return 100 * in_fq * cc
    elif isinstance(in_fq, list):
        return [100 * cc * i for i in in_fq]
    else:
        raise TypeError


def freq__s1_to_cm1(in_fq: "float or list[floats], freqs s-1") -> "float or list[floats] freqs cm-1":
    # transforms vibrational frequencies from s-1 to cm-1
    if isinstance(in_fq, float) or isinstance(in_fq, int):
        return in_fq / (100 * cc)
    elif isinstance(in_fq, list):
        return [i / (100 * cc) for i in in_fq]
    else:
        raise TypeError

# vibratonal temperatures
def freq_to_vib_temp(in_fq: "float or list[floats], freqs cm-1") -> "float or list[floats] vib. temp [K]":
    # transforms cm-1 -> vib. Temperature K
    if isinstance(in_fq, float) or isinstance(in_fq, int):
        return hh * freq__cm1_to_s1(in_fq) / kb
    elif isinstance(in_fq, list):
        return [hh * freq__cm1_to_s1(i) / kb for i in in_fq]
    else:
        raise TypeError


def vib_temp_to_freq(in_vt: "float or list[floats], vib temp [K]") -> "float or list[floats] freqs [cm-1]":
    # transforms rot. Temperature [K] -> freqs. [cm-1]
    if isinstance(in_vt, float) or isinstance(in_vt, int):
        return freq__s1_to_cm1(in_vt * kb / hh)
    elif isinstance(in_vt, list):
        return [freq__s1_to_cm1(i * kb / hh) for i in in_vt]
    else:
        raise TypeError
