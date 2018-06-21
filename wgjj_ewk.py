photon_eta_cutstring = "1.566 < abs(photon_eta) && abs(photon_eta) < 2.5"
#photon_eta_cutstring = "abs(photon_eta) < 1.4442"

#lepton_name = "muon"
lepton_name = "electron"

import sys
import style

import optparse

parser = optparse.OptionParser()

parser.add_option('--lumi',dest='lumi')
parser.add_option('--variable',dest='variable')
parser.add_option('--xaxislabel',dest='xaxislabel',default='m_{jj} (GeV)')

parser.add_option('-i',dest='inputfile')
parser.add_option('-o',dest='outputfile',default="/eos/user/a/amlevin/www/tmp/delete_this.png")

(options,args) = parser.parse_args()

import eff_scale_factor

from ROOT import *

xoffsetstart = 0.0;
yoffsetstart = 0.0;
xoffset = 0.20;
yoffset = 0.05;

xpositions = [0.60,0.60,0.60,0.60,0.60,0.60,0.40,0.40,0.40]
ypositions = [0,1,2,3,4,5,0,1,2]

style.GoodStyle().cd()

muon_fr_file = TFile("/afs/cern.ch/user/a/amlevin/vbs-wgamma/muon_frs.root")
electron_fr_file = TFile("/afs/cern.ch/user/a/amlevin/vbs-wgamma/electron_frs.root")

muon_fr_hist=muon_fr_file.Get("muon_frs")
electron_fr_hist=electron_fr_file.Get("electron_frs")

from array import array

photon_ptbins=array('d', [25,30,40,50,70,100,135,400])

fake_photon_event_weights_muon_barrel = [0.15484810789240228, 0.11524277444694236, 0.09110788743705224, 0.07294107854072265, 0.06490413072813697, 0.04693263880230566, 0.03503294901179513]

fake_photon_event_weights_electron_barrel = [0.1447727736767519, 0.11180460340651761, 0.08074003048354975, 0.06530210040842324, 0.05420211026702524, 0.048118621720450956, 0.02967721492668453]

fake_photon_event_weights_muon_endcap = [0.20783807385298056, 0.17530144239812215, 0.14802126262996834, 0.1137724518288847, 0.09480076729582236, 0.057066601725354965, 0.043023751606317905]

fake_photon_event_weights_electron_endcap = [0.197481755047577, 0.15028936497262135, 0.1197346440252747, 0.10517930137670145, 0.08989475516812702, 0.04777790529184045, 0.0388377405319603]

fake_photon_event_weights_muon_barrel_hist=TH1F("fake_photon_event_weights_muon_barrel_hist","fake_photon_event_weights_muon_barrel_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_event_weights_electron_barrel_hist=TH1F("fake_photon_event_weights_electron_barrel_hist","fake_photon_event_weights_electron_barrel_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_event_weights_muon_endcap_hist=TH1F("fake_photon_event_weights_muon_endcap_hist","fake_photon_event_weights_muon_endcap_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_event_weights_electron_endcap_hist=TH1F("fake_photon_event_weights_electron_endcap_hist","fake_photon_event_weights_electron_endcap_hist",len(photon_ptbins)-1,photon_ptbins)

for i in range(fake_photon_event_weights_muon_barrel_hist.GetNbinsX()):
    fake_photon_event_weights_muon_barrel_hist.SetBinContent(i+1,fake_photon_event_weights_muon_barrel[i])

for i in range(fake_photon_event_weights_electron_barrel_hist.GetNbinsX()):
    fake_photon_event_weights_electron_barrel_hist.SetBinContent(i+1,fake_photon_event_weights_electron_barrel[i])

for i in range(fake_photon_event_weights_muon_endcap_hist.GetNbinsX()):
    fake_photon_event_weights_muon_endcap_hist.SetBinContent(i+1,fake_photon_event_weights_muon_endcap[i])

for i in range(fake_photon_event_weights_electron_endcap_hist.GetNbinsX()):
    fake_photon_event_weights_electron_endcap_hist.SetBinContent(i+1,fake_photon_event_weights_electron_endcap[i])

fake_photon_event_weights_muon_barrel_hist.Print("all")
fake_photon_event_weights_muon_endcap_hist.Print("all")
fake_photon_event_weights_electron_barrel_hist.Print("all")
fake_photon_event_weights_electron_endcap_hist.Print("all")

if lepton_name == "muon":
    lepton_abs_pdg_id = 13
else:
    lepton_abs_pdg_id = 11

btagging_selection = 0

def photonfakerate(eta,pt,lepton_pdg_id,syst):

    if abs(lepton_pdg_id) == 11:
        if abs(eta) < 1.4442:
            myeta  = min(abs(eta),2.4999)
            mypt   = min(pt,399.999)

            fr = fake_photon_event_weights_electron_barrel_hist.GetBinContent(fake_photon_event_weights_electron_barrel_hist.GetXaxis().FindFixBin(mypt))

            return fr

        elif 1.566 < abs(eta) and abs(eta) < 2.5:
            myeta  = min(abs(eta),2.4999)
            mypt   = min(pt,399.999)

            fr = fake_photon_event_weights_electron_endcap_hist.GetBinContent(fake_photon_event_weights_electron_endcap_hist.GetXaxis().FindFixBin(mypt))

            return fr

        else:

            assert(0)
    elif abs(lepton_pdg_id) == 13:
        if abs(eta) < 1.4442:
            myeta  = min(abs(eta),2.4999)
            mypt   = min(pt,399.999)

            fr = fake_photon_event_weights_muon_barrel_hist.GetBinContent(fake_photon_event_weights_muon_barrel_hist.GetXaxis().FindFixBin(mypt))

            return fr

        elif 1.566 < abs(eta) and abs(eta) < 2.5:
            myeta  = min(abs(eta),2.4999)
            mypt   = min(pt,399.999)

            fr = fake_photon_event_weights_muon_endcap_hist.GetBinContent(fake_photon_event_weights_muon_endcap_hist.GetXaxis().FindFixBin(mypt))

            return fr

        else:

            assert(0)

    else:

        assert(0)

def muonfakerate(eta,pt,syst):

    myeta  = min(abs(eta),2.4999)
    #mypt   = min(pt,69.999)
    mypt   = min(pt,44.999)

    etabin = muon_fr_hist.GetXaxis().FindFixBin(myeta)
    ptbin = muon_fr_hist.GetYaxis().FindFixBin(mypt)

    prob = muon_fr_hist.GetBinContent(etabin,ptbin)

    if syst == "up":
        prob+=muon_fr_hist.GetBinError(etabin,ptbin)
    elif syst == "down":
        prob-=muon_fr_hist.GetBinError(etabin,ptbin)
    else:
        if syst != "nominal":
            sys.exit(0)

    return prob/(1-prob)

def electronfakerate(eta,pt,syst):
    
    myeta  = min(abs(eta),2.4999)
    mypt   = min(pt,44.999)

    etabin = electron_fr_hist.GetXaxis().FindFixBin(myeta)
    ptbin = electron_fr_hist.GetYaxis().FindFixBin(mypt)

    prob = electron_fr_hist.GetBinContent(etabin,ptbin)

    if syst == "up":
        prob+=electron_fr_hist.GetBinError(etabin,ptbin)
    elif syst == "down":
        prob-=electron_fr_hist.GetBinError(etabin,ptbin)
    else:
        if syst != "nominal":
            sys.exit(0)

    return prob/(1-prob)


def set_axis_fonts(thstack, coordinate, title):

    if coordinate == "x":
        axis = thstack.GetXaxis();
    elif coordinate == "y":
        axis = thstack.GetYaxis();
    else:
        assert(0)
    
    axis.SetLabelFont  (   42)
    axis.SetLabelOffset(0.015)
    axis.SetLabelSize  (0.050)
    axis.SetNdivisions (  505)
    axis.SetTitleFont  (   42)
    axis.SetTitleOffset(  1.5)
    axis.SetTitleSize  (0.050)
    if (coordinate == "y"):
        axis.SetTitleOffset(1.6)
    axis.SetTitle(title)    

def draw_legend(x1,y1,hist,label,options):

    legend = TLegend(x1+xoffsetstart,y1+yoffsetstart,x1+xoffsetstart + xoffset,y1+yoffsetstart + yoffset)

    legend.SetBorderSize(     0)
    legend.SetFillColor (     0)
    legend.SetTextAlign (    12)
    legend.SetTextFont  (    42)
    legend.SetTextSize  ( 0.040)

    legend.AddEntry(hist,label,options)

    legend.Draw("same")

    #otherwise the legend goes out of scope and is deleted once the function finishes
    hist.label = legend

if lepton_name == "muon":
    data_file = TFile.Open("/afs/cern.ch/work/a/amlevin/data/wgamma_single_muon.root")
elif lepton_name == "electron":
    data_file = TFile.Open("/afs/cern.ch/work/a/amlevin/data/wgamma_single_electron.root")
else:
    assert(0)

wg_qcd_file = TFile.Open("/afs/cern.ch/work/a/amlevin/data/wgamma_qcd_wg.root")
zg_qcd_file = TFile.Open("/afs/cern.ch/work/a/amlevin/data/wgamma_qcd_zg.root")
ttg_file = TFile.Open("/afs/cern.ch/work/a/amlevin/data/wgamma_ttg.root")
ttsemi_file = TFile.Open("/afs/cern.ch/work/a/amlevin/data/wgamma_ttsemi.root")
tt2l2nu_file = TFile.Open("/afs/cern.ch/work/a/amlevin/data/wgamma_tt2l2nu.root")
wg_ewk_file = TFile.Open("/afs/cern.ch/user/a/amlevin/vbs-wgamma/wgammajj_ewk.root")

c1 = TCanvas("c1", "c1",5,50,500,500);

gROOT.cd()

#variable = "mjj"

wg_qcd_tree = wg_qcd_file.Get("Events")
ttg_tree = ttg_file.Get("Events")
ttsemi_tree = ttg_file.Get("Events")
tt2l2nu_tree = ttg_file.Get("Events")
zg_qcd_tree = zg_qcd_file.Get("Events")
wg_ewk_tree = wg_ewk_file.Get("Events")
data_events_tree = data_file.Get("Events")

wg_qcd_n_weighted_events_hist = wg_qcd_file.Get("nWeightedEvents")

wg_qcd_n_weighted_events = wg_qcd_n_weighted_events_hist.GetBinContent(1)

zg_qcd_n_weighted_events_hist = zg_qcd_file.Get("nWeightedEvents")

zg_qcd_n_weighted_events = zg_qcd_n_weighted_events_hist.GetBinContent(1)

ttg_n_weighted_events_hist = ttg_file.Get("nWeightedEvents")

ttg_n_weighted_events = ttg_n_weighted_events_hist.GetBinContent(1)

tt2l2nu_n_weighted_events_hist = tt2l2nu_file.Get("nWeightedEvents")

tt2l2nu_n_weighted_events = tt2l2nu_n_weighted_events_hist.GetBinContent(1)

ttsemi_n_weighted_events_hist = ttsemi_file.Get("nWeightedEvents")

ttsemi_n_weighted_events = ttsemi_n_weighted_events_hist.GetBinContent(1)

data_hist = TH1F("data","",18,200,2000)
double_fake_hist = TH1F("double fake hist","",18,200,2000)
fake_photon_hist = TH1F("fake photon hist","",18,200,2000)
fake_electron_hist = TH1F("fake electron hist","",18,200,2000)
fake_muon_hist = TH1F("fake muon hist","",18,200,2000)
data_hist.Sumw2()
fake_muon_hist.Sumw2()
fake_electron_hist.Sumw2()
fake_photon_hist.Sumw2()
double_fake_hist.Sumw2()

wg_qcd_hist = TH1F("wg_qcd","",18,200,2000)
wg_qcd_hist.Sumw2()

ttg_hist = TH1F("ttg","",18,200,2000)
ttg_hist.Sumw2()

tt2l2nu_hist = TH1F("tt2l2nu","",18,200,2000)
tt2l2nu_hist.Sumw2()

ttsemi_hist = TH1F("ttsemi","",18,200,2000)
ttsemi_hist.Sumw2()

zg_qcd_hist = TH1F("zg_qcd","",18,200,2000)
zg_qcd_hist.Sumw2()

wg_ewk_hist = TH1F("wg_ewk","",18,200,2000)
wg_ewk_hist.Sumw2()

data_events_tree.Draw("mjj >> data","mjj < 400 && abs(lepton_pdg_id) == "+str(lepton_abs_pdg_id)+" && is_lepton_tight == 1 && "+photon_eta_cutstring+" && photon_selection == 2 && photon_pt > 25 && photon_pt < 70 && btagging_selection == "+ str(btagging_selection))

wg_ewk_tree.Draw("mjj >> wg_ewk","lepton_pdg_id == 11 && is_lepton_tight == 1 && photon_pt > 25 && photon_pt < 70","Generator_weight")

def fillHistogramMC(tree,hist,xs,n_weighted_events):
    for i in range(tree.GetEntries()):
        tree.GetEntry(i)

        if photon_eta_cutstring == "abs(photon_eta) < 1.4442":        
            if tree.lepton_pdg_id == lepton_abs_pdg_id and tree.is_lepton_tight == '\x01' and abs(tree.photon_eta) < 1.4442 and tree.photon_selection == 2 and tree.photon_pt > 25 and tree.photon_pt < 70 and tree.btagging_selection == btagging_selection and tree.is_lepton_real == '\x01' and tree.is_photon_real == '\x01':
                if tree.Generator_weight > 0:
                    #hist.Fill(tree.mjj,eff_scale_factor.photon_efficiency_scale_factor(tree.photon_pt,tree.photon_eta)*eff_scale_factor.electron_efficiency_scale_factor(tree.lepton_pt,tree.lepton_eta)*xs*1000*36.15/n_weighted_events)
                    hist.Fill(tree.mjj,xs*1000*36.15/n_weighted_events)
                else:
                    #hist.Fill(tree.mjj,-eff_scale_factor.photon_efficiency_scale_factor(tree.photon_pt,tree.photon_eta)*eff_scale_factor.electron_efficiency_scale_factor(tree.lepton_pt,tree.lepton_eta)*xs*1000*36.15/n_weighted_events)
                    hist.Fill(tree.mjj,-xs*1000*36.15/n_weighted_events)
        elif photon_eta_cutstring == "1.566 < abs(photon_eta) && abs(photon_eta) < 2.5":    
            if tree.lepton_pdg_id == lepton_abs_pdg_id and tree.is_lepton_tight == '\x01' and 1.566 < abs(tree.photon_eta) and abs(tree.photon_eta) < 2.5 and tree.photon_selection == 2 and tree.photon_pt > 25 and tree.photon_pt < 70 and tree.btagging_selection == btagging_selection and tree.is_lepton_real == '\x01' and tree.is_photon_real == '\x01':
                if tree.Generator_weight > 0:
#                    hist.Fill(tree.mjj,eff_scale_factor.photon_efficiency_scale_factor(tree.photon_pt,tree.photon_eta)*eff_scale_factor.electron_efficiency_scale_factor(tree.lepton_pt,tree.lepton_eta)*xs*1000*36.15/n_weighted_events)
                    hist.Fill(tree.mjj,xs*1000*36.15/n_weighted_events)
                else:
#                    hist.Fill(tree.mjj,-eff_scale_factor.photon_efficiency_scale_factor(tree.photon_pt,tree.photon_eta)*eff_scale_factor.electron_efficiency_scale_factor(tree.lepton_pt,tree.lepton_eta)*xs*1000*36.15/n_weighted_events)
                    hist.Fill(tree.mjj,-xs*1000*36.15/n_weighted_events)
        else:
            assert(0)

    hist.Print("all")


for i in range(data_events_tree.GetEntries()):
    data_events_tree.GetEntry(i)

    if photon_eta_cutstring == "abs(photon_eta) < 1.4442":
        if data_events_tree.lepton_pdg_id == lepton_abs_pdg_id and data_events_tree.is_lepton_tight == '\x00' and abs(data_events_tree.photon_eta) < 1.4442 and (data_events_tree.photon_selection == 1 or data_events_tree.photon_selection == 0) and data_events_tree.photon_pt > 25 and data_events_tree.photon_pt < 70 and data_events_tree.btagging_selection == btagging_selection:        
            if lepton_name == "muon":
                double_fake_hist.Fill(data_events_tree.mjj,muonfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")*photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
                fake_muon_hist.Fill(data_events_tree.mjj,-muonfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")*photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
            elif lepton_name == "electron":
                double_fake_hist.Fill(data_events_tree.mjj,electronfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")*photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
                fake_electron_hist.Fill(data_events_tree.mjj,-electronfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")*photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
            else:
                assert(0)
    elif photon_eta_cutstring == "1.566 < abs(photon_eta) && abs(photon_eta) < 2.5":
        if data_events_tree.lepton_pdg_id == lepton_abs_pdg_id and data_events_tree.is_lepton_tight == '\x00' and 1.566 < abs(data_events_tree.photon_eta) and abs(data_events_tree.photon_eta) < 2.5 and (data_events_tree.photon_selection == 1 or data_events_tree.photon_selection == 0) and data_events_tree.photon_pt > 25 and data_events_tree.photon_pt < 70 and data_events_tree.btagging_selection == btagging_selection:        
            if lepton_name == "muon":
                double_fake_hist.Fill(data_events_tree.mjj,muonfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")*photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
                fake_muon_hist.Fill(data_events_tree.mjj,-muonfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")*photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
            elif lepton_name == "electron":
                double_fake_hist.Fill(data_events_tree.mjj,electronfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")*photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
                fake_electron_hist.Fill(data_events_tree.mjj,-electronfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")*photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
            else:
                assert(0)
    else:
        assert(0)
    
    if photon_eta_cutstring == "abs(photon_eta) < 1.4442":        
        if data_events_tree.lepton_pdg_id == lepton_abs_pdg_id and data_events_tree.is_lepton_tight == '\x00' and abs(data_events_tree.photon_eta) < 1.4442 and data_events_tree.photon_selection == 2 and data_events_tree.photon_pt > 25 and data_events_tree.photon_pt < 70  and data_events_tree.btagging_selection == btagging_selection:
            if lepton_name == "muon":
                fake_muon_hist.Fill(data_events_tree.mjj,muonfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal"))
            elif lepton_name == "electron":
                fake_electron_hist.Fill(data_events_tree.mjj,electronfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal"))
            else:
                assert(0)
    elif photon_eta_cutstring == "1.566 < abs(photon_eta) && abs(photon_eta) < 2.5":            
        if data_events_tree.lepton_pdg_id == lepton_abs_pdg_id and data_events_tree.is_lepton_tight == '\x00' and 1.566 < abs(data_events_tree.photon_eta) and abs(data_events_tree.photon_eta) < 2.5 and data_events_tree.photon_selection == 2 and data_events_tree.photon_pt > 25 and data_events_tree.photon_pt < 70 and data_events_tree.btagging_selection == btagging_selection:
            if lepton_name == "muon":
                fake_muon_hist.Fill(data_events_tree.mjj,muonfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal"))
            elif lepton_name == "electron":
                fake_electron_hist.Fill(data_events_tree.mjj,electronfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal"))
            else:
                assert(0)
    else:
        assert(0)

    if photon_eta_cutstring == "abs(photon_eta) < 1.4442":        
        if data_events_tree.lepton_pdg_id == lepton_abs_pdg_id and data_events_tree.is_lepton_tight == '\x01' and abs(data_events_tree.photon_eta) < 1.4442 and (data_events_tree.photon_selection == 1 or data_events_tree.photon_selection == 0) and data_events_tree.photon_pt > 25 and data_events_tree.photon_pt < 70 and data_events_tree.btagging_selection == btagging_selection:
            fake_photon_hist.Fill(data_events_tree.mjj,photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
    elif photon_eta_cutstring == "1.566 < abs(photon_eta) && abs(photon_eta) < 2.5":    
        if data_events_tree.lepton_pdg_id == lepton_abs_pdg_id and data_events_tree.is_lepton_tight == '\x01' and 1.566 < abs(data_events_tree.photon_eta) and abs(data_events_tree.photon_eta) < 2.5 and (data_events_tree.photon_selection == 1 or data_events_tree.photon_selection == 0) and data_events_tree.photon_pt > 25 and data_events_tree.photon_pt < 70 and data_events_tree.btagging_selection == btagging_selection:
            fake_photon_hist.Fill(data_events_tree.mjj,photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
    else:
        assert(0)

for i in range(wg_qcd_tree.GetEntries()):
    wg_qcd_tree.GetEntry(i)


    if photon_eta_cutstring == "abs(photon_eta) < 1.4442":        
        if wg_qcd_tree.lepton_pdg_id == lepton_abs_pdg_id and wg_qcd_tree.is_lepton_tight == '\x01' and abs(wg_qcd_tree.photon_eta) < 1.4442 and (wg_qcd_tree.photon_selection == 1 or wg_qcd_tree.photon_selection == 0) and wg_qcd_tree.photon_pt > 25 and wg_qcd_tree.photon_pt < 70 and wg_qcd_tree.btagging_selection == btagging_selection:
            fake_photon_hist.Fill(wg_qcd_tree.mjj,-photonfakerate(wg_qcd_tree.photon_eta, wg_qcd_tree.photon_pt,wg_qcd_tree.lepton_pdg_id, "nominal"))  
    elif photon_eta_cutstring == "1.566 < abs(photon_eta) && abs(photon_eta) < 2.5":    
        if wg_qcd_tree.lepton_pdg_id == lepton_abs_pdg_id and wg_qcd_tree.is_lepton_tight == '\x01' and 1.566 < abs(wg_qcd_tree.photon_eta) and abs(wg_qcd_tree.photon_eta) < 2.5 and (wg_qcd_tree.photon_selection == 1 or wg_qcd_tree.photon_selection == 0) and wg_qcd_tree.photon_pt > 25 and wg_qcd_tree.photon_pt < 70 and wg_qcd_tree.btagging_selection == btagging_selection:
            fake_photon_hist.Fill(wg_qcd_tree.mjj,-photonfakerate(wg_qcd_tree.photon_eta, wg_qcd_tree.photon_pt,wg_qcd_tree.lepton_pdg_id, "nominal"))  
    else:
        assert(0)

    if photon_eta_cutstring == "abs(photon_eta) < 1.4442":
        if wg_qcd_tree.lepton_pdg_id == lepton_abs_pdg_id and wg_qcd_tree.is_lepton_tight == '\x00' and abs(wg_qcd_tree.photon_eta) < 1.4442 and wg_qcd_tree.photon_selection == 2 and wg_qcd_tree.photon_pt > 25 and wg_qcd_tree.photon_pt < 70 and wg_qcd_tree.btagging_selection == btagging_selection:
            if lepton_name == "muon":
                if wg_qcd_tree.Generator_weight > 0:
                    fake_muon_hist.Fill(wg_qcd_tree.mjj,-muonfakerate(wg_qcd_tree.lepton_eta, wg_qcd_tree.lepton_pt,"nominal")*178.6 * 1000 * 36.15 / wg_qcd_n_weighted_events)
                else:    
                    fake_muon_hist.Fill(wg_qcd_tree.mjj,muonfakerate(wg_qcd_tree.lepton_eta, wg_qcd_tree.lepton_pt,"nominal")*178.6 * 1000 * 36.15 / wg_qcd_n_weighted_events)
            elif lepton_name == "electron":
                if wg_qcd_tree.Generator_weight > 0:
                    fake_electron_hist.Fill(wg_qcd_tree.mjj,-electronfakerate(wg_qcd_tree.lepton_eta, wg_qcd_tree.lepton_pt,"nominal")*178.6 * 1000 * 36.15 / wg_qcd_n_weighted_events)
                else:
                    fake_electron_hist.Fill(wg_qcd_tree.mjj,electronfakerate(wg_qcd_tree.lepton_eta, wg_qcd_tree.lepton_pt,"nominal")*178.6 * 1000 * 36.15 / wg_qcd_n_weighted_events)
                pass
            else:
                assert(0)
    elif photon_eta_cutstring == "1.566 < abs(photon_eta) && abs(photon_eta) < 2.5":            
        if wg_qcd_tree.lepton_pdg_id == lepton_abs_pdg_id and wg_qcd_tree.is_lepton_tight == '\x00' and 1.566 < abs(wg_qcd_tree.photon_eta) and abs(wg_qcd_tree.photon_eta) < 2.5 and wg_qcd_tree.photon_selection == 2 and wg_qcd_tree.photon_pt > 25 and wg_qcd_tree.photon_pt < 70 and wg_qcd_tree.btagging_selection == btagging_selection:
            if lepton_name == "muon":
                if wg_qcd_tree.Generator_weight > 0:
                    fake_muon_hist.Fill(wg_qcd_tree.mjj,-muonfakerate(wg_qcd_tree.lepton_eta, wg_qcd_tree.lepton_pt,"nominal")*178.6 * 1000 * 36.15 / wg_qcd_n_weighted_events)
                else:
                    fake_muon_hist.Fill(wg_qcd_tree.mjj,muonfakerate(wg_qcd_tree.lepton_eta, wg_qcd_tree.lepton_pt,"nominal")*178.6 * 1000 * 36.15 / wg_qcd_n_weighted_events)
            elif lepton_name == "electron":
                if wg_qcd_tree.Generator_weight > 0:
                    fake_electron_hist.Fill(wg_qcd_tree.mjj,-electronfakerate(wg_qcd_tree.lepton_eta, wg_qcd_tree.lepton_pt,"nominal")*178.6 * 1000 * 36.15 / wg_qcd_n_weighted_events)
                else:    
                    fake_electron_hist.Fill(wg_qcd_tree.mjj,electronfakerate(wg_qcd_tree.lepton_eta, wg_qcd_tree.lepton_pt,"nominal")*178.6 * 1000 * 36.15 / wg_qcd_n_weighted_events)
            else:
                assert(0)
    else:
        assert(0)



fillHistogramMC(wg_qcd_tree,wg_qcd,178.6,wg_qcd_n_weighted_events)    

#fillHistogramMC(zg_qcd_tree,zg_qcd,,zg_qcd_n_weighted_events)    

fillHistogramMC(tt2l2nu_tree,tt2l2nu_hist,76.7,tt2l2nu_n_weighted_events)

fillHistogramMC(ttsemi_tree,ttsemi_hist,320.1,ttsemi_n_weighted_events)

fillHistogramMC(ttg_tree,ttg_hist,3.795,ttg_n_weighted_events)

#wg_qcd_tree.Draw("mjj >> wg_qcd","lepton_pdg_id == "+str(lepton_abs_pdg_id)+" && is_lepton_tight == 1 && "+photon_eta_cutstring+" && abs(photon_eta) < 2.5 && photon_selection == 2 && photon_pt > 25 && photon_pt < 70 && btagging_selection == "+str(btagging_selection),"Generator_weight > 0 ? 1 : -1")

#ttg_tree.Draw("mjj >> ttg","lepton_pdg_id == "+str(lepton_abs_pdg_id)+" && is_lepton_tight == 1 && "+photon_eta_cutstring+" && abs(photon_eta) < 2.5 && photon_selection == 2 && photon_pt > 25 && photon_pt < 70 && btagging_selection == "+str(btagging_selection) + " && is_lepton_real == 1 && is_photon_real == 1" ,"Generator_weight > 0 ? 1 : -1")

#ttsemi_tree.Draw("mjj >> ttsemi","lepton_pdg_id == "+str(lepton_abs_pdg_id)+" && is_lepton_tight == 1 && "+photon_eta_cutstring+" && abs(photon_eta) < 2.5 && photon_selection == 2 && photon_pt > 25 && photon_pt < 70 && btagging_selection == "+str(btagging_selection) + " && is_lepton_real == 1 && is_photon_real == 1" ,"Generator_weight > 0 ? 1 : -1")

#tt2l2nu_tree.Draw("mjj >> tt2l2nu","lepton_pdg_id == "+str(lepton_abs_pdg_id)+" && is_lepton_tight == 1 && "+photon_eta_cutstring+" && abs(photon_eta) < 2.5 && photon_selection == 2 && photon_pt > 25 && photon_pt < 70 && btagging_selection == "+str(btagging_selection) + " && is_lepton_real == 1 && is_photon_real == 1" ,"Generator_weight > 0 ? 1 : -1")

#single_muon_hist = gDirectory.Get("single_muon")



#wg_qcd_hist.Scale(178.6 * 1000 * 36.15 / wg_qcd_n_weighted_events)

#tt2l2nu_hist.Scale(76.7 * 1000 * 36.15 / tt2l2nu_n_weighted_events)

#ttsemi_hist.Scale(320.1 * 1000 * 36.15 / ttsemi_n_weighted_events)

#ttg_hist.Scale(3.795 * 1000 * 36.15 / ttg_n_weighted_events)

#zg_qcd_hist.Scale(178.6 * 1000 * 36.15 / zg_qcd_n_weighted_events)

wg_ewk_hist.Scale(0.7605 * 1000 * 36.15 / 699444)

#events_tree.Scan("mjj")

data_hist.SetMarkerStyle(kFullCircle)
data_hist.SetLineWidth(3)

#data_hist.Draw()

fake_photon_hist.SetFillColor(kMagenta)
fake_electron_hist.SetFillColor(kBlue)
fake_muon_hist.SetFillColor(kBlue)
double_fake_hist.SetFillColor(kOrange)
wg_qcd_hist.SetFillColor(kGreen+2)
ttg_hist.SetFillColor(kAzure-1)
ttsemi_hist.SetFillColor(kYellow)
tt2l2nu_hist.SetFillColor(kRed)

fake_photon_hist.SetLineColor(kMagenta)
fake_electron_hist.SetLineColor(kBlue)
fake_muon_hist.SetLineColor(kBlue)
double_fake_hist.SetLineColor(kOrange)
wg_qcd_hist.SetLineColor(kGreen+2)
ttg_hist.SetLineColor(kAzure-1)
ttsemi_hist.SetLineColor(kYellow)
tt2l2nu_hist.SetLineColor(kRed)

fake_photon_hist.SetFillStyle(1001)
fake_electron_hist.SetFillStyle(1001)
fake_muon_hist.SetFillStyle(1001)
double_fake_hist.SetFillStyle(1001)
wg_qcd_hist.SetFillStyle(1001)
ttg_hist.SetFillStyle(1001)
ttsemi_hist.SetFillStyle(1001)
tt2l2nu_hist.SetFillStyle(1001)


#wg_qcd_hist.Draw("hist")

#fake_photon_hist.Draw("same")
#fake_electron_hist.Draw("same")

#wg_qcd_hist.Draw("hist same")

#wg_ewk_hist.Draw("hist same")

#wg_qcd.Draw("same")

s=str(options.lumi)+" fb^{-1} (13 TeV)"
lumilabel = TLatex (0.95, 0.93, s)
lumilabel.SetNDC ()
lumilabel.SetTextAlign (30)
lumilabel.SetTextFont (42)
lumilabel.SetTextSize (0.040)

#
hsum = data_hist.Clone()
hsum.Scale(0.0)

hsum.Add(wg_qcd)
hsum.Add(ttg_hist)
hsum.Add(ttsemi_hist)
hsum.Add(tt2l2nu_hist)
if lepton_name == "muon":
    hsum.Add(fake_muon_hist)
elif lepton_name == "electron":
    hsum.Add(fake_electron_hist)
else:
    assert(0)
hsum.Add(fake_photon_hist)
hsum.Add(double_fake_hist)

hstack = THStack()
hstack.Add(wg_qcd)
hstack.Add(ttg_hist)
hstack.Add(ttsemi_hist)
hstack.Add(tt2l2nu_hist)
if lepton_name == "muon":
    hstack.Add(fake_muon_hist)
elif lepton_name == "electron":
    hstack.Add(fake_electron_hist)
else:
    assert(0)
hstack.Add(fake_photon_hist)
hstack.Add(double_fake_hist)

data_hist.Draw("")

hstack.Draw("hist same")

#wg_qcd.Draw("hist same")
#fake_electron_hist.Draw("hist same")
#fake_photon_hist.Draw("hist same")

#wg_ewk_hist.Print("all")

#cmslabel = TLatex (0.18, 0.93, "#bf{CMS} (Unpublished)")
cmslabel = TLatex (0.18, 0.93, "")
cmslabel.SetNDC ()
cmslabel.SetTextAlign (10)
cmslabel.SetTextFont (42)
cmslabel.SetTextSize (0.040)
cmslabel.Draw ("same") 

lumilabel.Draw("same")

#wpwpjjewk.Draw("same")

j=0
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,data_hist,"data","lp")
j=j+1
if lepton_name == "muon":
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,fake_muon_hist,"fake muon","f")
elif lepton_name == "electron":
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,fake_electron_hist,"fake electron","f")
else:
    assert(0)
j=j+1
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,fake_photon_hist,"fake photon","f")
j=j+1
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,double_fake_hist,"double fake","f")
j=j+1
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wg_qcd_hist,"wg+jets","f")
j=j+1
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,ttg_hist,"ttg","f")
j=j+1
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,tt2l2nu_hist,"tt2l2nu","f")
j=j+1
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,ttsemi_hist,"ttsemi","f")
#j=j+1
#draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wg_ewk_hist,"wgjj ewk","f")
#j=j+1
#draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wzjjewk,"WZ+jets","f")
#j=j+1
#draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wzjjqcd,"WZ+jets","f")
#j=j+1
#draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wpwpjjqcd,"WWJJ QCD","f")


#j=j+1
#draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wgjets,"WGJJ","f")
#j=j+1
#draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wpwpjjewk,"WWJJ","f")
#j=j+1
#draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,data,"data","lp")

#data.Draw("same")

#set_axis_fonts(hstack,"x","m_{ll} (GeV)")
#set_axis_fonts(hstack,"x","|\Delta \eta_{jj}|")
set_axis_fonts(data_hist,"x",options.xaxislabel)
set_axis_fonts(hstack,"x",options.xaxislabel)
#set_axis_fonts(hstack,"x","pt_{l}^{max} (GeV)")
#set_axis_fonts(data_hist,"y","Events / bin")
#set_axis_fonts(hstack,"y","Events / bin")

gstat = TGraphAsymmErrors(hsum);

for i in range(0,gstat.GetN()):
    gstat.SetPointEYlow (i, hsum.GetBinError(i+1));
    gstat.SetPointEYhigh(i, hsum.GetBinError(i+1));

gstat.SetFillColor(12);
gstat.SetFillStyle(3345);
gstat.SetMarkerSize(0);
gstat.SetLineWidth(0);
gstat.SetLineColor(kWhite);
gstat.Draw("E2same");

data_hist.Draw("same")

c1.Update()
c1.ForceUpdate()
c1.Modified()

c1.SaveAs(options.outputfile)
