#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from  wgModule import *

from countHistogramsModule import *

from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv4/WGToLNuG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/Nano14Dec2018_102X_upgrade2018_realistic_v16_ext1-v1/280000/2718AFF6-1E91-C049-A93A-7FBD99B9417B.root"],None,"keep_and_drop.txt",[countHistogramsModule(),exampleModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True, outputbranchsel = "output_branch_selection.txt")

p=PostProcessor(".",inputFiles(),None,"keep_and_drop.txt",[countHistogramsModule(),exampleModule()],provenance=True,justcount=False,fwkJobReport=True,jsonInput=runsAndLumis(),noOut=False,outputbranchsel = "output_branch_selection.txt")

p.run()

print "DONE"
#os.system("ls -lR")
