#there is a bug which causes a crash inside of the TFractionFitter destructor: https://sft.its.cern.ch/jira/browse/ROOT-9414
#I think this makes it necessary to create the tfractionfitters only once for each set of input files that are used, and then reuse the tfractionfitters

import sys
import random
import ROOT

ROOT.gStyle.SetOptStat(0)

met_cut = 30

fake_fractions = {}

fake_event_weights = {}

total_met_for_fake_electron_fraction_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/single_electron_fake_electron.root") 
fake_electron_template_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/single_electron_fake_electron_template.root")
real_electron_template_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/real_electron_template.root")

total_met_for_fake_electron_fraction_tree = total_met_for_fake_electron_fraction_file.Get("Events")
total_met_for_fake_electron_fraction_hist = ROOT.TH1F("total_met_for_fake_electron_fraction_hist","total_met_for_fake_electron_fraction_hist",n_bins,sieie_lower,sieie_upper)
total_met_for_fake_electron_fraction_tree.Draw("met >> total_met_for_fake_electron_fraction_hist","(electron_selection == 1 || electron_selection == 2)")
            
fake_electron_template_tree = fake_electron_template_file.Get("Events")
fake_electron_template_hist = ROOT.TH1F("fake_electron_template_hist","fake_electron_template_hist",n_bins,met_lower,met_upper)
fake_electron_template_tree.Draw("met >> fake_electron_template_hist")

real_electron_template_tree = real_electron_template_file.Get("Events")
real_electron_template_hist = ROOT.TH1F("real_electron_template_hist","real_electron_template_hist",n_bins,met_lower,met_upper)

for i in range(real_electron_template_tree.GetEntries()):
    real_electron_template_tree.GetEntry(i)

    if real_electron_template_tree.gen_weight > 0:
        real_electron_template_hist.Fill(real_electron_template_tree.electron_sieie)
    else:    
        real_electron_template_hist.Fill(real_electron_template_tree.electron_sieie,-1)

for i in range(real_electron_template_hist.GetNbinsX()+2):
    if real_electron_template_hist.GetBinContent(i) < 0:
        real_electron_template_hist.SetBinContent(i,0)

mc = ROOT.TObjArray(2)
        
mc.Add(fake_electron_template_hist)
mc.Add(real_electron_template_hist)

ffitter = ROOT.TFractionFitter(total_met_for_fake_electron_fraction_hist,mc)
            
c1 = ROOT.TCanvas("c1", "c1",5,50,500,500);

real_electron_template_hist.Draw("hist")

c1.SaveAs("/eos/user/a/amlevin/www/fake-electron/real_electron_template.png")

fake_electron_template_hist.Draw("hist")

c1.SaveAs("/eos/user/a/amlevin/www/fake-electron/fake_electron_template.png")

ffitter.Fit()

total_met_for_fake_electron_fraction_hist.Draw("hist")

c1.SaveAs("/eos/user/a/amlevin/www/fake-electron/total.png")

total_met_for_fake_electron_fraction_hist.Draw("Ep")

ffitter.GetPlot().Draw("same")

c1.SaveAs("/eos/user/a/amlevin/www/fake-electron/fit.png")

c1.ForceUpdate()
c1.Modified()

value = ROOT.Double(-1)
error = ROOT.Double(-1)

ffitter.GetResult(0,value,error)

print str(value) + "+/-" + str(error)

print total_met_for_fake_electron_fraction_hist.GetXaxis().FindFixBin( met_cut )

print value*fake_electron_template_hist.Integral()/total_sieie_for_fake_electron_fraction_hist.Integral()

print total_electron_for_fake_electron_fraction_tree.GetEntries("(electron_selection == 0 || electron_selection == 1)")

print value*fake_electron_template_hist.Integral(1,fake_electron_template_hist.GetXaxis().FindFixBin( met_cut ))*total_met_for_fake_electron_fraction_hist.Integral()/total_met_for_fake_electron_fraction_hist.Integral(1,total_met_for_fake_electron_fraction_hist.GetXaxis().FindFixBin( met_cut ))/fake_electron_template_hist.Integral()
