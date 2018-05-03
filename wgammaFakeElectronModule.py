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

        if not (event.HLT_Ele27_WPTight_Gsf):
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

            if electrons[i].pt/electrons[i].eCorr < 30:
                continue
            
            if abs(electrons[i].eta) > 2.5:
                continue

            if electrons[i].cutBased >= 3:
                tight_electrons.append(i)

            elif electrons[i].cutBased >= 1:
                loose_but_not_tight_electrons.append(i)

        if len(tight_muons)+ len(loose_but_not_tight_muons) != 0:
            return False

        if len(tight_electrons) + len(loose_but_not_tight_electrons) != 1:
            return False

        if len(tight_electrons) == 1:
            electron_index = tight_electrons[0]
            self.out.fillBranch("is_lepton_tight",1)

        if len(loose_but_not_tight_electrons) == 1:
            electron_index = loose_but_not_tight_electrons[0]
            self.out.fillBranch("is_lepton_tight",0)

        self.out.fillBranch("lepton_pt",electrons[electron_index].pt)
        self.out.fillBranch("lepton_eta",electrons[electron_index].eta)

        try:
            self.out.fillBranch("gen_weight",event.Generator_weight)
        except:
            pass

        if sqrt(2*electrons[electron_index].pt*event.MET_pt*(1 - cos(event.MET_phi - electrons[electron_index].phi))) > 20:
            return False

        found_other_jet = False

        for i in range(0,len(jets)):

            if jets[i].pt < 30:
                continue

            if abs(jets[i].eta) > 4.7:
                continue

            if not jets[i].jetId & (1 << 0):
                continue

            if deltaR(electrons[electron_index].eta,electrons[electron_index].phi,jets[i].eta,jets[i].phi) < 0.3:
                found_other_jet = True

        if not found_other_jet:
            return False

        return True

exampleModule = lambda : exampleProducer()
