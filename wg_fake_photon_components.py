data_driven = True
data_driven_correction = True

import json

import sys
import style

import optparse

from math import hypot, pi, sqrt, acos, cos, sin, atan2

from pprint import pprint

parser = optparse.OptionParser()

parser.add_option('--lep',dest='lep',default='both')
parser.add_option('--phoeta',dest='phoeta',default='both')
parser.add_option('-i',dest='inputfile')
parser.add_option('-o',dest='outputdir',default="/eos/user/a/amlevin/www/tmp/")

(options,args) = parser.parse_args()

year = "2016"
lumi = 35.9

def get_postfilter_selection_string(syst="nominal"):
    assert(syst == "nominal" or syst == "JESUp" or syst == "JERUp")

    if syst == "nominal":
        return "(puppimet > 40)"
    elif syst == "JESUp":
        return "(puppimetJESUp > 40)"
    elif syst == "JERUp":
        return "(puppimetJERUp > 40)"
    else:
        assert(0)

def get_filter_string(year,isdata=True):
    if not isdata:
        puppimet_cutstring = "(puppimet > 40 || puppimetJESUp > 40 || puppimetJERUp > 40)"
    else:    
        puppimet_cutstring = "(puppimet > 40)"

    if options.lep == "muon":
        if year == "2016":
            return "(pass_selection && " + photon_eta_cutstring+" && " + puppimet_cutstring + " && abs(lepton_pdg_id) == 13 && photon_pt > 25 && lepton_pt > 25)"
        elif year == "2017":
            return "(pass_selection && " + photon_eta_cutstring+" && " + puppimet_cutstring + " && abs(lepton_pdg_id) == 13 && photon_pt > 25 && lepton_pt > 30)"
        elif year == "2018":
            return "(pass_selection && " + photon_eta_cutstring+" && " + puppimet_cutstring + " && abs(lepton_pdg_id) == 13 && photon_pt > 25 && lepton_pt > 25)"
        else:
            assert(0)
    elif options.lep == "electron":                
        if year == "2016":
            return "(pass_selection && " + photon_eta_cutstring+" && " + puppimet_cutstring + " && abs(lepton_pdg_id) == 11 && photon_pt > 25 && lepton_pt > 30)"
        elif year == "2017":
            return "(pass_selection && " + photon_eta_cutstring+" && " + puppimet_cutstring + " && abs(lepton_pdg_id) == 11 && photon_pt > 25 && lepton_pt > 35)"
        elif year == "2018":
            return "(pass_selection && " + photon_eta_cutstring+" && " + puppimet_cutstring + " && abs(lepton_pdg_id) == 11 && photon_pt > 25 && lepton_pt > 35)"
        else:
            assert(0)
    elif options.lep == "both":    
        if year == "2016":
            return "(pass_selection && " + photon_eta_cutstring+" && " + puppimet_cutstring + " && ((abs(lepton_pdg_id) == 13 && photon_pt > 25 && lepton_pt > 25) || (abs(lepton_pdg_id) == 11 && photon_pt > 25 && lepton_pt > 30)))"
        elif year == "2017":
            return "(pass_selection && " + photon_eta_cutstring+" && " + puppimet_cutstring + " && ((abs(lepton_pdg_id) == 13 && photon_pt > 25 && lepton_pt > 30) || (abs(lepton_pdg_id) == 11 && photon_pt > 25 && lepton_pt > 35)))"
        elif year == "2018":
            return "(pass_selection && " + photon_eta_cutstring+" && " + puppimet_cutstring + " && ((abs(lepton_pdg_id) == 13 && photon_pt > 25 && lepton_pt > 25) || (abs(lepton_pdg_id) == 11 && photon_pt > 25 && lepton_pt > 35)))"
        else:
            assert(0)
    else:
        assert(0)

if options.lep == "muon":
    lepton_name = "muon"
elif options.lep == "electron":
    lepton_name = "electron"
elif options.lep == "both":
    lepton_name = "both"
else:
    assert(0)

if options.phoeta == "barrel":
    photon_eta_min = 0
    photon_eta_max = 1.5
elif options.phoeta == "endcap":
    photon_eta_min = 1.5
    photon_eta_max = 2.5
elif options.phoeta == "both":
    photon_eta_min = 0
    photon_eta_max = 2.5
else:
    assert(0)

photon_eta_cutstring = "((abs(photon_eta) < "+str(photon_eta_max)+") && (abs(photon_eta) > "+str(photon_eta_min)+"))"

import ROOT

ROOT.gROOT.cd()

ROOT.ROOT.EnableImplicitMT()

#when the TMinuit object is reused, the random seed is not reset after each fit, so the fit result can change when it is run on the same input 
ROOT.TMinuitMinimizer.UseStaticMinuit(False)

mlg_fit_upper_bound = 400

#the first variable is for the ewdim6 analysis
#variables = ["photon_pt","dphilg","met","lepton_pt","lepton_eta","photon_pt","photon_eta","mlg","lepton_phi","photon_phi","njets40","mt","npvs","drlg"]
#variables_labels = ["ewdim6_photon_pt","dphilg","met","lepton_pt","lepton_eta","photon_pt","photon_eta","mlg","lepton_phi","photon_phi","njets40","mt","npvs","drlg"]

variables = ["photon_pt_overflow","detalg","dphilmet","dphilg","puppimet","lepton_pt","lepton_eta","photon_pt","photon_eta","mlg","mlg","lepton_phi","photon_phi","njets40","mt","puppimt","npvs","drlg","photon_pt","met","photon_recoil"]
variables_labels = ["ewdim6_photon_pt","detalg","dphilmet","dphilg","puppimet","lepton_pt","lepton_eta","photon_pt","photon_eta","fit_mlg","mlg","lepton_phi","photon_phi","njets40","mt","puppimt","npvs","drlg","photon_pt_20to180","met","photon_recoil"]


assert(len(variables) == len(variables_labels))

from array import array

binning_photon_pt = array('f',[400,500,600,900,1500])
#binning_photon_pt = array('f',[300,500,750,1000,1500])
#binning_photon_pt = array('f',[100,200,300,400,500,600])

n_photon_pt_bins = len(binning_photon_pt)-1

variable_definitions = [
["detalg" , "abs(lepton_eta-photon_eta)"],
["dphilmet" , "abs(lepton_phi - metphi) > TMath::Pi() ? abs(abs(lepton_phi - metphi) - 2*TMath::Pi()) : abs(lepton_phi - metphi)"],
["dphilg" , "abs(lepton_phi - photon_phi) > TMath::Pi() ? abs(abs(lepton_phi - photon_phi) - 2*TMath::Pi()) : abs(lepton_phi - photon_phi)"],
["drlg" , "sqrt(dphilg*dphilg+detalg*detalg)" ],
["photon_recoil","cos(photon_phi)*(-lepton_pt*cos(lepton_phi)-puppimet*cos(puppimetphi)) + sin(photon_phi)*(-lepton_pt*sin(lepton_phi) -puppimet*sin(puppimetphi))"],
["photon_pt_overflow","TMath::Min(float(photon_pt),float("+str(   (binning_photon_pt[n_photon_pt_bins] + binning_photon_pt[n_photon_pt_bins-1])/2) +"))"  ]
]


histogram_models = [ROOT.RDF.TH1DModel('', '', n_photon_pt_bins, binning_photon_pt ),ROOT.RDF.TH1DModel('','',16,0,6),ROOT.RDF.TH1DModel('','',16,0,pi),ROOT.RDF.TH1DModel('','',48,0,pi), ROOT.RDF.TH1DModel("met", "", 15 , 0., 300 ), ROOT.RDF.TH1DModel('lepton_pt', '', 8, 20., 180 ), ROOT.RDF.TH1DModel('lepton_eta', '', 10, -2.5, 2.5 ), ROOT.RDF.TH1DModel('', '', n_photon_pt_bins, binning_photon_pt ), ROOT.RDF.TH1DModel('photon_eta', '', 10, -2.5, 2.5 ), ROOT.RDF.TH1DModel("mlg","",mlg_fit_upper_bound/2,0,mlg_fit_upper_bound), ROOT.RDF.TH1DModel("mlg","",100,0,200),ROOT.RDF.TH1DModel("lepton_phi","",14,-3.5,3.5), ROOT.RDF.TH1DModel("photon_phi","",14,-3.5,3.5), ROOT.RDF.TH1DModel("njets40","",7,-0.5,6.5), ROOT.RDF.TH1DModel("mt","",10,0,200), ROOT.RDF.TH1DModel("puppimt","",10,0,200), ROOT.RDF.TH1DModel("npvs","",51,-0.5,50.5), ROOT.RDF.TH1DModel("drlg","",16,0,5), ROOT.RDF.TH1DModel('photon_pt', '', 8, 20., 180 ),ROOT.RDF.TH1DModel("met", "", 15 , 0., 300 ),ROOT.RDF.TH1DModel('photon_recoil', '', 20, -70., 130 )] 

assert(len(variables) == len(histogram_models))

mlg_index = 9

def getXaxisLabel(varname):
    if varname == "njets40":
        return "number of jets"
    elif varname == "detalg":
        return "#Delta #eta(l,g)"
    elif varname == "dphilmet":
        return "#Delta#phi(l,MET)"
    elif varname == "corrdphilmet":
        return "corrected #Delta#phi(l,MET)"
    elif varname == "drlg":
        return "#Delta R(l,g)"
    elif varname == "dphilg":
        return "#Delta#phi(l,g)"
    elif varname == "npvs":
        return "number of PVs"
    elif varname == "mt":
        return "m_{t} (GeV)"
    elif varname == "puppimt":
        return "Puppi m_{t} (GeV)"
    elif varname == "corrmt":
        return "corrected m_{t} (GeV)"
    elif varname == "mlg":
        return "m_{lg} (GeV)"
    elif varname == "puppimet":
        return "Puppi MET (GeV)"
    elif varname == "met":
        return "MET (GeV)"
    elif varname == "corrmet":
        return "corrected MET (GeV)"
    elif varname == "lepton_pt":
        return "lepton p_{T} (GeV)"
    elif varname == "lepton_eta":
        return "lepton #eta"
    elif varname == "lepton_phi":
        return "lepton #phi"
    elif varname == "photon_pt":
        return "photon p_{T} (GeV)"
    elif varname == "photon_pt_overflow":
        return "photon p_{T} (GeV)"
    elif varname == "photon_eta":
        return "photon #eta"    
    elif varname == "photon_phi":
        return "photon #phi"
    elif varname == "photon_recoil":
        return "photon recoil (GeV)"
    else:
        assert(0)

xoffsetstart = 0.0;
yoffsetstart = 0.0;
xoffset = 0.20;
yoffset = 0.05;

xpositions = [0.68,0.68,0.68,0.68,0.4,0.4,0.4,0.4,0.21,0.21,0.21,0.21]
ypositions = [0,1,2,3,0,1,2,3,0,1,2,3]

#xpositions = [0.68,0.68,0.68,0.68,0.68,0.68,0.68,0.445,0.445,0.445,0.445,0.445,0.445,0.445,0.21,0.21,0.21,0.21,0.21,0.21,0.21]
#ypositions = [0,1,2,3,4,5,6,0,1,2,3,4,5,6,0,1,2,3,4,5,6]

style.GoodStyle().cd()

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


wjets_pileup = {}
wjets_real = {}
wjets_fake = {}

wjets_pileup["hists"] = []
wjets_real["hists"] = []
wjets_fake["hists"] = []

sample = {"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019/wjets.root", "xs" : 60430.0}
#sample = {"filename" : "/afs/cern.ch/work/a/amlevin/tmp/wjets.root", "xs" : 60430.0}



sample["file"] = ROOT.TFile.Open(sample["filename"])
sample["tree"] = sample["file"].Get("Events")
sample["nweightedevents"] = sample["file"].Get("nEventsGenWeighted").GetBinContent(1)

for i in range(len(variables)):
    wjets_pileup["hists"].append(histogram_models[i].GetHistogram())
    wjets_real["hists"].append(histogram_models[i].GetHistogram())
    wjets_fake["hists"].append(histogram_models[i].GetHistogram())

for i in range(len(variables)):
    wjets_pileup["hists"][i].Sumw2()
    wjets_pileup["hists"][i].SetName("wjets pileup "+variables[i])
    wjets_real["hists"][i].Sumw2()
    wjets_real["hists"][i].SetName("wjets real "+variables[i])
    wjets_fake["hists"][i].Sumw2()
    wjets_fake["hists"][i].SetName("wjets fake "+variables[i])

c1 = ROOT.TCanvas("c1", "c1",5,50,500,500)

ROOT.gROOT.cd()

eff_scale_factor_cpp = '''

TFile photon_id_2016_sf_file("eff_scale_factors/2016/Fall17V2_2016_Medium_photons.root");
TH2F * photon_id_2016_sf = (TH2F*) photon_id_2016_sf_file.Get("EGamma_SF2D");

TFile photon_id_2017_sf_file("eff_scale_factors/2017/2017_PhotonsMedium.root");
TH2F * photon_id_2017_sf = (TH2F*) photon_id_2017_sf_file.Get("EGamma_SF2D");

TFile photon_id_2018_sf_file("eff_scale_factors/2018/2018_PhotonsMedium.root","read");
TH2F * photon_id_2018_sf = (TH2F*) photon_id_2018_sf_file.Get("EGamma_SF2D");

TFile electron_id_2016_sf_file("eff_scale_factors/2016/2016LegacyReReco_ElectronMedium_Fall17V2.root","read");
TH2F * electron_id_2016_sf = (TH2F*) electron_id_2016_sf_file.Get("EGamma_SF2D");

TFile electron_id_2017_sf_file("eff_scale_factors/2017/2017_ElectronMedium.root","read");
TH2F * electron_id_2017_sf = (TH2F*)electron_id_2017_sf_file.Get("EGamma_SF2D");

TFile electron_id_2018_sf_file("eff_scale_factors/2018/2018_ElectronMedium.root","read");
TH2F * electron_id_2018_sf = (TH2F*)electron_id_2018_sf_file.Get("EGamma_SF2D");

TFile electron_reco_2016_sf_file("eff_scale_factors/2016/EGM2D_BtoH_GT20GeV_RecoSF_Legacy2016.root","read");
TH2F * electron_reco_2016_sf = (TH2F*) electron_reco_2016_sf_file.Get("EGamma_SF2D");

TFile electron_reco_2017_sf_file("eff_scale_factors/2017/egammaEffi.txt_EGM2D_runBCDEF_passingRECO.root","read");
TH2F * electron_reco_2017_sf = (TH2F*)electron_reco_2017_sf_file.Get("EGamma_SF2D");

TFile electron_reco_2018_sf_file("eff_scale_factors/2018/egammaEffi.txt_EGM2D_updatedAll.root" ,"read");
TH2F * electron_reco_2018_sf = (TH2F*)electron_reco_2018_sf_file.Get("EGamma_SF2D");

TFile muon_iso_2016_sf_file("eff_scale_factors/2016/RunBCDEF_SF_ISO.root","read");
TH2D * muon_iso_2016_sf = (TH2D*) muon_iso_2016_sf_file.Get("NUM_TightRelIso_DEN_TightIDandIPCut_eta_pt");

TFile muon_id_2016_sf_file("eff_scale_factors/2016/RunBCDEF_SF_ID.root","read");
TH2D * muon_id_2016_sf = (TH2D*) muon_id_2016_sf_file.Get("NUM_TightID_DEN_genTracks_eta_pt");

TFile muon_iso_2017_sf_file("eff_scale_factors/2017/RunBCDEF_SF_ISO.root","read");
TH2D * muon_iso_2017_sf = (TH2D*) muon_iso_2017_sf_file.Get("NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta");

TFile muon_id_2017_sf_file("eff_scale_factors/2017/RunBCDEF_SF_ID.root","read");
TH2D * muon_id_2017_sf = (TH2D*) muon_id_2017_sf_file.Get("NUM_TightID_DEN_genTracks_pt_abseta");

TFile muon_iso_2018_sf_file("eff_scale_factors/2018/RunABCD_SF_ISO.root","read");
TH2D * muon_iso_2018_sf = (TH2D*) muon_iso_2018_sf_file.Get("NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta");

TFile muon_id_2018_sf_file("eff_scale_factors/2018/RunABCD_SF_ID.root","read");
TH2D * muon_id_2018_sf = (TH2D*)muon_id_2018_sf_file.Get("NUM_TightID_DEN_TrackerMuons_pt_abseta");

float electron_efficiency_scale_factor(float pt, float eta, string year,bool id_err_up=false, bool reco_err_up=false) {

    TH2F * electron_reco_sf = 0;
    TH2F * electron_id_sf = 0;

    if (year == "2016") {
        electron_reco_sf = electron_reco_2016_sf;
        electron_id_sf = electron_id_2016_sf;
    }
    else if (year == "2017"){
        electron_reco_sf = electron_reco_2017_sf;
        electron_id_sf = electron_id_2017_sf;
    }
    else if (year == "2018") {
        electron_reco_sf = electron_reco_2018_sf;
        electron_id_sf = electron_id_2018_sf;
    }
    else
        assert(0);


    //the reco 2D histogram is really a 1D histogram
    float sf_id=electron_id_sf->GetBinContent(electron_id_sf->GetXaxis()->FindFixBin(eta),electron_id_sf->GetYaxis()->FindFixBin(pt));
    if (id_err_up) sf_id+=electron_id_sf->GetBinError(electron_id_sf->GetXaxis()->FindFixBin(eta),electron_id_sf->GetYaxis()->FindFixBin(pt));

    float sf_reco=electron_reco_sf->GetBinContent(electron_reco_sf->GetXaxis()->FindFixBin(eta),1);

    if (reco_err_up) sf_reco+=electron_reco_sf->GetBinError(electron_reco_sf->GetXaxis()->FindFixBin(eta),1);
    
    return sf_id*sf_reco;
}

float photon_efficiency_scale_factor(float pt,float eta,string year,bool err_up=false){

    TH2F * photon_id_sf = 0;

    if (year == "2016") photon_id_sf = photon_id_2016_sf;
    else if (year == "2017") photon_id_sf = photon_id_2017_sf;
    else if (year == "2018") photon_id_sf = photon_id_2018_sf;
    else assert(0);

    float mypt = TMath::Min(pt,float(photon_id_sf->GetYaxis()->GetBinCenter(photon_id_sf->GetNbinsY())));
    float myeta = TMath::Max(TMath::Min(eta,float(photon_id_sf->GetXaxis()->GetBinCenter(photon_id_sf->GetNbinsX()))),float(photon_id_sf->GetXaxis()->GetBinCenter(1)));

    float sf = photon_id_sf->GetBinContent(photon_id_sf->GetXaxis()->FindFixBin(myeta),photon_id_sf->GetYaxis()->FindFixBin(mypt));

    if (err_up) sf += photon_id_sf->GetBinError(photon_id_sf->GetXaxis()->FindFixBin(myeta),photon_id_sf->GetYaxis()->FindFixBin(mypt));

    return sf;
}

float muon_efficiency_scale_factor(float pt,float eta,string year,bool iso_err_up=false,bool id_err_up=false) {

    TH2D * muon_iso_sf = 0;
    TH2D * muon_id_sf = 0;

    if (year == "2016") {
        muon_iso_sf = muon_iso_2016_sf;
        muon_id_sf = muon_id_2016_sf;
    }
    else if (year == "2017") {
        muon_iso_sf = muon_iso_2017_sf;
        muon_id_sf = muon_id_2017_sf;
    }
    else if (year == "2018"){
        muon_iso_sf = muon_iso_2018_sf;
        muon_id_sf = muon_id_2018_sf;
    }
    else assert(0);

    int muon_iso_sf_xaxisbin = -1;
    int muon_iso_sf_yaxisbin = -1;

    if (year == "2016") {   
        muon_iso_sf_xaxisbin = muon_iso_sf->GetXaxis()->FindFixBin(eta);
        muon_iso_sf_yaxisbin = muon_iso_sf->GetYaxis()->FindFixBin(TMath::Min(pt,float(muon_iso_sf->GetYaxis()->GetBinCenter(muon_iso_sf->GetNbinsY()))));
    }
    else if (year == "2017") {
        muon_iso_sf_yaxisbin = muon_iso_sf->GetYaxis()->FindFixBin(abs(eta));
        muon_iso_sf_xaxisbin = muon_iso_sf->GetXaxis()->FindFixBin(TMath::Min(pt,float(muon_iso_sf->GetXaxis()->GetBinCenter(muon_iso_sf->GetNbinsX()))));
    }
    else if (year == "2018") {
        muon_iso_sf_yaxisbin = muon_iso_sf->GetYaxis()->FindFixBin(abs(eta));
        muon_iso_sf_xaxisbin = muon_iso_sf->GetXaxis()->FindFixBin(TMath::Min(pt,float(muon_iso_sf->GetXaxis()->GetBinCenter(muon_iso_sf->GetNbinsX()))));
    }
    else assert(0);

    int muon_id_sf_xaxisbin = -1;
    int muon_id_sf_yaxisbin = -1;

    if (year == "2016") {    
        muon_id_sf_xaxisbin = muon_id_sf->GetXaxis()->FindFixBin(eta);
        muon_id_sf_yaxisbin = muon_id_sf->GetYaxis()->FindFixBin(TMath::Min(pt,float(muon_id_sf->GetYaxis()->GetBinCenter(muon_id_sf->GetNbinsY()))));
    }
    else if (year == "2017") {
        muon_id_sf_yaxisbin = muon_id_sf->GetYaxis()->FindFixBin(abs(eta));
        muon_id_sf_xaxisbin = muon_id_sf->GetXaxis()->FindFixBin(TMath::Min(pt,float(muon_id_sf->GetXaxis()->GetBinCenter(muon_id_sf->GetNbinsX()))));
    }
    else if (year == "2018") {
        muon_id_sf_yaxisbin = muon_id_sf->GetYaxis()->FindFixBin(abs(eta));
        muon_id_sf_xaxisbin = muon_id_sf->GetXaxis()->FindFixBin(TMath::Min(pt,float(muon_id_sf->GetXaxis()->GetBinCenter(muon_id_sf->GetNbinsX()))));
    }
    else assert(0);

    float iso_sf = muon_iso_sf->GetBinContent(muon_iso_sf_xaxisbin,muon_iso_sf_yaxisbin);

    if (iso_err_up) iso_sf += muon_iso_sf->GetBinError(muon_iso_sf_xaxisbin,muon_iso_sf_yaxisbin);

    float id_sf = muon_id_sf->GetBinContent(muon_id_sf_xaxisbin,muon_id_sf_yaxisbin); 
    
    if (id_err_up) id_sf += muon_id_sf->GetBinError(muon_id_sf_xaxisbin,muon_id_sf_yaxisbin) ;

    return iso_sf * id_sf;

}

'''

ROOT.gInterpreter.Declare(eff_scale_factor_cpp)

photon_gen_matching_cutstring="!(photon_gen_matching == 1 || photon_gen_matching == 4 || photon_gen_matching == 5 || photon_gen_matching == 6)"
                
rdf = ROOT.RDataFrame("Events",sample["filename"])

rinterface = rdf.Filter(get_filter_string(year))

rinterface = rinterface.Define("xs_weight",str(sample["xs"]*1000*lumi/sample["nweightedevents"]) + "*gen_weight/abs(gen_weight)") 
#rinterface = rinterface.Define("xs_weight","gen_weight/abs(gen_weight)") 
#rinterface = rinterface.Define("xs_weight","1") 

prefire_weight_string = "PrefireWeight"
prefire_up_weight_string = "PrefireWeight_Up"

rinterface = rinterface.Define("base_weight",get_postfilter_selection_string()+"*xs_weight*puWeight*"+prefire_weight_string+"*photon_efficiency_scale_factor(photon_pt,photon_eta,\""+year+"\")*(abs(lepton_pdg_id) == 13 ? muon_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\") : electron_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\"))")      
#rinterface = rinterface.Define("base_weight",get_postfilter_selection_string()+"*xs_weight")      
rinterface = rinterface.Define("weight_pileup","(photon_genjet_matching == 0 && photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_cutstring + ")*base_weight")
rinterface = rinterface.Define("weight_fake","(photon_genjet_matching == 1 && !(photon_gen_matching == 3) && photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_cutstring + ")*base_weight")
rinterface = rinterface.Define("weight_real","(photon_genjet_matching == 1 && photon_gen_matching == 3 && photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_cutstring + ")*base_weight")
#rinterface = rinterface.Define("weight_pileup","(photon_mergedgen_matching <= 5 && photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_cutstring + ")*base_weight")
#rinterface = rinterface.Define("weight_fake","(photon_mergedgen_matching > 5 && !(photon_gen_matching == 3) && photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_cutstring + ")*base_weight")
#rinterface = rinterface.Define("weight_real","(photon_mergedgen_matching > 5 && photon_gen_matching == 3 && photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_cutstring + ")*base_weight")

for variable_definition in variable_definitions:
    rinterface = rinterface.Define(variable_definition[0],variable_definition[1])
    
rresultptrs_wjets_pileup = []    
rresultptrs_wjets_real = []    
rresultptrs_wjets_fake = []    

for i in range(len(variables)):
    rresultptrs_wjets_pileup.append(rinterface.Histo1D(histogram_models[i],variables[i],"weight_pileup"))
    rresultptrs_wjets_real.append(rinterface.Histo1D(histogram_models[i],variables[i],"weight_real"))
    rresultptrs_wjets_fake.append(rinterface.Histo1D(histogram_models[i],variables[i],"weight_fake"))

    

for i in range(len(variables)):
    wjets_pileup["hists"][i].Add(rresultptrs_wjets_pileup[i].GetValue())
    wjets_real["hists"][i].Add(rresultptrs_wjets_real[i].GetValue())
    wjets_fake["hists"][i].Add(rresultptrs_wjets_fake[i].GetValue())


for i in range(len(variables)):
    wjets_pileup["hists"][i].SetFillColor(ROOT.kRed)
    wjets_pileup["hists"][i].SetFillStyle(1001)
    wjets_pileup["hists"][i].SetLineColor(ROOT.kRed)
    wjets_real["hists"][i].SetFillColor(ROOT.kBlue)
    wjets_real["hists"][i].SetFillStyle(1001)
    wjets_real["hists"][i].SetLineColor(ROOT.kBlue)
    wjets_fake["hists"][i].SetFillColor(ROOT.kGreen)
    wjets_fake["hists"][i].SetFillStyle(1001)
    wjets_fake["hists"][i].SetLineColor(ROOT.kGreen)
    
for i in range(len(variables)):


    s=str(lumi)+" fb^{-1} (13 TeV)"
    lumilabel = ROOT.TLatex (0.95, 0.93, s)
    lumilabel.SetNDC ()
    lumilabel.SetTextAlign (30)
    lumilabel.SetTextFont (42)
    lumilabel.SetTextSize (0.040)

    hsum = wjets_pileup["hists"][i].Clone()
    hsum.Scale(0.0)

    hstack = ROOT.THStack()

    hsum.Add(wjets_pileup["hists"][i])
    hstack.Add(wjets_pileup["hists"][i])

    hsum.Add(wjets_real["hists"][i])
    hstack.Add(wjets_real["hists"][i])

    hsum.Add(wjets_fake["hists"][i])
    hstack.Add(wjets_fake["hists"][i])

    hstack.SetMinimum(0)
    hsum.SetMinimum(0)

    wjets_pileup["hists"][i].Print("all")

#    hsum.Print("all")

    hsum.SetMaximum(hsum.GetMaximum()*1.55)

    set_axis_fonts(hsum,"x",getXaxisLabel(variables[i]))

    hsum.Draw("hist")
    hstack.Draw("hist same")


    cmslabel = ROOT.TLatex (0.18, 0.93, "")
    cmslabel.SetNDC ()
    cmslabel.SetTextAlign (10)
    cmslabel.SetTextFont (42)
    cmslabel.SetTextSize (0.040)
    cmslabel.Draw ("same") 
    
    lumilabel.Draw("same")


    j=0
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wjets_pileup["hists"][i],"pileup","f")
    j=1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wjets_real["hists"][i],"real","f")
    j=2
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wjets_fake["hists"][i],"instrumental","f")


#    hstack.Draw("hist same")

    gstat = ROOT.TGraphAsymmErrors(hsum);

    for j in range(0,gstat.GetN()):
        gstat.SetPointEYlow (j, hsum.GetBinError(j+1));
        gstat.SetPointEYhigh(j, hsum.GetBinError(j+1));

    gstat.SetFillColor(12);
    gstat.SetFillStyle(3345);
    gstat.SetMarkerSize(0);
    gstat.SetLineWidth(0);
    gstat.SetLineColor(ROOT.kWhite);
    gstat.Draw("E2same");

    c1.Update()
    c1.ForceUpdate()
    c1.Modified()

    c1.SaveAs(options.outputdir + "/" + variables_labels[i] + ".png")

c1.Close()

