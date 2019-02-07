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
        self.out.branch("run",  "i");
        self.out.branch("lumi",  "i");
        self.out.branch("event",  "l");
        self.out.branch("npu",  "I");
        self.out.branch("ntruepu",  "F");
        self.out.branch("lepton_pdg_id",  "I");
        self.out.branch("lepton_pt",  "F");
        self.out.branch("lepton_phi",  "F");
        self.out.branch("lepton_eta",  "F");
        self.out.branch("photon_pt",  "F");
        self.out.branch("photon_phi",  "F");
        self.out.branch("photon_eta",  "F");
        self.out.branch("mlg",  "F");
        self.out.branch("photon_selection",  "I");
        self.out.branch("btagging_selection",  "I");
        self.out.branch("met",  "F");
        self.out.branch("mt",  "F");
        self.out.branch("mjj","F")
        self.out.branch("npvs","I")
        self.out.branch("njets","I")
        self.out.branch("is_lepton_tight",  "B");
        self.out.branch("gen_weight",  "F");
        self.out.branch("is_lepton_real",  "B");
        self.out.branch("lhe_lepton_charge",  "B");
        self.out.branch("photon_gen_matching",  "I");
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        photons = Collection(event, "Photon")

        try:
            genparts = Collection(event, "GenPart")
            lheparts = Collection(event, "LHEPart")
        except:
            
            pass
            

        tight_muons = []

        loose_but_not_tight_muons = []
        
        tight_electrons = []

        loose_but_not_tight_electrons = []
        
        tight_photons = []

        for i in range(0,len(muons)):

            if muons[i].pt < 20:
                continue

            if abs(muons[i].eta) > 2.4:
                continue

            if muons[i].tightId and muons[i].pfRelIso04_all < 0.15:
                tight_muons.append(i)
            elif muons[i].pfRelIso04_all < 0.25:
                loose_but_not_tight_muons.append(i)

        for i in range (0,len(electrons)):

            if electrons[i].pt < 20:
                continue
            
            if abs(electrons[i].eta + electrons[i].deltaEtaSC) > 2.5:
                continue

            if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):
                if electrons[i].cutBased >= 3:
                    tight_electrons.append(i)

                elif electrons[i].cutBased >= 1:
                    loose_but_not_tight_electrons.append(i)

        for i in range (0,len(photons)):

            if photons[i].pt < 20:
                continue

            #if not ((abs(photons[i].eta) < 1.4442) or (1.566 < abs(photons[i].eta) and abs(photons[i].eta) < 2.5) ):
            if not ((abs(photons[i].eta) < 1.4442) or (1.566 < abs(photons[i].eta) and abs(photons[i].eta) < 2.5) ):
                continue

            mask1 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) | (1 << 6)
            mask2 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) 
            mask3 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 6)
            mask4 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 5) | (1 << 6)
            mask5 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 4) | (1 << 5) | (1 << 6) #invert the medium photon ID with the sigma_ietaieta cut removed

            bitmap = photons[i].vidNestedWPBitmap & mask1

            #first add the photons that pass the full ID
            if not (bitmap == mask1):
                continue

            if not((bitmap == mask1) or (bitmap == mask2) or (bitmap == mask3) or (bitmap == mask4) or (bitmap == mask5)):
                continue

            #if photons[i].cutBased == 0 or photons[i].cutBased == 1:
            #    continue

#            if not photons[i].electronVeto:
#                continue

            if photons[i].pixelSeed:
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

        for i in range (0,len(photons)):


            if photons[i].pt < 20:
                continue

            #if not ((abs(photons[i].eta) < 1.4442) or (1.566 < abs(photons[i].eta) and abs(photons[i].eta) < 2.5) ):
            if not ((abs(photons[i].eta) < 1.4442) or (1.566 < abs(photons[i].eta) and abs(photons[i].eta) < 2.5) ):
                continue

            mask1 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) | (1 << 6)
            mask2 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) 
            mask3 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 6)
            mask4 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 5) | (1 << 6)
            mask5 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 4) | (1 << 5) | (1 << 6) #invert the medium photon ID with the sigma_ietaieta cut removed

            bitmap = photons[i].vidNestedWPBitmap & mask1

            #after adding the photons that pass the full ID, add the photons that pass the inverted ID
            if (bitmap == mask1):
                continue

            if not((bitmap == mask1) or (bitmap == mask2) or (bitmap == mask3) or (bitmap == mask4) or (bitmap == mask5)):
                continue

            #if photons[i].cutBased == 0 or photons[i].cutBased == 1:
            #    continue

#            if not photons[i].electronVeto:
#                continue

            if photons[i].pixelSeed:
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

        njets = 0

        for i in range(0,len(jets)):

            if jets[i].pt < 40:
                continue

            if abs(jets[i].eta) > 4.7:
                continue

#            if not jets[i].jetId & (1 << 0):
#                continue

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

            njets+=1


        if photons[tight_photons[0]].pt < 20:
            return False

        #if not (abs(photons[tight_photons[0]].eta) < 1.4442):
        #if not (abs(photons[tight_photons[0]].eta) < 1.4442):
        #    return False        

        if not ((abs(photons[tight_photons[0]].eta) < 1.4442) or (1.566 < abs(photons[tight_photons[0]].eta) and abs(photons[tight_photons[0]].eta) < 2.5) ):
            return False        

        #if photons[tight_photons[0]].cutBased == 0 or photons[tight_photons[0]].cutBased == 1:
        #    return False

#        if not photons[tight_photons[0]].electronVeto:
#            return False

        if photons[tight_photons[0]].pixelSeed:
            return False

        #if event.MET_pt < 35:
        #    return False

        if len(tight_muons) + len(loose_but_not_tight_muons) +  len(tight_electrons) + len(loose_but_not_tight_electrons) > 1:
            return False

        isprompt_mask = (1 << 0) #isPrompt
        isprompttaudecayproduct_mask = (1 << 4) #isPromptTauDecayProduct


        is_lepton_real=0


        if len(tight_muons) == 1:

            try:

                for i in range(0,len(genparts)):
                    if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 13 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct_mask == isprompttaudecayproduct_mask)) and deltaR(muons[tight_muons[0]].eta,muons[tight_muons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        is_lepton_real=1

            except:
                pass

            if not event.HLT_IsoMu24:
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

            #if sqrt(2*muons[tight_muons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - muons[tight_muons[0]].phi))) < 30:
            #    return False

            self.out.fillBranch("mt",sqrt(2*muons[tight_muons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - muons[tight_muons[0]].phi))))

            print "selected muon event: " + str(event.event) + " " + str(event.luminosityBlock) + " " + str(event.run)
            
            mask1 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) | (1 << 6)
            mask2 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) 
            mask3 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 6)
            mask4 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 5) | (1 << 6)
            mask5 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 4) | (1 << 5) | (1 << 6) #invert the medium photon ID with the sigma_ietaieta cut removed

            bitmap = photons[tight_photons[0]].vidNestedWPBitmap & mask1

            if (bitmap == mask1):
                self.out.fillBranch("photon_selection",2)
            elif (bitmap == mask5):
                self.out.fillBranch("photon_selection",1)
            elif (bitmap == mask2) or (bitmap == mask3) or (bitmap == mask4):
                self.out.fillBranch("photon_selection",0)
            else:
                assert(0)

            self.out.fillBranch("is_lepton_real",is_lepton_real)
            self.out.fillBranch("lepton_pdg_id",13)
            self.out.fillBranch("lepton_pt",muons[tight_muons[0]].pt)
            self.out.fillBranch("lepton_eta",muons[tight_muons[0]].eta)
            self.out.fillBranch("lepton_phi",muons[tight_muons[0]].phi)
            self.out.fillBranch("met",event.MET_pt)
            self.out.fillBranch("photon_pt",photons[tight_photons[0]].pt)
            self.out.fillBranch("photon_eta",photons[tight_photons[0]].eta)
            self.out.fillBranch("photon_phi",photons[tight_photons[0]].phi)
            self.out.fillBranch("mlg",(muons[tight_muons[0]].p4() + photons[tight_photons[0]].p4()).M())
            self.out.fillBranch("is_lepton_tight",1)

        elif len(loose_but_not_tight_muons) == 1:

            try:

                for i in range(0,len(genparts)):
                    if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 13 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct_mask == isprompttaudecayproduct_mask)) and deltaR(muons[loose_but_not_tight_muons[0]].eta,muons[loose_but_not_tight_muons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        is_lepton_real=1
            except:
                pass

            if not event.HLT_IsoMu24:
                return False
        
            if deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,muons[loose_but_not_tight_muons[0]].eta,muons[loose_but_not_tight_muons[0]].phi) < 0.5:
                return False

            if muons[loose_but_not_tight_muons[0]].pt < 25:
                return False

            if abs(muons[loose_but_not_tight_muons[0]].eta) > 2.4:
                return False

            #if sqrt(2*muons[loose_but_not_tight_muons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - muons[loose_but_not_tight_muons[0]].phi))) < 30:
            #    return False

            self.out.fillBranch("mt",sqrt(2*muons[loose_but_not_tight_muons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - muons[loose_but_not_tight_muons[0]].phi))))

            mask1 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) | (1 << 6)
            mask2 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) 
            mask3 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 6)
            mask4 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 5) | (1 << 6)
            mask5 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 4) | (1 << 5) | (1 << 6) #invert the medium photon ID with the sigma_ietaieta cut removed

            bitmap = photons[tight_photons[0]].vidNestedWPBitmap & mask1

            if (bitmap == mask1):
                self.out.fillBranch("photon_selection",2)
            elif (bitmap == mask5):
                self.out.fillBranch("photon_selection",1)
            elif (bitmap == mask2) or (bitmap == mask3) or (bitmap == mask4):
                self.out.fillBranch("photon_selection",0)
            else:
                assert(0)

            self.out.fillBranch("is_lepton_real",is_lepton_real)
            self.out.fillBranch("lepton_pdg_id",13)
            self.out.fillBranch("lepton_pt",muons[loose_but_not_tight_muons[0]].pt)
            self.out.fillBranch("lepton_eta",muons[loose_but_not_tight_muons[0]].eta)
            self.out.fillBranch("lepton_phi",muons[loose_but_not_tight_muons[0]].phi)
            self.out.fillBranch("met",event.MET_pt)
            self.out.fillBranch("photon_pt",photons[tight_photons[0]].pt)
            self.out.fillBranch("photon_eta",photons[tight_photons[0]].eta)
            self.out.fillBranch("photon_phi",photons[tight_photons[0]].phi)
            self.out.fillBranch("mlg",(muons[loose_but_not_tight_muons[0]].p4() + photons[tight_photons[0]].p4()).M())
            self.out.fillBranch("is_lepton_tight",0)

        elif len(tight_electrons) == 1:

            try:

                for i in range(0,len(genparts)):
                    if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 11 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct_mask == isprompttaudecayproduct_mask)) and deltaR(electrons[tight_electrons[0]].eta,electrons[tight_electrons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        is_lepton_real=1
            except:
                pass

            if not event.HLT_Ele35_WPTight_Gsf:
                return False

            if electrons[tight_electrons[0]].cutBased == 0 or electrons[tight_electrons[0]].cutBased == 1:
                return False

            if deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,electrons[tight_electrons[0]].eta,electrons[tight_electrons[0]].phi) < 0.5:
                return False

            if electrons[tight_electrons[0]].pt < 30:
                return False

            if abs(electrons[tight_electrons[0]].eta) > 2.5:
                return False


            self.out.fillBranch("mt",sqrt(2*electrons[tight_electrons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - electrons[tight_electrons[0]].phi))))

            mask1 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) | (1 << 6)
            mask2 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) 
            mask3 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 6)
            mask4 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 5) | (1 << 6)
            mask5 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 4) | (1 << 5) | (1 << 6) #invert the medium photon ID with the sigma_ietaieta cut removed

            bitmap = photons[tight_photons[0]].vidNestedWPBitmap & mask1

            if (bitmap == mask1):
                self.out.fillBranch("photon_selection",2)
            elif (bitmap == mask5):
                self.out.fillBranch("photon_selection",1)
            elif (bitmap == mask2) or (bitmap == mask3) or (bitmap == mask4):
                self.out.fillBranch("photon_selection",0)
            else:
                assert(0)




            self.out.fillBranch("is_lepton_real",is_lepton_real)
            self.out.fillBranch("lepton_pdg_id",11)
            self.out.fillBranch("lepton_pt",electrons[tight_electrons[0]].pt)
            self.out.fillBranch("lepton_eta",electrons[tight_electrons[0]].eta)
            self.out.fillBranch("lepton_phi",electrons[tight_electrons[0]].phi)
            self.out.fillBranch("met",event.MET_pt)
            self.out.fillBranch("photon_pt",photons[tight_photons[0]].pt)
            self.out.fillBranch("photon_eta",photons[tight_photons[0]].eta)
            self.out.fillBranch("photon_phi",photons[tight_photons[0]].phi)
            self.out.fillBranch("mlg",(electrons[tight_electrons[0]].p4() + photons[tight_photons[0]].p4()).M())
            self.out.fillBranch("is_lepton_tight",1)

            print "selected electron event: " + str(event.event) + " " + str(event.luminosityBlock) + " " + str(event.run)

        elif len(loose_but_not_tight_electrons) == 1:

            try:

                for i in range(0,len(genparts)):
                    if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 11 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct_mask == isprompttaudecayproduct_mask)) and deltaR(electrons[loose_but_not_tight_electrons[0]].eta,electrons[loose_but_not_tight_electrons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        is_lepton_real=1

            except:

                pass
                        
            if not event.HLT_Ele35_WPTight_Gsf:
                return False

            if deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,electrons[loose_but_not_tight_electrons[0]].eta,electrons[loose_but_not_tight_electrons[0]].phi) < 0.5:
                return False

            if electrons[loose_but_not_tight_electrons[0]].pt < 30:
                return False

            if abs(electrons[loose_but_not_tight_electrons[0]].eta) > 2.5:
                return False

            self.out.fillBranch("mt",sqrt(2*electrons[loose_but_not_tight_electrons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - electrons[loose_but_not_tight_electrons[0]].phi))))

            mask1 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) | (1 << 6)
            mask2 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) 
            mask3 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 6)
            mask4 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 5) | (1 << 6)
            mask5 = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 4) | (1 << 5) | (1 << 6) #invert the medium photon ID with the sigma_ietaieta cut removed

            bitmap = photons[tight_photons[0]].vidNestedWPBitmap & mask1

            if (bitmap == mask1):
                self.out.fillBranch("photon_selection",2)
            elif (bitmap == mask5):
                self.out.fillBranch("photon_selection",1)
            elif (bitmap == mask2) or (bitmap == mask3) or (bitmap == mask4):
                self.out.fillBranch("photon_selection",0)
            else:
                assert(0)



            self.out.fillBranch("is_lepton_real",is_lepton_real)
            self.out.fillBranch("lepton_pdg_id",11)
            self.out.fillBranch("lepton_pt",electrons[loose_but_not_tight_electrons[0]].pt)
            self.out.fillBranch("lepton_eta",electrons[loose_but_not_tight_electrons[0]].eta)
            self.out.fillBranch("lepton_phi",electrons[loose_but_not_tight_electrons[0]].phi)
            self.out.fillBranch("met",event.MET_pt)
            self.out.fillBranch("photon_pt",photons[tight_photons[0]].pt)
            self.out.fillBranch("photon_eta",photons[tight_photons[0]].eta)
            self.out.fillBranch("photon_phi",photons[tight_photons[0]].phi)
            self.out.fillBranch("mlg",(electrons[loose_but_not_tight_electrons[0]].p4() + photons[tight_photons[0]].p4()).M())
            self.out.fillBranch("is_lepton_tight",0)

        else:
            return False


        #print event.event


        #self.out.fillBranch("EventMass",eventSum.M())
        #if eventSum.M() < 2000:
        #    return False
        #else:
        #    return True

        photon_gen_matching=0

        try:

            for i in range(0,len(genparts)):
                if genparts[i].pt > 5 and genparts[i].status == 1 and abs(genparts[i].pdgId) == 13 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct_mask == isprompttaudecayproduct_mask)) and deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                    photon_gen_matching += 1 #m -> g
                    break

            for i in range(0,len(genparts)):
                if genparts[i].pt > 5 and genparts[i].status == 1 and abs(genparts[i].pdgId) == 11 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct_mask == isprompttaudecayproduct_mask)) and deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                    photon_gen_matching += 2 #e -> g
                    break
                    
            for i in range(0,len(genparts)):
                if genparts[i].pt > 5 and genparts[i].status == 1 and genparts[i].pdgId == 22 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct_mask == isprompttaudecayproduct_mask)) and deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                    if genparts[i].genPartIdxMother >= 0 and (abs(genparts[genparts[i].genPartIdxMother].pdgId) == 11 or abs(genparts[genparts[i].genPartIdxMother].pdgId) == 13 or abs(genparts[genparts[i].genPartIdxMother].pdgId) == 15):
                        photon_gen_matching += 8 #fsr photon
                    else:
                        photon_gen_matching += 4 #non-fsr photon
                    break

        except:
            pass

        self.out.fillBranch("photon_gen_matching",photon_gen_matching)

        try:
            self.out.fillBranch("gen_weight",event.Generator_weight)
        except:
            pass

        try:
            self.out.fillBranch("npu",event.Pileup_nPU)
            self.out.fillBranch("ntruepu",event.Pileup_nTrueInt)
        except:
            pass

        try:
            n_w_plus = 0
            n_w_minus = 0
            
            for i in range(0,len(lheparts)):
                if lheparts[i].pdgId == -11 or lheparts[i].pdgId == -13 or lheparts[i].pdgId == -15:
                    n_w_plus+=1
                elif lheparts[i].pdgId == 11 or lheparts[i].pdgId == 13 or lheparts[i].pdgId == 15:
                    n_w_minus+=1

            assert(n_w_plus == 1 or n_w_minus == 1)        
            
            self.out.fillBranch("lhe_lepton_charge",bool(n_w_plus))
        except:
            pass

        self.out.fillBranch("njets",njets)
        self.out.fillBranch("npvs",event.PV_npvs)
        self.out.fillBranch("event",event.event)
        self.out.fillBranch("lumi",event.luminosityBlock)
        self.out.fillBranch("run",event.run)

        return True

exampleModule = lambda : exampleProducer()
