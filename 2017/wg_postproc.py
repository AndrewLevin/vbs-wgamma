#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from  wgModule import *

from countHistogramsModule import *

#from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/data/Run2017F/SingleElectron/NANOAOD/31Mar2018-v1/80000/FAA47698-566B-E811-B4D3-FA163E54DF16.root"],None,"keep_and_drop.txt",[countHistogramsModule(),exampleModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True, outputbranchsel = "output_branch_selection.txt")

#p=PostProcessor(".",inputFiles(),None,"keep_and_drop.txt",[countHistogramsModule(),exampleModule()],provenance=True,justcount=False,fwkJobReport=True,jsonInput=runsAndLumis(),noOut=False,outputbranchsel = "output_branch_selection.txt")

p.run()

print "DONE"
os.system("ls -lR")
