#### Physical constants
kb			= 1.3806488E-23		# Boltzmann's constant [m2 kg / s2 K]
hh			= 6.62606957E-34	# Plack's constant [m2 kG/s]
cc			= 299792458			# Light speed in vacuum [m/s]
Nav			= 6.02214129E23		# Avogadro's Number [particles/mol]

#### Conversion factors
eV2J		= 1.602176634E-19	# eV -> J
eV2kJ       = eV2J/1000         # eV -> kJ
eV2kJpmol	= (eV2J*Nav)/1000	# eV -> kJ/mol

ha2eV       = 27.211386245988   # ha -> eV

J2cal       = 0.238902957       # J -> cal

bar2Pa		= 100000.			# bar -> Pa

##### Atomic mases
atom_mases = {
    'H':1.0079,'He':4.0026,
    'Li':6.941,'Be':9.0122,'B':10.811,'C':12.0107,'N':14.0067,'O':15.9994,'F':18.9984,'Ne':20.1797,
    'Na':22.9897,'Mg':24.305,'Al':26.9815,'Si':28.0855,'P':30.9738,
    'S':32.065,'Cl':35.453,'K':39.0983,'Ar':39.948,
    'Ca':40.078,'Sc':44.9559,'Ti':47.867,'V':50.9415,'Cr':51.9961,
    'Mn':54.938,'Fe':55.845,'Ni':58.6934,'Co':58.9332,
    'Cu':63.546,'Zn':65.39,'Ga':69.723,'Ge':72.64,'As':74.9216,'Se':78.96,
    'Br':79.904,'Kr':83.8, 'Rb':85.4678,'Sr':87.62, 'Y':88.9059,'Zr':91.224,'Nb':92.9064,
    'Mo':95.94,'Tc':98,'Ru':101.07,'Rh':102.9055,'Pd':106.42,'Ag':107.8682,'Cd':112.411,
    'In':114.818,'Sn':118.71,'Sb':121.76,'I':126.9045,'Te':127.6,'Xe':131.293,'Cs':132.9055,
    'Ba':137.327,'La':138.9055,'Ce':140.116,'Pr':140.9077,'Nd':144.24,'Pm':145,'Sm':150.36,
    'Eu':151.964,'Gd':157.25,'Tb':158.9253,'Dy':162.5,'Ho':164.9303,'Er':167.259,'Tm':168.9342,
    'Yb':173.04,'Lu':174.967,'Hf':178.49,'Ta':180.9479,'W':183.84,'Re':186.207,'Os':190.23,
    'Ir':192.217,'Pt':195.078,'Au':196.9665,'Hg':200.59,'Tl':204.3833,'Pb':207.2,'Bi':208.9804,
    'Po':209,'At':210,'Rn':222,'Fr':223,'Ra':226,'Ac':227,'Pa':231.0359,'Th':232.0381,'Np':237,
    'U':238.0289,'Am':243,'Pu':244,'Cm':247,'Bk':247,'Cf':251,'Es':252,'Fm':257,'Md':258,
    'No':259,'Rf':261,'Lr':262,'Db':262,'Bh':264,'Sg':266,'Mt':268,'Rg':272,'Hs':277
}

#### Environment parameters
def_T = 298.15           # K
def_P = 1.0000           # bar
def_Etype  = 'Gibbs'     # Energy type to work with
def_Eunits = 'eV'
def_PlotType = 'E0'

def_HoverNoteBin = []

def showdefaults():
	print('-'*4+' def. parameters '+'-'*4)
	print('def T		/K		: '+ str(def_T))
	print('def P		/bar	: ' + str(def_P))
	print('def E-type			: ' + str(def_P))
	print('def E-units			: ' + str(def_P))
	print('-'*25)



