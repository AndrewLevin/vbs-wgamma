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

muon_total_sieie_for_fake_photon_fraction_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/single_muon_fake_photon.root") 
muon_fake_photon_template_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/single_muon_fake_photon_template.root")
electron_total_sieie_for_fake_photon_fraction_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/single_electron_fake_photon.root") 
electron_fake_photon_template_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/single_electron_fake_photon_template.root")
real_photon_template_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/real_photon_template.root")

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

            #if not (lepton_pdg_id == "11" and photon_pt_range_cutstring == "photon_pt > 100 && photon_pt < 135" and eta_range == "abs(photon_eta) > 1.566 && abs(photon_eta) < 2.5"):
            #    continue

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
                #n_bins = 160
                #n_bins = 80
                n_bins = 40
                sieie_lower = 0.01
                sieie_upper = 0.06
             

            total_sieie_for_fake_photon_fraction_tree = total_sieie_for_fake_photon_fraction_file.Get("Events")
            total_sieie_for_fake_photon_fraction_hist = ROOT.TH1F("total_sieie_for_fake_photon_fraction_hist","",n_bins,sieie_lower,sieie_upper)
            total_sieie_for_fake_photon_fraction_hist.Sumw2()
            total_sieie_for_fake_photon_fraction_tree.Draw("photon_sieie >> total_sieie_for_fake_photon_fraction_hist",eta_range+" && lepton_pdg_id == "+lepton_pdg_id+" && (photon_selection == 1 || photon_selection == 2) && "+photon_pt_range_cutstring)
            
            fake_photon_template_tree = fake_photon_template_file.Get("Events")
            fake_photon_template_hist = ROOT.TH1F("fake_photon_template_hist","",n_bins,sieie_lower,sieie_upper)
            fake_photon_template_hist.Sumw2()
            fake_photon_template_tree.Draw("photon_sieie >> fake_photon_template_hist",eta_range + " && lepton_pdg_id == "+lepton_pdg_id+" && "+photon_pt_range_cutstring)

            real_photon_template_tree = real_photon_template_file.Get("Events")
            real_photon_template_hist = ROOT.TH1F("real_photon_template_hist","",n_bins,sieie_lower,sieie_upper)
            real_photon_template_hist.Sumw2()
            for i in range(real_photon_template_tree.GetEntries()):
                real_photon_template_tree.GetEntry(i)

                pass_eta_range = False

                if eta_range == "abs(photon_eta) < 1.4442":
                    if abs(real_photon_template_tree.photon_eta) < 1.4442:
                        pass_eta_range = True
                elif eta_range == "abs(photon_eta) > 1.566 && abs(photon_eta) < 2.5":        
                    if 1.4442 < abs(real_photon_template_tree.photon_eta) and abs(real_photon_template_tree.photon_eta) < 2.5:
                        pass_eta_range = True
                else:
                    assert(0)

                pass_lepton_pdg_id = False    
                
                if str(real_photon_template_tree.lepton_pdg_id) == lepton_pdg_id:
                    pass_lepton_pdg_id = True
                    
                pass_photon_pt_range = False

                if photon_pt_range_cutstring == "photon_pt > 25 && photon_pt < 30":
                    if real_photon_template_tree.photon_pt > 25 and real_photon_template_tree.photon_pt < 30:
                        pass_photon_pt_range = True
                elif photon_pt_range_cutstring == "photon_pt > 30 && photon_pt < 40":       
                    if real_photon_template_tree.photon_pt > 30 and real_photon_template_tree.photon_pt < 40:
                        pass_photon_pt_range = True
                elif photon_pt_range_cutstring == "photon_pt > 40 && photon_pt < 50":       
                    if real_photon_template_tree.photon_pt > 40 and real_photon_template_tree.photon_pt < 50:
                        pass_photon_pt_range = True
                elif photon_pt_range_cutstring == "photon_pt > 50 && photon_pt < 70":       
                    if real_photon_template_tree.photon_pt > 50 and real_photon_template_tree.photon_pt < 70:
                        pass_photon_pt_range = True
                elif photon_pt_range_cutstring == "photon_pt > 70 && photon_pt < 100":       
                    if real_photon_template_tree.photon_pt > 70 and real_photon_template_tree.photon_pt < 100:
                        pass_photon_pt_range = True
                elif photon_pt_range_cutstring == "photon_pt > 100 && photon_pt < 135":       
                    if real_photon_template_tree.photon_pt > 100 and real_photon_template_tree.photon_pt < 135:
                        pass_photon_pt_range = True
                elif photon_pt_range_cutstring == "photon_pt > 135 && photon_pt < 400":       
                    if real_photon_template_tree.photon_pt > 135 and real_photon_template_tree.photon_pt < 400:
                        pass_photon_pt_range = True
                else:
                    assert(0)

                if pass_photon_pt_range and pass_lepton_pdg_id and pass_eta_range:        
                    #real_photon_template_hist.Fill(real_photon_template_tree.photon_sieie)
                    if real_photon_template_tree.gen_weight > 0:
                        real_photon_template_hist.Fill(real_photon_template_tree.photon_sieie)
                    else:    
                        real_photon_template_hist.Fill(real_photon_template_tree.photon_sieie,-1)

            for i in range(real_photon_template_hist.GetNbinsX()+2):
                if real_photon_template_hist.GetBinContent(i) < 0:
                    real_photon_template_hist.SetBinContent(i,0)

            mc = ROOT.TObjArray(2)
        
            mc.Add(fake_photon_template_hist)
            mc.Add(real_photon_template_hist)

            ffitter = ROOT.TFractionFitter(total_sieie_for_fake_photon_fraction_hist,mc)

            #ffitter.SetData(total_sieie_for_fake_photon_fraction_hist)
            #ffitter.SetMC(0,fake_photon_template_hist)
            #ffitter.SetMC(1,real_photon_template_hist)

            #print "andrew debug 1"

            c1 = ROOT.TCanvas("c1", "c1",5,50,500,500);

            real_photon_template_hist.GetXaxis().SetTitle("\sigma_{i \eta i \eta}")
            real_photon_template_hist.SetLineWidth(2)
#            real_photon_template_hist.Draw("hist")
            real_photon_template_hist.Draw()

            if eta_range == "abs(photon_eta) < 1.4442":
                eta_range_no_spaces = "barrel"
            elif eta_range == "abs(photon_eta) > 1.566 && abs(photon_eta) < 2.5":     
                eta_range_no_spaces = "endcap"
            else:
                assert(0)

            if photon_pt_range_cutstring == "photon_pt > 25 && photon_pt < 30":
                photon_pt_range_cutstring_no_spaces = "25to30"
            elif photon_pt_range_cutstring == "photon_pt > 30 && photon_pt < 40":       
                photon_pt_range_cutstring_no_spaces = "30to40"
            elif photon_pt_range_cutstring == "photon_pt > 40 && photon_pt < 50":       
                photon_pt_range_cutstring_no_spaces = "40to50"
            elif photon_pt_range_cutstring == "photon_pt > 50 && photon_pt < 70":       
                photon_pt_range_cutstring_no_spaces = "50to70"
            elif photon_pt_range_cutstring == "photon_pt > 70 && photon_pt < 100":       
                photon_pt_range_cutstring_no_spaces = "70to100"
            elif photon_pt_range_cutstring == "photon_pt > 100 && photon_pt < 135":       
                photon_pt_range_cutstring_no_spaces = "100to135"
            elif photon_pt_range_cutstring == "photon_pt > 135 && photon_pt < 400":       
                photon_pt_range_cutstring_no_spaces = "135to400"
            else:
                   assert(0)

            c1.SaveAs("/eos/user/a/amlevin/www/fake-photon/"+lepton_name+"/"+eta_range_no_spaces+"/real_photon_template_"+photon_pt_range_cutstring_no_spaces+".png")
            
            #print "andrew debug 2"

            #raw_input()

            fake_photon_template_hist.GetXaxis().SetTitle("\sigma_{i \eta i \eta}")
            fake_photon_template_hist.SetLineWidth(2)
            fake_photon_template_hist.Draw()

            c1.SaveAs("/eos/user/a/amlevin/www/fake-photon/"+lepton_name+"/"+eta_range_no_spaces+"/fake_photon_template_"+photon_pt_range_cutstring_no_spaces+".png")

#            real_photon_template_hist.SetLineWidth(3)
#            real_photon_template_hist.SetLineColor(ROOT.kRed)
#            real_photon_template_hist.Draw("hist")

#            fake_photon_template_hist.SetLineWidth(3)
#            fake_photon_template_hist.SetLineColor(ROOT.kBlue)
#            fake_photon_template_hist.Draw("same hist")#

#            c1.SaveAs("/eos/user/a/amlevin/www/fake-photon/"+lepton_name+"/"+eta_range_no_spaces+"/both_templates_"+photon_pt_range_cutstring_no_spaces+".png")



            #raw_input()
            
            ffitter.Fit()

            total_sieie_for_fake_photon_fraction_hist.GetXaxis().SetTitle("\sigma_{i \eta i \eta}")            
            total_sieie_for_fake_photon_fraction_hist.SetLineWidth(2)            
            total_sieie_for_fake_photon_fraction_hist.Draw()

            c1.SaveAs("/eos/user/a/amlevin/www/fake-photon/"+lepton_name+"/"+eta_range_no_spaces+"/total_"+photon_pt_range_cutstring_no_spaces+".png")

            total_sieie_for_fake_photon_fraction_hist.Draw()

            ffitter.GetPlot().SetLineColor(ROOT.kRed)
#            ffitter.GetPlot().SetLineWidth(2)
#            ffitter.GetPlot().SetLineStyle(ROOT.kDashed)
#            ffitter.GetPlot().SetMarkerSize(3)
#            ffitter.GetPlot().SetMarkerStyle(ROOT.kStar)
#            ffitter.GetPlot().SetMarkerStyle(9)

            ffitter.GetPlot().SetOption("")
            ffitter.GetPlot().Draw("hist same l")

            red_th1f=ROOT.TH1F("red_th1f","red_th1f",1,0,1)
            red_th1f.SetLineColor(ROOT.kRed)
            red_th1f.SetLineWidth(2)
#            red_th1f.SetLineStyle(ROOT.kDashed)
            blue_th1f=ROOT.TH1F("blue_th1f","blue_th1f",1,0,1)
            blue_th1f.SetLineColor(ROOT.kBlue)
            blue_th1f.SetLineWidth(2)
#            blue_th1f.SetLineStyle(ROOT.kDashed)
            
            legend1 = ROOT.TLegend(0.6, 0.7, 0.89, 0.89)
            legend1.SetBorderSize(0)  # no border
            legend1.SetFillStyle(0)  # make transparent
            legend1.AddEntry(blue_th1f,"data fitted to","lp")
            legend1.AddEntry(red_th1f,"fit result","lp")
            legend1.Draw("same")

            c1.SaveAs("/eos/user/a/amlevin/www/fake-photon/"+lepton_name+"/"+eta_range_no_spaces+"/fit_"+photon_pt_range_cutstring_no_spaces+".png")
                
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
