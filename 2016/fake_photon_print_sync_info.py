import ROOT

data_f = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/single_electron_fake_photon.root")
data_tree = data_f.Get("Events")

data_tree.SetScanField(0)

data_tree.Scan("run:lumi:event","abs(photon_eta) < 1.4442 && lepton_pdg_id == 11 && (photon_selection == 1 || photon_selection == 2) && photon_pt > 30 && photon_pt < 40","colsize=10")
