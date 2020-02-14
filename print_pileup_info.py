import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--infile",type=str,help="Input filename",required=True)
parser.add_argument("--lumi",type=int,help="Luminosity block number",required=True)
parser.add_argument("--event",type=int,help="Event number",required=True)


args = parser.parse_args()

import ROOT
import sys
from DataFormats.FWLite import Events, Handle

#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/EEF150FB-C5B1-E611-87B0-FA163EFD20EB.root'])

#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISpring15PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v2-v2/80008/9C1072E7-FC82-E611-A3CD-0CC47A78A3F8.root']) 

#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v2/10000/F81C1AE5-A14C-E711-8F12-FA163E662601.root'])

#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/5A15E25A-6BBE-E611-BBB5-001E67A40442.root']) #event 1

#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/44F71518-BDBE-E611-BFC9-047D7BD6DD56.root']) #event 2

#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/C2570CF1-8CBE-E611-9F56-0CC47A00A814.root']) #event 3

#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/FEE5FAF1-0EBF-E611-B699-002590AB38DA.root']) #event 4

#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/9A90BF89-11BF-E611-B9F9-842B2B71EDBE.root']) #event 5

#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/345A6B28-FABE-E611-BA99-D4AE526A0B47.root']) #event 6

#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/E012BFB6-C7BE-E611-8142-D4AE526A0DAE.root']) #event 7

#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/06845F4A-10BF-E611-983E-0CC47A7E6A8E.root']) #event 8

#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/7C9AA3AE-C2BE-E611-8F63-70106F4D2378.root']) #event 9

#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/0E560383-8CBE-E611-9A71-E41D2D08DE80.root']) #event 10

events = Events ([args.infile])

#events = Events (['/afs/cern.ch/work/a/amlevin/wjets_prod/CMSSW_8_0_21/src/SMP-RunIISummer16DR80Premix-00199.root']) 

genparticles, genParticlesLabel = Handle("vector<reco::GenParticle>"), "genParticles"

photons,photonsLabel = Handle("vector<reco::Photon>"), 'gedPhotons'

ebdigis,ebdigisLabel = Handle("EBDigiCollection"),("selectDigi","selectedEcalEBDigiCollection","RECO")

#puSummaryInfo,puSummaryInfoLabel = Handle("vector<PileupSummaryInfo>"),("addPileupInfo")
puSummaryInfo,puSummaryInfoLabel = Handle("vector<PileupSummaryInfo>"),("mixData")

from math import hypot, pi

def deltaPhi(phi1,phi2):
    ## Catch if being called with two objects                                                                                                                                             
    if type(phi1) != float and type(phi1) != int:
        phi1 = phi1.phi
    if type(phi2) != float and type(phi2) != int:
        phi2 = phi2.phi
    ## Otherwise                                                                                                                                                                          
    dphi = (phi1-phi2)
    while dphi >  pi: dphi -= 2*pi
    while dphi < -pi: dphi += 2*pi
    return dphi

def deltaR(eta1,phi1,eta2=None,phi2=None):
    ## catch if called with objects                                                                                                                                                       
    if eta2 == None:
        return deltaR(eta1.eta,eta1.phi,phi1.eta,phi1.phi)
    ## otherwise                                                                                                                                                                          
    return hypot(eta1-eta2, deltaPhi(phi1,phi2))

# loop over events
count= 0
for event in events:

#    if event.eventAuxiliary().luminosityBlock() != 210477: #event 1
#    if event.eventAuxiliary().luminosityBlock() != 27628: #event 2
#    if event.eventAuxiliary().luminosityBlock() != 248202: #event 3
#    if event.eventAuxiliary().luminosityBlock() != 102025: #event 4
#    if event.eventAuxiliary().luminosityBlock() != 101558: #event 5
#    if event.eventAuxiliary().luminosityBlock() != 184736: #event 6
#    if event.eventAuxiliary().luminosityBlock() != 166948: #event 7
#    if event.eventAuxiliary().luminosityBlock() != 127833: #event 8
#    if event.eventAuxiliary().luminosityBlock() != 100386: #event 9
#    if event.eventAuxiliary().luminosityBlock() != 249031: #event 10
    if event.eventAuxiliary().luminosityBlock() != args.lumi: #event 10
        continue

#    if event.eventAuxiliary().event() != 51776516: #event 1
#    if event.eventAuxiliary().event() != 6796538: #event 2
#    if event.eventAuxiliary().event() != 61049477: #event 3
#    if event.eventAuxiliary().event() != 25099099: #event 4
#    if event.eventAuxiliary().event() != 24983852: #event 5
#    if event.eventAuxiliary().event() != 45437507: #event 6
#    if event.eventAuxiliary().event() != 41062367: #event 7
#    if event.eventAuxiliary().event() != 31446158: #event 8
#    if event.eventAuxiliary().event() != 24694228: #event 9
#    if event.eventAuxiliary().event() != 61254337: #event 10
    if event.eventAuxiliary().event() != args.event: #event 10
        continue

    event.getByLabel(genParticlesLabel, genparticles)

#    event.getByLabel(photonsLabel, photons)
    event.getByLabel(puSummaryInfoLabel, puSummaryInfo)

#    print "len(puSummaryInfo.product()) = "+str(len(puSummaryInfo.product()))

    for pu in puSummaryInfo.product():
        if pu.getBunchCrossing() != 0:
            continue
#        print "len(pu.getPU_EventID()) = "+str(len(pu.getPU_EventID()))
        for eventid in pu.getPU_EventID():
            print str(eventid.run()) + " "+str(eventid.luminosityBlock()) + " " + str(eventid.event())



