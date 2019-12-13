import ROOT

from math import sin, cos, sqrt

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi

class wgProducer(Module):
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
        self.out.branch("n_gen_neutrinos",  "I");
        self.out.branch("n_gen_leptons",  "I");
        self.out.branch("n_gen_photons",  "I");
        self.out.branch("gen_leptons_pt",  "F");
        self.out.branch("gen_leptons_phi",  "F");
        self.out.branch("gen_neutrinos_pt",  "F");
        self.out.branch("gen_neutrinos_phi",  "F");
        self.out.branch("gen_photons_pt",  "F");
        self.out.branch("gen_photons_phi",  "F");
        self.out.branch("lepton_pdg_id",  "I");
        self.out.branch("lepton_pt",  "F");
        self.out.branch("lepton_phi",  "F");
        self.out.branch("lepton_eta",  "F");
        self.out.branch("photon_genjet_matching",  "I");
        self.out.branch("photon_pt",  "F");
        self.out.branch("photon_phi",  "F");
        self.out.branch("photon_eta",  "F");
        self.out.branch("mlg",  "F");
        self.out.branch("photon_selection",  "I");
        self.out.branch("met",  "F");
        self.out.branch("lhemet",  "F");
        self.out.branch("lhemetphi",  "F");
        self.out.branch("rawmet",  "F");
        self.out.branch("rawmetphi",  "F");
        self.out.branch("metup",  "F");
        self.out.branch("metphi",  "F");
        self.out.branch("mt",  "F");
        self.out.branch("puppimet",  "F");
        self.out.branch("puppimetphi",  "F");
        self.out.branch("puppimt",  "F");
        self.out.branch("npvs","I")
        self.out.branch("njets50","I")
        self.out.branch("njets40","I")
        self.out.branch("njets30","I")
        self.out.branch("njets20","I")
        self.out.branch("njets15","I")
        self.out.branch("pass_lhe_selection",  "B");
        self.out.branch("is_lepton_tight",  "B");
        self.out.branch("gen_weight",  "F");
        self.out.branch("is_lepton_real",  "B");
        self.out.branch("lhe_lepton_charge",  "B");
        self.out.branch("n_lhe_partons",  "I");
        self.out.branch("n_lhe_photons",  "I");
        self.out.branch("n_lower_pt_leptons",  "I");
        self.out.branch("photon_gen_matching",  "I");
        self.out.branch("photon_vidNestedWPBitmap",  "I");
        self.out.branch("photon_sieie",  "F");
        self.out.branch("photon_pfRelIso03_chg",  "F");
        self.out.branch("photon_gen_matching_old",  "I");
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        #do this first for processing speed-up
        if not (event.HLT_Ele27_WPTight_Gsf or event.HLT_IsoMu24 or event.HLT_IsoTkMu24):
            return False

        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        photons = Collection(event, "Photon")
        genjets = Collection(event, "GenJet")

        if hasattr(event,'nGenPart'):
            genparts = Collection(event, "GenPart")

        if hasattr(event,'nLHEPart'):    
            lheparts = Collection(event, "LHEPart")
            
        debug = False

        lower_pt_muons = []

        tight_muons = []
        
        loose_but_not_tight_muons = []
        
        lower_pt_electrons = []

        tight_electrons = []

        loose_but_not_tight_electrons = []
        
        tight_photons = []

        for i in range(0,len(muons)):
            if muons[i].pt > 20 and abs(muons[i].eta) < 2.4:
                if muons[i].tightId and muons[i].pfRelIso04_all < 0.15:
                    tight_muons.append(i)
                elif muons[i].tightId and muons[i].pfRelIso04_all < 0.25:
                    loose_but_not_tight_muons.append(i)
            elif muons[i].pt > 10 and abs(muons[i].eta) < 2.4:
                if muons[i].tightId and muons[i].pfRelIso04_all < 0.15:
                    lower_pt_muons.append(i)
                elif muons[i].tightId and muons[i].pfRelIso04_all < 0.25:
                    lower_pt_muons.append(i)

        #for processing speed-up
        if len(tight_muons) + len(loose_but_not_tight_muons) > 1:
            return False


        for i in range (0,len(electrons)):
            if electrons[i].pt > 20 and abs(electrons[i].eta + electrons[i].deltaEtaSC) < 2.5:
                if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):
                    if electrons[i].cutBased >= 3:
                        tight_electrons.append(i)
                    elif electrons[i].cutBased >= 1:
                        loose_but_not_tight_electrons.append(i)
            elif electrons[i].pt > 10 and abs(electrons[i].eta + electrons[i].deltaEtaSC) < 2.5:
                if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):
                    if electrons[i].cutBased >= 3:
                        lower_pt_electrons.append(i)
                    elif electrons[i].cutBased >= 1:
                        lower_pt_electrons.append(i)

        if len(tight_muons) + len(loose_but_not_tight_muons) +  len(tight_electrons) + len(loose_but_not_tight_electrons) > 1:
            return False

        for i in range (0,len(photons)):

            if photons[i].pt < 20:
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

            #first add the photons that pass the full ID
            if not (bitmap == mask1):
                continue

            #this is redundant after the if statement above
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

            mask1 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) | (1 << 13)
            mask2 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) 
            mask3 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) |  (1 << 13)
            mask4 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 11) | (1 << 13)
            mask5 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 9) | (1 << 11) | (1 << 13) #invert the medium photon ID with the sigma_ietaieta cut removed

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


        njets50 = 0
        njets40 = 0
        njets30 = 0
        njets20 = 0
        njets15 = 0

        for i in range(0,len(jets)):

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

            if jets[i].pt > 50:
                njets50+=1
            if jets[i].pt > 40:
                njets40+=1
            if jets[i].pt > 30:
                njets30+=1
            if jets[i].pt > 20:
                njets20+=1
            if jets[i].pt > 15:
                njets15+=1

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

        isprompt_mask = (1 << 0) #isPrompt
        isdirectprompttaudecayproduct_mask = (1 << 5) #isDirectPromptTauDecayProduct
        isfromhardprocess_mask = (1 << 8) #isPrompt
        
        is_lepton_real=0

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

            #if sqrt(2*muons[tight_muons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - muons[tight_muons[0]].phi))) < 30:
            #    return False

            if debug:
                print "selected muon event: " + str(event.event) + " " + str(event.luminosityBlock) + " " + str(event.run)
            
            mask1 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) | (1 << 13)
            mask2 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) 
            mask3 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) |  (1 << 13)
            mask4 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 11) | (1 << 13)
            mask5 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 9) | (1 << 11) | (1 << 13) #invert the medium photon ID with the sigma_ietaieta cut removed

            bitmap = photons[tight_photons[0]].vidNestedWPBitmap & mask1

            if (bitmap == mask1):
                self.out.fillBranch("photon_selection",0) #all cuts applied
            elif (bitmap == mask2):
                self.out.fillBranch("photon_selection",1)
            elif (bitmap == mask3):
                self.out.fillBranch("photon_selection",2)
            elif (bitmap == mask4):
                self.out.fillBranch("photon_selection",3) #invert the charged isolation cut
            elif (bitmap == mask5):
                self.out.fillBranch("photon_selection",4) #invert the sigma_ietaieta cut
            else:
                assert(0)                


            try:
                for i in range(0,len(genparts)):
                    if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 13 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and deltaR(muons[tight_muons[0]].eta,muons[tight_muons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        is_lepton_real=1
            except:
                pass

            self.out.fillBranch("mt",sqrt(2*muons[tight_muons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - muons[tight_muons[0]].phi))))
            self.out.fillBranch("puppimt",sqrt(2*muons[tight_muons[0]].pt*event.PuppiMET_pt*(1 - cos(event.PuppiMET_phi - muons[tight_muons[0]].phi))))
            self.out.fillBranch("is_lepton_real",is_lepton_real)
            self.out.fillBranch("lepton_pdg_id",13)
            self.out.fillBranch("lepton_pt",muons[tight_muons[0]].pt)
            self.out.fillBranch("lepton_eta",muons[tight_muons[0]].eta)
            self.out.fillBranch("lepton_phi",muons[tight_muons[0]].phi)

            self.out.fillBranch("photon_vidNestedWPBitmap",photons[tight_photons[0]].vidNestedWPBitmap)
            self.out.fillBranch("photon_pfRelIso03_chg",photons[tight_photons[0]].pfRelIso03_chg)
            self.out.fillBranch("photon_sieie",photons[tight_photons[0]].sieie)
            self.out.fillBranch("photon_pt",photons[tight_photons[0]].pt)
            self.out.fillBranch("photon_eta",photons[tight_photons[0]].eta)
            self.out.fillBranch("photon_phi",photons[tight_photons[0]].phi)
            self.out.fillBranch("mlg",(muons[tight_muons[0]].p4() + photons[tight_photons[0]].p4()).M())
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

            #if sqrt(2*muons[loose_but_not_tight_muons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - muons[loose_but_not_tight_muons[0]].phi))) < 30:
            #    return False


            mask1 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) | (1 << 13)
            mask2 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) 
            mask3 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) |  (1 << 13)
            mask4 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 11) | (1 << 13)
            mask5 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 9) | (1 << 11) | (1 << 13) #invert the medium photon ID with the sigma_ietaieta cut removed

            bitmap = photons[tight_photons[0]].vidNestedWPBitmap & mask1

            if (bitmap == mask1):
                self.out.fillBranch("photon_selection",0) #all cuts applied
            elif (bitmap == mask2):
                self.out.fillBranch("photon_selection",1)
            elif (bitmap == mask3):
                self.out.fillBranch("photon_selection",2)
            elif (bitmap == mask4):
                self.out.fillBranch("photon_selection",3) #invert the charged isolation cut
            elif (bitmap == mask5):
                self.out.fillBranch("photon_selection",4) #invert the sigma_ietaieta cut
            else:
                assert(0)                


            try:

                for i in range(0,len(genparts)):
                    if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 13 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and deltaR(muons[loose_but_not_tight_muons[0]].eta,muons[loose_but_not_tight_muons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        is_lepton_real=1
            except:
                pass


            self.out.fillBranch("mt",sqrt(2*muons[loose_but_not_tight_muons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - muons[loose_but_not_tight_muons[0]].phi))))
            self.out.fillBranch("puppimt",sqrt(2*muons[loose_but_not_tight_muons[0]].pt*event.PuppiMET_pt*(1 - cos(event.PuppiMET_phi - muons[loose_but_not_tight_muons[0]].phi))))
            self.out.fillBranch("is_lepton_real",is_lepton_real)
            self.out.fillBranch("lepton_pdg_id",13)
            self.out.fillBranch("lepton_pt",muons[loose_but_not_tight_muons[0]].pt)
            self.out.fillBranch("lepton_eta",muons[loose_but_not_tight_muons[0]].eta)
            self.out.fillBranch("lepton_phi",muons[loose_but_not_tight_muons[0]].phi)

            self.out.fillBranch("photon_pt",photons[tight_photons[0]].pt)
            self.out.fillBranch("photon_vidNestedWPBitmap",photons[tight_photons[0]].vidNestedWPBitmap)
            self.out.fillBranch("photon_pfRelIso03_chg",photons[tight_photons[0]].pfRelIso03_chg)
            self.out.fillBranch("photon_sieie",photons[tight_photons[0]].sieie)
            self.out.fillBranch("photon_eta",photons[tight_photons[0]].eta)
            self.out.fillBranch("photon_phi",photons[tight_photons[0]].phi)
            self.out.fillBranch("mlg",(muons[loose_but_not_tight_muons[0]].p4() + photons[tight_photons[0]].p4()).M())
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

            if abs(electrons[tight_electrons[0]].eta) > 2.5:
                return False

            if debug:
                print "selected electron event: " + str(event.event) + " " + str(event.luminosityBlock) + " " + str(event.run)

            mask1 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) | (1 << 13)
            mask2 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) 
            mask3 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) |  (1 << 13)
            mask4 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 11) | (1 << 13)
            mask5 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 9) | (1 << 11) | (1 << 13) #invert the medium photon ID with the sigma_ietaieta cut removed

            bitmap = photons[tight_photons[0]].vidNestedWPBitmap & mask1

            if (bitmap == mask1):
                self.out.fillBranch("photon_selection",0) #all cuts applied
            elif (bitmap == mask2):
                self.out.fillBranch("photon_selection",1)
            elif (bitmap == mask3):
                self.out.fillBranch("photon_selection",2)
            elif (bitmap == mask4):
                self.out.fillBranch("photon_selection",3) #invert the charged isolation cut
            elif (bitmap == mask5):
                self.out.fillBranch("photon_selection",4) #invert the sigma_ietaieta cut
            else:
                assert(0)                


            try:

                for i in range(0,len(genparts)):
                    if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 11 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and deltaR(electrons[tight_electrons[0]].eta,electrons[tight_electrons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        is_lepton_real=1
            except:
                pass

            self.out.fillBranch("mt",sqrt(2*electrons[tight_electrons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - electrons[tight_electrons[0]].phi))))
            self.out.fillBranch("puppimt",sqrt(2*electrons[tight_electrons[0]].pt*event.PuppiMET_pt*(1 - cos(event.PuppiMET_phi - electrons[tight_electrons[0]].phi))))
            self.out.fillBranch("is_lepton_real",is_lepton_real)
            self.out.fillBranch("lepton_pdg_id",11)
            self.out.fillBranch("lepton_pt",electrons[tight_electrons[0]].pt)
            self.out.fillBranch("lepton_eta",electrons[tight_electrons[0]].eta)
            self.out.fillBranch("lepton_phi",electrons[tight_electrons[0]].phi)

            self.out.fillBranch("photon_pt",photons[tight_photons[0]].pt)
            self.out.fillBranch("photon_vidNestedWPBitmap",photons[tight_photons[0]].vidNestedWPBitmap)
            self.out.fillBranch("photon_pfRelIso03_chg",photons[tight_photons[0]].pfRelIso03_chg)
            self.out.fillBranch("photon_sieie",photons[tight_photons[0]].sieie)
            self.out.fillBranch("photon_eta",photons[tight_photons[0]].eta)
            self.out.fillBranch("photon_phi",photons[tight_photons[0]].phi)
            self.out.fillBranch("mlg",(electrons[tight_electrons[0]].p4()+photons[tight_photons[0]].p4()).M())
            self.out.fillBranch("is_lepton_tight",1)

        elif len(loose_but_not_tight_electrons) == 1:

                        
            if not event.HLT_Ele27_WPTight_Gsf:
                return False

            if deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,electrons[loose_but_not_tight_electrons[0]].eta,electrons[loose_but_not_tight_electrons[0]].phi) < 0.5:
                return False

            if electrons[loose_but_not_tight_electrons[0]].pt < 30:
                return False

            if abs(electrons[loose_but_not_tight_electrons[0]].eta) > 2.5:
                return False

            mask1 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) | (1 << 13)
            mask2 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) 
            mask3 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) |  (1 << 13)
            mask4 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 11) | (1 << 13)
            mask5 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 9) | (1 << 11) | (1 << 13) #invert the medium photon ID with the sigma_ietaieta cut removed

            bitmap = photons[tight_photons[0]].vidNestedWPBitmap & mask1

            if (bitmap == mask1):
                self.out.fillBranch("photon_selection",0) #all cuts applied
            elif (bitmap == mask2):
                self.out.fillBranch("photon_selection",1)
            elif (bitmap == mask3):
                self.out.fillBranch("photon_selection",2)
            elif (bitmap == mask4):
                self.out.fillBranch("photon_selection",3) #invert the charged isolation cut
            elif (bitmap == mask5):
                self.out.fillBranch("photon_selection",4) #invert the sigma_ietaieta cut
            else:
                assert(0)                


            try:

                for i in range(0,len(genparts)):
                    if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 11 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and deltaR(electrons[loose_but_not_tight_electrons[0]].eta,electrons[loose_but_not_tight_electrons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        is_lepton_real=1

            except:

                pass

            self.out.fillBranch("mt",sqrt(2*electrons[loose_but_not_tight_electrons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - electrons[loose_but_not_tight_electrons[0]].phi))))
            self.out.fillBranch("puppimt",sqrt(2*electrons[loose_but_not_tight_electrons[0]].pt*event.PuppiMET_pt*(1 - cos(event.PuppiMET_phi - electrons[loose_but_not_tight_electrons[0]].phi))))
            self.out.fillBranch("is_lepton_real",is_lepton_real)
            self.out.fillBranch("lepton_pdg_id",11)
            self.out.fillBranch("lepton_pt",electrons[loose_but_not_tight_electrons[0]].pt)
            self.out.fillBranch("lepton_eta",electrons[loose_but_not_tight_electrons[0]].eta)
            self.out.fillBranch("lepton_phi",electrons[loose_but_not_tight_electrons[0]].phi)

            self.out.fillBranch("photon_pt",photons[tight_photons[0]].pt)
            self.out.fillBranch("photon_vidNestedWPBitmap",photons[tight_photons[0]].vidNestedWPBitmap)
            self.out.fillBranch("photon_pfRelIso03_chg",photons[tight_photons[0]].pfRelIso03_chg)
            self.out.fillBranch("photon_sieie",photons[tight_photons[0]].sieie)
            self.out.fillBranch("photon_eta",photons[tight_photons[0]].eta)
            self.out.fillBranch("photon_phi",photons[tight_photons[0]].phi)
            self.out.fillBranch("mlg",(electrons[loose_but_not_tight_electrons[0]].p4()+photons[tight_photons[0]].p4()).M())
            self.out.fillBranch("is_lepton_tight",0)

        else:
            return False

        photon_gen_matching=0

        if hasattr(photons[tight_photons[0]],'genPartIdx'):
            if photons[tight_photons[0]].genPartIdx >= 0 and genparts[photons[tight_photons[0]].genPartIdx].pdgId  == 22: 
                if ((genparts[photons[tight_photons[0]].genPartIdx].statusFlags & isprompt_mask == isprompt_mask) or (genparts[photons[tight_photons[0]].genPartIdx].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and (genparts[photons[tight_photons[0]].genPartIdx].statusFlags & isfromhardprocess_mask == isfromhardprocess_mask):
                    photon_gen_matching = 6
                elif ((genparts[photons[tight_photons[0]].genPartIdx].statusFlags & isprompt_mask == isprompt_mask) or (genparts[photons[tight_photons[0]].genPartIdx].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)):       
                    if (genparts[photons[tight_photons[0]].genPartIdx].genPartIdxMother >= 0 and (abs(genparts[genparts[photons[tight_photons[0]].genPartIdx].genPartIdxMother].pdgId) == 11 or abs(genparts[genparts[photons[tight_photons[0]].genPartIdx].genPartIdxMother].pdgId) == 13 or abs(genparts[genparts[photons[tight_photons[0]].genPartIdx].genPartIdxMother].pdgId) == 15)):
                        photon_gen_matching = 4
                    else:    
                        photon_gen_matching = 5
                else:
                    photon_gen_matching = 3
            elif photons[tight_photons[0]].genPartIdx >= 0 and abs(genparts[photons[tight_photons[0]].genPartIdx].pdgId) == 11:     
                if ((genparts[photons[tight_photons[0]].genPartIdx].statusFlags & isprompt_mask == isprompt_mask) or (genparts[photons[tight_photons[0]].genPartIdx].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)):  
                    photon_gen_matching = 1
                else:
                    photon_gen_matching = 2
                    
            else:
                assert(photons[tight_photons[0]].genPartFlav == 0)
                photon_gen_matching = 0

        self.out.fillBranch("photon_gen_matching",photon_gen_matching)

        photon_gen_matching_old=0

        if hasattr(event,'nGenPart'):

            for i in range(0,len(genparts)):
                if genparts[i].pt > 5 and genparts[i].status == 1 and abs(genparts[i].pdgId) == 13 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                    photon_gen_matching_old += 1 #m -> g

                if genparts[i].pt > 5 and genparts[i].status == 1 and abs(genparts[i].pdgId) == 11 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                    photon_gen_matching_old += 2 #e -> g

                if genparts[i].pt > 5 and genparts[i].status == 1 and genparts[i].pdgId == 22 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and deltaR(photons[tight_photons[0]].eta,photons[tight_photons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                    if genparts[i].genPartIdxMother >= 0 and (abs(genparts[genparts[i].genPartIdxMother].pdgId) == 11 or abs(genparts[genparts[i].genPartIdxMother].pdgId) == 13 or abs(genparts[genparts[i].genPartIdxMother].pdgId) == 15):
                        photon_gen_matching_old += 8 #fsr photon
                    else:
                        photon_gen_matching_old += 4 #non-fsr photon

        self.out.fillBranch("photon_gen_matching_old",photon_gen_matching_old)

        if hasattr(event,'Generator_weight'):
            self.out.fillBranch("gen_weight",event.Generator_weight)
        else:    
            self.out.fillBranch("gen_weight",0)

        if hasattr(event,'Pileup_nPU'):    
            self.out.fillBranch("npu",event.Pileup_nPU)
        else:
            self.out.fillBranch("npu",0)
    
        if hasattr(event,'Pileup_nTrueInt'):    
            self.out.fillBranch("ntruepu",event.Pileup_nTrueInt)
        else:
            self.out.fillBranch("ntruepu",0)

        lhe_neutrino_index=-1 

        try:
            n_lhe_w_plus = 0
            n_lhe_w_minus = 0
            n_lhe_photons = 0
            n_lhe_partons = 0
            n_lhe_neutrinos = 0
            
            for i in range(0,len(lheparts)):
                if lheparts[i].pdgId == 22:
                    lhe_photon_index=i
                    n_lhe_photons+=1

                if abs(lheparts[i].pdgId == 1) or abs(lheparts[i].pdgId) == 2 or abs(lheparts[i].pdgId) == 3 or abs(lheparts[i].pdgId) == 4 or abs(lheparts[i].pdgId) == 5 or abs(lheparts[i].pdgId) == 21:
                    n_lhe_partons+=1

                if lheparts[i].pdgId == -11 or lheparts[i].pdgId == -13 or lheparts[i].pdgId == -15:
                    n_lhe_w_plus+=1
                    lhe_lepton_index=i
                elif lheparts[i].pdgId == 11 or lheparts[i].pdgId == 13 or lheparts[i].pdgId == 15:
                    n_lhe_w_minus+=1
                    lhe_lepton_index=i
                elif abs(lheparts[i].pdgId) == 12 or abs(lheparts[i].pdgId) == 14 or abs(lheparts[i].pdgId) == 16:
                    n_lhe_neutrinos+=1 
                    lhe_neutrino_index=i 
             
            self.out.fillBranch("n_lhe_partons",n_lhe_partons)
            self.out.fillBranch("n_lhe_photons",n_lhe_photons)

            assert((n_lhe_w_plus == 1 and n_lhe_w_minus == 0) or (n_lhe_w_minus == 1 and n_lhe_w_plus == 0))        
            assert(n_lhe_neutrinos == 1 or n_lhe_neutrinos == 0)

            
            if deltaR(lheparts[lhe_lepton_index].eta,lheparts[lhe_lepton_index].phi,lheparts[lhe_photon_index].eta,lheparts[lhe_photon_index].phi) > 0.1 and lheparts[lhe_lepton_index].pt > 15 and lheparts[lhe_photon_index].pt > 15 and abs(lheparts[lhe_photon_index].eta) < 2.6:       
                self.out.fillBranch("pass_lhe_selection",1)
            else:    
                self.out.fillBranch("pass_lhe_selection",0)
     
            self.out.fillBranch("lhe_lepton_charge",bool(n_lhe_w_plus))
        except:   
            self.out.fillBranch("lhe_lepton_charge",0)
            self.out.fillBranch("pass_lhe_selection",0)
            self.out.fillBranch("n_lhe_partons",0)
            self.out.fillBranch("n_lhe_photons",0)

        n_gen_leptons = 0
        n_gen_neutrinos = 0
        n_gen_photons = 0

        gen_leptons = ROOT.TLorentzVector()
        gen_neutrinos = ROOT.TLorentzVector()
        gen_photons  = ROOT.TLorentzVector()

        photon_genjet_matching = 0

        if hasattr(event,'nGenJet'):
            for i in range(0,len(genjets)):
                if genjets[i].pt > 10 and deltaR(genjets[i].eta,genjets[i].phi,photons[tight_photons[0]].eta,photons[tight_photons[0]].phi) < 0.5:
                    photon_genjet_matching = 1

        self.out.fillBranch("photon_genjet_matching",photon_genjet_matching)

        if hasattr(event,'nGenPart'):    

            n_gen_leptons_fiducial = 0
            n_gen_photons_fiducial = 0
            for i in range(0,len(genparts)):

                if genparts[i].status == 1 and (abs(genparts[i].pdgId) == 12 or abs(genparts[i].pdgId) == 14 or abs(genparts[i].pdgId) == 16) and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)):
                    gen_neutrinos += genparts[i].p4()
                    n_gen_neutrinos +=  1

                if genparts[i].status == 1 and (abs(genparts[i].pdgId) == 11 or abs(genparts[i].pdgId) == 13) and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)):
                    gen_leptons += genparts[i].p4()
                    n_gen_leptons +=  1

                if genparts[i].status == 1 and genparts[i].pdgId == 22 and (genparts[i].statusFlags & isprompt_mask == isprompt_mask) and genparts[i].pt > 20 :
                    gen_photons += genparts[i].p4()
                    n_gen_photons +=  1


                if genparts[i].pt > 20 and genparts[i].status == 1 and (abs(genparts[i].pdgId) == 11 or abs(genparts[i].pdgId) == 13) and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)):
                    gen_lepton_index = i
                    n_gen_leptons_fiducial +=  1
                if genparts[i].pt > 20 and genparts[i].status == 1 and genparts[i].pdgId == 22 and abs(genparts[i].eta) < 2.5 and (genparts[i].statusFlags & isprompt_mask == isprompt_mask):
                    
                    pho_iso=0
                    for j in range(0,len(genparts)):

                        if j == i:
                            continue

                        if genparts[j].status != 1:
                            continue

                        if abs(genparts[j].pdgId) == 12 or abs(genparts[j].pdgId) == 14 or abs(genparts[j].pdgId) == 16:
                            continue

                        if genparts[j].pt > 20 and genparts[j].status == 1 and (abs(genparts[j].pdgId) == 11 or abs(genparts[j].pdgId) == 13) and ((genparts[j].statusFlags & isprompt_mask == isprompt_mask) or (genparts[j].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)):
                            continue

                        if deltaR(genparts[j].eta,genparts[j].phi,genparts[i].eta,genparts[i].phi) < 0.4:
                            pho_iso += genparts[j].pt

                    pho_iso /= genparts[i].pt

                    if pho_iso < 0.5:
                        gen_photon_index = i
                        n_gen_photons_fiducial +=1

        self.out.fillBranch("n_gen_leptons",n_gen_leptons)
        self.out.fillBranch("n_gen_photons",n_gen_photons)
        self.out.fillBranch("n_gen_neutrinos",n_gen_neutrinos)
        self.out.fillBranch("gen_leptons_pt",gen_leptons.Pt())
        self.out.fillBranch("gen_leptons_phi",gen_leptons.Phi())
        self.out.fillBranch("gen_neutrinos_pt",gen_neutrinos.Pt())
        self.out.fillBranch("gen_neutrinos_phi",gen_neutrinos.Phi())
        self.out.fillBranch("gen_photons_pt",gen_photons.Pt())
        self.out.fillBranch("gen_photons_phi",gen_photons.Phi())
        self.out.fillBranch("n_lower_pt_leptons",len(lower_pt_muons)+len(lower_pt_electrons))
        self.out.fillBranch("njets50",njets50)
        self.out.fillBranch("njets40",njets40)
        self.out.fillBranch("njets30",njets30)
        self.out.fillBranch("njets20",njets20)
        self.out.fillBranch("njets15",njets15)
        self.out.fillBranch("npvs",event.PV_npvs)
        self.out.fillBranch("event",event.event)
        self.out.fillBranch("lumi",event.luminosityBlock)
        self.out.fillBranch("run",event.run)
        self.out.fillBranch("met",event.MET_pt)
        self.out.fillBranch("metup",sqrt(pow(event.MET_pt*cos(event.MET_phi) + event.MET_MetUnclustEnUpDeltaX,2) + pow(event.MET_pt*sin(event.MET_phi) + event.MET_MetUnclustEnUpDeltaY,2)))
        self.out.fillBranch("puppimet",event.PuppiMET_pt)
        self.out.fillBranch("puppimetphi",event.PuppiMET_phi)
        self.out.fillBranch("rawmet",event.RawMET_pt)
        if lhe_neutrino_index != -1:
            self.out.fillBranch("lhemet",lheparts[lhe_neutrino_index].pt)
            self.out.fillBranch("lhemetphi",lheparts[lhe_neutrino_index].phi)
        self.out.fillBranch("rawmetphi",event.RawMET_phi)
        self.out.fillBranch("metphi",event.MET_phi)

        return True

wgModule = lambda : wgProducer()
