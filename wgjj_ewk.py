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

fake_photon_event_weights_muon_barrel = [0.15484967425962273, 0.11526136026220057, 0.091070354122829253, 0.072917453493902371, 0.064764981348695988, 0.04700463570126253, 0.034922659781958389]

fake_photon_event_weights_electron_barrel = [0.15573742576164373, 0.12494329030474935, 0.096571497677979998, 0.075752643786702545, 0.064617228770499982, 0.056704093703044904, 0.036730045038103808]

fake_photon_event_weights_muon_endcap = [0.20839170212916272, 0.17498013594607562, 0.1466030335824296, 0.1125004979329069, 0.091837292330306144, 0.05591928780784014, 0.043609726517627824]

fake_photon_event_weights_electron_endcap = [0.2160443399100257, 0.16915440022208778, 0.13628256324769972, 0.11803145426485719, 0.10802953403391163, 0.057281068272119165, 0.052668295670617482]

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
wg_qcd_file = TFile.Open("/afs/cern.ch/user/a/amlevin/vbs-wgamma/wgamma_qcd.root")
wg_ewk_file = TFile.Open("/afs/cern.ch/user/a/amlevin/vbs-wgamma/wgammajj_ewk.root")

c1 = TCanvas("c1", "c1",5,50,500,500);

gROOT.cd()

#variable = "mjj"

wg_qcd_tree = wg_qcd_file.Get("Events")
wg_ewk_tree = wg_ewk_file.Get("Events")
data_events_tree = data_file.Get("Events")

data_hist = TH1F("data","",18,200,2000)
fake_photon_hist = TH1F("fake photon hist","",18,200,2000)
fake_electron_hist = TH1F("fake electron hist","",18,200,2000)
fake_muon_hist = TH1F("fake muon hist","",18,200,2000)
data_hist.Sumw2()
fake_muon_hist.Sumw2()
fake_electron_hist.Sumw2()
fake_photon_hist.Sumw2()

wg_qcd_hist = TH1F("wg_qcd","",18,200,2000)
wg_qcd_hist.Sumw2()

wg_ewk_hist = TH1F("wg_ewk","",18,200,2000)
wg_ewk_hist.Sumw2()

data_events_tree.Draw("mjj >> data","mjj < 400 && abs(lepton_pdg_id) == "+str(lepton_abs_pdg_id)+" && is_lepton_tight == 1 && "+photon_eta_cutstring+" && photon_selection == 2 && photon_pt > 25 && photon_pt < 70")

wg_ewk_tree.Draw("mjj >> wg_ewk","lepton_pdg_id == 11 && is_lepton_tight == 1 && photon_pt > 25 && photon_pt < 70","Generator_weight")

for i in range(data_events_tree.GetEntries()):
    data_events_tree.GetEntry(i)
    
    if photon_eta_cutstring == "abs(photon_eta) < 1.4442":        
        if data_events_tree.lepton_pdg_id == lepton_abs_pdg_id and data_events_tree.is_lepton_tight == '\x00' and abs(data_events_tree.photon_eta) < 1.4442 and data_events_tree.photon_selection == 2 and data_events_tree.photon_pt > 25 and data_events_tree.photon_pt < 70:
            if lepton_name == "muon":
                fake_muon_hist.Fill(data_events_tree.mjj,muonfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal"))
            elif lepton_name == "electron":
                fake_electron_hist.Fill(data_events_tree.mjj,electronfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal"))
            else:
                assert(0)
    elif photon_eta_cutstring == "1.566 < abs(photon_eta) && abs(photon_eta) < 2.5":            
        if data_events_tree.lepton_pdg_id == lepton_abs_pdg_id and data_events_tree.is_lepton_tight == '\x00' and 1.566 < abs(data_events_tree.photon_eta) and abs(data_events_tree.photon_eta) < 2.5 and data_events_tree.photon_selection == 2 and data_events_tree.photon_pt > 25 and data_events_tree.photon_pt < 70:
            if lepton_name == "muon":
                fake_muon_hist.Fill(data_events_tree.mjj,muonfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal"))
            elif lepton_name == "electron":
                fake_electron_hist.Fill(data_events_tree.mjj,electronfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal"))
            else:
                assert(0)
    else:
        assert(0)

    if photon_eta_cutstring == "abs(photon_eta) < 1.4442":        
        if data_events_tree.lepton_pdg_id == lepton_abs_pdg_id and data_events_tree.is_lepton_tight == '\x01' and abs(data_events_tree.photon_eta) < 1.4442 and (data_events_tree.photon_selection == 1 or data_events_tree.photon_selection == 0) and data_events_tree.photon_pt > 25 and data_events_tree.photon_pt < 70:
            fake_photon_hist.Fill(data_events_tree.mjj,photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
    elif photon_eta_cutstring == "1.566 < abs(photon_eta) && abs(photon_eta) < 2.5":    
        if data_events_tree.lepton_pdg_id == lepton_abs_pdg_id and data_events_tree.is_lepton_tight == '\x01' and 1.566 < abs(data_events_tree.photon_eta) and abs(data_events_tree.photon_eta) < 2.5 and (data_events_tree.photon_selection == 1 or data_events_tree.photon_selection == 0) and data_events_tree.photon_pt > 25 and data_events_tree.photon_pt < 70:
            fake_photon_hist.Fill(data_events_tree.mjj,photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
    else:
        assert(0)

for i in range(wg_qcd_tree.GetEntries()):
    wg_qcd_tree.GetEntry(i)
    if photon_eta_cutstring == "abs(photon_eta) < 1.4442":        
        if wg_qcd_tree.lepton_pdg_id == lepton_abs_pdg_id and wg_qcd_tree.is_lepton_tight == '\x00' and abs(wg_qcd_tree.photon_eta) < 1.4442 and wg_qcd_tree.photon_selection == 2 and wg_qcd_tree.photon_pt > 25 and wg_qcd_tree.photon_pt < 70:
            if lepton_name == "muon":
                fake_muon_hist.Fill(wg_qcd_tree.mjj,-muonfakerate(wg_qcd_tree.lepton_eta, wg_qcd_tree.lepton_pt,"nominal")*wg_qcd_tree.Generator_weight*378.2 * 1000 * 36.15 / 6103817)
            elif lepton_name == "electron":
                fake_electron_hist.Fill(wg_qcd_tree.mjj,-electronfakerate(wg_qcd_tree.lepton_eta, wg_qcd_tree.lepton_pt,"nominal")*wg_qcd_tree.Generator_weight*378.2 * 1000 * 36.15 / 6103817)
                pass
            else:
                assert(0)
    elif photon_eta_cutstring == "1.566 < abs(photon_eta) && abs(photon_eta) < 2.5":            
        if wg_qcd_tree.lepton_pdg_id == lepton_abs_pdg_id and wg_qcd_tree.is_lepton_tight == '\x00' and 1.566 < abs(wg_qcd_tree.photon_eta) and abs(wg_qcd_tree.photon_eta) < 2.5 and wg_qcd_tree.photon_selection == 2 and wg_qcd_tree.photon_pt > 25 and wg_qcd_tree.photon_pt < 70:
            if lepton_name == "muon":
                fake_muon_hist.Fill(wg_qcd_tree.mjj,-muonfakerate(wg_qcd_tree.lepton_eta, wg_qcd_tree.lepton_pt,"nominal")*wg_qcd_tree.Generator_weight*378.2 * 1000 * 36.15 / 6103817)
            elif lepton_name == "electron":
                fake_electron_hist.Fill(wg_qcd_tree.mjj,-electronfakerate(wg_qcd_tree.lepton_eta, wg_qcd_tree.lepton_pt,"nominal")*wg_qcd_tree.Generator_weight*378.2 * 1000 * 36.15 / 6103817)
            else:
                assert(0)
    else:
        assert(0)

    

wg_qcd_tree.Draw("mjj >> wg_qcd","lepton_pdg_id == "+str(lepton_abs_pdg_id)+" && is_lepton_tight == 1 && "+photon_eta_cutstring+" && abs(photon_eta) < 2.5 && photon_selection == 2 && photon_pt > 25 && photon_pt < 70","Generator_weight")

#single_muon_hist = gDirectory.Get("single_muon")

wg_qcd_hist.Scale(378.2 * 1000 * 36.15 / 6103817)

wg_ewk_hist.Scale(0.7605 * 1000 * 36.15 / 699444)

#events_tree.Scan("mjj")

data_hist.SetMarkerStyle(kFullCircle)
data_hist.SetLineWidth(3)

#data_hist.Draw()

fake_photon_hist.SetFillColor(kMagenta)
fake_electron_hist.SetFillColor(kBlue)
fake_muon_hist.SetFillColor(kBlue)
wg_qcd_hist.SetFillColor(kGreen+2)

fake_photon_hist.SetLineColor(kMagenta)
fake_electron_hist.SetLineColor(kBlue)
fake_muon_hist.SetLineColor(kBlue)
wg_qcd_hist.SetLineColor(kGreen+2)

fake_photon_hist.SetFillStyle(1001)
fake_electron_hist.SetFillStyle(1001)
fake_muon_hist.SetFillStyle(1001)
wg_qcd_hist.SetFillStyle(1001)

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
if lepton_name == "muon":
    hsum.Add(fake_muon_hist)
elif lepton_name == "electron":
    hsum.Add(fake_electron_hist)
else:
    assert(0)
hsum.Add(fake_photon_hist)

hstack = THStack()
hstack.Add(wg_qcd)
if lepton_name == "muon":
    hstack.Add(fake_muon_hist)
elif lepton_name == "electron":
    hstack.Add(fake_electron_hist)
else:
    assert(0)
hstack.Add(fake_photon_hist)

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
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wg_qcd_hist,"wg+jets","f")
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

c1.Update()
c1.ForceUpdate()
c1.Modified()

c1.SaveAs(options.outputfile)
