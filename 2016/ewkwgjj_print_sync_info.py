import ROOT

f=ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/ewkwgjj/wgjets.root")
t=f.Get("Events")

t.SetScanField(0)

t.Scan("run:lumi:event","photon_pt > 30 && lepton_pdg_id == 11 && photon_pt < 135 && photon_selection == 2 && is_lepton_tight == 1 && met > 30 && mt > 30 && (mlg < 75 || mlg > 105) && 1.566 < abs(photon_eta) && abs(photon_eta) < 2.5 && btagging_selection == 1 && mjj > 200 && mjj < 400")
