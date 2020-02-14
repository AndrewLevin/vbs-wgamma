import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--infile",type=str,help="Input file",required=True)
parser.add_argument("--lumi",type=int,help="Luminosity block number",required=True)
parser.add_argument("--evmin",type=int,help="Event number minimum",required=True)
parser.add_argument("--evmax",type=int,help="Event number maximum",required=True)
parser.add_argument("--phi",type=float,help="Photon phi",required=True)
parser.add_argument("--eta",type=float,help="Photon eta",required=True)

args = parser.parse_args()


import ROOT
import sys
from DataFormats.FWLite import Events, Handle

#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/EEF150FB-C5B1-E611-87B0-FA163EFD20EB.root'])

#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer15GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1_ext1-v1/40007/481E1328-FBD0-E511-97F6-0CC47A4C8E86.root']) #event 1
#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer15GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1_ext1-v1/00004/32DFB77B-B2D0-E511-BFC4-002590908F8E.root']) #event 2
#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer15GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1_ext1-v1/10001/2824D5DF-73D0-E511-9054-001E67DBE36D.root']) #event 3
#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer15GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1_ext1-v1/80002/5067194F-D2D0-E511-87FD-001C23C105E3.root']) #event 4
#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer15GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1_ext1-v1/10005/B2658B23-E0D0-E511-9A77-00A0D1EE8DA4.root']) #event 5
#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer15GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1_ext1-v1/80001/4E624D45-C3D0-E511-A426-0CC47A4C8E8A.root']) #event 6
#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer15GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1_ext1-v1/00006/B4491CCD-DDD0-E511-9C43-008CFA1C645C.root']) #event 7
#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer15GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1_ext1-v1/40007/C440A553-F4D0-E511-B068-02163E015D6D.root']) #event 8
#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer15GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1_ext1-v1/80002/20888B7F-D5D0-E511-AC8D-002618943913.root']) #event 9
#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer15GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1_ext1-v1/60002/6AD4B8D9-2AD1-E511-8470-44A842B4B3FE.root']) #event 10
events = Events ([args.infile])

#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v2/70001/901B42AA-D229-E711-AD84-A4BF0101202F.root']) 

#events = Events (['/afs/cern.ch/work/a/amlevin/wjets_prod/CMSSW_8_0_21/src/SMP-RunIISummer16DR80Premix-00199.root']) 

genparticles, genParticlesLabel = Handle("vector<reco::GenParticle>"), "genParticles"

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


#    if not ((event.eventAuxiliary().luminosityBlock() == 983395 and event.eventAuxiliary().event() in range(193939363,193939365+1)) or  (event.eventAuxiliary().luminosityBlock() == 983394 and event.eventAuxiliary().event() in range(193939328,193939362+1))):
#    if not (event.eventAuxiliary().luminosityBlock() == 1813624 and event.eventAuxiliary().event() in range(357672540,357672565+1)): #event 1
#    if not (event.eventAuxiliary().luminosityBlock() == 1679141 and event.eventAuxiliary().event() in range(331150584,331150611+1)): #event 2
#    if not (event.eventAuxiliary().luminosityBlock() == 471587 and event.eventAuxiliary().event() in range(93003611,93003638+1)): #event 3
#    if not (event.eventAuxiliary().luminosityBlock() == 2203812 and event.eventAuxiliary().event() in range(434623122,434623146+1)): #event 4
#    if not (event.eventAuxiliary().luminosityBlock() ==  2622795 and event.eventAuxiliary().event() in range(517252552,517252579+1)): #event 5
#    if not (event.eventAuxiliary().luminosityBlock() ==  2271173 and event.eventAuxiliary().event() in range(447907660,447907687+1)): #event 6
#    if not (event.eventAuxiliary().luminosityBlock() == 1919870 and event.eventAuxiliary().event() in range(378625679,378625701+1)): #event 7
#    if not (event.eventAuxiliary().luminosityBlock() == 950990 and event.eventAuxiliary().event() in range(187548794,187548822+1)): #event 8
#    if not (event.eventAuxiliary().luminosityBlock() == 2188278 and event.eventAuxiliary().event() in range(431559691,431559705+1)) or (event.eventAuxiliary().luminosityBlock() == 2188279 and event.eventAuxiliary().event() in range(431559706,431559706+1)): #event 9
#    if not (event.eventAuxiliary().luminosityBlock() == 2503143 and event.eventAuxiliary().event() in range(493655487,493655512+1)): #event 10
    if not (event.eventAuxiliary().luminosityBlock() == args.lumi and event.eventAuxiliary().event() in range(args.evmin,args.evmax+1)): 
        continue

#    if event.eventAuxiliary().event() != 193939338:
#        continue


    print event.eventAuxiliary().event()


    event.getByLabel(genParticlesLabel, genparticles)

    print "genparticles:"
    print ""

    for genparticle in genparticles.product():

        if genparticle.status() != 1:
            continue

#        dr_genpart_photon = deltaR(genparticle.eta(),genparticle.phi(),-1.254150,0.8995361) #event 1
#        dr_genpart_photon = deltaR(genparticle.eta(),genparticle.phi(),-2.151367,1.0310058) #event 2
#        dr_genpart_photon = deltaR(genparticle.eta(),genparticle.phi(),-0.971679,-1.743652) #event 3
#        dr_genpart_photon = deltaR(genparticle.eta(),genparticle.phi(),0.8183593,1.7409668) #event 4
#        dr_genpart_photon = deltaR(genparticle.eta(),genparticle.phi(),0.2225341,2.9409179) #event 5
#        dr_genpart_photon = deltaR(genparticle.eta(),genparticle.phi(),0.5649414,1.5053710) #event 6
#        dr_genpart_photon = deltaR(genparticle.eta(),genparticle.phi(),-0.839843,-1.068847) #event 7
#        dr_genpart_photon = deltaR(genparticle.eta(),genparticle.phi(),-1.595947,3.1020507) #event 8
#        dr_genpart_photon = deltaR(genparticle.eta(),genparticle.phi(),1.5783691,2.3637695) #event 9
#        dr_genpart_photon = deltaR(genparticle.eta(),genparticle.phi(),0.3132934,1.2114257) #event 10
        dr_genpart_photon = deltaR(genparticle.eta(),genparticle.phi(),args.eta,args.phi)

        if dr_genpart_photon > 0.5:
            continue

        
        if genparticle.pt() < 5:
            continue

#        print deltaR(genparticle.eta(),genparticle.phi(),0.126993700862,1.96148002148)

#        if genparticle.numberOfMothers() > 0:
#            print str(genparticle.status())+" "+str(genparticle.pdgId())+" "+str(genparticle.energy())+" "+str(genparticle.pt())+" "+str(genparticle.eta())+" "+str(genparticle.phi())+" "+str(genparticle.mass())+" "+str(genparticle.numberOfMothers())+" "+str(genparticle.mother(0).pdgId())+" "+str(genparticle.mother(0).pt())
#        else:    
#            print str(genparticle.status())+" "+str(genparticle.pdgId())+" "+str(genparticle.energy())+" "+str(genparticle.pt())+" "+str(genparticle.eta())+" "+str(genparticle.phi())+" "+str(genparticle.mass())+" "+str(genparticle.numberOfMothers())
        print str(genparticle.status())+" "+str(genparticle.pdgId())+" "+str(genparticle.pt())+" "+str(dr_genpart_photon)+" "+str(genparticle.mother(0).pdgId())



