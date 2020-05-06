import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

#when the TMinuit object is reused, the random seed is not reset after each fit, so the fit result can change when it is run on the same input
ROOT.TMinuitMinimizer.UseStaticMinuit(False)

ROOT.ROOT.EnableImplicitMT()

import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--chiso_denom',action='store_true')
parser.add_argument('--subtract_prompt_from_denom',action='store_true')
parser.add_argument('--true',action='store_true')
parser.add_argument('--mc',action='store_true')
parser.add_argument('--year',dest='year',default='2016')
parser.add_argument('--lep',dest='lep',default='both')
parser.add_argument('-o',dest='outdir',default="/eos/user/a/amlevin/www/wg/fake-photon-fits/")

args = parser.parse_args()

assert(not args.subtract_prompt_from_denom or not args.mc)

assert(not args.true or args.mc)

#there is a bug which causes a crash inside of the TFractionFitter destructor: https://sft.its.cern.ch/jira/browse/ROOT-9414
#I think this makes it necessary to create the tfractionfitters only once for each set of input files that are used, and then reuse the tfractionfitters

import sys
import random
import numpy as np
import json

from pprint import pprint

ROOT.gStyle.SetOptStat(0)

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

photon1_pt_range_cutstrings = ["photon1_pt > 20 && photon1_pt < 30","photon1_pt > 30 && photon1_pt < 40","photon1_pt > 40 && photon1_pt < 50","photon1_pt > 50 && photon1_pt < 400"]
photon2_pt_range_cutstrings = ["photon2_pt > 20 && photon2_pt < 30","photon2_pt > 30 && photon2_pt < 40","photon2_pt > 40 && photon2_pt < 50","photon2_pt > 50 && photon2_pt < 400"]

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

if args.true:
    photon1_veto_signal_selection_cutstring = "((puppimet > 40 && lepton_pt > 30 && photon1_pt > 25 && abs(lepton_pdg_id) == 11) || (puppimet > 40 && lepton_pt > 25 && photon1_pt > 25 && abs(lepton_pdg_id) == 13))" 
    photon2_veto_signal_selection_cutstring = "((puppimet > 40 && lepton_pt > 30 && photon2_pt > 25 && abs(lepton_pdg_id) == 11) || (puppimet > 40 && lepton_pt > 25 && photon2_pt > 25 && abs(lepton_pdg_id) == 13))" 
else:
    photon1_veto_signal_selection_cutstring = "!((puppimet > 40 && lepton_pt > 30 && photon1_pt > 25 && abs(lepton_pdg_id) == 11) || (puppimet > 40 && lepton_pt > 25 && photon1_pt > 25 && abs(lepton_pdg_id) == 13))" 
    photon2_veto_signal_selection_cutstring = "!((puppimet > 40 && lepton_pt > 30 && photon2_pt > 25 && abs(lepton_pdg_id) == 11) || (puppimet > 40 && lepton_pt > 25 && photon2_pt > 25 && abs(lepton_pdg_id) == 13))" 

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

if not args.chiso_denom:
    max_sieie_barrel = sieie_barrel*1.75
    max_sieie_endcap = sieie_endcap*1.75
    max_chiso_barrel = chiso_barrel*1000
    max_chiso_endcap = chiso_endcap*1000
else:    
    max_sieie_barrel = sieie_barrel*1000
    max_sieie_endcap = sieie_endcap*1000
    max_chiso_barrel = chiso_barrel*1.75
    max_chiso_endcap = chiso_endcap*1.75
 
njets_min = 0
njets_max = 1000

#mc_fake_photon_samples = []

mc_fake_photon_samples = [{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/"+args.year+"/1June2019/wjets_fake_photon.root","xs" : 60430.0, "prompt" : False},{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/"+args.year+"/1June2019/wgjets_fake_photon.root","xs" : 178.6, "prompt" : True}]

#mc_fake_photon_samples = [{"file" : ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/"+args.year+"/1June2019/wjets_fake_photon.root"),"xs" : 60430.0, "prompt" : False}]

muon_data_fake_photon_samples = [{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/"+args.year+"/1June2019/single_muon_fake_photon.root"}]

if args.year == "2016" or args.year == "2017":
    electron_data_fake_photon_samples = [{"file" : "/afs/cern.ch/work/a/amlevin/data/wg/"+args.year+"/1June2019/single_electron_fake_photon.root"}]
elif args.year == "2018":
    electron_data_fake_photon_samples = [{"file" : "/afs/cern.ch/work/a/amlevin/data/wg/"+args.year+"/1June2019/egamma_fake_photon.root"}]
else:
    assert(0)

data_fake_photon_samples = [{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/"+args.year+"/1June2019/data_fake_photon.root"}]

#data_fake_photon_samples = []

#muon_data_fake_photon_samples = []
#electron_data_fake_photon_samples = []

real_photon_template_filename = "/afs/cern.ch/work/a/amlevin/data/wg/"+args.year+"/1June2019/real_photon_template.root"

created_muon_fitter = False
created_electron_fitter = False

dict_lumi = {"2016" : 35.9, "2017" : 41.5, "2018" : 59.6}

lumi=dict_lumi[args.year]

if args.lep == "muon":
    lepton_pdg_id = "(lepton_pdg_id == 13)"
elif args.lep == "electron":
    lepton_pdg_id = "(lepton_pdg_id == 11)"
elif args.lep == "both":    
    lepton_pdg_id = "true"
else:
    assert(0)

if args.lep == "muon":
    fake_photon_data_samples = muon_data_fake_photon_samples
    fake_photon_mc_samples = mc_fake_photon_samples
elif args.lep == "electron":
    fake_photon_data_samples = electron_data_fake_photon_samples
    fake_photon_mc_samples = mc_fake_photon_samples
elif args.lep == "both":
    fake_photon_data_samples = data_fake_photon_samples
    fake_photon_mc_samples = mc_fake_photon_samples
else:
    assert(0)

for i in range(len(photon1_eta_ranges)):
    for j in range(len(photon1_pt_range_cutstrings)):

        photon1_eta_range = photon1_eta_ranges[i]
        photon2_eta_range = photon2_eta_ranges[i]
        photon1_pt_range_cutstring = photon1_pt_range_cutstrings[j]
        photon2_pt_range_cutstring = photon2_pt_range_cutstrings[j]
        
        print "Processing " + photon1_eta_range + ", " + photon1_pt_range_cutstring

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


        if not args.true:    
            total_hist_model = ROOT.RDF.TH1DModel("","",n_bins,sieie_lower,sieie_upper)
            total_hist = total_hist_model.GetHistogram()
            total_hist.Sumw2()

            fake_photon_template_hist_model = ROOT.RDF.TH1DModel("","",n_bins,sieie_lower,sieie_upper)
            fake_photon_template_hist = fake_photon_template_hist_model.GetHistogram()
            fake_photon_template_hist.Sumw2()

        numerator = float(0)
        denominator = float(0)

        if not args.mc:

            for k,fake_photon_data_sample in enumerate(fake_photon_data_samples):

                rdf=ROOT.RDataFrame("Events",fake_photon_data_sample["filename"])

                denominator+=rdf.Filter(photon1_eta_range+ " && "+lepton_pdg_id + " && (photon1_selection == "+den_pho_sel+") && "+ photon1_pt_range_cutstring + " && pass_selection1" + " && " + photon1_recoil_cutstring + " && njets_fake >= "+ str(njets_min) + " && njets_fake <= "+str(njets_max) + " && photon1_sieie < "+str(max_sieie) + " && photon1_pfRelIso03_chg*photon1_pt < "+str(max_chiso)+ " && " + str(photon1_veto_signal_selection_cutstring)).Count().GetValue()


            for k,fake_photon_data_sample in enumerate(fake_photon_data_samples):

                rresultptr_total_hist_data = rdf.Filter(photon1_eta_range+ " && "+lepton_pdg_id+" && (photon1_selection == 0 || photon1_selection == 4) && "+photon1_pt_range_cutstring + " && pass_selection1 && "+str(photon1_veto_signal_selection_cutstring) + " && " + photon1_recoil_cutstring + "&& njets_fake >= "+str(njets_min) + " && njets_fake <= "+str(njets_max)).Histo1D(total_hist_model,"photon1_sieie")

                total_hist.Add(rresultptr_total_hist_data.GetValue())

                rresultptr_fake_photon_template_hist_data = rdf.Filter(photon2_eta_range + " && "+lepton_pdg_id+" && "+photon2_pt_range_cutstring + " && pass_selection2 && "+str(photon2_veto_signal_selection_cutstring)  + " && " + photon2_recoil_cutstring +" && njets_fake_template  >= "+str(njets_min) + " && njets_fake_template <= " + str(njets_max)).Histo1D(total_hist_model,"photon2_sieie")

                fake_photon_template_hist.Add(rresultptr_fake_photon_template_hist_data.GetValue())

        else:

            for k,fake_photon_mc_sample in enumerate(fake_photon_mc_samples):   

                rdf=ROOT.RDataFrame("Events",fake_photon_mc_sample["filename"])

                if fake_photon_mc_sample["prompt"]:
                    photon1_gen_matching_cutstring = "(photon1_gen_matching == 6 || photon1_gen_matching == 5 || photon1_gen_matching == 4 || photon1_gen_matching == 1)"
                    photon2_gen_matching_cutstring = "(photon2_gen_matching == 6 || photon2_gen_matching == 5 || photon2_gen_matching == 4 || photon2_gen_matching == 1)"
#                photon1_gen_matching_cutstring = "photon1_gen_matching_old > 0"
#                photon2_gen_matching_cutstring = "photon2_gen_matching_old > 0"
                else:
                    photon1_gen_matching_cutstring = "!(photon1_gen_matching == 6 || photon1_gen_matching == 5 || photon1_gen_matching == 4 || photon1_gen_matching == 1)"
                    photon2_gen_matching_cutstring = "!(photon2_gen_matching == 6 || photon2_gen_matching == 5 || photon2_gen_matching == 4 || photon2_gen_matching == 1)"    

                if not fake_photon_mc_sample["prompt"]:
                    tfile=ROOT.TFile.Open(fake_photon_mc_sample["filename"])
                    neventsgenweighted=tfile.Get("nEventsGenWeighted").GetBinContent(1)
                    denominator+=rdf.Filter(photon1_eta_range+ " && "+lepton_pdg_id + " && (photon1_selection == "+den_pho_sel+") && "+ photon1_pt_range_cutstring + " && pass_selection1" + " && " + photon1_recoil_cutstring + " && njets_fake >= "+ str(njets_min) + " && njets_fake <= "+str(njets_max) + " && photon1_sieie < "+str(max_sieie) + " && photon1_pfRelIso03_chg*photon1_pt < "+str(max_chiso) + " && gen_weight > 0 && " + photon1_gen_matching_cutstring+ " && " + str(photon1_veto_signal_selection_cutstring)).Count().GetValue()*fake_photon_mc_sample["xs"]*1000*lumi/neventsgenweighted
                    denominator-=rdf.Filter(photon1_eta_range+ " && "+lepton_pdg_id + " && (photon1_selection == "+den_pho_sel+") && "+ photon1_pt_range_cutstring + " && pass_selection1" + " && " + photon1_recoil_cutstring + " && njets_fake >= "+ str(njets_min) + " && njets_fake <= "+str(njets_max) + " && photon1_sieie < "+str(max_sieie) + " && photon1_pfRelIso03_chg*photon1_pt < "+str(max_chiso) + " && gen_weight < 0 && " + photon1_gen_matching_cutstring+ " && " + str(photon1_veto_signal_selection_cutstring)).Count().GetValue()*fake_photon_mc_sample["xs"]*1000*lumi/neventsgenweighted

                if not args.true:    

                    tfile=ROOT.TFile.Open(fake_photon_mc_sample["filename"])
                    neventsgenweighted=tfile.Get("nEventsGenWeighted").GetBinContent(1)

                    rdf=ROOT.RDataFrame("Events",fake_photon_mc_sample["filename"])

                    rresultptr_total_hist = rdf.Filter(photon1_eta_range+ " && "+lepton_pdg_id+" && (photon1_selection == 0 || photon1_selection == 4) && "+photon1_pt_range_cutstring + " && pass_selection1 && "+str(photon1_veto_signal_selection_cutstring) + " && " + photon1_recoil_cutstring + "&& njets_fake >= "+str(njets_min) + " && njets_fake <= "+str(njets_max) + " && " + photon1_gen_matching_cutstring).Define("weight",str(fake_photon_mc_sample["xs"]*1000*lumi/neventsgenweighted)+"*gen_weight/abs(gen_weight)").Histo1D(total_hist_model,"photon1_sieie","weight")

                    total_hist.Add(rresultptr_total_hist.GetValue())

                    rresultptr_fake_photon_template_hist = rdf.Filter(photon2_eta_range + " && "+lepton_pdg_id+" && "+photon2_pt_range_cutstring + " && pass_selection2 && "+str(photon2_veto_signal_selection_cutstring)  + " && " + photon2_recoil_cutstring +" && njets_fake_template  >= "+str(njets_min) + " && njets_fake_template <= " + str(njets_max)  + " && "+photon2_gen_matching_cutstring).Define("weight",str(fake_photon_mc_sample["xs"]*1000*lumi/neventsgenweighted)+"*gen_weight/abs(gen_weight)").Histo1D(fake_photon_template_hist_model,"photon2_sieie","weight")
                
                    fake_photon_template_hist.Add(rresultptr_fake_photon_template_hist.GetValue())

                else:
                    if not fake_photon_mc_sample["prompt"]:
                        
                        tfile= ROOT.TFile.Open(fake_photon_mc_sample["filename"])
                        
                        neventsgenweighted=tfile.Get("nEventsGenWeighted").GetBinContent(1)

                        rdf=ROOT.RDataFrame("Events",fake_photon_mc_sample["filename"])

                        numerator+=rdf.Filter(photon1_eta_range+ " && "+lepton_pdg_id + " && (photon1_selection == 0) && "+ photon1_pt_range_cutstring + " && pass_selection1" + " && " + photon1_recoil_cutstring + " && njets_fake >= "+ str(njets_min) + " && njets_fake <= "+str(njets_max) + " && gen_weight > 0 &&" + photon1_gen_matching_cutstring+ " && " + str(photon1_veto_signal_selection_cutstring)).Count().GetValue()*fake_photon_mc_sample["xs"]*1000*lumi/neventsgenweighted
                        numerator-=rdf.Filter(photon1_eta_range+ " && "+lepton_pdg_id + " && (photon1_selection == 0) && "+ photon1_pt_range_cutstring + " && pass_selection1" + " && " + photon1_recoil_cutstring + " && njets_fake >= "+ str(njets_min) + " && njets_fake <= "+str(njets_max) + " && gen_weight < 0 &&" + photon1_gen_matching_cutstring+ " && " + str(photon1_veto_signal_selection_cutstring)).Count().GetValue()*fake_photon_mc_sample["xs"]*1000*lumi/neventsgenweighted

        if args.subtract_prompt_from_denom:        
            for k,fake_photon_mc_sample in enumerate(fake_photon_mc_samples):   

                if fake_photon_mc_sample["prompt"]:
                    tfile= ROOT.TFile.Open(fake_photon_mc_sample["filename"])
                    neventsgenweighted=tfile.Get("nEventsGenWeighted").GetBinContent(1)
                    rdf=ROOT.RDataFrame("Events",fake_photon_mc_sample["filename"])
                    photon1_gen_matching_cutstring = "(photon1_gen_matching == 6 || photon1_gen_matching == 5 || photon1_gen_matching == 4 || photon1_gen_matching == 1)"
                    photon2_gen_matching_cutstring = "(photon2_gen_matching == 6 || photon2_gen_matching == 5 || photon2_gen_matching == 4 || photon2_gen_matching == 1)"
                    denominator-=rdf.Filter(photon1_eta_range+ " && "+lepton_pdg_id + " && (photon1_selection == "+den_pho_sel+") && "+ photon1_pt_range_cutstring + " && pass_selection1" + " && " + photon1_recoil_cutstring + " && njets_fake >= "+ str(njets_min) + " && njets_fake <= "+str(njets_max) + " && photon1_sieie < "+str(max_sieie) + " && photon1_pfRelIso03_chg*photon1_pt < "+str(max_chiso) + " && gen_weight > 0 && " + photon1_gen_matching_cutstring+ " && " + str(photon1_veto_signal_selection_cutstring)).Count().GetValue()*fake_photon_mc_sample["xs"]*1000*lumi/neventsgenweighted
                    denominator+=rdf.Filter(photon1_eta_range+ " && "+lepton_pdg_id + " && (photon1_selection == "+den_pho_sel+") && "+ photon1_pt_range_cutstring + " && pass_selection1" + " && " + photon1_recoil_cutstring + " && njets_fake >= "+ str(njets_min) + " && njets_fake <= "+str(njets_max) + " && photon1_sieie < "+str(max_sieie) + " && photon1_pfRelIso03_chg*photon1_pt < "+str(max_chiso) + " && gen_weight < 0 && "  + photon1_gen_matching_cutstring + " && " + str(photon1_veto_signal_selection_cutstring)).Count().GetValue()*fake_photon_mc_sample["xs"]*1000*lumi/neventsgenweighted

        if not args.true:        

            rdf=ROOT.RDataFrame("Events",real_photon_template_filename)
            real_photon_template_hist_model = ROOT.RDF.TH1DModel("","",n_bins,sieie_lower,sieie_upper)
            real_photon_template_hist = real_photon_template_hist_model.GetHistogram()
            real_photon_template_hist.Sumw2()

            rresultptr_real_photon_template_hist=rdf.Filter(photon1_eta_range.replace("photon1","photon") + " && " + photon1_pt_range_cutstring.replace("photon1","photon")+ " && " + lepton_pdg_id).Define("weight","gen_weight/abs(gen_weight)").Histo1D(real_photon_template_hist_model,"photon_sieie","weight")
            real_photon_template_hist.Add(rresultptr_real_photon_template_hist.GetValue())

            for k in range(real_photon_template_hist.GetNbinsX()+2):
                if real_photon_template_hist.GetBinContent(k) < 0:
                    real_photon_template_hist.SetBinContent(k,0)

#            for k in range(fake_photon_template_hist.GetNbinsX()+2):
#                if fake_photon_template_hist.GetBinContent(k) < 0:
#                    fake_photon_template_hist.SetBinContent(k,0)

            print "andrew debug 1"
            fake_photon_template_hist.Print("all")
            print "andrew debug 2"
            real_photon_template_hist.Print("all")
            print "andrew debug 3"
            total_hist.Print("all")
            print "andrew debug 4"

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

            if photon1_pt_range_cutstring == "photon1_pt > 20 && photon1_pt < 30":
                photon_pt_range_cutstring_no_spaces = "20to30"
            elif photon1_pt_range_cutstring == "photon1_pt > 30 && photon1_pt < 40":
                photon_pt_range_cutstring_no_spaces = "30to40"
            elif photon1_pt_range_cutstring == "photon1_pt > 40 && photon1_pt < 50":
                photon_pt_range_cutstring_no_spaces = "40to50"
            elif photon1_pt_range_cutstring == "photon1_pt > 50 && photon1_pt < 400":
                photon_pt_range_cutstring_no_spaces = "50to400"
            else:
                assert(0)


            c1.SaveAs(args.outdir+"/"+args.year+"/"+args.lep+"/"+eta_range_no_spaces+"/real_photon_template_"+photon_pt_range_cutstring_no_spaces+".png")
            
            fake_photon_template_hist.GetXaxis().SetTitle("\sigma_{i \eta i \eta}")
            fake_photon_template_hist.SetLineWidth(2)
            fake_photon_template_hist.SetTitle("")
            fake_photon_template_hist.Draw()
            
            c1.SaveAs(args.outdir+"/"+args.year+"/"+args.lep+"/"+eta_range_no_spaces+"/fake_photon_template_"+photon_pt_range_cutstring_no_spaces+".png")
            
            ROOT.gROOT.cd() #avoids some TFractionFitter destructor crashes (see https://sft.its.cern.ch/jira/browse/ROOT-10752)
            ffitter.Fit()
            
            total_hist.GetXaxis().SetTitle("\sigma_{i \eta i \eta}")            
            total_hist.SetLineWidth(2)            
            total_hist.Draw()

            c1.SaveAs(args.outdir+"/"+args.year+"/"+args.lep+"/"+eta_range_no_spaces+"/total_"+photon_pt_range_cutstring_no_spaces+".png")

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

            c1.SaveAs(args.outdir+"/"+args.year+"/"+args.lep+"/"+eta_range_no_spaces+"/fit_"+photon_pt_range_cutstring_no_spaces+".png")
            
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

            c1.SaveAs(args.outdir+"/"+args.year+"/"+args.lep+"/"+eta_range_no_spaces+"/components_"+photon_pt_range_cutstring_no_spaces+".png")

                
            print total_hist.GetXaxis().FindFixBin( sieie_cut )
            
            print value*fake_photon_template_hist.Integral()/total_hist.Integral()

#            print total_sieie_for_fake_photon_fraction_tree.GetEntries(eta_range+" && lepton_pdg_id == "+lepton_pdg_id+" && (photon_selection == 0 || photon_selection == 1) && "+ photon_pt_range_cutstring)                                                                                                                                                                     
#            print fake_photon_tree.GetEntries(photon1_eta_range+ " && lepton_pdg_id == "+lepton_pdg_id+" && (photon1_selection == 3) && "+ photon1_pt_range_cutstring+ " && pass_selection1")

#            print value*fake_photon_template_hist.Integral(1,fake_photon_template_hist.GetXaxis().FindFixBin( sieie_cut ))*total_hist.Integral()/total_hist.Integral(1,total_hist.GetXaxis().FindFixBin( sieie_cut ))/fake_photon_template_hist.Integral()



        if not args.true:
            array_fitted_fraction = np.array([value,error])
            array_fake_fraction = array_fitted_fraction * fake_photon_template_hist.Integral(1,fake_photon_template_hist.GetXaxis().FindFixBin( sieie_cut ))*total_hist.Integral()/total_hist.Integral(1,total_hist.GetXaxis().FindFixBin( sieie_cut ))/fake_photon_template_hist.Integral()
        else:    
            array_fake_fraction = np.array([-1,-1])

        if not args.true:
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
            fake_fractions[args.lep+ "_barrel"].append(list(array_fake_fraction))
        else:
            fake_fractions[args.lep+ "_endcap"].append(list(array_fake_fraction))

        if photon1_eta_range == "photon1_isScEtaEB":
            fake_event_weights[args.lep+"_barrel"].append(list(array_fake_event_weight))
        else:
            fake_event_weights[args.lep+"_endcap"].append(list(array_fake_event_weight))

pprint(fake_fractions)

pprint(fake_event_weights)

json.dump(fake_event_weights,open("fake_photon_event_weights_data.txt","w"))

json.dump(fake_fractions,open("fake_photon_fractions_data.txt","w"))
