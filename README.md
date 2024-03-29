
![made](https://img.shields.io/badge/python-3.8-green?logo=python&logoColor=green&style=flat)
![license](https://img.shields.io/github/license/sebagodoy/stegoplot)
![repo size](https://img.shields.io/github/repo-size/sebagodoy/stegoplot)
![last commit](https://img.shields.io/github/last-commit/sebagodoy/stegoplot)
![jup example](https://img.shields.io/github/directory-file-count/sebagodoy/stegoplot/test?extension=ipynb&label=jupyter%20examples&type=file)

# Stego(reaction) plot, a DFT analysis tool

A python package that helps with organizing and analyzing DFT results, computing thermodynamic properties, 
analyzing DOS and more things to come.


#### Requirements
* Python 3.6 or later
* NumPy
* matplotlib
* scipy (optional, for curvy reaction profiles)

## Installation
Install the Numpy and matplotlib if you dont have these already. Install the distribution uploaded to TestPy with 
```
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps stegoplot
```
#### Installation in virtual environment
While testing, is recomended to install stego in a separate virtual environment, so it does not
interfere with anything else. Following [this](https://packaging.python.org/en/latest/tutorials/packaging-projects/), 
[this](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-and-using-virtual-environments) and [this]() guides (in Ubuntu 20.04 with python3 and pip):
```
# select a location, open a terminal there, 
# create a folder for the virtual environment and move in
mkdir sandbox
cd sandbox 

# create virtual environment
python3 -m venv ./
source ./bin/activate

# install stego and other packages
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps stegoplot
pip install numpy
pip install matplotlib
```
or use `pip3` is needed for you will be using `python3`. If you want to plot smooth reaction profiles be sure to also install the `scipy` package 
with `pip3 install scipy`.

While in this virtual environment, python3 can import stegoplot, numpy and matplotlib, give it a 
test entering with `python3` and checking the value of the Boltzmann constant (in m2 kg / s2 K) 
with `import stegoplot.parameters as stg; stg.kb` (spoiler: 1.3806488e-23).
To use jupyter notebooks with this virtual environment you need to create and add a new kernel using:
```
# create and add kernel for jupyter notebooks
pip install ipykernel
python -m ipykernel install --user --name=sandbox

```
now you can call `jupyter notebook` from any terminal and select the `kernel > sandbox` to use
stego and check the test examples included in the test folder.

## Basic examples 
#### 1. Properties for some species
Loading and adding a molecule
```
import stegoplot.item_types as stg
H2O = stg.Gas(Name='H2O',
              G_ID='ads', E0=-14.14745554,
              F_ID='McQuarrie', FreqR=[3833.413608, 3721.047191, 1597.447164],
              Geometry='Poliatomic', Mass=18.00,
              RotT=[40.1, 20.9, 13.4], RotSymNum=2)
```
Computing some properties
```
H2O.E0                        # electronic energy
H2O.ZPVE                      # Zero Point Vibrational Energy
H2O.E0ZPVE()                  # electronic energy + ZPVE
H2O.Enthalpy(T=298.15, P=1)   # enthalpy
H2O.Entrop(T=298.15, P=1)     # entropy
H2O.Gibbs(T=298.15, P=1)      # Gibbs free energy
```
#### 2. Basic plot
Let's plot CO(g) + * -> *CO, *CO + * -> *C + *O. Start by adding the species
```
# load species
import stegoplot.item_types as Model

# CO in empty cubic box: CO(g)
COg = Model.GasItem(Name="CO(g)", 
                    E0=-14.42576166, # DFT energy, eV
                    FreqR=[2104.300781], # Real frequencies, cm-1
                    Geometry='Diatomic heteronuclear', 
                    Mass=28.01, # Atomic mass, g/mol
                    RotT=2.77, # Rotational temperature, K
                    RotSymNum=1 # Rotational symmetry number = 1 (diatomic heteronuclear)
                   )
# Clean Ni(100) surface
N100 = Model.CleanSurf(Name='Ni100', E0=-291.86035891)

# Adsorbed CO/Ni(100)
N100_CO = Model.AdsItem(Name='N10/R17i CO.h', E0=-307.82811536,
                        FreqR=[1597.286883, 238.05862, 229.727279, 199.589309, 147.878114, 117.974835])
# Transition state CO -> C + O /Ni(100)
N100_CO_TS = Model.AdsItem(Name='N10/R17d CO.h -> C.h + O.h', E0=-305.94631980, 
                           FreqR=[593.036612, 551.302284, 450.144514, 344.84786, 250.855827], 
                           FreqI=[367.384136] # Imaginary frequency, cm-1 (not used, may be omited)
                          )
# Co-Adsorbed C+O/Ni(100) 
N100_C_O = Model.AdsItem(Name='N10/R17f C.h + O.h', E0=-307.69629330, 
                         FreqR=[672.032831, 640.703844, 400.586463, 342.050762, 328.190997, 259.747561])
```
Create the plot and add the steps
```
# plot base
import matplotlib.pyplot as plt
import stegoplot.Plot as stgplt

fig, axs = plt.subplots(1, 1, figsize=(8., 3.))
MyRef = stgplt.RxRef(1.5, 0.)

# Adding to plot
stgplt.RxStepTS([ [N100,COg], N100_CO ], Ref=MyRef, ThermoType='Gibbs', T = 265 + 273.15, P=1.,
    Name='CO adsorption', Hover=True, Color='r', AlphaLines=1.)
stgplt.RxStepTS([ N100_CO, N100_CO_TS, N100_CO ], Ref=MyRef, ThermoType='Gibbs', T = 265 + 273.15, 
    Name='CO disociation', Hover=True, Color='b', AlphaLines=1., PlotShape='Spline')
```
Remove `PlotShape='Spline'` if you don't have the `scipy` package.
Add a couple things to get a nicer plot
```
# Make it nicer
plt.ylabel("Gibbs free energy (kJ/mol)", fontweight='bold', fontsize='9')
plt.tick_params(axis="y", direction="inout", length=12.)
plt.axhline(y=0., color="k", alpha=.5, linewidth=.4)
axs.set_xticks([i[0] for i in MyRef.log])
axs.set_xticklabels(['CO + Ni(100)', 'C/Ni(100)', 'C+O/Ni(100)'])
plt.grid(which='major', color='k', linestyle='dashed', linewidth=.5, alpha=.3)
plt.show()
```

#### 3. Analysis of Density of States files (DOSCAR)
Loading a VASP-DOS file
```
import stegoplot.dedos as ds

N100 = ds.DOS("./DOSCAR_direction", Name="Ni(111), polarized, spd partition, no ml partition, 64 atoms and 656 electrons", 
              Pol=True, Orb="spd", ml=False, Nelect=656)
```
Ploting DOS
```
import matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 1)

# plot total DOS
N100.Plot(("total", "+"), Filled=True) 
N100.Plot(("total", "-"), Filled=True, PlotDown=True)

# plot d dos atom 32, amplified for better visibility
N100.Plot(("32", "+"), AmplifyFactor=10, Color='r') 
N100.Plot(("32", "-"), PlotDown=True, AmplifyFactor=10, Color='r')

# create curve summing d-DOS atoms 30-35 and plot it
N100.SumDOS(("d30-35",'d+'),[(str(i), 'd+') for i in range(30,36)])
N100.SumDOS(("d30-35",'d-'),[(str(i), 'd-') for i in range(30,36)])

N100.Plot(("d30-35", "d+"), AmplifyFactor=5, Color='g') 
N100.Plot(("d30-35", "d-"), PlotDown=True, AmplifyFactor=5, Color='g')

```
#### FAQ: Why "stego"?
I like dinosaurs :t-rex: :sauropod:.
