#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from  PhysicsTools.NanoAODTools.postprocessing.examples.exampleModule import *
p=PostProcessor(".",inputFiles(),"nJet >= 2 && Jet_pt[0] >= 30 && Jet_pt[1] >= 30 && nPhoton >= 1 && Photon_pt[0] > 25 && ((nMuon >= 2) || (nElectron >= 2))",modules=[exampleModule()],provenance=True,fwkJobReport=True,jsonInput=runsAndLumis(),justcount=False)
p.run()

print "DONE"
os.system("ls -lR")


