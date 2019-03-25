#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from  wgFakeLeptonModule import *

from countHistogramsModule import *

from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/data/Run2016B/SingleElectron/NANOAOD/05Feb2018_ver2-v2/00000/4C5A00D6-600B-E811-BB0C-D8D385AF891A.root"],None,"wg_fake_lepton_keep_and_drop.txt",[countHistogramsModule(),wgFakeLeptonModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True, outputbranchsel = "wg_fake_lepton_output_branch_selection.txt")

p=PostProcessor(".",inputFiles(),None,"wg_fake_lepton_keep_and_drop.txt",[countHistogramsModule(),wgFakeLeptonModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True, jsonInput=runsAndLumis(), outputbranchsel = "wg_fake_lepton_output_branch_selection.txt")

p.run()

print "DONE"
