import sys
import random
import ROOT

ROOT.gStyle.SetOptStat(0)

photon_pt_range_cutstrings = ["photon_pt > 25 && photon_pt < 30","photon_pt > 30 && photon_pt < 40","photon_pt > 40 && photon_pt < 50","photon_pt > 50 && photon_pt < 70","photon_pt > 70 && photon_pt < 100","photon_pt > 100 && photon_pt < 135","photon_pt > 135 && photon_pt < 400"]


photon_pt_range_cutstring = photon_pt_range_cutstrings[6]

total_sieie_for_fake_photon_fraction_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/tmp/wgamma_single_electron_total_sieie_for_fake_photon_fraction.root")
total_sieie_for_fake_photon_fraction_tree = total_sieie_for_fake_photon_fraction_file.Get("Events")
total_sieie_for_fake_photon_fraction_hist = ROOT.TH1F("total_sieie_for_fake_photon_fraction_hist","total_sieie_for_fake_photon_fraction_hist",128,0,0.04)
total_sieie_for_fake_photon_fraction_tree.Draw("photon_sieie >> total_sieie_for_fake_photon_fraction_hist","abs(photon_eta) < 1.4442 && lepton_pdg_id == 11 && "+photon_pt_range_cutstring)

fake_photon_template_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/tmp/wgamma_single_electron_fake_photon_template.root")
fake_photon_template_tree = fake_photon_template_file.Get("Events")
fake_photon_template_hist = ROOT.TH1F("fake_photon_template_hist","fake_photon_template_hist",128,0,0.04)
fake_photon_template_tree.Draw("photon_sieie >> fake_photon_template_hist","abs(photon_eta) < 1.4442 && lepton_pdg_id == 11 && "+photon_pt_range_cutstring)

real_photon_template_file = ROOT.TFile.Open("/afs/cern.ch/user/a/amlevin/vbs-wgamma/wgamma_real_photon_template.root")
real_photon_template_tree = real_photon_template_file.Get("Events")
real_photon_template_hist = ROOT.TH1F("real_photon_template_hist","real_photon_template_hist",128,0,0.04)
real_photon_template_tree.Draw("photon_sieie >> real_photon_template_hist","abs(photon_eta) < 1.4442 && lepton_pdg_id == 11 && "+photon_pt_range_cutstring)

x= ROOT.RooRealVar("x","",0,0.04) 
data= ROOT.RooDataHist( "data" , "dataset with x",ROOT.RooArgList(x),total_sieie_for_fake_photon_fraction_hist) 
data_pdf = ROOT.RooHistPdf("data pdf","pdf with x",ROOT.RooArgSet(x),data)
fake_photon_data= ROOT.RooDataHist( "fake photon data" , "dataset with x",ROOT.RooArgList(x),fake_photon_template_hist) 
real_photon_data= ROOT.RooDataHist( "real photon data" , "dataset with x",ROOT.RooArgList(x),real_photon_template_hist) 
fake_photon_pdf = ROOT.RooHistPdf("fake photon pdf","pdf with x",ROOT.RooArgSet(x),fake_photon_data)
real_photon_pdf = ROOT.RooHistPdf("real photon pdf","pdf with x",ROOT.RooArgSet(x),real_photon_data)

ffrac = ROOT.RooRealVar("ffrac","fake photon fraction",0.75,0,1)

model = ROOT.RooAddPdf("model","model",ROOT.RooArgList(fake_photon_pdf,real_photon_pdf),ROOT.RooArgList(ffrac))

model.fitTo(data)

print ffrac.getVal()

mc = ROOT.TObjArray(2)

mc.Add(fake_photon_template_hist)
mc.Add(real_photon_template_hist)

ffitter = ROOT.TFractionFitter(total_sieie_for_fake_photon_fraction_hist,mc)

ffitter.Fit()

total_sieie_for_fake_photon_fraction_hist.Draw("Ep")
ffitter.GetPlot().Draw("same")

value = ROOT.Double(-1)
error = ROOT.Double(-1)

ffitter.GetResult(0,value,error)

print str(value) + "+/-" + str(error)

print total_sieie_for_fake_photon_fraction_hist.GetXaxis().FindFixBin( 0.01022 )

print value*fake_photon_template_hist.Integral()/total_sieie_for_fake_photon_fraction_hist.Integral()

print value*fake_photon_template_hist.Integral(1,fake_photon_template_hist.GetXaxis().FindFixBin( 0.01022 ))*total_sieie_for_fake_photon_fraction_hist.Integral()/total_sieie_for_fake_photon_fraction_hist.Integral(1,total_sieie_for_fake_photon_fraction_hist.GetXaxis().FindFixBin( 0.01022 ))/fake_photon_template_hist.Integral()

#there is a bug which causes a crash inside of the TFractionFitter destructor: https://sft.its.cern.ch/jira/browse/ROOT-9414

raw_input()
