#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from  wgFakePhotonModule import *

from countHistogramsModule import *

from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv4/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6_ext2-v1/30000/9838A052-18F1-7440-B7A9-2A693784A78C.root"],None,"wg_fake_photon_keep_and_drop.txt",[countHistogramsModule(), exampleModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True,outputbranchsel = "wg_fake_photon_output_branch_selection.txt")

#p=PostProcessor(".",["/afs/cern.ch/work/a/amlevin/wjets_prod/CMSSW_10_2_11/src/Merged.root"],None,"wg_fake_photon_keep_and_drop.txt",[countHistogramsModule(), exampleModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True,outputbranchsel = "wg_fake_photon_output_branch_selection.txt")

#p=PostProcessor(".",["/eos/user/y/yangli/andrew/data/nano/unmerged/wjets.10.root","/eos/user/y/yangli/andrew/data/nano/unmerged/wjets.100.root","/eos/user/y/yangli/andrew/data/nano/unmerged/wjets.1005.root"],None,"wg_fake_photon_keep_and_drop.txt",[exampleModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True,outputbranchsel = "wg_fake_photon_output_branch_selection.txt")

#p=PostProcessor(".",["/afs/cern.ch/user/a/amlevin/miniaod_production/condor/jobs/Merged.root"],None,"wg_fake_photon_keep_and_drop.txt",[exampleModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True,outputbranchsel = "wg_fake_photon_output_branch_selection.txt")

p=PostProcessor(".",inputFiles(),None,"wg_fake_photon_keep_and_drop.txt",[countHistogramsModule(),exampleModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True,jsonInput=runsAndLumis(),outputbranchsel = "wg_fake_photon_output_branch_selection.txt")

p.run()

print "DONE"

