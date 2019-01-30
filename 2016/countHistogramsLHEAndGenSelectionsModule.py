import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

class countHistogramsLHEAndGenSelectionsProducer(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.h_nweightedeventspassgenselection=ROOT.TH1D('nWeightedEventsPassGenSelection',   'nWeightedEventsPassGenSelection',   1, 0, 1)
        self.h_nweightedeventspasslheselection=ROOT.TH1D('nWeightedEventsPassLHESelection',   'nWeightedEventsPassLHESelection',   1, 0, 1)
        self.h_nweightedeventspasslheandgenselection=ROOT.TH1D('nWeightedEventsPassLHEAndGenSelection',   'nWeightedEventsPassLHEAndGenSelection',   1, 0, 1)
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        prevdir = ROOT.gDirectory
        outputFile.cd()
        self.h_nweightedeventspassgenselection.Write()
        self.h_nweightedeventspasslheselection.Write()
        self.h_nweightedeventspasslheandgenselection.Write()
        prevdir.cd()        
    def analyze(self, event):
        if True:

            genparts = Collection(event, "GenPart")
            lheparts = Collection(event, "LHEPart")
            
            isprompt_mask = (1 << 0) #isPrompt
            isfromhardprocess_mask = (1 << 8) #isFromHardProcess
            isprompttaudecayproduct_mask = (1 << 4) #isPromptTauDecayProduct

            n_gen_leptons = 0
            n_gen_photons = 0
            for i in range(0,len(genparts)):
                if genparts[i].pt > 5 and genparts[i].status == 1 and (abs(genparts[i].pdgId) == 11 or abs(genparts[i].pdgId) == 13 or abs(genparts[i].pdgId) == 15) and (genparts[i].statusFlags & isfromhardprocess_mask == isfromhardprocess_mask) and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct_mask == isprompttaudecayproduct_mask)):
                    gen_lepton_index = i
                    n_gen_leptons +=  1
                if genparts[i].pt > 5 and genparts[i].status == 1 and genparts[i].pdgId == 22 and (genparts[i].statusFlags & isfromhardprocess_mask == isfromhardprocess_mask) and (genparts[i].statusFlags & isprompt_mask == isprompt_mask):
                    gen_photon_index = i
                    n_gen_photons +=1

            if n_gen_leptons == 1 and n_gen_photons == 1:
                if deltaR(genparts[gen_lepton_index].eta,genparts[gen_lepton_index].phi,genparts[gen_photon_index].eta,genparts[gen_photon_index].phi) > 0.7 and genparts[gen_lepton_index].pt > 20 and genparts[gen_photon_index].pt > 20 and abs(genparts[gen_photon_index].eta) < 2.5:
                    pass_gen_selection = True
                else:
                    pass_gen_selection = False
            else:        
                pass_gen_selection = False

            n_lhe_photons = 0
            n_lhe_leptons = 0

            for i in range(0,len(lheparts)):
                if lheparts[i].pdgId == 22:
                    lhe_photon_index=i
                    n_lhe_photons+=1
                    
                if abs(lheparts[i].pdgId) == 11 or abs(lheparts[i].pdgId) == 13 or abs(lheparts[i].pdgId) == 15:
                    lhe_lepton_index=i
                    n_lhe_leptons+=1

            #n_lhe_photons may be 0 for POWHEG        
            assert((n_lhe_leptons == 1 and n_lhe_photons == 1) or (n_lhe_leptons == 1 and n_lhe_photons == 0))  


            if n_lhe_leptons == 1 and n_lhe_photons == 1:
                if deltaR(lheparts[lhe_lepton_index].eta,lheparts[lhe_lepton_index].phi,lheparts[lhe_photon_index].eta,lheparts[lhe_photon_index].phi) > 0.1 and lheparts[lhe_lepton_index].pt > 15 and lheparts[lhe_photon_index].pt > 15 and abs(lheparts[lhe_photon_index].eta) < 2.6:
                    pass_lhe_selection = True
                else:
                    pass_lhe_selection = False

                if pass_lhe_selection:    
                    if event.Generator_weight > 0:
                        self.h_nweightedeventspasslheselection.Fill(0.5)
                    else:
                        self.h_nweightedeventspasslheselection.Fill(0.5,-1)

                if pass_gen_selection:    
                    if event.Generator_weight > 0:
                        self.h_nweightedeventspassgenselection.Fill(0.5)
                    else:
                        self.h_nweightedeventspassgenselection.Fill(0.5,-1)
                
                if pass_lhe_selection and pass_gen_selection:        
                    if event.Generator_weight > 0:
                        self.h_nweightedeventspasslheandgenselection.Fill(0.5)
                    else:
                        self.h_nweightedeventspasslheandgenselection.Fill(0.5,-1)

        return True

countHistogramsLHEAndGenSelectionsModule = lambda : countHistogramsLHEAndGenSelectionsProducer() 

