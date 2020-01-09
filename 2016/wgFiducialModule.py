import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

class wgFiducialProducer(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("pass_fid_selection",  "B");
        self.out.branch("fid_met_pt",  "F");
        self.out.branch("fid_met_phi",  "F");
        self.out.branch("fid_lepton_pt",  "F");
        self.out.branch("fid_lepton_phi",  "F");
        self.out.branch("fid_lepton_eta",  "F");
        self.out.branch("fid_lepton_mass",  "F");
        self.out.branch("fid_photon_pt",  "F");
        self.out.branch("fid_photon_phi",  "F");
        self.out.branch("fid_photon_eta",  "F");
        self.out.branch("fid_photon_mass",  "F");

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        prevdir = ROOT.gDirectory
        outputFile.cd()
        prevdir.cd()        
    def analyze(self, event):
        genparts = Collection(event, "MergedGenPart")
            
        n_gen_leptons = 0
        n_gen_photons = 0

        for j in range(0,len(genparts)):

            if genparts[j].pt > 25 and genparts[j].status == 1 and (abs(genparts[j].pdgId) == 11 or abs(genparts[j].pdgId) == 13):
                lep_iso=0
                for k in range(0,len(genparts)):
                    
                    if k == j:
                        continue
                    
                    if  genparts[k].status != 1:
                        continue
                    
                    if abs(genparts[k].pdgId) == 12 or abs(genparts[k].pdgId) == 14 or abs(genparts[k].pdgId) == 16:
                        continue
                    
                    if deltaR(genparts[k].eta,genparts[k].phi,genparts[j].eta,genparts[j].phi) < 0.4:
                        lep_iso += genparts[k].pt
                        
                lep_iso /= genparts[j].pt

                if lep_iso < 0.5:
                    if n_gen_leptons == 0:
                        gen_lepton_index = j
                    n_gen_leptons +=1

            if genparts[j].pt > 25 and genparts[j].status == 1 and genparts[j].pdgId == 22 and abs(genparts[j].eta) < 2.5:
                pho_iso=0
                for k in range(0,len(genparts)):

                    if k == j:
                        continue
                        
                    if  genparts[k].status != 1:
                        continue

                    if abs(genparts[k].pdgId) == 12 or abs(genparts[k].pdgId) == 14 or abs(genparts[k].pdgId) == 16:
                        continue

                    if deltaR(genparts[k].eta,genparts[k].phi,genparts[j].eta,genparts[j].phi) < 0.4:
                        pho_iso += genparts[k].pt

                    pho_iso /= genparts[j].pt

                    if pho_iso < 0.5:
                        if n_gen_photons == 0:
                            gen_photon_index = j
                        n_gen_photons +=1

        pass_fid_selection = False

        if n_gen_leptons >= 1 and n_gen_photons >= 1:
#            if deltaR(genparts[gen_lepton_index].eta,genparts[gen_lepton_index].phi,genparts[gen_photon_index].eta,genparts[gen_photon_index].phi) > 0.5 and genparts[gen_lepton_index].pt > 25 and genparts[gen_photon_index].pt > 25 and abs(genparts[gen_lepton_index].eta) < 2.5 and abs(genparts[gen_photon_index].eta) < 2.5 and event.GenMET_pt > 40:
            if deltaR(genparts[gen_lepton_index].eta,genparts[gen_lepton_index].phi,genparts[gen_photon_index].eta,genparts[gen_photon_index].phi) > 0.5 and genparts[gen_lepton_index].pt > 25 and genparts[gen_photon_index].pt > 25 and abs(genparts[gen_lepton_index].eta) < 2.5 and abs(genparts[gen_photon_index].eta) < 2.5 and event.GenMET_pt > 40 and (genparts[gen_photon_index].statusFlags & (1 << 0) == (1 << 0) and ((genparts[gen_lepton_index].statusFlags & (1 << 0) == (1 << 0)) or (genparts[gen_lepton_index].statusFlags & (1 << 5) == (1 << 5)))):
                pass_fid_selection = True

        if pass_fid_selection:    
            self.out.fillBranch("pass_fid_selection",1)
            self.out.fillBranch("fid_met_pt",event.GenMET_pt)
            self.out.fillBranch("fid_met_phi",event.GenMET_phi)
            self.out.fillBranch("fid_lepton_pt",genparts[gen_lepton_index].pt)
            self.out.fillBranch("fid_lepton_eta",genparts[gen_lepton_index].eta)
            self.out.fillBranch("fid_lepton_phi",genparts[gen_lepton_index].phi)
            self.out.fillBranch("fid_lepton_mass",genparts[gen_lepton_index].mass)
            self.out.fillBranch("fid_photon_pt",genparts[gen_photon_index].pt)
            self.out.fillBranch("fid_photon_eta",genparts[gen_photon_index].eta)
            self.out.fillBranch("fid_photon_phi",genparts[gen_photon_index].phi)
            self.out.fillBranch("fid_photon_mass",genparts[gen_photon_index].mass)
        else:    
            self.out.fillBranch("pass_fid_selection",0)

        return True

wgFiducialModule = lambda : wgFiducialProducer() 
