import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--year',dest='year',default='2016')
parser.add_argument('-o',dest='outdir',default="/eos/user/a/amlevin/www/wg/fake-photon-fits/")

args = parser.parse_args()

#there is a bug which causes a crash inside of the TFractionFitter destructor: https://sft.its.cern.ch/jira/browse/ROOT-9414
#I think this makes it necessary to create the tfractionfitters only once for each set of input files that are used, and then reuse the tfractionfitters

import sys
import random
import numpy as np
import json

from pprint import pprint

ROOT.gStyle.SetOptStat(0)

#lepton_names =["muon","electron"]
#lepton_names =["electron","muon"]
#lepton_names =["muon"]
#lepton_names =["electron"]
lepton_names =["both"]

fake_fractions = {}

fake_event_weights = {}

fake_fractions["both_barrel"] = []

fake_fractions["both_endcap"] = []

fake_fractions["muon_barrel"] = []

fake_fractions["muon_endcap"] = []

fake_fractions["electron_barrel"] = []

fake_fractions["electron_endcap"] = []

fake_event_weights["both_barrel"] = []

fake_event_weights["both_endcap"] = []

fake_event_weights["muon_barrel"] = []

fake_event_weights["muon_endcap"] = []

fake_event_weights["electron_barrel"] = []

fake_event_weights["electron_endcap"] = []

photon1_eta_ranges = ["photon1_isScEtaEB","photon1_isScEtaEE"]
photon2_eta_ranges = ["photon2_isScEtaEB","photon2_isScEtaEE"]

#photon1_pt_range_cutstrings = ["photon1_pt > 20 && photon1_pt < 25","photon1_pt > 25 && photon1_pt < 30","photon1_pt > 30 && photon1_pt < 40","photon1_pt > 40 && photon1_pt < 50","photon1_pt > 50 && photon1_pt < 70","photon1_pt > 70 && photon1_pt < 100","photon1_pt > 100 && photon1_pt < 135","photon1_pt > 135 && photon1_pt < 400"]

#photon2_pt_range_cutstrings = ["photon2_pt > 20 && photon2_pt < 25","photon2_pt > 25 && photon2_pt < 30","photon2_pt > 30 && photon2_pt < 40","photon2_pt > 40 && photon2_pt < 50","photon2_pt > 50 && photon2_pt < 70","photon2_pt > 70 && photon2_pt < 100","photon2_pt > 100 && photon2_pt < 135","photon2_pt > 135 && photon2_pt < 400"]

photon1_pt_range_cutstrings = ["photon1_pt > 20 && photon1_pt < 25","photon1_pt > 25 && photon1_pt < 30","photon1_pt > 30 && photon1_pt < 40","photon1_pt > 40 && photon1_pt < 50","photon1_pt > 50 && photon1_pt < 400"]

photon2_pt_range_cutstrings = ["photon2_pt > 20 && photon2_pt < 25","photon2_pt > 25 && photon2_pt < 30","photon2_pt > 30 && photon2_pt < 40","photon2_pt > 40 && photon2_pt < 50","photon2_pt > 50 && photon2_pt < 400"]

assert(len(photon1_pt_range_cutstrings) == len(photon2_pt_range_cutstrings))
assert(len(photon2_eta_ranges) == len(photon2_eta_ranges))

photon1_recoil_string = "(cos(photon1_phi)*(- lepton_pt*cos(lepton_phi) - puppimet*cos(puppimetphi)) + sin(photon1_phi)*(-lepton_pt*sin(lepton_phi) - puppimet*sin(puppimetphi)))"

photon2_recoil_string = "(cos(photon2_phi)*(- lepton_pt*cos(lepton_phi) - puppimet*cos(puppimetphi)) + sin(photon2_phi)*(-lepton_pt*sin(lepton_phi) - puppimet*sin(puppimetphi)))"

#photon1_recoil_string = "(cos(photon1_phi)*(- lepton_pt*cos(lepton_phi) - gen_neutrinos_pt*cos(gen_neutrinos_phi)) + sin(photon1_phi)*(-lepton_pt*sin(lepton_phi) - gen_neutrinos_pt*sin(gen_neutrinos_phi)))"

#photon2_recoil_string = "(cos(photon2_phi)*(- lepton_pt*cos(lepton_phi) - gen_neutrinos_pt*cos(gen_neutrinos_phi)) + sin(photon2_phi)*(-lepton_pt*sin(lepton_phi) - gen_neutrinos_pt*sin(gen_neutrinos_phi)))"

photon1_dphilg_string = "(abs(photon1_phi - lepton_phi) > pi ? abs(abs(photon1_phi - lepton_phi) - 2*pi) : abs(photon1_phi - lepton_phi))"
photon2_dphilg_string = "(abs(photon2_phi - lepton_phi) > pi ? abs(abs(photon2_phi - lepton_phi) - 2*pi) : abs(photon2_phi - lepton_phi))"

photon1_recoil_cutstring = photon1_recoil_string + " > -1000 && " + photon1_recoil_string + " < 1000"
photon2_recoil_cutstring = photon2_recoil_string + " > -1000 && " + photon2_recoil_string + " < 1000"

#photon1_recoil_cutstring = photon1_dphilg_string+" < pi/2"
#photon2_recoil_cutstring = photon2_dphilg_string+" < pi/2"

photon1_veto_signal_selection_cutstring = "!((puppimet > 40 && lepton_pt > 30 && photon1_pt > 25 && abs(lepton_pdg_id) == 11) || (puppimet > 40 && lepton_pt > 25 && photon1_pt > 25 && abs(lepton_pdg_id) == 13))" 

photon2_veto_signal_selection_cutstring = "!((puppimet > 40 && lepton_pt > 30 && photon2_pt > 25 && abs(lepton_pdg_id) == 11) || (puppimet > 40 && lepton_pt > 25 && photon2_pt > 25 && abs(lepton_pdg_id) == 13))" 

#photon1_veto_signal_selection_cutstring = "(puppimet > 60 && puppimt < 30)"
#photon2_veto_signal_selection_cutstring = "(puppimet > 60 && puppimt < 30)"

#photon1_veto_signal_selection_cutstring = "1"
#photon2_veto_signal_selection_cutstring = "1"

den_pho_sel = str(4) #fail sieie
#den_pho_sel = str(3) #fail charged isolation

#max_sieie = 0.0125
sieie_2016_barrel = 0.01022
sieie_2016_endcap = 0.03001
sieie_2017_barrel = 0.01015
sieie_2017_endcap = 0.0272
sieie_2018_barrel = 0.01015
sieie_2018_endcap = 0.0272

chiso_2016_barrel = 1.416
chiso_2016_endcap = 1.012 
chiso_2017_barrel = 1.141
chiso_2017_endcap = 1.051
chiso_2018_barrel = 1.141
chiso_2018_endcap = 1.051

if args.year == "2016":
    sieie_barrel = sieie_2016_barrel
    sieie_endcap = sieie_2016_endcap
    chiso_barrel = chiso_2016_barrel
    chiso_endcap = chiso_2016_endcap
elif args.year == "2017":
    sieie_barrel = sieie_2017_barrel
    sieie_endcap = sieie_2017_endcap
    chiso_barrel = chiso_2017_barrel
    chiso_endcap = chiso_2017_endcap
elif args.year == "2018":
    sieie_barrel = sieie_2018_barrel
    sieie_endcap = sieie_2018_endcap
    chiso_barrel = chiso_2018_barrel
    chiso_endcap = chiso_2018_endcap
else:
    assert(0)

max_sieie_barrel = sieie_barrel*1.75
max_sieie_endcap = sieie_endcap*1.75
#max_sieie_barrel = sieie_barrel*1000
#max_sieie_endcap = sieie_endcap*1000
    
#max_sieie = 0.0375
#max_sieie = 0.0375
#max_sieie = 1000000
#max_chiso_barrel = chiso_barrel*1.75
#max_chiso_endcap = chiso_endcap*1.75
max_chiso_barrel = chiso_barrel*1000
max_chiso_endcap = chiso_endcap*1000
#max_chiso = 10
 
njets_min = 0
njets_max = 1000

fit  = True

index = 0

mc_fake_photon_samples = []

#mc_fake_photon_samples = [{"file" : ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/"+args.year+"/1June2019/wjets_fake_photon.root"),"xs" : 60430.0, "subtract" : False, "prompt" : False},{"file" : ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/"+args.year+"/1June2019/wgjets_fake_photon.root"),"xs" : 178.6, "subtract" : False, "prompt" : True}]

#mc_fake_photon_samples = [{"file" : ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/"+args.year+"/1June2019/wjets_fake_photon.root"),"xs" : 60430.0, "subtract" : False, "prompt" : False}]

muon_data_fake_photon_samples = [{"file" : ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/"+args.year+"/1June2019/single_muon_fake_photon.root")}]

if args.year == "2016" or args.year == "2017":
    electron_data_fake_photon_samples = [{"file" : ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/"+args.year+"/1June2019/single_electron_fake_photon.root")}]
elif args.year == "2018":
    electron_data_fake_photon_samples = [{"file" : ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/"+args.year+"/1June2019/egamma_fake_photon.root")}]
else:
    assert(0)

data_fake_photon_samples = [{"file" : ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/"+args.year+"/1June2019/data_fake_photon.root")}]

#data_fake_photon_samples = []

#muon_data_fake_photon_samples = []
#electron_data_fake_photon_samples = []

real_photon_template_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/"+args.year+"/1June2019/real_photon_template.root")

created_muon_fitter = False
created_electron_fitter = False

lumi=35.9

for lepton_name in lepton_names:

    if lepton_name == "muon":
        lepton_pdg_id = "(lepton_pdg_id == 13)"
    elif lepton_name == "electron":
        lepton_pdg_id = "(lepton_pdg_id == 11)"
    elif lepton_name == "both":    
        lepton_pdg_id = "1"
    else:
        assert(0)

    if lepton_name == "muon":
        fake_photon_data_samples = muon_data_fake_photon_samples
        fake_photon_mc_samples = mc_fake_photon_samples
    elif lepton_name == "electron":
        fake_photon_data_samples = electron_data_fake_photon_samples
        fake_photon_mc_samples = mc_fake_photon_samples
    elif lepton_name == "both":
        fake_photon_data_samples = data_fake_photon_samples
        fake_photon_mc_samples = mc_fake_photon_samples

    for i in range(len(photon1_eta_ranges)):
        for j in range(len(photon1_pt_range_cutstrings)):

            photon1_eta_range = photon1_eta_ranges[i]
            photon2_eta_range = photon2_eta_ranges[i]
            photon1_pt_range_cutstring = photon1_pt_range_cutstrings[j]
            photon2_pt_range_cutstring = photon2_pt_range_cutstrings[j]

            print "Processing " + lepton_name + ", " + photon1_eta_range + ", " + photon1_pt_range_cutstring

            if photon1_eta_range == "photon1_isScEtaEB":
                sieie_cut = sieie_barrel
                n_bins = 128
                sieie_lower = 0.00
                sieie_upper = 0.04
                max_sieie = max_sieie_barrel
                max_chiso = max_chiso_barrel
            else:
                sieie_cut = sieie_endcap
                #n_bins = 160                                                                                                                                                             
                #n_bins = 80                                                                                                                                                              
                n_bins = 20
                sieie_lower = 0.01
                sieie_upper = 0.06
                max_sieie = max_sieie_endcap
                max_chiso = max_chiso_endcap


            if fit:    
                total_hist = ROOT.TH1F("total","",n_bins,sieie_lower,sieie_upper)
                total_hist.Sumw2()

                fake_photon_template_hist = ROOT.TH1F("fake_photon_template_hist","fake_photon_template_hist",n_bins,sieie_lower,sieie_upper)
                fake_photon_template_hist.Sumw2()

            numerator = float(0)
            denominator = float(0)

            for k,fake_photon_data_sample in enumerate(fake_photon_data_samples):   
                fake_photon_tree = fake_photon_data_sample["file"].Get("Events")

                denominator+=fake_photon_tree.GetEntries(photon1_eta_range+ " && "+lepton_pdg_id + " && (photon1_selection == "+den_pho_sel+") && "+ photon1_pt_range_cutstring + " && pass_selection1" + " && " + photon1_recoil_cutstring + " && njets_fake >= "+ str(njets_min) + " && njets_fake <= "+str(njets_max) + " && photon1_sieie < "+str(max_sieie) + " && photon1_pfRelIso03_chg*photon1_pt < "+str(max_chiso)+ " && " + str(photon1_veto_signal_selection_cutstring))

                if fit:
                    total_hist_data = ROOT.TH1F("total_hist_data_sample"+str(k),"total_hist_data_sample"+str(k),n_bins,sieie_lower,sieie_upper)
                    total_hist_data.Sumw2()

                    fake_photon_template_hist_data = ROOT.TH1F("fake_photon_template_hist_data_sample"+str(k),"fake_photon_template_hist_data_sample"+str(k),n_bins,sieie_lower,sieie_upper)
                    fake_photon_template_hist_data.Sumw2()

                    fake_photon_tree.Draw("photon1_sieie >> total_hist_data_sample"+str(k),photon1_eta_range+ " && "+lepton_pdg_id+" && (photon1_selection == 0 || photon1_selection == 4) && "+photon1_pt_range_cutstring + " && pass_selection1 && "+str(photon1_veto_signal_selection_cutstring) + " && " + photon1_recoil_cutstring + "&& njets_fake >= "+str(njets_min) + " && njets_fake_template <= "+str(njets_max))

                    fake_photon_tree.Draw("photon2_sieie >> fake_photon_template_hist_data_sample"+str(k),photon2_eta_range + " && "+lepton_pdg_id+" && "+photon2_pt_range_cutstring + " && pass_selection2 && "+str(photon2_veto_signal_selection_cutstring)  + " && " + photon2_recoil_cutstring +" && njets_fake_template  >= "+str(njets_min) + " && njets_fake_template <= " + str(njets_max))

                    total_hist.Add(total_hist_data)
                    fake_photon_template_hist.Add(fake_photon_template_hist_data)

                else:    

                    numerator+=fake_photon_tree.GetEntries(photon1_eta_range+ " && "+lepton_pdg_id+ " && (photon1_selection == 0) && "+ photon1_pt_range_cutstring + " && pass_selection1" + " && " + photon1_recoil_cutstring + " && njets_fake >= "+ str(njets_min) + " && njets_fake <= "+str(njets_max)+ " && " + str(photon1_veto_signal_selection_cutstring))
                

            for k,fake_photon_mc_sample in enumerate(fake_photon_mc_samples):   

                fake_photon_tree = fake_photon_mc_sample["file"].Get("Events")

                if fake_photon_mc_sample["prompt"]:
                    photon1_gen_matching_cutstring = "(photon1_gen_matching == 6 || photon1_gen_matching == 5 || photon1_gen_matching == 4 || photon1_gen_matching == 1)"
                    photon2_gen_matching_cutstring = "(photon2_gen_matching == 6 || photon2_gen_matching == 5 || photon2_gen_matching == 4 || photon2_gen_matching == 1)"
#                    photon1_gen_matching_cutstring = "photon1_gen_matching_old > 0"
#                    photon2_gen_matching_cutstring = "photon2_gen_matching_old > 0"
                else:
                    photon1_gen_matching_cutstring = "!(photon1_gen_matching == 6 || photon1_gen_matching == 5 || photon1_gen_matching == 4 || photon1_gen_matching == 1)"
                    photon2_gen_matching_cutstring = "!(photon2_gen_matching == 6 || photon2_gen_matching == 5 || photon2_gen_matching == 4 || photon2_gen_matching == 1)"    
#                    photon1_gen_matching_cutstring = "((photon1_genjet_matching == 1) && !(photon1_gen_matching == 6 || photon1_gen_matching == 5 || photon1_gen_matching == 4 || photon1_gen_matching == 1))"
#                    photon2_gen_matching_cutstring = "((photon2_genjet_matching == 1) && !(photon2_gen_matching == 6 || photon2_gen_matching == 5 || photon2_gen_matching == 4 || photon2_gen_matching == 1))"
#                    photon1_gen_matching_cutstring = "((photon1_genjet_matching == 0) && (photon1_gen_matching == 0))"
#                    photon2_gen_matching_cutstring = "((photon2_genjet_matching == 0) && (photon2_gen_matching == 0))"
#                    photon1_gen_matching_cutstring = "photon1_gen_matching_old == 0"
#                    photon2_gen_matching_cutstring = "photon2_gen_matching_old == 0"

                denominator+=fake_photon_tree.GetEntries(photon1_eta_range+ " && "+lepton_pdg_id + " && (photon1_selection == "+den_pho_sel+") && "+ photon1_pt_range_cutstring + " && pass_selection1" + " && " + photon1_recoil_cutstring + " && njets_fake >= "+ str(njets_min) + " && njets_fake <= "+str(njets_max) + " && photon1_sieie < "+str(max_sieie) + " && photon1_pfRelIso03_chg*photon1_pt < "+str(max_chiso) + " && gen_weight > 0 && " + photon1_gen_matching_cutstring+ " && " + str(photon1_veto_signal_selection_cutstring))*fake_photon_mc_sample["xs"]*1000*lumi/fake_photon_mc_sample["file"].Get("nEventsGenWeighted").GetBinContent(1)
                denominator-=fake_photon_tree.GetEntries(photon1_eta_range+ " && "+lepton_pdg_id + " && (photon1_selection == "+den_pho_sel+") && "+ photon1_pt_range_cutstring + " && pass_selection1" + " && " + photon1_recoil_cutstring + " && njets_fake >= "+ str(njets_min) + " && njets_fake <= "+str(njets_max) + " && photon1_sieie < "+str(max_sieie) + " && photon1_pfRelIso03_chg*photon1_pt < "+str(max_chiso) + " && gen_weight < 0 && "  + photon1_gen_matching_cutstring + " && " + str(photon1_veto_signal_selection_cutstring))*fake_photon_mc_sample["xs"]*1000*lumi/fake_photon_mc_sample["file"].Get("nEventsGenWeighted").GetBinContent(1)

                if fit:    
                    total_hist_pos = ROOT.TH1F("total_hist_pos_sample"+str(k),"total_hist_pos_sample"+str(k),n_bins,sieie_lower,sieie_upper)
                    total_hist_neg = ROOT.TH1F("total_hist_neg_sample"+str(k),"total_hist_neg_sample"+str(k),n_bins,sieie_lower,sieie_upper)
                    total_hist_pos.Sumw2()
                    total_hist_neg.Sumw2()

                    fake_photon_tree.Draw("photon1_sieie >> total_hist_pos_sample"+str(k),photon1_eta_range+ " && "+lepton_pdg_id+" && (photon1_selection == 0 || photon1_selection == 4) && "+photon1_pt_range_cutstring + " && pass_selection1 && "+str(photon1_veto_signal_selection_cutstring) + " && " + photon1_recoil_cutstring + "&& njets_fake >= "+str(njets_min) + " && njets_fake_template <= "+str(njets_max) + " && gen_weight > 0 && " + photon1_gen_matching_cutstring)
                    fake_photon_tree.Draw("photon1_sieie >> total_hist_neg_sample"+str(k),photon1_eta_range+ " && "+lepton_pdg_id+" && (photon1_selection == 0 || photon1_selection == 4) && "+photon1_pt_range_cutstring + " && pass_selection1 && "+str(photon1_veto_signal_selection_cutstring) + " && " + photon1_recoil_cutstring + "&& njets_fake >= "+str(njets_min) + " && njets_fake_template <= "+str(njets_max) + " && gen_weight < 0 && "+photon1_gen_matching_cutstring)

                    total_hist_pos.Scale(fake_photon_mc_sample["xs"]*1000*lumi/fake_photon_mc_sample["file"].Get("nEventsGenWeighted").GetBinContent(1))
                    total_hist_neg.Scale(-fake_photon_mc_sample["xs"]*1000*lumi/fake_photon_mc_sample["file"].Get("nEventsGenWeighted").GetBinContent(1))

                    total_hist.Add(total_hist_pos)
                    total_hist.Add(total_hist_neg)

                    fake_photon_template_hist_pos = ROOT.TH1F("fake_photon_template_hist_pos_sample"+str(k),"fake_photon_template_hist_pos_sample"+str(k),n_bins,sieie_lower,sieie_upper)
                    fake_photon_template_hist_neg = ROOT.TH1F("fake_photon_template_hist_neg_sample"+str(k),"fake_photon_template_hist_neg_sample"+str(k),n_bins,sieie_lower,sieie_upper)
                    fake_photon_template_hist_pos.Sumw2()
                    fake_photon_template_hist_neg.Sumw2()

                    fake_photon_tree.Draw("photon2_sieie >> fake_photon_template_hist_pos_sample"+str(k),photon2_eta_range + " && "+lepton_pdg_id+" && "+photon2_pt_range_cutstring + " && pass_selection2 && "+str(photon2_veto_signal_selection_cutstring)  + " && " + photon2_recoil_cutstring +" && njets_fake_template  >= "+str(njets_min) + " && njets_fake_template <= " + str(njets_max)  + " && gen_weight > 0 && "+photon2_gen_matching_cutstring)
                    fake_photon_tree.Draw("photon2_sieie >> fake_photon_template_hist_neg_sample"+str(k),photon2_eta_range + " && "+lepton_pdg_id+" && "+photon2_pt_range_cutstring + " && pass_selection2 && "+str(photon2_veto_signal_selection_cutstring)  + " && " + photon2_recoil_cutstring +" && njets_fake_template  >= "+str(njets_min) + " && njets_fake_template <= " + str(njets_max) + " && gen_weight < 0 &&" + photon2_gen_matching_cutstring)

                    fake_photon_template_hist_pos.Scale(fake_photon_mc_sample["xs"]*1000*lumi/fake_photon_mc_sample["file"].Get("nEventsGenWeighted").GetBinContent(1))
                    fake_photon_template_hist_neg.Scale(-fake_photon_mc_sample["xs"]*1000*lumi/fake_photon_mc_sample["file"].Get("nEventsGenWeighted").GetBinContent(1))

                    fake_photon_template_hist.Add(fake_photon_template_hist_pos)
                    fake_photon_template_hist.Add(fake_photon_template_hist_neg)

                else:
                    if not fake_photon_mc_sample["prompt"]:
                        numerator+=fake_photon_tree.GetEntries(photon1_eta_range+ " && "+lepton_pdg_id + " && (photon1_selection == 0) && "+ photon1_pt_range_cutstring + " && pass_selection1" + " && " + photon1_recoil_cutstring + " && njets_fake >= "+ str(njets_min) + " && njets_fake <= "+str(njets_max) + " && gen_weight > 0 &&" + photon1_gen_matching_cutstring+ " && " + str(photon1_veto_signal_selection_cutstring))*fake_photon_mc_sample["xs"]*1000*lumi/fake_photon_mc_sample["file"].Get("nEventsGenWeighted").GetBinContent(1)
                        numerator-=fake_photon_tree.GetEntries(photon1_eta_range+ " && "+lepton_pdg_id + " && (photon1_selection == 0) && "+ photon1_pt_range_cutstring + " && pass_selection1" + " && " + photon1_recoil_cutstring + " && njets_fake >= "+ str(njets_min) + " && njets_fake <= "+str(njets_max) + " && gen_weight < 0 &&" + photon1_gen_matching_cutstring+ " && " + str(photon1_veto_signal_selection_cutstring))*fake_photon_mc_sample["xs"]*1000*lumi/fake_photon_mc_sample["file"].Get("nEventsGenWeighted").GetBinContent(1)
                
#                fake_photon_tree.Scan("run:lumi:event:photon1_pt:photon1_eta:photon1_phi:lepton_pt:lepton_eta:lepton_phi:lepton_pdg_id",photon1_eta_range+ "  && lepton_pdg_id == "+lepton_pdg_id + " && (photon1_selection == 3) && "+ photon1_pt_range_cutstring + " && pass_selection1" + " && " + photon1_recoil_cutstring + " && njets_fake >= "+ str(njets_min) + " && njets_fake <= "+str(njets_max) + " && photon1_sieie < "+str(max_sieie) + " && photon1_pfRelIso03_chg*photon1_pt < "+str(max_chiso) + " && "+photon1_gen_matching_cutstring)*fake_photon_mc_sample["xs"]*1000*lumi/fake_photon_mc_sample["file"].Get("nEventsGenWeighted").GetBinContent(1)
#                fake_photon_tree.Scan("run:lumi:event:photon1_pt:photon1_eta:photon1_phi:lepton_pt:lepton_eta:lepton_phi:lepton_pdg_id",photon1_eta_range+ " && lumi == 1054017 && lepton_pdg_id == "+lepton_pdg_id + " && (photon1_selection == 4) && "+ photon1_pt_range_cutstring + " && pass_selection1" + " && " + photon1_recoil_cutstring + " && njets_fake >= "+ str(njets_min) + " && njets_fake <= "+str(njets_max) + " && photon1_sieie < "+str(max_sieie) + " && photon1_pfRelIso03_chg*photon1_pt < "+str(max_chiso) + " && "+photon1_gen_matching_cutstring)*fake_photon_mc_sample["xs"]*1000*lumi/fake_photon_mc_sample["file"].Get("nEventsGenWeighted").GetBinContent(1)


#            fake_photon_tree.Draw("photon2_sieie >> fake_photon_template_hist",photon2_eta_range + " && lepton_pdg_id == "+lepton_pdg_id+" && "+photon2_pt_range_cutstring + " && pass_selection2 && "+str(veto_signal_selection_cutstring))


            if fit:        

                real_photon_template_tree = real_photon_template_file.Get("Events")
                real_photon_template_hist = ROOT.TH1F("real_photon_template_hist","real_photon_template_hist",n_bins,sieie_lower,sieie_upper)
                real_photon_template_hist.Sumw2()
                for k in range(real_photon_template_tree.GetEntries()):
                    real_photon_template_tree.GetEntry(k)

                    pass_eta_range = False

                    if photon1_eta_range == "photon1_isScEtaEB":
                        if real_photon_template_tree.photon_isScEtaEB == '\x01':
                            pass_eta_range = True
                    elif photon1_eta_range == "photon1_isScEtaEE":
                        if real_photon_template_tree.photon_isScEtaEE == '\x01':
                            pass_eta_range = True
                    else:
                        assert(0)

                    pass_lepton_pdg_id = False

                    if lepton_name == "muon":
                        if real_photon_template_tree.lepton_pdg_id == 13:
                            pass_lepton_pdg_id = True
                    elif lepton_name == "electron":
                        if real_photon_template_tree.lepton_pdg_id == 11:
                            pass_lepton_pdg_id = True
                    elif lepton_name == "both":    
                        pass_lepton_pdg_id = True
                    else:
                        assert(0)

                    pass_photon_pt_range = False

                    if photon1_pt_range_cutstring == "photon1_pt > 20 && photon1_pt < 25":
                        if real_photon_template_tree.photon_pt > 20 and real_photon_template_tree.photon_pt < 25:
                            pass_photon_pt_range = True
                    elif photon1_pt_range_cutstring == "photon1_pt > 25 && photon1_pt < 30":
                        if real_photon_template_tree.photon_pt > 25 and real_photon_template_tree.photon_pt < 30:
                            pass_photon_pt_range = True
                    elif photon1_pt_range_cutstring == "photon1_pt > 30 && photon1_pt < 40":
                        if real_photon_template_tree.photon_pt > 30 and real_photon_template_tree.photon_pt < 40:
                            pass_photon_pt_range = True
                    elif photon1_pt_range_cutstring == "photon1_pt > 40 && photon1_pt < 50":
                        if real_photon_template_tree.photon_pt > 40 and real_photon_template_tree.photon_pt < 50:
                            pass_photon_pt_range = True
                    elif photon1_pt_range_cutstring == "photon1_pt > 50 && photon1_pt < 400":
                        if real_photon_template_tree.photon_pt > 100 and real_photon_template_tree.photon_pt < 400:
                            pass_photon_pt_range = True
                    else:
                        assert(0)


#                    pass_signal_selection_veto = not ((real_photon_template_tree.puppimet > 60 and real_photon_template_tree.puppimt > 30 and real_photon_template_tree.lepton_pt > 30 and real_photon_template_tree.photon_pt > 25 and real_photon_template_tree.lepton_pdg_id == 11) or (real_photon_template_tree.puppimet > 60 and real_photon_template_tree.puppimt > 30 and real_photon_template_tree.lepton_pt > 25 and real_photon_template_tree.photon_pt > 25 and real_photon_template_tree.lepton_pdg_id == 13))

                    pass_signal_selection_veto = True
#                pass_signal_selection_veto = real_photon_template_tree.puppimet > 60 and real_photon_template_tree.puppimt < 30

                    if pass_photon_pt_range and pass_lepton_pdg_id and pass_eta_range and pass_signal_selection_veto:

                        if real_photon_template_tree.gen_weight > 0:
                            real_photon_template_hist.Fill(real_photon_template_tree.photon_sieie)
                        else:
                            real_photon_template_hist.Fill(real_photon_template_tree.photon_sieie,-1)

                for k in range(real_photon_template_hist.GetNbinsX()+2):
                    if real_photon_template_hist.GetBinContent(k) < 0:
                        real_photon_template_hist.SetBinContent(k,0)

                mc = ROOT.TObjArray(2)

                mc.Add(fake_photon_template_hist)
                mc.Add(real_photon_template_hist)

                ffitter = ROOT.TFractionFitter(total_hist,mc)


                c1 = ROOT.TCanvas("c1", "c1",5,50,500,500);

                real_photon_template_hist.GetXaxis().SetTitle("\sigma_{i \eta i \eta}")
                real_photon_template_hist.SetLineWidth(2)
#            real_photon_template_hist.Draw("hist")
                real_photon_template_hist.SetTitle("")
                real_photon_template_hist.Draw()



                if photon1_eta_range == "photon1_isScEtaEB":
                    eta_range_no_spaces = "barrel"
                elif photon1_eta_range == "photon1_isScEtaEE":
                    eta_range_no_spaces = "endcap"
                else:
                    assert(0)

                if photon1_pt_range_cutstring == "photon1_pt > 20 && photon1_pt < 25":
                    photon_pt_range_cutstring_no_spaces = "20to25"
                elif photon1_pt_range_cutstring == "photon1_pt > 25 && photon1_pt < 30":
                    photon_pt_range_cutstring_no_spaces = "25to30"
                elif photon1_pt_range_cutstring == "photon1_pt > 30 && photon1_pt < 40":
                    photon_pt_range_cutstring_no_spaces = "30to40"
                elif photon1_pt_range_cutstring == "photon1_pt > 40 && photon1_pt < 50":
                    photon_pt_range_cutstring_no_spaces = "40to50"
                elif photon1_pt_range_cutstring == "photon1_pt > 50 && photon1_pt < 400":
                    photon_pt_range_cutstring_no_spaces = "50to400"
                else:
                    assert(0)


                c1.SaveAs(args.outdir+"/"+args.year+"/"+lepton_name+"/"+eta_range_no_spaces+"/real_photon_template_"+photon_pt_range_cutstring_no_spaces+".png")

                fake_photon_template_hist.GetXaxis().SetTitle("\sigma_{i \eta i \eta}")
                fake_photon_template_hist.SetLineWidth(2)
                fake_photon_template_hist.SetTitle("")
                fake_photon_template_hist.Draw()

                c1.SaveAs(args.outdir+"/"+args.year+"/"+lepton_name+"/"+eta_range_no_spaces+"/fake_photon_template_"+photon_pt_range_cutstring_no_spaces+".png")


                ffitter.Fit()

                total_hist.GetXaxis().SetTitle("\sigma_{i \eta i \eta}")            
                total_hist.SetLineWidth(2)            
                total_hist.Draw()

                c1.SaveAs(args.outdir+"/"+args.year+"/"+lepton_name+"/"+eta_range_no_spaces+"/total_"+photon_pt_range_cutstring_no_spaces+".png")

                total_hist.SetLineColor(ROOT.kBlack)
                total_hist.SetMarkerColor(ROOT.kBlack)
                total_hist.Draw()

                ffitter.GetPlot().SetLineColor(ROOT.kRed)

                ffitter.GetPlot().SetOption("")
                ffitter.GetPlot().Draw("hist same l")

                black_th1f=ROOT.TH1F("black_th1f","black_th1f",1,0,1)
                black_th1f.SetLineColor(ROOT.kBlack)
                black_th1f.SetLineWidth(2)
            #            black_th1f.SetLineStyle(ROOT.kDashed)
                red_th1f=ROOT.TH1F("red_th1f","red_th1f",1,0,1)
                red_th1f.SetLineColor(ROOT.kRed)
                red_th1f.SetLineWidth(2)
#            red_th1f.SetLineStyle(ROOT.kDashed)
                blue_th1f=ROOT.TH1F("blue_th1f","blue_th1f",1,0,1)
                blue_th1f.SetLineColor(ROOT.kBlue)
                blue_th1f.SetLineWidth(2)
#            blue_th1f.SetLineStyle(ROOT.kDashed)
                blue_dashed_th1f=ROOT.TH1F("blue_th1f","blue_th1f",1,0,1)
                blue_dashed_th1f.SetLineColor(ROOT.kBlue)
                blue_dashed_th1f.SetLineWidth(2)
                blue_dashed_th1f.SetLineStyle(ROOT.kDashed)
            
                legend1 = ROOT.TLegend(0.6, 0.7, 0.89, 0.89)
                legend1.SetBorderSize(0)  # no border
                legend1.SetFillStyle(0)  # make transparent
                legend1.AddEntry(black_th1f,"data fitted to","lp")
                legend1.AddEntry(red_th1f,"fit result","lp")
                legend1.Draw("same")

                c1.SaveAs(args.outdir+"/"+args.year+"/"+lepton_name+"/"+eta_range_no_spaces+"/fit_"+photon_pt_range_cutstring_no_spaces+".png")

                c1.ForceUpdate()
                c1.Modified()

                value = ROOT.Double(-1)
                error = ROOT.Double(-1)

                ffitter.GetResult(0,value,error)

                print str(value) + "+/-" + str(error)

                ffitter.GetPlot().SetOption("")
                ffitter.GetPlot().SetLineColor(ROOT.kRed)
#            ffitter.GetPlot().SetLineWidth(2)
                ffitter.GetPlot().SetTitle("")
                ffitter.GetPlot().Draw("hist l")
                real_component = real_photon_template_hist.Clone("real component")
                fake_component = fake_photon_template_hist.Clone("fake component")
            
                real_component.SetLineColor(ROOT.kBlue)
                fake_component.SetLineColor(ROOT.kBlue)
                fake_component.SetLineStyle(ROOT.kDashed)

                real_component.Scale((1-value)*ffitter.GetPlot().Integral()/real_component.Integral())
                fake_component.Scale(value*ffitter.GetPlot().Integral()/fake_component.Integral())
            
                real_component.Draw("hist same l")
                fake_component.Draw("hist same l")
                ffitter.GetPlot().Draw("hist same l")

                legend1 = ROOT.TLegend(0.6, 0.7, 0.89, 0.89)
                legend1.SetBorderSize(0)  # no border
                legend1.SetFillStyle(0)  # make transparent
                legend1.AddEntry(red_th1f,"fit result","lp")
                legend1.AddEntry(blue_th1f,"true component","lp")
                legend1.AddEntry(blue_dashed_th1f,"fake component","lp")
                legend1.Draw("same")
                
                c1.ForceUpdate()
                c1.Modified()

                c1.SaveAs(args.outdir+"/"+args.year+"/"+lepton_name+"/"+eta_range_no_spaces+"/components_"+photon_pt_range_cutstring_no_spaces+".png")

                
                print total_hist.GetXaxis().FindFixBin( sieie_cut )

                print value*fake_photon_template_hist.Integral()/total_hist.Integral()

#            print total_sieie_for_fake_photon_fraction_tree.GetEntries(eta_range+" && lepton_pdg_id == "+lepton_pdg_id+" && (photon_selection == 0 || photon_selection == 1) && "+ photon_pt_range_cutstring)                                                                                                                                                                     
                print fake_photon_tree.GetEntries(photon1_eta_range+ " && lepton_pdg_id == "+lepton_pdg_id+" && (photon1_selection == 3) && "+ photon1_pt_range_cutstring+ " && pass_selection1")

                print value*fake_photon_template_hist.Integral(1,fake_photon_template_hist.GetXaxis().FindFixBin( sieie_cut ))*total_hist.Integral()/total_hist.Integral(1,total_hist.GetXaxis().FindFixBin( sieie_cut ))/fake_photon_template_hist.Integral()



            if fit:
                array_fitted_fraction = np.array([value,error])
                array_fake_fraction = array_fitted_fraction * fake_photon_template_hist.Integral(1,fake_photon_template_hist.GetXaxis().FindFixBin( sieie_cut ))*total_hist.Integral()/total_hist.Integral(1,total_hist.GetXaxis().FindFixBin( sieie_cut ))/fake_photon_template_hist.Integral()
            else:    
                array_fake_fraction = np.array([-1,-1])

            if fit:
                print "numerator = "+str(array_fitted_fraction * fake_photon_template_hist.Integral(1,fake_photon_template_hist.GetXaxis().FindFixBin( sieie_cut ))*total_hist.Integral(\
)/fake_photon_template_hist.Integral())
                array_fake_event_weight = array_fitted_fraction * fake_photon_template_hist.Integral(1,fake_photon_template_hist.GetXaxis().FindFixBin( sieie_cut ))*total_hist.Integral()/fake_photon_template_hist.Integral()/denominator
            else:
                print "numerator = "+str(numerator)
                if denominator > 0: 
                    array_fake_event_weight = np.array([numerator/denominator,0])
                else:    
                    array_fake_event_weight = np.array([-1,-1])

            print "denominator = "+str(denominator)    
                
            if photon1_eta_range == "photon1_isScEtaEB":
                fake_fractions[lepton_name+ "_barrel"].append(list(array_fake_fraction))
            else:
                fake_fractions[lepton_name+ "_endcap"].append(list(array_fake_fraction))

            if photon1_eta_range == "photon1_isScEtaEB":
                fake_event_weights[lepton_name+"_barrel"].append(list(array_fake_event_weight))
            else:
                fake_event_weights[lepton_name+"_endcap"].append(list(array_fake_event_weight))


pprint(fake_fractions)

pprint(fake_event_weights)

json.dump(fake_event_weights,open("fake_photon_event_weights_data.txt","w"))

json.dump(fake_fractions,open("fake_photon_fractions_data.txt","w"))
