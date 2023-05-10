#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from Databin import *
import stego.Plot, stego.promps

GibbsOpts = {'T': 265 + 273.15, 'P': 0.01 * 1.}  # 1% CH4
GibbsOpts_H2 = {'T': 265 + 273.15, 'P': 0.25 * 1.}  # 25% H2

CO2.E0 += 0.3711642128942156

########################################################################################################################
# Creating Plot, CHx series ############################################################################################
########################################################################################################################

MayorSection('Creating Plot')

fig, axs = plt.subplots(2, 3, figsize=(12, 6), dpi=90, sharey='row')
plt.subplots_adjust(wspace=.0, hspace=.05, left=.08, right=.98, bottom=.05, top=.95)
HoverList = []

# References

RefN111_e = stego.Plot.RxRef(0., 0.)
RefC111_e = stego.Plot.RxRef(0., 0.)
RefCN111_e = stego.Plot.RxRef(0., 0.)

# Place holders
HoverList = []
SectionRefs_N111e = RefN111_e.branch()
SectionRefs_C111e = RefC111_e.branch()
SectionRefs_CN111e = RefCN111_e.branch()

# Color ref: https://gist.github.com/thriveth/8560036

# Default parameters
Main_Line_Props = {"StepSpan": .5, "LineStyle": "solid", "LineWidth": 1.5, "AlphaLines": 1., 'T-rate':265 + 273.15}
Main_Line_Props_Co = {"StepSpan": 1., "LineStyle": "solid", "LineWidth": 1.5, "AlphaLines": 1.}
Jump_Line_Props = {"StepSpan": .2, "LineStyle": "solid", "LineWidth": .8, "AlphaLines": 1.}
OH_Line_Props = {"StepSpan": .2, "LineStyle": 'solid', "LineWidth": 1., "AlphaLines": .9, 'Color':'g'}

ColorNi = 'purple'
ColorCo = 'c'
ColorCN = 'orange'


########################################################################################################################
# Nickel (111s)----------------------------------------------------------------
stego.promps.MinorSection('Adding steps to Plot: Gibbs - Ni(111s)')
plt.axes(axs[0][2])
plt.title('Reaction profile $\longrightarrow$')


# Global Rx from CO2
RefN111_e_CO2g = RefN111_e.branch()
stego.Plot.RxStep([CO2.Gibbs(**GibbsOpts)+4*H2.Gibbs(**GibbsOpts_H2),
                  CH4_g.Gibbs(**GibbsOpts) + 2*H2O.Gibbs(**GibbsOpts)],
                 Ref=RefN111_e_CO2g,
                 Name="Gas Rx",
                 Hover=HoverList, Color='k', StepSpan=6.5, LineWidth=1, LineStyle='dashed', AlphaLines=1.)


# .....................................
# CO2 series ..........................
# .....................................
RefN111_e_CO2 = RefN111_e.branch()

# Ads
stego.Plot.RxStep([CO2.Gibbs(**GibbsOpts) + N111s.Gibbs(**GibbsOpts),N1sR23_i.Gibbs(**GibbsOpts)],
                 Ref=RefN111_e_CO2,
                 Name='N1s/CO2ad:{}+(CO2) -> {CO2.tt}',
                 Hover=HoverList, Color=ColorNi, **Jump_Line_Props)

# N/R23 : CO2.tt -> CO.h + O.h(m)

stego.Plot.RxStepTS([N1sR23_i.Gibbs(**GibbsOpts), N1sR23_d.Gibbs(**GibbsOpts), N1sR23_f.Gibbs(**GibbsOpts)],
                   Ref=RefN111_e_CO2,
                   Name="N1s/R23: CO2.tt -> CO.h + O.h(m)",
                   Hover=HoverList, Color=ColorNi, **{**Main_Line_Props, "StepSpan": 1.})
# Name
# stego.Plot.AnnotateStepAxis(["$CO_{2}$",''], Ref=RefN111_e_CO2, Colour="k")
SectionRefs_N111e.UpdateFromTail(RefN111_e_CO2)






# # .....................................
# # CO desorbs ..........................
# # .....................................
# RefN111_e_CO_d = RefN111_e_CO2.branch()
#
# # N/(+O jump!) {CO.h + O.h(m)} + 1/2(H2) + {} -> {CO.h} + {O.f + H.h}
# stego.Plot.RxStep([N1sR23_f.Gibbs(**GibbsOpts) + 0.5 * H2.Gibbs(**GibbsOpts_H2) + N111s.Gibbs(**GibbsOpts),
#                   N1sR17_i.Gibbs(**GibbsOpts) + N1sR132_i.Gibbs(**GibbsOpts)],
#                  Ref=RefN111_e_CO_d,
#                  Name="N1s/(+O jump!) {CO.h + O.h(m)} + 1/2(H2) + {} -> {CO.h} + {O.h + H.f}",
#                  Hover=HoverList, Color="m", **Jump_Line_Props)
#
# stego.Plot.RxStep([N1sR17_i.Gibbs(**GibbsOpts), N111s.Gibbs(**GibbsOpts) + COg.Gibbs(**GibbsOpts)],
#                  Ref=RefN111_e_CO_d,
#                  Name="CO desorption",
#                  Hover=HoverList, Color='m', **Main_Line_Props_Co)

# # Global Rx from CO
# stego.Plot.RxStep([COg.Gibbs(**GibbsOpts)+3*H2.Gibbs(**GibbsOpts_H2) , CH4_g.Gibbs(**GibbsOpts)+H2O.Gibbs(**GibbsOpts)],
#                  Ref=RefN111_e_CO_d,
#                  Name="Gas Rx",
#                  Hover=HoverList, Color='c')




# .....................................
# HCO series ..........................
# .....................................
RefN111_e_HCO = RefN111_e_CO2.branch()

# Separe CO + O
# N/(+O jump!) {CO.h + O.h(m)} + H2 + {} -> {CO.h + H.h} + {O.f + H.h}
stego.Plot.RxStep([N1sR23_f.Gibbs(**GibbsOpts) + H2.Gibbs(**GibbsOpts_H2) + N111s.Gibbs(**GibbsOpts),
                  N1sR5_i.Gibbs(**GibbsOpts) + N1sR132_i.Gibbs(**GibbsOpts)],
                 Ref=RefN111_e_HCO,
                 Name="N1s/(+O jump!) {CO.h + O.h(m)} + H2 + {} -> {CO.h + H.h} + {O.h + H.f}",
                 Hover=HoverList, Color=ColorNi, **Jump_Line_Props)

# ----------------------------------
# OH elimination
RefN111_e_temp_OH = RefN111_e_HCO.branch()
stego.Plot.RxStepTS([N1sR132_i.Gibbs(**GibbsOpts), N1sR132_d.Gibbs(**GibbsOpts), N1sR132_f.Gibbs(**GibbsOpts)],
                   Ref=RefN111_e_temp_OH,
                   Name="N1s/R13.2 O.f + H.h -> OH.f",
                   Hover=HoverList, **OH_Line_Props)
# N/(+O jump!) {CO.h + O.h(m)} + H2 + {} -> {CO.h + H.h} + {O.f + H.h}
stego.Plot.RxStep([N1sR132_f.Gibbs(**GibbsOpts) + 0.5*H2.Gibbs(**GibbsOpts_H2),
                  N1sR28_i.Gibbs(**GibbsOpts)],
                 Ref=RefN111_e_temp_OH,
                 Name="N1s/(jump!) {OH} + 1/2 H2 -> {OH + H}",
                 Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStepTS([N1sR28_i.Gibbs(**GibbsOpts), N1sR28_d.Gibbs(**GibbsOpts), N1sR28_f.Gibbs(**GibbsOpts)],
                   Ref=RefN111_e_temp_OH,
                   Name="N1s/R28 OH + H -> H2O",
                   Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStep([N1sR28_f.Gibbs(**GibbsOpts),
                  H2O.Gibbs(**GibbsOpts)+ N111s.Gibbs(**GibbsOpts)],
                 Ref=RefN111_e_temp_OH,
                 Name="N1s/(jump!) {OH} + 1/2 H2 -> {OH + H}",
                 Hover=HoverList, **OH_Line_Props)

RefN111_e_HCO.UpdateFromTail(RefN111_e_temp_OH)
# ----------------------------------



# R5 (bridge): CO.h + H.h -> HCO.htO
stego.Plot.RxStepTS([N1sR5_i.Gibbs(**GibbsOpts), N1sR5_d.Gibbs(**GibbsOpts), N1sR5_f.Gibbs(**GibbsOpts)],
                   Ref=RefN111_e_HCO,
                   Name="N1s/R5(bridge): CO.h + H.h -> HCO.htO",
                   Hover=HoverList, Color=ColorNi, **Main_Line_Props)

# R15 (split): HCO.hcptO -> CH.fcc + O.fcc
stego.Plot.RxStepTS([N1sR15_i.Gibbs(**GibbsOpts), N1sR15_d.Gibbs(**GibbsOpts), N1sR15_f.Gibbs(**GibbsOpts)],
                   Ref=RefN111_e_HCO,
                   Name="N1s/R15(split): HCO.hcptO -> CH.fcc + O.fcc",
                   Hover=HoverList, Color=ColorNi, **Main_Line_Props)

# Separe {CH.f + O.f} + (H2) + {} -> {CH.h + H.h} + {O.f + H.f}
stego.Plot.RxStep([N1sR15_f.Gibbs(**GibbsOpts) + H2.Gibbs(**GibbsOpts_H2) + N111s.Gibbs(**GibbsOpts),
                  N1sR9top_i.Gibbs(**GibbsOpts) + N1sR132_i.Gibbs(**GibbsOpts)],
                 Ref=RefN111_e_HCO,
                 Name="N1s/(+ jump CH) {CH.f + O.f} + {H.f} -> {CH.f + H.h} + {O.f + H.f}",
                 Hover=HoverList, **OH_Line_Props)


# Section
SectionRefs_N111e.UpdateFromTail(RefN111_e_HCO)
# stego.Plot.AnnotateStepAxis(['','$HCO$',''], Ref=SectionRefs_N111e, Colour="g")



# ----------------------------------
# OH elimination
RefN111_e_temp_OH = RefN111_e_HCO.branch()
stego.Plot.RxStepTS([N1sR132_i.Gibbs(**GibbsOpts), N1sR132_d.Gibbs(**GibbsOpts), N1sR132_f.Gibbs(**GibbsOpts)],
                   Ref=RefN111_e_temp_OH,
                   Name="N1s/R13.2 O.f + H.h -> OH.f",
                   Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStep([N1sR132_f.Gibbs(**GibbsOpts) + 0.5*H2.Gibbs(**GibbsOpts_H2),
                  N1sR28_i.Gibbs(**GibbsOpts)],
                 Ref=RefN111_e_temp_OH,
                 Name="N1s/(jump!) {OH} + 1/2 H2 -> {OH + H}",
                 Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStepTS([N1sR28_i.Gibbs(**GibbsOpts), N1sR28_d.Gibbs(**GibbsOpts), N1sR28_f.Gibbs(**GibbsOpts)],
                   Ref=RefN111_e_temp_OH,
                   Name="N1s/R28 OH + H -> H2O",
                   Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStep([N1sR28_f.Gibbs(**GibbsOpts),
                  H2O.Gibbs(**GibbsOpts)+ N111s.Gibbs(**GibbsOpts)],
                 Ref=RefN111_e_temp_OH,
                 Name="N1s/(jump!) {OH} + 1/2 H2 -> {OH + H}",
                 Hover=HoverList, **OH_Line_Props)

RefN111_e_HCO.UpdateFromTail(RefN111_e_temp_OH)
# ----------------------------------




# .....................................
# CHx series ..........................
# .....................................
RefN111_e_CHx = RefN111_e_HCO.branch()

# ---- CH+H -> CH2

# Jump N/ R21 -> R9
# stego.Plot.RxStep([N1sR21top_f.Gibbs(**GibbsOpts) + (1. / 2.) * H2.Gibbs(**GibbsOpts_H2),
#                   N1sR9top_i.Gibbs(**GibbsOpts)],
#                  Ref=RefN111_e_CHx,
#                  Name='N1s/{CH.f}+(3/2)H2->{CH.f+H.h}+H2',
#                  Hover=HoverList, Color="k", **Jump_Line_Props)

# R9 on top: CH.f + H.h -> CH2.f
stego.Plot.RxStepTS([N1sR9top_i.Gibbs(**GibbsOpts), N1sR9top_TS.Gibbs(**GibbsOpts),
                    N1sR9top_f.Gibbs(**GibbsOpts)],
                   Ref=RefN111_e_CHx,
                   Name='N1s/R9 on top: CH.f + H.h -> CH2.f',
                   Hover=HoverList, Color=ColorNi, **Main_Line_Props)

# ---- CH2+H -> CH3

# Jump N/ R0 -> R10
stego.Plot.RxStep([N1sR9top_f.Gibbs(**GibbsOpts) + H2.Gibbs(**GibbsOpts_H2), N1sR10top_i.Gibbs(**GibbsOpts) + .5 * H2.Gibbs(**GibbsOpts_H2)],
                 Ref=RefN111_e_CHx,
                 Name='N1s/{CH2.f}+H2->{CH2.f+H.f}+(1./2.)*H2',
                 Hover=HoverList, Color=ColorNi, **Jump_Line_Props)

# R10 on top: CH2.f +H.f -> CH3.f
stego.Plot.RxStepTS([N1sR10top_i.Gibbs(**GibbsOpts), N1sR10top_TS.Gibbs(**GibbsOpts), N1sR10top_f.Gibbs(**GibbsOpts)],
                   Ref=RefN111_e_CHx,
                   Name='N1s/R10 on top: CH2.f +H.f -> CH3.f',
                   Hover=HoverList, Color=ColorNi, **Main_Line_Props)

# ---- CH3+H -> CH4

# Jump N/ R10 -> R11
stego.Plot.RxStep([N1sR10top_f.Gibbs(**GibbsOpts) + .5 * H2.Gibbs(**GibbsOpts_H2), N1sR11top_i.Gibbs(**GibbsOpts)],
                 Ref=RefN111_e_CHx,
                 Name='N1s/{CH3.f}+(1/2)H2->{CH3.f+H.f}',
                 Hover=HoverList, Color=ColorNi, **Jump_Line_Props)

# R11 on top: CH3.f +H.f -> CH4.g
stego.Plot.RxStepTS([N1sR11top_i.Gibbs(**GibbsOpts), N1sR11top_TS.Gibbs(**GibbsOpts), N1sR11top_f.Gibbs(**GibbsOpts)],
                   Ref=RefN111_e_CHx,
                   Name='N1s/R11 on top: CH3.f +H.f -> CH4.g',
                   Hover=HoverList, Color=ColorNi, **Main_Line_Props)

# Jump physisorption
stego.Plot.RxStep([N1sR11top_f.Gibbs(**GibbsOpts), CH4_g.Gibbs(**GibbsOpts) + N111s.Gibbs(**GibbsOpts)],
                 Ref=RefN111_e_CHx,
                 Name='N1s/{}CH4g->{}+CH4g',
                 Hover=HoverList, Color=ColorNi, **{**Main_Line_Props, 'StepSpan':.4})







SectionRefs_N111e.UpdateFromTail(RefN111_e_CHx)
# stego.Plot.AnnotateStepAxis(['$CH_{x}$', '$CH_{4(g)}$'], Ref=SectionRefs_N111e, Colour="k")
stego.Plot.Align_Rx_Ticks(SectionRefs_N111e, TSmode=False)



# ----------------------------------------------------------------------------------------------------------------------
# Cobalt ----------------------------------------------------------------
stego.promps.MinorSection('Adding steps to Plot: Gibbs - Co(111s)')
plt.axes(axs[0][0])
plt.title('Reaction profile $\longrightarrow$')






# Global Rx from CO2
RefC111_e_CO2g = RefC111_e.branch()
stego.Plot.RxStep([CO2.Gibbs(**GibbsOpts)+4*H2.Gibbs(**GibbsOpts_H2),
                  CH4_g.Gibbs(**GibbsOpts) + 2*H2O.Gibbs(**GibbsOpts)],
                 Ref=RefC111_e_CO2g,
                 Name="Gas Rx",
                 Hover=HoverList, Color='k', StepSpan=6.5, LineWidth=1, LineStyle='dashed', AlphaLines=1.)

# .....................................
# CO2 series ..........................
# .....................................
RefC111_e_CO2 = RefC111_e.branch()

# ads
stego.Plot.RxStep([CO2.Gibbs(**GibbsOpts) + C111s.Gibbs(**GibbsOpts), C1sR23_i.Gibbs(**GibbsOpts)],
                 Ref=RefC111_e_CO2,
                 Name='C1s/R23.1 (CO2)+{} -> {CO2.tt}',
                 Hover=HoverList, Color=ColorCo, **Jump_Line_Props)

# R23.1 CO2.tt -> CO.t + O.h
stego.Plot.RxStepTS([C1sR23_i.Gibbs(**GibbsOpts), C1sR23_d.Gibbs(**GibbsOpts), C1sR23_f.Gibbs(**GibbsOpts)],
                   Ref=RefC111_e_CO2,
                   Name="C1s/R23.1 CO2.tt -> CO.t + O.h",
                   Hover=HoverList, Color=ColorCo, **{**Main_Line_Props, "StepSpan": 1.})
# Section
SectionRefs_C111e.UpdateFromTail(RefC111_e_CO2)
# stego.Plot.AnnotateStepAxis(['$CO_{2}$',''], Ref=SectionRefs_C111e, Colour='k')





# # .....................................
# # CO desorbs ..........................
# # .....................................
# RefC111_e_CO_d = RefC111_e_CO2.branch()
#
# # ---------------- from CO.t (main path)
# # Separe {CO.t+O.h} + 1/2(H2) + {} -> {CO.t} + {O.h+H.f}
# stego.Plot.RxStep([C1sR23_f.Gibbs(**GibbsOpts) + 0.5 * H2.Gibbs(**GibbsOpts_H2) + C111s.Gibbs(**GibbsOpts), C1sR13_i.Gibbs(**GibbsOpts) + C1sR171_i.Gibbs(**GibbsOpts)],
#                  Ref=RefC111_e_CO_d,
#                  Name="C1s/ {CO.t+O.h} + 1/2(H2) + {} -> {CO.t} + {O.h+H.f}",
#                  Hover=HoverList, Color="m", **Jump_Line_Props)
#
# # Desorption
# stego.Plot.RxStep([C1sR171_i.Gibbs(**GibbsOpts), COg.Gibbs(**GibbsOpts) + C111s.Gibbs(**GibbsOpts)],
#                  Ref=RefC111_e_CO_d,
#                  Name="C1s/ {CO.t} -> (COg) + {}",
#                  Hover=HoverList, Color="m", **Main_Line_Props_Co)





# .....................................
# HCO series ..........................
# .....................................
RefC111_e_HCO = RefC111_e_CO2.branch()


# Separe/ {CO.t+O.h} + H2 + {} -> {CO.h+H.} + {O.h+H.f}
stego.Plot.RxStep([C1sR23_f.Gibbs(**GibbsOpts) + H2.Gibbs(**GibbsOpts_H2) + C111s.Gibbs(**GibbsOpts),
                  C1sR5h_i.Gibbs(**GibbsOpts) + C1sR13_i.Gibbs(**GibbsOpts)],
                 Ref=RefC111_e_HCO,
                 Name="C/ {CO.t+O.h}+(H2)+{} -> {CO.h+H.hd}+{O.h+H.f}",
                 Hover=HoverList, Color=ColorCo, **Jump_Line_Props)


# --------------------------------------------------------------------------------
# OH elimination
stego.Plot.RxStepTS([C1sR13_i.Gibbs(**GibbsOpts), C1sR13_d.Gibbs(**GibbsOpts), C1sR13_f.Gibbs(**GibbsOpts)],
                   Ref=RefC111_e_HCO,
                   Name="C1s/R13.2 O.h + H.f -(t)-> OH.h",
                   Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStep([C1sR13_f.Gibbs(**GibbsOpts) + 0.5*H2.Gibbs(**GibbsOpts_H2),
                  C1sR28_i.Gibbs(**GibbsOpts)],
                 Ref=RefC111_e_HCO,
                 Name="N1s/(jump!) {OH} + 1/2 H2 -> {OH + H}",
                 Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStepTS([C1sR28_i.Gibbs(**GibbsOpts), C1sR28_d.Gibbs(**GibbsOpts), C1sR28_f.Gibbs(**GibbsOpts)],
                   Ref=RefC111_e_HCO,
                   Name="N1s/R28 OH + H -> H2O",
                   Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStep([C1sR28_f.Gibbs(**GibbsOpts),
                  H2O.Gibbs(**GibbsOpts)+ C111s.Gibbs(**GibbsOpts)],
                 Ref=RefC111_e_HCO,
                 Name="N1s/(jump!) {H2O} -> {} + H2O",
                 Hover=HoverList, **OH_Line_Props)
# ----------------------------------






# C/R5 CO.h + H.hd -> HCO.hbO
stego.Plot.RxStepTS([C1sR5h_i.Gibbs(**GibbsOpts), C1sR5h_d.Gibbs(**GibbsOpts), C1sR5h_f.Gibbs(**GibbsOpts)],
                   Ref=RefC111_e_HCO,
                   Name="C/ CO.h+H.hd -> HCO.hbO(R5)",
                   Hover=HoverList, Color=ColorCo, **Main_Line_Props)

# C/R15 HCO.hbO -(split)-> CH.h + O.hm
stego.Plot.RxStepTS([C1sR15h_i.Gibbs(**GibbsOpts), C1sR15h_d.Gibbs(**GibbsOpts), C1sR15h_f.Gibbs(**GibbsOpts)],
                   Ref=RefC111_e_HCO,
                   Name="C1s/R15 HCO.fbO -(split)-> CH.h + O.hm",
                   Hover=HoverList, Color=ColorCo, **Main_Line_Props)

# Separe {CH.h + O.hm} + H2 + {} -> {CH.h} + {O.h + H.f}
stego.Plot.RxStep([C1sR15h_f.Gibbs(**GibbsOpts) + H2.Gibbs(**GibbsOpts_H2) + C111s.Gibbs(**GibbsOpts),
                  C1sR9_i.Gibbs(**GibbsOpts) + C1sR13_i.Gibbs(**GibbsOpts)],
                 Ref=RefC111_e_HCO,
                 Name="C1s/{CH.h + O.hm} + (H2) + {} -> {CH.h + H.f} + {O.h + H.f}",
                 Hover=HoverList, Color=ColorCo, **Jump_Line_Props)

# Converge branches
SectionRefs_C111e.UpdateFromTail(RefC111_e_HCO)
# stego.Plot.AnnotateStepAxis(['','$HCO$',''], Ref=SectionRefs_C111e, Colour="g")



# --------------------------------------------------------------------------------
# OH elimination
stego.Plot.RxStepTS([C1sR13_i.Gibbs(**GibbsOpts), C1sR13_d.Gibbs(**GibbsOpts), C1sR13_f.Gibbs(**GibbsOpts)],
                   Ref=RefC111_e_HCO,
                   Name="C1s/R13.2 O.h + H.f -(t)-> OH.h",
                   Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStep([C1sR13_f.Gibbs(**GibbsOpts) + 0.5*H2.Gibbs(**GibbsOpts_H2),
                  C1sR28_i.Gibbs(**GibbsOpts)],
                 Ref=RefC111_e_HCO,
                 Name="N1s/(jump!) {OH} + 1/2 H2 -> {OH + H}",
                 Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStepTS([C1sR28_i.Gibbs(**GibbsOpts), C1sR28_d.Gibbs(**GibbsOpts), C1sR28_f.Gibbs(**GibbsOpts)],
                   Ref=RefC111_e_HCO,
                   Name="N1s/R28 OH + H -> H2O",
                   Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStep([C1sR28_f.Gibbs(**GibbsOpts),
                  H2O.Gibbs(**GibbsOpts)+ C111s.Gibbs(**GibbsOpts)],
                 Ref=RefC111_e_HCO,
                 Name="N1s/(jump!) {H2O} -> {} + H2O",
                 Hover=HoverList, **OH_Line_Props)
# ----------------------------------



# .....................................
# CHx series ..........................
# .....................................
RefC111_e_CHx = RefC111_e_HCO.branch()


# ---- CH+H -> CH2

# # Jump C/ R21 -> R9
# stego.Plot.RxStep([C1sR21_f.Gibbs(**GibbsOpts) + (3. / 2.) * H2.Gibbs(**GibbsOpts_H2),
#                   C1sR9_i.Gibbs(**GibbsOpts) + H2.Gibbs(**GibbsOpts_H2)],
#                  Ref=RefC111_e_CHx,
#                  Name='C1s/{CH.h}+(3/2)*H2->{CH.h+H.f}+H2',
#                  Hover=HoverList, Color="k", **Jump_Line_Props)

# R9: CH.h + H.f -> CH2.h
stego.Plot.RxStepTS([C1sR9_i.Gibbs(**GibbsOpts), C1sR9_TS.Gibbs(**GibbsOpts), C1sR9_f.Gibbs(**GibbsOpts)],
                   Ref=RefC111_e_CHx,
                   Name='C11s/R9 on top: CH.h + H.f -> CH2.h',
                   Hover=HoverList, Color=ColorCo, **Main_Line_Props)

# ---- CH2+H -> CH3

# Jump C/ R9 -> R10
stego.Plot.RxStep([C1sR9_f.Gibbs(**GibbsOpts) + H2.Gibbs(**GibbsOpts_H2),
                  C1sR10_i.Gibbs(**GibbsOpts) + .5 * H2.Gibbs(**GibbsOpts_H2)],
                 Ref=RefC111_e_CHx,
                 Name='C1s/{CH2.h}+H2->{CH2.h+H.f}+(1/2)H2',
                 Hover=HoverList, Color=ColorCo, **Jump_Line_Props)

# R10: CH2.h + H.f -> CH3.h
stego.Plot.RxStepTS([C1sR10_i.Gibbs(**GibbsOpts), C1sR10_TS.Gibbs(**GibbsOpts), C1sR10_f.Gibbs(**GibbsOpts)],
                   Ref=RefC111_e_CHx,
                   Name='C1s/R10: CH2.h + H.f -> CH3.h',
                   Hover=HoverList, Color=ColorCo, **Main_Line_Props)

# ---- CH3+H -> CH4

# Jump C/ R10 -> R11
stego.Plot.RxStep([C1sR10_f.Gibbs(**GibbsOpts) + .5 * H2.Gibbs(**GibbsOpts_H2),
                  C1sR11_i.Gibbs(**GibbsOpts)],
                 Ref=RefC111_e_CHx,
                 Name='C1s/{CH3.h}+(1/2)H2->{CH2.h+H.f}',
                 Hover=HoverList, Color=ColorCo, **Jump_Line_Props)
# R11: CH3.h + H.f -> CH4.g
stego.Plot.RxStepTS([C1sR11_i.Gibbs(**GibbsOpts), C1sR11_TS.Gibbs(**GibbsOpts), C1sR11_f.Gibbs(**GibbsOpts)],
                   Ref=RefC111_e_CHx,
                   Name='C1s/R11: CH3.h + H.f -> CH4.g',
                   Hover=HoverList, Color=ColorCo, **Main_Line_Props)

# Physisorption
stego.Plot.RxStep([C1sR11_f.Gibbs(**GibbsOpts), CH4_g.Gibbs(**GibbsOpts) + C111s.Gibbs(**GibbsOpts)],
                 Ref=RefC111_e_CHx,
                 Name='C1s/R11 {}CH4->{}+CH4g',
                 Hover=HoverList, Color=ColorCo, **{**Main_Line_Props, 'StepSpan':.4})

# Jump Test whole path
# if ShowGlobal_e:
#     RefC111_e_full = RefC111_e.branch(Step=0)
#     stego.Plot.RxStep([C1s_Ch.Gibbs(**GibbsOpts) + 2 * H2.Gibbs(**GibbsOpts_H2), C111s.Gibbs(**GibbsOpts) + CH4_g.Gibbs(**GibbsOpts)],
#                      Ref=RefC111_e_full, Name='C1s/{C.hN+H.f}+2*H2->{}+CH4g',
#                      Hover=HoverList, StepSpan=2.4, Color='c', **LineProps)
#     RefC111_e_full.PlotExtend(Until=11, Color="c")

SectionRefs_C111e.UpdateFromTail(RefC111_e_CHx)
# stego.Plot.AnnotateStepAxis(['$CH_{x}$', '$CH_{4(g)}$'], Ref=SectionRefs_C111e, Colour="k")
stego.Plot.Align_Rx_Ticks(SectionRefs_C111e, TSmode=False)



# ----------------------------------------------------------------------------------------------------------------------
# Cobalt-Nickel ----------------------------------------------------------------
stego.promps.MinorSection('Adding steps to Plot: Gibbs - CoNi(111s)')
plt.axes(axs[0][1])
plt.title('Reaction profile $\longrightarrow$')



# Global Rx from CO2
RefCN111_e_CO2g = RefCN111_e.branch()
stego.Plot.RxStep([CO2.Gibbs(**GibbsOpts)+4*H2.Gibbs(**GibbsOpts_H2),
                  CH4_g.Gibbs(**GibbsOpts) + 2*H2O.Gibbs(**GibbsOpts)],
                 Ref=RefCN111_e_CO2g,
                 Name="Gas Rx",
                 Hover=HoverList, Color='k', StepSpan=6.5, LineWidth=1, LineStyle='dashed', AlphaLines=1.)





# .....................................
# CO2 series ..........................
# .....................................

RefCN111_e_CO2 = RefCN111_e.branch()

# ads
stego.Plot.RxStep([CO2.Gibbs(**GibbsOpts) + CN111s.Gibbs(**GibbsOpts), CN1sR23_i.Gibbs(**GibbsOpts)],
                 Ref=RefCN111_e_CO2,
                 Name='CN1s/(CO2)+{} -> {CO2.tCtC}',
                 Hover=HoverList, Color=ColorCN, **Jump_Line_Props)

# CN/R23 CO
stego.Plot.RxStepTS([CN1sR23_i.Gibbs(**GibbsOpts), CN1sR23_d.Gibbs(**GibbsOpts), CN1sR23_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN111_e_CO2,
                   Name="CN1s/R23-d CO2.tCtC -> CO.tC + O.hC",
                   Hover=HoverList, Color=ColorCN, **{**Main_Line_Props, "StepSpan": 1.})

# Section
SectionRefs_CN111e.UpdateFromTail(RefCN111_e_CO2)
# stego.Plot.AnnotateStepAxis(['$CO_{2}$',''], Ref=RefCN111_e_CO2, Colour='k')



# # .....................................
# # CO desorbs ..........................
# # .....................................
# RefCN111_e_CO_desorb = RefCN111_e_CO2.branch()
#
# # -------------------------------- ruta 1: O+H/C
#
# # Separate/ {CO.tC + O.hC} + 1/2(H2) + {} -> {CO.tC} + {O+H/R13.2C}
# stego.Plot.RxStep([CN1sR23_f.Gibbs(**GibbsOpts) + 0.5 * H2.Gibbs(**GibbsOpts_H2) + CN111s.Gibbs(**GibbsOpts),
#                   CN1sR17bCN_i.Gibbs(**GibbsOpts) + CN1sR132C_i.Gibbs(**GibbsOpts)],
#                  Ref=RefCN111_e_CO_desorb,
#                  Name="CN/{CO.tC + O.hC} + 1/2(H2) + {} -> {CO.tC} + {O.fN + H.fN}",
#                  Hover=HoverList, Color='r', **Jump_Line_Props)
#
# # CO desorption
# stego.Plot.RxStep([CN1sR17bCN_i.Gibbs(**GibbsOpts), COg.Gibbs(**GibbsOpts) + CN111s.Gibbs(**GibbsOpts)],
#                  Ref=RefCN111_e_CO_desorb,
#                  Name="CO desorb",
#                  Hover=HoverList, Color='m', **Main_Line_Props_Co)






# .....................................
# HCO series ..........................
# .....................................
RefCN111_e_HCO = RefCN111_e_CO2.branch()

# # ------------------------------------------------ Ruta HCO.hNbOC
# RefCN111_e_HCOb = RefCN111_e_HCO.branch()
#
# # Separe/ {CO.tC + O.hC} + (H2) + {} -> {(R5b) CO.hN + H.fN} + {(R13.2C) O.fN+H.hN}
# stego.Plot.RxStep([CN1sR23_f.Gibbs(**GibbsOpts) + H2.Gibbs(**GibbsOpts_H2) + CN111s.Gibbs(**GibbsOpts), CN1sR5b_i.Gibbs(**GibbsOpts) + CN1sR132C_i.Gibbs(**GibbsOpts)],
#                  Ref=RefCN111_e_HCOb,
#                  Name="{CO.tC + O.hC} +(H2) + {} -> {(R5b) CO.hN + H.fN} + {(R13.2C) O.fN+H.hN}",
#                  Hover=HoverList, Color='g', **Jump_Line_Props)
#
# # OH elimination (C) (branched out)
# stego.Plot.RxStepTS([CN1sR132C_i.Gibbs(**GibbsOpts), CN1sR132C_d.Gibbs(**GibbsOpts), CN1sR132C_f.Gibbs(**GibbsOpts)],
#                    Ref=RefCN111_e_HCOb, UpdateRef=False,
#                    Name="CN1s/R13.2C-i O.fN+H.hN -(C)-> OH.fN",
#                    Hover=HoverList, Color='b', **OH_Line_Props)
#
# # CN/R5 CO.hN + H.fN -> HCO.hNbOC
# stego.Plot.RxStepTS([CN1sR5b_i.Gibbs(**GibbsOpts), CN1sR5b_d.Gibbs(**GibbsOpts), CN1sR5b_f.Gibbs(**GibbsOpts)],
#                    Ref=RefCN111_e_HCOb,
#                    Name="CN/R5 CO.hN + H.fN -> HCO.hNbOC",
#                    Hover=HoverList, Color="g", **Main_Line_Props)
#
# # CN/R15 HCO.hNbOC -> CH.fC + O.fN
# stego.Plot.RxStepTS([CN1sR15C_i.Gibbs(**GibbsOpts), CN1sR15C_d.Gibbs(**GibbsOpts), CN1sR15C_f.Gibbs(**GibbsOpts)],
#                    Ref=RefCN111_e_HCOb,
#                    Name="CN/R15 HCO.hNbOC -> CH.fC + O.fN",
#                    Hover=HoverList, Color="g", **Main_Line_Props)
#
# # Separe CN/{CH.fC + O.fN} + 1/2(H2) + {} -> {(R21)CH.hN}  + {(R13.2C) O.fN+H.hN}
# stego.Plot.RxStep([CN1sR15C_f.Gibbs(**GibbsOpts) + 0.5*H2.Gibbs(**GibbsOpts_H2) + CN111s.Gibbs(**GibbsOpts), CN1sR21C_f.Gibbs(**GibbsOpts) + CN1sR132C_i.Gibbs(**GibbsOpts)],
#                  Ref=RefCN111_e_HCOb,
#                  Name="CN/{CH.fC + O.fN} + {H.hN} -> {(R21)CH.hN}  + {(R13.2C) O.fN+H.hN}",
#                  Hover=HoverList, Color="g", **Jump_Line_Props)
#
# # OH elimination (C)
# stego.Plot.RxStepTS([CN1sR132C_i.Gibbs(**GibbsOpts), CN1sR132C_d.Gibbs(**GibbsOpts), CN1sR132C_f.Gibbs(**GibbsOpts)],
#                    Ref=RefCN111_e_HCOb,
#                    Name="CN1s/R13.2C-i O.fN+H.hN -(C)-> OH.fN",
#                    Hover=HoverList, Color='b', **OH_Line_Props)

# ------------------------------------------------ Ruta HCO.tCtC (secundaria)

# Separe CN/ {CO.tC + O.hC} + H2 + {} -> {CO.hN + H.fN}+{(R13.2C) O.fN+H.hN}
stego.Plot.RxStep([CN1sR23_f.Gibbs(**GibbsOpts) + H2.Gibbs(**GibbsOpts_H2) + CN111s.Gibbs(**GibbsOpts),
                  CN1sR5bt_i.Gibbs(**GibbsOpts) + CN1sR132C_i.Gibbs(**GibbsOpts)],
                 Ref=RefCN111_e_HCO,
                 Name="CN/ {CO.tC + O.hC} + 2*{H.fN} -> {CO.hN + H.fN}+{(R13.2C) O.fN+H.hN} + {}",
                 Hover=HoverList, Color=ColorCN, **Jump_Line_Props)

# --------------------------------------------------------------------------
# OH elimination (C) (branched out)
stego.Plot.RxStepTS([CN1sR132N_i.Gibbs(**GibbsOpts), CN1sR132N_d.Gibbs(**GibbsOpts), CN1sR132N_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN111_e_HCO, UpdateRef=False,
                   Name="CN1s/R13.2C-i O.fN+H.hN -(C)-> OH.fN",
                   Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStepTS([CN1sR132C_i.Gibbs(**GibbsOpts), CN1sR132C_d.Gibbs(**GibbsOpts), CN1sR132C_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN111_e_HCO,
                   Name="CN1s/R13.2C-i O.fN+H.hN -(C)-> OH.fN",
                   Hover=HoverList, **OH_Line_Props)

stego.Plot.RxStep([CN1sR132C_f.Gibbs(**GibbsOpts) + 0.5*H2.Gibbs(**GibbsOpts_H2),
                  CN1sR28C_i.Gibbs(**GibbsOpts)],
                 Ref=RefCN111_e_HCO,
                 Name="N1s/(jump!) {OH} + 1/2 H2 -> {OH + H}",
                 Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStepTS([CN1sR28C_i.Gibbs(**GibbsOpts), CN1sR28C_d.Gibbs(**GibbsOpts), CN1sR28C_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN111_e_HCO,
                   Name="N1s/R28 OH + H -> H2O",
                   Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStep([CN1sR28C_f.Gibbs(**GibbsOpts),
                  H2O.Gibbs(**GibbsOpts)+ CN111s.Gibbs(**GibbsOpts)],
                 Ref=RefCN111_e_HCO,
                 Name="N1s/(jump!) {H2O} -> {} + H2O",
                 Hover=HoverList, **OH_Line_Props)
# --------------------------------------------------------------------------



# CN/R5bt CO.hN + H.fN -> HCO.tCtC
stego.Plot.RxStepTS([CN1sR5bt_i.Gibbs(**GibbsOpts), CN1sR5bt_d.Gibbs(**GibbsOpts), CN1sR5bt_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN111_e_HCO,
                   Name="CN/R5 CO.hN + H.fN -> HCO.tCtC",
                   Hover=HoverList, Color=ColorCN, **Main_Line_Props)

# CN/R15 HCO.tCtC -> CH.fC + O.fN
stego.Plot.RxStepTS([CN1sR15tCtC_i.Gibbs(**GibbsOpts), CN1sR15tCtC_d.Gibbs(**GibbsOpts), CN1sR15tCtC_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN111_e_HCO,
                   Name="CN/R15 HCO.tCtC -> CH.fC + O.fN",
                   Hover=HoverList, Color=ColorCN, **Main_Line_Props)

# Compile Refs
# RefCN111_e_HCO.UpdateFromTail(RefCN111_e_HCOb)
SectionRefs_CN111e.UpdateFromTail(RefCN111_e_HCO)
# stego.Plot.AnnotateStepAxis(['$HCO$'], Ref=SectionRefs_CN111e, Colour="g")




# --------------------------------------------------------------------------
# OH elimination (C) (branched out)
stego.Plot.RxStepTS([CN1sR132N_i.Gibbs(**GibbsOpts), CN1sR132N_d.Gibbs(**GibbsOpts), CN1sR132N_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN111_e_HCO, UpdateRef=False,
                   Name="CN1s/R13.2C-i O.fN+H.hN -(C)-> OH.fN",
                   Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStepTS([CN1sR132C_i.Gibbs(**GibbsOpts), CN1sR132C_d.Gibbs(**GibbsOpts), CN1sR132C_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN111_e_HCO,
                   Name="CN1s/R13.2C-i O.fN+H.hN -(C)-> OH.fN",
                   Hover=HoverList, **OH_Line_Props)

stego.Plot.RxStep([CN1sR132C_f.Gibbs(**GibbsOpts) + 0.5*H2.Gibbs(**GibbsOpts_H2),
                  CN1sR28C_i.Gibbs(**GibbsOpts)],
                 Ref=RefCN111_e_HCO,
                 Name="N1s/(jump!) {OH} + 1/2 H2 -> {OH + H}",
                 Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStepTS([CN1sR28C_i.Gibbs(**GibbsOpts), CN1sR28C_d.Gibbs(**GibbsOpts), CN1sR28C_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN111_e_HCO,
                   Name="N1s/R28 OH + H -> H2O",
                   Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStep([CN1sR28C_f.Gibbs(**GibbsOpts),
                  H2O.Gibbs(**GibbsOpts)+ CN111s.Gibbs(**GibbsOpts)],
                 Ref=RefCN111_e_HCO,
                 Name="N1s/(jump!) {H2O} -> {} + H2O",
                 Hover=HoverList, **OH_Line_Props)
# --------------------------------------------------------------------------



# .....................................
# CHx series ..........................
# .....................................
RefCN111_e_CHx = RefCN111_e_HCO.branch()


# ---- CH+H -> CH2

# Jump CN/ R21C -> R9C
stego.Plot.RxStep([CN1sR15tCtC_f.Gibbs(**GibbsOpts) + H2.Gibbs(**GibbsOpts_H2) + CN111s.Gibbs(**GibbsOpts_H2),
                  CN1sR9C_i.Gibbs(**GibbsOpts) + CN1sR132C_i.Gibbs(**GibbsOpts)],
                 Ref=RefCN111_e_CHx,
                 Name='CN1s/{CH.fC + O.fN} + (H2) + {} -> {CH.hN + H.fN} + {O.fN + H.hN}',
                 Hover=HoverList, Color=ColorCN, **Jump_Line_Props)

# R9C: CH.hN + H.fN -> CH2.hNtC
stego.Plot.RxStepTS([CN1sR9C_i.Gibbs(**GibbsOpts), CN1sR9C_TS.Gibbs(**GibbsOpts), CN1sR9C_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN111_e_CHx,
                   Name='CN1s/R9C: CH.hN + H.fN -> CH2.hNtC',
                   Hover=HoverList, Color=ColorCN, **Main_Line_Props)

# ---- CH2+H -> CH3

# Jump CN/ R9C -> R10C
stego.Plot.RxStep([CN1sR9C_f.Gibbs(**GibbsOpts) + H2.Gibbs(**GibbsOpts_H2),
                  CN1sR10C_i.Gibbs(**GibbsOpts) + .5 * H2.Gibbs(**GibbsOpts_H2)],
                 Ref=RefCN111_e_CHx,
                 Name='CN1s/{CH2.hNtC}+H2->{CH2.hNtC+H.fN}+(1/2)H2',
                 Hover=HoverList, Color=ColorCN, **Jump_Line_Props)

# R10C: CH2.hNtC + H.fN -> CH3.hN
stego.Plot.RxStepTS([CN1sR10C_i.Gibbs(**GibbsOpts), CN1sR10C_TS.Gibbs(**GibbsOpts), CN1sR10C_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN111_e_CHx,
                   Name='CN1s/R10C: CH2.hNtC + H.fN -> CH3.hN',
                   Hover=HoverList, Color=ColorCN, **Main_Line_Props)



# ---- CH3+H -(C)-> CH4

# Jump CN/ R10C -> R11C
stego.Plot.RxStep([CN1sR10C_f.Gibbs(**GibbsOpts) + .5 * H2.Gibbs(**GibbsOpts_H2),
                  CN1sR11C_i.Gibbs(**GibbsOpts)],
                 Ref=RefCN111_e_CHx,
                 Name='CN1s/{CH3.hN}+(1/2)H2->{CH3.hN+H.fN}',
                 Hover=HoverList, Color=ColorCN, **Jump_Line_Props)

# R11C: CH3.hN + H.fN -> CH4.g
stego.Plot.RxStepTS([CN1sR11C_i.Gibbs(**GibbsOpts), CN1sR11C_TS.Gibbs(**GibbsOpts), CN1sR11C_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN111_e_CHx,
                   Name='CN1s/R11C CH3.hN + H.fN -> CH4g',
                   Hover=HoverList, Color=ColorCN, **Main_Line_Props)

# Physisorption
stego.Plot.RxStep([CN1sR11C_f.Gibbs(**GibbsOpts),
                  CN111s.Gibbs(**GibbsOpts) + CH4_g.Gibbs(**GibbsOpts)],
                 Ref=RefCN111_e_CHx,
                 Name='CN1s/{}CH4g->{}+CH4g',
                 Hover=HoverList, Color=ColorCN, **{**Main_Line_Props, 'StepSpan':.4})

# Jump Test whole path
# if ShowGlobal_e:
#     RefCN111_e_full = RefCN111_e.branch(Step=0)
#     stego.Plot.RxStep([CN1s_ChN.Gibbs(**GibbsOpts) + 2 * H2.Gibbs(**GibbsOpts_H2),
#                       CN111s.Gibbs(**GibbsOpts) + CH4_g.Gibbs(**GibbsOpts)],
#                      Ref=RefCN111_e_full, Name='CN1s/{C.hN+H.hN}+2*H2->{}+CH4g',
#                      Hover=HoverList, StepSpan=2.4, Color='k', **LineProps)
#     RefCN111_e_full.PlotExtend(Until=11., Color="m", **LineProps)


SectionRefs_CN111e.UpdateFromTail(RefCN111_e_CHx)
# stego.Plot.AnnotateStepAxis(['$CH_{x}$', '$CH_{4(g)}$'], Ref=SectionRefs_CN111e, Colour="k")
stego.Plot.Align_Rx_Ticks(SectionRefs_CN111e, TSmode=False)


########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
# (100) ----------------------------------------------------------------------------------------------------------------

# References
RefN100_e = stego.Plot.RxRef(0., 0.)
RefC100_e = stego.Plot.RxRef(0., 0.)
RefCN100_e = stego.Plot.RxRef(0., 0.)

# Place holders
SectionRefs_N100e = RefN100_e.branch()
SectionRefs_C100e = RefC100_e.branch()
SectionRefs_CN100e = RefCN100_e.branch()




# ----------------------------------------------------------------------------------------------------------------------
# Nickel ---------------------------------------------------------------------------------------------------------------
stego.promps.MinorSection('Adding steps to Plot: Gibbs - Ni(100)')
plt.axes(axs[1][2])




# Global Rx from CO2
RefN100_e_CO2g = RefN100_e.branch()
stego.Plot.RxStep([CO2.Gibbs(**GibbsOpts)+4*H2.Gibbs(**GibbsOpts_H2),
                  CH4_g.Gibbs(**GibbsOpts) + 2*H2O.Gibbs(**GibbsOpts)],
                 Ref=RefN100_e_CO2g,
                 Name="Gas Rx",
                 Hover=HoverList, Color='k', StepSpan=6.9, LineWidth=1, LineStyle='dashed', AlphaLines=1.)



# .....................................
# CO2 series ..........................
# .....................................
RefN100_e_CO2 = RefN100_e.branch()

# ads
stego.Plot.RxStep([CO2.Gibbs(**GibbsOpts) + N100.Gibbs(**GibbsOpts), N10R23_1_i.Gibbs(**GibbsOpts)],
                 Ref=RefN100_e_CO2,
                 Name='N100/(CO2)+{} -> {CO2.hbh}',
                 Hover=HoverList, Color=ColorNi, **Jump_Line_Props)

# N/ {CO2.bhb} -> {CO.b + O.h} (R32.1)
stego.Plot.RxStepTS([N10R23_1_i.Gibbs(**GibbsOpts), N10R23_1_d.Gibbs(**GibbsOpts), N10R23_1_f.Gibbs(**GibbsOpts)],
                   Ref=RefN100_e_CO2,
                   Name='N/R23.1 CO2.bhb->CO.b+O.h',
                   Hover=HoverList, Color=ColorNi, **{**Main_Line_Props, "StepSpan": 1.})


# section
SectionRefs_N100e.UpdateFromTail(RefN100_e_CO2)
# stego.Plot.AnnotateStepAxis(['$CO_{2}$',''], Ref=SectionRefs_N100e, Colour='k')




# # .....................................
# # CO desorb ...........................
# # .....................................
# RefN100_e_CO_des = RefN100_e_CO2.branch()
#
# # Separe/ {CO.b+O.h} + 1/2(H2) + {} -> {CO.h}+{O.h+H.hd} (Split R23.1 -> R17, R13.2)
# stego.Plot.RxStep([N10R23_1_f.Gibbs(**GibbsOpts) + 0.5 * H2.Gibbs(**GibbsOpts_H2) + N100.Gibbs(**GibbsOpts),
#                   N10R17_i.Gibbs(**GibbsOpts) + N10R13_2_i.Gibbs(**GibbsOpts)],
#                  Ref=RefN100_e_CO_des,
#                  Name='N/{CO.b+O.h}+1/2(H2)+{} -> {CO.h}+{O.h+H.hd}',
#                  Hover=HoverList, Color='r', **Jump_Line_Props)
# # CO desorbs
# stego.Plot.RxStep([N10R17_i.Gibbs(**GibbsOpts), N100.Gibbs(**GibbsOpts) + COg.Gibbs(**GibbsOpts)],
#                  Ref=RefN100_e_CO_des,
#                  Name='CO desorbs',
#                  Hover=HoverList, Color='m', **Main_Line_Props_Co)



# .....................................
# COH series ..........................
# .....................................
RefN100_e_COH = RefN100_e_CO2.branch()



# Separe/ {CO.b + O.h} + H2 + {} -> {CO.h + H.hd} + {O.h + H.hd} (Split R23.1 -> R6,R13.2)
stego.Plot.RxStep([N10R23_1_f.Gibbs(**GibbsOpts) + H2.Gibbs(**GibbsOpts_H2) + N100.Gibbs(**GibbsOpts), N10R6_i.Gibbs(**GibbsOpts) + N10R13_2_i.Gibbs(**GibbsOpts)],
                 Ref=RefN100_e_COH,
                 Name='N/{CO.b+O.h}+(H2)+{} -> {CO.h+H.hd}+{O.h+H.hd}',
                 Hover=HoverList, Color=ColorNi, **Jump_Line_Props)

# -----------------------------------------------------------------------------------------
# OH elimination {O.h + H.hd} -> {OH.h} (R13.2) (branched out)
stego.Plot.RxStepTS([N10R13_2_i.Gibbs(**GibbsOpts), N10R13_2_d.Gibbs(**GibbsOpts), N10R13_2_f.Gibbs(**GibbsOpts)],
                   Ref=RefN100_e_COH,
                   Name='R13.2 O.h + H.hd -> OH.h',
                   Hover=HoverList, **OH_Line_Props)

stego.Plot.RxStep([N10R13_2_f.Gibbs(**GibbsOpts)+0.5*H2.Gibbs(**GibbsOpts_H2),
                  N10R28_i.Gibbs(**GibbsOpts)],
                 Ref=RefN100_e_COH,
                 Name='R13.2 -> R28',
                 Hover=HoverList, **OH_Line_Props)

stego.Plot.RxStepTS([N10R28_i.Gibbs(**GibbsOpts), N10R28_d.Gibbs(**GibbsOpts), N10R28_f.Gibbs(**GibbsOpts)],
                   Ref=RefN100_e_COH,
                   Name='R28 OH.h + H.hd -> H2O',
                   Hover=HoverList, **OH_Line_Props)

stego.Plot.RxStep([N10R28_f.Gibbs(**GibbsOpts),
                  H2O.Gibbs(**GibbsOpts)+N100.Gibbs(**GibbsOpts)],
                 Ref=RefN100_e_COH,
                 Name='R13.2 O.h + H.hd -> OH.h',
                 Hover=HoverList, **OH_Line_Props)
# -----------------------------------------------------------------------------------------




# N/R6 {CO.h + H.hd} -> {COH.h} (R6)
stego.Plot.RxStepTS([N10R6_i.Gibbs(**GibbsOpts), N10R6_d.Gibbs(**GibbsOpts), N10R6_f.Gibbs(**GibbsOpts)],
                   Ref=RefN100_e_COH,
                   Name='N/R6: CO.h+H.hd->COH.ht',
                   Hover=HoverList, Color=ColorNi, **Main_Line_Props)

# N/R16 {COH.ht} -> {C.h + OH.hd} (R16)
stego.Plot.RxStepTS([N10R16_i.Gibbs(**GibbsOpts), N10R16_d.Gibbs(**GibbsOpts), N10R16_f.Gibbs(**GibbsOpts)],
                   Ref=RefN100_e_COH,
                   Name='N/R16: COH.ht->C.h+OH.hd',
                   Hover=HoverList, Color=ColorNi, **Main_Line_Props)



# Name and tick
SectionRefs_N100e.UpdateFromTail(RefN100_e_COH)
# stego.Plot.AnnotateStepAxis(['','$COH$',''], Ref=SectionRefs_N100e, Colour="m")


# .....................................
# CHx series ..........................
# .....................................
RefN100_e_CHx = RefN100_e_COH.branch()



# Separe/ {C.h + OH.h} + {} + 1/2(H2) -> {C.h + H.hd} + {OH.h} (R16 -> R21, R13.2)
stego.Plot.RxStep([N10R16_f.Gibbs(**GibbsOpts) + N100.Gibbs(**GibbsOpts) + (1/2) * H2.Gibbs(**GibbsOpts_H2),
                  N10R21_i.Gibbs(**GibbsOpts) + N10R13_2_f.Gibbs(**GibbsOpts)],
                 Ref=RefN100_e_CHx,
                 Name='{C.h + OH.h} + {} + 1/2(H2) -> {C.h + H.h} + {OH.h}',
                 Hover=HoverList, Color=ColorNi, **Jump_Line_Props)

# -----------------------------------------------------------------------------------------
# OH elimination

stego.Plot.RxStep([N10R13_2_f.Gibbs(**GibbsOpts)+0.5*H2.Gibbs(**GibbsOpts_H2),
                  N10R28_i.Gibbs(**GibbsOpts)],
                 Ref=RefN100_e_CHx,
                 Name='R13.2 -> R28',
                 Hover=HoverList, **OH_Line_Props)

stego.Plot.RxStepTS([N10R28_i.Gibbs(**GibbsOpts), N10R28_d.Gibbs(**GibbsOpts), N10R28_f.Gibbs(**GibbsOpts)],
                   Ref=RefN100_e_CHx,
                   Name='R28 OH.h + H.hd -> H2O',
                   Hover=HoverList, **OH_Line_Props)

stego.Plot.RxStep([N10R28_f.Gibbs(**GibbsOpts),
                  H2O.Gibbs(**GibbsOpts)+N100.Gibbs(**GibbsOpts)],
                 Ref=RefN100_e_CHx,
                 Name='R13.2 O.h + H.hd -> OH.h',
                 Hover=HoverList, **OH_Line_Props)

# -----------------------------------------------------------------------------------------


# N/R21 C.h+H.f->CH
stego.Plot.RxStepTS([N10R21_i.Gibbs(**GibbsOpts), N10R21_d.Gibbs(**GibbsOpts), N10R21_f.Gibbs(**GibbsOpts)],
                   Ref=RefN100_e_CHx,
                   Name='N/R21: C.h + H.h -> CH.h',
                   Hover=HoverList, Color=ColorNi, **Main_Line_Props)

# ---- CH-CH2

# Jump C/ R21 -> R9
stego.Plot.RxStep([N10R21_f.Gibbs(**GibbsOpts) + (3. / 2.) * H2.Gibbs(**GibbsOpts_H2),
                  N10R9_i.Gibbs(**GibbsOpts) + H2.Gibbs(**GibbsOpts_H2)],
                 Ref=RefN100_e_CHx,
                 Name='N/{CH.h}+(3/2)H2->{CH.h+H.h}+H2',
                 Hover=HoverList, Color=ColorNi, **Jump_Line_Props)

# N/R9 CH.h+H.f->CH2.hb
stego.Plot.RxStepTS([N10R9_i.Gibbs(**GibbsOpts), N10R9_d.Gibbs(**GibbsOpts), N10R9_f.Gibbs(**GibbsOpts)],
                   Ref=RefN100_e_CHx,
                   Name='N/R9: CH.h + H.h -> CH2.hb',
                   Hover=HoverList, Color=ColorNi, **Main_Line_Props)

# ---- CH2-CH3

# Jump C/ R9 -> R10
stego.Plot.RxStep([N10R9_f.Gibbs(**GibbsOpts) + H2.Gibbs(**GibbsOpts_H2),
                  N10R10_i.Gibbs(**GibbsOpts) + .5 * H2.Gibbs(**GibbsOpts_H2)],
                 Ref=RefN100_e_CHx,
                 Name='N/{CH2.hb}+H2 -> {CH2.hb+H.hd}+(1/2)H2',
                 Hover=HoverList, Color=ColorNi, **Jump_Line_Props)
# N/R10 CH2.hb+H.f->CH3.b3
stego.Plot.RxStepTS([N10R10_i.Gibbs(**GibbsOpts), N10R10_d.Gibbs(**GibbsOpts), N10R10_f.Gibbs(**GibbsOpts)],
                   Ref=RefN100_e_CHx,
                   Name='N/R10: CH2.hb + H.h -> CH3.b3',
                   Hover=HoverList, Color=ColorNi, **Main_Line_Props)

# ---- CH3-CH4

# Jump C/ R10 -> R11
stego.Plot.RxStep([N10R10_f.Gibbs(**GibbsOpts) + .5 * H2.Gibbs(**GibbsOpts_H2),
                  N10R11_i.Gibbs(**GibbsOpts)],
                 Ref=RefN100_e_CHx,
                 Name='N/{CH3.b}+(1/2)H2->{CH3.hb+H.hd}',
                 Hover=HoverList, Color=ColorNi, **Jump_Line_Props)

# N/R11 CH3.hb + H.hd -> CH4.g
stego.Plot.RxStepTS([N10R11_i.Gibbs(**GibbsOpts), N10R11_TS.Gibbs(**GibbsOpts), N10R11_f.Gibbs(**GibbsOpts)],
                   Ref=RefN100_e_CHx,
                   Name='N/R11: CH3.hb + H.hd -> CH4.g',
                   Hover=HoverList, Color=ColorNi, **Main_Line_Props)

# ---- Physisorption
stego.Plot.RxStep([N10R11_f.Gibbs(**GibbsOpts), N100.Gibbs(**GibbsOpts) + CH4_g.Gibbs(**GibbsOpts)],
                 Ref=RefN100_e_CHx,
                 Name='N/{}CH4g->{}+CH4g',
                 Hover=HoverList, Color=ColorNi, **{**Main_Line_Props, 'StepSpan':.4})

# Jump Test complete series
# if ShowGlobal_e:
#     RefN_e_2 = RefN100_e.branch(Step=0)
#     stego.Plot.RxStep([N100_Ch.Gibbs(**GibbsOpts) + 2 * H2.Gibbs(**GibbsOpts_H2),
#                       N100.Gibbs(**GibbsOpts) + CH4_g.Gibbs(**GibbsOpts)], Ref=RefN_e_2, Name='{C.h+H.h}+2*H2->{}+CH4g',
#                      Hover=HoverList, StepSpan=4.4, **LineProps, Color="orange")
#     RefN_e_2.PlotExtend(Until=11, Color="orange", **LineProps)

SectionRefs_N100e.UpdateFromTail(RefN100_e_CHx)
# stego.Plot.AnnotateStepAxis(['$CH_{x}$', '$CH_{4(g)}$'], Ref=SectionRefs_N100e, Colour="k")
stego.Plot.Align_Rx_Ticks(SectionRefs_N100e, TSmode=False)

# ----------------------------------------------------------------------------------------------------------------------
# Cobalt ---------------------------------------------------------------------------------------------------------------
stego.promps.MinorSection('Adding steps to Plot: Gibbs - Co(100)')
plt.axes(axs[1][0])

# Global Rx from CO2
RefC100_e_CO2g = RefC100_e.branch()
stego.Plot.RxStep([CO2.Gibbs(**GibbsOpts)+4*H2.Gibbs(**GibbsOpts_H2),
                  CH4_g.Gibbs(**GibbsOpts) + 2*H2O.Gibbs(**GibbsOpts)],
                 Ref=RefC100_e_CO2g,
                 Name="Gas Rx",
                 Hover=HoverList, Color='k', StepSpan=6.9, LineWidth=1, LineStyle='dashed', AlphaLines=1.)


# .....................................
# CO2 series ..........................
# .....................................
RefC100_e_CO2 = RefC100_e.branch()

# ads
stego.Plot.RxStep([CO2.Gibbs(**GibbsOpts)+C100.Gibbs(**GibbsOpts), C10R23_i.Gibbs(**GibbsOpts)],
                 Ref=RefC100_e_CO2,
                 Name='C100/(CO2)+{} --> {CO2}',
                 Hover=HoverList, Color=ColorCo, **Jump_Line_Props)

stego.Plot.RxStepTS([C10R23_i.Gibbs(**GibbsOpts), C10R23_d.Gibbs(**GibbsOpts), C10R23_f.Gibbs(**GibbsOpts)],
                   Ref=RefC100_e_CO2,
                   Name='C/R23d CO2 -> CO.t + O.h',
                   Hover=HoverList, Color=ColorCo, **{**Main_Line_Props, "StepSpan": 1.})
# Section
SectionRefs_C100e.UpdateFromTail(RefC100_e_CO2)
# stego.Plot.AnnotateStepAxis(['$CO_{2}$',''], Ref=SectionRefs_C100e, Colour='k')


# # .....................................
# # CO desorbs  .........................
# # .....................................
# RefC100_e_CO_des = RefC100_e_CO2.branch()
#
#
# # Separe/ {CO.t+O.h}+1/2(H2)+{}->{CO.t}+{O.h+H.h} (split R23->R17, R13.2)
# stego.Plot.RxStep([C10R23_f.Gibbs(**GibbsOpts) + 0.5 * H2.Gibbs(**GibbsOpts_H2) + C100.Gibbs(**GibbsOpts),
#                   C10R17t_i.Gibbs(**GibbsOpts) + C10R132_i.Gibbs(**GibbsOpts)],
#                  Ref=RefC100_e_CO_des,
#                  Name='C/{CO.t+O.h}+{H.h}->{CO.t}+{O.h+H.d}',
#                  Hover=HoverList, Color='r', **Jump_Line_Props)
# # CO desorbs
# stego.Plot.RxStep([C10R17t_i.Gibbs(**GibbsOpts), COg.Gibbs(**GibbsOpts)+C100.Gibbs(**GibbsOpts)],
#                  Ref=RefC100_e_CO_des,
#                  Name='CO desorbs',
#                  Hover=HoverList, Color='m', **Main_Line_Props_Co
#                  )






# .....................................
# CO series ...........................
# .....................................
RefC100_e_CO = RefC100_e_CO2.branch()


# Separe/ {CO.t+O.h}+1/2(H2)+{}->{CO.t}+{O.h+H.h} (split R23->R17, R13.2)
stego.Plot.RxStep([C10R23_f.Gibbs(**GibbsOpts) + 0.5 * H2.Gibbs(**GibbsOpts_H2) + C100.Gibbs(**GibbsOpts),
                  C10R17t_i.Gibbs(**GibbsOpts) + C10R132_i.Gibbs(**GibbsOpts)],
                 Ref=RefC100_e_CO,
                 Name='C/{CO.t+O.h}+{H.h}->{CO.t}+{O.h+H.d}',
                 Hover=HoverList, Color=ColorCo, **Jump_Line_Props)

# -----------------------------------------------------------------------------------------
# OH elimination {O.h+H.hd} -> {OH.h} (R13.2) (branched out)
stego.Plot.RxStepTS([C10R132_i.Gibbs(**GibbsOpts), C10R132_d.Gibbs(**GibbsOpts), C10R132_f.Gibbs(**GibbsOpts)],
                   Ref=RefC100_e_CO,
                   Name="C/R13.2: O.h + H.h -(t)-> OH.h",
                   Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStep([C10R132_f.Gibbs(**GibbsOpts)+0.5*H2.Gibbs(**GibbsOpts_H2),
                  C10R28_i.Gibbs(**GibbsOpts)],
                 Ref=RefC100_e_CO,
                 Name='R13.2 -> R28 OH.h + 1/2H2 -> OH + H',
                 Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStepTS([C10R28_i.Gibbs(**GibbsOpts), C10R28_d.Gibbs(**GibbsOpts), C10R28_f.Gibbs(**GibbsOpts)],
                   Ref=RefC100_e_CO,
                   Name="C/R28: OH.h + H.h -(t)-> OH.h",
                   Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStep([C10R28_f.Gibbs(**GibbsOpts),
                  H2O.Gibbs(**GibbsOpts)+C100.Gibbs(**GibbsOpts)],
                 Ref=RefC100_e_CO,
                 Name='R13.2 O.h + H.hd -> OH.h',
                 Hover=HoverList, **OH_Line_Props)
# -----------------------------------------------------------------------------------------


# C/{CO.t} -> {C.h + O.h} (R17t)
stego.Plot.RxStepTS([C10R17t_i.Gibbs(**GibbsOpts), C10R17t_d.Gibbs(**GibbsOpts), C10R17t_f.Gibbs(**GibbsOpts)],
                   Ref=RefC100_e_CO,
                   Name='C/R17.1d CO.t -> C.h + O.h',
                   Hover=HoverList, Color=ColorCo, **Main_Line_Props)

# Separe/ {C.h+O.h}+1/2(H2) + {} -> {C.h}+{O.h+H.h} (split R17-> R21, R13.2)
stego.Plot.RxStep([C10R17t_f.Gibbs(**GibbsOpts) + 0.5 * H2.Gibbs(**GibbsOpts_H2) + C100.Gibbs(**GibbsOpts),
                  C100_Ch.Gibbs(**GibbsOpts) + C10R132_i.Gibbs(**GibbsOpts)],
                 Ref=RefC100_e_CO,
                 Name='C/{C.h+O.h}+1/2(H2)+{} -> {C.h+H.h}+{O.h+H.h}',
                 Hover=HoverList, Color=ColorCo, **Jump_Line_Props)

# -----------------------------------------------------------------------------------------
# OH elimination {O.h+H.hd} -> {OH.h} (R13.2) (branched out)
stego.Plot.RxStepTS([C10R132_i.Gibbs(**GibbsOpts), C10R132_d.Gibbs(**GibbsOpts), C10R132_f.Gibbs(**GibbsOpts)],
                   Ref=RefC100_e_CO,
                   Name="C/R13.2: O.h + H.h -(t)-> OH.h",
                   Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStep([C10R132_f.Gibbs(**GibbsOpts)+0.5*H2.Gibbs(**GibbsOpts_H2),
                  C10R28_i.Gibbs(**GibbsOpts)],
                 Ref=RefC100_e_CO,
                 Name='R13.2 -> R28 OH.h + 1/2H2 -> OH + H',
                 Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStepTS([C10R28_i.Gibbs(**GibbsOpts), C10R28_d.Gibbs(**GibbsOpts), C10R28_f.Gibbs(**GibbsOpts)],
                   Ref=RefC100_e_CO,
                   Name="C/R28: OH.h + H.h -(t)-> OH.h",
                   Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStep([C10R28_f.Gibbs(**GibbsOpts),
                  H2O.Gibbs(**GibbsOpts)+C100.Gibbs(**GibbsOpts)],
                 Ref=RefC100_e_CO,
                 Name='R13.2 O.h + H.hd -> OH.h',
                 Hover=HoverList, **OH_Line_Props)
# -----------------------------------------------------------------------------------------

# Section
SectionRefs_C100e.UpdateFromTail(RefC100_e_CO)
# stego.Plot.AnnotateStepAxis(['$CO$',''], Ref=SectionRefs_C100e, Colour="r")





# .....................................
# CHx series ..........................
# .....................................
RefC100_e_CHx = RefC100_e_CO.branch()

# ---- C.h + H.h -> CH.h

stego.Plot.RxStep([C100_Ch.Gibbs(**GibbsOpts) + 2. * H2.Gibbs(**GibbsOpts_H2),
                  C10R21_i.Gibbs(**GibbsOpts) + (3. / 2.) * H2.Gibbs(**GibbsOpts_H2)],
                 Ref=RefC100_e_CHx,
                 Name="C100/{C.h}+2*H2 -> {C.h+H.h}+(3/2)*H2",
                 Hover=HoverList, Color=ColorCo, **Jump_Line_Props)
# C/R21 C.h+H.f->CH.h
stego.Plot.RxStepTS([C10R21_i.Gibbs(**GibbsOpts), C10R21_d.Gibbs(**GibbsOpts), C10R21_f.Gibbs(**GibbsOpts)],
                   Ref=RefC100_e_CHx,
                   Name='C/R21: C.h + H.h -> CH.h',
                   Hover=HoverList, Color=ColorCo, **Main_Line_Props)

# ---- CH->CH2

# Jump C/ R21 -> R9
stego.Plot.RxStep([C10R21_f.Gibbs(**GibbsOpts) + (3. / 2.) * H2.Gibbs(**GibbsOpts_H2),
                  C10R9_i.Gibbs(**GibbsOpts) + H2.Gibbs(**GibbsOpts_H2)],
                 Ref=RefC100_e_CHx,
                 Name='C/{CH.h}+(3/2)*H2->{CH.h+H.h}+H2',
                 Hover=HoverList, Color=ColorCo, **Jump_Line_Props)

# C/R9 CH.h+H.f->CH2.hb
stego.Plot.RxStepTS([C10R9_i.Gibbs(**GibbsOpts), C10R9_d.Gibbs(**GibbsOpts), C10R9_f.Gibbs(**GibbsOpts)],
                   Ref=RefC100_e_CHx,
                   Name='C/R9: CH.h + H.h -> CH2.h',
                   Hover=HoverList, Color=ColorCo, **Main_Line_Props)

# ---- CH2->CH3

# Jump C/ R9 -> R10
stego.Plot.RxStep([C10R9_f.Gibbs(**GibbsOpts) + H2.Gibbs(**GibbsOpts_H2),
                  C10R10_i.Gibbs(**GibbsOpts) + .5 * H2.Gibbs(**GibbsOpts_H2)],
                 Ref=RefC100_e_CHx,
                 Name='C/{CH2.h}+H2->{CH2.h+H.hd}+(1/2)H2',
                 Hover=HoverList, Color=ColorCo, **Jump_Line_Props)

# C/R10 CH2.h + H.hd -> CH3.b3
stego.Plot.RxStepTS([C10R10_i.Gibbs(**GibbsOpts), C10R10_d.Gibbs(**GibbsOpts), C10R10_f.Gibbs(**GibbsOpts)],
                   Ref=RefC100_e_CHx,
                   Name='C/R10: CH2.h + H.hd -> CH3.b',
                   Hover=HoverList, Color=ColorCo, **Main_Line_Props)

# ---- CH3->CH4

# Jump C/ R10 -> R11
stego.Plot.RxStep([C10R10_f.Gibbs(**GibbsOpts) + .5 * H2.Gibbs(**GibbsOpts_H2),
                  C10R11_i.Gibbs(**GibbsOpts)],
                 Ref=RefC100_e_CHx,
                 Name='C/{CH3.h}+{H.h}->{CH3.h+H.hd}',
                 Hover=HoverList, Color=ColorCo, **Jump_Line_Props)

# C/R11 CH3.b + H.hd -> CH4.g
stego.Plot.RxStepTS([C10R11_i.Gibbs(**GibbsOpts), C10R11_TS.Gibbs(**GibbsOpts), C10R11_f.Gibbs(**GibbsOpts)],
                   Ref=RefC100_e_CHx,
                   Name='C/R11: CH3.b + H.hd -> CH4.g',
                   Hover=HoverList, Color=ColorCo, **Main_Line_Props)

# ---- Physisorption
stego.Plot.RxStep([C10R11_f.Gibbs(**GibbsOpts), C100.Gibbs(**GibbsOpts) + CH4_g.Gibbs(**GibbsOpts)],
                 Ref=RefC100_e_CHx,
                 Name='C/{}CH4g->{}+CH4g',
                 Hover=HoverList, Color=ColorCo, **{**Main_Line_Props, 'StepSpan':.4})

# Jump test complete
# if ShowGlobal_e:
#     RefC100_e_full = RefC100_e.branch(Step=0)
#     stego.Plot.RxStep([C100_Ch.Gibbs(**GibbsOpts) + 2 * H2.Gibbs(**GibbsOpts_H2),
#                       C100.Gibbs(**GibbsOpts) + CH4_g.Gibbs(**GibbsOpts)],
#                      Ref=RefC100_e_full, Name='C/{C.h+H.h}+2*H2 -> {}+CH4g',
#                      Hover=HoverList, StepSpan=4.4, **LineProps)
#     RefC100_e_full.PlotExtend(Until=11., Color="gray", **LineProps)

SectionRefs_C100e.UpdateFromTail(RefC100_e_CHx)
# stego.Plot.AnnotateStepAxis(['$CH_{x}$', '$CH_{4(g)}$'], Ref=SectionRefs_C100e, Colour="k")
stego.Plot.Align_Rx_Ticks(SectionRefs_C100e, TSmode=False)






# ----------------------------------------------------------------------------------------------------------------------
# Cobalt-Nickel --------------------------------------------------------------------------------------------------------
stego.promps.MinorSection('Adding steps to Plot: Gibbs - CoNi(100)')
plt.axes(axs[1][1])
extend = 1.4

# Global Rx from CO2
RefCN100_e_CO2g = RefCN100_e.branch()
stego.Plot.RxStep([CO2.Gibbs(**GibbsOpts)+4*H2.Gibbs(**GibbsOpts_H2),
                  CH4_g.Gibbs(**GibbsOpts) + 2*H2O.Gibbs(**GibbsOpts)],
                 Ref=RefCN100_e_CO2g,
                 Name="Gas Rx",
                 Hover=HoverList, Color='k', StepSpan=8., LineWidth=1, LineStyle='dashed', AlphaLines=1.)


# .....................................
# CO2 series ..........................
# .....................................
RefCN100_e_CO2 = RefCN100_e.branch()

# ads
stego.Plot.RxStep([CO2.Gibbs(**GibbsOpts)+CN100.Gibbs(**GibbsOpts), CN10R23_i.Gibbs(**GibbsOpts)],
                 Ref=RefCN100_e_CO2,
                 Name='CN100/(CO2)+{} -> {CO2.hNbb}',
                 Hover=HoverList, Color=ColorCN, **Jump_Line_Props)

# CN/R23 CO2.hNbb -(b)-> CO.bCN + O.hC
stego.Plot.RxStepTS([CN10R23_i.Gibbs(**GibbsOpts), CN10R23_d.Gibbs(**GibbsOpts), CN10R23_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN100_e_CO2,
                   Name="CN/R23 CO2.hNbb -> CO.bCN + O.hC",
                   Hover=HoverList, Color=ColorCN, **{**Main_Line_Props, "StepSpan": 1.})

# Section
SectionRefs_CN100e.UpdateFromTail(RefCN100_e_CO2)
# stego.Plot.AnnotateStepAxis(['$CO_{2}$',''], Ref=SectionRefs_CN100e, Colour='k')





# # .....................................
# # CO desorbs ..........................
# # .....................................
# RefCN100_e_CO_des = RefCN100_e_CO2.branch()
#
# # Separe/ {CO.bCN+O.hC}+ 1/2(H2) + {} -> {CO.tC} + {O+H/R13.2C}
# stego.Plot.RxStep([CN10R23_f.Gibbs(**GibbsOpts) + 0.5*H2.Gibbs(**GibbsOpts_H2) + CN100.Gibbs(**GibbsOpts), CN10R17tC_i.Gibbs(**GibbsOpts) + CN10R132C_i.Gibbs(**GibbsOpts)],
#                  Ref=RefCN100_e_CO_des,
#                  Name="CN/{CO.bCN+O.hC}+1/2(H2)+{}->{CO.tC} + {O+H/R13.2C}",
#                  Hover=HoverList, Color='r', **Jump_Line_Props)
# # CO desorbs
# stego.Plot.RxStep([CN10R17tC_i.Gibbs(**GibbsOpts), CN100.Gibbs(**GibbsOpts) + COg.Gibbs(**GibbsOpts)],
#                  Ref=RefCN100_e_CO_des,
#                  Name="CO desorbs",
#                  Hover=HoverList, Color='m', **Main_Line_Props_Co
#                  )







# .....................................
# CO series ...........................
# .....................................
RefCN100_e_CO = RefCN100_e_CO2.branch()

# ----------------------------------------------- branch 1 CO.tC, OH-R13C
RefCN100_e_CO_1 = RefCN100_e_CO.branch()

# Separe/ {CO.bCN+O.hC}+ 1/2(H2) + {} -> {CO.tC} + {O+H/R13.2C}
stego.Plot.RxStep([CN10R23_f.Gibbs(**GibbsOpts) + 0.5*H2.Gibbs(**GibbsOpts_H2) + CN100.Gibbs(**GibbsOpts),
                  CN10R17tC_i.Gibbs(**GibbsOpts) + CN10R132C_i.Gibbs(**GibbsOpts)],
                 Ref=RefCN100_e_CO_1,
                 Name="CN/{CO.bCN+O.hC}+1/2(H2)+{}->{CO.tC} + {O+H/R13.2C}",
                 Hover=HoverList, Color=ColorCN, **Jump_Line_Props)

# --------------------------------------------------------------------------------------
# OH elimination
stego.Plot.RxStepTS([CN10R132C_i.Gibbs(**GibbsOpts), CN10R132C_d.Gibbs(**GibbsOpts), CN10R132C_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN100_e_CO_1,
                   Name="CN(R13C)/O.h + H.h -(tC)-> OH.h",
                   Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStep([CN10R132C_f.Gibbs(**GibbsOpts)+0.5*H2.Gibbs(**GibbsOpts_H2),
                  CN10R28C_i.Gibbs(**GibbsOpts)],
                 Ref=RefCN100_e_CO_1,
                 Name='R13.2->R28 {OH} + (H2) -> {OH+H}',
                 Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStepTS([CN10R28C_i.Gibbs(**GibbsOpts), CN10R28C_d.Gibbs(**GibbsOpts), CN10R28C_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN100_e_CO_1,
                   Name="CN(R28C)/OH + H -(tC)-> H2O",
                   Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStep([CN10R28C_f.Gibbs(**GibbsOpts),
                  H2O.Gibbs(**GibbsOpts)+CN100.Gibbs(**GibbsOpts)],
                 Ref=RefCN100_e_CO_1,
                 Name='R13.2 O.h + H.hd -> OH.h',
                 Hover=HoverList, **OH_Line_Props)
# --------------------------------------------------------------------------------------




# CN(R17tC)/ {CO.tC} -> {C.hN + O.hC}
stego.Plot.RxStepTS([CN10R17tC_i.Gibbs(**GibbsOpts),
                    CN10R17tC_d.Gibbs(**GibbsOpts),
                    CN10R17tC_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN100_e_CO_1,
                   Name="CN/R13tC CO.tC -> C.hN + O.hC",
                   Hover=HoverList, Color=ColorCN, **{**Main_Line_Props, "StepSpan": 1.3*extend})

# Separe/ {C.hN + O.hC}+1/2(H2)+{} -> {C.hN} + {(R13C) O.h + H.h} + {}
stego.Plot.RxStep([CN10R17tC_f.Gibbs(**GibbsOpts) + 1. * H2.Gibbs(**GibbsOpts_H2) + CN100.Gibbs(**GibbsOpts),
                  # CN100_ChN.Gibbs(**GibbsOpts) + CN10R132C_i.Gibbs(**GibbsOpts)],
                  CN10R21_i.Gibbs(**GibbsOpts) + CN10R132C_i.Gibbs(**GibbsOpts)],
                 Ref=RefCN100_e_CO_1,
                 Name="CN/ {C.hN + O.hC}+1/2(H2)+{} -> {C.hN} + {(R13C) OH.h}",
                 Hover=HoverList, Color=ColorCN, **Jump_Line_Props)
SectionRefs_CN100e.UpdateFromTail(RefCN100_e_CO_1)

# --------------------------------------------------------------------------------------
# OH elimination
stego.Plot.RxStepTS([CN10R132C_i.Gibbs(**GibbsOpts), CN10R132C_d.Gibbs(**GibbsOpts), CN10R132C_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN100_e_CO_1,
                   Name="CN(R13C)/O.h + H.h -(tC)-> OH.h",
                   Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStep([CN10R132C_f.Gibbs(**GibbsOpts)+0.5*H2.Gibbs(**GibbsOpts_H2),
                  CN10R28C_i.Gibbs(**GibbsOpts)],
                 Ref=RefCN100_e_CO_1,
                 Name='R13.2->R28 {OH} + (H2) -> {OH+H}',
                 Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStepTS([CN10R28C_i.Gibbs(**GibbsOpts), CN10R28C_d.Gibbs(**GibbsOpts), CN10R28C_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN100_e_CO_1,
                   Name="CN(R28C)/OH + H -(tC)-> H2O",
                   Hover=HoverList, **OH_Line_Props)
stego.Plot.RxStep([CN10R28C_f.Gibbs(**GibbsOpts),
                  H2O.Gibbs(**GibbsOpts)+CN100.Gibbs(**GibbsOpts)],
                 Ref=RefCN100_e_CO_1,
                 Name='R13.2 O.h + H.hd -> OH.h',
                 Hover=HoverList, **OH_Line_Props)
# --------------------------------------------------------------------------------------


# Compile branches, section
RefCN100_e_CO.UpdateFromTail(RefCN100_e_CO_1)
# SectionRefs_CN100e.UpdateFromTail(RefCN100_e_CO)
# stego.Plot.AnnotateStepAxis(['$CO$',''], Ref=SectionRefs_CN100e, Colour="r")




# # .....................................
# # HCO series ..........................
# # .....................................
# RefCN100_e_HCO = RefCN100_e_CO2.branch()
# RefCN100_e_HCO.PlotExtend(Until=5.0, Color='m')
#
#
# # Separe/ {CO.bCN+O.hC} + H2 + {} -> {CO.hN + H.hNd} + {(R13C) O.h + H.h} (split R23->R5, R13.2C)
# stego.Plot.RxStep([CN10R23_f.Gibbs(**GibbsOpts) + H2.Gibbs(**GibbsOpts_H2) + CN100.Gibbs(**GibbsOpts), CN10R5tN_i.Gibbs(**GibbsOpts) + CN10R132C_i.Gibbs(**GibbsOpts)],
#                  Ref=RefCN100_e_HCO,
#                  Name="CN/ {CO.bCN+O.hC}+(H2)+{}->{CO.hN+H.hNd}+{(R13C)O.h+H.h}",
#                  Hover=HoverList, Color='g', **Jump_Line_Props)
#
# # OH elimination R13C {O.h + H.h} -(tC)-> {OH.h}
# stego.Plot.RxStepTS([CN10R132C_i.Gibbs(**GibbsOpts), CN10R132C_d.Gibbs(**GibbsOpts), CN10R132C_f.Gibbs(**GibbsOpts)],
#                    Ref=RefCN100_e_HCO, UpdateRef=False,
#                    Name="CN(R13C)/O.h + H.h -(tC)-> OH.h",
#                    Hover=HoverList, Color='b', **OH_Line_Props)
#
# # CN/R5 CO.hN + H.hNd -> HCO.bbN
# stego.Plot.RxStepTS([CN10R5tN_i.Gibbs(**GibbsOpts), CN10R5tN_d.Gibbs(**GibbsOpts), CN10R5tN_f.Gibbs(**GibbsOpts)],
#                    Ref=RefCN100_e_HCO,
#                    Name="CN/R5 CO.hN + H.hNd -> HCO.bbN",
#                    Hover=HoverList, Color='g', **Main_Line_Props)
#
# # CN/R15 HCO.bbN -(b)-> CH.hN + O.hC
# stego.Plot.RxStepTS([CN10R15b_i.Gibbs(**GibbsOpts), CN10R15b_d.Gibbs(**GibbsOpts), CN10R15b_f.Gibbs(**GibbsOpts)],
#                    Ref=RefCN100_e_HCO,
#                    Name="CN10/R15b-d HCO.bbN -(b)-> CH.hN + O.hC",
#                    Hover=HoverList, Color='g', **Main_Line_Props)
#
# # Separe/ {CH.hN + O.hC} + 1/2(H2) + {} -> {CH.hN} + {(R13C) O.h + H.h}
# stego.Plot.RxStep([CN10R15b_f.Gibbs(**GibbsOpts) + 0.5 * H2.Gibbs(**GibbsOpts_H2) + CN100.Gibbs(**GibbsOpts), CN10R21_f.Gibbs(**GibbsOpts) + CN10R132C_i.Gibbs(**GibbsOpts)],
#                  Ref=RefCN100_e_HCO,
#                  Name="CN/ {CH.hN + O.hC} + 1/2(H2) + {} -> {CH.hN} + {(R13C) O.h + H.h}",
#                  Hover=HoverList, Color='g', **Jump_Line_Props)
#
# # OH elimination R13C {O.h + H.h} -(tC)-> {OH.h}
# stego.Plot.RxStepTS([CN10R132C_i.Gibbs(**GibbsOpts), CN10R132C_d.Gibbs(**GibbsOpts), CN10R132C_f.Gibbs(**GibbsOpts)],
#                    Ref=RefCN100_e_HCO,
#                    Name="CN(R13C)/O.h + H.h -(tC)-> OH.h",
#                    Hover=HoverList, Color='b', **OH_Line_Props)
#
# # Section
# SectionRefs_CN100e.UpdateFromTail(RefCN100_e_HCO)
# stego.Plot.AnnotateStepAxis(['','$HCO$',''], Ref=SectionRefs_CN100e, Colour="g")



# .....................................
# COH series ..........................
# .....................................
RefCN100_e_COH = RefCN100_e_CO_1.branch(Step=-7)


# Separe/ {CO.bCN + O.hC}+(H2)+{} -> {CO.hN+H.hNd}+{(R132C)O.h+H.h}
stego.Plot.RxStep([CN10R17tC_i.Gibbs(**GibbsOpts) + 0.5*H2.Gibbs(**GibbsOpts_H2),
                  CN10R6tN_i.Gibbs(**GibbsOpts)],
                 Ref=RefCN100_e_COH,
                 Name="CN/{CO}+1/2(H2) -> {CO.hN+H.hNd}",
                 Hover=HoverList, Color=ColorCN, **{**Jump_Line_Props, "LineStyle":'dotted', 'LineWidth':1.5})

# #--------------------------------------------------------------------------------------------------
# # OH elimination R13C {O.h + H.h} -(tC)-> {OH.h}
# stego.Plot.RxStepTS([CN10R132C_i.Gibbs(**GibbsOpts), CN10R132C_d.Gibbs(**GibbsOpts), CN10R132C_f.Gibbs(**GibbsOpts)],
#                    Ref=RefCN100_e_COH,
#                    Name="CN(R13C)/O.h + H.h -(tC)-> OH.h",
#                    Hover=HoverList, **OH_Line_Props)
# stego.Plot.RxStep([CN10R132C_f.Gibbs(**GibbsOpts)+0.5*H2.Gibbs(**GibbsOpts_H2),
#                   H2O.Gibbs(**GibbsOpts)+CN100.Gibbs(**GibbsOpts)],
#                  Ref=RefCN100_e_COH,
#                  Name='R13.2 O.h + H.hd -> OH.h',
#                  Hover=HoverList, **{**OH_Line_Props, 'StepSpan':.4})
#--------------------------------------------------------------------------------------------------

# CN/R6tN CO.hN + H.hNd -> COH.hNtN
stego.Plot.RxStepTS([CN10R6tN_i.Gibbs(**GibbsOpts), CN10R6tN_d.Gibbs(**GibbsOpts), CN10R6tN_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN100_e_COH,
                   Name="CN/R6tN CO.hN + H.hNd -> COH.hNtN",
                   Hover=HoverList, Color=ColorCN, **{**Main_Line_Props, "StepSpan":0.5*extend,
                                                      "LineStyle":'dotted', 'LineWidth':1.5})

# CN/R16tN COH.hNtN -> C.hN + OH.hN
stego.Plot.RxStepTS([CN10R16tN_i.Gibbs(**GibbsOpts), CN10R16tN_d.Gibbs(**GibbsOpts), CN10R16tN_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN100_e_COH,
                   Name="CN/R16tN COH.hNtN -> C.hN + OH.hN",
                   Hover=HoverList, Color=ColorCN, **{**Main_Line_Props, "StepSpan":0.5*extend,
                                                      "LineStyle":'dotted', 'LineWidth':1.5})

# Separe/ {C.hN + OH.hN}+{} -> {C.hN} + {(R132C)OH.hN}
stego.Plot.RxStep([CN10R16tN_f.Gibbs(**GibbsOpts) + CN100.Gibbs(**GibbsOpts) + H2.Gibbs(**GibbsOpts_H2),
                  CN10R21_i.Gibbs(**GibbsOpts) + CN10R28C_i.Gibbs(**GibbsOpts)],
                 Ref=RefCN100_e_COH,
                 Name="CN/ {C.hN + OH.hN}+1/2H2+{} -> {C.hN+H}+{(R132C)OH.hN}",
                 Hover=HoverList, Color=ColorCN, **{**Jump_Line_Props, "StepSpan":.8, "LineStyle":'dotted', 'LineWidth':1.5}, zorder=0)

#--------------------------------------------------------------------------------------------------
# # OH elimination
# stego.Plot.RxStepTS([CN10R28C_i.Gibbs(**GibbsOpts), CN10R28C_d.Gibbs(**GibbsOpts), CN10R28C_f.Gibbs(**GibbsOpts)],
#                    Ref=RefCN100_e_COH,
#                    Name="CN(R28C)/OH + H -(tC)-> H2O",
#                    Hover=HoverList, **OH_Line_Props)
# stego.Plot.RxStep([CN10R28C_f.Gibbs(**GibbsOpts),
#                   H2O.Gibbs(**GibbsOpts)+CN100.Gibbs(**GibbsOpts)],
#                  Ref=RefCN100_e_COH,
#                  Name='R13.2 O.h + H.hd -> OH.h',
#                  Hover=HoverList, **OH_Line_Props)
#--------------------------------------------------------------------------------------------------

# Sections
# SectionRefs_CN100e.UpdateFromTail(RefCN100_e_COH)
# stego.Plot.AnnotateStepAxis(['','$COH$',''], Ref=SectionRefs_CN100e, Colour="m")



# .....................................
# CHx series ..........................
# .....................................


RefCN100_e_CHx = RefCN100_e_CO.branch()
# RefCN100_e_CHx.PlotExtend(Until=12., Color='m', Alpha=1, LineWidth=.8)


# # ---- C.hN + H.hC -> CH.hN
# stego.Plot.RxStep([CN100_ChN.Gibbs(**GibbsOpts) + 2 * H2.Gibbs(**GibbsOpts_H2),
#                   CN10R21_i.Gibbs(**GibbsOpts) + (3. / 2.) * H2.Gibbs(**GibbsOpts_H2)],
#                  Ref=RefCN100_e_CHx,
#                  Name="CN100/ {C.hN}+2*H2 -> {C.hN+H.hC}+(3/2)H2",
#                  Hover=HoverList, Color="k", **Jump_Line_Props)

# CN/R21 C.h+H.f->CH.h
stego.Plot.RxStepTS([CN10R21_i.Gibbs(**GibbsOpts), CN10R21_d.Gibbs(**GibbsOpts), CN10R21_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN100_e_CHx,
                   Name='CN/R21: C.hN + H.hC -> CH.hN',
                   Hover=HoverList, Color=ColorCN, **Main_Line_Props)

# ---- CH -> CH2

# Jump C/ R21 -> R9
stego.Plot.RxStep([CN10R21_f.Gibbs(**GibbsOpts) + (3. / 2.) * H2.Gibbs(**GibbsOpts_H2),
                  CN10R9_i.Gibbs(**GibbsOpts) + H2.Gibbs(**GibbsOpts_H2)],
                 Ref=RefCN100_e_CHx,
                 Name='CN/{CH.hN}+H(3/2)2->{CH.hN+h.hC}+H2',
                 Hover=HoverList, Color=ColorCN, **Jump_Line_Props)

# CN/R9 CH.hN+H.hC->CH2.hNb
stego.Plot.RxStepTS([CN10R9_i.Gibbs(**GibbsOpts), CN10R9_d.Gibbs(**GibbsOpts), CN10R9_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN100_e_CHx,
                   Name='CN/R9: CH.hN + H.hC -> CH2.hNb',
                   Hover=HoverList, Color=ColorCN, **Main_Line_Props)


# ---- CH2 -> CH3
# ramificación primaria

# Jump C/ R9 -> R10-C
stego.Plot.RxStep([CN10R9_f.Gibbs(**GibbsOpts) + H2.Gibbs(**GibbsOpts_H2),
                  CN10R10tCbC_i.Gibbs(**GibbsOpts) + .5 * H2.Gibbs(**GibbsOpts_H2)],
                 Ref=RefCN100_e_CHx,
                 Name='CN/{CH2.hN}+H2->{CH2.hN+h.hN}+(1/2)H2',
                 Hover=HoverList, Color=ColorCN, **Jump_Line_Props)

# CN/R10 tCbC
stego.Plot.RxStepTS([CN10R10tCbC_i.Gibbs(**GibbsOpts),
                    CN10R10tCbC_TS.Gibbs(**GibbsOpts),
                    CN10R10tCbC_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN100_e_CHx,
                   Name='CN/R10-C: CH2.hN + H.hN -> CH3.bC',
                   Hover=HoverList, Color=ColorCN, **Main_Line_Props)



# # ---- CH2 -> CH3
# # ramificación secundaria
# RefCN100_e_CHx_2 = RefCN100_e_CHx.branch()
#
# # Jump C/ R9 -> R10-N
# stego.Plot.RxStep([CN10R9_f.Gibbs(**GibbsOpts) + H2.Gibbs(**GibbsOpts_H2),
#                   CN10R10tN_i.Gibbs(**GibbsOpts) + .5 * H2.Gibbs(**GibbsOpts_H2)],
#                  Ref=RefCN100_e_CHx_2,
#                  Name='CN/{CH2.hN}+H2->{CH2.hN+h.hN}+(1/2)H2',
#                  Hover=HoverList, Color="r", **Jump_Line_Props)
# # CN/R10 tN
# stego.Plot.RxStepTS([CN10R10tN_i.Gibbs(**GibbsOpts), CN10R10tN_TS.Gibbs(**GibbsOpts), CN10R10tN_f.Gibbs(**GibbsOpts)],
#                    Ref=RefCN100_e_CHx_2,
#                    Name='CN/R10-N: CH2.hN + H.hC -> CH3.bN',
#                    Hover=HoverList, Color="r", **Main_Line_Props)

# ---- CH3 -> CH4
# ramificación  secundaria (continuación)

# Jump C/ R10 -> R11C (rota CH3)
stego.Plot.RxStep([CN10R10tCbC_f.Gibbs(**GibbsOpts) + .5 * H2.Gibbs(**GibbsOpts_H2),
                  CN10R11C_i.Gibbs(**GibbsOpts)],
                 Ref=RefCN100_e_CHx,
                 Name='{CH3.bC}+(1/2)H2->{CH3.bN(rot)+H.hN}',
                 Hover=HoverList, Color=ColorCN, **Jump_Line_Props)

# CN10/R11C: CH3btN + Hh -> CH4.g
stego.Plot.RxStepTS([CN10R11C_i.Gibbs(**GibbsOpts), CN10R11C_TS.Gibbs(**GibbsOpts), CN10R11C_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN100_e_CHx,
                   Name='CN/R11C: CH3bC + H.h -> CH4.g',
                   Hover=HoverList, Color=ColorCN, **Main_Line_Props)



# ---- CH3 -> CH4
# rama principal

# # Jump N/ R10 -> R11N (mantiene CH3)
# stego.Plot.RxStep([CN10R10tCbC_f.Gibbs(**GibbsOpts) + .5 * H2.Gibbs(**GibbsOpts_H2),
#                   CN10R11N_i.Gibbs(**GibbsOpts)],
#                  Ref=RefCN100_e_CHx,
#                  Name='CN/{CH3.bC}+(1/2)H2->{CH3.bC+h.hN}',
#                  Hover=HoverList, Color="m", **Jump_Line_Props)
#
# # CN10/R11N: CH3btC + H.h -> CH4.g
# stego.Plot.RxStepTS([CN10R11N_i.Gibbs(**GibbsOpts), CN10R11N_TS.Gibbs(**GibbsOpts), CN10R11N_f.Gibbs(**GibbsOpts)],
#                    Ref=RefCN100_e_CHx,
#                    Name='CN/R11N: CH3bC + H.h -> CH4.g',
#                    Hover=HoverList, Color="m", **Main_Line_Props)





# ---- Physisorption
stego.Plot.RxStep([CN10R11N_f.Gibbs(**GibbsOpts), CN100.Gibbs(**GibbsOpts) + CH4_g.Gibbs(**GibbsOpts)],
                 Ref=RefCN100_e_CHx,
                 Name='CN/{}CH4.gf->{}+CH4',
                 Hover=HoverList, Color=ColorCN, **{**Main_Line_Props, 'StepSpan':.4})


# Section
SectionRefs_CN100e.UpdateFromTail(RefCN100_e_CHx)
# stego.Plot.AnnotateStepAxis(['$CH_{x}$', '$CH_{4(g)}$'], Ref=SectionRefs_CN100e, Colour="k")
stego.Plot.Align_Rx_Ticks(SectionRefs_CN100e, TSmode=False)

# # ---- Physisorption
# stego.Plot.RxStep([CN10R11C_f.Gibbs(**GibbsOpts), CN100.Gibbs(**GibbsOpts) + CH4_g.Gibbs(**GibbsOpts)], Ref=RefCN100_e_tail2,
#                Name='CN/{}CH4.gf->{}+CH4', Hover=HoverList, StepSpan=.4, Color='b', **LineProps)

# Check full plot
# if ShowGlobal_e:
#     RefCN_e_full = RefCN100_e.branch(Step=0)
#     stego.Plot.RxStep([CN100_ChN.Gibbs(**GibbsOpts) + 2 * H2.Gibbs(**GibbsOpts_H2),
#                       CN100.Gibbs(**GibbsOpts) + CH4_g.Gibbs(**GibbsOpts)],
#                      Ref=RefCN_e_full, Name="CN10/{C.hN}+2*H2 -> {}+CH4",
#                      Hover=HoverList, Color="lime", StepSpan=4.4, **LineProps)
#     RefCN_e_full.PlotExtend(Until=11., Color="lime", **LineProps)

# ------------------------------------------------------------------------------------------------ Ending subplot
# Ajustes finales de plots

stego.Plot.ActivateHover(HoverList, fig)
Ley = [Line2D([0], [0], color="k", linewidth=3, linestyle='-', alpha=0.8),
       Line2D([0], [0], color="r", linewidth=3, linestyle='-', alpha=0.8)]

# Lado izquierdo
for xax in axs:
    plt.axes(xax[0])
    plt.ylabel("Gibbs free energy (kJ/mol)")
    plt.tick_params(axis="y", direction="in")

plt.ylim([-105, 170])

# centro y derecho
for iax in [axs[i][j] for i in range(0,2) for j in range(1,3)]:
    plt.axes(iax)
    plt.tick_params(axis="y", direction="inout", length=12.)

# all plots
for iax in [axs[i][j] for i in range(0,2) for j in range(0,3)]:
    plt.axes(iax)
    plt.axhline(y=0., color="k", alpha=.5, linewidth=.4)
    plt.grid(which='major', color='k', linewidth=.5, alpha=.3)
    # iax.set_xticklabels([])
    # plt.legend(Ley, ["(111)", "(100)"], prop={'size': 8}, loc='upper right')

for xax, geom in zip(axs,['(111)','(100)']):
    for iax, type in zip(xax, ['Co','NiCo','Ni']):
        plt.axes(iax)
        plt.annotate(type+geom,
                     xy=[.05, .95], xytext=[0, 0],
                     xycoords='axes fraction', textcoords='offset points',
                     ha='left', va='top', size=12, color='k', fontweight='bold',
                     bbox=dict(facecolor='white', edgecolor='white', pad=2.0))


plt.savefig("./Current_test.png", dpi=180)
plt.show()
