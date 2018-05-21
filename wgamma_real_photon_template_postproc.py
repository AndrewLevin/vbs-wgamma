#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from  wgammaRealPhotonTemplateModule import *

#from countHistogramsModule import *

#from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext3-v1/00000/2679E038-0116-E811-B474-24BE05BD4F61.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext3-v1/00000/16C79854-0316-E811-BB87-5065F381A251.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext3-v1/00000/50A199D9-0416-E811-9D17-E0071B73C620.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext3-v1/00000/9E91A538-0116-E811-A070-24BE05CEBD61.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext3-v1/00000/B84B387D-1416-E811-B3BA-24BE05CECBD1.root"],"","wgamma_real_photon_template_keep_and_drop.txt",[exampleModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True)

p.run()

print "DONE"
os.system("ls -lR")
