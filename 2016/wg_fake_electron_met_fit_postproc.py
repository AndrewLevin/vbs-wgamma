#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from  wgFakeElectronMETFitModule import *

from countHistogramsModule import *

#from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/data/Run2016B/SingleElectron/NANOAOD/05Feb2018_ver2-v2/00000/4C5A00D6-600B-E811-BB0C-D8D385AF891A.root"],"","keep_and_drop.txt", [countHistogramsModule(),exampleModule()],outputbranchsel = "output_branch_selection.txt",provenance=True,justcount=False,noOut=False,fwkJobReport=True)

p=PostProcessor(".",["/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/927F1543-6366-E811-84E9-0025905A6070.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/A0BF21E0-7A66-E811-A6A0-0CC47A7C3636.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/BCB6497A-9B66-E811-88B7-0CC47A7C349C.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/C4D0FA76-5D66-E811-A00C-0CC47A4D76C6.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/C689CE02-C066-E811-BE54-0CC47A7C3628.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/C8DFB777-7366-E811-890F-0CC47A4D7674.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/D4E600EA-9F66-E811-9E19-A0369FE2C0D0.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/DA3D01B4-5066-E811-AC03-0025905A497A.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/E675F33F-4D66-E811-9A8D-0025905B85DC.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/E6F2574C-D766-E811-B047-0CC47ABB518A.root"],None,"keep_and_drop.txt",[countHistogramsModule(),exampleModule()],outputbranchsel = "output_branch_selection.txt",provenance=True,justcount=False,noOut=False)

#p=PostProcessor(".",inputFiles(),None,"wg_fake_electron_keep_and_drop.txt",[countHistogramsModule(),exampleModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True,jsonInput=runsAndLumis(), outputbranchsel = "output_branch_selection.txt")

p.run()

print "DONE"
os.system("ls -lR")
