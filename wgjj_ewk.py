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

#fr_file = TFile("/afs/cern.ch/user/a/amlevin/vbs-wgamma/muon_frs.root")
fr_file = TFile("/afs/cern.ch/user/a/amlevin/vbs-wgamma/electron_frs.root")

muon_fr_hist=fr_file.Get("muon_frs")
electron_fr_hist=fr_file.Get("electron_frs")

from array import array

photon_ptbins=array('d', [25,30,40,50,70,100,135,400])

photon_frs = [0.15550473705,0.124784207531,0.0966858503868,0.0758489934184,0.0642462907324,0.0564518837214,0.0369812872883]

photon_fr_hist=TH1F("photon_fr_hist","photon_fr_hist",len(photon_ptbins)-1,photon_ptbins)

for i in range(photon_fr_hist.GetNbinsX()):
    photon_fr_hist.SetBinContent(i+1,photon_frs[i])

photon_fr_hist.Print("all")

def photonfakerate(eta,pt,syst):

    myeta  = min(abs(eta),2.3999)
    #mypt   = min(pt,69.999)
    mypt   = min(pt,399.999)

    fr = photon_fr_hist.GetXaxis().FindFixBin(mypt)

    return fr

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

data_file = TFile.Open("/afs/cern.ch/work/a/amlevin/tmp/wgamma_single_electron.root")
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
data_hist.Sumw2()
fake_electron_hist.Sumw2()
fake_photon_hist.Sumw2()

wg_qcd_hist = TH1F("wg_qcd","",18,200,2000)
wg_qcd_hist.Sumw2()

wg_ewk_hist = TH1F("wg_ewk","",18,200,2000)
wg_ewk_hist.Sumw2()

data_events_tree.Draw("mjj >> data","mjj < 400 && lepton_pdg_id == 11 && is_lepton_tight == 1 && abs(photon_eta) < 1.4442 && photon_selection == 2 && photon_pt < 70")

wg_ewk_tree.Draw("mjj >> wg_ewk","lepton_pdg_id == 11 && is_lepton_tight == 1 && photon_pt < 70","Generator_weight")

for i in range(data_events_tree.GetEntries()):
    data_events_tree.GetEntry(i)
    
    #if data_events_tree.lepton_pdg_id == 13 and data_events_tree.is_lepton_tight == '\x00':
    #    fake_hist.Fill(data_events_tree.mjj,muonfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal"))

    if data_events_tree.lepton_pdg_id == 11 and data_events_tree.is_lepton_tight == '\x00' and (data_events_tree.photon_eta) < 1.4442 and data_events_tree.photon_selection == 2 and data_events_tree.photon_pt < 70:
        fake_electron_hist.Fill(data_events_tree.mjj,electronfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal"))

    if data_events_tree.lepton_pdg_id == 11 and data_events_tree.is_lepton_tight == '\x00' and (data_events_tree.photon_eta) < 1.4442 and (data_events_tree.photon_selection == 1 or data_events_tree.photon_selection == 0) and data_events_tree.photon_pt < 70:
        fake_photon_hist.Fill(data_events_tree.mjj,photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,"nominal"))

wg_qcd_tree.Draw("mjj >> wg_qcd","lepton_pdg_id == 11 && is_lepton_tight == 1 && abs(photon_eta) < 1.4442 && photon_selection == 2 && photon_pt < 70","Generator_weight")

#single_muon_hist = gDirectory.Get("single_muon")

wg_qcd_hist.Scale(378.2 * 1000 * 36.15 / 6103817)

wg_ewk_hist.Scale(0.7605 * 1000 * 36.15 / 699444)

#events_tree.Scan("mjj")

data_hist.SetMarkerStyle(kFullCircle)
data_hist.SetLineWidth(3)

#data_hist.Draw()

fake_photon_hist.SetFillColor(kMagenta)
fake_electron_hist.SetFillColor(kBlue)
wg_qcd_hist.SetFillColor(kGreen+2)

fake_photon_hist.SetLineColor(kMagenta)
fake_electron_hist.SetLineColor(kBlue)
wg_qcd_hist.SetLineColor(kGreen+2)

fake_photon_hist.SetFillStyle(1001)
fake_electron_hist.SetFillStyle(1001)
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
hsum.Add(fake_electron_hist)
hsum.Add(fake_photon_hist)

hstack = THStack()
hstack.Add(wg_qcd)
hstack.Add(fake_electron_hist)
hstack.Add(fake_photon_hist)

hstack.Draw("hist")

data_hist.Draw("same")

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
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,fake_electron_hist,"fake electron","f")
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
