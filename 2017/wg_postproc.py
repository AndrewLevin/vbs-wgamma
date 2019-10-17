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

#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv5/WGToLNuG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/110000/1D07F9F3-EB9C-2143-B467-387E4F7D4A72.root"],None,"wg_keep_and_drop.txt",[countHistogramsModule(),puWeight_2017(),wgModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True, outputbranchsel = "wg_output_branch_selection.txt")

p=PostProcessor(".",inputFiles(),None,"wg_keep_and_drop.txt",[countHistogramsModule(),puWeight_2017(),PrefCorr(),wgModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True, jsonInput=runsAndLumis(), outputbranchsel = "wg_output_branch_selection.txt")

p.run()

print "DONE"
os.system("ls -lR")
