# Stego(reaction) plot, a DFT analysis tool

A python package that helps with organizing and analyzing DFT results, computing thermodynamic properties, 
analyzing DOS and more things to come.


#### Requirements
* Python 3.6 or later
* NumPy
* matplotlib
* scipy (optional, for curvy reaction profiles)

#### Installation
While testing, is recomended to install stego in a separate virtual environment, so it does not
interfere with anything else. Following [this](https://packaging.python.org/en/latest/tutorials/packaging-projects/) and 
[this](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-and-using-virtual-environments) guides, and working in the `<DIR>` directory:
```
python3 -m venv <DIR>
source <DIR>/bin/activate
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps example-package-YOUR-USERNAME-HERE
```
now you can check the test examples included above (test folder) as  python scripts and jupyter noteboks.

#### Why "stego"?
I like dinosaurs :sauropod:.

#### Basic example 
Loading and adding a molecule
```
import stegoplot as stg
H2O = stg.items.Gas(Name='H2O',
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
Loading a VASP-DOS file
```
import stegoplot.dedos as ds

N100 = ds.DOS("./DOSCAR_direction", Name="Ni(111), polarized, spd partition, no ml partition, 64 atoms, 656 electrons", 
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
