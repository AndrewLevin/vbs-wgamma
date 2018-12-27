import ROOT
import sys
from DataFormats.FWLite import Events, Handle

events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/023963AD-CBBE-E611-AC12-D4AE526A048B.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/04444FF8-C3BE-E611-828A-0CC47A7D9966.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/049966D9-E9BE-E611-A935-70106F49CBD8.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/04CD3B59-D4BE-E611-A74B-00266CF3E0A4.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/061311C1-DBBE-E611-A958-002590AC4C49.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/066A6CA6-9EBE-E611-AD42-0CC47A7EED28.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/06754142-C3BE-E611-85E9-E41D2D08DFF0.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/0817EA07-43BE-E611-A42D-0CC47A4C8E1C.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/08A5BC66-C4BE-E611-821A-0025904C7DF0.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/08B98FD8-43BE-E611-A30C-0025905A6122.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/0A1C63F2-BEBE-E611-9824-002590DE6E1E.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/0A4C8E1D-D9BE-E611-9F24-70106F4A9248.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/0A5F3498-DCBE-E611-A198-0CC47A7E6A12.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/0C22CB5C-DABE-E611-88C0-70106F4A9254.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/0E289455-CFBE-E611-82FB-00266CF94C44.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/0E560383-8CBE-E611-9A71-E41D2D08DE80.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/0EE24920-08BF-E611-9F5F-0CC47A706CDE.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/10525C41-C7BE-E611-8EE7-0CC47A7FC434.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/106B0231-D1BF-E611-A0B6-0CC47AC08BD4.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/10937B34-42BE-E611-9998-0CC47A4C8E2A.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/10F26366-13BF-E611-8118-0025905A60F8.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/1440B6D0-E6BE-E611-99D1-0CC47A7E6A12.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/18689589-CDBE-E611-ABBE-047D7BD6DED2.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/18850323-40BE-E611-A006-0CC47A78A41C.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/1A71C143-C3BE-E611-AB77-842B2B766242.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/1AD21C58-DEBE-E611-8207-70106F4D23D0.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/1AFA7EB2-D1BE-E611-8871-70106F4A91C8.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/1C3D64FD-D4BE-E611-B91A-047D7B881D26.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/1CC56E02-C5BE-E611-844D-1CC1DE192734.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/1CE37D2E-44BE-E611-969F-0CC47A4D764A.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/1E7C3C40-D8BE-E611-A6FA-0CC47A7EEE48.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/1E9B03EE-E4BE-E611-BFEC-002590AC5012.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/1EA07CA3-DEBE-E611-A3D3-70106F4A9254.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/1EE7FDFF-CDBE-E611-B4E4-1CC1DE18CFF0.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/206A8159-85BE-E611-9FE3-0CC47A7E6A60.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/223544AB-44BE-E611-B302-0CC47A4D7604.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/2271D6E6-DFBE-E611-9F8B-0CC47A7FC72A.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/22B6134F-C3BE-E611-9655-3417EBE7063F.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/2459CE58-E6BE-E611-BE2E-047D7BD6DED2.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/24942410-CBBE-E611-9B5F-70106F4D2378.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/24D16BC3-C0BE-E611-B41B-1CC1DE18CFF0.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/267A34FE-C6BE-E611-814E-0CC47A7EED28.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/281DCFA4-03BF-E611-A114-0CC47A706CDE.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/28E0870B-C7BE-E611-98EB-00266CF3E3C4.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/2A7CB314-BDBE-E611-AF9A-0CC47A7EEF1A.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/2AB37455-48BE-E611-B9B4-0025905A60CE.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/2ADFBDC1-43BE-E611-9793-0CC47A7C34A6.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/2AEA4694-41BE-E611-A58D-0025905A6122.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/2C4C28BF-11BF-E611-89EF-0CC47A703326.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/2E012977-93BE-E611-8469-0CC47A7EED28.root'])

genparticles, genParticlesLabel = Handle("vector<reco::GenParticle>"), "genParticles"
photons, photonsLabel = Handle("vector<reco::Photon>"), "gedPhotons"

from math import hypot, pi
def deltaR(a,b):
    dphi = abs(a.phi()-b.phi());
    if dphi > pi: dphi = 2*pi-dphi
    return hypot(a.eta()-b.eta(),dphi)

f=ROOT.TFile("delete_this.root","recreate")

sieie_th1f_1=ROOT.TH1F("sieie_1","sieie_1",100,0,0.05)
sieie_th1f_2=ROOT.TH1F("sieie_2","sieie_2",100,0,0.05)
sieie_th1f_3=ROOT.TH1F("sieie_3","sieie_3",100,0,0.05)
sieie_th1f_4=ROOT.TH1F("sieie_4","sieie_4",100,0,0.05)
sieie_th1f_5=ROOT.TH1F("sieie_5","sieie_5",100,0,0.05)
sieie_th1f_6=ROOT.TH1F("sieie_6","sieie_6",100,0,0.05)
sieie_th1f_7=ROOT.TH1F("sieie_7","sieie_7",100,0,0.05)
sieie_th1f_8=ROOT.TH1F("sieie_8","sieie_8",100,0,0.05)
sieie_th1f_9=ROOT.TH1F("sieie_9","sieie_9",100,0,0.05)
sieie_th1f_10=ROOT.TH1F("sieie_10","sieie_10",100,0,0.05)

n_events_processed = 0

for event in events:

    n_events_processed = n_events_processed + 1

    if n_events_processed %  1000 == 0:
        print n_events_processed

    event.getByLabel(genParticlesLabel, genparticles)
    event.getByLabel(photonsLabel, photons)

    for photon in photons.product():

        if not (photon.pt() > 20 and abs(photon.superCluster().eta()) < 1.4442):
            continue

        n_matching_etas = 0

        for genparticle in genparticles.product():
            if genparticle.pdgId() == 223 and deltaR(photon,genparticle) < 0.2 and genparticle.pt() > 5:
                n_matching_etas += 1

        n_matching_neutral_pions = 0

        for genparticle in genparticles.product():
            if genparticle.pdgId() == 111 and deltaR(photon,genparticle) < 0.2 and genparticle.pt() > 5:
                n_matching_neutral_pions += 1

        n_matching_photons = 0

        for genparticle in genparticles.product():
            if genparticle.pdgId() == 22 and deltaR(photon,genparticle) < 0.2 and genparticle.pt() > 5:
                n_matching_photons+=1

        if n_matching_photons == 0:
            sieie_th1f_1.Fill(photon.full5x5_sigmaIetaIeta())
        if n_matching_photons == 1:
            sieie_th1f_2.Fill(photon.full5x5_sigmaIetaIeta())
        if n_matching_photons == 2:
            sieie_th1f_3.Fill(photon.full5x5_sigmaIetaIeta())
        if n_matching_photons == 3:
            sieie_th1f_4.Fill(photon.full5x5_sigmaIetaIeta())
        if n_matching_photons == 4:
            sieie_th1f_5.Fill(photon.full5x5_sigmaIetaIeta())
        if n_matching_neutral_pions == 0:
            sieie_th1f_6.Fill(photon.full5x5_sigmaIetaIeta())
        if n_matching_neutral_pions == 1:
            sieie_th1f_7.Fill(photon.full5x5_sigmaIetaIeta())
        if n_matching_neutral_pions == 2:
            sieie_th1f_8.Fill(photon.full5x5_sigmaIetaIeta())
        if n_matching_neutral_pions == 3:
            sieie_th1f_9.Fill(photon.full5x5_sigmaIetaIeta())
        if n_matching_neutral_pions == 4:
            sieie_th1f_10.Fill(photon.full5x5_sigmaIetaIeta())

f.cd()

sieie_th1f_1.Write()
sieie_th1f_2.Write()
sieie_th1f_3.Write()
sieie_th1f_4.Write()
sieie_th1f_5.Write()
sieie_th1f_6.Write()
sieie_th1f_7.Write()
sieie_th1f_8.Write()
sieie_th1f_9.Write()
sieie_th1f_10.Write()
