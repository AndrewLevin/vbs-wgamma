#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from  wgModule import *

from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *

from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv5/WGToLNuG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/250000/F8A07C7D-D4F6-9D47-ACD1-DE2A0B9861A2.root"],None,"wg_keep_and_drop.txt",[countHistogramsModule(),wgModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True, outputbranchsel = "wg_output_branch_selection.txt")

p=PostProcessor(".",inputFiles(),None,"wg_keep_and_drop.txt",[countHistogramsModule(),puWeight_2018(),wgModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True, jsonInput=runsAndLumis(), outputbranchsel = "wg_output_branch_selection.txt")

p.run()

print "DONE"
os.system("ls -lR")
