import os
import pybel
from rmgpy.molecule.molecule import Molecule
from rmgpy.rmg.model import Species
from rmgpy.rmg.model import CoreEdgeReactionModel
from rmgpy.rmg.main import RMG
from rmgpy import settings
from rmgpy.data.rmg import RMGDatabase
# import rmgpy.thermo.ThermoData

delimiter = '\t'
JtoCal = 1.0/4.184

rmg = RMG()
rmg.database = RMGDatabase()
path = os.path.join(settings['database.directory'])
rmg.database.loadThermo(os.path.join(path,'thermo'))

fw = open('output_thermo.txt','w')
fw.write('Name\tSMILES\tH298\tS298\t300 K\t400 K\t500 K\t600 K\t800 K\t1000 K\t1500 K\tComment\n')

#for mymol in pybel.readfile("xyz","testfile.txt"):
#	bel_mol = mymol.write('smi')
#	mol_smi = bel_mol.split()[0]
#	mol_name = bel_mol.split()[1]
#	print mol_name
#
#	mol = Molecule().fromSMILES(mol_smi)
#	print type(mol)
#	print mol.toAdjacencyList()
#	print mol.toInChI()
#	print mol.isCyclic()
#	print mol.isAromatic()
#	tdt = rmg.database.thermo.estimateThermoViaGroupAdditivity(mol)
#	
#	tempstr = mol_name + delimiter + mol_smi + delimiter + str(tdt.H298.value*JtoCal) + delimiter + str(tdt.S298.value*JtoCal)
#	tempstr = tempstr + delimiter + str(tdt.Cpdata.value[0]*JtoCal) + delimiter + str(tdt.Cpdata.value[1]*JtoCal) + delimiter + str(tdt.Cpdata.value[2]*JtoCal)
#	tempstr = tempstr + delimiter + str(tdt.Cpdata.value[3]*JtoCal) + delimiter + str(tdt.Cpdata.value[4]*JtoCal) + delimiter + str(tdt.Cpdata.value[5]*JtoCal)
#	tempstr = tempstr + delimiter + str(tdt.Cpdata.value[6]*JtoCal) + delimiter + tdt.comment + '\n'
#	fw.write( tempstr )
#
#	print tdt.comment
#	print '\n'
	
mol = Molecule().fromSMILES('C1=CC=CC=C1')
tdt = rmg.database.thermo.estimateThermoViaGroupAdditivity(mol)
print tdt.comment
print mol.isAromatic()

spc = Species().fromSMILES('C1=CC=CC=C1')
tdt = rmg.database.thermo.getThermoDataFromGroups(spc)
print tdt.comment


rmg.reactionModel = CoreEdgeReactionModel()
spc, isNew = rmg.reactionModel.makeNewSpecies(mol)
rmg.reactionModel.addSpeciesToEdge(spc)
rmg.initialSpecies = []
rmg.initialSpecies.append(spc)
for species in rmg.initialSpecies:
	#species.generateThermoData(rmg.database, quantumMechanics=rmg.reactionModel.quantumMechanics)
	#print species.thermo.comment
	tdt = rmg.database.thermo.getThermoDataFromGroups(spc)
	print tdt.comment


fw.close()

