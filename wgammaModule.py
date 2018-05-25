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
        self.out.branch("lepton_pdg_id",  "I");
        self.out.branch("lepton_pt",  "F");
        self.out.branch("lepton_eta",  "F");
        self.out.branch("photon_pt",  "F")
        self.out.branch("photon_eta",  "F");
        self.out.branch("photon_selection",  "I");
        self.out.branch("met",  "F");
        self.out.branch("mjj","F")
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

        for i in range(0,len(muons)):

            if muons[i].pt < 25:
                continue

            if abs(muons[i].eta) > 2.4:
                continue

            if muons[i].tightId and muons[i].pfRelIso04_all < 0.15:
                tight_muons.append(i)
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

        for i in range (0,len(photons)):

            if photons[i].pt/photons[i].eCorr < 20:
                continue

            #if not ((abs(photons[i].eta) < 1.4442) or (1.566 < abs(photons[i].eta) and abs(photons[i].eta) < 2.5) ):
            if not ((abs(photons[i].eta) < 1.4442) or (1.566 < abs(photons[i].eta) and abs(photons[i].eta) < 2.5) ):
                continue

            mask1 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) | (1 << 13)
            mask2 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) 
            mask3 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) |  (1 << 13)
            mask4 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 11) | (1 << 13)
            mask5 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 9) | (1 << 11) | (1 << 13) #invert the medium photon ID with the sigma_ietaieta cut removed

            bitmap = photons[i].vidNestedWPBitmap & mask1

            if not((bitmap == mask1) or (bitmap == mask2) or (bitmap == mask3) or (bitmap == mask4) or (bitmap == mask5)):
                continue

            #if photons[i].cutBased == 0 or photons[i].cutBased == 1:
            #    continue

            if not photons[i].electronVeto:
                continue

            pass_lepton_dr_cut = True

            for j in range(0,len(tight_muons)):
                if deltaR(muons[tight_muons[j]].eta,muons[tight_muons[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False

            for j in range(0,len(tight_electrons)):

                if deltaR(electrons[tight_electrons[j]].eta,electrons[tight_electrons[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False

            if not pass_lepton_dr_cut:
                continue

            tight_photons.append(i)

        if len(tight_photons) == 0:
            return False

        for i in range(0,len(jets)):

            if jets[i].pt < 30:
                continue

            if abs(jets[i].eta) > 4.7:
                continue

            if not jets[i].jetId & (1 << 0):
                continue

            #pass_photon_dr_cut = True

            #for j in range(0,len(tight_photons)):

            #    print "deltaR(photons[tight_photons[j]].eta,photons[tight_photons[j]].phi,jets[i].eta,jets[i].phi) = " + str(deltaR(photons[tight_photons[j]].eta,photons[tight_photons[j]].phi,jets[i].eta,jets[i].phi))
                
            #    if deltaR(photons[tight_photons[j]].eta,photons[tight_photons[j]].phi,jets[i].eta,jets[i].phi) < 0.5:
            #        pass_photon_dr_cut = False

            #if not pass_photon_dr_cut:
            #    continue

            if deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,jets[i].eta,jets[i].phi) < 0.5:
                continue

            pass_lepton_dr_cut = True

            for j in range(0,len(tight_muons)):

                if deltaR(muons[tight_muons[j]].eta,muons[tight_muons[j]].phi,jets[i].eta,jets[i].phi) < 0.5:
                    pass_lepton_dr_cut = False

            for j in range(0,len(tight_electrons)):
                
                if deltaR(electrons[tight_electrons[j]].eta,electrons[tight_electrons[j]].phi,jets[i].eta,jets[i].phi) < 0.5:

                    pass_lepton_dr_cut = False

            for j in range(0,len(loose_but_not_tight_muons)):

                if deltaR(muons[loose_but_not_tight_muons[j]].eta,muons[loose_but_not_tight_muons[j]].phi,jets[i].eta,jets[i].phi) < 0.5:

                    pass_lepton_dr_cut = False

            for j in range(0,len(loose_but_not_tight_electrons)):

                if deltaR(electrons[loose_but_not_tight_electrons[j]].eta,electrons[loose_but_not_tight_electrons[j]].phi,jets[i].eta,jets[i].phi) < 0.5:

                     pass_lepton_dr_cut = False

            if not pass_lepton_dr_cut:
                continue

            tight_jets.append(i)

        if len(tight_jets) < 2:
            return False

        if jets[tight_jets[0]].btagCSVV2 > 0.8484:
            return False

        if jets[tight_jets[1]].btagCSVV2 > 0.8484:
            return False

        if jets[tight_jets[0]].pt < 40:
            return False

        if jets[tight_jets[1]].pt < 30:
            return False

        if abs(jets[tight_jets[0]].eta) > 4.7:
            return False

        if abs(jets[tight_jets[1]].eta) > 4.7:
            return False

        if (jets[tight_jets[0]].p4() + jets[tight_jets[1]].p4()).M() < 200:
            return False

        #if abs(jets[0].p4().Eta() - jets[1].p4().Eta()) < 2.5:
        #    return False

        if photons[tight_photons[0]].pt/photons[tight_photons[0]].eCorr < 20:
            return False

        #if not (abs(photons[tight_photons[0]].eta) < 1.4442):
        #if not (abs(photons[tight_photons[0]].eta) < 1.4442):
        #    return False        

        if not ((abs(photons[tight_photons[0]].eta) < 1.4442) or (1.566 < abs(photons[tight_photons[0]].eta) and abs(photons[tight_photons[0]].eta) < 2.5) ):
            return False        

        if deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,jets[tight_jets[0]].eta,jets[tight_jets[0]].phi) < 0.5:
            return False

        if deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,jets[tight_jets[1]].eta,jets[tight_jets[1]].phi) < 0.5:
            return False

        if deltaR(jets[tight_jets[0]].eta,jets[tight_jets[0]].phi,jets[tight_jets[1]].eta,jets[tight_jets[1]].phi) < 0.5:
            return False

        #if photons[tight_photons[0]].cutBased == 0 or photons[tight_photons[0]].cutBased == 1:
        #    return False

        if not photons[tight_photons[0]].electronVeto:
            return False

        if event.MET_pt < 35:
            return False

        if abs(deltaPhi(event.MET_phi,jets[tight_jets[0]].phi)) < 0.4:
            return False

        if abs(deltaPhi(event.MET_phi,jets[tight_jets[1]].phi)) < 0.4:
            return False

        if len(tight_muons) +len(loose_but_not_tight_muons) +  len(tight_electrons) + len(loose_but_not_tight_electrons) > 1:
            return False

        if len(tight_muons) == 1:

            if not (event.HLT_IsoMu24 or event.HLT_IsoTkMu24):
                return False
        
            if deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,muons[tight_muons[0]].eta,muons[tight_muons[0]].phi) < 0.5:
                return False

            if muons[tight_muons[0]].pt < 25:
                return False

            if abs(muons[tight_muons[0]].eta) > 2.4:
                return False

            if muons[tight_muons[0]].pfRelIso04_all > 0.15:
                return False

            if not muons[tight_muons[0]].tightId:
                return False

            if sqrt(2*muons[tight_muons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - muons[tight_muons[0]].phi))) < 30:
                return False

            print "selected muon event: " + str(event.event) + " " + str(event.luminosityBlock) + " " + str(event.run)
            
            mask1 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) | (1 << 13)
            mask2 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) 
            mask3 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) |  (1 << 13)
            mask4 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 11) | (1 << 13)
            mask5 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 9) | (1 << 11) | (1 << 13) #invert the medium photon ID with the sigma_ietaieta cut removed

            bitmap = photons[tight_photons[0]].vidNestedWPBitmap & mask1

            if (bitmap == mask1):
                self.out.fillBranch("photon_selection",2)
            elif (bitmap == mask5):
                self.out.fillBranch("photon_selection",1)
            elif (bitmap == mask2) or (bitmap == mask3) or (bitmap == mask4):
                self.out.fillBranch("photon_selection",0)
            else:
                assert(0)

            self.out.fillBranch("lepton_pdg_id",13)
            self.out.fillBranch("lepton_pt",muons[tight_muons[0]].pt)
            self.out.fillBranch("lepton_eta",muons[tight_muons[0]].eta)
            self.out.fillBranch("met",event.MET_pt)
            self.out.fillBranch("photon_pt",photons[tight_photons[0]].pt/photons[tight_photons[0]].eCorr)
            self.out.fillBranch("photon_eta",photons[tight_photons[0]].eta)
            self.out.fillBranch("mjj",(jets[tight_jets[0]].p4() + jets[tight_jets[1]].p4()).M())
            self.out.fillBranch("is_lepton_tight",1)

        elif len(loose_but_not_tight_muons) == 1:

            if not (event.HLT_IsoMu24 or event.HLT_IsoTkMu24):
                return False
        
            if deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,muons[loose_but_not_tight_muons[0]].eta,muons[loose_but_not_tight_muons[0]].phi) < 0.5:
                return False

            if muons[loose_but_not_tight_muons[0]].pt < 25:
                return False

            if abs(muons[loose_but_not_tight_muons[0]].eta) > 2.4:
                return False

            if sqrt(2*muons[loose_but_not_tight_muons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - muons[loose_but_not_tight_muons[0]].phi))) < 30:
                return False

            mask1 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) | (1 << 13)
            mask2 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) 
            mask3 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) |  (1 << 13)
            mask4 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 11) | (1 << 13)
            mask5 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 9) | (1 << 11) | (1 << 13) #invert the medium photon ID with the sigma_ietaieta cut removed

            bitmap = photons[tight_photons[0]].vidNestedWPBitmap & mask1

            if (bitmap == mask1):
                self.out.fillBranch("photon_selection",2)
            elif (bitmap == mask5):
                self.out.fillBranch("photon_selection",1)
            elif (bitmap == mask2) or (bitmap == mask3) or (bitmap == mask4):
                self.out.fillBranch("photon_selection",0)
            else:
                assert(0)

            self.out.fillBranch("lepton_pdg_id",13)
            self.out.fillBranch("lepton_pt",muons[loose_but_not_tight_muons[0]].pt)
            self.out.fillBranch("lepton_eta",muons[loose_but_not_tight_muons[0]].eta)
            self.out.fillBranch("met",event.MET_pt)
            self.out.fillBranch("photon_pt",photons[tight_photons[0]].pt/photons[tight_photons[0]].eCorr)
            self.out.fillBranch("photon_eta",photons[tight_photons[0]].eta)
            self.out.fillBranch("mjj",(jets[tight_jets[0]].p4() + jets[tight_jets[1]].p4()).M())
            self.out.fillBranch("is_lepton_tight",0)

        elif len(tight_electrons) == 1:

            if not event.HLT_Ele27_WPTight_Gsf:
                return False

            if electrons[tight_electrons[0]].cutBased == 0 or electrons[tight_electrons[0]].cutBased == 1:
                return False

            if deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,electrons[tight_electrons[0]].eta,electrons[tight_electrons[0]].phi) < 0.5:
                return False

            if electrons[tight_electrons[0]].pt < 30:
                return False

            if abs(electrons[tight_electrons[0]].eta) > 2.4:
                return False

            if (electrons[tight_electrons[0]].p4() + photons[tight_photons[0]].p4()).M() > 82 and (electrons[tight_electrons[0]].p4() + photons[tight_photons[0]].p4()).M() < 102:
                return False

            if sqrt(2*electrons[tight_electrons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - electrons[tight_electrons[0]].phi))) < 30:
                return False

            mask1 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) | (1 << 13)
            mask2 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) 
            mask3 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) |  (1 << 13)
            mask4 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 11) | (1 << 13)
            mask5 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 9) | (1 << 11) | (1 << 13) #invert the medium photon ID with the sigma_ietaieta cut removed

            bitmap = photons[tight_photons[0]].vidNestedWPBitmap & mask1

            if (bitmap == mask1):
                self.out.fillBranch("photon_selection",2)
            elif (bitmap == mask5):
                self.out.fillBranch("photon_selection",1)
            elif (bitmap == mask2) or (bitmap == mask3) or (bitmap == mask4):
                self.out.fillBranch("photon_selection",0)
            else:
                assert(0)

            self.out.fillBranch("lepton_pdg_id",11)
            self.out.fillBranch("lepton_pt",electrons[tight_electrons[0]].pt)
            self.out.fillBranch("lepton_eta",electrons[tight_electrons[0]].eta)
            self.out.fillBranch("met",event.MET_pt)
            self.out.fillBranch("photon_pt",photons[tight_photons[0]].pt/photons[tight_photons[0]].eCorr)
            self.out.fillBranch("photon_eta",photons[tight_photons[0]].eta)
            self.out.fillBranch("mjj",(jets[tight_jets[0]].p4() + jets[tight_jets[1]].p4()).M())
            self.out.fillBranch("is_lepton_tight",1)

            print "selected electron event: " + str(event.event) + " " + str(event.luminosityBlock) + " " + str(event.run)

        elif len(loose_but_not_tight_electrons) == 1:

            if not event.HLT_Ele27_WPTight_Gsf:
                return False

            if deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,electrons[loose_but_not_tight_electrons[0]].eta,electrons[loose_but_not_tight_electrons[0]].phi) < 0.5:
                return False

            if electrons[loose_but_not_tight_electrons[0]].pt < 30:
                return False

            if abs(electrons[loose_but_not_tight_electrons[0]].eta) > 2.4:
                return False

            if (electrons[loose_but_not_tight_electrons[0]].p4() + photons[tight_photons[0]].p4()).M() > 82 and (electrons[loose_but_not_tight_electrons[0]].p4() + photons[tight_photons[0]].p4()).M() < 102:
                return False

            if sqrt(2*electrons[loose_but_not_tight_electrons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - electrons[loose_but_not_tight_electrons[0]].phi))) < 30:
                return False

            mask1 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) | (1 << 13)
            mask2 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) 
            mask3 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) |  (1 << 13)
            mask4 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 11) | (1 << 13)
            mask5 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 9) | (1 << 11) | (1 << 13) #invert the medium photon ID with the sigma_ietaieta cut removed

            bitmap = photons[tight_photons[0]].vidNestedWPBitmap & mask1

            if (bitmap == mask1):
                self.out.fillBranch("photon_selection",2)
            elif (bitmap == mask5):
                self.out.fillBranch("photon_selection",1)
            elif (bitmap == mask2) or (bitmap == mask3) or (bitmap == mask4):
                self.out.fillBranch("photon_selection",0)
            else:
                assert(0)

            self.out.fillBranch("lepton_pdg_id",11)
            self.out.fillBranch("lepton_pt",electrons[loose_but_not_tight_electrons[0]].pt)
            self.out.fillBranch("lepton_eta",electrons[loose_but_not_tight_electrons[0]].eta)
            self.out.fillBranch("met",event.MET_pt)
            self.out.fillBranch("photon_pt",photons[tight_photons[0]].pt/photons[tight_photons[0]].eCorr)
            self.out.fillBranch("photon_eta",photons[tight_photons[0]].eta)
            self.out.fillBranch("mjj",(jets[tight_jets[0]].p4() + jets[tight_jets[1]].p4()).M())
            self.out.fillBranch("is_lepton_tight",0)

        else:
            return False


        try:
            self.out.fillBranch("gen_weight",event.Generator_weight)
        except:
            pass

        #print event.event


        #self.out.fillBranch("EventMass",eventSum.M())
        #if eventSum.M() < 2000:
        #    return False
        #else:
        #    return True

        return True

exampleModule = lambda : exampleProducer()
