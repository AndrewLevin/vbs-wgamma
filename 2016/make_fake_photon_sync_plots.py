import ROOT

#n_bins = 128
n_bins = 200
sieie_lower = 0.00
sieie_upper = 0.04

jie_data_f = ROOT.TFile.Open("/afs/cern.ch/work/j/jixiao/public/WGamma/data_template_30_40.root")
jie_fake_template_f = ROOT.TFile.Open("/afs/cern.ch/work/j/jixiao/public/WGamma/fake_template_30_40.root")
jie_real_template_f = ROOT.TFile.Open("/afs/cern.ch/work/j/jixiao/public/WGamma/true_template_30_40.root")

jie_data_hist = jie_data_f.Get("histo")
jie_fake_template_hist = jie_real_template_f.Get("histo")
jie_real_template_hist = jie_fake_template_f.Get("histo")

jie_data_hist.SetStats(0)
jie_fake_template_hist.SetStats(0)
jie_real_template_hist.SetStats(0)
jie_data_hist.SetTitle("")
jie_fake_template_hist.SetTitle("")
jie_real_template_hist.SetTitle("")

data_f = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/single_electron_fake_photon.root")
fake_template_f = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/single_electron_fake_photon_template.root")
real_template_f = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/real_photon_template.root")

data_tree = data_f.Get("Events")
data_hist = ROOT.TH1F("data_hist","data_hist",n_bins,sieie_lower,sieie_upper)
data_tree.Draw("photon_sieie >> data_hist","abs(photon_eta) < 1.4442 && lepton_pdg_id == 11 && (photon_selection == 1 || photon_selection == 2) && photon_pt > 30 && photon_pt < 40")
data_hist.SetStats(0)            
data_hist.SetTitle("")            


fake_template_tree = fake_template_f.Get("Events")
fake_template_hist = ROOT.TH1F("fake_template_hist","fake_template_hist",n_bins,sieie_lower,sieie_upper)
fake_template_tree.Draw("photon_sieie >> fake_template_hist","abs(photon_eta) < 1.4442 && lepton_pdg_id == 1 && photon_pt > 30 && photon_pt < 40")
fake_template_hist.SetStats(0)
fake_template_hist.SetTitle("")

real_template_tree = real_template_f.Get("Events")
real_template_hist = ROOT.TH1F("real_template_hist","real_template_hist",n_bins,sieie_lower,sieie_upper)
real_template_hist.SetStats(0)
real_template_hist.SetTitle("")

for i in range(real_template_tree.GetEntries()):
    real_template_tree.GetEntry(i)
    
    if abs(real_template_tree.photon_eta) > 1.4442:
        pass_eta_range = True

    if str(real_template_tree.lepton_pdg_id) != "11":
        pass_lepton_pdg_id = True

    if not(real_template_tree.photon_pt > 30 and real_template_tree.photon_pt < 40):
        continue

    if real_template_tree.gen_weight > 0:
        real_template_hist.Fill(real_template_tree.photon_sieie)
    else:    
        real_template_hist.Fill(real_template_tree.photon_sieie,-1)

c1 = ROOT.TCanvas("c1","c1")

leg1 = ROOT.TLegend(0.6, 0.7, 0.89, 0.89)
leg1.AddEntry(jie_real_template_hist,"Jie","lp")
leg1.AddEntry(real_template_hist,"Andrew","lp")

real_template_hist.SetLineColor(ROOT.kRed)
jie_real_template_hist.SetLineColor(ROOT.kBlue)

real_template_hist.Draw()
jie_real_template_hist.Draw("same")
leg1.Draw("same")

c1.SaveAs("/eos/user/a/amlevin/www/tmp/real_template.png")

c2 = ROOT.TCanvas("c2","c2")

leg2 = ROOT.TLegend(0.6, 0.7, 0.89, 0.89)
leg2.AddEntry(jie_fake_template_hist,"Jie","lp")
leg2.AddEntry(fake_template_hist,"Andrew","lp")

fake_template_hist.SetLineColor(ROOT.kRed)
jie_fake_template_hist.SetLineColor(ROOT.kBlue)

fake_template_hist.Draw()
jie_fake_template_hist.Draw("same")
leg2.Draw("same")

c2.SaveAs("/eos/user/a/amlevin/www/tmp/fake_template.png")

c3 = ROOT.TCanvas("c3","c3")

leg3 = ROOT.TLegend(0.6, 0.7, 0.89, 0.89)
leg3.AddEntry(jie_data_hist,"Jie","lp")
leg3.AddEntry(data_hist,"Andrew","lp")

data_hist.SetLineColor(ROOT.kRed)
jie_data_hist.SetLineColor(ROOT.kBlue)

data_hist.Scale(1/data_hist.Integral())
jie_data_hist.Scale(1/jie_data_hist.Integral())

jie_data_hist.Draw()
data_hist.Draw("same")


leg3.Draw("same")

c3.SaveAs("/eos/user/a/amlevin/www/tmp/data.png")
