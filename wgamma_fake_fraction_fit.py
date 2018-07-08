#there is a bug which causes a crash inside of the TFractionFitter destructor: https://sft.its.cern.ch/jira/browse/ROOT-9414
#I think this makes it necessary to create the tfractionfitters only once for each set of input files that are used, and then reuse the tfractionfitters

import sys
import random
import ROOT

ROOT.gStyle.SetOptStat(0)

fake_fractions = {}

fake_event_weights = {}

fake_fractions["muon_barrel"] = []

fake_fractions["muon_endcap"] = []

fake_fractions["electron_barrel"] = []

fake_fractions["electron_endcap"] = []

fake_event_weights["muon_barrel"] = []

fake_event_weights["muon_endcap"] = []

fake_event_weights["electron_barrel"] = []

fake_event_weights["electron_endcap"] = []

#lepton_names =["muon","electron"]
lepton_names =["electron","muon"]

eta_ranges = ["abs(photon_eta) < 1.4442","abs(photon_eta) > 1.566 && abs(photon_eta) < 2.5"]

photon_pt_range_cutstrings = ["photon_pt > 25 && photon_pt < 30","photon_pt > 30 && photon_pt < 40","photon_pt > 40 && photon_pt < 50","photon_pt > 50 && photon_pt < 70","photon_pt > 70 && photon_pt < 100","photon_pt > 100 && photon_pt < 135","photon_pt > 135 && photon_pt < 400"]

index = 0

muon_total_sieie_for_fake_photon_fraction_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wgamma_single_muon_fake_photon.root") 
muon_fake_photon_template_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wgamma_single_muon_fake_photon_template.root")
electron_total_sieie_for_fake_photon_fraction_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wgamma_single_electron_fake_photon.root") 
electron_fake_photon_template_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wgamma_single_electron_fake_photon_template.root")
real_photon_template_file = ROOT.TFile.Open("/afs/cern.ch/user/a/amlevin/vbs-wgamma/wgamma_real_photon_template.root")

created_muon_fitter = False
created_electron_fitter = False


for lepton_name in lepton_names:

    if lepton_name == "muon":
        lepton_pdg_id = "13"
        total_sieie_for_fake_photon_fraction_file = muon_total_sieie_for_fake_photon_fraction_file
    else:    
        lepton_pdg_id = "11"
        total_sieie_for_fake_photon_fraction_file = electron_total_sieie_for_fake_photon_fraction_file

    if lepton_name == "muon":
        fake_photon_template_file = muon_fake_photon_template_file
    else:    
        fake_photon_template_file = electron_fake_photon_template_file
    
    for eta_range in eta_ranges:
        for photon_pt_range_cutstring in photon_pt_range_cutstrings:

            index = index+1
        
            i = str(index)

            print i
            
            if eta_range == "abs(photon_eta) < 1.4442":
                sieie_cut = 0.01022
                n_bins = 128
                sieie_lower = 0.00
                sieie_upper = 0.04
            else:
                sieie_cut = 0.03001
                n_bins = 160
                sieie_lower = 0.01
                sieie_upper = 0.06
             

            total_sieie_for_fake_photon_fraction_tree = total_sieie_for_fake_photon_fraction_file.Get("Events")
            total_sieie_for_fake_photon_fraction_hist = ROOT.TH1F("total_sieie_for_fake_photon_fraction_hist","total_sieie_for_fake_photon_fraction_hist",n_bins,sieie_lower,sieie_upper)
            total_sieie_for_fake_photon_fraction_tree.Draw("photon_sieie >> total_sieie_for_fake_photon_fraction_hist",eta_range+" && lepton_pdg_id == "+lepton_pdg_id+" && (photon_selection == 1 || photon_selection == 2) && "+photon_pt_range_cutstring)
            
            fake_photon_template_tree = fake_photon_template_file.Get("Events")
            fake_photon_template_hist = ROOT.TH1F("fake_photon_template_hist","fake_photon_template_hist",n_bins,sieie_lower,sieie_upper)
            fake_photon_template_tree.Draw("photon_sieie >> fake_photon_template_hist",eta_range + " && lepton_pdg_id == "+lepton_pdg_id+" && "+photon_pt_range_cutstring)

            real_photon_template_tree = real_photon_template_file.Get("Events")
            real_photon_template_hist = ROOT.TH1F("real_photon_template_hist","real_photon_template_hist",n_bins,sieie_lower,sieie_upper)
            real_photon_template_tree.Draw("photon_sieie >> real_photon_template_hist",eta_range + " && lepton_pdg_id == "+lepton_pdg_id+" && "+photon_pt_range_cutstring,"gen_weight > 0 ? 1 : -1")

            mc = ROOT.TObjArray(2)
        
            mc.Add(fake_photon_template_hist)
            mc.Add(real_photon_template_hist)

            if created_muon_fitter == False and lepton_name == "muon":

                muon_ffitter = ROOT.TFractionFitter(total_sieie_for_fake_photon_fraction_hist,mc)

                created_muon_fitter = True

            elif created_electron_fitter == False and lepton_name == "electron":

                electron_ffitter = ROOT.TFractionFitter(total_sieie_for_fake_photon_fraction_hist,mc)

                created_electron_fitter = True

            if lepton_name == "muon":
                ffitter = muon_ffitter
            else:
                ffitter = electron_ffitter


            ffitter.SetData(total_sieie_for_fake_photon_fraction_hist)
            ffitter.SetMC(0,fake_photon_template_hist)
            ffitter.SetMC(1,real_photon_template_hist)
            
            ffitter.Fit()
            
            c1 = ROOT.TCanvas("c1", "c1",5,50,500,500);

            total_sieie_for_fake_photon_fraction_hist.Draw("Ep")

            ffitter.GetPlot().Draw("same")
                
            c1.ForceUpdate()
            c1.Modified()
                
            value = ROOT.Double(-1)
            error = ROOT.Double(-1)
                
            ffitter.GetResult(0,value,error)
                
            print str(value) + "+/-" + str(error)

            print total_sieie_for_fake_photon_fraction_hist.GetXaxis().FindFixBin( sieie_cut )

            print value*fake_photon_template_hist.Integral()/total_sieie_for_fake_photon_fraction_hist.Integral()

            print total_sieie_for_fake_photon_fraction_tree.GetEntries(eta_range+" && lepton_pdg_id == "+lepton_pdg_id+" && (photon_selection == 0 || photon_selection == 1) && "+ photon_pt_range_cutstring)

            print value*fake_photon_template_hist.Integral(1,fake_photon_template_hist.GetXaxis().FindFixBin( sieie_cut ))*total_sieie_for_fake_photon_fraction_hist.Integral()/total_sieie_for_fake_photon_fraction_hist.Integral(1,total_sieie_for_fake_photon_fraction_hist.GetXaxis().FindFixBin( sieie_cut ))/fake_photon_template_hist.Integral()

            if eta_range == "abs(photon_eta) < 1.4442":

                fake_fractions[lepton_name+ "_barrel"].append(value*fake_photon_template_hist.Integral(1,fake_photon_template_hist.GetXaxis().FindFixBin( sieie_cut ))*total_sieie_for_fake_photon_fraction_hist.Integral()/total_sieie_for_fake_photon_fraction_hist.Integral(1,total_sieie_for_fake_photon_fraction_hist.GetXaxis().FindFixBin( sieie_cut ))/fake_photon_template_hist.Integral())

            else:    

                fake_fractions[lepton_name+ "_endcap"].append(value*fake_photon_template_hist.Integral(1,fake_photon_template_hist.GetXaxis().FindFixBin( sieie_cut ))*total_sieie_for_fake_photon_fraction_hist.Integral()/total_sieie_for_fake_photon_fraction_hist.Integral(1,total_sieie_for_fake_photon_fraction_hist.GetXaxis().FindFixBin( sieie_cut ))/fake_photon_template_hist.Integral())


            print value*fake_photon_template_hist.Integral(1,fake_photon_template_hist.GetXaxis().FindFixBin( sieie_cut ))*total_sieie_for_fake_photon_fraction_hist.Integral()/fake_photon_template_hist.Integral()/total_sieie_for_fake_photon_fraction_tree.GetEntries(eta_range + " && lepton_pdg_id == "+lepton_pdg_id+" && (photon_selection == 0 || photon_selection == 1) && "+ photon_pt_range_cutstring)

            if eta_range == "abs(photon_eta) < 1.4442":

                fake_event_weights[lepton_name+"_barrel"].append(value*fake_photon_template_hist.Integral(1,fake_photon_template_hist.GetXaxis().FindFixBin( sieie_cut ))*total_sieie_for_fake_photon_fraction_hist.Integral()/fake_photon_template_hist.Integral()/total_sieie_for_fake_photon_fraction_tree.GetEntries(eta_range + " && lepton_pdg_id == "+lepton_pdg_id+" && (photon_selection == 0 || photon_selection == 1) && "+ photon_pt_range_cutstring))

            else:

                fake_event_weights[lepton_name+"_endcap"].append(value*fake_photon_template_hist.Integral(1,fake_photon_template_hist.GetXaxis().FindFixBin( sieie_cut ))*total_sieie_for_fake_photon_fraction_hist.Integral()/fake_photon_template_hist.Integral()/total_sieie_for_fake_photon_fraction_tree.GetEntries(eta_range + " && lepton_pdg_id == "+lepton_pdg_id+" && (photon_selection == 0 || photon_selection == 1) && "+ photon_pt_range_cutstring))
                

print fake_fractions

print fake_event_weights
