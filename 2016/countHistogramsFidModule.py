import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

class countHistogramsFidProducer(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.h_nweightedeventspassfiducial=ROOT.TH1F('nWeightedEventsPassFiducial',   'nWeightedEventsPassFiducial',   1, 0, 1)

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        prevdir = ROOT.gDirectory
        outputFile.cd()
        self.h_nweightedeventspassfiducial.Write()
        prevdir.cd()        
    def analyze(self, event):
        try:

            genparts = Collection(event, "GenPart")
            
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
                    pass_fiducial = True
                else:
                    pass_fiducial = False
            else:        
                pass_fiducial = False

            if pass_fiducial:    
                if event.Generator_weight > 0:
                    self.h_nweightedeventspassfiducial.Fill(0.5)
                else:
                    self.h_nweightedeventspassfiducial.Fill(0.5,-1)
        except:
            pass


        return True

countHistogramsFidModule = lambda : countHistogramsFidProducer() 

