#this script should be used with ROOT version 6.14 or greater in order to get the RDataFrame

import math

import json

import sys
import os

#otherwise, root will parse the command line options, see here http://root.cern.ch/phpBB3/viewtopic.php?f=14&t=18637
sys.argv = []

from ROOT import *

from array import array

gStyle.SetOptStat(0)

year = "2016"

if year == "2016":
    lumi = 35.9
elif year == "2017":
    lumi = 41.5
elif year == "2018":
    lumi = 59.6
else:
    assert(0)

felectronout=TFile("electron_"+year+"_frs.root","recreate")
fmuonout=TFile("muon_"+year+"_frs.root","recreate")

#electron_data_samples = []

if year == "2016" or year == "2017":
    electron_data_samples = [{"filename" : "/eos/user/y/yangli/andrew/data/wg/"+year+"/1June2019/single_electron_fake_lepton.root"}]
elif year == "2018":
    electron_data_samples = [{"filename" : "/eos/user/y/yangli/andrew/data/wg/"+year+"/1June2019/egamma_fake_lepton.root"}]
else:
    assert(0)

#electron_mc_samples = []

electron_mc_samples = [{"filename" : "/eos/user/y/yangli/andrew/data/wg/"+year+"/1June2019/wjets_fake_lepton.root", "xs" : 60430.0, "subtract" : True},{"filename" : "/eos/user/y/yangli/andrew/data/wg/"+year+"/1June2019/zjets_fake_lepton.root", "xs" : 4963.0, "subtract" : True}]

#electron_mc_samples = [{"filename" : "/eos/user/y/yangli/andrew/data/wg/2016/qcd_bctoe_170250.root", "xs" : 2608, "subtract" : False},{"filename" : "/eos/user/y/yangli/andrew/data/wg/2016/qcd_bctoe_2030.root", "xs" : 363100, "subtract" : False},{"filename" : "/eos/user/y/yangli/andrew/data/wg/2016/qcd_bctoe_250.root", "xs" : 722.6, "subtract" : False},{"filename" : "/eos/user/y/yangli/andrew/data/wg/2016/qcd_bctoe_3080.root", "xs" : 417800, "subtract" : False},{"filename" : "/eos/user/y/yangli/andrew/data/wg/2016/qcd_bctoe_80170.root", "xs" : 39860, "subtract" : False}]

muon_data_samples = [{"filename" : "/eos/user/y/yangli/andrew/data/wg/"+year+"/1June2019/single_muon_fake_lepton.root"}]

#muon_data_samples = []

#muon_mc_samples = []

muon_mc_samples = [{"filename" : "/eos/user/y/yangli/andrew/data/wg/"+year+"/1June2019/wjets_fake_lepton.root", "xs" : 60430.0, "subtract" : True},{"filename" : "/eos/user/y/yangli/andrew/data/wg/"+year+"/1June2019/zjets_fake_lepton.root", "xs" : 4963.0, "subtract" : True}]

electron_ptbins=array('d', [30,40,50])
electron_etabins=array('d', [0,0.5,1,1.479,2.0,2.5])

electron_hist_parameters=[len(electron_etabins)-1,electron_etabins,len(electron_ptbins)-1,electron_ptbins]

loose_electron_hist=TH2D("loose_electron_hist","loose_electron_hist",electron_hist_parameters[0],electron_hist_parameters[1],electron_hist_parameters[2],electron_hist_parameters[3])
tight_electron_hist=TH2D("tight_electron_hist","tight_electron_hist",electron_hist_parameters[0],electron_hist_parameters[1],electron_hist_parameters[2],electron_hist_parameters[3])

muon_ptbins=array('d', [25,30,40,50])    
muon_etabins=array('d', [0,0.5,1.0,1.479,2.0,2.5])

muon_highest_pt_bin_center=(muon_ptbins[len(muon_ptbins)-1]+muon_ptbins[len(muon_ptbins)-2])/2
electron_highest_pt_bin_center=(electron_ptbins[len(electron_ptbins)-1]+electron_ptbins[len(electron_ptbins)-2])/2

muon_hist_parameters=[len(muon_etabins)-1,muon_etabins,len(muon_ptbins)-1,muon_ptbins]

loose_muon_hist=TH2D("loose_muon_hist","loose_muon_hist",muon_hist_parameters[0],muon_hist_parameters[1],muon_hist_parameters[2],muon_hist_parameters[3])
tight_muon_hist=TH2D("tight_muon_hist","tight_muon_hist",muon_hist_parameters[0],muon_hist_parameters[1],muon_hist_parameters[2],muon_hist_parameters[3])

loose_muon_hist.Sumw2()
tight_muon_hist.Sumw2()

loose_electron_hist.Sumw2()
tight_electron_hist.Sumw2()

ROOT.EnableImplicitMT()

print "Processing electron data samples"

for sample in electron_data_samples:
    rdf=ROOT.RDataFrame("Events",sample["filename"])
    h_pass=rdf.Filter("met <= 30 && mt <= 20 && is_lepton_tight == '\x01' && abs(lepton_pdgid) == 11").Define("abs_lepton_eta","abs(lepton_eta)").Define("cropped_lepton_pt","lepton_pt < "+str(electron_highest_pt_bin_center)+" ? lepton_pt : "+str(electron_highest_pt_bin_center)).Histo2D(("electron data pass","electron data pass",electron_hist_parameters[0],electron_hist_parameters[1],electron_hist_parameters[2],electron_hist_parameters[3]),"abs_lepton_eta","cropped_lepton_pt")
    h_fail=rdf.Filter("met <= 30 && mt <= 20 && is_lepton_tight != '\x01' && abs(lepton_pdgid) == 11").Define("abs_lepton_eta","abs(lepton_eta)").Define("cropped_lepton_pt","lepton_pt < "+str(electron_highest_pt_bin_center)+" ? lepton_pt : "+str(electron_highest_pt_bin_center)).Histo2D(("electron data fail","electron data fail",electron_hist_parameters[0],electron_hist_parameters[1],electron_hist_parameters[2],electron_hist_parameters[3]),"abs_lepton_eta","cropped_lepton_pt")
    tight_electron_hist.Add(h_pass.GetValue())
    loose_electron_hist.Add(h_fail.GetValue())

print "Processing electron MC samples"

for sample in electron_mc_samples:
    f = TFile.Open(sample["filename"])
    t = f.Get("Events")
    n_weighted_events = f.Get("nEventsGenWeighted").GetBinContent(1)

    if sample["subtract"]:
        plus_sign = "-"
        minus_sign = "+"
    else:
        plus_sign = "+"
        minus_sign = "-"

    rdf=ROOT.RDataFrame("Events",sample["filename"])
    h_pass_plus=rdf.Filter("met <= 30 && mt <= 20 && is_lepton_tight == '\x01' && abs(lepton_pdgid) == 11 && gen_weight > 0").Define("abs_lepton_eta","abs(lepton_eta)").Define("cropped_lepton_pt","lepton_pt < "+str(electron_highest_pt_bin_center)+" ? lepton_pt : "+str(electron_highest_pt_bin_center)).Define("weight",plus_sign+str(sample["xs"]*1000*lumi/n_weighted_events)).Histo2D(("electron mc pass plus","electron mc pass plus",electron_hist_parameters[0],electron_hist_parameters[1],electron_hist_parameters[2],electron_hist_parameters[3]),"abs_lepton_eta","cropped_lepton_pt","weight")
    h_pass_minus=rdf.Filter("met <= 30 && mt <= 20 && is_lepton_tight == '\x01' && abs(lepton_pdgid) == 11 && gen_weight < 0").Define("abs_lepton_eta","abs(lepton_eta)").Define("cropped_lepton_pt","lepton_pt < "+str(electron_highest_pt_bin_center)+" ? lepton_pt : "+str(electron_highest_pt_bin_center)).Define("weight",minus_sign+str(sample["xs"]*1000*lumi/n_weighted_events)).Histo2D(("electron mc pass minus","electron mc pass minus",electron_hist_parameters[0],electron_hist_parameters[1],electron_hist_parameters[2],electron_hist_parameters[3]),"abs_lepton_eta","cropped_lepton_pt","weight")
    h_fail_plus=rdf.Filter("met <= 30 && mt <= 20 && is_lepton_tight != '\x01' && abs(lepton_pdgid) == 11 && gen_weight > 0").Define("abs_lepton_eta","abs(lepton_eta)").Define("cropped_lepton_pt","lepton_pt < "+str(electron_highest_pt_bin_center)+" ? lepton_pt : "+str(electron_highest_pt_bin_center)).Define("weight",plus_sign+str(sample["xs"]*1000*lumi/n_weighted_events)).Histo2D(("electron mc fail plus","electron mc fail plus",electron_hist_parameters[0],electron_hist_parameters[1],electron_hist_parameters[2],electron_hist_parameters[3]),"abs_lepton_eta","cropped_lepton_pt","weight")
    h_fail_minus=rdf.Filter("met <= 30 && mt <= 20 && is_lepton_tight != '\x01' && abs(lepton_pdgid) == 11 && gen_weight < 0").Define("abs_lepton_eta","abs(lepton_eta)").Define("cropped_lepton_pt","lepton_pt < "+str(electron_highest_pt_bin_center)+" ? lepton_pt : "+str(electron_highest_pt_bin_center)).Define("weight",minus_sign+str(sample["xs"]*1000*lumi/n_weighted_events)).Histo2D(("electron mc fail minus","electron mc fail minus",electron_hist_parameters[0],electron_hist_parameters[1],electron_hist_parameters[2],electron_hist_parameters[3]),"abs_lepton_eta","cropped_lepton_pt","weight")

    tight_electron_hist.Add(h_pass_plus.GetValue())
    tight_electron_hist.Add(h_pass_minus.GetValue())
    loose_electron_hist.Add(h_fail_plus.GetValue())
    loose_electron_hist.Add(h_fail_minus.GetValue())

    f.Close()

print "Processing muon data samples"

for sample in muon_data_samples:
    rdf=ROOT.RDataFrame("Events",sample["filename"])
    h_pass=rdf.Filter("met <= 30 && mt <= 20 && is_lepton_tight == '\x01' && abs(lepton_pdgid) == 13").Define("abs_lepton_eta","abs(lepton_eta)").Define("cropped_lepton_pt","lepton_pt < "+str(muon_highest_pt_bin_center)+" ? lepton_pt : "+str(muon_highest_pt_bin_center)).Histo2D(("muon data pass","muon data pass",muon_hist_parameters[0],muon_hist_parameters[1],muon_hist_parameters[2],muon_hist_parameters[3]),"abs_lepton_eta","cropped_lepton_pt")
    h_fail=rdf.Filter("met <= 30 && mt <= 20 && is_lepton_tight != '\x01' && abs(lepton_pdgid) == 13").Define("abs_lepton_eta","abs(lepton_eta)").Define("cropped_lepton_pt","lepton_pt < "+str(muon_highest_pt_bin_center)+" ? lepton_pt : "+str(muon_highest_pt_bin_center)).Histo2D(("muon data fail","muon data fail",muon_hist_parameters[0],muon_hist_parameters[1],muon_hist_parameters[2],muon_hist_parameters[3]),"abs_lepton_eta","cropped_lepton_pt")
    tight_muon_hist.Add(h_pass.GetValue())
    loose_muon_hist.Add(h_fail.GetValue())

print "Processing muon MC samples"

for sample in muon_mc_samples:
    f = TFile.Open(sample["filename"])
    t = f.Get("Events")
    n_weighted_events = f.Get("nEventsGenWeighted").GetBinContent(1)

    if sample["subtract"]:
        plus_sign = "-"
        minus_sign = "+"
    else:
        plus_sign = "+"
        minus_sign = "-"

    rdf=ROOT.RDataFrame("Events",sample["filename"])
    h_pass_plus=rdf.Filter("met <= 30 && mt <= 20 && is_lepton_tight == '\x01' && abs(lepton_pdgid) == 13 && gen_weight > 0").Define("abs_lepton_eta","abs(lepton_eta)").Define("cropped_lepton_pt","lepton_pt < "+str(muon_highest_pt_bin_center)+" ? lepton_pt : "+str(muon_highest_pt_bin_center)).Define("weight",plus_sign+str(sample["xs"]*1000*lumi/n_weighted_events)).Histo2D(("muon mc pass plus","muon mc pass plus",muon_hist_parameters[0],muon_hist_parameters[1],muon_hist_parameters[2],muon_hist_parameters[3]),"abs_lepton_eta","cropped_lepton_pt","weight")
    h_pass_minus=rdf.Filter("met <= 30 && mt <= 20 && is_lepton_tight == '\x01' && abs(lepton_pdgid) == 13 && gen_weight < 0").Define("abs_lepton_eta","abs(lepton_eta)").Define("cropped_lepton_pt","lepton_pt < "+str(muon_highest_pt_bin_center)+" ? lepton_pt : "+str(muon_highest_pt_bin_center)).Define("weight",minus_sign+str(sample["xs"]*1000*lumi/n_weighted_events)).Histo2D(("muon mc pass minus","muon mc pass minus",muon_hist_parameters[0],muon_hist_parameters[1],muon_hist_parameters[2],muon_hist_parameters[3]),"abs_lepton_eta","cropped_lepton_pt","weight")
    h_fail_plus=rdf.Filter("met <= 30 && mt <= 20 && is_lepton_tight != '\x01' && abs(lepton_pdgid) == 13 && gen_weight > 0").Define("abs_lepton_eta","abs(lepton_eta)").Define("cropped_lepton_pt","lepton_pt < "+str(muon_highest_pt_bin_center)+" ? lepton_pt : "+str(muon_highest_pt_bin_center)).Define("weight",plus_sign+str(sample["xs"]*1000*lumi/n_weighted_events)).Histo2D(("muon mc fail plus","muon mc fail plus",muon_hist_parameters[0],muon_hist_parameters[1],muon_hist_parameters[2],muon_hist_parameters[3]),"abs_lepton_eta","cropped_lepton_pt","weight")
    h_fail_minus=rdf.Filter("met <= 30 && mt <= 20 && is_lepton_tight != '\x01' && abs(lepton_pdgid) == 13 && gen_weight < 0").Define("abs_lepton_eta","abs(lepton_eta)").Define("cropped_lepton_pt","lepton_pt < "+str(muon_highest_pt_bin_center)+" ? lepton_pt : "+str(muon_highest_pt_bin_center)).Define("weight",minus_sign+str(sample["xs"]*1000*lumi/n_weighted_events)).Histo2D(("muon mc fail minus","muon mc fail minus",muon_hist_parameters[0],muon_hist_parameters[1],muon_hist_parameters[2],muon_hist_parameters[3]),"abs_lepton_eta","cropped_lepton_pt","weight")

    tight_muon_hist.Add(h_pass_plus.GetValue())
    tight_muon_hist.Add(h_pass_minus.GetValue())
    loose_muon_hist.Add(h_fail_plus.GetValue())
    loose_muon_hist.Add(h_fail_minus.GetValue())

    f.Close()


felectronout.cd()

tight_electron_hist.Clone().Write()
loose_electron_hist.Clone().Write()

loose_electron_hist.Add(tight_electron_hist)
    
tight_electron_hist.Divide(loose_electron_hist)
tight_electron_hist.Clone("electron_frs").Write()

fmuonout.cd()

tight_muon_hist.Clone().Write()
loose_muon_hist.Clone().Write()

loose_muon_hist.Add(tight_muon_hist)
    
tight_muon_hist.Divide(loose_muon_hist)
tight_muon_hist.Clone("muon_frs").Write()
