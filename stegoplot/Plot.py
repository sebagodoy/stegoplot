# Packages

import matplotlib.pyplot as plt
import stegoplot.item_types
from .promps import CodeStatus, fStringLength, fNum
from .parameters import eV2J, eV2kJpmol

import stegoplot.parameters

print('>> Loading Plot tools', end='...')


########################################################################################################################
################ Reference Object

class RxRef:
    # Reference objects to construct reaction plots
    def __init__(self, Pos0=0, En0=0., **kwargs):
        self.RootE = En0
        self.RootX = Pos0
        self.log = [(Pos0, En0)]
        self.TailE = En0
        self.TailX = Pos0
        self.Tail = (En0, Pos0)
        # default things
        self.FlatWidth = .4
        self.Color = kwargs.get('Color', 'k')
        self.LineStyle = kwargs.get('LineStyle', 'solid')
        self.LineWidth = kwargs.get('LineWidth', 1.5)
        self.AlphaLines = kwargs.get('AlphaLines', .3)

    # Utility functions
    def __str__(self):
        return f'Reference obj from {self.log[-1]} to {self.Tail}'

    def Tail(self):
        return self.log[-1]

    def TailX(self):
        return self.Tail()[0]

    def TailE(self):
        return self.Tail()[1]

    def Root(self):
        return self.log[0]

    def RootX(self):
        return self.Root()[0]

    def RootE(self):
        return self.Root()[1]

    # Creation and manipulation functions
    def branch(self, **kwargs):
        # Create new object from base reference
        # Create new branch
        NewBranch = RxRef(Branched=True)
        # Tail info until step
        EndStep = kwargs.get('Step', len(self.log))
        print('End step = ' + str(EndStep))
        NewBranch.log = [self.log[i] for i in range(0, int(EndStep))]

        CodeStatus('Reference branched from previous')

        return NewBranch

    def Update(self, NewX, NewE, **kwargs):
        self.TailE = NewE
        self.TailX = NewX
        self.Tail = (NewX, NewE)

        if not kwargs.get('Props', None):
            self.log = [i for i in self.log] + [(NewX, NewE, kwargs.get('Props'))]
        else:
            self.log = [i for i in self.log] + [(NewX, NewE)]

    def UpdateFromTail(self, Ref):
        if isinstance(Ref, RxRef):
            self.Update(Ref.TailX, Ref.TailE)
        else:
            CodeStatus('Error trying to update reference object from other reference object')

    def PlotExtend(self, SpanX=1, **kwargs):
        # Defaults for plot
        iColor = kwargs.get('Color', self.Color)
        iLineStyle = kwargs.get('LineStyle', self.LineStyle)
        iLineWidth = kwargs.get('LineWidth', self.LineWidth)
        iAlpha = kwargs.get('Alpha', self.AlphaLines)

        if 'Until' in kwargs:
            if kwargs.get('Until') >= self.TailX:
                SpanX = kwargs.get('Until') - self.TailX

        # Plot
        plt.plot([self.TailX, self.TailX + SpanX], [self.TailE, self.TailE],
                 color=iColor, linestyle=iLineStyle, alpha=iAlpha,
                 linewidth=iLineWidth, zorder=1.)

        # Update
        self.Update(self.TailX + SpanX, self.TailE)

    # def PlotConect(self, SpanX=1, **kwargs):
    #     # Defaults for plot
    #     iColor = kwargs.get('Color', self.Color)
    #     iLineStyle = kwargs.get('LineStyle', self.LineStyle)
    #     iLineWidth = kwargs.get('LineWidth', self.LineWidth)
    #     iAlpha = kwargs.get('Alpha', self.AlphaLines)
    #
    #     if 'Until' in kwargs:
    #         if kwargs.get('Until') >= self.TailX:
    #             SpanX = kwargs.get('Until') - self.TailX
    #
    #     # Plot
    #     plt.plot([self.TailX, self.TailX + SpanX], [self.TailE, self.TailE],
    #              color=iColor, linestyle=iLineStyle, alpha=iAlpha,
    #              linewidth=iLineWidth, zorder=1.)
    #
    #     # Update
    #     self.Update(self.TailX + SpanX, self.TailE)


################################################################################################################################
################ Quick add note
def QuickNote(iStr: "Note, str",
              ixy: "[float , float] position data",
              Color='k',
              **kwargs):
    # Default parameters
    ixytext = kwargs.get('ixytext', [.5, .5])
    iha = 'center'
    iva = 'center'

    # Location options
    Loc = kwargs.get('Loc', 'top-left')
    if Loc == 'top-center':
        ixytext = [.5, .95]
        iva = 'top'
        iha = 'center'
    elif Loc == 'bottom-center':
        ixytext = [.5, .05]
        iva = 'bottom'
        iha = 'center'
    elif Loc == 'top-left':
        ixytext = [.95, .95]
        iva = 'top'
        iha = 'right'
    elif Loc == 'bottom-center':
        ixytext = [.5, .05]
        iva = 'bottom'
        iha = 'center'
    elif Loc == 'top-right':
        ixytext = [.95, .95]
        iva = 'top'
        iha = 'right'
    elif Loc == "out-left-top":
        ixytext = [1.02, .95]
        iva = 'top'
        iha = 'left'
    elif Loc == "out-left-bottom":
        ixytext = [1.01, .05]
        iva = 'bottom'
        iha = 'left'
    elif Loc == "out-left-center":
        ixytext = [1.01, .5]
        iva = 'center'
        iha = 'left'

    ThisNote = plt.gca().annotate(iStr, xy=ixy,
                                  xytext=ixytext, ha=iha, va=iva,
                                  xycoords='data',
                                  textcoords='axes fraction',
                                  size=kwargs.get('Size', 12), color='k',
                                  bbox=dict(boxstyle='round', facecolor='darkgray', edgecolor=Color, alpha=.8),
                                  arrowprops=dict(arrowstyle='->', color=Color, alpha=0.5), zorder=100
                                  )
    return ThisNote


########################################################################################################################
################ Hover annotation functions

def AddHoverNote(iHoverList : 'list, hover notes container',
                 iStr : 'text in note',
                 ixy : '[x, y], position',
                 Color='k', **kwargs):
    iColor = Color
    # Create pointer
    ThisPoint = plt.gca().scatter(ixy[0], ixy[1], color=Color, alpha=0.)
    # Create Note
    ThisNote = QuickNote(iStr, ixy, Color=iColor, **kwargs)
    # Occult Note
    ThisNote.set_visible(False)

    # almacenate
    iHoverList.append((ThisPoint, ThisNote))


def ActivateHover(iHoverList: list = None,
                  Figure: "figure handler" = False):
    # Prepare containers
    # if no container list of notes is given uses default in stegoplot.parameters
    # if no figure is specified, takes current figure
    if not Figure:
        Figure = plt.gcf()
    if iHoverList == None:
        iHoverList = stegoplot.parameters.def_HoverNoteBin
    # define event
    def hover(event):
        cont = False
        ind = 0
        if event.inaxes:
            for iSc in range(len(iHoverList)):
                if iHoverList[iSc][0].contains(event)[0]:
                    cont = True
                    ind = iSc
                    break
                else:
                    cont = False
                    ind = 0
            if cont:
                iHoverList[ind][1].set_visible(True)
                Figure.canvas.draw_idle()
            else:
                for iSc in iHoverList:
                    iSc[1].set_visible(False)
                    Figure.canvas.draw_idle()
    # Execute
    Figure.canvas.mpl_connect('motion_notify_event', hover)


################################################################################################################################
#### Add step to plot
def RxStepTS(En, Ref=0.,
             UpdateRef = True, Hover = False,
             PlotShape ='Stepped', StepSpan=1.,
             Name = 'No name given',
             **kwargs):

    # Reference (get Etail, Xtail)
    if isinstance(Ref, RxRef):
        Etail = Ref.TailE
        Xtail = Ref.TailX
        FlatWidth = min(Ref.FlatWidth, StepSpan * 2 / 4)
        iColor = Ref.Color

    # ---------------------------------------------------------------------------

    # Get Step only info
    FlatWidth = min(kwargs.get('FlatWidth', .4), StepSpan * 2 / 4)
    UnitsFactor = float(kwargs.get('UnitsFactor', eV2kJpmol))  # unit converter, def= input eV -> plot output kJ/mol

    # Color and style in plot
    iColor = kwargs.get('Color', 'k')
    iLineStyle = kwargs.get('LineStyle', 'solid')
    iLineWidth = kwargs.get('LineWidth', 1.5)
    iAlphaLines = kwargs.get('AlphaLines', .3)
    iHoverLocation = kwargs.get("HoverLocation", "top-center")

    # -----------------------------------------------------------------------------
    # ---- Pre-treating Energy input
    # Energy input can be [ A , B ] or [A, B, C]; A,B,C float or SingleItem clases
    # with built in energy functions
    for iE, EE in enumerate(En):
        if isinstance(EE, float) or isinstance(EE, int):
            # Case: Element already is number, kept it like that
            En[iE] = float(EE)

        elif isinstance(EE, list):
            # Case: Element is list [E1, E2, E3, ...], every item needs to be analyzed
            tempE = 0.
            for iEE in EE:
                if isinstance(iEE, float) or isinstance(iEE, int):
                    # SubCase: Element already is number, add it like that
                    tempE += float(iEE)
                elif isinstance(iEE, tuple) and len(iEE) == 2:
                    # SubCase: Element is tuple (X, SingleItem), treated as SingleItem with multiplier X
                    tempE += iEE[0] * iEE[1].GetThermo(
                        ThermoType=kwargs.get('ThermoType', stegoplot.parameters.def_PlotType),
                        T=kwargs.get('T', None),
                        P=kwargs.get('P', None),
                        Report=True)
                else:
                    # SubCase: Element is of the  SingleItem class derivatives (GasItem, ...)
                    tempE += iEE.GetThermo(
                        ThermoType=kwargs.get('ThermoType', stegoplot.parameters.def_PlotType),
                        T=kwargs.get('T', None),
                        P=kwargs.get('P', None),
                        Report=False)
            En[iE] = tempE
        elif isinstance(EE, tuple) and len(EE) == 2:
            # Case: Element is ( X, SingleItem class), treated as Single Item with multiplier X.
            En[iE] = EE[0] * EE[1].GetThermo(ThermoType=kwargs.get('ThermoType', stegoplot.parameters.def_PlotType),
                                             T=kwargs.get('T', None),
                                             P=kwargs.get('P', None),
                                             Report=False)
        else:
            # Case: Element is of the  SingleItem class derivatives (GasItem, ...)
            # with built in functions
            En[iE] = EE.GetThermo(ThermoType=kwargs.get('ThermoType', stegoplot.parameters.def_PlotType),
                                  T=kwargs.get('T', None),
                                  P=kwargs.get('P', None),
                                  Report=True)

    # ---------------------------------------------------------------------------
    # Scale input (eV) to kwargs.UnitsFactor, by default in eV->kJ/mol
    for i in range(len(En)):
        En[i] *= UnitsFactor

    # ---- Energy deltas
    DE = En[1] - En[0]  # reaction energy
    if len(En) == 3:
        Eaf = En[1] - En[0]  # activation forward
        Eab = En[1] - En[2]  # activation backwards


    # Direction of the reference
    if kwargs.get('RefDir', 'F')[0] == 'B':
        iRxDir = -1
        ERef = En[2] - Etail
    else:
        iRxDir = 1
        ERef = En[0] - Etail

    # Positions [ini->TS->fin] or [ini -> fin]
    Pos = [Xtail + i * StepSpan * iRxDir for i in range(len(En))]

    # ---------------------------------------------------------------------------
    # Preparing plot numbers
    RxLinesProps = {'color': iColor, 'linestyle': iLineStyle, 'alpha': iAlphaLines,
                    'linewidth': iLineWidth, 'zorder': 5.}

    # Plotting
    if PlotShape == 'Stepped':
        # Step with TS
        if len(En) == 3:
            x_stepline = [Pos[0], Pos[0] + FlatWidth / 2.,
                          Pos[1] - FlatWidth / 2., Pos[1] + FlatWidth / 2.,
                          Pos[2] - FlatWidth / 2., Pos[2]]
            y_stepline = [En[0] - ERef, En[0] - ERef,
                          En[1] - ERef, En[1] - ERef,
                          En[2] - ERef, En[2] - ERef]
        # Step without TS
        elif len(En) == 2:
            x_stepline = [Pos[0], Pos[0] + FlatWidth / 2.,
                          Pos[-1] - FlatWidth / 2., Pos[-1]]
            y_stepline = [En[0] - ERef, En[0] - ERef,
                          En[-1] - ERef, En[-1] - ERef]
        # Plotting
        plt.plot(x_stepline, y_stepline, **RxLinesProps)

    elif PlotShape == 'Spline':
        # same for len(En) == 2 or 3
        from numpy import linspace
        from scipy.interpolate import BPoly
        bpoly = BPoly.from_derivatives(Pos, [[i-ERef,0] for i in En])
        x_spline = linspace(Pos[0], Pos[-1], 25)
        y_spline = bpoly(x_spline)
        plt.plot(x_spline, y_spline, **RxLinesProps)

    # Promp
    CodeStatus(fStringLength('Adding reaction step to current plot', Side='r', l=90, Filling='.'),
               end=' ' + Name + '\n')
    if len(En) == 3:
        CodeStatus('Ea(f)=' + fNum(Eaf, '2f') + ' ; Ea(b)=' + fNum(Eab, '2f') + ' ; Delta E = ' + fNum(DE, '2f'),l=8)
    elif len(En) == 2:
        CodeStatus('Delta E = ' + fNum(DE, '2f'), l=8)


    #### ---------------------------------------------------------------------------------------------------------------
    #### Hover Note Option
    if Hover:
        # Add note to collection given (list)
        # or default list (stegoplot.parameters.def_HoverNoteBin)
        if not isinstance(Hover, list):
            Hover = stegoplot.parameters.def_HoverNoteBin

        # ---- Ending Note
        xy_point_position = [Pos[-1], En[-1] - ERef]
        strNote = Name + ' -end\n' + r'$x=$' + fNum(Pos[-1], '2f') + '\n' + \
                  r'$E_f(-ref)=$' + fNum(En[-1] - ERef, '2f') + ' kJ/mol'
        # Create note
        AddHoverNote(Hover, strNote, xy_point_position,
                     Size=kwargs.get('NoteSize', 9),
                     Color=iColor,
                     Loc=iHoverLocation)

        # ---- Middle Note - TS
        if len(En) == 3:
            xy_point_position = [Pos[1], En[1] - ERef]
            strNote = Name + '\n' + \
                      r'$\Delta E_{rx}=$' + fNum(DE, '2f') + ' , ' + \
                      r'$E_a=$' + fNum(Eaf, '2f') + '(' + fNum(Eab, '2f') + ') ' + 'kJ/mol\n'\
                      r'$E_{a}(-ref)=$' + fNum(En[1] - ERef,'2f') + ' /kJ/mol'
        # ---- Middle Note - No TS
        elif len(En) == 2:
            xy_point_position = [(Pos[1]+Pos[0])/2, (En[1] + En[0])/2 - ERef]
            strNote = Name + '\n' + \
                      r'$\Delta E_{rx}=$' + fNum(DE, '2f') + ' /kJ/mol'
        # Create Note
        AddHoverNote(Hover, strNote, xy_point_position,
                     Size=kwargs.get('NoteSize', 9),
                     Color=iColor,
                     Loc=iHoverLocation)






    #### Update references
    if UpdateRef:
        if iRxDir == 1:
            if isinstance(Ref, RxRef):
                Ref.Update(Pos[-1], En[-1] - ERef)
            elif isinstance(Ref, list) and isinstance(Ref[-1], tuple):
                Ref.append((Pos[-1], En[-1] - ERef))
            # CodeStatus('Reference updated forward', l=8)
        elif iRxDir == -1:
            if isinstance(Ref, RxRef):
                Ref.Update(Pos[0], En[0] - ERef)
            elif isinstance(Ref, list) and isinstance(Ref[-1], tuple):
                Ref.append((Pos[0], En[0] - ERef))
            # CodeStatus('Reference updated backwards', l=8)
    else:
        if isinstance(Ref, RxRef):
            Ref.Update(Ref.TailX, Ref.TailE)
        else:
            Ref.append(Ref[-1])
        CodeStatus('Reference NOT updated', l=8)





def AnnotateStepAxis(Names, Ref, **kwargs):
    ### kwargs				Size = text size
    #						Colour = text colour
    #						Level = text level from bottom

    # Checks
    if not isinstance(Names, list): quit('>>>> Names option has to be a list, bye!')
    if not isinstance(Ref, RxRef) and not isinstance(Ref[-1], tuple):
        quit('>>>> Names option has to be a RxRef object or list of tuples, bye!')

    # Reference - last one
    iSpanLog = 2
    if isinstance(Ref, RxRef):
        Xtail = Ref.TailX
        # Get span
        if len(Ref.log) > 1:
            iSpanLog = Ref.TailX - Ref.log[-2][0]

    elif isinstance(Ref, list) and isinstance(Ref[-1], tuple):
        Xtail = Ref[-1][0]

    # Parameters
    iSize = kwargs.get('Size', 8)
    iColour = kwargs.get('Colour', 'k')
    iSpan = float(kwargs.get('StepSpan', iSpanLog))
    iLevel = '\n' * (kwargs.get('Level', 1) - 1)
    Loc = kwargs.get('Loc', 'bottom')
    Hhandler = kwargs.get('H_Handler', 'center')

    # Positions
    if kwargs.get('RefDir', 'Forw')[0] == 'B':
        Pos = [Xtail + i for i in range(3)]
    else:
        Pos = [Xtail - i * iSpan / 2 for i in range(3)]
        Pos.sort()

    # String construction
    iStr = ''
    if len(Names) == 1:
        iStr = r'$\rightarrow$' + Names[0]
    if len(Names) > 1:
        iStr = Names[0]
        for iNm in Names[1:]:
            iStr += r'$\rightarrow$' + iNm

    # Position
    if Loc == 'bottom':
        plt.annotate(iLevel + iStr,
                     xy=[(Pos[0] + Pos[-1]) / 2., 0.], xytext=[0, -5],
                     xycoords=('data', 'axes fraction'), textcoords='offset points',
                     ha=Hhandler, va='top', size=iSize, color=iColour)
    elif Loc == 'top':
        plt.annotate(iStr + iLevel,
                     xy=[(Pos[0] + Pos[-1]) / 2., 1.], xytext=[0, 5],
                     xycoords=('data', 'axes fraction'), textcoords='offset points',
                     ha=Hhandler, va='bottom', size=iSize, color=iColour)


print('Ok')
