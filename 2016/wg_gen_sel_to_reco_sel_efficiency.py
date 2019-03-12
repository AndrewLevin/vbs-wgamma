import ROOT

lepton_pdgid = "13"

#h_gen_photon_pt_powheg_plus_num_pos

ROOT.gROOT.cd()

h_gen_photon_pt_powheg_plus_num_neg = ROOT.TH1F("h_gen_photon_pt_powheg_plus_num_neg","h_gen_photon_pt_powheg_plus_num_neg",9,20,200)
h_gen_photon_pt_powheg_minus_num_neg = ROOT.TH1F("h_gen_photon_pt_powheg_minus_num_neg","h_gen_photon_pt_powheg_minus_num_neg",9,20,200)
h_gen_photon_pt_powheg_plus_den_neg = ROOT.TH1F("h_gen_photon_pt_powheg_plus_den_neg","h_gen_photon_pt_powheg_plus_den_neg",9,20,200)
h_gen_photon_pt_powheg_minus_den_neg = ROOT.TH1F("h_gen_photon_pt_powheg_minus_den_neg","h_gen_photon_pt_powheg_minus_den_neg",9,20,200)

h_gen_photon_pt_powheg_plus_den_pos = ROOT.TH1F("h_gen_photon_pt_powheg_plus_den_pos","h_gen_photon_pt_powheg_plus_den_pos",9,20,200)
h_gen_photon_pt_powheg_minus_den_pos = ROOT.TH1F("h_gen_photon_pt_powheg_minus_den_pos","h_gen_photon_pt_powheg_minus_den_pos",9,20,200)
h_gen_photon_pt_powheg_plus_num_pos = ROOT.TH1F("h_gen_photon_pt_powheg_plus_num_pos","h_gen_photon_pt_powheg_plus_num_pos",9,20,200)
h_gen_photon_pt_powheg_minus_num_pos = ROOT.TH1F("h_gen_photon_pt_powheg_minus_num_pos","h_gen_photon_pt_powheg_minus_num_pos",9,20,200)


h_gen_photon_pt_mg5amc_num_neg = ROOT.TH1F("h_gen_photon_pt_mg5amc_num_neg","h_gen_photon_pt_mg5amc_num_neg",9,20,200)
h_gen_photon_pt_mg5amc_den_neg = ROOT.TH1F("h_gen_photon_pt_mg5amc_den_neg","h_gen_photon_pt_mg5amc_den_neg",9,20,200)
h_gen_photon_pt_mg5amc_den_pos = ROOT.TH1F("h_gen_photon_pt_mg5amc_den_pos","h_gen_photon_pt_mg5amc_den_pos",9,20,200)
h_gen_photon_pt_mg5amc_num_pos = ROOT.TH1F("h_gen_photon_pt_mg5amc_num_pos","h_gen_photon_pt_mg5amc_num_pos",9,20,200)

h_gen_photon_pt_powheg_plus_num_neg.Sumw2()
h_gen_photon_pt_powheg_minus_num_neg.Sumw2()
h_gen_photon_pt_powheg_plus_den_neg.Sumw2()
h_gen_photon_pt_powheg_minus_den_neg.Sumw2()

h_gen_photon_pt_powheg_plus_den_pos.Sumw2()
h_gen_photon_pt_powheg_minus_den_pos.Sumw2()
h_gen_photon_pt_powheg_plus_num_pos.Sumw2()
h_gen_photon_pt_powheg_minus_num_pos.Sumw2()

h_gen_photon_pt_mg5amc_num_neg.Sumw2()
h_gen_photon_pt_mg5amc_den_neg.Sumw2()
h_gen_photon_pt_mg5amc_den_pos.Sumw2()
h_gen_photon_pt_mg5amc_num_pos.Sumw2()

powheg_wpgjets_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/2016/gen/wpg_powheg.root")
powheg_wmgjets_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/2016/gen/wmg_powheg.root")
wgjets_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/2016/gen/wgjets.root")

powheg_wpgjets_tree = powheg_wpgjets_file.Get("Events")
powheg_wmgjets_tree = powheg_wmgjets_file.Get("Events")
wgjets_tree = wgjets_file.Get("Events")

ROOT.gROOT.cd()

wgjets_tree.Draw("gen_photon_pt >> h_gen_photon_pt_mg5amc_num_pos","pass_gen_selection && pass_selection && is_lepton_tight && photon_selection == 2 && abs(gen_lepton_pdgid) == "+str(lepton_pdgid)+" && photon_gen_matching > 0 && gen_weight > 0")

wgjets_tree.Draw("gen_photon_pt >> h_gen_photon_pt_mg5amc_num_neg","pass_gen_selection && pass_selection && is_lepton_tight && photon_selection == 2 && abs(gen_lepton_pdgid) == "+str(lepton_pdgid)+" && photon_gen_matching > 0 && gen_weight < 0")

wgjets_tree.Draw("gen_photon_pt >> h_gen_photon_pt_mg5amc_den_pos","abs(gen_lepton_pdgid) == "+str(lepton_pdgid)+" && pass_gen_selection && gen_weight > 0")

wgjets_tree.Draw("gen_photon_pt >> h_gen_photon_pt_mg5amc_den_neg","abs(gen_lepton_pdgid) == "+str(lepton_pdgid)+" && pass_gen_selection && gen_weight < 0")

powheg_wpgjets_tree.Draw("gen_photon_pt >> h_gen_photon_pt_powheg_plus_num_pos","pass_gen_selection && pass_selection && is_lepton_tight && photon_selection == 2 && abs(gen_lepton_pdgid) == "+str(lepton_pdgid)+" && photon_gen_matching > 0 && gen_weight > 0")

powheg_wpgjets_tree.Draw("gen_photon_pt >> h_gen_photon_pt_powheg_plus_num_neg","pass_gen_selection && pass_selection && is_lepton_tight && photon_selection == 2 && abs(gen_lepton_pdgid) == "+str(lepton_pdgid)+" && photon_gen_matching > 0 && gen_weight < 0")

powheg_wpgjets_tree.Draw("gen_photon_pt >> h_gen_photon_pt_powheg_plus_den_pos","abs(gen_lepton_pdgid) == "+str(lepton_pdgid)+" && pass_gen_selection && gen_weight > 0")

powheg_wpgjets_tree.Draw("gen_photon_pt >> h_gen_photon_pt_powheg_plus_den_neg","abs(gen_lepton_pdgid) == "+str(lepton_pdgid)+" && pass_gen_selection && gen_weight < 0")

powheg_wmgjets_tree.Draw("gen_photon_pt >> h_gen_photon_pt_powheg_minus_num_pos","pass_gen_selection && pass_selection && is_lepton_tight && photon_selection == 2 && abs(gen_lepton_pdgid) == "+str(lepton_pdgid)+" && photon_gen_matching > 0 && gen_weight > 0")

powheg_wmgjets_tree.Draw("gen_photon_pt >> h_gen_photon_pt_powheg_minus_num_neg","pass_gen_selection && pass_selection && is_lepton_tight && photon_selection == 2 && abs(gen_lepton_pdgid) == "+str(lepton_pdgid)+" && photon_gen_matching > 0 && gen_weight < 0")

powheg_wmgjets_tree.Draw("gen_photon_pt >> h_gen_photon_pt_powheg_minus_den_pos","abs(gen_lepton_pdgid) == "+str(lepton_pdgid)+" && pass_gen_selection && gen_weight > 0")

powheg_wmgjets_tree.Draw("gen_photon_pt >> h_gen_photon_pt_powheg_minus_den_neg","abs(gen_lepton_pdgid) == "+str(lepton_pdgid)+" && pass_gen_selection && gen_weight < 0")

h_gen_photon_pt_mg5amc_num_neg.Scale(-1)
h_gen_photon_pt_mg5amc_den_neg.Scale(-1)
h_gen_photon_pt_powheg_minus_num_neg.Scale(-24780./33420.)
h_gen_photon_pt_powheg_minus_den_neg.Scale(-24780./33420.)
h_gen_photon_pt_powheg_plus_num_neg.Scale(-1)
h_gen_photon_pt_powheg_plus_den_neg.Scale(-1)

h_gen_photon_pt_mg5amc_num_pos.Add(h_gen_photon_pt_mg5amc_num_neg)
h_gen_photon_pt_mg5amc_den_pos.Add(h_gen_photon_pt_mg5amc_den_neg)

h_gen_photon_pt_powheg_minus_num_pos.Add(h_gen_photon_pt_powheg_minus_num_neg)
h_gen_photon_pt_powheg_minus_den_pos.Add(h_gen_photon_pt_powheg_minus_den_neg)
h_gen_photon_pt_powheg_plus_num_pos.Add(h_gen_photon_pt_powheg_plus_num_neg)
h_gen_photon_pt_powheg_plus_den_pos.Add(h_gen_photon_pt_powheg_plus_den_neg)

h_gen_photon_pt_powheg_plus_num_pos.Add(h_gen_photon_pt_powheg_minus_num_pos)
h_gen_photon_pt_powheg_plus_den_pos.Add(h_gen_photon_pt_powheg_minus_den_pos)

h_gen_photon_pt_powheg_plus_num_pos.Divide(h_gen_photon_pt_powheg_plus_den_pos)

h_gen_photon_pt_mg5amc_num_pos.Divide(h_gen_photon_pt_mg5amc_den_pos)

c = ROOT.TCanvas()

h_gen_photon_pt_powheg_plus_num_pos.SetStats(0)
h_gen_photon_pt_powheg_plus_num_pos.SetMinimum(0)
h_gen_photon_pt_powheg_plus_num_pos.SetMaximum(0.6)
h_gen_photon_pt_powheg_plus_num_pos.Draw()

h_gen_photon_pt_mg5amc_num_pos.SetLineColor(ROOT.kRed)

h_gen_photon_pt_mg5amc_num_pos.Draw("same")

c.SaveAs("/eos/user/a/amlevin/www/tmp/delete_this.png")
