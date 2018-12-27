#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from  ewkwgjjModule import *

from countHistogramsModule import *

#from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

#p=PostProcessor(".",inputFiles(),None,"keep_and_drop.txt",[countHistogramsModule(),exampleModule()],provenance=True,justcount=False,fwkJobReport=True,jsonInput=runsAndLumis(),noOut=False,outputbranchsel = "output_branch_selection.txt")

#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/A6FA98D6-2C10-E811-979C-0CC47AA992D0.root"],"luminosityBlock < 4000","keep_and_drop.txt",[countHistogramsModule(),exampleModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True, outputbranchsel = "output_branch_selection.txt")

#p=PostProcessor(".",["/afs/cern.ch/work/a/amlevin/data/ZGToLLG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/F632B479-9E66-E811-97CB-0CC47AD98BC6.root"],"luminosityBlock < 10000","keep_and_drop.txt",[countHistogramsModule(),exampleModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True, outputbranchsel = "output_branch_selection.txt")

#p=PostProcessor(".",["/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/2CB977C4-D366-E811-B0E7-F4E9D4AEC940.root"],None,"keep_and_drop.txt",[countHistogramsModule(),exampleModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True, outputbranchsel = "output_branch_selection.txt")

p=PostProcessor(".",["/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/00CB3868-B166-E811-926C-A0369FD0B1FE.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/0252C3ED-9F66-E811-9E46-0025905B85DE.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/08F74682-9B66-E811-A6F5-0CC47A4D75F4.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/12B7972F-B066-E811-94CF-002590E7DDE6.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/20D2E131-6366-E811-A2F9-0CC47ABD6C6C.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/2CB977C4-D366-E811-B0E7-F4E9D4AEC940.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/8CF45655-D266-E811-AFB0-0CC47A1DF806.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/927F1543-6366-E811-84E9-0025905A6070.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/A0BF21E0-7A66-E811-A6A0-0CC47A7C3636.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/BCB6497A-9B66-E811-88B7-0CC47A7C349C.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/C4D0FA76-5D66-E811-A00C-0CC47A4D76C6.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/C689CE02-C066-E811-BE54-0CC47A7C3628.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/C8DFB777-7366-E811-890F-0CC47A4D7674.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/D4E600EA-9F66-E811-9E19-A0369FE2C0D0.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/DA3D01B4-5066-E811-AC03-0025905A497A.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/E675F33F-4D66-E811-9A8D-0025905B85DC.root","/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/E6F2574C-D766-E811-B047-0CC47ABB518A.root",],"event == 10708120","keep_and_drop.txt",[countHistogramsModule(),exampleModule()],provenance=True,justcount=False,noOut=False,outputbranchsel = "output_branch_selection.txt")

#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/FCBAED65-2310-E811-B753-FA163E7BC23F.root"],None,"keep_and_drop.txt",[countHistogramsModule(),exampleModule()],provenance=True,justcount=False,noOut=False)

#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/LNuAJJ_EWK_MJJ-120_13TeV-madgraph-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/0A47B7D5-4C13-E811-82B9-3417EBE46601.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/LNuAJJ_EWK_MJJ-120_13TeV-madgraph-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/F4FE2CE1-4C13-E811-891B-44A84225C827.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/LNuAJJ_EWK_MJJ-120_13TeV-madgraph-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/B603787F-8D13-E811-83FE-0CC47A6C06C2.root"],None,"keep_and_drop.txt",[exampleModule()],provenance=True,justcount=False,noOut=False)

#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/data/Run2016B/SingleMuon/NANOAOD/05Feb2018_ver2-v1/20000/00935047-750C-E811-B32E-14DDA9243247.root"],"","keep_and_drop.txt",[exampleModule()],provenance=True,justcount=False,noOut=False)

#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/LNuAJJ_EWK_MJJ-120_13TeV-madgraph-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/0A47B7D5-4C13-E811-82B9-3417EBE46601.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/LNuAJJ_EWK_MJJ-120_13TeV-madgraph-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/F4FE2CE1-4C13-E811-891B-44A84225C827.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/LNuAJJ_EWK_MJJ-120_13TeV-madgraph-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/B603787F-8D13-E811-83FE-0CC47A6C06C2.root"],"nJet >= 2 && Jet_pt[0] >= 40 && Jet_pt[1] >= 30 && event == 9968","keep_and_drop.txt",[exampleModule()],provenance=True,justcount=False,noOut=False)

p.run()

print "DONE"
os.system("ls -lR")
