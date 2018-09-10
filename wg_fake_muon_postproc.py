#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from  wgFakeMuonModule import *

from countHistogramsModule import *

from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/data/Run2016B/SingleMuon/NANOAOD/05Feb2018_ver2-v1/00000/3E505A6E-3110-E811-A6C7-001E677924DA.root"],"","wgamma_fake_muon_keep_and_drop.txt",[exampleModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True)

p=PostProcessor(".",inputFiles(),None,"wg_fake_muon_keep_and_drop.txt",[countHistogramsModule(),exampleModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True,jsonInput=runsAndLumis())

#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/10A1E550-0C13-E811-9B62-02163E01A0EA.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/1C863721-1213-E811-945E-FA163ED0EEE2.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/48E79972-1213-E811-8728-90E2BAD1C730.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/5A394C06-0413-E811-9ABA-02163E019FBE.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/5C73F562-1213-E811-80EB-000AE488BA7A.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/7AF75650-1213-E811-A970-E0071B696BB1.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/7C4D3E8C-0A13-E811-9D86-FA163E619054.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/84A7AB2E-0713-E811-A207-0025905C5438.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/88306BAD-0913-E811-A02A-0025905C3D98.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/8E2D575B-1213-E811-86B3-002590D9D894.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/C6B0785E-0A13-E811-8D10-0CC47AF9B2BA.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/DA8FC11F-1213-E811-BB78-0025905C53A6.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/F0B929B4-0213-E811-ABCC-0CC47AF9B2CA.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/80000/CED8A61B-B515-E811-85AE-0025904C4F9E.root"],"","wgamma_fake_muon_keep_and_drop.txt",[exampleModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True)

#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/10A1E550-0C13-E811-9B62-02163E01A0EA.root"],"","wgamma_fake_muon_keep_and_drop.txt",[exampleModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True)

#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/40000/02B1EABD-8813-E811-AC2C-02163E01A002.root"],"","wgamma_fake_muon_keep_and_drop.txt",[exampleModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True)

#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/40000/08CAFE03-5514-E811-8DAC-ECB1D7B67E10.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/40000/02B1EABD-8813-E811-AC2C-02163E01A002.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/40000/084BFDFD-9513-E811-AA07-B496910A80E8.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/40000/1436EE09-C513-E811-8EC0-38EAA78D8AF4.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/40000/1EDE33FB-B813-E811-888E-34E6D7BEAF1B.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/40000/24F52D93-BE13-E811-9D73-008CFA197A70.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/40000/2689C84A-9414-E811-9492-A0369FC5E9A4.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/40000/604A7D18-6214-E811-82D6-44A84225C851.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/40000/625ECF7F-FC13-E811-991E-FA163EB77965.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/40000/6C921C20-5814-E811-8A50-7CD30AC03054.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/40000/8CFE1C49-7613-E811-B327-02163E012F16.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/40000/A00C43B2-9114-E811-9DF4-D8D385AF889C.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/40000/D0C1D928-9A14-E811-8679-1458D04923EC.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/40000/DE70E70A-7613-E811-97CC-FA163E4D44E3.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/40000/E44F048D-A613-E811-8DBC-02163E013BEB.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/40000/E4B8778D-9213-E811-818F-002590D8C77A.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/40000/EA96C347-8513-E811-B449-008CFA14F814.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/40000/ECFDC1D4-CC13-E811-ACC5-FA163EF2B678.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/40000/FAB6D6BA-FB13-E811-8646-002590E3A004.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/80000/069ACBBE-0914-E811-AB7B-FA163E766FEC.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/80000/1E5BC3BD-3414-E811-95C1-00215A45F882.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/80000/1EEE9FC6-3414-E811-8204-0CC47A5FC495.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/80000/56B16DE6-3214-E811-AF18-0026B9278692.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/80000/58E89AA6-3414-E811-B111-008CFA0A5830.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/80000/5C2C9867-FC13-E811-887F-0CC47AD98A9A.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/80000/6C680CAB-3414-E811-9C15-0CC47AD98B94.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/80000/7293622E-E314-E811-85FC-0025905B856E.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/80000/72C7432C-8613-E811-A0BE-FA163EE11529.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/80000/740BF0CB-3414-E811-9194-FA163EE240BA.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/80000/C6AB9001-3514-E811-8433-141877641875.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/80000/C8BF2940-C013-E811-B6E1-8CDCD4A9A484.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/80000/CAAD3AD2-6913-E811-BC8B-FA163E4B02D6.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/80000/D2F703D8-AC13-E811-A914-02163E017C6D.root","root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext1-v1/80000/DA18896D-9B13-E811-9130-FA163E250C6C.root"],"","wgamma_fake_muon_keep_and_drop.txt",[exampleModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True)

p.run()

print "DONE"
os.system("ls -lR")