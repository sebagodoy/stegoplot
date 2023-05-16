from stegoplot.tools import InertiaMoment as imo
from stegoplot.promps import fNum

#### ---- Case 1
print('-'*80+'\n'+ 'Case 1' +'\n'+'-'*80)
# The complete definition is
imo(filedir='./CONTCAR', subset=None)
# which will only show the computed eigenvalues and eigenvectors
# filedir: (string) defines the direction of the POSCAR/CONTCAR file to open
# subset: (string) allows to only take a subset of the available atoms,
# e.g. 3,5,6-9,13 for a file with at least 13 atoms, None if all atoms
# are to be considered

#### ---- Case 2
print('-'*80+'\n'+ 'Case 2' +'\n'+'-'*80)
# A short definition such will ask about the direction and if only a subset of atoms
# is to be considered
imo()

#### ---- Case 3
print('-'*80+'\n'+ 'Case 3' +'\n'+'-'*80)
# You can drop the keyword of the argument as long as you respect the order of
# arguments and all keyworded arguments are after all not-keyworded arguments
# return value is a list of tuples that are the eigenvalue, eigenvector (as list)
asd = imo('./CONTCAR', None)
# Fancy way of printing output
print('\nPrinting saved output in a fancy way')
[print(fNum(i[0], '6f')+' : '+str([fNum(j,'4f') for j in i[1]])) for i in asd]