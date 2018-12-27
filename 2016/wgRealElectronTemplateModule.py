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
        self.out.branch("met",  "F");
        self.out.branch("electron_pt",  "F");
        self.out.branch("electron_eta",  "F");
        self.out.branch("gen_weight",  "F");
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        photons = Collection(event, "Photon")
        genparts = Collection(event, "GenPart")

        selected_gen_electrons = []

        selected_electrons = []

        mask1 = (1 << 0) | (1 << 7) | (1 << 8) | (1 << 12) | (1 << 13)
        mask2 = (1 << 0) | (1 << 8) | (1 << 13)

        for i in range(0,len(genparts)):

            #if genparts[i].pdgId == 22:

                #print str(int(genparts[i].statusFlags & (1 << 0) == (1 << 0))) + " " + str(int(genparts[i].statusFlags & (1 << 1) == (1 << 1))) + " " + str(int(genparts[i].statusFlags & (1 << 2) == (1 << 2))) + " " + str(int(genparts[i].statusFlags & (1 << 3) == (1 << 3))) + " " + str(int(genparts[i].statusFlags & (1 << 4) == (1 << 4))) + " " + str(int(genparts[i].statusFlags & (1 << 5) == (1 << 5))) + " " + str(int(genparts[i].statusFlags & (1 << 6) == (1 << 6))) + " " + str(int(genparts[i].statusFlags & (1 << 7) == (1 << 7))) + " " + str(int(genparts[i].statusFlags & (1 << 8) == (1 << 8))) + " " + str(int(genparts[i].statusFlags & (1 << 9) == (1 << 9))) + " " + str(int(genparts[i].statusFlags & (1 << 10) == (1 << 10))) + " " + str(int(genparts[i].statusFlags & (1 << 11) == (1 << 11))) + " " + str(int(genparts[i].statusFlags & (1 << 12) == (1 << 12)))  + " " + str(int(genparts[i].statusFlags & (1 << 13) == (1 << 13))) + " " + str(int(genparts[i].statusFlags & (1 << 14) == (1 << 14)))

            if abs(genparts[i].pdgId) == 11:
                if genparts[i].pdgId == 11 and ((genparts[i].statusFlags & mask1 == mask1) or (genparts[i].statusFlags & mask2 == mask2)):
                    selected_gen_electrons.append(i)

        assert( len(selected_gen_electrons) <= 1)

        if len(selected_gen_electrons) != 1:
            return False

        for i in range (0,len(electrons)):

            if electrons[i].pt/electrons[i].eCorr < 20:
                continue
            
            if abs(electrons[i].eta+electrons[i].deltaEtaSC) > 2.5:
                continue

            if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):

                if electrons[i].cutBased == 0:
                    continue

                if deltaR(genparts[selected_gen_electrons[0]].eta,genparts[selected_gen_electrons[0]].phi,electrons[i].eta,electrons[i].phi) > 0.1:
                    continue

                selected_electrons.append(i)

        if len(selected_electrons) != 1:
            return False

        self.out.fillBranch("met",event.MET_pt)
        self.out.fillBranch("electron_pt",electrons[selected_electrons[0]].pt)
        self.out.fillBranch("electron_eta",electrons[selected_electrons[0]].eta)

        try:
            self.out.fillBranch("gen_weight",event.Generator_weight)
        except:
            pass

        return True

exampleModule = lambda : exampleProducer()
