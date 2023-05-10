#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from Databin import *
import stego.Plot, stego.promps


########################################################################################################################
########################################################################################################################
# Creating Plot, CHx series ############################################################################################
########################################################################################################################

stego.promps.MayorSection('Creating Plot')

fig, axs = plt.subplots(1, 1, figsize=(6, 5.), dpi=90, sharey='row', sharex='all')
plt.subplots_adjust(wspace=.0, hspace=0., left=.14, right=.98, bottom=.4, top=.94)
HoverList = []

# References
RefCN111_e = stego.Plot.RxRef(1.5, 0.)

# Place holders
HoverList = []
SectionRefs_CN111e = RefCN111_e.branch()




# Start branches
refStart_HCO = 5.5
refStart_COH = 9.5

# Color ref: https://gist.github.com/thriveth/8560036

# Default parameters
Main_Line_Props = {"StepSpan": .5, "LineStyle": "solid", "LineWidth": 1.5, "AlphaLines": 1., 'T-rate':265 + 273.15}
Main_Line_Props_Co = {"StepSpan": 1., "LineStyle": "solid", "LineWidth": 1.5, "AlphaLines": 1.}
Jump_Line_Props = {"StepSpan": .2, "LineStyle": "solid", "LineWidth": .8, "AlphaLines": 1.}
OH_Line_Props = {"StepSpan": .2, "LineStyle": 'solid', "LineWidth": 2, "AlphaLines": .2}

GibbsOpts = {'T': 265 + 273.15, 'P': 0.01 * 1.}  # 1% CH4
GibbsOpts_H2 = {'T': 265 + 273.15, 'P': 0.25 * 1.}  # 25% H2

########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################


# ----------------------------------------------------------------------------------------------------------------------
# Cobalt-Nickel --------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
stego.promps.MinorSection('Adding steps to Plot: Gibbs - CoNi(111s)')



# ..............................................................................
# CO series ....................................................................
# ..............................................................................
RefCN111_e_CO = RefCN111_e.branch()

# CO adsorption
stego.Plot.RxStep([CN111s.Gibbs(**GibbsOpts)+COg.Gibbs(**GibbsOpts),
                  CN1sR17bCN_i.Gibbs(**GibbsOpts)],
                 Ref=RefCN111_e_CO,
                 Name='CO adsorption',
                 Hover=HoverList, Color='k', **Jump_Line_Props)

# CN/R17bCN CO.tC -> C.hN + O.hN
stego.Plot.RxStepTS([CN1sR17bCN_i.Gibbs(**GibbsOpts),
                    CN1sR17bCN_d.Gibbs(**GibbsOpts),
                    CN1sR17bCN_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN111_e_CO,
                   Name="CN/R17bCN CO.tC -> C.hN + O.hN",
                   Hover=HoverList, Color='r', **Main_Line_Props)

# Separate/ {C.hN+O.hN} + (H2) + {} -> {C.hN (C) } + {O.hN+H.hN}
stego.Plot.RxStep([CN1sR17bCN_f.Gibbs(**GibbsOpts) + H2.Gibbs(**GibbsOpts_H2) + CN111s.Gibbs(**GibbsOpts),
                  CN1sR21C_i.Gibbs(**GibbsOpts) + CN1sR132C_i.Gibbs(**GibbsOpts)],
                 Ref=RefCN111_e_CO,
                 Name="CN/ {C.hN+O.hN} + (H2) -> {(C)C.hN+H.hN} + {(C)O.hN+H.hN}",
                 Hover=HoverList, Color='r', **Jump_Line_Props)

# OH elimination (C)
stego.Plot.RxStepTS([CN1sR132C_i.Gibbs(**GibbsOpts),
                    CN1sR132C_d.Gibbs(**GibbsOpts),
                    CN1sR132C_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN111_e_CO,
                   Name="CN1s/R13.2C-i O.fN+H.hN -(C)-> OH.fN",
                   Hover=HoverList, Color='b', **OH_Line_Props)

# R21 - C : C.hN + H.fN -> CH.hN
stego.Plot.RxStepTS([CN1sR21C_i.Gibbs(**GibbsOpts),
                    CN1sR21C_TS.Gibbs(**GibbsOpts),
                    CN1sR21C_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN111_e_CO,
                   Name='CN1s/R21 on top C: C.hN+H.fN->CH.hN',
                   Hover=HoverList, Color="k", **Main_Line_Props)



# ..............................................................................
# HCO series ...................................................................
# ..............................................................................
RefCN111_e_HCOt = RefCN111_e.branch()
RefCN111_e_HCOt.PlotExtend(Until=refStart_HCO, Color='k', Alpha=1, LineWidth=.8)


# Separe CN/ {CO.tC + O.hC} + H2 + {} -> {CO.hN + H.fN}+{(R13.2C) O.fN+H.hN}
stego.Plot.RxStep([CN111s.Gibbs(**GibbsOpts) + 0.5*H2.Gibbs(**GibbsOpts_H2)+COg.Gibbs(**GibbsOpts),
                  CN1sR5bt_i.Gibbs(**GibbsOpts)],
                 Ref=RefCN111_e_HCOt,
                 Name="CN/ {CO.tC} + 1/2(H2) -> {(R5bt) CO.hN + H.fN}",
                 Hover=HoverList, Color="g", **Jump_Line_Props)

# CN/R5bt CO.hN + H.fN -> HCO.tCtC
stego.Plot.RxStepTS([CN1sR5bt_i.Gibbs(**GibbsOpts),
                    CN1sR5bt_d.Gibbs(**GibbsOpts),
                    CN1sR5bt_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN111_e_HCOt,
                   Name="CN/R5 CO.hN + H.fN -> HCO.tCtC",
                   Hover=HoverList, Color="g", **Main_Line_Props)

# CN/R15 HCO.tCtC -> CH.fC + O.fN
stego.Plot.RxStepTS([CN1sR15tCtC_i.Gibbs(**GibbsOpts),
                    CN1sR15tCtC_d.Gibbs(**GibbsOpts),
                    CN1sR15tCtC_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN111_e_HCOt,
                   Name="CN/R15 HCO.tCtC -> CH.fC + O.fN",
                   Hover=HoverList, Color="g", **Main_Line_Props)



# Separe CN/{CH.fC + O.fN} + 1/2(H2) + {} -> {(R21)CH.hN}  + {(R13.2C) O.fN+H.hN}
stego.Plot.RxStep([CN1sR15tCtC_f.Gibbs(**GibbsOpts) + 0.5*H2.Gibbs(**GibbsOpts_H2) + CN111s.Gibbs(**GibbsOpts),
                  CN1sR21C_f.Gibbs(**GibbsOpts) + CN1sR132C_i.Gibbs(**GibbsOpts)],
                 Ref=RefCN111_e_HCOt,
                 Name="CN/{CH.fC + O.fN} + {H.hN} -> {(R21)CH.hN}  + {(R13.2C) O.fN+H.hN}",
                 Hover=HoverList, Color="g", **Jump_Line_Props)

# OH elimination (C)
stego.Plot.RxStepTS([CN1sR132C_i.Gibbs(**GibbsOpts),
                    CN1sR132C_d.Gibbs(**GibbsOpts),
                    CN1sR132C_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN111_e_HCOt,
                   Name="CN1s/R13.2C-i O.fN+H.hN -(C)-> OH.fN",
                   Hover=HoverList, Color='b', **OH_Line_Props)





# .....................................
# COH series ..........................
# .....................................
RefCN111_e_COH = RefCN111_e.branch()
RefCN111_e_COH.PlotExtend(Until=refStart_COH, Color='k', Alpha=1, LineWidth=.8)
SectionRefs_CN111e.UpdateFromTail(RefCN111_e_COH)

# Separe CN/{(R23-f)CO.tC + O.hC}+ H2 + {} -> {(R6)CO.hN + H.fN}+{(R13.2C)O.fN+H.hN}
stego.Plot.RxStep([CN111s.Gibbs(**GibbsOpts) + 0.5*H2.Gibbs(**GibbsOpts_H2)+COg.Gibbs(**GibbsOpts),
                  CN1sR6_i.Gibbs(**GibbsOpts)],
                 Ref=RefCN111_e_COH,
                 Name="CN/{(R23-f) CO.tC} + 1/2(H2) -> {(R6)CO.hN + H.fN}",
                 Hover=HoverList, Color='m', **Jump_Line_Props)

# CN/R6C CO.hN + H.fN -(C)-> COH.hN
stego.Plot.RxStepTS([CN1sR6_i.Gibbs(**GibbsOpts),
                    CN1sR6_d.Gibbs(**GibbsOpts),
                    CN1sR6_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN111_e_COH,
                   Name="CN/R6C CO.hN + H.fN -(C)-> COH.hN",
                   Hover=HoverList, Color="m", **Main_Line_Props)

# CN/R16C COH.hNtC -> C.hN + OH.fN
stego.Plot.RxStepTS([CN1sR16C_i.Gibbs(**GibbsOpts),
                    CN1sR16C_d.Gibbs(**GibbsOpts),
                    CN1sR16C_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN111_e_COH,
                   Name="CN/R16C COH.hNtC -> C.hN + OH.fN",
                   Hover=HoverList, Color="m", **Main_Line_Props)

# Separa CN/{(R16C-f)C.hN+OH.fN}+ 1/2(H2) + {} -> {(R21C) C.hN+H.fN} + {(R13.2C-f) OH.fN}
stego.Plot.RxStep([CN1sR16C_f.Gibbs(**GibbsOpts) + 0.5*H2.Gibbs(**GibbsOpts_H2) + CN111s.Gibbs(**GibbsOpts),
                  CN1sR21C_i.Gibbs(**GibbsOpts) + CN1sR132C_f.Gibbs(**GibbsOpts)],
                 Ref=RefCN111_e_COH,
                 Name="CN/{(R16C-f)C.hN+OH.fN}+1/2(H2)+{}->{(R21C)C.hN+H.fN}+{(R13.2C-f)OH.fN}",
                 Hover=HoverList, Color="m", **Jump_Line_Props)

# R21 - C : C.hN + H.fN -> CH.hN
stego.Plot.RxStepTS([CN1sR21C_i.Gibbs(**GibbsOpts),
                    CN1sR21C_TS.Gibbs(**GibbsOpts),
                    CN1sR21C_f.Gibbs(**GibbsOpts)],
                   Ref=RefCN111_e_COH,
                   Name='CN1s/R21 on top C: C.hN+H.fN->CH.hN',
                   Hover=HoverList, Color="k", **Main_Line_Props)

testRxstep = Model.reactionstep(CN1sR21C_i, CN1sR21C_TS, CN1sR21C_f)

stego.Plot.RxStepTS(testRxstep,
                   Ref=RefCN111_e_COH,
                   Name='CN1s/R21 on top C: C.hN+H.fN->CH.hN',
                   Hover=HoverList, Color="k", **Main_Line_Props)







stego.Plot.Align_Rx_Ticks(SectionRefs_CN111e, TSmode=False)

#-----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------ Ending subplot
#-----------------------------------------------------------------------------------------------------------------------

# Ajustes finales de plots

stego.Plot.ActivateHover(HoverList, fig)
Ley = [Line2D([0], [0], color="k", linewidth=3, linestyle='-', alpha=0.8),
       Line2D([0], [0], color="r", linewidth=3, linestyle='-', alpha=0.8)]

plt.xlim([0, 14])
plt.ylim([-49, 280])

# Lado izquierdo
plt.ylabel("Gibbs free energy (kJ/mol)", fontweight='bold', fontsize='12')
plt.tick_params(axis="y", direction="in")

# centro y derecho
plt.tick_params(axis="y", direction="inout", length=12.)

# all plots
plt.axhline(y=0., color="k", alpha=.5, linewidth=.4)
plt.grid(which='major', color='k', linewidth=.5, alpha=.3)
axs.set_xticklabels([])


# -
# legendas de titulo
labelname = iter(('NiCo(111)','Ni(111)',
                  'Co(100)','NiCo(100)','Ni(100)'))

plt.annotate(next(  labelname),
             xy=[.5, .95], xytext=[0, 0],
             xycoords='axes fraction', textcoords='offset points',
             ha='center', va='top', size=12, color='k', fontweight='bold',
             bbox=dict(facecolor='white', edgecolor='white', pad=2.0))





plt.savefig("./Profile_CO_Gibbs_NiCo111_extended_raw.png", dpi=180)
plt.show()
