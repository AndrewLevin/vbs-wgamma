data_driven = True

import json

import sys
import style

import optparse

from math import hypot, pi, sqrt

def deltaPhi(phi1,phi2):
    ## Catch if being called with two objects                                                                                                                        
    if type(phi1) != float and type(phi1) != int:
        phi1 = phi1.phi
    if type(phi2) != float and type(phi2) != int:
        phi2 = phi2.phi
    ## Otherwise                                                                                                                                                     
    dphi = (phi1-phi2)
    while dphi >  pi: dphi -= 2*pi
    while dphi < -pi: dphi += 2*pi
    return dphi

def deltaR(eta1,phi1,eta2=None,phi2=None):
    ## catch if called with objects                                                                                                                                  
    if eta2 == None:
        return deltaR(eta1.eta,eta1.phi,phi1.eta,phi1.phi)
    ## otherwise                                                                                                                                                     
    return hypot(eta1-eta2, deltaPhi(phi1,phi2))


parser = optparse.OptionParser()

parser.add_option('--lep',dest='lep',default='both')
parser.add_option('--phoeta',dest='phoeta',default='both')

parser.add_option('--lumi',dest='lumi')
parser.add_option('--variable',dest='variable')
parser.add_option('--xaxislabel',dest='xaxislabel',default='m_{jj} (GeV)')

parser.add_option('-i',dest='inputfile')
parser.add_option('-o',dest='outputdir',default="/eos/user/a/amlevin/www/tmp/")

(options,args) = parser.parse_args()

if options.lep == "muon":
    lepton_name = "muon"
elif options.lep == "electron":
    lepton_name = "electron"
else:
    assert(0)

if lepton_name == "muon":
    lepton_abs_pdg_id = 13
else:
    lepton_abs_pdg_id = 11

import ROOT

f_pu_weights = ROOT.TFile("/afs/cern.ch/user/a/amlevin/PileupWeights2016.root")

pu_weight_hist = f_pu_weights.Get("ratio")

samples = [{ 'filename' : '/afs/cern.ch/work/a/amlevin/data/wg/gjets_ht40100.root', 'xs' : 20660.0},{ 'filename' : '/afs/cern.ch/work/a/amlevin/data/wg/gjets_ht100200.root'  , 'xs' : 9249.0},{ 'filename' : '/afs/cern.ch/work/a/amlevin/data/wg/gjets_ht200400.root' , 'xs' : 2321.0},{ 'filename' : '/afs/cern.ch/work/a/amlevin/data/wg/gjets_ht400600.root', 'xs' : 275.2},{ 'filename' : '/afs/cern.ch/work/a/amlevin/data/wg/gjets_ht600.root', 'xs' : 93.19}]

variables = ["met","lepton_pt","lepton_eta","photon_pt","photon_eta","mlg","lepton_phi","photon_phi","njets","mt","npvs","drlg"]

histogram_templates = { "met" : ROOT.TH1F("met", "", 15 , 0., 300 ), "lepton_pt" : ROOT.TH1F('lepton_pt', '', 8, 20., 180 ), "lepton_eta" : ROOT.TH1F('lepton_eta', '', 10, -2.5, 2.5 ), "photon_pt" : ROOT.TH1F('photon_pt', '', 8, 20., 180 ), "photon_eta" : ROOT.TH1F('photon_eta', '', 10, -2.5, 2.5 ), "mlg" : ROOT.TH1F("mlg","",20,0,200) , "lepton_phi" : ROOT.TH1F("lepton_phi","",14,-3.5,3.5), "photon_phi" : ROOT.TH1F("photon_phi","",14,-3.5,3.5), "njets" : ROOT.TH1F("njets","",7,-0.5,6.5), "mt" : ROOT.TH1F("mt","",20,0,200), "npvs" : ROOT.TH1F("npvs","",51,-0.5,50.5), "drlg" : ROOT.TH1F("drlg","",60,0,6)} 

def getVariable(varname, tree):
    if varname == "mlg":
        return tree.mlg
    elif varname == "drlg":
        return deltaR(tree.lepton_eta,tree.lepton_phi,tree.photon_eta,tree.photon_phi)
    elif varname == "mt":
        return tree.mt
    elif varname == "njets":
        return float(tree.njets)
    elif varname == "npvs":
        return float(tree.npvs)
    elif varname == "met":
        return tree.met
    elif varname == "lepton_pt":
        return tree.lepton_pt
    elif varname == "lepton_eta":
        return tree.lepton_eta
    elif varname == "lepton_phi":
        return tree.lepton_phi
    elif varname == "photon_pt":
        return tree.photon_pt
    elif varname == "photon_eta":
        return tree.photon_eta
    elif varname == "photon_phi":
        return tree.photon_phi
    else:
        assert(0)

def getXaxisLabel(varname):
    if varname == "njets":
        return "number of jets"
    elif varname == "drlg":
        return "#Delta R(l,g)"
    elif varname == "npvs":
        return "number of PVs"
    elif varname == "mt":
        return "m_{t} (GeV)"
    elif varname == "mlg":
        return "m_{lg} (GeV)"
    elif varname == "met":
        return "MET (GeV)"
    elif varname == "lepton_pt":
        return "lepton p_{T} (GeV)"
    elif varname == "lepton_eta":
        return "lepton #eta"
    elif varname == "lepton_phi":
        return "lepton #phi"
    elif varname == "photon_pt":
        return "photon p_{T} (GeV)"
    elif varname == "photon_eta":
        return "photon #eta"    
    elif varname == "photon_phi":
        return "photon #phi"

    else:
        assert(0)

def pass_selection(tree, barrel_or_endcap_or_both = "both", fake_lepton = False , fake_photon = False):

    if barrel_or_endcap_or_both == "both":
        pass_photon_eta = True    
    elif barrel_or_endcap == "barrel":        
        if abs(tree.photon_eta) < 1.4442:
            pass_photon_eta = True
        else:
            pass_photon_eta = False
    elif barrel_or_endcap_or_both == "endcap":        
        if 1.566 < abs(tree.photon_eta) and abs(tree.photon_eta) < 2.5:
            pass_photon_eta = True
        else:
            pass_photon_eta = False
    else:
        assert(0)

    if tree.lepton_pdg_id == lepton_abs_pdg_id:
        pass_lepton_flavor = True
    else:
        pass_lepton_flavor = False
        
    if lepton_abs_pdg_id == 11:    
#        if not (tree.mlg > 60.0 and tree.mlg < 120.0):
        if True:
            pass_mlg = True
        else:
            pass_mlg = False
    else:        
#       if not (tree.mlg > 60.0 and tree.mlg < 100.0):
#        if tree.mlg > 80.0 and tree.mlg < 90.0:
        if True:
            pass_mlg = True
        else:
            pass_mlg = False

#    if tree.met > 35:
#    if tree.met > 70:
    if tree.met > 0:
        pass_met = True
    else:
        pass_met = False

#    if tree.mt > 30:
    if tree.mt > 0:
        pass_mt = True
    else:
        pass_mt = False

    if fake_photon:    
        if tree.photon_selection == 0 or tree.photon_selection == 1:
            pass_photon_selection = True
        else:
            pass_photon_selection = False
    else:    
        if tree.photon_selection == 2:
            pass_photon_selection = True
        else:
            pass_photon_selection = False

    if fake_lepton:    
        if tree.is_lepton_tight == '\x00':
            pass_lepton_selection = True
        else:
            pass_lepton_selection = False
    else:
        if tree.is_lepton_tight == '\x01':
            pass_lepton_selection = True
        else:
            pass_lepton_selection = False
            
    if tree.photon_pt > 25 and tree.photon_pt < 700:
#    if tree.photon_pt > 25 and tree.photon_pt < 135:
        pass_photon_pt =True
    else:
        pass_photon_pt = False

    if pass_photon_pt and pass_lepton_selection and pass_photon_selection and pass_mlg and pass_photon_eta and pass_lepton_flavor and pass_met and pass_mt:
        return True
    else:
        return False

#def fillHistograms(tree,hists):

xoffsetstart = 0.0;
yoffsetstart = 0.0;
xoffset = 0.20;
yoffset = 0.05;

#xpositions = [0.60,0.60,0.60,0.60,0.60,0.60,0.40,0.40,0.40]
xpositions = [0.68,0.68,0.68,0.68,0.445,0.445,0.445,0.445,0.21,0.21,0.21,0.21]
#ypositions = [0,1,2,3,4,5,0,1,2]
ypositions = [0,1,2,3,0,1,2,3,0,1,2,3]

style.GoodStyle().cd()

muon_fr_file = ROOT.TFile("/afs/cern.ch/user/a/amlevin/wg/muon_frs.root")
#electron_fr_file = ROOT.TFile("/afs/cern.ch/user/a/amlevin/wg/electron_frs.root")
electron_fr_file = ROOT.TFile("/afs/cern.ch/user/a/amlevin/wg/electron_closure_test_frs.root")

muon_fr_hist=muon_fr_file.Get("muon_frs")
electron_fr_hist=electron_fr_file.Get("electron_frs")

from array import array

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

def leptonfakerate(lepton_abs_pdg_id,eta,pt,syst):
    if lepton_abs_pdg_id == 11:
        return electronfakerate(eta,pt,syst)
    elif lepton_abs_pdg_id == 13:
        return muonfakerate(eta,pt,syst)
    else:
        assert(0)

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

    legend = ROOT.TLegend(x1+xoffsetstart,y1+yoffsetstart,x1+xoffsetstart + xoffset,y1+yoffsetstart + yoffset)

    legend.SetBorderSize(     0)
    legend.SetFillColor (     0)
    legend.SetTextAlign (    12)
    legend.SetTextFont  (    42)
    legend.SetTextSize  ( 0.040)

    legend.AddEntry(hist,label,options)

    legend.Draw("same")

    #otherwise the legend goes out of scope and is deleted once the function finishes
    hist.label = legend

gjets = {}
gjets_data_fr = {}

gjets["hists"] = {}
gjets_data_fr["hists"] = {}

for variable in variables:
    gjets["hists"][variable] = histogram_templates[variable].Clone("gjets " + variable)
    gjets["hists"][variable].Sumw2()

    gjets_data_fr["hists"][variable] = histogram_templates[variable].Clone("gjets data FR " + variable)
    gjets_data_fr["hists"][variable].Sumw2()
    
for sample in samples:
    sample["file"] = ROOT.TFile.Open(sample["filename"])
    sample["tree"] = sample["file"].Get("Events")
    sample["nweightedevents"] = sample["file"].Get("nWeightedEvents").GetBinContent(1)

c1 = ROOT.TCanvas("c1", "c1",5,50,500,500)

ROOT.gROOT.cd()

for sample in samples:
    for i in range(sample["tree"].GetEntries()):
        sample["tree"].GetEntry(i)

        if pass_selection(sample["tree"],options.phoeta):
            for variable in variables:
                gjets["hists"][variable].Fill(getVariable(variable,sample["tree"]))        

        if pass_selection(sample["tree"],options.phoeta,True,False):

            weight = leptonfakerate(sample["tree"].lepton_pdg_id,sample["tree"].lepton_eta,sample["tree"].lepton_pt,"nominal")

            for variable in variables:
                gjets_data_fr["hists"][variable].Fill(getVariable(variable,sample["tree"]),weight)

#gjets["hists"]["mlg"].Print("all")
#gjets_data_fr["hists"]["mlg"].Print("all")

nbins = gjets["hists"]["lepton_pt"].GetXaxis().GetNbins()
integral_gjets_error = ROOT.Double()
integral_gjets_data_fr_error = ROOT.Double()
integral_gjets = gjets["hists"]["lepton_pt"].IntegralAndError(1,nbins,integral_gjets_error)
integral_gjets_data_fr =  gjets_data_fr["hists"]["lepton_pt"].IntegralAndError(1,nbins,integral_gjets_data_fr_error)

print str(integral_gjets) + " +/- " +str(integral_gjets_error)
print str(integral_gjets_data_fr) + " +/- " +str(integral_gjets_data_fr_error)

c1 = ROOT.TCanvas("c1", "c1",5,50,500,500);

gjets["hists"]["lepton_pt"].SetLineColor(ROOT.kRed)
gjets_data_fr["hists"]["lepton_pt"].SetLineColor(ROOT.kBlue)

gjets["hists"]["lepton_pt"].Draw()
gjets_data_fr["hists"]["lepton_pt"].Draw("same")

c1.SaveAs("/eos/user/a/amlevin/www/tmp/delete_this.png")
