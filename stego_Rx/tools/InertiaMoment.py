#!/usr/bin/env python3

# This script reads POSCAR/CONTCAR type files and computes center of mass and inertia moments.
# It allows selecting a subset of atoms

# v0.2 - 16/ago/2022 - SAGG

# packages
def InertiaMoment(filedir: 'str, CONTCAR direction' = None,
                  subset: 'str, atom subset (e.g. 3,5,6-9,13), None for all atoms' = 'def_none')\
        -> "[(eual1, [evect1])]":
    import numpy as np
    from stego.parameters import atom_mases
    from stego.promps import CodeStatus as Report

    # Custom functions
    def FixNum(iNum, **kwargs):
        myformat = "{:"+str(kwargs.get('tot',12))+"."+str(kwargs.get('dec',4))+"f}"
        return myformat.format(iNum)


    # Open file
    if filedir == None:
        filedir = input('  > File (def=./CONTCAR) : ') or './CONTCAR'
    try:
        with open(filedir, 'r') as f:
            content = f.readlines()
            Report('Opened '+filedir+' file')
    except FileNotFoundError:
        print('That\'s no file')

    # Get box
    latfactor = float(content[1])
    cellbox = [[float(j)*latfactor for j in content[i].split()] for i in range(2,5)]

    # Get atom types
    atomtype_names = content[5].split()
    atomtype_numbers = [int(i) for i in content[6].split()]
    natoms = sum(atomtype_numbers)
    Report('Detected '+str(natoms)+' atoms including : '+', '.join(atomtype_names))

    # Get coords n mass
    AtomData = [] # [x, y, z, 'atom name', atom mass (float)]
    atomcounter = 0
    for i, k in zip(atomtype_names, atomtype_numbers):
        for iatom in range(k):
            AtomData.append([float(coor) for coor in content[9 + atomcounter].split()[:3]]+[i] + [atom_mases[i]])
            atomcounter += 1

    # Correct direct coordinates
    if content[8][:-1].rstrip() in 'Direct':
        # scalate coordinates to the box
        Report('Scaling direct coordinates to cartesian for all atoms')
        for iatom in AtomData:
            iatom[:3] = [ sum([cellbox[i][j]*iatom[i] for i in range(3)]) for j in range(3)]

    # ---------------------------------------------------------------------------------------------------------------
    # Select subset
    if subset == 'def_none':
        subset = input('  > Select subset of atoms (e.g. 3,5,6-9,13) or use all (def.) :')
    if not subset:
        Report('Using all atoms')
        Atoms = [i for i in AtomData]
    else:
        Atoms = []
        for k in subset.split(','):
            if '-' in k:
                for j in range(int(k.split('-')[0]) -1 , int(k.split('-')[1])):
                    Atoms.append(AtomData[j])
            else:
                Atoms.append(AtomData[int(k)-1])
        Report('Chosen a subset of the available atoms.')

    # Ask about mases
    ThisMases = {}
    for i in Atoms:
        ThisMases[i[3]]=i[4]
    Report('Selection includes : '+', '.join(list(ThisMases.keys())))


    # --------------------------------------------------------------------------------
    # Compute mass center
    TotalMass = sum([i[4] for i in Atoms])
    MassCenter = [sum([i[j]*i[4]/TotalMass for i in Atoms]) for j in range(3)]
    Report('Total mass of the selected subset is : '+FixNum(TotalMass))
    Report('Mass center is : ['+' , '.join([FixNum(i, tot=8) for i in MassCenter])+']')

    if [[cellbox[i][j] for j in range(3) if j!=i] for i in range(3)] == [[0.,0.],[0.,0.],[0.,0.]]:
        # squared cell
        Report('        direct : ['+' , '.join([FixNum(MassCenter[i]/cellbox[i][i], tot=8) for i in range(3)])+']')

    # Correct coordinates to mass center
    for iatom in Atoms:
        iatom[0:3] = [iatom[j]-MassCenter[j] for j in range(3)]

    # Inertia tensor
    Itens = [[0., 0., 0.], [0., 0., 0.], [0., 0., 0.]]
    for iatom in Atoms:
        mag2 = sum([i**2 for i in iatom[:3]])
        for i in range(3):
            for j in range(3):
                Itens[i][j] -= iatom[i]*iatom[j]*iatom[4]
            Itens[i][i] += mag2*iatom[4]

    Report('Inertia tensor : ')
    for i in Itens:
        print(' '*16, end='')
        for j in i:
            print(FixNum(j), end=' , ')
        print()

    # Ineria moments around principal axis
    ITensArray = np.array(Itens)
    w, v = np.linalg.eig(ITensArray)
    Report('Inertia moments and principal rotation axis : ')
    for i, j in zip(w,v):
        print(' '*16, end='')
        print('['+' , '.join([FixNum(k, tot=8) for k in j])+']', end=' -> ')
        print(FixNum(i, tot=8) + ' (g/mol)*A2')

    # Return values
    return [(i, [k for k in j]) for i,j in zip(w,v)]

