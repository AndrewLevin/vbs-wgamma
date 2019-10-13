#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from  wgFakePhotonModule import *

from countHistogramsModule import *

from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv5/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/60000/FB94D122-ED9B-5A47-B583-87F129CA0AC5.root"],None,"wg_fake_photon_keep_and_drop.txt",[countHistogramsModule(),exampleModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True,outputbranchsel = "wg_fake_photon_output_branch_selection.txt")

p=PostProcessor(".",inputFiles(),None,"wg_fake_photon_keep_and_drop.txt",[countHistogramsModule(),exampleModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True,jsonInput=runsAndLumis(),outputbranchsel = "wg_fake_photon_output_branch_selection.txt")

p.run()

print "DONE"





