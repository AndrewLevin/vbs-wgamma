import ROOT

from math import cos, sqrt

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi

class exampleProducer(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("lepton_pt",  "F");
        self.out.branch("lepton_eta",  "F");
        self.out.branch("is_lepton_tight",  "B");
        self.out.branch("gen_weight",  "F");
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        photons = Collection(event, "Photon")

        tight_muons = []

        loose_but_not_tight_muons = []
        
        tight_electrons = []

        loose_but_not_tight_electrons = []
        
        tight_photons = []

        tight_jets = []

        if not (event.HLT_IsoMu24 or event.HLT_IsoTkMu24):
        #if not (event.HLT_Mu17_TrkIsoVVL):
            return False

        if event.MET_pt > 30:
            return False

        for i in range(0,len(muons)):

            if muons[i].pt < 25:
                continue

            if abs(muons[i].eta) > 2.4:
                continue

            if muons[i].tightId and muons[i].pfRelIso04_all < 0.15:
                tight_muons.append(i)
#            elif muons[i].pfRelIso04_all < 0.4:
            elif muons[i].pfRelIso04_all < 0.25:
                loose_but_not_tight_muons.append(i)

        for i in range (0,len(electrons)):

            if electrons[i].pt < 30:
                continue
            
            if abs(electrons[i].eta+ electrons[i].deltaEtaSC) > 2.5:
                continue

            if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):
                if electrons[i].cutBased >= 3:
                    tight_electrons.append(i)

                elif electrons[i].cutBased >= 1:
                    loose_but_not_tight_electrons.append(i)

        if len(tight_muons)+ len(loose_but_not_tight_muons) != 1:
            return False

        if len(tight_electrons) + len(loose_but_not_tight_electrons) != 0:
            return False

        if len(tight_muons) == 1:
            muon_index = tight_muons[0]
            self.out.fillBranch("is_lepton_tight",1)

        if len(loose_but_not_tight_muons) == 1:
            muon_index = loose_but_not_tight_muons[0]
            self.out.fillBranch("is_lepton_tight",0)

        self.out.fillBranch("lepton_pt",muons[muon_index].pt)
        self.out.fillBranch("lepton_eta",muons[muon_index].eta)

        try:
            self.out.fillBranch("gen_weight",event.Generator_weight)
        except:
            pass

        if sqrt(2*muons[muon_index].pt*event.MET_pt*(1 - cos(event.MET_phi - muons[muon_index].phi))) > 20:
            return False

        found_other_jet = False

        for i in range(0,len(jets)):

            if jets[i].pt < 20:
                continue

            if abs(jets[i].eta) > 4.7:
                continue

            if not jets[i].jetId & (1 << 0):
                continue

            if deltaR(muons[muon_index].eta,muons[muon_index].phi,jets[i].eta,jets[i].phi) > 0.3:
                found_other_jet = True

        if not found_other_jet:
            return False

        return True

exampleModule = lambda : exampleProducer()
