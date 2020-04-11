import ROOT

from math import cos, sqrt

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi

class wgFakePhotonProducer(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("run",  "i")
        self.out.branch("lumi",  "i")
        self.out.branch("event",  "l")
        self.out.branch("npu",  "I")
        self.out.branch("npvs","I")
        self.out.branch("n_gen_neutrinos",  "I");
        self.out.branch("n_gen_leptons",  "I");
        self.out.branch("n_gen_photons",  "I");
        self.out.branch("gen_leptons_pt",  "F");
        self.out.branch("gen_leptons_phi",  "F");
        self.out.branch("gen_neutrinos_pt",  "F");
        self.out.branch("gen_neutrinos_phi",  "F");
        self.out.branch("gen_photons_pt",  "F");
        self.out.branch("gen_photons_phi",  "F");
        self.out.branch("njets_fake",  "I")
        self.out.branch("njets_fake_template",  "I")
        self.out.branch("photon1_sieie",  "F")
        self.out.branch("photon1_pfRelIso03_chg",  "F")
        self.out.branch("photon1_selection",  "I")
        self.out.branch("photon1_pt",  "F")
        self.out.branch("photon1_phi",  "F")
        self.out.branch("photon1_eta",  "F")
        self.out.branch("photon1_isScEtaEE",  "B")
        self.out.branch("photon1_isScEtaEB",  "B")
        self.out.branch("photon2_sieie",  "F")
        self.out.branch("photon2_pfRelIso03_chg",  "F")
        self.out.branch("photon2_pt",  "F")
        self.out.branch("photon2_phi",  "F")
        self.out.branch("photon2_eta",  "F")
        self.out.branch("photon2_isScEtaEE",  "B")
        self.out.branch("photon2_isScEtaEB",  "B")
        self.out.branch("gen_weight",  "F")
        self.out.branch("lepton_pdg_id",  "I")
        self.out.branch("lepton_pt",  "F")
        self.out.branch("lepton_eta",  "F")
        self.out.branch("lepton_phi",  "F")
        self.out.branch("photon1_genjet_matching",  "I")
        self.out.branch("photon2_genjet_matching",  "I")
        self.out.branch("photon1_gen_matching",  "I")
        self.out.branch("photon2_gen_matching",  "I")
        self.out.branch("photon1_gen_matching_old",  "I")
        self.out.branch("photon2_gen_matching_old",  "I")
        self.out.branch("photon1_genpart_pdgid",  "I")
        self.out.branch("photon2_genpart_pdgid",  "I")
        self.out.branch("photon1_genpart_pt",  "F")
        self.out.branch("photon2_genpart_pt",  "F")
        self.out.branch("photon1_moth_genpart_pdgid",  "I")
        self.out.branch("photon2_moth_genpart_pdgid",  "I")
        self.out.branch("photon1_moth_genpart_pt",  "F")
        self.out.branch("photon2_moth_genpart_pt",  "F")
        self.out.branch("mt",  "F")
        self.out.branch("met",  "F")
        self.out.branch("metphi",  "F")
        self.out.branch("puppimt",  "F")
        self.out.branch("puppimet",  "F")
        self.out.branch("puppimetphi",  "F")
        self.out.branch("pass_selection1",  "B");
        self.out.branch("pass_selection2",  "B");
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        photons = Collection(event, "Photon")

        if hasattr(event,"nGenJet"):
            genjets = Collection(event, "GenJet")

        pass_selection1 = False
        pass_selection2 = False                

        if hasattr(event,"nGenPart"):
            genparts = Collection(event, "GenPart")

        tight_muons = []

        loose_but_not_tight_muons = []
        
        tight_electrons = []

        loose_but_not_tight_electrons = []
        
        selected_tight_or_control_photons = []
        selected_fake_template_photons = []

        tight_jets = []

#        if event.MET_pt < 35:
#            return False

        for i in range(0,len(muons)):

            if muons[i].pt < 20:
                continue

            if abs(muons[i].eta) > 2.4:
                continue

            if muons[i].tightId and muons[i].pfRelIso04_all < 0.15:
                tight_muons.append(i)
#            elif muons[i].pfRelIso04_all < 0.4:
            elif muons[i].tightId and muons[i].pfRelIso04_all < 0.25:
                loose_but_not_tight_muons.append(i)

        for i in range (0,len(electrons)):

            if electrons[i].pt < 20:
                continue
            
            if abs(electrons[i].eta+ electrons[i].deltaEtaSC) > 2.5:
                continue

            if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):
                if electrons[i].cutBased >= 3:
                    tight_electrons.append(i)

                elif electrons[i].cutBased >= 1:
                    loose_but_not_tight_electrons.append(i)

        for i in range (0,len(photons)):

            if photons[i].pt < 20:
                continue

            if not (photons[i].isScEtaEE or photons[i].isScEtaEB):    
                continue

            mask1 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) | (1 << 13)
            mask2 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) 
            mask3 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) |  (1 << 13)
            mask4 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 11) | (1 << 13)
            mask5 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 9) | (1 << 11) | (1 << 13) #invert the medium photon ID with the sigma_ietaieta cut removed

            bitmap = photons[i].vidNestedWPBitmap & mask1

            #after adding the photons that pass the full ID, add the photons that pass the inverted ID
            if not (bitmap == mask1):
                continue

            #this is redundant after the if statement above
            if not((bitmap == mask1) or (bitmap == mask2) or (bitmap == mask3) or (bitmap == mask4) or (bitmap == mask5)):
                continue

#            if not photons[i].electronVeto:
#                continue

            if photons[i].pixelSeed:
                continue

            #if photons[i].pfRelIso03_chg > 10 or not (photons[i].pfRelIso03_chg > 4 or photons[i].sieie > 0.01031):
            #if photons[i].pfRelIso03_chg*photons[i].pt > 10 or photons[i].pfRelIso03_chg*photons[i].pt < 4:
            #    continue

            pass_lepton_dr_cut = True

            for j in range(0,len(tight_muons)):
                if deltaR(muons[tight_muons[j]].eta,muons[tight_muons[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False

            for j in range(0,len(tight_electrons)):
                if deltaR(electrons[tight_electrons[j]].eta,electrons[tight_electrons[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False

            if not pass_lepton_dr_cut:
                continue

            selected_tight_or_control_photons.append(i)

        for i in range (0,len(photons)):

            if photons[i].pt < 20:
                continue

            if not (photons[i].isScEtaEE or photons[i].isScEtaEB):    
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

#            if not photons[i].electronVeto:
#                continue

            if photons[i].pixelSeed:
                continue

            #if photons[i].pfRelIso03_chg > 10 or not (photons[i].pfRelIso03_chg > 4 or photons[i].sieie > 0.01031):
            #if photons[i].pfRelIso03_chg*photons[i].pt > 10 or photons[i].pfRelIso03_chg*photons[i].pt < 4:
            #    continue

            pass_lepton_dr_cut = True

            for j in range(0,len(tight_muons)):
                if deltaR(muons[tight_muons[j]].eta,muons[tight_muons[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False

            for j in range(0,len(tight_electrons)):
                if deltaR(electrons[tight_electrons[j]].eta,electrons[tight_electrons[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False

            if not pass_lepton_dr_cut:
                continue

            selected_tight_or_control_photons.append(i)

        for i in range (0,len(photons)):

            if photons[i].pt < 20:
                continue

            if not (photons[i].isScEtaEE or photons[i].isScEtaEB):    
                continue

            #invert the medium photon ID with the sigma_ietaieta cut removed
            mask = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 11) | (1 << 13)

            if not (mask & photons[i].vidNestedWPBitmap == mask):
                continue

#            if not photons[i].electronVeto:
#                continue

            if photons[i].pixelSeed:
                continue

            #if photons[i].pfRelIso03_chg > 10 or not (photons[i].pfRelIso03_chg > 4 or photons[i].sieie > 0.01031):
            if photons[i].pfRelIso03_chg*photons[i].pt > 10 or photons[i].pfRelIso03_chg*photons[i].pt < 4:
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

            selected_fake_template_photons.append(i)


        if len(tight_muons)+ len(loose_but_not_tight_muons) + len(tight_electrons) + len(loose_but_not_tight_electrons)!= 1:
            return False


        if not (len(selected_tight_or_control_photons) >= 1 or len(selected_fake_template_photons) == 1):
            return False

        if len(tight_muons) == 1:

            if not event.HLT_IsoMu24:
                return False
            
            pass_selection1 = len(selected_tight_or_control_photons) >= 1
            pass_selection2 = len(selected_fake_template_photons) == 1

            self.out.fillBranch("lepton_pdg_id",13)

            self.out.fillBranch("mt",sqrt(2*muons[tight_muons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - muons[tight_muons[0]].phi))))
            self.out.fillBranch("puppimt",sqrt(2*muons[tight_muons[0]].pt*event.PuppiMET_pt*(1 - cos(event.PuppiMET_phi - muons[tight_muons[0]].phi))))
            self.out.fillBranch("lepton_pt",muons[tight_muons[0]].pt)
            self.out.fillBranch("lepton_eta",muons[tight_muons[0]].eta)
            self.out.fillBranch("lepton_phi",muons[tight_muons[0]].phi)
            
        elif len(tight_electrons) == 1:

            if not event.HLT_Ele32_WPTight_Gsf:
                return False

            if len(selected_tight_or_control_photons) >= 1:
                if abs((electrons[tight_electrons[0]].p4() + photons[selected_tight_or_control_photons[0]].p4()).M() - 91.2) >= 10:
                    pass_selection1 = True

            if len(selected_fake_template_photons) == 1:
                if abs((electrons[tight_electrons[0]].p4() + photons[selected_fake_template_photons[0]].p4()).M() - 91.2) >= 10:
                    pass_selection2 = True

            self.out.fillBranch("lepton_pdg_id",11)

            self.out.fillBranch("mt",sqrt(2*electrons[tight_electrons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - electrons[tight_electrons[0]].phi))))
            self.out.fillBranch("puppimt",sqrt(2*electrons[tight_electrons[0]].pt*event.PuppiMET_pt*(1 - cos(event.PuppiMET_phi - electrons[tight_electrons[0]].phi))))

            self.out.fillBranch("lepton_pt",electrons[tight_electrons[0]].pt)
            self.out.fillBranch("lepton_eta",electrons[tight_electrons[0]].eta)
            self.out.fillBranch("lepton_phi",electrons[tight_electrons[0]].phi)

        if not pass_selection1 and not pass_selection2:
            return False

        njets_fake_template = 0
        njets_fake = 0

        for i in range(0,len(jets)):

            if abs(jets[i].eta) > 4.7:
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

            if jets[i].pt <= 40:
                continue

            if len(selected_tight_or_control_photons) >= 1:

                if deltaR(photons[selected_tight_or_control_photons[0]].eta,photons[selected_tight_or_control_photons[0]].phi,jets[i].eta,jets[i].phi) > 0.5:
                    njets_fake+=1

            if len(selected_fake_template_photons) == 1:
                if deltaR(photons[selected_fake_template_photons[0]].eta,photons[selected_fake_template_photons[0]].phi,jets[i].eta,jets[i].phi) > 0.5:
                    njets_fake_template+=1

        self.out.fillBranch("pass_selection1",pass_selection1)
        self.out.fillBranch("pass_selection2",pass_selection2)

        if pass_selection1:    
            photon1_gen_matching = 0
            photon1_gen_matching_old=0
            photon1_genpart_pdgid=0
            photon1_genpart_pt=0
            photon1_moth_genpart_pdgid=0
            photon1_moth_genpart_pt=0

            isprompt_mask = (1 << 0) #isPrompt
            isfromhardprocess_mask = (1 << 8) #isFromHardProcess 
            isprompttaudecayproduct_mask = (1 << 4) #isPromptTauDecayProduct
            isdirectprompttaudecayproduct_mask = (1 << 5) #isDirectPromptTauDecayProduct


            photon1_genjet_matching = 0

            if hasattr(event,'nGenJet'):
                for i in range(0,len(genjets)):
                    if genjets[i].pt > 10 and deltaR(genjets[i].eta,genjets[i].phi,photons[selected_tight_or_control_photons[0]].eta,photons[selected_tight_or_control_photons[0]].phi) < 0.5:
                        photon1_genjet_matching = 1

            if hasattr(photons[selected_tight_or_control_photons[0]],'genPartIdx'):

                if photons[selected_tight_or_control_photons[0]].genPartIdx >= 0:
                    photon1_genpart_pdgid =  genparts[photons[selected_tight_or_control_photons[0]].genPartIdx].pdgId
                    if genparts[photons[selected_tight_or_control_photons[0]].genPartIdx].genPartIdxMother >= 0:
                        photon1_moth_genpart_pdgid = genparts[genparts[photons[selected_tight_or_control_photons[0]].genPartIdx].genPartIdxMother].pdgId
                        photon1_moth_genpart_pt = genparts[genparts[photons[selected_tight_or_control_photons[0]].genPartIdx].genPartIdxMother].pt

                        
                    photon1_genpart_pt =  genparts[photons[selected_tight_or_control_photons[0]].genPartIdx].pt
                

                if photons[selected_tight_or_control_photons[0]].genPartIdx >= 0 and genparts[photons[selected_tight_or_control_photons[0]].genPartIdx].pdgId  == 22:
                    if ((genparts[photons[selected_tight_or_control_photons[0]].genPartIdx].statusFlags & isprompt_mask == isprompt_mask) or (genparts[photons[selected_tight_or_control_photons[0]].genPartIdx].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and (genparts[photons[selected_tight_or_control_photons[0]].genPartIdx].statusFlags & isfromhardprocess_mask == isfromhardprocess_mask):
                        photon1_gen_matching = 6
                    elif ((genparts[photons[selected_tight_or_control_photons[0]].genPartIdx].statusFlags & isprompt_mask == isprompt_mask) or (genparts[photons[selected_tight_or_control_photons[0]].genPartIdx].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)):
                        if (genparts[photons[selected_tight_or_control_photons[0]].genPartIdx].genPartIdxMother >= 0 and (abs(genparts[genparts[photons[selected_tight_or_control_photons[0]].genPartIdx].genPartIdxMother].pdgId) == 11 or abs(genparts[genparts[photons[selected_tight_or_control_photons[0]].genPartIdx].genPartIdxMother].pdgId) == 13 or abs(genparts[genparts[photons[selected_tight_or_control_photons[0]].genPartIdx].genPartIdxMother].pdgId) == 15)):
                            photon1_gen_matching = 4
                        else:
                            photon1_gen_matching = 5
                    else:
                        photon1_gen_matching = 3
                elif photons[selected_tight_or_control_photons[0]].genPartIdx >= 0 and abs(genparts[photons[selected_tight_or_control_photons[0]].genPartIdx].pdgId) == 11:
                    if ((genparts[photons[selected_tight_or_control_photons[0]].genPartIdx].statusFlags & isprompt_mask == isprompt_mask) or (genparts[photons[selected_tight_or_control_photons[0]].genPartIdx].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)):
                        photon1_gen_matching = 1
                    else:
                        photon1_gen_matching = 2

                else:
                    assert(photons[selected_tight_or_control_photons[0]].genPartFlav == 0)


            if hasattr(event,'nGenPart'):

                for i in range(0,len(genparts)):
                    if genparts[i].pt > 5 and genparts[i].status == 1 and abs(genparts[i].pdgId) == 13 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and deltaR(photons[selected_tight_or_control_photons[0]].eta,photons[selected_tight_or_control_photons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        photon1_gen_matching_old += 1 #m -> g

                    if genparts[i].pt > 5 and genparts[i].status == 1 and abs(genparts[i].pdgId) == 11 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and deltaR(photons[selected_tight_or_control_photons[0]].eta,photons[selected_tight_or_control_photons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        photon1_gen_matching_old += 2 #e -> g

                    if genparts[i].pt > 5 and genparts[i].status == 1 and genparts[i].pdgId == 22 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and deltaR(photons[selected_tight_or_control_photons[0]].eta,photons[selected_tight_or_control_photons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        if genparts[i].genPartIdxMother >= 0 and (abs(genparts[genparts[i].genPartIdxMother].pdgId) == 11 or abs(genparts[genparts[i].genPartIdxMother].pdgId) == 13 or abs(genparts[genparts[i].genPartIdxMother].pdgId) == 15):
                            photon1_gen_matching_old += 8 #fsr photon
                        else:
                            photon1_gen_matching_old += 4 #non-fsr photon

            mask1 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11) | (1 << 13) #all cuts applied
            mask2 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) | (1 << 11)
            mask3 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 9) |  (1 << 13)
            mask4 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 7) | (1 << 11) | (1 << 13) #invert the charged isolation cut
            mask5 = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 9) | (1 << 11) | (1 << 13) #invert the sigma_ietaieta cut                                                   

            bitmap = photons[selected_tight_or_control_photons[0]].vidNestedWPBitmap & mask1

            if (bitmap == mask1):
                self.out.fillBranch("photon1_selection",0) #all cuts applied
            elif (bitmap == mask2):
                self.out.fillBranch("photon1_selection",1)
            elif (bitmap == mask3):
                self.out.fillBranch("photon1_selection",2)
            elif (bitmap == mask4):
                self.out.fillBranch("photon1_selection",3) #invert the charged isolation cut
            elif (bitmap == mask5):
                self.out.fillBranch("photon1_selection",4) #invert the sigma_ietaieta cut
            else:
                assert(0)                

            self.out.fillBranch("photon1_sieie",photons[selected_tight_or_control_photons[0]].sieie)
            self.out.fillBranch("photon1_pfRelIso03_chg",photons[selected_tight_or_control_photons[0]].pfRelIso03_chg)
            self.out.fillBranch("photon1_pt",photons[selected_tight_or_control_photons[0]].pt)
            self.out.fillBranch("photon1_phi",photons[selected_tight_or_control_photons[0]].phi)
            self.out.fillBranch("photon1_eta",photons[selected_tight_or_control_photons[0]].eta)
            self.out.fillBranch("photon1_isScEtaEE",photons[selected_tight_or_control_photons[0]].isScEtaEE)
            self.out.fillBranch("photon1_isScEtaEB",photons[selected_tight_or_control_photons[0]].isScEtaEB)
            self.out.fillBranch("photon1_gen_matching",photon1_gen_matching)
            self.out.fillBranch("photon1_genpart_pdgid",photon1_genpart_pdgid)
            self.out.fillBranch("photon1_genpart_pt",photon1_genpart_pt)
            self.out.fillBranch("photon1_genjet_matching",photon1_genjet_matching)
            self.out.fillBranch("photon1_moth_genpart_pdgid",photon1_moth_genpart_pdgid)
            self.out.fillBranch("photon1_moth_genpart_pt",photon1_moth_genpart_pt)
            self.out.fillBranch("photon1_gen_matching_old",photon1_gen_matching_old)
            self.out.fillBranch("njets_fake",njets_fake)
        else:
            self.out.fillBranch("photon1_sieie",0)
            self.out.fillBranch("photon1_pfRelIso03_chg",0)
            self.out.fillBranch("photon1_pt",0)
            self.out.fillBranch("photon1_phi",0)
            self.out.fillBranch("photon1_eta",0)
            self.out.fillBranch("photon1_isScEtaEE",0)
            self.out.fillBranch("photon1_isScEtaEB",0)
            self.out.fillBranch("photon1_gen_matching",0)
            self.out.fillBranch("photon1_genpart_pdgid",0)
            self.out.fillBranch("photon1_genpart_pt",0)
            self.out.fillBranch("photon1_genjet_matching",0)
            self.out.fillBranch("photon1_moth_genpart_pdgid",0)
            self.out.fillBranch("photon1_moth_genpart_pt",0)
            self.out.fillBranch("photon1_gen_matching_old",0)
            self.out.fillBranch("njets_fake",0)
            self.out.fillBranch("photon1_selection",0)

        if pass_selection2:
            photon2_gen_matching = 0
            photon2_gen_matching_old=0
            photon2_genpart_pdgid=0
            photon2_genpart_pt=0
            photon2_moth_genpart_pdgid=0
            photon2_moth_genpart_pt=0

            isprompt_mask = (1 << 0) #isPrompt
            isfromhardprocess_mask = (1 << 8) #isFromHardProcess 
            isprompttaudecayproduct_mask = (1 << 4) #isPromptTauDecayProduct
            isdirectprompttaudecayproduct_mask = (1 << 5) #isDirectPromptTauDecayProduct

            photon2_genjet_matching = 0
                        
            if hasattr(event,'nGenJet'):
                for i in range(0,len(genjets)):
                    if genjets[i].pt > 10 and deltaR(genjets[i].eta,genjets[i].phi,photons[selected_fake_template_photons[0]].eta,photons[selected_fake_template_photons[0]].phi) < 0.5:
                        photon2_genjet_matching = 1

            if hasattr(photons[selected_fake_template_photons[0]],'genPartIdx'):

                if photons[selected_fake_template_photons[0]].genPartIdx >= 0:
                    photon2_genpart_pdgid =  genparts[photons[selected_fake_template_photons[0]].genPartIdx].pdgId
                    photon2_genpart_pt =  genparts[photons[selected_fake_template_photons[0]].genPartIdx].pt
                    if genparts[photons[selected_fake_template_photons[0]].genPartIdx].genPartIdxMother >= 0:
                        photon2_moth_genpart_pdgid = genparts[genparts[photons[selected_fake_template_photons[0]].genPartIdx].genPartIdxMother].pdgId
                        photon2_moth_genpart_pt = genparts[genparts[photons[selected_fake_template_photons[0]].genPartIdx].genPartIdxMother].pt
                

                if photons[selected_fake_template_photons[0]].genPartIdx >= 0 and genparts[photons[selected_fake_template_photons[0]].genPartIdx].pdgId  == 22:
                    if ((genparts[photons[selected_fake_template_photons[0]].genPartIdx].statusFlags & isprompt_mask == isprompt_mask) or (genparts[photons[selected_fake_template_photons[0]].genPartIdx].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and (genparts[photons[selected_fake_template_photons[0]].genPartIdx].statusFlags & isfromhardprocess_mask == isfromhardprocess_mask):
                        photon2_gen_matching = 6
                    elif ((genparts[photons[selected_fake_template_photons[0]].genPartIdx].statusFlags & isprompt_mask == isprompt_mask) or (genparts[photons[selected_fake_template_photons[0]].genPartIdx].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)):
                        if (genparts[photons[selected_fake_template_photons[0]].genPartIdx].genPartIdxMother >= 0 and (abs(genparts[genparts[photons[selected_fake_template_photons[0]].genPartIdx].genPartIdxMother].pdgId) == 11 or abs(genparts[genparts[photons[selected_fake_template_photons[0]].genPartIdx].genPartIdxMother].pdgId) == 13 or abs(genparts[genparts[photons[selected_fake_template_photons[0]].genPartIdx].genPartIdxMother].pdgId) == 15)):
                            photon2_gen_matching = 4
                        else:
                            photon2_gen_matching = 5
                    else:
                        photon2_gen_matching = 3
                elif photons[selected_fake_template_photons[0]].genPartIdx >= 0 and abs(genparts[photons[selected_fake_template_photons[0]].genPartIdx].pdgId) == 11:
                    if ((genparts[photons[selected_fake_template_photons[0]].genPartIdx].statusFlags & isprompt_mask == isprompt_mask) or (genparts[photons[selected_fake_template_photons[0]].genPartIdx].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)):
                        photon2_gen_matching = 1
                    else:
                        photon2_gen_matching = 2

                else:
                    assert(photons[selected_fake_template_photons[0]].genPartFlav == 0)


            if hasattr(event,'nGenPart'):

                for i in range(0,len(genparts)):
                    if genparts[i].pt > 5 and genparts[i].status == 1 and abs(genparts[i].pdgId) == 13 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and deltaR(photons[selected_fake_template_photons[0]].eta,photons[selected_fake_template_photons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        photon2_gen_matching_old += 1 #m -> g

                    if genparts[i].pt > 5 and genparts[i].status == 1 and abs(genparts[i].pdgId) == 11 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and deltaR(photons[selected_fake_template_photons[0]].eta,photons[selected_fake_template_photons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        photon2_gen_matching_old += 2 #e -> g

                    if genparts[i].pt > 5 and genparts[i].status == 1 and genparts[i].pdgId == 22 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and deltaR(photons[selected_fake_template_photons[0]].eta,photons[selected_fake_template_photons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        if genparts[i].genPartIdxMother >= 0 and (abs(genparts[genparts[i].genPartIdxMother].pdgId) == 11 or abs(genparts[genparts[i].genPartIdxMother].pdgId) == 13 or abs(genparts[genparts[i].genPartIdxMother].pdgId) == 15):
                            photon2_gen_matching_old += 8 #fsr photon
                        else:
                            photon2_gen_matching_old += 4 #non-fsr photon

            self.out.fillBranch("photon2_sieie",photons[selected_fake_template_photons[0]].sieie)
            self.out.fillBranch("photon2_pfRelIso03_chg",photons[selected_fake_template_photons[0]].pfRelIso03_chg)
            self.out.fillBranch("photon2_pt",photons[selected_fake_template_photons[0]].pt)
            self.out.fillBranch("photon2_phi",photons[selected_fake_template_photons[0]].phi)
            self.out.fillBranch("photon2_eta",photons[selected_fake_template_photons[0]].eta)
            self.out.fillBranch("photon2_isScEtaEE",photons[selected_fake_template_photons[0]].isScEtaEE)
            self.out.fillBranch("photon2_isScEtaEB",photons[selected_fake_template_photons[0]].isScEtaEB)
            self.out.fillBranch("photon2_gen_matching",photon2_gen_matching)
            self.out.fillBranch("photon2_genpart_pdgid",photon2_genpart_pdgid)
            self.out.fillBranch("photon2_genpart_pt",photon2_genpart_pt)
            self.out.fillBranch("photon2_genjet_matching",photon2_genjet_matching)
            self.out.fillBranch("photon2_moth_genpart_pdgid",photon2_moth_genpart_pdgid)
            self.out.fillBranch("photon2_moth_genpart_pt",photon2_moth_genpart_pt)
            self.out.fillBranch("photon2_gen_matching_old",photon2_gen_matching_old)
            self.out.fillBranch("njets_fake_template",njets_fake_template)

        else:
            self.out.fillBranch("photon2_sieie",0)
            self.out.fillBranch("photon2_pfRelIso03_chg",0)
            self.out.fillBranch("photon2_pt",0)
            self.out.fillBranch("photon2_phi",0)
            self.out.fillBranch("photon2_eta",0)
            self.out.fillBranch("photon2_isScEtaEE",0)
            self.out.fillBranch("photon2_isScEtaEB",0)
            self.out.fillBranch("photon2_gen_matching",0)
            self.out.fillBranch("photon2_genpart_pdgid",0)
            self.out.fillBranch("photon2_genpart_pt",0)
            self.out.fillBranch("photon2_genjet_matching",0)
            self.out.fillBranch("photon2_moth_genpart_pdgid",0)
            self.out.fillBranch("photon2_moth_genpart_pt",0)
            self.out.fillBranch("photon2_gen_matching_old",0)
            self.out.fillBranch("njets_fake_template",0)

        if hasattr(event,'Generator_weight'):
            self.out.fillBranch("gen_weight",event.Generator_weight)


        n_gen_leptons = 0
        n_gen_neutrinos = 0
        n_gen_photons = 0

        gen_leptons = ROOT.TLorentzVector()
        gen_neutrinos = ROOT.TLorentzVector()
        gen_photons  = ROOT.TLorentzVector()

        if hasattr(event,'nGenPart'):

            
            isprompt_mask = (1 << 0) #isPrompt
            isdirectprompttaudecayproduct_mask = (1 << 5) #isDirectPromptTauDecayProduct
            isfromhardprocess_mask = (1 << 8) #isPrompt

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

        self.out.fillBranch("n_gen_leptons",n_gen_leptons)
        self.out.fillBranch("n_gen_photons",n_gen_photons)
        self.out.fillBranch("n_gen_neutrinos",n_gen_neutrinos)
        self.out.fillBranch("gen_leptons_pt",gen_leptons.Pt())
        self.out.fillBranch("gen_leptons_phi",gen_leptons.Phi())
        self.out.fillBranch("gen_neutrinos_pt",gen_neutrinos.Pt())
        self.out.fillBranch("gen_neutrinos_phi",gen_neutrinos.Phi())
        self.out.fillBranch("gen_photons_pt",gen_photons.Pt())
        self.out.fillBranch("gen_photons_phi",gen_photons.Phi())
        self.out.fillBranch("met",event.MET_pt)
        self.out.fillBranch("puppimet",event.PuppiMET_pt)
        self.out.fillBranch("metphi",event.MET_phi)
        self.out.fillBranch("puppimetphi",event.PuppiMET_phi)
        self.out.fillBranch("event",event.event)
        self.out.fillBranch("lumi",event.luminosityBlock)
        self.out.fillBranch("run",event.run)

        self.out.fillBranch("npvs",event.PV_npvs)

        if hasattr(event,'Pileup_nPU'):
            self.out.fillBranch("npu",event.Pileup_nPU)
        else:
            self.out.fillBranch("npu",0)

        return True

wgFakePhotonModule = lambda : wgFakePhotonProducer()
