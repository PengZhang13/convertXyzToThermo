import os
from rmgpy.molecule.molecule import Molecule
from rmgpy.rmg.model import Species
from rmgpy.rmg.model import CoreEdgeReactionModel
from rmgpy.rmg.main import RMG
from rmgpy import settings
from rmgpy.data.rmg import RMGDatabase

rmg = RMG()
rmg.database = RMGDatabase()
path = os.path.join(settings['database.directory'])
rmg.database.loadThermo(os.path.join(path,'thermo'))
	
mol = Molecule().fromSMILES('C1=CC=CC=C1')
tdt = rmg.database.thermo.estimateThermoViaGroupAdditivity(mol)
print tdt.comment
print mol.isAromatic()

spc = Species().fromSMILES('C1=CC=CC=C1')
tdt = rmg.database.thermo.getThermoDataFromGroups(spc)
print tdt.comment
print '\n'
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

