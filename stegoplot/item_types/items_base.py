# This defines type to store computation results is defined
import stegoplot.promps
import stegoplot.parameters

class SingleItem:
	def __init__(self, **kwargs):
		"""
		Default values available for all kind of model
		"""
		# Identification
		self.Name 		= kwargs.get('Name','No name given')	# Name
		self.G_ID 		= kwargs.get('G_ID', None)				# Job ID of geometry job
		self.F_ID		= kwargs.get('F_ID', None)				# Job ID of frequency job
		self.type		= kwargs.get('type', 'Adsorbed')		# Type of model:
																#	'Adsorbed' (default)
																#	'Gas'
																#	'Clean surface'
																#	'Physisorbed'
		# for gaseous species, more specifications to compute thermodynamic properties are needed
		if self.type == 'Gas':
			self.mass 		= kwargs.get('Mass', None) 		# [AMU = g/mol]
			self.Geometry 	= kwargs.get('Geometry', None)	# 'Diatomic homonuclear'
															# 'Diatomic Heteronuclear' or
															# 'Poliatomic'
			self.RotSym		= kwargs.get('RotSymNum', None)	# Rotation symmetry number
			self.RotTemp 	= kwargs.get('RotT', None)		# Rotational temperatures [K]

		# Content
		self.Species	= None									# Species in the model

		# Results from computations
		self.E0			= float(	kwargs.get('E0', 0.))		# Energy, pure electronic, eV
		self.FreqR		= kwargs.get('FreqR', None)				# List of real frequencies
		self.FreqI		= kwargs.get('FreqI', None)				# List of imaginary frequencies

		# Run info
		self.Accuracy	= kwargs.get('Acc', None)				# Precision level, personal reference
		self.TS			= kwargs.get('TS', None)				# TS if transition state, otherwise stable geom
		self.Notes		= kwargs.get('Notes', None)				# General notes



	def __str__(self):
		mystr = 'Item: ' + self.Name + ' , type: ' + self.type
		if self.Notes: mystr += ' , Notes: ' + str(self.Notes)
		if self.G_ID: mystr += ' , ID(g): ' + str(self.G_ID)
		if self.G_ID: mystr += ' , ID(fq): ' + str(self.F_ID)

		return mystr 		# human readable

	def __repr__(self):
		myrepr = '|'.join([str(i)+':'+str(self.__dict__[i])
							for i in list(self.__dict__.keys())
							if not self.__dict__[i] == None])
		return myrepr	# unique, all info



	####################################################################################################################
	#### Thermodynamic functions by type :
	#### These should be overwritten in each kind class created from SingleItem

	#### ---------------- Base for Partition functions
	def q_tras(self, **kwargs):
		pass
	def q_rot(self, **kwargs):
		pass
	def q_vib(self, **kwargs):
		pass
	def q_el(self, **kwargs):
		pass
	# q total is always the product
	def q_total(self, Report=False, **kwargs):
		out = self.q_tras(**kwargs) * self.q_rot(**kwargs) * self.q_vib(**kwargs) * self.q_el(**kwargs)
		stegoplot.promps.report(Report, 'q(total)', out, self)
		return out

	#### ---------------- Base for Thermo Energy contributions
	def ZPVE(self, **kwargs):
		pass
	def Etras(self, **kwargs):
		pass
	def Erot(self, **kwargs):
		pass
	def Evib(self, **kwargs):
		pass
	def Eel(self, **kwargs):
		pass

	#### ---------------- Base for Thermo Entropy contributions
	def Stras(self, **kwargs):
		pass
	def Srot(self, **kwargs):
		pass
	def Svib(self, **kwargs):
		pass
	def Sel(self, **kwargs):
		pass


	#### ---------------- Thermodynamic functions

	def Internal(self, **kwargs):
		# U = (E0 + Eel) + Etras + Erot + (ZPVE + Evib)
		pass

	def Enthalpy(self, **kwargs):
		# H = U + PV = U + kbT
		pass

	def E0(self):
		# E0, called as function if is convenient
		return self.E0()

	def E0ZPVE(self, Report=False, **_unused):
		# E0 + ZPVE
		out = self.E0 + self.ZPVE()
		stegoplot.promps.report(Report, 'E0-ZPVE', out, self)
		return out

	def Entropy(self, **kwargs):
		# S = Sel + Stras + Srot + Svib
		pass

	# Gibbs G
	def Gibbs(self, T=None, P=None, Report=False):
		# H-TS
		outH = self.Enthalpy(T=T)
		outS = self.Entropy(T=T, P=P)
		out = outH - T * outS
		if Report:
			stegoplot.promps.report(True, 'Gibbs', out, self)
			if Report == 'Detailed':
				print(f"    >>>>  G/eV="+str(out))
				print(f"    >>>>  H/eV="+str(outH))
				print(f"    >>>>  S/(eV/K)="+str(outS))
		return out

	def GetThermo(self, ThermoType=stegoplot.parameters.def_PlotType,
				  T=None, P=None, Report=True, **_unused) -> float:
		# Calls for E0 or thermo functions with strings 'E0', 'Internal', ... , 'Gibbs'
		# ThermoType has to be defined here or in the child classes from SingleItem
		try:
			if ThermoType == 'E0':
				out =  self.E0
			else:
				fun	= getattr(self, ThermoType)
				out = fun(T=T, P=P, Report=False, **_unused)

			stegoplot.promps.report(Report,ThermoType,out,self, end='')
			if Report:
				print(' '*5+'(T = '+str(T) + ' , P = '+str(P)+')')

			return out
		except NameError:
			raise NameError('Error computing ' + ThermoType + ' for ' + self.Name)




