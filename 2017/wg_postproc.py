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

p=PostProcessor(".",inputFiles(),None,"wg_keep_and_drop.txt",[countHistogramsModule(),puWeight_2017(),PrefCorr(),wgModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True, jsonInput=runsAndLumis(), outputbranchsel = "wg_output_branch_selection.txt")

#p=PostProcessor(".",inputFiles(),None,"wg_keep_and_drop.txt",[countHistogramsModule(),wgModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True, jsonInput=runsAndLumis(), outputbranchsel = "wg_output_branch_selection.txt")

p.run()

print "DONE"
