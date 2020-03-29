data_driven = True
data_driven_correction = True

import json
import sys
import style

import optparse

from math import hypot, pi, sqrt, acos, cos, sin, atan2

from pprint import pprint

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
    return abs(dphi)

def deltaR(eta1,phi1,eta2=None,phi2=None):
    ## catch if called with objects                                                                                                                                  
    if eta2 == None:
        return deltaR(eta1.eta,eta1.phi,phi1.eta,phi1.phi)
    ## otherwise                                                                                                                                                     
    return hypot(eta1-eta2, deltaPhi(phi1,phi2))

#make the Down shape from the Up shape
def makeDownShape(histUp,hist):

    hist_clone=hist.Clone()
    histUp_clone=histUp.Clone()

    hist_clone.Scale(2)
    histUp_clone.Scale(-1)

    hist_clone.Add(histUp_clone)

    return hist_clone

dict_lumi = {"2016" : 35.9, "2017" : 41.5, "2018" : 59.6}

parser = optparse.OptionParser()

parser.add_option('--userdir',dest='userdir',default='/afs/cern.ch/user/a/amlevin/') #not used now
parser.add_option('--workdir',dest='workdir',default='/afs/cern.ch/work/a/amlevin/')
parser.add_option('--lep',dest='lep',default='both')
parser.add_option('--year',dest='year',default='all')
parser.add_option('--zveto',dest='zveto',action='store_true',default=False)
parser.add_option('--phoeta',dest='phoeta',default='both')
parser.add_option('--overflow',dest='overflow',action='store_true',default=False)
parser.add_option('--make_datacard',dest='make_datacard',action='store_true',default=False)
parser.add_option('--make_cut_and_count_datacard',dest='make_cut_and_count_datacard',action='store_true',default=False)
parser.add_option('--fit',dest='fit',action='store_true',default=False)
parser.add_option('--closure_test',dest='closure_test',action='store_true',default=False)
parser.add_option('--no_pdf_var_for_2017_and_2018',dest='no_pdf_var_for_2017_and_2018',action='store_true',default=False)
parser.add_option('--no_wjets_for_2017_and_2018',dest='no_wjets_for_2017_and_2018',action='store_true',default=False)
parser.add_option('--ewdim6',dest='ewdim6',action='store_true',default=False)
parser.add_option('--use_wjets_for_fake_photon',dest='use_wjets_for_fake_photon',action='store_true',default=False)
parser.add_option('--float_fake_sig_cont',dest='float_fake_sig_cont',action='store_true',default=False)
parser.add_option('--draw_ewdim6',dest='draw_ewdim6',action='store_true',default=False)
parser.add_option('--ewdim6_scaling_only',dest='ewdim6_scaling_only',action='store_true',default=False)
parser.add_option('--make_plots',dest='make_plots',action='store_true',default=False)
parser.add_option('--blind',dest='blind',action='store_true',default=False)

parser.add_option('-i',dest='inputfile')
parser.add_option('-o',dest='outputdir',default="/eos/user/a/amlevin/www/tmp/")

(options,args) = parser.parse_args()

if options.ewdim6_scaling_only and not options.ewdim6:
    assert(0)

if options.fit and not options.lep == "electron":
    assert(0)

if options.year == "2016":
    years = ["2016"]
    totallumi=dict_lumi["2016"]
elif options.year == "2017":
    years=["2017"]
    totallumi=dict_lumi["2017"]
elif options.year == "2018":
    years=["2018"]
    totallumi=dict_lumi["2018"]
elif options.year == "run2":
    years=["2016","2017","2018"]
    totallumi=dict_lumi["2016"]+dict_lumi["2017"]+dict_lumi["2018"]
else:
    assert(0)

den_pho_sel = 4

sieie_cut_2016_barrel = 0.01022
sieie_cut_2016_endcap = 0.03001
sieie_cut_2017_barrel = 0.01015
sieie_cut_2017_endcap = 0.0272
sieie_cut_2018_barrel = 0.01015
sieie_cut_2018_endcap = 0.0272

chiso_cut_2016_barrel = 1.416
chiso_cut_2016_endcap = 1.012
chiso_cut_2017_barrel = 1.141
chiso_cut_2017_endcap = 1.051
chiso_cut_2018_barrel = 1.141
chiso_cut_2018_endcap = 1.051

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

#f_json=open("/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt")
#f_json=open("delete_this_JSON.txt")

#good_run_lumis=json.loads(f_json.read())

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

def get_filter_string(year,isdata=True,lep=None):

    if lep == None:
        lep = options.lep

    if not isdata:
        puppimet_cutstring = "(puppimet > 40 || puppimetJESUp > 40 || puppimetJERUp > 40)"
    else:    
        puppimet_cutstring = "(puppimet > 40)"

    if options.zveto:
        zveto_cutstring = "(mlg < 60 || mlg > 120)"
    else:
        zveto_cutstring = "1"

    if lep == "muon":
        if year == "2016":
            return "(pass_selection && " + photon_eta_cutstring+" && " + zveto_cutstring + " && " + puppimet_cutstring + " && abs(lepton_pdg_id) == 13 && photon_pt > 25 && lepton_pt > 26)"
        elif year == "2017":
            return "(pass_selection && " + photon_eta_cutstring+" && " + zveto_cutstring + " && " + puppimet_cutstring + " && abs(lepton_pdg_id) == 13 && photon_pt > 25 && lepton_pt > 30)"
        elif year == "2018":
            return "(pass_selection && " + photon_eta_cutstring+" && " + zveto_cutstring + " && " + puppimet_cutstring + " && abs(lepton_pdg_id) == 13 && photon_pt > 25 && lepton_pt > 26)"
        else:
            assert(0)
    elif lep == "electron":                
        if year == "2016":
            return "(pass_selection && " + photon_eta_cutstring+" && " + zveto_cutstring + " && " + puppimet_cutstring + " && abs(lepton_pdg_id) == 11 && photon_pt > 25 && lepton_pt > 30)"
        elif year == "2017":
            return "(pass_selection && " + photon_eta_cutstring+" && " + zveto_cutstring + " && " + puppimet_cutstring + " && abs(lepton_pdg_id) == 11 && photon_pt > 25 && lepton_pt > 35)"
        elif year == "2018":
            return "(pass_selection && " + photon_eta_cutstring+" && " + zveto_cutstring + " && " + puppimet_cutstring + " && abs(lepton_pdg_id) == 11 && photon_pt > 25 && lepton_pt > 35)"
        else:
            assert(0)
    elif lep == "both":    
        if year == "2016":
            return "(pass_selection && " + photon_eta_cutstring+" && " + zveto_cutstring + " && " + puppimet_cutstring + " && ((abs(lepton_pdg_id) == 13 && photon_pt > 25 && lepton_pt > 26) || (abs(lepton_pdg_id) == 11 && photon_pt > 25 && lepton_pt > 30)))"
#            return "(pass_selection && " + photon_eta_cutstring+" && " + zveto_cutstring + " && " + puppimet_cutstring + " && ((abs(lepton_pdg_id) == 13 && photon_pt > 20 && lepton_pt > 26) || (abs(lepton_pdg_id) == 11 && photon_pt > 20 && lepton_pt > 30)))"
        elif year == "2017":
            return "(pass_selection && " + photon_eta_cutstring+" && " + zveto_cutstring + " && " + puppimet_cutstring + " && ((abs(lepton_pdg_id) == 13 && photon_pt > 25 && lepton_pt > 30) || (abs(lepton_pdg_id) == 11 && photon_pt > 25 && lepton_pt > 35)))"
        elif year == "2018":
            return "(pass_selection && " + photon_eta_cutstring+" && " + zveto_cutstring + " && " + puppimet_cutstring + " && ((abs(lepton_pdg_id) == 13 && photon_pt > 25 && lepton_pt > 26) || (abs(lepton_pdg_id) == 11 && photon_pt > 25 && lepton_pt > 35)))"
        else:
            assert(0)
    else:
        assert(0)

def pass_json(run,lumi):

    if str(run) not in good_run_lumis.keys():
        return False

    for lumi_pair in good_run_lumis[str(run)]:
        if lumi < lumi_pair[1] and lumi > lumi_pair[0]:
            return True

    return False    

import ROOT

ROOT.gROOT.cd()

ROOT.ROOT.EnableImplicitMT()

#when the TMinuit object is reused, the random seed is not reset after each fit, so the fit result can change when it is run on the same input 
ROOT.TMinuitMinimizer.UseStaticMinuit(False)

if options.closure_test:
    from wg_labels_closuretest import labels
else:
    from wg_labels import labels
#    from wg_labels_wjets import labels
#from wg_labels_recoil_tree import labels

#mlg_fit_lower_bound = 10
#mlg_fit_upper_bound = 30

mlg_fit_lower_bound = 10
mlg_fit_upper_bound = 250
#mlg_fit_upper_bound = 200
#mlg_fit_upper_bound = 300
mlg_bin_width=2

#the first variable is for the ewdim6 analysis
#variables = ["photon_pt","dphilg","met","lepton_pt","lepton_eta","photon_pt","photon_eta","mlg","lepton_phi","photon_phi","njets40","mt","npvs","drlg"]
#variables_labels = ["ewdim6_photon_pt","dphilg","met","lepton_pt","lepton_eta","photon_pt","photon_eta","mlg","lepton_phi","photon_phi","njets40","mt","npvs","drlg"]

variables = ["photon_pt_overflow","detalg","dphilpuppimet","dphilg","puppimet","lepton_pt","lepton_eta","photon_pt","photon_eta","mlg","mlg","lepton_phi","photon_phi","njets40","mt","puppimt","npvs","drlg","photon_pt","met","photon_recoil","dphigpuppimet","puppimetphi","mlg","mlg","mlg","mlg","mlg","mlg","mlg","photon_pt","photon_pt"]
variables_labels = ["ewdim6_photon_pt","detalg","dphilpuppimet","dphilg","puppimet","lepton_pt","lepton_eta","photon_pt","photon_eta","fit_mlg","mlg","lepton_phi","photon_phi","njets40","mt","puppimt","npvs","drlg","photon_pt_20to180","met","photon_recoil","dphigpuppimet","puppimetphi","mlg_large_bins","mlg_3bin","mlg_1bin","mlg_10bins","mlg_15bins","mlg_6bins","mlg_variable_binning","photon_pt","photon_pt"]


assert(len(variables) == len(variables_labels))

from array import array

binning_photon_pt = array('f',[400,500,600,900,1500])
#binning_photon_pt = array('f',[300,500,750,1000,1500])
#binning_photon_pt = array('f',[100,200,300,400,500,600])

#binning_mlg = array('f',[10,60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,98,100,102,104,106,108,110,112,114,116,118,120,200])
#binning_mlg = array('f',[10,60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,98,100,102,104,106,108,110,112,114,116,118,120,200]
binning_mlg = array('f',[60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,98,100,102,104,106,108,110,112,114,116,118,120])
#binning_mlg = array('f',[10,30,40,50,60,70,80,90,100,125,150,200,300])
#binning_mlg = array('f',[10,50,90,100,125,150,200,300])

n_photon_pt_bins = len(binning_photon_pt)-1

variable_definitions = [
["detalg" , "abs(lepton_eta-photon_eta)"],
["dphilpuppimet" , "abs(lepton_phi - puppimetphi) > TMath::Pi() ? abs(abs(lepton_phi - puppimetphi) - 2*TMath::Pi()) : abs(lepton_phi - puppimetphi)"],
["dphigpuppimet" , "abs(photon_phi - puppimetphi) > TMath::Pi() ? abs(abs(photon_phi - puppimetphi) - 2*TMath::Pi()) : abs(photon_phi - puppimetphi)"],
["dphilg" , "abs(lepton_phi - photon_phi) > TMath::Pi() ? abs(abs(lepton_phi - photon_phi) - 2*TMath::Pi()) : abs(lepton_phi - photon_phi)"],
["drlg" , "sqrt(dphilg*dphilg+detalg*detalg)" ],
["photon_recoil","cos(photon_phi)*(-lepton_pt*cos(lepton_phi)-puppimet*cos(puppimetphi)) + sin(photon_phi)*(-lepton_pt*sin(lepton_phi) -puppimet*sin(puppimetphi))"],
["photon_pt_overflow","TMath::Min(float(photon_pt),float("+str(   (binning_photon_pt[n_photon_pt_bins] + binning_photon_pt[n_photon_pt_bins-1])/2) +"))"  ]
]


histogram_models = [
ROOT.RDF.TH1DModel('', '', n_photon_pt_bins, binning_photon_pt ),
ROOT.RDF.TH1DModel('','',50,0,5), #detalg
ROOT.RDF.TH1DModel('','',48,0,pi), #dphilmet
ROOT.RDF.TH1DModel('','',12,0,pi), #dphilg
ROOT.RDF.TH1DModel("met", "", 40, 40., 200 ), 
ROOT.RDF.TH1DModel('lepton_pt', '', 48, 20., 180 ), 
ROOT.RDF.TH1DModel('lepton_eta', '', 50, -2.5, 2.5 ),
ROOT.RDF.TH1DModel('', '', n_photon_pt_bins, binning_photon_pt ), 
ROOT.RDF.TH1DModel('photon_eta', '', 50, -2.5, 2.5 ), 
#ROOT.RDF.TH1DModel("mlg","",mlg_fit_upper_bound/2,0,mlg_fit_upper_bound), 
ROOT.RDF.TH1DModel("mlg","",(mlg_fit_upper_bound-mlg_fit_lower_bound)/mlg_bin_width,mlg_fit_lower_bound,mlg_fit_upper_bound), 
ROOT.RDF.TH1DModel("mlg","",100,0,200),
ROOT.RDF.TH1DModel("lepton_phi","",56,-3.5,3.5), 
ROOT.RDF.TH1DModel("photon_phi","",56,-3.5,3.5), 
ROOT.RDF.TH1DModel("","",7,-0.5,6.5), #njets40
ROOT.RDF.TH1DModel("mt","",10,0,200), 
ROOT.RDF.TH1DModel("puppimt","",40,40,200), 
ROOT.RDF.TH1DModel("npvs","",51,-0.5,50.5), 
ROOT.RDF.TH1DModel("","",50,0,5), #drlg
ROOT.RDF.TH1DModel('photon_pt', '', 48, 20., 180 ),
ROOT.RDF.TH1DModel("met", "", 15 , 0., 300 ),
ROOT.RDF.TH1DModel('photon_recoil', '', 20, -70., 130 ),
ROOT.RDF.TH1DModel('','',48,0,pi), #dphigmet
ROOT.RDF.TH1DModel("","",56,-3.5,3.5), #puppimetphi
ROOT.RDF.TH1DModel("mlg","",30,0,300), #mlg
ROOT.RDF.TH1DModel("mlg","",3,0,300), #mlg
ROOT.RDF.TH1DModel("mlg","",1,0,300), #mlg
ROOT.RDF.TH1DModel("mlg","",10,0,300), #mlg
ROOT.RDF.TH1DModel("mlg","",15,0,300), #mlg
ROOT.RDF.TH1DModel("mlg","",6,0,300), #mlg
ROOT.RDF.TH1DModel('', '', len(binning_mlg) - 1, binning_mlg ), #variable mlg binning,
ROOT.RDF.TH1DModel('photon_pt', '', 40, 100., 400 ),
ROOT.RDF.TH1DModel('photon_pt', '', 10, 300., 400 ),
] 

assert(len(variables) == len(histogram_models))

mlg_index = 9
#mlg_index = 29

ewdim6_samples = {
"2016" : [{"xs" : 5.248, "filename" : options.workdir+"/data/wg/2016/1June2019/wgjetsewdim6.root"}],
"2017" : [{"xs" : 5.248, "filename" : options.workdir+"/data/wg/2016/1June2019/wgjetsewdim6.root"}],
"2018" : [{"xs" : 5.248, "filename" : options.workdir+"/data/wg/2016/1June2019/wgjetsewdim6.root"}]
}

for year in years:
    for sample in ewdim6_samples[year]:
        sample["file"] = ROOT.TFile(sample["filename"])
        sample["nweightedevents"] = sample["file"].Get("nEventsGenWeighted").GetBinContent(1)

def getXaxisLabel(varname):
    if varname == "njets40":
        return "number of jets"
    elif varname == "detalg":
        return "#Delta#eta(l,g)"
    elif varname == "dphilpuppimet":
        return "#Delta#phi(l,MET)"
    elif varname == "dphigpuppimet":
        return "#Delta#phi(g,MET)"
    elif varname == "corrdphilpuppimet":
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
        return "m_{t} (GeV)"
    elif varname == "corrmt":
        return "corrected m_{t} (GeV)"
    elif varname == "mlg":
        return "m_{lg} (GeV)"
    elif varname == "puppimet":
        return "MET (GeV)"
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
    elif varname == "puppimetphi":
        return "MET #phi"
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

for label in labels.keys():



    labels[label]["hists"] = {}

    labels[label]["hists-electron-id-sf-up"] = {}
    labels[label]["hists-electron-reco-sf-up"] = {}
    labels[label]["hists-electron-hlt-sf-up"] = {}
    labels[label]["hists-muon-id-sf-up"] = {}
    labels[label]["hists-muon-iso-sf-up"] = {}
    labels[label]["hists-muon-hlt-sf-up"] = {}
    labels[label]["hists-photon-id-sf-up"] = {}
    labels[label]["hists-pileup-up"] = {}
    labels[label]["hists-prefire-up"] = {}
    labels[label]["hists-jes-up"] = {}
    labels[label]["hists-jer-up"] = {}

    if labels[label]["syst-pdf"]:
        for i in range(0,32):
            labels[label]["hists-pdf-variation"+str(i)] = {}

    if labels[label]["syst-scale"]:
        for i in range(0,8):
            labels[label]["hists-scale-variation"+str(i)] = {}

    for i in range(len(variables)):    
        if labels[label]["color"] == None:
            continue

        labels[label]["hists"][i] = histogram_models[i].GetHistogram()
        labels[label]["hists"][i].SetName(label+" "+variables[i])
        labels[label]["hists"][i].Sumw2()

        labels[label]["hists-pileup-up"][i] = histogram_models[i].GetHistogram()
        labels[label]["hists-prefire-up"][i] = histogram_models[i].GetHistogram()
        labels[label]["hists-jes-up"][i] = histogram_models[i].GetHistogram()
        labels[label]["hists-jer-up"][i] = histogram_models[i].GetHistogram()
        labels[label]["hists-electron-id-sf-up"][i] = histogram_models[i].GetHistogram()
        labels[label]["hists-electron-reco-sf-up"][i] = histogram_models[i].GetHistogram()
        labels[label]["hists-electron-hlt-sf-up"][i] = histogram_models[i].GetHistogram()
        labels[label]["hists-muon-id-sf-up"][i] = histogram_models[i].GetHistogram()
        labels[label]["hists-muon-iso-sf-up"][i] = histogram_models[i].GetHistogram()
        labels[label]["hists-muon-hlt-sf-up"][i] = histogram_models[i].GetHistogram()
        labels[label]["hists-photon-id-sf-up"][i] = histogram_models[i].GetHistogram()
        labels[label]["hists-pileup-up"][i].Sumw2()
        labels[label]["hists-prefire-up"][i].Sumw2()
        labels[label]["hists-electron-id-sf-up"][i].Sumw2()
        labels[label]["hists-electron-reco-sf-up"][i].Sumw2()
        labels[label]["hists-electron-hlt-sf-up"][i].Sumw2()
        labels[label]["hists-muon-id-sf-up"][i].Sumw2()
        labels[label]["hists-muon-iso-sf-up"][i].Sumw2()
        labels[label]["hists-muon-hlt-sf-up"][i].Sumw2()
        labels[label]["hists-photon-id-sf-up"][i].Sumw2()
        

        if labels[label]["syst-pdf"]:
            for j in range(0,32):
                labels[label]["hists-pdf-variation"+str(j)][i] = histogram_models[i].GetHistogram()
                labels[label]["hists-pdf-variation"+str(j)][i].Sumw2()

        if labels[label]["syst-scale"]:
            for j in range(0,8):
                labels[label]["hists-scale-variation"+str(j)][i] = histogram_models[i].GetHistogram()
                labels[label]["hists-scale-variation"+str(j)][i].Sumw2()


    for year in years:            
        for sample in labels[label]["samples"][year]:
            sample["file"] = ROOT.TFile.Open(sample["filename"])
            sample["tree"] = sample["file"].Get("Events")
            sample["nweightedevents"] = sample["file"].Get("nEventsGenWeighted").GetBinContent(1)



if "wg+jets" in labels:

    labels["wg+jets"]["hists-pass-fiducial"] = {}

    for i in range(len(variables)):    
        labels["wg+jets"]["hists-pass-fiducial"][i] = histogram_models[i].GetHistogram()
        labels["wg+jets"]["hists-pass-fiducial"][i].Sumw2()

    for year in years:            
        for sample in labels["wg+jets"]["samples"][year]:
            sample["nweightedevents_passfiducial"] = sample["file"].Get("nEventsGenWeighted_PassFidSelection").GetBinContent(1)

        if labels["wg+jets"]["syst-scale"]:
            for i in range(0,8):
                labels["wg+jets"]["samples"][year][0]["nweightedevents_qcdscaleweight"+str(i)]=labels["wg+jets"]["samples"][year][0]["file"].Get("nEventsGenWeighted_PassFidSelection_QCDScaleWeight"+str(i)).GetBinContent(1)

                if labels["wg+jets"]["samples"][year][0]["filename"] == options.workdir+"/data/wg/2016/1June2019/wgjets.root":
                    labels["wg+jets"]["samples"][year][0]["nweightedevents_qcdscaleweight"+str(i)] *= 2
                    
        if labels["wg+jets"]["syst-pdf"]:
            for i in range(1,32):
                if (year == "2017" or year == "2018") and options.no_pdf_var_for_2017_and_2018:
                    continue
                labels["wg+jets"]["samples"][year][0]["nweightedevents_pdfweight"+str(i)]=labels["wg+jets"]["samples"][year][0]["file"].Get("nEventsGenWeighted_PassFidSelection_PDFWeight"+str(i)).GetBinContent(1)

                if labels["wg+jets"]["samples"][year][0]["filename"] == options.workdir+"/data/wg/2016/1June2019/wgjets.root":
                    labels["wg+jets"]["samples"][year][0]["nweightedevents_pdfweight"+str(i)] *= 2


#    for year in years:
#        labels["wg+jets"]["samples"][year][0]["nweightedeventspassgenselection"]=labels["wg+jets"]["samples"][year][0]["file"].Get("nWeightedEventsPassGenSelection").GetBinContent(1)
    #labels["wg+jets"]["samples"][year][0]["nweightedeventspassgenselection"]=1

    nweightedeventspassgenselection=0
    nweightedevents = 0
    for year in years:

        lumi = dict_lumi[year]

        nweightedeventspassgenselection+=labels["wg+jets"]["samples"][year][0]["nweightedevents_passfiducial"]*lumi
        nweightedevents+=labels["wg+jets"]["samples"][year][0]["nweightedevents"]*lumi

    fiducial_region_cuts_efficiency = nweightedeventspassgenselection/nweightedevents

data = {}
fake_signal_contamination = {}

wjets = {}
wjets_fake_photon = {}
wjets_fake_photon_2016 = {}
wjets_fake_photon_chiso_2016 = {}
fake_photon = {}
fake_photon_2016 = {}
wjets_2016 = {}
fake_photon_alt = {}
fake_photon_stat_up = {}
fake_lepton = {}
fake_lepton_stat_down = {}
fake_lepton_stat_up = {}
double_fake = {}
double_fake_alt = {}
double_fake_stat_up = {}
e_to_p = {}
e_to_p_non_res = {}
ewdim6 = {}

data["hists"] = []
fake_signal_contamination["hists"] = []
wjets_fake_photon_2016["hists"] = []
wjets_fake_photon_chiso_2016["hists"] = []
wjets_2016["hists"] = []
fake_photon["hists"] = []
fake_photon_2016["hists"] = []
fake_photon_alt["hists"] = []
fake_photon_stat_up["hists"] = []
fake_lepton["hists"] = []
fake_lepton_stat_down["hists"] = []
fake_lepton_stat_up["hists"] = []
double_fake["hists"] = []
double_fake_alt["hists"] = []
double_fake_stat_up["hists"] = []
e_to_p_non_res["hists"] = []
e_to_p["hists"] = []
e_to_p["hists-electron-id-sf-up"] = []
e_to_p["hists-electron-reco-sf-up"] = []
e_to_p["hists-electron-hlt-sf-up"] = []
e_to_p["hists-photon-id-sf-up"] = []
e_to_p["hists-pileup-up"] = []
e_to_p["hists-prefire-up"] = []
e_to_p["hists-jes-up"] = []
e_to_p["hists-jer-up"] = []
ewdim6["hists"] = []

for i in range(len(variables)):
    data["hists"].append(histogram_models[i].GetHistogram())
    wjets_fake_photon_2016["hists"].append(histogram_models[i].GetHistogram())
    wjets_fake_photon_chiso_2016["hists"].append(histogram_models[i].GetHistogram())
    wjets_2016["hists"].append(histogram_models[i].GetHistogram())
    fake_photon["hists"].append(histogram_models[i].GetHistogram())
    fake_photon_2016["hists"].append(histogram_models[i].GetHistogram())
    fake_photon_alt["hists"].append(histogram_models[i].GetHistogram())
    fake_photon_stat_up["hists"].append(histogram_models[i].GetHistogram())
    fake_lepton["hists"].append(histogram_models[i].GetHistogram())
    fake_lepton_stat_up["hists"].append(histogram_models[i].GetHistogram())
    fake_lepton_stat_down["hists"].append(histogram_models[i].GetHistogram())
    double_fake["hists"].append(histogram_models[i].GetHistogram())
    double_fake_alt["hists"].append(histogram_models[i].GetHistogram())
    double_fake_stat_up["hists"].append(histogram_models[i].GetHistogram())
    e_to_p_non_res["hists"].append(histogram_models[i].GetHistogram())
    e_to_p["hists"].append(histogram_models[i].GetHistogram())
    e_to_p["hists-electron-id-sf-up"].append(histogram_models[i].GetHistogram())
    e_to_p["hists-electron-reco-sf-up"].append(histogram_models[i].GetHistogram())
    e_to_p["hists-electron-hlt-sf-up"].append(histogram_models[i].GetHistogram())
    e_to_p["hists-photon-id-sf-up"].append(histogram_models[i].GetHistogram())
    e_to_p["hists-pileup-up"].append(histogram_models[i].GetHistogram())
    e_to_p["hists-prefire-up"].append(histogram_models[i].GetHistogram())
    e_to_p["hists-jes-up"].append(histogram_models[i].GetHistogram())
    e_to_p["hists-jer-up"].append(histogram_models[i].GetHistogram())
    fake_signal_contamination["hists"].append(histogram_models[i].GetHistogram())
    ewdim6["hists"].append(histogram_models[i].GetHistogram())


for i in range(len(variables)):
    data["hists"][i].Sumw2()
    data["hists"][i].SetName("data "+variables[i])
    wjets_fake_photon_2016["hists"][i].Sumw2()
    wjets_fake_photon_chiso_2016["hists"][i].Sumw2()
    wjets_2016["hists"][i].Sumw2()
    fake_photon["hists"][i].Sumw2()
    fake_photon_2016["hists"][i].Sumw2()
    fake_photon["hists"][i].SetName("fake photon "+variables[i])
    fake_photon_2016["hists"][i].SetName("fake photon 2016 "+variables[i])
    fake_lepton["hists"][i].Sumw2()
    fake_lepton_stat_up["hists"][i].Sumw2()
    fake_lepton_stat_down["hists"][i].Sumw2()
    fake_photon_alt["hists"][i].Sumw2()
    fake_photon_stat_up["hists"][i].Sumw2()
    double_fake["hists"][i].Sumw2()
    double_fake_alt["hists"][i].Sumw2()
    double_fake_stat_up["hists"][i].Sumw2()
    e_to_p_non_res["hists"][i].Sumw2()
    e_to_p["hists"][i].Sumw2()
    e_to_p["hists-electron-id-sf-up"][i].Sumw2()
    e_to_p["hists-electron-reco-sf-up"][i].Sumw2()
    e_to_p["hists-electron-hlt-sf-up"][i].Sumw2()
    e_to_p["hists-photon-id-sf-up"][i].Sumw2()
    e_to_p["hists-pileup-up"][i].Sumw2()
    e_to_p["hists-prefire-up"][i].Sumw2()
    e_to_p["hists-jes-up"][i].Sumw2()
    e_to_p["hists-jer-up"][i].Sumw2()
    ewdim6["hists"][i].Sumw2()
    fake_signal_contamination["hists"][i].Sumw2()

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

TFile electron_hlt_2016_sf_file("eff_scale_factors/2016/electron_hlt_sfs_2016.root","read");
TH2D * electron_hlt_2016_sf = (TH2D*) electron_hlt_2016_sf_file.Get("hlt_sfs_etapt");

TFile electron_hlt_2017_sf_file("eff_scale_factors/2017/electron_hlt_sfs_2017.root","read");
TH2D * electron_hlt_2017_sf = (TH2D*)electron_hlt_2017_sf_file.Get("hlt_sfs_etapt");

TFile electron_hlt_2018_sf_file("eff_scale_factors/2018/electron_hlt_sfs_2018.root" ,"read");
TH2D * electron_hlt_2018_sf = (TH2D*)electron_hlt_2018_sf_file.Get("hlt_sfs_etapt");

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

TFile muon_hlt_2016_sf_file("eff_scale_factors/2016/EfficienciesStudies_2016_trigger_EfficienciesAndSF_RunGtoH.root","read");
TH2F * muon_hlt_2016_sf = (TH2F*) muon_hlt_2016_sf_file.Get("IsoMu24_OR_IsoTkMu24_PtEtaBins/abseta_pt_ratio");

TFile muon_hlt_2017_sf_file("eff_scale_factors/2017/EfficienciesAndSF_RunBtoF_Nov17Nov2017.root","read");
TH2F * muon_hlt_2017_sf = (TH2F*) muon_hlt_2017_sf_file.Get("IsoMu27_PtEtaBins/abseta_pt_ratio");

TFile muon_hlt_2018_sf_file("eff_scale_factors/2018/EfficienciesStudies_2018_trigger_EfficienciesAndSF_2018Data_BeforeMuonHLTUpdate.root","read");
TH2F * muon_hlt_2018_sf = (TH2F*) muon_hlt_2018_sf_file.Get("IsoMu24_PtEtaBins/abseta_pt_ratio");


float electron_efficiency_scale_factor(float pt, float eta, string year,bool id_err_up=false, bool reco_err_up=false, bool hlt_err_up=false) {

    TH2F * electron_reco_sf = 0;
    TH2F * electron_id_sf = 0;
    TH2D * electron_hlt_sf = 0;

    if (year == "2016") {
        electron_reco_sf = electron_reco_2016_sf;
        electron_id_sf = electron_id_2016_sf;
        electron_hlt_sf = electron_hlt_2016_sf;
    }
    else if (year == "2017"){
        electron_reco_sf = electron_reco_2017_sf;
        electron_id_sf = electron_id_2017_sf;
        electron_hlt_sf = electron_hlt_2017_sf;
    }
    else if (year == "2018") {
        electron_reco_sf = electron_reco_2018_sf;
        electron_id_sf = electron_id_2018_sf;
        electron_hlt_sf = electron_hlt_2018_sf;
    }
    else
        assert(0);

    int electron_id_sf_xaxisbin = -1;
    int electron_id_sf_yaxisbin = -1;

    if (year == "2016") {    
        electron_id_sf_xaxisbin = electron_id_sf->GetXaxis()->FindFixBin(eta);
        electron_id_sf_yaxisbin = electron_id_sf->GetYaxis()->FindFixBin(TMath::Min(pt,float(electron_id_sf->GetYaxis()->GetBinCenter(electron_id_sf->GetNbinsY()))));
    }
    else if (year == "2017") {
        electron_id_sf_xaxisbin = electron_id_sf->GetXaxis()->FindFixBin(eta);
        electron_id_sf_yaxisbin = electron_id_sf->GetYaxis()->FindFixBin(TMath::Min(pt,float(electron_id_sf->GetYaxis()->GetBinCenter(electron_id_sf->GetNbinsY()))));
    }
    else if (year == "2018") {
        electron_id_sf_xaxisbin = electron_id_sf->GetXaxis()->FindFixBin(eta);
        electron_id_sf_yaxisbin = electron_id_sf->GetYaxis()->FindFixBin(TMath::Min(pt,float(electron_id_sf->GetYaxis()->GetBinCenter(electron_id_sf->GetNbinsY()))));
    }
    else assert(0);

    int electron_hlt_sf_xaxisbin = -1;
    int electron_hlt_sf_yaxisbin = -1;

    if (year == "2016") {    
        electron_hlt_sf_xaxisbin = electron_hlt_sf->GetXaxis()->FindFixBin(eta);
        electron_hlt_sf_yaxisbin = electron_hlt_sf->GetYaxis()->FindFixBin(TMath::Min(pt,float(electron_hlt_sf->GetYaxis()->GetBinCenter(electron_hlt_sf->GetNbinsY()))));
    }
    else if (year == "2017") {
        electron_hlt_sf_xaxisbin = electron_hlt_sf->GetXaxis()->FindFixBin(eta);
        electron_hlt_sf_yaxisbin = electron_hlt_sf->GetYaxis()->FindFixBin(TMath::Min(pt,float(electron_hlt_sf->GetYaxis()->GetBinCenter(electron_hlt_sf->GetNbinsY()))));
    }
    else if (year == "2018") {
        electron_hlt_sf_xaxisbin = electron_hlt_sf->GetXaxis()->FindFixBin(eta);
        electron_hlt_sf_yaxisbin = electron_hlt_sf->GetYaxis()->FindFixBin(TMath::Min(pt,float(electron_hlt_sf->GetYaxis()->GetBinCenter(electron_hlt_sf->GetNbinsY()))));
    }
    else assert(0);


    float sf_id = electron_id_sf->GetBinContent(electron_id_sf_xaxisbin,electron_id_sf_yaxisbin); 
    if (id_err_up) sf_id += electron_id_sf->GetBinError(electron_id_sf_xaxisbin,electron_id_sf_yaxisbin) ;

    //the reco 2D histogram is really a 1D histogram
    float sf_reco=electron_reco_sf->GetBinContent(electron_reco_sf->GetXaxis()->FindFixBin(eta),1);
    if (reco_err_up) sf_reco+=electron_reco_sf->GetBinError(electron_reco_sf->GetXaxis()->FindFixBin(eta),1);

    float sf_hlt = electron_hlt_sf->GetBinContent(electron_hlt_sf_xaxisbin,electron_hlt_sf_yaxisbin); 
    if (hlt_err_up) sf_hlt += electron_hlt_sf->GetBinError(electron_hlt_sf_xaxisbin,electron_hlt_sf_yaxisbin) ;

    return sf_id*sf_reco*sf_hlt;
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

float muon_efficiency_scale_factor(float pt,float eta,string year,bool iso_err_up=false,bool id_err_up=false, bool hlt_err_up=false) {

    TH2D * muon_iso_sf = 0;
    TH2D * muon_id_sf = 0;
    TH2F * muon_hlt_sf = 0;

    if (year == "2016") {
        muon_iso_sf = muon_iso_2016_sf;
        muon_id_sf = muon_id_2016_sf;
        muon_hlt_sf = muon_hlt_2016_sf;
    }
    else if (year == "2017") {
        muon_iso_sf = muon_iso_2017_sf;
        muon_id_sf = muon_id_2017_sf;
        muon_hlt_sf = muon_hlt_2017_sf;
    }
    else if (year == "2018"){
        muon_iso_sf = muon_iso_2018_sf;
        muon_id_sf = muon_id_2018_sf;
        muon_hlt_sf = muon_hlt_2018_sf;
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

    int muon_hlt_sf_xaxisbin = -1;
    int muon_hlt_sf_yaxisbin = -1;

    if (year == "2016") {    
        muon_hlt_sf_xaxisbin = muon_hlt_sf->GetXaxis()->FindFixBin(abs(eta));
        muon_hlt_sf_yaxisbin = muon_hlt_sf->GetYaxis()->FindFixBin(TMath::Min(pt,float(muon_hlt_sf->GetYaxis()->GetBinCenter(muon_hlt_sf->GetNbinsY()))));
    }
    else if (year == "2017") {
        muon_hlt_sf_xaxisbin = muon_hlt_sf->GetXaxis()->FindFixBin(abs(eta));
        muon_hlt_sf_yaxisbin = muon_hlt_sf->GetYaxis()->FindFixBin(TMath::Min(pt,float(muon_hlt_sf->GetYaxis()->GetBinCenter(muon_hlt_sf->GetNbinsY()))));
    }
    else if (year == "2018") {
        muon_hlt_sf_xaxisbin = muon_hlt_sf->GetXaxis()->FindFixBin(abs(eta));
        muon_hlt_sf_yaxisbin = muon_hlt_sf->GetYaxis()->FindFixBin(TMath::Min(pt,float(muon_hlt_sf->GetYaxis()->GetBinCenter(muon_hlt_sf->GetNbinsY()))));
    }
    else assert(0);

    float iso_sf = muon_iso_sf->GetBinContent(muon_iso_sf_xaxisbin,muon_iso_sf_yaxisbin);

    if (iso_err_up) iso_sf += muon_iso_sf->GetBinError(muon_iso_sf_xaxisbin,muon_iso_sf_yaxisbin);

    float id_sf = muon_id_sf->GetBinContent(muon_id_sf_xaxisbin,muon_id_sf_yaxisbin); 
    
    if (id_err_up) id_sf += muon_id_sf->GetBinError(muon_id_sf_xaxisbin,muon_id_sf_yaxisbin) ;

    float hlt_sf = muon_hlt_sf->GetBinContent(muon_hlt_sf_xaxisbin,muon_hlt_sf_yaxisbin); 
    
    if (hlt_err_up) hlt_sf += muon_hlt_sf->GetBinError(muon_hlt_sf_xaxisbin,muon_hlt_sf_yaxisbin) ;

    return iso_sf * id_sf * hlt_sf;

}

'''

fake_lepton_weight_cpp = '''

TFile muon_2016_file("fake_lepton_weights/muon_2016_frs.root");
TFile electron_2016_file("fake_lepton_weights/electron_2016_frs.root");

TFile muon_2017_file("fake_lepton_weights/muon_2017_frs.root");
TFile electron_2017_file("fake_lepton_weights/electron_2017_frs.root");

TFile muon_2018_file("fake_lepton_weights/muon_2018_frs.root");
TFile electron_2018_file("fake_lepton_weights/electron_2018_frs.root");

TH2D * muon_2016_fr_hist = (TH2D*)muon_2016_file.Get("muon_frs");
TH2D * electron_2016_fr_hist = (TH2D*)electron_2016_file.Get("electron_frs");
TH2D * muon_2017_fr_hist = (TH2D*)muon_2017_file.Get("muon_frs");
TH2D * electron_2017_fr_hist = (TH2D*)electron_2017_file.Get("electron_frs");
TH2D * muon_2018_fr_hist = (TH2D*)muon_2018_file.Get("muon_frs");
TH2D * electron_2018_fr_hist = (TH2D*)electron_2018_file.Get("electron_frs");

float get_fake_lepton_weight(float eta, float pt, string year, int lepton_pdg_id, string syst = "nominal")
{
    TH2D * fr_hist = 0;

    if (year == "2016" && abs(lepton_pdg_id) == 13) fr_hist = muon_2016_fr_hist;
    else if (year == "2016" && abs(lepton_pdg_id) == 11) fr_hist = electron_2016_fr_hist;
    else if (year == "2017" && abs(lepton_pdg_id) == 13) fr_hist = muon_2017_fr_hist;
    else if (year == "2017" && abs(lepton_pdg_id) == 11) fr_hist = electron_2017_fr_hist;
    else if (year == "2018" && abs(lepton_pdg_id) == 13) fr_hist = muon_2018_fr_hist;
    else if (year == "2018" && abs(lepton_pdg_id) == 11) fr_hist = electron_2018_fr_hist;
    else assert(0);

    float myeta  = TMath::Min(abs(eta),float(2.4999));
    float mypt  = TMath::Min(pt,float(44.999));

    int etabin = fr_hist->GetXaxis()->FindFixBin(myeta);
    int ptbin = fr_hist->GetYaxis()->FindFixBin(mypt);

    float prob = fr_hist->GetBinContent(etabin,ptbin);

    if (syst == "up") prob += fr_hist->GetBinError(etabin,ptbin);
    else if (syst == "down") prob -= fr_hist->GetBinError(etabin,ptbin);
    else assert(syst == "nominal");

    return prob/(1-prob);
}
'''

fake_photon_weight_cpp = '''

float get_fake_photon_weight(float eta, float pt, string year, int lepton_pdg_id, string version = "nominal") {

assert(version == "nominal" || version == "alt" || version == "stat_up" || version == "wjets" || version == "wjets_chiso"); 

if (version == "wjets") { 
    assert(year == "2016");
    float fr = 0;
    if (year == "2016") {
        if (abs(eta) < 1.4442) {
            if (pt < 25 and pt > 20) fr = 0.6469175340272219;
            else if (pt < 30 and pt > 25) fr = 0.7593930635838149;
            else if (pt < 40 and pt > 30) fr = 0.9052396878483837;
            else if (pt < 50 and pt > 40) fr = 0.7128205128205127;
            else if (pt > 50) fr = 0.5080459770114942;
            else assert(0); 
        }
        else if (1.566 < abs(eta) && abs(eta) < 2.5) {
           if (pt < 25 and pt > 20) fr = 0.9821810406272273;
               else if (pt < 30 and pt > 25) fr = 1.160148975791434;
               else if (pt < 40 and pt > 30) fr = 1.0594965675057209;
               else if (pt < 50 and pt > 40) fr = 1.2920353982300883;
               else if (pt > 50) fr = 1.2293577981651373;
               else assert(0); 
           }
        }
        return fr;
    }
else if (version == "wjets_chiso") {
    assert(year == "2016");
    float fr = 0;
    if (year == "2016") {
        if (abs(eta) < 1.4442) {
            if (pt < 25 and pt > 20) fr = 2.139452780229479;
            else if (pt < 30 and pt > 25) fr = 1.7089430894308941;
            else if (pt < 40 and pt > 30) fr = 1.4072790294627382;
            else if (pt < 50 and pt > 40) fr = 1.053030303030303;
            else if (pt > 50) fr = 0.8095238095238096;
            else assert(0); 
    
           }
           else if (1.566 < abs(eta) && abs(eta) < 2.5) {
               if (pt < 25 and pt > 20) fr = 3.8277777777777775;
               else if (pt < 30 and pt > 25) fr = 2.708695652173913;
               else if (pt < 40 and pt > 30) fr = 2.292079207920792;
               else if (pt < 50 and pt > 40) fr = 2.1470588235294117;
               else if (pt > 50) fr = 2.5769230769230766;
               else assert(0); 
           }
        }
        return fr;
    }
else if (version == "nominal" || version == "alt" || version == "stat_up") { //based on inverting chiso and making the maximum 1.75*chiso_cut
    float fr = 0;
    if (year == "2016") {
       if (abs(eta) < 1.4442) {
          if (pt < 25 and pt > 20) fr = 0.6996237332067621;
          else if (pt < 30 and pt > 25) fr = 0.7485724858910313;
          else if (pt < 40 and pt > 30) fr = 0.6920954897858362;
          else if (pt < 50 and pt > 40) fr = 0.5922363985857421;
          else if (pt > 50) fr = 0.4151116840422024;
          else assert(0); 
    
       }
       else if (1.566 < abs(eta) && abs(eta) < 2.5) {
          if (pt < 25 and pt > 20) fr = 0.9248844370602675;
          else if (pt < 30 and pt > 25) fr = 0.9799675969963608;
          else if (pt < 40 and pt > 30) fr = 0.9750818843293853;
          else if (pt < 50 and pt > 40) fr = 0.937879263758023;
          else if (pt > 50) fr = 0.9580822239127585;
          else assert(0); 
       }
    }
    else if (year == "2017") {
       if (abs(eta) < 1.4442) {
          if (pt < 25 and pt > 20) fr = 0.6912680790821342;
          else if (pt < 30 and pt > 25) fr = 0.7636732062430018;
          else if (pt < 40 and pt > 30) fr = 0.7309187507758684;
          else if (pt < 50 and pt > 40) fr = 0.6559368305211164;
          else if (pt > 50) fr = 0.5068425857427465;
          else assert(0); 
    
       }
       else if (1.566 < abs(eta) && abs(eta) < 2.5) {
          if (pt < 25 and pt > 20) fr = 0.3147229931595173;
          else if (pt < 30 and pt > 25) fr = 0.34277057433872954;
          else if (pt < 40 and pt > 30) fr = 0.34959057399376964;
          else if (pt < 50 and pt > 40) fr = 0.4001123746683101;
          else if (pt > 50) fr = 0.5109029075333011;
          else assert(0); 
       }
    }
    else if (year == "2018") {
       if (abs(eta) < 1.4442) {
          if (pt < 25 and pt > 20) fr =  0.6819628126916278;
          else if (pt < 30 and pt > 25) fr = 0.7738571901458522;
          else if (pt < 40 and pt > 30) fr = 0.7516333386056144;
          else if (pt < 50 and pt > 40) fr = 0.6950256916933786;
          else if (pt > 50) fr = 0.504158202340239;
          else assert(0); 
    
       }
       else if (1.566 < abs(eta) && abs(eta) < 2.5) {
          if (pt < 25 and pt > 20) fr =  0.27489785614816215;
          else if (pt < 30 and pt > 25) fr = 0.31779777996179676;
          else if (pt < 40 and pt > 30) fr = 0.33081812493411455;
          else if (pt < 50 and pt > 40) fr = 0.35671632932371405;
          else if (pt > 50) fr = 0.49287015359051706;
          else assert(0); 
       }
    }

    if (version == "alt") {
       if (year == "2016") {
          if (abs(eta) < 1.4442) {
             if (pt < 25 and pt > 20) fr += 0.6469175340272219 -  0.6808966653040407;
             else if (pt < 30 and pt > 25) fr += 0.7593930635838149 -  0.7624786257622868;
             else if (pt < 40 and pt > 30) fr += 0.9052396878483837 - 0.7427103452313788;
             else if (pt < 50 and pt > 40) fr += 0.7128205128205127 -  0.6443786091779561;
             else if (pt > 50) fr += 0.5080459770114942 - 0.4012017084603665;
             else assert(0); 
    
          }
          else if (1.566 < abs(eta) && abs(eta) < 2.5) {
             if (pt < 25 and pt > 20) fr += 0.9821810406272273 -  0.9593621632637661;
             else if (pt < 30 and pt > 25) fr += 1.160148975791434 -  0.9402109983117282;
             else if (pt < 40 and pt > 30) fr += 1.0594965675057209 - 0.8076708282273575;
             else if (pt < 50 and pt > 40) fr += 1.2920353982300883 - 1.2271914169232672;
             else if (pt > 50) fr += 1.2293577981651373  - 0.9377974387415269;
             else assert(0); 
          }
       }
       else if (year == "2017") {
          if (abs(eta) < 1.4442) {
             if (pt < 25 and pt > 20) fr += 0.5920017017655818 -  0.675219301111022;
             else if (pt < 30 and pt > 25) fr += 0.7620164126611957 -  0.7880502803690924;
             else if (pt < 40 and pt > 30) fr += 0.8587786259541983 - 0.8149971396299441; 
             else if (pt < 50 and pt > 40) fr += 0.7945945945945946 - 0.732169348128166;
             else if (pt > 50) fr += 0.5646551724137931 - 0.5889482915913384;
             else assert(0); 
          }
          else if (1.566 < abs(eta) && abs(eta) < 2.5) {
             if (pt < 25 and pt > 20) fr += 0.5351190476190476 -  0.3336229060031224;
             else if (pt < 30 and pt > 25) fr += 0.7174603174603175 -  0.4214485303045893;
             else if (pt < 40 and pt > 30) fr += 0.6980198019801981 - 0.44808235568211063;
             else if (pt < 50 and pt > 40) fr += 0.746031746031746 - 0.4882394061692232;
             else if (pt > 50) fr += 0.6575342465753424 - 0.7417937101120567;
             else assert(0); 
          }
       }
       else if (year == "2018") {
          if (abs(eta) < 1.4442) {
             if (pt < 25 and pt > 20) fr += 0.6434456928838951 - 0.7508905741815809;
             else if (pt < 30 and pt > 25) fr += 0.6980392156862745 - 0.8258283193385701;
             else if (pt < 40 and pt > 30) fr += 0.8702064896755163 - 0.8435371457514238;
             else if (pt < 50 and pt > 40) fr += 0.9174311926605504 -  0.7456986592354332;
             else if (pt > 50) fr += 0.6343283582089553 - 0.4698553383698952;
             else assert(0); 
          }
          else if (1.566 < abs(eta) && abs(eta) < 2.5) {
             if (pt < 25 and pt > 20) fr += 0.5732368896925858 - 0.34631002339070077;
             else if (pt < 30 and pt > 25) fr += 0.8591549295774648 - 0.3435483305230785;
             else if (pt < 40 and pt > 30) fr += 0.8108108108108107 - 0.409059955258932;
             else if (pt < 50 and pt > 40) fr += 0.5967741935483871 - 0.4055865165305403;
             else if (pt > 50) fr += 0.9268292682926829 - 0.4696040830060756;
             else assert(0); 
          }
       }
    }

    if (version == "stat_up") {
       if (year == "2016") {
          if (abs(eta) < 1.4442) {
             if (pt < 25 and pt > 20) fr += 0.002937265704094981;
             else if (pt < 30 and pt > 25) fr += 0.0062805701638771845;
             else if (pt < 40 and pt > 30) fr += 0.006477726168950861;
             else if (pt < 50 and pt > 40) fr += 0.0087970999952064;
             else if (pt > 50) fr += 0.005442704584429666;
             else assert(0); 
    
          }
          else if (1.566 < abs(eta) && abs(eta) < 2.5) {
             if (pt < 25 and pt > 20) fr += 0.0064449696265627115;
             else if (pt < 30 and pt > 25) fr += 0.01258402077183808;
             else if (pt < 40 and pt > 30) fr += 0.014621685284402344;
             else if (pt < 50 and pt > 40) fr += 0.023745888823496042;
             else if (pt > 50) fr += 0.025855780798136833;
             else assert(0); 
          }
       }
       else if (year == "2017") {
          if (abs(eta) < 1.4442) {
             if (pt < 25 and pt > 20) fr += 0.6912680790821342;
             else if (pt < 30 and pt > 25) fr += 0.7636732062430018;
             else if (pt < 40 and pt > 30) fr += 0.7309187507758684;
             else if (pt < 50 and pt > 40) fr += 0.6559368305211164;
             else if (pt > 50) fr += 0.5068425857427465;
             else assert(0); 
          }
          else if (1.566 < abs(eta) && abs(eta) < 2.5) {
             if (pt < 25 and pt > 20) fr += 0.3147229931595173;
             else if (pt < 30 and pt > 25) fr += 0.34277057433872954;
             else if (pt < 40 and pt > 30) fr += 0.34959057399376964;
             else if (pt < 50 and pt > 40) fr += 0.4001123746683101;
             else if (pt > 50) fr += 0.5109029075333011;
             else assert(0); 
          }
       }
       else if (year == "2018") {
          if (abs(eta) < 1.4442) {
             if (pt < 25 and pt > 20) fr += 0.0024140690750868183;
             else if (pt < 30 and pt > 25) fr += 0.005184544256765383;
             else if (pt < 40 and pt > 30) fr += 0.005868144318298048;
             else if (pt < 50 and pt > 40) fr += 0.008224769860031768;
             else if (pt > 50) fr += 0.005667933573402517;
             else assert(0); 
          }
          else if (1.566 < abs(eta) && abs(eta) < 2.5) {
             if (pt < 25 and pt > 20) fr += 0.0019240540418093948;
             else if (pt < 30 and pt > 25) fr += 0.0038455484020956843;
             else if (pt < 40 and pt > 30) fr += 0.004759983282437974;
             else if (pt < 50 and pt > 40) fr += 0.00822110783712988;
             else if (pt > 50) fr += 0.011315829843225643;
             else assert(0); 
          }
       }
    }


    return fr;
} else {

assert(0);

}

return 0;  

}
'''

ROOT.gInterpreter.Declare(fake_lepton_weight_cpp)
ROOT.gInterpreter.Declare(fake_photon_weight_cpp)
ROOT.gInterpreter.Declare(eff_scale_factor_cpp)

#ewdim6_index = 31
#ewdim6_index = 30
ewdim6_index = 0

if options.ewdim6:

    sm_lhe_weight = 0

#    sm_lhe_weight_hist = ROOT.TH1D('', '', n_photon_pt_bins, binning_photon_pt )

#    sm_hist = ROOT.TH1D('', '', n_photon_pt_bins, binning_photon_pt )

    sm_lhe_weight_hist = histogram_models[ewdim6_index].GetHistogram()

    sm_hist = histogram_models[ewdim6_index].GetHistogram()

    cwww_reweights = [0,0+1,0+2,0+3,0+4,0+5,0+6]

    #cwww_coefficients = [0.0, 10.0,-10.0,20.0,-20.0,-30.0,30.0]

    cwww_coefficients = [0.0, 1.0,-1.0,2.0,-2.0,-3.0,3.0]

    cwww_hists = []

    cw_reweights = [0,0+7,0+8,0+9,0+10,0+11,0+12]

    #cw_coefficients = [0.0, 80.0,-80.0,160.0,-160.0,240.0,-240.0]

#    cw_coefficients = [0.0, 17.0,-17.0,34.0,-34.0,51.0,-51.0]

    cw_coefficients = [0.0, 51.0,-51.0,34.0,-34.0,17.0,-17.0]

    cw_hists = []

    cb_reweights = [0,0+13,0+14,0+15,0+16,0+17,0+18]

    #cb_coefficients = [0.0, 80.0,-80.0,160.0,-160.0,240.0,-240.0]

#    cb_coefficients = [0.0, 17.0,-17.0,34.0,-34.0,51.0,-51.0]

    cb_coefficients = [0.0, 51.0,-51.0,34.0,-34.0,17.0,-17.0]

    cb_hists = []

    cpwww_reweights = [0,0+19,0+20,0+21,0+22,0+23,0+24]

    #cpwww_coefficients = [0.0, 4.0,-4.0,8.0,-8.0,12.0,-12.0]

#    cpwww_coefficients = [0.0, 0.5,-0.5,1.0,-1.0,1.5,-1.5]

    cpwww_coefficients = [0.0, 1.5,-1.5,1.0,-1.0,0.5,-0.5]

    cpwww_hists = []

    cpw_reweights = [0,0+25,0+26,0+27,0+28,0+29,0+30]

    #cpw_coefficients = [0.0, 40.0,-40.0,80.0,-80.0,120.0,-120.0]

    cpw_coefficients = [0.0, 24.0,-24.0,16.0,-16.0,8.0,-8.0]

    cpw_hists = []

    for i in range(0,len(cwww_reweights)):
        cwww_hists.append(ROOT.TH1D('', '', n_photon_pt_bins, binning_photon_pt ))

    for i in range(0,len(cw_reweights)):
        cw_hists.append(ROOT.TH1D('', '', n_photon_pt_bins, binning_photon_pt ))

    for i in range(0,len(cb_reweights)):
        cb_hists.append(ROOT.TH1D('', '', n_photon_pt_bins, binning_photon_pt ))

    for i in range(0,len(cpwww_reweights)):
        cpwww_hists.append(ROOT.TH1D('', '', n_photon_pt_bins, binning_photon_pt ))

    for i in range(0,len(cpw_reweights)):
        cpw_hists.append(ROOT.TH1D('', '', n_photon_pt_bins, binning_photon_pt ))

    gen_matching_string = "(is_lepton_real == 1 && (photon_gen_matching == 4 || photon_gen_matching == 5 || photon_gen_matching == 6))"

    for year in years:    

        lumi = dict_lumi[year]

        rdf=ROOT.RDataFrame("Events",labels["wg+jets"]["samples"][year][0]["filename"])

        rinterface = rdf.Filter(get_filter_string(year) + " && " + gen_matching_string)

        rinterface = rinterface.Define("xs_weight",str(labels["wg+jets"]["samples"][year][0]["xs"]*1000*lumi/labels["wg+jets"]["samples"][year][0]["nweightedevents"]) + "*gen_weight/abs(gen_weight)")  

        rinterface = rinterface.Define("weight","xs_weight*photon_efficiency_scale_factor(photon_pt,photon_eta,\""+year+"\")*(abs(lepton_pdg_id) == 13 ? muon_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\") : electron_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\"))")    

        for variable_definition in variable_definitions:
            rinterface = rinterface.Define(variable_definition[0],variable_definition[1])

        rresultptr = rinterface.Histo1D(histogram_models[ewdim6_index],variables[ewdim6_index],"weight")

        sm_hist.Add(rresultptr.GetValue())

    sm_hist.Print("all")

    for year in years:

        lumi = dict_lumi[year]

        rdf=ROOT.RDataFrame("Events",ewdim6_samples[year][0]["filename"])

        rinterface = rdf.Filter(get_filter_string(year) + " && " + gen_matching_string)

        rinterface = rinterface.Define("xs_weight",str(ewdim6_samples[year][0]["xs"]*1000*lumi/ewdim6_samples[year][0]["nweightedevents"]) + "*gen_weight/abs(gen_weight)")  

        rinterface = rinterface.Define("weight","xs_weight*photon_efficiency_scale_factor(photon_pt,photon_eta,\""+year+"\")*(abs(lepton_pdg_id) == 13 ? muon_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\") : electron_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\"))")    

        for variable_definition in variable_definitions:
            rinterface = rinterface.Define(variable_definition[0],variable_definition[1])

        rresultptrs_cwww = []
        rresultptrs_cw = []
        rresultptrs_cb = []
        rresultptrs_cpwww = []
        rresultptrs_cpw = []

        for i in range(len(cwww_reweights)):
            rinterface = rinterface.Define("cwww_weight_"+str(i),"weight*LHEReweightingWeight["+str(cwww_reweights[i])+"]")
            rresultptrs_cwww.append(rinterface.Histo1D(histogram_models[0],variables[0],"cwww_weight_"+str(i)))
            
        for i in range(len(cw_reweights)):
            rinterface = rinterface.Define("cw_weight_"+str(i),"weight*LHEReweightingWeight["+str(cw_reweights[i])+"]")
            rresultptrs_cw.append(rinterface.Histo1D(histogram_models[0],variables[0],"cw_weight_"+str(i)))

        for i in range(len(cb_reweights)):
            rinterface = rinterface.Define("cb_weight_"+str(i),"weight*LHEReweightingWeight["+str(cb_reweights[i])+"]")
            rresultptrs_cb.append(rinterface.Histo1D(histogram_models[0],variables[0],"cb_weight_"+str(i)))

        for i in range(len(cpwww_reweights)):
            rinterface = rinterface.Define("cpwww_weight_"+str(i),"weight*LHEReweightingWeight["+str(cpwww_reweights[i])+"]")
            rresultptrs_cpwww.append(rinterface.Histo1D(histogram_models[0],variables[0],"cpwww_weight_"+str(i)))

        for i in range(len(cpw_reweights)):
            rinterface = rinterface.Define("cpw_weight_"+str(i),"weight*LHEReweightingWeight["+str(cpw_reweights[i])+"]")
            rresultptrs_cpw.append(rinterface.Histo1D(histogram_models[0],variables[0],"cpw_weight_"+str(i)))

        rinterface = rinterface.Define("sm_weight","weight*LHEReweightingWeight["+str(sm_lhe_weight)+"]")
        rresultptr_sm = rinterface.Histo1D(histogram_models[ewdim6_index],variables[ewdim6_index],"sm_weight")



        for i in range(len(cwww_reweights)):
            cwww_hists[i].Add(rresultptrs_cwww[i].GetValue())

        for i in range(len(cw_reweights)):
            cw_hists[i].Add(rresultptrs_cw[i].GetValue())

        for i in range(len(cb_reweights)):
            cb_hists[i].Add(rresultptrs_cb[i].GetValue())

        for i in range(len(cpwww_reweights)):
            cpwww_hists[i].Add(rresultptrs_cpwww[i].GetValue())

        for i in range(len(cpw_reweights)):
            cpw_hists[i].Add(rresultptrs_cpw[i].GetValue())

        sm_lhe_weight_hist.Add(rresultptr_sm.GetValue())

    cwww_scaling_outfile = ROOT.TFile("cwww_scaling.root",'recreate')
    cw_scaling_outfile = ROOT.TFile("cw_scaling.root",'recreate')
    cb_scaling_outfile = ROOT.TFile("cb_scaling.root",'recreate')
    cpwww_scaling_outfile = ROOT.TFile("cpwww_scaling.root",'recreate')
    cpw_scaling_outfile = ROOT.TFile("cpw_scaling.root",'recreate')

    cwww_hist_max = max(cwww_coefficients) + (max(cwww_coefficients) - min(cwww_coefficients))/(len(cwww_coefficients)-1)/2
    cwww_hist_min = min(cwww_coefficients) - (max(cwww_coefficients) - min(cwww_coefficients))/(len(cwww_coefficients)-1)/2

    cw_hist_max = max(cw_coefficients) + (max(cw_coefficients) - min(cw_coefficients))/(len(cw_coefficients)-1)/2
    cw_hist_min = min(cw_coefficients) - (max(cw_coefficients) - min(cw_coefficients))/(len(cw_coefficients)-1)/2

    cb_hist_max = max(cb_coefficients) + (max(cb_coefficients) - min(cb_coefficients))/(len(cb_coefficients)-1)/2
    cb_hist_min = min(cb_coefficients) - (max(cb_coefficients) - min(cb_coefficients))/(len(cb_coefficients)-1)/2

    cpwww_hist_max = max(cpwww_coefficients) + (max(cpwww_coefficients) - min(cpwww_coefficients))/(len(cpwww_coefficients)-1)/2
    cpwww_hist_min = min(cpwww_coefficients) - (max(cpwww_coefficients) - min(cpwww_coefficients))/(len(cpwww_coefficients)-1)/2

    cpw_hist_max = max(cpw_coefficients) + (max(cpw_coefficients) - min(cpw_coefficients))/(len(cpw_coefficients)-1)/2
    cpw_hist_min = min(cpw_coefficients) - (max(cpw_coefficients) - min(cpw_coefficients))/(len(cpw_coefficients)-1)/2

    sm_lhe_weight_hist.Print("all")

    c = ROOT.TCanvas("c", "c",5,50,500,500)
    sm_hist.SetLineColor(ROOT.kRed)
    sm_lhe_weight_hist.SetLineColor(ROOT.kBlue)
    sm_hist.SetLineWidth(2)
    sm_lhe_weight_hist.SetLineWidth(2)
    sm_hist.SetMaximum(1.55*max(sm_hist.GetMaximum(),sm_lhe_weight_hist.GetMaximum()))
    sm_hist.Draw()
    sm_lhe_weight_hist.Draw("same")
    s=str(totallumi)+" fb^{-1} (13 TeV)"
    lumilabel = ROOT.TLatex (0.95, 0.93, s)
    lumilabel.SetNDC ()
    lumilabel.SetTextAlign (30)
    lumilabel.SetTextFont (42)
    lumilabel.SetTextSize (0.040)
    lumilabel.Draw("same")
    set_axis_fonts(sm_hist,"x",getXaxisLabel(variables[ewdim6_index]))
    j=0
    draw_legend(xpositions[j]-0.05,0.84 - ypositions[j]*yoffset,sm_hist,"SM unweighted","l")
    j=j+1
    draw_legend(xpositions[j]-0.05,0.84 - ypositions[j]*yoffset,sm_lhe_weight_hist,"SM reweighted","l")
    c.SaveAs(options.outputdir + "/" + "sm_reweighting.png")

    cwww_scaling_hists = {}
    cw_scaling_hists = {}
    cb_scaling_hists = {}
    cpw_scaling_hists = {}
    cpwww_scaling_hists = {}

    for i in range(1,cwww_hists[0].GetNbinsX()+1):
        ROOT.gROOT.cd() #so that the histogram created in the next line is not put in a file that is closed
        cwww_scaling_hists[i]=ROOT.TH1D("ewdim6_scaling_bin_"+str(i),"ewdim6_scaling_bin_"+str(i),len(cwww_coefficients),cwww_hist_min,cwww_hist_max)

        for j in range(0,len(cwww_hists)):
            assert(sm_lhe_weight_hist.GetBinContent(i) > 0)

            cwww_scaling_hists[i].SetBinContent(cwww_scaling_hists[i].GetXaxis().FindFixBin(cwww_coefficients[j]), cwww_hists[j].GetBinContent(i)/sm_lhe_weight_hist.GetBinContent(i))
        
        cwww_scaling_outfile.cd()
        cwww_scaling_hists[i].Write()

    cwww_scaling_outfile.Close()

    for i in range(1,cw_hists[0].GetNbinsX()+1):
        cw_scaling_hists[i]=ROOT.TH1D("ewdim6_scaling_bin_"+str(i),"ewdim6_scaling_bin_"+str(i),len(cw_coefficients),cw_hist_min,cw_hist_max)

        for j in range(0,len(cw_hists)):
            assert(sm_lhe_weight_hist.GetBinContent(i) > 0)

            cw_scaling_hists[i].SetBinContent(cw_scaling_hists[i].GetXaxis().FindFixBin(cw_coefficients[j]), cw_hists[j].GetBinContent(i)/sm_lhe_weight_hist.GetBinContent(i))
            
        cw_scaling_outfile.cd()
        cw_scaling_hists[i].Write()

    cw_scaling_outfile.Close()

    for i in range(1,cb_hists[0].GetNbinsX()+1):
        ROOT.gROOT.cd() #so that the histogram created in the next line is not put in a file that is closed
        cb_scaling_hists[i]=ROOT.TH1D("ewdim6_scaling_bin_"+str(i),"ewdim6_scaling_bin_"+str(i),len(cb_coefficients),cb_hist_min,cb_hist_max);

        for j in range(0,len(cb_hists)):
            assert(sm_lhe_weight_hist.GetBinContent(i) > 0)

            cb_scaling_hists[i].SetBinContent(cb_scaling_hists[i].GetXaxis().FindFixBin(cb_coefficients[j]), cb_hists[j].GetBinContent(i)/sm_lhe_weight_hist.GetBinContent(i))
        
        cb_scaling_outfile.cd()
        cb_scaling_hists[i].Write()

    cb_scaling_outfile.Close()

    for i in range(1,cpwww_hists[0].GetNbinsX()+1):
        cpwww_scaling_hists[i]=ROOT.TH1D("ewdim6_scaling_bin_"+str(i),"ewdim6_scaling_bin_"+str(i),len(cpwww_coefficients),cpwww_hist_min,cpwww_hist_max);

        for j in range(0,len(cpwww_hists)):
            assert(sm_lhe_weight_hist.GetBinContent(i) > 0)

            cpwww_scaling_hists[i].SetBinContent(cpwww_scaling_hists[i].GetXaxis().FindFixBin(cpwww_coefficients[j]), cpwww_hists[j].GetBinContent(i)/sm_lhe_weight_hist.GetBinContent(i))
        
        cpwww_scaling_outfile.cd()
        cpwww_scaling_hists[i].Write()

    cpwww_scaling_outfile.Close()

    for i in range(1,cpw_hists[0].GetNbinsX()+1):
        cpw_scaling_hists[i]=ROOT.TH1D("ewdim6_scaling_bin_"+str(i),"ewdim6_scaling_bin_"+str(i),len(cpw_coefficients),cpw_hist_min,cpw_hist_max);

        for j in range(0,len(cpw_hists)):
            assert(sm_lhe_weight_hist.GetBinContent(i) > 0)

            cpw_scaling_hists[i].SetBinContent(cpw_scaling_hists[i].GetXaxis().FindFixBin(cpw_coefficients[j]), cpw_hists[j].GetBinContent(i)/sm_lhe_weight_hist.GetBinContent(i))
        
        cpw_scaling_outfile.cd()
        cpw_scaling_hists[i].Write()

    cpw_scaling_outfile.Close()

if options.ewdim6_scaling_only:
    sys.exit(1)

data_mlg_tree = ROOT.TTree()

array_data_mlg=array('f',[0])

data_mlg_tree.Branch('m',array_data_mlg,'m/F')



for year in years:

    if year == "2016":
        lumi=35.9
    elif year == "2017":
        lumi=41.5
    elif year == "2018":
        lumi=59.6
    else:
        assert(0)

    if lepton_name == "muon":
        if not options.closure_test:
            data_filename = options.workdir+"/data/wg/"+year+"/1June2019/single_muon.root"
        else:
            data_filename = options.workdir+"/data/wg/"+year+"/1June2019/wjets.root"

    elif lepton_name == "electron":
        if not options.closure_test:
            if year != "2018":
                data_filename = options.workdir+"/data/wg/"+year+"/1June2019/single_electron.root"
            else:    
                data_filename = options.workdir+"/data/wg/"+year+"/1June2019/egamma.root"
        else:
            data_filename = options.workdir+"/data/wg/"+year+"/1June2019/wjets.root"

    elif lepton_name == "both":
        if not options.closure_test:
            if year != "2018":
                data_filename = options.workdir+"/data/wg/"+year+"/1June2019/data.root"
            else:
                data_filename = options.workdir+"/data/wg/"+year+"/1June2019/data.root"
        else:
            data_filename = options.workdir+"/data/wg/"+year+"/1June2019/wjets.root"
    else:
        assert(0)

    if year == "2016":
        sieie_cut_barrel = sieie_cut_2016_barrel
        sieie_cut_endcap = sieie_cut_2016_endcap
        chiso_cut_barrel = chiso_cut_2016_barrel
        chiso_cut_endcap = chiso_cut_2016_endcap
    elif year == "2017":
        sieie_cut_barrel = sieie_cut_2017_barrel
        sieie_cut_endcap = sieie_cut_2017_endcap
        chiso_cut_barrel = chiso_cut_2017_barrel
        chiso_cut_endcap = chiso_cut_2017_endcap
    elif year == "2018":
        sieie_cut_barrel = sieie_cut_2018_barrel
        sieie_cut_endcap = sieie_cut_2018_endcap
        chiso_cut_barrel = chiso_cut_2018_barrel
        chiso_cut_endcap = chiso_cut_2018_endcap
    else:
        assert(0)

    fake_photon_sieie_cut_barrel = sieie_cut_barrel*1.75
    fake_photon_sieie_cut_endcap = sieie_cut_endcap*1.75
    fake_photon_chiso_cut_barrel = chiso_cut_barrel*1000
    fake_photon_chiso_cut_endcap = chiso_cut_endcap*1000    

    print "Running over "+year+" data"

    rdf=ROOT.RDataFrame("Events",data_filename)

    rinterface = rdf.Filter(get_filter_string(year))

    fake_photon_sieie_cut_cutstring = "((abs(photon_eta) < 1.5 && photon_sieie < "+str(fake_photon_sieie_cut_barrel)+ ") || (abs(photon_eta) > 1.5 && photon_sieie < "+str(fake_photon_sieie_cut_endcap)+ "))" 

    fake_photon_chiso_cut_cutstring = "((abs(photon_eta) < 1.5 && photon_pfRelIso03_chg*photon_pt < "+str(fake_photon_chiso_cut_barrel)+ ") || (abs(photon_eta) > 1.5 && photon_pfRelIso03_chg*photon_pt < "+str(fake_photon_chiso_cut_endcap)+ "))" 

    rinterface = rinterface.Define("weight","photon_selection == 0 && is_lepton_tight == 1")
    rinterface = rinterface.Define("fake_lepton_weight","photon_selection == 0 && is_lepton_tight == 0 ? get_fake_lepton_weight(lepton_eta,lepton_pt,\""+year+"\",lepton_pdg_id) : 0")
    rinterface = rinterface.Define("fake_lepton_stat_up_weight","photon_selection == 0 && is_lepton_tight == 0 ? get_fake_lepton_weight(lepton_eta,lepton_pt,\""+year+"\",lepton_pdg_id,\"up\") : 0")
    rinterface = rinterface.Define("fake_lepton_stat_down_weight","photon_selection == 0 && is_lepton_tight == 0 ? get_fake_lepton_weight(lepton_eta,lepton_pt,\""+year+"\",lepton_pdg_id,\"down\") : 0")
    rinterface = rinterface.Define("fake_photon_weight","photon_selection == 4 && "+fake_photon_sieie_cut_cutstring + " && " + fake_photon_chiso_cut_cutstring+" && is_lepton_tight == 1 ? get_fake_photon_weight(photon_eta,photon_pt,\""+year+"\",lepton_pdg_id) : 0")
    rinterface = rinterface.Define("fake_photon_alt_weight","photon_selection == 4 && "+fake_photon_sieie_cut_cutstring + " && " + fake_photon_chiso_cut_cutstring+" && is_lepton_tight == 1 ? get_fake_photon_weight(photon_eta,photon_pt,\""+year+"\",lepton_pdg_id,\"alt\") : 0")
    rinterface = rinterface.Define("fake_photon_stat_up_weight","photon_selection == 4 && "+fake_photon_sieie_cut_cutstring + " && " + fake_photon_chiso_cut_cutstring+" && is_lepton_tight == 1 ? get_fake_photon_weight(photon_eta,photon_pt,\""+year+"\",lepton_pdg_id,\"stat_up\") : 0")
    rinterface = rinterface.Define("double_fake_weight","photon_selection == 4 && "+fake_photon_sieie_cut_cutstring + " && " + fake_photon_chiso_cut_cutstring+" && is_lepton_tight == 0 ? get_fake_lepton_weight(lepton_eta,lepton_pt,\""+year+"\",lepton_pdg_id)*get_fake_photon_weight(photon_eta,photon_pt,\""+year+"\",lepton_pdg_id) : 0") 
    rinterface = rinterface.Define("double_fake_alt_weight","photon_selection == 4 && "+fake_photon_sieie_cut_cutstring + " && " + fake_photon_chiso_cut_cutstring+" && is_lepton_tight == 0 ? get_fake_lepton_weight(lepton_eta,lepton_pt,\""+year+"\",lepton_pdg_id)*get_fake_photon_weight(photon_eta,photon_pt,\""+year+"\",lepton_pdg_id,\"alt\") : 0") 
    rinterface = rinterface.Define("double_fake_stat_up_weight","photon_selection == 4 && "+fake_photon_sieie_cut_cutstring + " && " + fake_photon_chiso_cut_cutstring+" && is_lepton_tight == 0 ? get_fake_lepton_weight(lepton_eta,lepton_pt,\""+year+"\",lepton_pdg_id)*get_fake_photon_weight(photon_eta,photon_pt,\""+year+"\",lepton_pdg_id,\"stat_up\") : 0") 

    if options.closure_test:
        if year == "2016" or year == "2017":    
            prefire_weight_string = "PrefireWeight"
        else:    
            prefire_weight_string = "1"

        data_file = ROOT.TFile.Open(data_filename)
        data_nweightedevents = data_file.Get("nEventsGenWeighted").GetBinContent(1)
        rinterface = rinterface.Define("closure_test_fake_photon_weight","fake_photon_weight*"+prefire_weight_string+"*puWeight*(!(photon_gen_matching == 1|| photon_gen_matching == 4 || photon_gen_matching == 5 || photon_gen_matching == 6) && is_lepton_real == 1)*gen_weight/abs(gen_weight)*60430.0*1000*"+str(lumi)+"/"+str(data_nweightedevents)+"*photon_efficiency_scale_factor(photon_pt,photon_eta,\""+year+"\")*(abs(lepton_pdg_id) == 13 ? muon_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\") : electron_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\"))")
        rinterface = rinterface.Define("closure_test_weight","weight*"+prefire_weight_string+"*puWeight*(!(photon_gen_matching == 1 || photon_gen_matching == 4 || photon_gen_matching == 5 || photon_gen_matching == 6) && is_lepton_real == 1)*gen_weight/abs(gen_weight)*60430.0*1000*"+str(lumi)+"/"+str(data_nweightedevents)+"*photon_efficiency_scale_factor(photon_pt,photon_eta,\""+year+"\")*(abs(lepton_pdg_id) == 13 ? muon_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\") : electron_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\"))")

    for variable_definition in variable_definitions:
            rinterface = rinterface.Define(variable_definition[0],variable_definition[1])

    rresultptrs = []    
    rresultptrs_fake_photon = []    
    rresultptrs_fake_photon_alt = []    
    rresultptrs_fake_photon_stat_up = []    
    rresultptrs_fake_lepton = []    
    rresultptrs_fake_lepton_stat_up = []    
    rresultptrs_fake_lepton_stat_down = []    
    rresultptrs_double_fake = []    
    rresultptrs_double_fake_alt = []    
    rresultptrs_double_fake_stat_up = []    

    for i in range(len(variables)):
        if options.closure_test:
            rresultptrs.append(rinterface.Histo1D(histogram_models[i],variables[i],"closure_test_weight"))
            rresultptrs_fake_photon.append(rinterface.Histo1D(histogram_models[i],variables[i],"closure_test_fake_photon_weight"))
        else:    
            rresultptrs_fake_photon.append(rinterface.Histo1D(histogram_models[i],variables[i],"fake_photon_weight"))
            rresultptrs.append(rinterface.Histo1D(histogram_models[i],variables[i],"weight"))
        rresultptrs_fake_photon_alt.append(rinterface.Histo1D(histogram_models[i],variables[i],"fake_photon_alt_weight"))
        rresultptrs_fake_photon_stat_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"fake_photon_stat_up_weight"))
        rresultptrs_fake_lepton.append(rinterface.Histo1D(histogram_models[i],variables[i],"fake_lepton_weight"))
        rresultptrs_fake_lepton_stat_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"fake_lepton_stat_up_weight"))
        rresultptrs_fake_lepton_stat_down.append(rinterface.Histo1D(histogram_models[i],variables[i],"fake_lepton_stat_down_weight"))
        rresultptrs_double_fake.append(rinterface.Histo1D(histogram_models[i],variables[i],"double_fake_weight"))
        rresultptrs_double_fake_alt.append(rinterface.Histo1D(histogram_models[i],variables[i],"double_fake_alt_weight"))
        rresultptrs_double_fake_stat_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"double_fake_stat_up_weight"))

    for i in range(len(variables)):
        data["hists"][i].Add(rresultptrs[i].GetValue())
        if year == "2016":    
            fake_photon_2016["hists"][i].Add(rresultptrs_fake_photon[i].GetValue())
        fake_photon["hists"][i].Add(rresultptrs_fake_photon[i].GetValue())

        if options.closure_test:
            continue

        fake_photon_alt["hists"][i].Add(rresultptrs_fake_photon_alt[i].GetValue())
        fake_photon_stat_up["hists"][i].Add(rresultptrs_fake_photon_stat_up[i].GetValue())
        fake_lepton["hists"][i].Add(rresultptrs_fake_lepton[i].GetValue())
        fake_lepton_stat_up["hists"][i].Add(rresultptrs_fake_lepton_stat_up[i].GetValue())
        fake_lepton_stat_down["hists"][i].Add(rresultptrs_fake_lepton_stat_down[i].GetValue())
        double_fake["hists"][i].Add(rresultptrs_double_fake[i].GetValue())
        double_fake_alt["hists"][i].Add(rresultptrs_double_fake_alt[i].GetValue())
        double_fake_stat_up["hists"][i].Add(rresultptrs_double_fake_stat_up[i].GetValue())
        rresultptrs_double_fake[i].GetPtr().Scale(-1)
        rresultptrs_double_fake_alt[i].GetPtr().Scale(-1)
        if year == "2016":    
            fake_photon_2016["hists"][i].Add(rresultptrs_double_fake[i].GetValue())
        fake_photon["hists"][i].Add(rresultptrs_double_fake[i].GetValue())
        fake_photon_alt["hists"][i].Add(rresultptrs_double_fake_alt[i].GetValue())
        fake_lepton["hists"][i].Add(rresultptrs_double_fake[i].GetValue())


hists = []

for year in years:
    for label in labels.keys():

#        if label != "w+jets":
#            continue

        if label == "w+jets" and (year == "2017" or year == "2018") and options.no_wjets_for_2017_and_2018:
            continue

        if year == "2016":
            lumi=35.9
        elif year == "2017":
            lumi=41.5
        elif year == "2018":
            lumi=59.6
        else:
            assert(0)

        if year == "2016":
            sieie_cut_barrel = sieie_cut_2016_barrel
            sieie_cut_endcap = sieie_cut_2016_endcap
            chiso_cut_barrel = chiso_cut_2016_barrel
            chiso_cut_endcap = chiso_cut_2016_endcap
        elif year == "2017":
            sieie_cut_barrel = sieie_cut_2017_barrel
            sieie_cut_endcap = sieie_cut_2017_endcap
            chiso_cut_barrel = chiso_cut_2017_barrel
            chiso_cut_endcap = chiso_cut_2017_endcap
        elif year == "2018":
            sieie_cut_barrel = sieie_cut_2018_barrel
            sieie_cut_endcap = sieie_cut_2018_endcap
            chiso_cut_barrel = chiso_cut_2018_barrel
            chiso_cut_endcap = chiso_cut_2018_endcap
        else:
            assert(0)

        fake_photon_sieie_cut_barrel = sieie_cut_barrel*1.75
        fake_photon_sieie_cut_endcap = sieie_cut_endcap*1.75
        fake_photon_chiso_cut_barrel = chiso_cut_barrel*1000
        fake_photon_chiso_cut_endcap = chiso_cut_endcap*1000    

        for sample in labels[label]["samples"][year]:
            print "Running over sample " + str(sample["filename"])

            photon_gen_matching_for_fake_cutstring = "("
            photon_gen_matching_cutstring = "("

            if sample["fsr"]:
                photon_gen_matching_for_fake_cutstring+="photon_gen_matching == 4"
                photon_gen_matching_cutstring+="photon_gen_matching == 4"
            if sample["non_fsr"]:  
                if photon_gen_matching_for_fake_cutstring != "(":
                    photon_gen_matching_for_fake_cutstring += " || "
                if photon_gen_matching_cutstring != "(":
                    photon_gen_matching_cutstring += " || "
                photon_gen_matching_for_fake_cutstring+="photon_gen_matching == 5 || photon_gen_matching == 6"
                photon_gen_matching_cutstring+="photon_gen_matching == 5 || photon_gen_matching == 6"
            if sample["e_to_p_for_fake"]:
                if photon_gen_matching_for_fake_cutstring != "(":
                    photon_gen_matching_for_fake_cutstring += " || "
                photon_gen_matching_for_fake_cutstring+="photon_gen_matching == 1"
            if sample["non-prompt"]:
                pass
                if photon_gen_matching_cutstring != "(":
                    photon_gen_matching_cutstring += " || "
                photon_gen_matching_cutstring+="!(photon_gen_matching == 1 || photon_gen_matching == 4 || photon_gen_matching == 5 || photon_gen_matching == 6)"
                
            if photon_gen_matching_for_fake_cutstring != "(":    
                photon_gen_matching_for_fake_cutstring+= ")"    
            else:
                photon_gen_matching_for_fake_cutstring= "0"    

            if photon_gen_matching_cutstring != "(":    
                photon_gen_matching_cutstring+= ")"    
            else:
                photon_gen_matching_cutstring= "0"    

            rdf = ROOT.RDataFrame("Events",sample["filename"])

            #the JERUp and JESUp information was not added to the w+jets sample
            if  label != "w+jets":
                rinterface = rdf.Filter(get_filter_string(year,isdata=False))
            else:    
                rinterface = rdf.Filter(get_filter_string(year,isdata=True,lep="both"))

            rinterface = rinterface.Define("xs_weight",str(sample["xs"]*1000*lumi/sample["nweightedevents"]) + "*gen_weight/abs(gen_weight)") 

            if year == "2016" or year == "2017":    
                prefire_weight_string = "PrefireWeight"
                prefire_up_weight_string = "PrefireWeight_Up"
            else:    
                prefire_weight_string = "1"
                prefire_up_weight_string = "1"

            rinterface = rinterface.Define("base_weight",get_postfilter_selection_string()+"*xs_weight*puWeight*"+prefire_weight_string+"*photon_efficiency_scale_factor(photon_pt,photon_eta,\""+year+"\")*(abs(lepton_pdg_id) == 13 ? muon_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\") : electron_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\"))")      
            rinterface = rinterface.Define("prefire_up_base_weight",get_postfilter_selection_string()+"*xs_weight*puWeight*"+prefire_up_weight_string+"*photon_efficiency_scale_factor(photon_pt,photon_eta,\""+year+"\")*(abs(lepton_pdg_id) == 13 ? muon_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\") : electron_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\"))")    
            rinterface = rinterface.Define("pileup_up_base_weight",get_postfilter_selection_string()+"*xs_weight*puWeightUp*"+prefire_weight_string+"*photon_efficiency_scale_factor(photon_pt,photon_eta,\""+year+"\")*(abs(lepton_pdg_id) == 13 ? muon_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\") : electron_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\"))")    
            rinterface = rinterface.Define("electron_id_sf_up_base_weight",get_postfilter_selection_string()+"*xs_weight*puWeight*"+prefire_weight_string+"*photon_efficiency_scale_factor(photon_pt,photon_eta,\""+year+"\")*(abs(lepton_pdg_id) == 13 ? muon_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\") : electron_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\",true))")                  
            rinterface = rinterface.Define("electron_reco_sf_up_base_weight",get_postfilter_selection_string()+"*xs_weight*puWeight*"+prefire_weight_string+"*photon_efficiency_scale_factor(photon_pt,photon_eta,\""+year+"\")*(abs(lepton_pdg_id) == 13 ? muon_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\") : electron_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\",false,true))")    
            rinterface = rinterface.Define("electron_hlt_sf_up_base_weight",get_postfilter_selection_string()+"*xs_weight*puWeight*"+prefire_weight_string+"*photon_efficiency_scale_factor(photon_pt,photon_eta,\""+year+"\")*(abs(lepton_pdg_id) == 13 ? muon_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\") : electron_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\",false,false,true))")    
            rinterface = rinterface.Define("muon_id_sf_up_base_weight",get_postfilter_selection_string()+"*xs_weight*puWeight*"+prefire_weight_string+"*photon_efficiency_scale_factor(photon_pt,photon_eta,\""+year+"\")*(abs(lepton_pdg_id) == 13 ? muon_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\",false,true) : electron_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\"))")                  
            rinterface = rinterface.Define("muon_iso_sf_up_base_weight",get_postfilter_selection_string()+"*xs_weight*puWeight*"+prefire_weight_string+"*photon_efficiency_scale_factor(photon_pt,photon_eta,\""+year+"\")*(abs(lepton_pdg_id) == 13 ? muon_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\",true) : electron_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\"))")    
            rinterface = rinterface.Define("muon_hlt_sf_up_base_weight",get_postfilter_selection_string()+"*xs_weight*puWeight*"+prefire_weight_string+"*photon_efficiency_scale_factor(photon_pt,photon_eta,\""+year+"\")*(abs(lepton_pdg_id) == 13 ? muon_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\",false,false,true) : electron_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\"))")    
            rinterface = rinterface.Define("photon_id_sf_up_base_weight",get_postfilter_selection_string()+"*xs_weight*puWeight*"+prefire_weight_string+"*photon_efficiency_scale_factor(photon_pt,photon_eta,\""+year+"\",true)*(abs(lepton_pdg_id) == 13 ? muon_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\") : electron_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\"))") 
            if label != "w+jets":
                rinterface = rinterface.Define("jes_up_base_weight",get_postfilter_selection_string("JESUp")+"*xs_weight*puWeight*"+prefire_weight_string+"*photon_efficiency_scale_factor(photon_pt,photon_eta,\""+year+"\")*(abs(lepton_pdg_id) == 13 ? muon_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\") : electron_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\"))") 
                rinterface = rinterface.Define("jer_up_base_weight",get_postfilter_selection_string("JERUp")+"*xs_weight*puWeight*"+prefire_weight_string+"*photon_efficiency_scale_factor(photon_pt,photon_eta,\""+year+"\")*(abs(lepton_pdg_id) == 13 ? muon_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\") : electron_efficiency_scale_factor(lepton_pt,lepton_eta,\""+year+"\"))") 

            rinterface = rinterface.Define("weight","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_cutstring + ")*base_weight")

            if label == "wg+jets":
                rinterface = rinterface.Define("weight_pass_fiducial","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_cutstring + " && pass_fid_selection)*base_weight")

            rinterface = rinterface.Define("pileup_up_weight","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_cutstring + ")*pileup_up_base_weight")
            rinterface = rinterface.Define("prefire_up_weight","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_cutstring + ")*prefire_up_base_weight")
            rinterface = rinterface.Define("electron_id_sf_up_weight","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_cutstring + ")*electron_id_sf_up_base_weight")
            rinterface = rinterface.Define("electron_reco_sf_up_weight","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_cutstring + ")*electron_reco_sf_up_base_weight")
            rinterface = rinterface.Define("electron_hlt_sf_up_weight","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_cutstring + ")*electron_hlt_sf_up_base_weight")
            rinterface = rinterface.Define("muon_id_sf_up_weight","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_cutstring + ")*muon_id_sf_up_base_weight")
            rinterface = rinterface.Define("muon_iso_sf_up_weight","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_cutstring + ")*muon_iso_sf_up_base_weight")
            rinterface = rinterface.Define("muon_hlt_sf_up_weight","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_cutstring + ")*muon_hlt_sf_up_base_weight")
            rinterface = rinterface.Define("photon_id_sf_up_weight","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_cutstring + ")*photon_id_sf_up_base_weight")

            if label != "w+jets":
                rinterface = rinterface.Define("jes_up_weight","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_cutstring + ")*jes_up_base_weight")
                rinterface = rinterface.Define("jer_up_weight","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_cutstring + ")*jer_up_base_weight")

            if labels[label]["syst-scale"]:
                for i in range(0,8):
                     #this sample has a bug that causes the scale weight to be 1/2 the correct value
                    if sample["filename"] == options.workdir+"/data/wg/2016/1June2019/wgjets.root":
                        rinterface = rinterface.Define("scale"+str(i)+"_weight","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_cutstring + ")*base_weight*LHEScaleWeight["+str(i)+"]*2")
                    else:    
                        rinterface = rinterface.Define("scale"+str(i)+"_weight","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_cutstring + ")*base_weight*LHEScaleWeight["+str(i)+"]")

            if labels[label]["syst-pdf"]:
                for i in range(0,32):
                    if (year == "2017" or year == "2018") and options.no_pdf_var_for_2017_and_2018:
                        continue
                    #this sample has a bug that causes the scale weight to be 1/2 the correct value
                    if sample["filename"] == options.workdir+"/data/wg/2016/1June2019/wgjets.root":
                        rinterface = rinterface.Define("pdf"+str(i)+"_weight","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_cutstring + ")*base_weight*LHEPdfWeight["+str(i+1)+"]*2")
                    else:    
                        rinterface = rinterface.Define("pdf"+str(i)+"_weight","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_cutstring + ")*base_weight*LHEPdfWeight["+str(i+1)+"]")

            fake_photon_sieie_cut_cutstring = "((abs(photon_eta) < 1.5 && photon_sieie < "+str(fake_photon_sieie_cut_barrel)+ ") || (abs(photon_eta) > 1.5 && photon_sieie < "+str(fake_photon_sieie_cut_endcap)+ "))" 

            fake_photon_chiso_cut_cutstring = "((abs(photon_eta) < 1.5 && photon_pfRelIso03_chg*photon_pt < "+str(fake_photon_chiso_cut_barrel)+ ") || (abs(photon_eta) > 1.5 && photon_pfRelIso03_chg*photon_pt < "+str(fake_photon_chiso_cut_endcap)+ "))" 

#            rinterface = rinterface.Define("fake_lepton_weight","photon_selection == 0 && is_lepton_tight == 0 && is_lepton_real == 1 && "+photon_gen_matching_for_fake_cutstring+" ? get_fake_lepton_weight(lepton_eta,lepton_pt,\""+year+"\",lepton_pdg_id)*base_weight : 0")
#            rinterface = rinterface.Define("fake_photon_weight","photon_selection == 4 && "+fake_photon_sieie_cut_cutstring + " && " + fake_photon_chiso_cut_cutstring+" && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_for_fake_cutstring+" ? get_fake_photon_weight(photon_eta,photon_pt,\""+year+"\",lepton_pdg_id)*base_weight : 0")
#            rinterface = rinterface.Define("double_fake_weight","photon_selection == 4 && "+fake_photon_sieie_cut_cutstring + " && " + fake_photon_chiso_cut_cutstring+" && is_lepton_tight == 0 && is_lepton_real == 1 && "+photon_gen_matching_for_fake_cutstring+" ? get_fake_lepton_weight(lepton_eta,lepton_pt,\""+year+"\",lepton_pdg_id)*get_fake_photon_weight(photon_eta,photon_pt,\""+year+"\",lepton_pdg_id)*base_weight : 0") 

            rinterface = rinterface.Define("fake_lepton_weight","photon_selection == 0 && is_lepton_tight == 0 && is_lepton_real == 1 && "+photon_gen_matching_for_fake_cutstring+" ? get_fake_lepton_weight(lepton_eta,lepton_pt,\""+year+"\",lepton_pdg_id)*xs_weight*puWeight*"+prefire_weight_string+"*" + get_postfilter_selection_string()+" : 0")
            rinterface = rinterface.Define("fake_lepton_stat_up_weight","photon_selection == 0 && is_lepton_tight == 0 && is_lepton_real == 1 && "+photon_gen_matching_for_fake_cutstring+" ? get_fake_lepton_weight(lepton_eta,lepton_pt,\""+year+"\",lepton_pdg_id,\"up\")*xs_weight*puWeight*"+prefire_weight_string + "*" + get_postfilter_selection_string()+" : 0")
            rinterface = rinterface.Define("fake_lepton_stat_down_weight","photon_selection == 0 && is_lepton_tight == 0 && is_lepton_real == 1 && "+photon_gen_matching_for_fake_cutstring+" ? get_fake_lepton_weight(lepton_eta,lepton_pt,\""+year+"\",lepton_pdg_id,\"down\")*xs_weight*puWeight*"+prefire_weight_string+"*" + get_postfilter_selection_string()+" : 0")
            rinterface = rinterface.Define("fake_photon_weight","photon_selection == 4 && "+fake_photon_sieie_cut_cutstring + " && " + fake_photon_chiso_cut_cutstring+" && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_for_fake_cutstring+" ? get_fake_photon_weight(photon_eta,photon_pt,\""+year+"\",lepton_pdg_id)*xs_weight*puWeight*"+prefire_weight_string+"*" + get_postfilter_selection_string()+" : 0")
            rinterface = rinterface.Define("fake_photon_alt_weight","photon_selection == 4 && "+fake_photon_sieie_cut_cutstring + " && " + fake_photon_chiso_cut_cutstring+" && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_for_fake_cutstring+" ? get_fake_photon_weight(photon_eta,photon_pt,\""+year+"\",lepton_pdg_id,\"alt\")*xs_weight*puWeight*"+prefire_weight_string+"*" + get_postfilter_selection_string()+" : 0")
            rinterface = rinterface.Define("fake_photon_stat_up_weight","photon_selection == 4 && "+fake_photon_sieie_cut_cutstring + " && " + fake_photon_chiso_cut_cutstring+" && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_for_fake_cutstring+" ? get_fake_photon_weight(photon_eta,photon_pt,\""+year+"\",lepton_pdg_id,\"stat_up\")*xs_weight*puWeight*"+prefire_weight_string+"*" + get_postfilter_selection_string()+" : 0")
            rinterface = rinterface.Define("double_fake_weight","photon_selection == 4 && "+fake_photon_sieie_cut_cutstring + " && " + fake_photon_chiso_cut_cutstring+" && is_lepton_tight == 0 && is_lepton_real == 1 && "+photon_gen_matching_for_fake_cutstring+" ? get_fake_lepton_weight(lepton_eta,lepton_pt,\""+year+"\",lepton_pdg_id)*get_fake_photon_weight(photon_eta,photon_pt,\""+year+"\",lepton_pdg_id)*xs_weight*puWeight*"+prefire_weight_string+"*" + get_postfilter_selection_string()+" : 0") 
            rinterface = rinterface.Define("double_fake_alt_weight","photon_selection == 4 && "+fake_photon_sieie_cut_cutstring + " && " + fake_photon_chiso_cut_cutstring+" && is_lepton_tight == 0 && is_lepton_real == 1 && "+photon_gen_matching_for_fake_cutstring+" ? get_fake_lepton_weight(lepton_eta,lepton_pt,\""+year+"\",lepton_pdg_id)*get_fake_photon_weight(photon_eta,photon_pt,\""+year+"\",lepton_pdg_id,\"alt\")*xs_weight*puWeight*"+prefire_weight_string+"*" + get_postfilter_selection_string()+" : 0") 
            rinterface = rinterface.Define("double_fake_stat_up_weight","photon_selection == 4 && "+fake_photon_sieie_cut_cutstring + " && " + fake_photon_chiso_cut_cutstring+" && is_lepton_tight == 0 && is_lepton_real == 1 && "+photon_gen_matching_for_fake_cutstring+" ? get_fake_lepton_weight(lepton_eta,lepton_pt,\""+year+"\",lepton_pdg_id)*get_fake_photon_weight(photon_eta,photon_pt,\""+year+"\",lepton_pdg_id,\"stat_up\")*xs_weight*puWeight*"+prefire_weight_string+"*" + get_postfilter_selection_string()+" : 0") 

            if label == "w+jets" and year == "2016":
#                rinterface = rinterface.Define("wjets_fake_photon_weight","photon_selection == 4 && "+fake_photon_sieie_cut_cutstring + " && " + fake_photon_chiso_cut_cutstring+" && is_lepton_tight == 1 && is_lepton_real == 1 && "+photon_gen_matching_for_fake_cutstring+" ? get_wjets_fake_photon_weight(photon_eta,photon_pt,\""+year+"\",lepton_pdg_id)*xs_weight*puWeight*"+prefire_weight_string+"*" + get_postfilter_selection_string()+" : 0")
                rinterface = rinterface.Define("wjets_fake_photon_weight","photon_selection == 4 && "+fake_photon_sieie_cut_cutstring + " && " + fake_photon_chiso_cut_cutstring+" && is_lepton_tight == 1 && is_lepton_real == 1 && !(photon_gen_matching == 1|| photon_gen_matching == 4 || photon_gen_matching == 5 || photon_gen_matching == 6) ? get_fake_photon_weight(photon_eta,photon_pt,\""+year+"\",lepton_pdg_id,\"wjets\")*xs_weight*puWeight*"+prefire_weight_string+"*" + get_postfilter_selection_string()+" : 0")
                rinterface = rinterface.Define("wjets_chiso_fake_photon_weight","photon_selection == 3 && ((abs(photon_eta) < 1.5 && photon_pfRelIso03_chg*photon_pt < "+str(chiso_cut_barrel)+"*1000) || (abs(photon_eta) > 1.5 && photon_pfRelIso03_chg*photon_pt < "+str(chiso_cut_endcap)+"*1000)) && is_lepton_tight == 1 && is_lepton_real == 1 && !(photon_gen_matching == 1|| photon_gen_matching == 4 || photon_gen_matching == 5 || photon_gen_matching == 6) ? get_fake_photon_weight(photon_eta,photon_pt,\""+year+"\",lepton_pdg_id,\"wjets_chiso\")*xs_weight*puWeight*"+prefire_weight_string+"*" + get_postfilter_selection_string()+" : 0")

            if sample["e_to_p"]:
                rinterface = rinterface.Define("e_to_p_weight","photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && photon_gen_matching == 1 ? base_weight : 0")
                rinterface = rinterface.Define("e_to_p_pileup_up_weight","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && photon_gen_matching == 1)*pileup_up_base_weight")
                rinterface = rinterface.Define("e_to_p_prefire_up_weight","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && photon_gen_matching == 1)*prefire_up_base_weight")
                rinterface = rinterface.Define("e_to_p_electron_id_sf_up_weight","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && photon_gen_matching == 1)*electron_id_sf_up_base_weight")
                rinterface = rinterface.Define("e_to_p_electron_reco_sf_up_weight","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && photon_gen_matching == 1)*electron_reco_sf_up_base_weight")
                rinterface = rinterface.Define("e_to_p_electron_hlt_sf_up_weight","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && photon_gen_matching == 1)*electron_hlt_sf_up_base_weight")
                rinterface = rinterface.Define("e_to_p_photon_id_sf_up_weight","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && photon_gen_matching == 1)*photon_id_sf_up_base_weight")
                rinterface = rinterface.Define("e_to_p_jes_up_weight","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && photon_gen_matching == 1)*jes_up_base_weight")
                rinterface = rinterface.Define("e_to_p_jer_up_weight","(photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && photon_gen_matching == 1)*jer_up_base_weight")

                
            if sample["e_to_p_non_res"]:
                rinterface = rinterface.Define("e_to_p_non_res_weight","photon_selection == 0 && is_lepton_tight == 1 && is_lepton_real == 1 && photon_gen_matching == 1 ? base_weight : 0") 

            for variable_definition in variable_definitions:
                rinterface = rinterface.Define(variable_definition[0],variable_definition[1])


            if labels[label]["syst-scale"]:
                rresultptrs_scale = []    
                for i in range(0,8):
                    rresultptrs_scale.append([])    
                    
            if labels[label]["syst-pdf"]:
                rresultptrs_pdf = []    
                for i in range(0,32):
                    if (year == "2017" or year == "2018") and options.no_pdf_var_for_2017_and_2018:
                        continue
                    rresultptrs_pdf.append([])    

            rresultptrs = []    
            if label == "w+jets" and year == "2016":
                rresultptrs_wjets_fake_photon_chiso = []    
                rresultptrs_wjets_fake_photon = []    
                rresultptrs_wjets = []    
            rresultptrs_fake_photon = []    
            rresultptrs_fake_photon_alt = []    
            rresultptrs_fake_photon_stat_up = []    
            rresultptrs_fake_lepton = []    
            rresultptrs_fake_lepton_stat_up = []    
            rresultptrs_fake_lepton_stat_down = []    
            rresultptrs_double_fake = []    
            rresultptrs_double_fake_alt = []    
            rresultptrs_double_fake_stat_up = []    
            rresultptrs_pileup_up = []
            rresultptrs_prefire_up = []    
            if label != "w+jets":
                rresultptrs_jes_up = []    
                rresultptrs_jer_up = []    
            rresultptrs_electron_id_sf_up = []    
            rresultptrs_electron_reco_sf_up = []    
            rresultptrs_electron_hlt_sf_up = []    
            rresultptrs_muon_id_sf_up = []    
            rresultptrs_muon_iso_sf_up = []    
            rresultptrs_muon_hlt_sf_up = []    
            rresultptrs_photon_id_sf_up = []    
            if sample["e_to_p"]:
                rresultptrs_e_to_p = []    
                rresultptrs_e_to_p_electron_id_sf_up = []    
                rresultptrs_e_to_p_electron_reco_sf_up = []    
                rresultptrs_e_to_p_electron_hlt_sf_up = []    
                rresultptrs_e_to_p_photon_id_sf_up = []    
                rresultptrs_e_to_p_pileup_up = []    
                rresultptrs_e_to_p_prefire_up = []    
                rresultptrs_e_to_p_jes_up = []    
                rresultptrs_e_to_p_jer_up = []    

            if sample["e_to_p_non_res"]:
                rresultptrs_e_to_p_non_res = []    
            if label == "wg+jets":
                rresultptrs_pass_fiducial = []    


            for i in range(len(variables)):
                if labels[label]["color"] != None:
                    rresultptrs.append(rinterface.Histo1D(histogram_models[i],variables[i],"weight"))
                    rresultptrs_pileup_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"pileup_up_weight"))
                    rresultptrs_prefire_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"prefire_up_weight"))
                    rresultptrs_muon_id_sf_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"muon_id_sf_up_weight"))
                    rresultptrs_muon_iso_sf_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"muon_iso_sf_up_weight"))
                    rresultptrs_muon_hlt_sf_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"muon_hlt_sf_up_weight"))
                    rresultptrs_electron_id_sf_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"electron_id_sf_up_weight"))
                    rresultptrs_electron_reco_sf_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"electron_reco_sf_up_weight"))
                    rresultptrs_electron_hlt_sf_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"electron_hlt_sf_up_weight"))
                    rresultptrs_photon_id_sf_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"photon_id_sf_up_weight"))
                    if label == "wg+jets":
                        rresultptrs_pass_fiducial.append(rinterface.Histo1D(histogram_models[i],variables[i],"weight_pass_fiducial"))
                    if label != "w+jets":
                        rresultptrs_jes_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"jes_up_weight"))
                        rresultptrs_jer_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"jer_up_weight"))

                if label == "w+jets" and year == "2016":
                    rresultptrs_wjets_fake_photon_chiso.append(rinterface.Histo1D(histogram_models[i],variables[i],"wjets_chiso_fake_photon_weight"))        
                    rresultptrs_wjets_fake_photon.append(rinterface.Histo1D(histogram_models[i],variables[i],"wjets_fake_photon_weight"))    
                    rresultptrs_wjets.append(rinterface.Histo1D(histogram_models[i],variables[i],"weight"))    

                rresultptrs_fake_photon.append(rinterface.Histo1D(histogram_models[i],variables[i],"fake_photon_weight"))
                rresultptrs_fake_photon_alt.append(rinterface.Histo1D(histogram_models[i],variables[i],"fake_photon_alt_weight"))
                rresultptrs_fake_photon_stat_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"fake_photon_stat_up_weight"))
                rresultptrs_fake_lepton.append(rinterface.Histo1D(histogram_models[i],variables[i],"fake_lepton_weight"))
                rresultptrs_fake_lepton_stat_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"fake_lepton_stat_up_weight"))
                rresultptrs_fake_lepton_stat_down.append(rinterface.Histo1D(histogram_models[i],variables[i],"fake_lepton_stat_down_weight"))
                rresultptrs_double_fake.append(rinterface.Histo1D(histogram_models[i],variables[i],"double_fake_weight"))
                rresultptrs_double_fake_alt.append(rinterface.Histo1D(histogram_models[i],variables[i],"double_fake_alt_weight"))
                rresultptrs_double_fake_stat_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"double_fake_stat_up_weight"))

                if labels[label]["syst-scale"]:
                    for j in range(0,8):
                        rresultptrs_scale[j].append(rinterface.Histo1D(histogram_models[i],variables[i],"scale"+str(j)+"_weight"))
                if labels[label]["syst-pdf"]:
                    for j in range(0,32):
                        if (year == "2017" or year == "2018") and options.no_pdf_var_for_2017_and_2018:
                            continue
                        rresultptrs_pdf[j].append(rinterface.Histo1D(histogram_models[i],variables[i],"pdf"+str(j)+"_weight"))

                if sample["e_to_p"]:
                    rresultptrs_e_to_p.append(rinterface.Histo1D(histogram_models[i],variables[i],"e_to_p_weight"))
                    rresultptrs_e_to_p_electron_id_sf_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"e_to_p_electron_id_sf_up_weight"))
                    rresultptrs_e_to_p_electron_reco_sf_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"e_to_p_electron_reco_sf_up_weight"))
                    rresultptrs_e_to_p_electron_hlt_sf_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"e_to_p_electron_hlt_sf_up_weight"))
                    rresultptrs_e_to_p_photon_id_sf_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"e_to_p_photon_id_sf_up_weight"))
                    rresultptrs_e_to_p_pileup_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"e_to_p_pileup_up_weight"))
                    rresultptrs_e_to_p_prefire_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"e_to_p_prefire_up_weight"))
                    rresultptrs_e_to_p_jes_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"e_to_p_jes_up_weight"))
                    rresultptrs_e_to_p_jer_up.append(rinterface.Histo1D(histogram_models[i],variables[i],"e_to_p_jer_up_weight"))

                if sample["e_to_p_non_res"]:
                    rresultptrs_e_to_p_non_res.append(rinterface.Histo1D(histogram_models[i],variables[i],"e_to_p_non_res_weight"))

            for i in range(len(variables)):

#                if i != mlg_index:
#                    continue

                if labels[label]["color"] != None:
                    labels[label]["hists"][i].Add(rresultptrs[i].GetValue())
                    labels[label]["hists-pileup-up"][i].Add(rresultptrs_pileup_up[i].GetValue())
                    labels[label]["hists-prefire-up"][i].Add(rresultptrs_prefire_up[i].GetValue())
                    labels[label]["hists-electron-id-sf-up"][i].Add(rresultptrs_electron_id_sf_up[i].GetValue())
                    labels[label]["hists-electron-reco-sf-up"][i].Add(rresultptrs_electron_reco_sf_up[i].GetValue())
                    labels[label]["hists-electron-hlt-sf-up"][i].Add(rresultptrs_electron_hlt_sf_up[i].GetValue())
                    labels[label]["hists-muon-id-sf-up"][i].Add(rresultptrs_muon_id_sf_up[i].GetValue())
                    labels[label]["hists-muon-iso-sf-up"][i].Add(rresultptrs_muon_iso_sf_up[i].GetValue())
                    labels[label]["hists-muon-hlt-sf-up"][i].Add(rresultptrs_muon_hlt_sf_up[i].GetValue())
                    labels[label]["hists-photon-id-sf-up"][i].Add(rresultptrs_photon_id_sf_up[i].GetValue())
                    if label == "wg+jets":
                        labels[label]["hists-pass-fiducial"][i].Add(rresultptrs_pass_fiducial[i].GetValue())
                    if label != "w+jets":
                        labels[label]["hists-jes-up"][i].Add(rresultptrs_jes_up[i].GetValue())
                        labels[label]["hists-jer-up"][i].Add(rresultptrs_jer_up[i].GetValue())
                        

            for i in range(len(variables)):
                rresultptrs_fake_photon[i].Scale(-1)
                rresultptrs_fake_lepton[i].Scale(-1)
                rresultptrs_fake_photon_alt[i].Scale(-1)
                rresultptrs_fake_photon_stat_up[i].Scale(-1)

                if labels[label]["syst-scale"]:
                    for j in range(0,8):
                         labels[label]["hists-scale-variation"+str(j)][i].Add(rresultptrs_scale[j][i].GetValue())

                if labels[label]["syst-pdf"]:
                    for j in range(0,32):
                        if (year == "2017" or year == "2018") and options.no_pdf_var_for_2017_and_2018:
                            continue
                        labels[label]["hists-pdf-variation"+str(j)][i].Add(rresultptrs_pdf[j][i].GetValue())

                if label == "wg+jets":
                    fake_signal_contamination["hists"][i].Add(rresultptrs_fake_lepton[i].GetValue())
                    fake_signal_contamination["hists"][i].Add(rresultptrs_fake_photon[i].GetValue())
                    fake_signal_contamination["hists"][i].Add(rresultptrs_double_fake[i].GetValue())
                    
                if year == "2016":    
                    fake_photon_2016["hists"][i].Add(rresultptrs_fake_photon[i].GetValue())

                if label == "w+jets" and year == "2016": 
                    wjets_fake_photon_chiso_2016["hists"][i].Add(rresultptrs_wjets_fake_photon_chiso[i].GetValue())
                    wjets_fake_photon_2016["hists"][i].Add(rresultptrs_wjets_fake_photon[i].GetValue())
                    wjets_2016["hists"][i].Add(rresultptrs_wjets[i].GetValue())

                fake_photon["hists"][i].Add(rresultptrs_fake_photon[i].GetValue())
                fake_photon_alt["hists"][i].Add(rresultptrs_fake_photon_alt[i].GetValue())
                fake_photon_stat_up["hists"][i].Add(rresultptrs_fake_photon_stat_up[i].GetValue())
                fake_lepton["hists"][i].Add(rresultptrs_fake_lepton[i].GetValue())
                fake_lepton_stat_up["hists"][i].Add(rresultptrs_fake_lepton_stat_up[i].GetValue())
                fake_lepton_stat_down["hists"][i].Add(rresultptrs_fake_lepton_stat_down[i].GetValue())
                double_fake["hists"][i].Add(rresultptrs_double_fake[i].GetValue())
                double_fake_alt["hists"][i].Add(rresultptrs_double_fake_alt[i].GetValue())
                double_fake_stat_up["hists"][i].Add(rresultptrs_double_fake_stat_up[i].GetValue())
                if sample["e_to_p"]:
                    e_to_p["hists"][i].Add(rresultptrs_e_to_p[i].GetValue())
                    e_to_p["hists-electron-id-sf-up"][i].Add(rresultptrs_e_to_p_electron_id_sf_up[i].GetValue())
                    e_to_p["hists-electron-reco-sf-up"][i].Add(rresultptrs_e_to_p_electron_reco_sf_up[i].GetValue())
                    e_to_p["hists-electron-hlt-sf-up"][i].Add(rresultptrs_e_to_p_electron_hlt_sf_up[i].GetValue())
                    e_to_p["hists-photon-id-sf-up"][i].Add(rresultptrs_e_to_p_photon_id_sf_up[i].GetValue())
                    e_to_p["hists-pileup-up"][i].Add(rresultptrs_e_to_p_pileup_up[i].GetValue())
                    e_to_p["hists-prefire-up"][i].Add(rresultptrs_e_to_p_prefire_up[i].GetValue())
                    e_to_p["hists-jes-up"][i].Add(rresultptrs_e_to_p_jes_up[i].GetValue())
                    e_to_p["hists-jer-up"][i].Add(rresultptrs_e_to_p_jer_up[i].GetValue())

                if sample["e_to_p_non_res"]:
                    e_to_p_non_res["hists"][i].Add(rresultptrs_e_to_p_non_res[i].GetValue())
                
        for i in range(len(variables)):    

            if labels[label]["color"] == None:
                continue

            labels[label]["hists"][i].SetFillColor(labels[label]["color"])
            labels[label]["hists"][i].SetFillStyle(1001)
            labels[label]["hists"][i].SetLineColor(labels[label]["color"])

for hist in hists:
    hists.Print("all")

if options.no_wjets_for_2017_and_2018 and "w+jets" in labels:
    for i in range(len(variables)):
        labels["w+jets"]["hists"][i].Scale(fake_photon["hists"][i].Integral()/fake_photon_2016["hists"][i].Integral())
#        wjets_2016["hists"][i].Scale(fake_photon["hists"][i].Integral()/fake_photon_2016["hists"][i].Integral())
#        wjets_fake_photon_2016["hists"][i].Scale(fake_photon["hists"][i].Integral()/fake_photon_2016["hists"][i].Integral())

#wjets_2016["hists"][3].Scale(fake_photon["hists"][mlg_index].Integral()/fake_photon_2016["hists"][mlg_index].Integral())
#wjets_fake_photon["hists"][3].Scale(fake_photon["hists"][mlg_index].Integral()/fake_photon_2016["hists"][mlg_index].Integral())
non_closure = []
for i in range(len(variables)):

    c = ROOT.TCanvas("c", "c",5,50,500,500)

    s="35.9 fb^{-1} (13 TeV)"
    lumilabel = ROOT.TLatex (0.95, 0.93, s)
    lumilabel.SetNDC ()
    lumilabel.SetTextAlign (30)
    lumilabel.SetTextFont (42)
    lumilabel.SetTextSize (0.040)

    minus_one_hist = histogram_models[i].GetHistogram()
    for j in range(1,minus_one_hist.GetNbinsX()+1):
        minus_one_hist.SetBinContent(j,-1)
        minus_one_hist.SetBinError(j,0)
    non_closure.append(histogram_models[i].GetHistogram())


    wjets_2016["hists"][i].SetLineColor(ROOT.kBlue)
    wjets_fake_photon_2016["hists"][i].SetLineColor(ROOT.kRed)
    wjets_fake_photon_2016["hists"][i].SetMinimum(0)
#    if wjets_fake_photon_2016["hists"][i].Integral() > 0:
#        wjets_fake_photon_2016["hists"][i].Scale(wjets_2016["hists"][i].Integral()/wjets_fake_photon_2016["hists"][i].Integral())
    wjets_fake_photon_2016["hists"][i].SetMaximum(1.55*max(wjets_fake_photon_2016["hists"][i].GetMaximum(),wjets_2016["hists"][i].GetMaximum()))
    set_axis_fonts(wjets_fake_photon_2016["hists"][i],"x",getXaxisLabel(variables[i]))
    wjets_fake_photon_2016["hists"][i].Draw()
    wjets_2016["hists"][i].Draw("same")
    lumilabel.Draw("same")


    set_axis_fonts(wjets_fake_photon_2016["hists"][i],"x",getXaxisLabel(variables[i]))
    j=0
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wjets_fake_photon_2016["hists"][i],"fake photon","l")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wjets_2016["hists"][i],"w+jets","l")
    j=j+1
    c.SaveAs(options.outputdir + "/" + "closure_test_"+variables_labels[i]+".png")

    wjets_fake_photon_chiso_2016["hists"][i].SetLineColor(ROOT.kRed)
#    if wjets_fake_photon_chiso_2016["hists"][i].Integral() > 0:
#        wjets_fake_photon_chiso_2016["hists"][i].Scale(wjets_2016["hists"][i].Integral()/wjets_fake_photon_chiso_2016["hists"][i].Integral())
    wjets_fake_photon_chiso_2016["hists"][i].SetMaximum(1.55*max(wjets_fake_photon_chiso_2016["hists"][i].GetMaximum(),wjets_2016["hists"][i].GetMaximum()))
    wjets_fake_photon_chiso_2016["hists"][i].SetMinimum(0)
    wjets_fake_photon_chiso_2016["hists"][i].Draw()
    wjets_2016["hists"][i].Draw("same")
    lumilabel.Draw("same")
    set_axis_fonts(wjets_fake_photon_chiso_2016["hists"][i],"x",getXaxisLabel(variables[i]))
    j=0
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wjets_fake_photon_chiso_2016["hists"][i],"fake photon","l")
    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wjets_2016["hists"][i],"w+jets","l")
    j=j+1
    c.SaveAs(options.outputdir + "/" + "closure_test_chiso_"+variables_labels[i]+".png")
    
    window_size=5

    if i == mlg_index:
        for j in range(1,wjets_2016["hists"][i].GetNbinsX()+1):
            rebinnum=ROOT.TH1F("","",2*window_size+1,0,2*window_size+1)
            rebinden=ROOT.TH1F("","",2*window_size+1,0,2*window_size+1)

            rebinnum.Sumw2()
            rebinden.Sumw2()

            if j < window_size+1:

                for k in range(1,2*window_size+2):
                    rebinnum.SetBinContent(k,wjets_2016["hists"][i].GetBinContent(k))
                    rebinnum.SetBinError(k,wjets_2016["hists"][i].GetBinError(k))
                    rebinden.SetBinContent(k,wjets_fake_photon_2016["hists"][i].GetBinContent(k))
                    rebinden.SetBinError(k,wjets_fake_photon_2016["hists"][i].GetBinError(k))
            elif j > wjets_2016["hists"][i].GetNbinsX() - window_size-1:        

                for k in range(wjets_2016["hists"][i].GetNbinsX()+1-2*window_size-1,wjets_2016["hists"][i].GetNbinsX()+1):
                    rebinnum.SetBinContent(k-wjets_2016["hists"][i].GetNbinsX()-1+2*window_size+1+1,wjets_2016["hists"][i].GetBinContent(k))
                    rebinnum.SetBinError(k-wjets_2016["hists"][i].GetNbinsX()-1+2*window_size+1+1,wjets_2016["hists"][i].GetBinError(k))
                    rebinden.SetBinContent(k-wjets_2016["hists"][i].GetNbinsX()-1+2*window_size+1+1,wjets_fake_photon_2016["hists"][i].GetBinContent(k))
                    rebinden.SetBinError(k-wjets_2016["hists"][i].GetNbinsX()-1+2*window_size+1+1,wjets_fake_photon_2016["hists"][i].GetBinError(k))
            else:

                for k in range(j-window_size,j+window_size+1):
                    rebinnum.SetBinContent(k-j+window_size+1,wjets_2016["hists"][i].GetBinContent(k))
                    rebinnum.SetBinError(k-j+window_size+1,wjets_2016["hists"][i].GetBinError(k))
                    rebinden.SetBinContent(k-j+window_size+1,wjets_fake_photon_2016["hists"][i].GetBinContent(k))
                    rebinden.SetBinError(k-j+window_size+1,wjets_fake_photon_2016["hists"][i].GetBinError(k))
                 
#            rebinnum.Print("all")        
#            rebinden.Print("all")        

            rebinnum.Rebin(2*window_size+1)        
            rebinden.Rebin(2*window_size+1)        

            rebinnum.Divide(rebinden)

#            rebinnum.Print("all")        
#            rebinden.Print("all") 

            non_closure[len(non_closure)-1].SetBinContent(j,rebinnum.GetBinContent(1))   
            non_closure[len(non_closure)-1].SetBinError(j,rebinnum.GetBinError(1))   

    else:
        non_closure[len(non_closure)-1].Add(wjets_2016["hists"][i])
#    wjets_fake_photon_2016["hists"][i].Scale(-1)
#    non_closure[len(non_closure)-1].Add(wjets_fake_photon_2016["hists"][i])
#    wjets_fake_photon["hists"][i].Scale(-1)
        non_closure[len(non_closure)-1].Divide(wjets_fake_photon_2016["hists"][i])

    non_closure[len(non_closure)-1].Add(minus_one_hist)
    non_closure[len(non_closure)-1].SetMinimum(-1.5)
    non_closure[len(non_closure)-1].SetMaximum(1.5)
    non_closure[len(non_closure)-1].Draw()
    set_axis_fonts(non_closure[len(non_closure)-1],"x",getXaxisLabel(variables[i]))
    c.SaveAs(options.outputdir + "/" + "non_closure_"+variables_labels[i]+".png")

#print "andrew debug -2"
#non_closure[mlg_index]
#print "andrew debug -1"

for i in range(len(variables)):

    c = ROOT.TCanvas("c", "c",5,50,500,500)

    s=str(totallumi)+" fb^{-1} (13 TeV)"
    lumilabel = ROOT.TLatex (0.95, 0.93, s)
    lumilabel.SetNDC ()
    lumilabel.SetTextAlign (30)
    lumilabel.SetTextFont (42)
    lumilabel.SetTextSize (0.040)

    central = labels["wg+jets"]["hists"][i].Clone()
    up = labels["wg+jets"]["hists-pileup-up"][i].Clone()
    down = makeDownShape(labels["wg+jets"]["hists-pileup-up"][i],labels["wg+jets"]["hists"][i]).Clone()

    central.SetLineColor(ROOT.kBlack)
    central.SetLineWidth(2)

    up.SetLineColor(ROOT.kRed)
    up.SetLineWidth(2)

    down.SetLineColor(ROOT.kBlue)
    down.SetLineWidth(2)

    central.Draw("hist")
    up.Draw("hist same")
    down.Draw("hist same")

    lumilabel.Draw("same")

    c.SaveAs(options.outputdir + "/" + "wgjets_pileup_unc_"+variables_labels[i]+".png")

    c.Close()

#wjets_fake_photon["hists"][mlg_index].Print("all")
#wjets_2016["hists"][mlg_index].Print("all")
#wjets_fake_photon["hists"][mlg_index].Scale(-1)
#wjets_2016["hists"][mlg_index].Add(wjets_fake_photon["hists"][mlg_index])
#wjets_2016["hists"][mlg_index].Print("all")
#abs(labels["w+jets"]["hists"][mlg_index].Integral() - fake_photon_2016["hists"][mlg_index].Integral())*fake_photon["hists"][mlg_index].Integral()/fake_photon_2016["hists"][mlg_index].Integral()

def mlg_fit(inputs):

    print "inputs[\"label\"] = "+str(inputs["label"])

    m= ROOT.RooRealVar("m","m",mlg_fit_lower_bound,mlg_fit_upper_bound)
    m0=ROOT.RooRealVar("m0",    "m0",-2,-3,3)
    sigma=ROOT.RooRealVar("sigma",  "sigma",1.75029,0.1,3)
    alpha=ROOT.RooRealVar("alpha",  "alpha",2.48320,0,10)
#    alpha=ROOT.RooRealVar("alpha",  "alpha",4.45779,4.45779-2,4.45779+2)
#    alpha=ROOT.RooRealVar("alpha",  "alpha",,0,10)
#    alpha=ROOT.RooRealVar("alpha",  "alpha",4.27560,4.27560,4.27560)
#    n=ROOT.RooRealVar("n",          "n",2.11960,1,3)
    n=ROOT.RooRealVar("n",          "n",2.11960,2.11960,2.11960)
    cb = ROOT.RooCBShape("cb", "Crystal Ball", m, m0, sigma, alpha, n)

#    mass = ROOT.RooRealVar("mass","mass",91.9311,89.855-5,89.855+5)
#    width = ROOT.RooRealVar("width","width",3.3244,0.5*3.3244/4.0,10*3.3244/3.0);
    mass = ROOT.RooRealVar("mass","mass",91.1876,91.1876,91.1876)
    width = ROOT.RooRealVar("width","width",2.4952,2.4952,2.4952);
    bw = ROOT.RooBreitWigner("bw","Breit Wigner",m,mass,width)

    RooFFTConvPdf_bwcb = ROOT.RooFFTConvPdf("bwcb","Breit Wigner convolved with a Crystal Ball",m,bw,cb)

    RooDataSet_mlg_data = ROOT.RooDataSet("data","dataset",data_mlg_tree,ROOT.RooArgSet(m))
    RooDataHist_mlg_data = ROOT.RooDataHist("data","dataset",ROOT.RooArgList(m),inputs["data"])

    RooDataHist_mlg_wg = ROOT.RooDataHist("wg data hist","wg data hist",ROOT.RooArgList(m),inputs["wg"])
    RooHistPdf_wg = ROOT.RooHistPdf("wg","wg",ROOT.RooArgSet(m),RooDataHist_mlg_wg)

    wg_plus_fake_wg_contamination_hist = inputs["wg"].Clone("wg plus fake wg contamination hist")
    wg_plus_fake_wg_contamination_hist.Add(inputs["fake-wg-contamination"])

    RooDataHist_mlg_wg_plus_fake_wg_contamination = ROOT.RooDataHist("wg plus fake wg contamination","wg plus fake wg contamination",ROOT.RooArgList(m),wg_plus_fake_wg_contamination_hist)
    RooHistPdf_wg_plus_fake_wg_contamination = ROOT.RooHistPdf("wg plus fake wg contamination","wg plus fake wg contamination",ROOT.RooArgSet(m),RooDataHist_mlg_wg_plus_fake_wg_contamination)

    RooDataHist_mlg_vv = ROOT.RooDataHist("vv data hist","vv data hist",ROOT.RooArgList(m),inputs["vv"])
    RooHistPdf_vv = ROOT.RooHistPdf("vv","vv",ROOT.RooArgSet(m),RooDataHist_mlg_vv)

    RooDataHist_mlg_top = ROOT.RooDataHist("top data hist","top data hist",ROOT.RooArgList(m),inputs["top"])
    RooHistPdf_top = ROOT.RooHistPdf("top","top",ROOT.RooArgSet(m),RooDataHist_mlg_top)

    RooDataHist_mlg_zg = ROOT.RooDataHist("zg data hist","zg data hist",ROOT.RooArgList(m),inputs["zg"])
    RooHistPdf_zg = ROOT.RooHistPdf("zg","zg",ROOT.RooArgSet(m),RooDataHist_mlg_zg)

    RooDataHist_mlg_fake_lepton = ROOT.RooDataHist("fake lepton","fake lepton",ROOT.RooArgList(m),inputs["fake_lepton"])
    RooHistPdf_fake_lepton = ROOT.RooHistPdf("fake lepton","fake lepton",ROOT.RooArgSet(m),RooDataHist_mlg_fake_lepton)

    RooDataHist_mlg_fake_photon = ROOT.RooDataHist("fake photon","fake photon",ROOT.RooArgList(m),inputs["fake_photon"])
    RooHistPdf_fake_photon = ROOT.RooHistPdf("fake photon","fake photon",ROOT.RooArgSet(m),RooDataHist_mlg_fake_photon)

    RooDataHist_mlg_double_fake = ROOT.RooDataHist("double fake","double fake",ROOT.RooArgList(m),inputs["double_fake"])
    RooHistPdf_double_fake = ROOT.RooHistPdf("double fake","double fake",ROOT.RooArgSet(m),RooDataHist_mlg_double_fake)

    if inputs["lepton"] == "electron":
        RooDataHist_mlg_etog = ROOT.RooDataHist("etog data hist","etog data hist",ROOT.RooArgList(m),inputs["e_to_p_non_res"])
        RooHistPdf_etog = ROOT.RooHistPdf("etog","etog",ROOT.RooArgSet(m),RooDataHist_mlg_etog)

    top_norm = ROOT.RooRealVar("top_norm","top_norm",inputs["top"].Integral(),inputs["top"].Integral())    
    wg_norm = ROOT.RooRealVar("wg_norm","wg_norm",125594.,75000,200000);    
    wg_plus_fake_wg_contamination_norm = ROOT.RooRealVar("wg_plus_fake_wg_contamination_norm","wg_plus_fake_wg_contamination_norm",13234.2,0.5*13234.2,2*13234.2);    
#    zg_norm = ROOT.RooRealVar("zg_norm","zg_norm",0,1000000);    
    zg_norm = ROOT.RooRealVar("zg_norm","zg_norm",inputs["zg"].Integral(),inputs["zg"].Integral());    
    vv_norm = ROOT.RooRealVar("vv_norm","vv_norm",inputs["vv"].Integral(),inputs["vv"].Integral());    
    bwcb_norm = ROOT.RooRealVar("bwcb_norm","bwcb_norm",152671.0,0,1000000);    
    fake_lepton_norm = ROOT.RooRealVar("fake_lepton_norm","fake_lepton_norm",inputs["fake_lepton"].Integral(),inputs["fake_lepton"].Integral());    
    fake_photon_norm = ROOT.RooRealVar("fake_photon_norm","fake_photon_norm",inputs["fake_photon"].Integral(),inputs["fake_photon"].Integral());    
    double_fake_norm = ROOT.RooRealVar("double_fake_norm","double_fake_norm",inputs["double_fake"].Integral(),inputs["double_fake"].Integral());    
    if inputs["lepton"] == "electron":
        etog_norm = ROOT.RooRealVar("etog_norm","etog_norm",inputs["e_to_p_non_res"].Integral(),inputs["e_to_p_non_res"].Integral())

    n1=ROOT.RooRealVar("n1","n1",0.1,0.01,100000)
    n2=ROOT.RooRealVar("n2","n2",0.1,0.01,100000)

    f= ROOT.RooRealVar("f","f",0.5,0.,1.) ;

    if inputs["lepton"] == "electron" or inputs["lepton"] == "both":
        if options.float_fake_sig_cont:
            sum=ROOT.RooAddPdf("sum","sum",ROOT.RooArgList(RooHistPdf_wg_plus_fake_wg_contamination,RooHistPdf_zg,RooHistPdf_vv,RooFFTConvPdf_bwcb,RooHistPdf_fake_lepton,RooHistPdf_fake_photon,RooHistPdf_double_fake,RooHistPdf_top,RooHistPdf_etog),ROOT.RooArgList(wg_plus_fake_wg_contamination_norm,zg_norm,vv_norm,bwcb_norm,fake_lepton_norm,fake_photon_norm,double_fake_norm,top_norm,etog_norm))
        else:    
            sum=ROOT.RooAddPdf("sum","sum",ROOT.RooArgList(RooHistPdf_wg,RooHistPdf_zg,RooHistPdf_vv,RooFFTConvPdf_bwcb,RooHistPdf_fake_lepton,RooHistPdf_fake_photon,RooHistPdf_double_fake,RooHistPdf_top,RooHistPdf_etog),ROOT.RooArgList(wg_norm,zg_norm,vv_norm,bwcb_norm,fake_lepton_norm,fake_photon_norm,double_fake_norm,top_norm,etog_norm))        
    elif inputs["lepton"] == "muon":
        if options.float_fake_sig_cont:
            sum=ROOT.RooAddPdf("sum","sum",ROOT.RooArgList(RooHistPdf_wg_plus_fake_wg_contamination,RooHistPdf_zg,RooHistPdf_vv,RooHistPdf_fake_lepton,RooHistPdf_fake_photon,RooHistPdf_double_fake,RooHistPdf_top),ROOT.RooArgList(wg_plus_fake_wg_contamination_norm,zg_norm,vv_norm,fake_lepton_norm,fake_photon_norm,double_fake_norm,top_norm))
        else:    
            sum=ROOT.RooAddPdf("sum","sum",ROOT.RooArgList(RooHistPdf_wg,RooHistPdf_zg,RooHistPdf_vv,RooHistPdf_fake_lepton,RooHistPdf_fake_photon,RooHistPdf_double_fake,RooHistPdf_top),ROOT.RooArgList(wg_norm,zg_norm,vv_norm,fake_lepton_norm,fake_photon_norm,double_fake_norm,top_norm))
    else:
        assert(0)

    print "nfits = "+str(0)

    roofitresult=sum.fitTo(RooDataHist_mlg_data,ROOT.RooFit.Extended(),ROOT.RooFit.Strategy(2),ROOT.RooFit.Save())
    #roofitresult=sum.fitTo(RooDataHist_mlg_data,ROOT.RooFit.Extended(),ROOT.RooFit.Strategy(2))
    #sum.fitTo(RooDataSet_mlg_data,ROOT.RooFit.Extended())


    print "roofitresult.status() = "+str(roofitresult.status())

    nfits=1

    while roofitresult.status() != 0 and nfits < 10:     

        width.setVal(ROOT.TRandom(0).Uniform(3,4))
        bwcb_norm.setVal(ROOT.TRandom(0).Uniform(140000,160000))
        m0.setVal(ROOT.TRandom(0).Uniform(-2,2))
        mass.setVal(ROOT.TRandom(0).Uniform(88,92))

        print "nfits = "+str(nfits)
        roofitresult=sum.fitTo(RooDataHist_mlg_data,ROOT.RooFit.Extended(),ROOT.RooFit.Strategy(2),ROOT.RooFit.Save())
        print "roofitresult.status() = "+str(roofitresult.status())
        nfits+=1

    frame1 = m.frame()
    frame2 = m.frame(ROOT.RooFit.Range(0,200))

    RooDataHist_mlg_data.plotOn(frame1)
    RooDataHist_mlg_data.plotOn(frame2)
    #RooDataSet_mlg_data.plotOn(frame1)
    #RooDataSet_mlg_data.plotOn(frame2)
    sum.plotOn(frame1)
    sum.plotOn(frame2)
    #sum.plotOn(frame, ROOT.RooFit.Components(ROOT.RooArgSet(sum.getComponents()["zg"])),ROOT.RooFit.LineStyle(ROOT.kDashed)) 
    #sum.plotOn(frame, ROOT.RooFit.Components("zg,wg,bwcb"),ROOT.RooFit.LineStyle(ROOT.kDashed)) 

    red_th1f=ROOT.TH1D("red_th1f","red_th1f",1,0,1)
    red_th1f.SetLineColor(ROOT.kRed)
    red_th1f.SetLineWidth(3)
    red_th1f.SetLineStyle(ROOT.kDashed)
    green_th1f=ROOT.TH1D("green_th1f","green_th1f",1,0,1)
    green_th1f.SetLineColor(ROOT.kGreen)
    green_th1f.SetLineWidth(3)
    green_th1f.SetLineStyle(ROOT.kDashed)
    magenta_th1f=ROOT.TH1D("magenta_th1f","magenta_th1f",1,0,1)
    magenta_th1f.SetLineColor(ROOT.kMagenta)
    magenta_th1f.SetLineWidth(3)
    magenta_th1f.SetLineStyle(ROOT.kDashed)
    orangeminus1_th1f=ROOT.TH1D("orangeminus1_th1f","orangeminus_th1f",1,0,1)
    orangeminus1_th1f.SetLineColor(ROOT.kOrange-1)
    orangeminus1_th1f.SetLineWidth(3)
    orangeminus1_th1f.SetLineStyle(ROOT.kDashed)

    if inputs["lepton"] == "both" or inputs["lepton"] == "electron":
        sum.plotOn(frame1, ROOT.RooFit.Components("wg"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kRed)) 
        sum.plotOn(frame1, ROOT.RooFit.Components("zg"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kGreen)) 
        sum.plotOn(frame1, ROOT.RooFit.Components("bwcb"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kMagenta)) 
        sum.plotOn(frame2, ROOT.RooFit.Components("wg"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kRed)) 
        sum.plotOn(frame2, ROOT.RooFit.Components("zg"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kGreen)) 
        sum.plotOn(frame2, ROOT.RooFit.Components("bwcb"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kMagenta)) 

        legend1 = ROOT.TLegend(0.6, 0.7, 0.89, 0.89)
        legend1.SetBorderSize(0)  # no border
        legend1.SetFillStyle(0)  # make transparent
        legend1.AddEntry(red_th1f,"wg","lp")
        legend1.AddEntry(green_th1f,"zg","lp")
        legend1.AddEntry(magenta_th1f,"bwcb","lp")
    elif lepton_name == "muon":
        sum.plotOn(frame1, ROOT.RooFit.Components("wg"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kRed)) 
        sum.plotOn(frame1, ROOT.RooFit.Components("zg"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kGreen)) 
        sum.plotOn(frame2, ROOT.RooFit.Components("wg"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kRed)) 
        sum.plotOn(frame2, ROOT.RooFit.Components("zg"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kGreen)) 

        legend1 = ROOT.TLegend(0.6, 0.7, 0.89, 0.89)
        legend1.SetBorderSize(0)  # no border
        legend1.SetFillStyle(0)  # make transparent
        legend1.AddEntry(red_th1f,"wg","lp")
        legend1.AddEntry(green_th1f,"zg","lp")
    else:
        assert(0)

    frame1.SetTitle("")
    frame1.GetYaxis().SetTitle("")
    frame1.GetXaxis().SetTitle("m_{lg} (GeV)")
    frame2.SetTitle("")
    frame2.GetYaxis().SetTitle("")
    frame2.GetXaxis().SetTitle("m_{lg} (GeV)")
    
    c2 = ROOT.TCanvas("c2", "c2",5,50,500,500)
    
    frame1.Draw()
    
    legend1.Draw("same")
    
    c2.Update()
    c2.ForceUpdate()
    c2.Modified()

    if inputs["label"] == None:
        prefix = ""
    else:
        prefix = inputs["label"] + "_"

    c2.SaveAs(options.outputdir + "/" +prefix+"frame1.png")

    c2.Close()

    c3 = ROOT.TCanvas("c3", "c3",5,50,500,500)

    frame2.Draw()

    legend1.Draw("same")

    c3.Update()
    c3.ForceUpdate()
    c3.Modified()

    c3.SaveAs(options.outputdir + "/" +prefix + "frame2.png")

    c3.Close()

    frame3 = m.frame()
    frame4 = m.frame(ROOT.RooFit.Range(0,200))

    RooDataHist_mlg_data.plotOn(frame3)
    RooDataHist_mlg_data.plotOn(frame4)
    #RooDataSet_mlg_data.plotOn(frame3)
    #RooDataSet_mlg_data.plotOn(frame4)
    sum.plotOn(frame3)
    sum.plotOn(frame4)
    
    sum.plotOn(frame3, ROOT.RooFit.Components("fake photon"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kRed)) 
    sum.plotOn(frame3, ROOT.RooFit.Components("fake lepton"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kGreen)) 
    sum.plotOn(frame3, ROOT.RooFit.Components("double fake"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kMagenta)) 
    sum.plotOn(frame4, ROOT.RooFit.Components("fake photon"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kRed)) 
    sum.plotOn(frame4, ROOT.RooFit.Components("fake lepton"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kGreen)) 
    sum.plotOn(frame4, ROOT.RooFit.Components("double fake"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kMagenta)) 
    
    if inputs["lepton"] == "electron" or inputs["lepton"] == "both":
        sum.plotOn(frame3, ROOT.RooFit.Components("etog"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kOrange-1)) 
        sum.plotOn(frame4, ROOT.RooFit.Components("etog"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kOrange-1)) 

    frame3.SetTitle("")
    frame3.GetYaxis().SetTitle("")
    frame3.GetXaxis().SetTitle("m_{lg} (GeV)")
    frame4.SetTitle("")
    frame4.GetYaxis().SetTitle("")
    frame4.GetXaxis().SetTitle("m_{lg} (GeV)")

    legend2 = ROOT.TLegend(0.6, 0.7, 0.89, 0.89)
    legend2.SetBorderSize(0)  # no border
    legend2.SetFillStyle(0)  # make transparent
    legend2.AddEntry(red_th1f,"fake photon","lp")
    legend2.AddEntry(green_th1f,"fake lepton","lp")
    legend2.AddEntry(magenta_th1f,"double fake","lp")
    if inputs["lepton"] == "electron" or inputs["lepton"] == "both":
        legend2.AddEntry(orangeminus1_th1f,"e->g non-res","lp")

    c4 = ROOT.TCanvas("c4", "c4",5,50,500,500)

    frame3.Draw()
    
    legend2.Draw("same")
    
    c4.Update()
    c4.ForceUpdate()
    c4.Modified()
    
    c4.SaveAs(options.outputdir + "/" +prefix + "frame3.png")
    
    c4.Close()
    

    c5 = ROOT.TCanvas("c5", "c5",5,50,500,500)
    
    frame4.Draw()
    
    legend2.Draw("same")

    c5.Update()
    c5.ForceUpdate()
    c5.Modified()
    
    c5.SaveAs(options.outputdir + "/" +prefix + "frame4.png")
    
    c5.Close()

    mlg_fit_results = {}

    print "wg_plus_fake_wg_contamination_norm.getVal() = "+str(wg_plus_fake_wg_contamination_norm.getVal())
    print "wg_plus_fake_wg_contamination_norm.getVal()*inputs[\"wg\"].Integral()/(inputs[\"wg\"].Integral() + inputs[\"fake-wg-contamination\"]) = "+str(wg_plus_fake_wg_contamination_norm.getVal()*inputs["wg"].Integral()/(inputs["wg"].Integral() + inputs["fake-wg-contamination"].Integral()))

    mlg_fit_results["bwcb_norm"] = bwcb_norm.getVal()
    if options.float_fake_sig_cont:
        mlg_fit_results["wg_norm"] = wg_plus_fake_wg_contamination_norm.getVal()*inputs["wg"].Integral()/(inputs["wg"].Integral() + inputs["fake-wg-contamination"].Integral())
        mlg_fit_results["wg_norm_err"] = wg_plus_fake_wg_contamination_norm.getError()*inputs["wg"].Integral()/(inputs["wg"].Integral() + inputs["fake-wg-contamination"].Integral())
    else:
        mlg_fit_results["wg_norm"] = wg_norm.getVal()
        mlg_fit_results["wg_norm_err"] = wg_norm.getError()

    return mlg_fit_results

if lepton_name == "electron" and options.fit:
#if False:

    fit_inputs = {
        "label" : None,
        "lepton" : "electron",
        "data" : data["hists"][mlg_index],
        "top" : labels["top+jets"]["hists"][mlg_index],
        "zg" : labels["zg+jets"]["hists"][mlg_index],
        "vv" : labels["vv+jets"]["hists"][mlg_index],
        "wg" : labels["wg+jets"]["hists"][mlg_index],
        "fake-wg-contamination" : fake_signal_contamination["hists"][mlg_index],
        "e_to_p_non_res" : e_to_p_non_res["hists"][mlg_index],
        "fake_photon" : fake_photon["hists"][mlg_index],
        "fake_lepton" : fake_lepton["hists"][mlg_index],
        "double_fake" : double_fake["hists"][mlg_index]
        }

    fit_results = mlg_fit(fit_inputs)
    
    fit_inputs_fake_lepton_syst = dict(fit_inputs)
    fake_lepton_mlg_syst = fake_lepton["hists"][mlg_index].Clone("fake lepton syst")
    fake_lepton_mlg_syst.Scale(1.4)
    fit_inputs_fake_lepton_syst["label"] = "fake_lepton_syst"
    fit_inputs_fake_lepton_syst["fake_lepton"] = fake_lepton_mlg_syst
    fit_results_fake_lepton_syst = mlg_fit(fit_inputs_fake_lepton_syst)
    
    fit_inputs_fake_lepton_stat_up = dict(fit_inputs)
    fit_inputs_fake_lepton_stat_up["label"] = "fake_lepton_stat_up"
    fit_inputs_fake_lepton_stat_up["fake_lepton"] = fake_lepton_stat_up["hists"][mlg_index]
    fit_results_fake_lepton_stat_up = mlg_fit(fit_inputs_fake_lepton_stat_up)

    fit_inputs_pileup_up = dict(fit_inputs)
    fit_inputs_pileup_up["label"] = "pileup_up"
    fit_inputs_pileup_up["zg"] = labels["zg+jets"]["hists-pileup-up"][mlg_index]
    fit_inputs_pileup_up["wg"] = labels["wg+jets"]["hists-pileup-up"][mlg_index]
    fit_inputs_pileup_up["top"] = labels["top+jets"]["hists-pileup-up"][mlg_index]
    fit_inputs_pileup_up["vv"] = labels["vv+jets"]["hists-pileup-up"][mlg_index]
    fit_results_pileup_up = mlg_fit(fit_inputs_pileup_up)

    fit_inputs_prefire_up = dict(fit_inputs)
    fit_inputs_prefire_up["label"] = "prefire_up"
    fit_inputs_prefire_up["zg"] = labels["zg+jets"]["hists-prefire-up"][mlg_index]
    fit_inputs_prefire_up["wg"] = labels["wg+jets"]["hists-prefire-up"][mlg_index]
    fit_inputs_prefire_up["top"] = labels["top+jets"]["hists-prefire-up"][mlg_index]
    fit_inputs_prefire_up["vv"] = labels["vv+jets"]["hists-prefire-up"][mlg_index]
    fit_results_prefire_up = mlg_fit(fit_inputs_prefire_up)

    fit_inputs_jes_up = dict(fit_inputs)
    fit_inputs_jes_up["label"] = "jes_up"
    fit_inputs_jes_up["zg"] = labels["zg+jets"]["hists-jes-up"][mlg_index]
    fit_inputs_jes_up["wg"] = labels["wg+jets"]["hists-jes-up"][mlg_index]
    fit_inputs_jes_up["top"] = labels["top+jets"]["hists-jes-up"][mlg_index]
    fit_inputs_jes_up["vv"] = labels["vv+jets"]["hists-jes-up"][mlg_index]
    fit_results_jes_up = mlg_fit(fit_inputs_jes_up)

    fit_inputs_jer_up = dict(fit_inputs)
    fit_inputs_jer_up["label"] = "jer_up"
    fit_inputs_jer_up["zg"] = labels["zg+jets"]["hists-jer-up"][mlg_index]
    fit_inputs_jer_up["wg"] = labels["wg+jets"]["hists-jer-up"][mlg_index]
    fit_inputs_jer_up["top"] = labels["top+jets"]["hists-jer-up"][mlg_index]
    fit_inputs_jer_up["vv"] = labels["vv+jets"]["hists-jer-up"][mlg_index]
    fit_results_jer_up = mlg_fit(fit_inputs_jer_up)

    fit_inputs_fake_lepton_stat_down = dict(fit_inputs)
    fit_inputs_fake_lepton_stat_down["label"] = "fake_lepton_stat_down"
    fit_inputs_fake_lepton_stat_down["fake_lepton"] = fake_lepton_stat_down["hists"][mlg_index]
    fit_results_fake_lepton_stat_down = mlg_fit(fit_inputs_fake_lepton_stat_down)

    fit_inputs_fake_photon_alt = dict(fit_inputs)
    fit_inputs_fake_photon_alt["fake_photon"] = fake_photon_alt["hists"][mlg_index]
    fit_inputs_fake_photon_alt["label"] = "fake_photon_alt"
    fit_results_fake_photon_alt = mlg_fit(fit_inputs_fake_photon_alt)

    fit_inputs_fake_photon_wjets = dict(fit_inputs)
    fit_inputs_fake_photon_wjets["fake_photon"] = labels["w+jets"]["hists"][mlg_index].Clone("fake photon wjets")
    if options.no_wjets_for_2017_and_2018:
        fit_inputs_fake_photon_wjets["fake_photon"].Scale(fake_photon["hists"][mlg_index].Integral()/fake_photon_2016["hists"][mlg_index].Integral())
    fit_inputs_fake_photon_wjets["label"] = "fake_photon_wjets"
    fit_results_fake_photon_wjets = mlg_fit(fit_inputs_fake_photon_wjets)

    fit_inputs_lumi_up= dict(fit_inputs)
    fit_inputs_lumi_up["zg"] = labels["zg+jets"]["hists"][mlg_index].Clone("zg+jets lumi up")
    fit_inputs_lumi_up["zg"].Scale(1.025)
    fit_inputs_lumi_up["top"] = labels["top+jets"]["hists"][mlg_index].Clone("top+jets lumi up")
    fit_inputs_lumi_up["top"].Scale(1.025)
    fit_inputs_lumi_up["vv"] = labels["vv+jets"]["hists"][mlg_index].Clone("vv+jets lumi up")
    fit_inputs_lumi_up["vv"].Scale(1.025)
    fit_inputs_lumi_up["label"] = "lumi_up"
    fit_results_lumi_up = mlg_fit(fit_inputs_lumi_up)

    fit_results_fake_photon_stat_up = []

    for i in range(1,fake_photon["hists"][mlg_index].GetNbinsX()+1):
        fake_photon_mlg_stat_up = fake_photon["hists"][mlg_index].Clone("fake photon stat up bin "+ str(i))
        print str(fake_photon_mlg_stat_up.GetBinContent(i)) + " --> " + str(fake_photon_mlg_stat_up.GetBinContent(i)+fake_photon_mlg_stat_up.GetBinError(i))
        fake_photon_mlg_stat_up.SetBinContent(i,fake_photon_mlg_stat_up.GetBinContent(i)+fake_photon_mlg_stat_up.GetBinError(i))
        fit_inputs_fake_photon_stat_up = dict(fit_inputs)
        fit_inputs_fake_photon_stat_up["label"] = "fake_photon_stat_up_bin_"+str(i)
        fit_inputs_fake_photon_stat_up["fake_photon"] = fake_photon_mlg_stat_up
        fit_results_fake_photon_stat_up.append(mlg_fit(fit_inputs_fake_photon_stat_up))

    fit_results_fake_lepton_stat_up = []

    for i in range(1,fake_lepton["hists"][mlg_index].GetNbinsX()+1):
        fake_lepton_mlg_stat_up = fake_lepton["hists"][mlg_index].Clone("fake lepton stat up bin "+ str(i))
        print str(fake_lepton_mlg_stat_up.GetBinContent(i)) + " --> " + str(fake_lepton_mlg_stat_up.GetBinContent(i)+fake_lepton_mlg_stat_up.GetBinError(i))
        fake_lepton_mlg_stat_up.SetBinContent(i,fake_lepton_mlg_stat_up.GetBinContent(i)+fake_lepton_mlg_stat_up.GetBinError(i))
        fit_inputs_fake_lepton_stat_up = dict(fit_inputs)
        fit_inputs_fake_lepton_stat_up["label"] = "fake_lepton_stat_up_bin_"+str(i)
        fit_inputs_fake_lepton_stat_up["fake_lepton"] = fake_lepton_mlg_stat_up
        fit_results_fake_lepton_stat_up.append(mlg_fit(fit_inputs_fake_lepton_stat_up))

    fit_results_double_fake_stat_up = []

    for i in range(1,double_fake["hists"][mlg_index].GetNbinsX()+1):
        double_fake_mlg_stat_up = double_fake["hists"][mlg_index].Clone("fake lepton stat up bin "+ str(i))
        print str(double_fake_mlg_stat_up.GetBinContent(i)) + " --> " + str(double_fake_mlg_stat_up.GetBinContent(i)+double_fake_mlg_stat_up.GetBinError(i))
        double_fake_mlg_stat_up.SetBinContent(i,double_fake_mlg_stat_up.GetBinContent(i)+double_fake_mlg_stat_up.GetBinError(i))
        fit_inputs_double_fake_stat_up = dict(fit_inputs)
        fit_inputs_double_fake_stat_up["label"] = "double_fake_stat_up_bin_"+str(i)
        fit_inputs_double_fake_stat_up["double_fake"] = double_fake_mlg_stat_up
        fit_results_double_fake_stat_up.append(mlg_fit(fit_inputs_double_fake_stat_up))

    fit_results_zg_stat_up = []

    for i in range(1,labels["zg+jets"]["hists"][mlg_index].GetNbinsX()+1):
        zg_mlg_stat_up = labels["zg+jets"]["hists"][mlg_index].Clone("zg stat up bin "+ str(i))
        print str(zg_mlg_stat_up.GetBinContent(i)) + " --> " + str(zg_mlg_stat_up.GetBinContent(i)+zg_mlg_stat_up.GetBinError(i))
        zg_mlg_stat_up.SetBinContent(i,zg_mlg_stat_up.GetBinContent(i)+zg_mlg_stat_up.GetBinError(i))
        fit_inputs_zg_stat_up = dict(fit_inputs)
        fit_inputs_zg_stat_up["label"] = "zg_stat_up_bin_"+str(i)
        fit_inputs_zg_stat_up["zg"] = zg_mlg_stat_up
        fit_results_zg_stat_up.append(mlg_fit(fit_inputs_zg_stat_up))

    fit_results_vv_stat_up = []

    for i in range(1,labels["vv+jets"]["hists"][mlg_index].GetNbinsX()+1):
        vv_mlg_stat_up = labels["vv+jets"]["hists"][mlg_index].Clone("vv stat up bin "+ str(i))
        print str(vv_mlg_stat_up.GetBinContent(i)) + " --> " + str(vv_mlg_stat_up.GetBinContent(i)+vv_mlg_stat_up.GetBinError(i))
        vv_mlg_stat_up.SetBinContent(i,vv_mlg_stat_up.GetBinContent(i)+vv_mlg_stat_up.GetBinError(i))
        fit_inputs_vv_stat_up = dict(fit_inputs)
        fit_inputs_vv_stat_up["label"] = "vv_stat_up_bin_"+str(i)
        fit_inputs_vv_stat_up["vv"] = vv_mlg_stat_up
        fit_results_vv_stat_up.append(mlg_fit(fit_inputs_vv_stat_up))

    fit_results_top_stat_up = []

    for i in range(1,labels["top+jets"]["hists"][mlg_index].GetNbinsX()+1):
        top_mlg_stat_up = labels["top+jets"]["hists"][mlg_index].Clone("top stat up bin "+ str(i))
        print str(top_mlg_stat_up.GetBinContent(i)) + " --> " + str(top_mlg_stat_up.GetBinContent(i)+top_mlg_stat_up.GetBinError(i))
        top_mlg_stat_up.SetBinContent(i,top_mlg_stat_up.GetBinContent(i)+top_mlg_stat_up.GetBinError(i))
        fit_inputs_top_stat_up = dict(fit_inputs)
        fit_inputs_top_stat_up["label"] = "top_stat_up_bin_"+str(i)
        fit_inputs_top_stat_up["top"] = top_mlg_stat_up
        fit_results_top_stat_up.append(mlg_fit(fit_inputs_top_stat_up))


    if labels["zg+jets"]["syst-scale"]:    
        fit_results_zg_scale_variation = []

        for i in range(0,8): 
            fit_inputs_zg_scale_variation = dict(fit_inputs)
            fit_inputs_zg_scale_variation["label"] = "zg_scale_variation_"+str(i)
            fit_inputs_zg_scale_variation["zg"] = labels["zg+jets"]["hists-scale-variation"+str(i)][mlg_index]
            fit_results_zg_scale_variation.append(mlg_fit(fit_inputs_zg_scale_variation))


    if labels["zg+jets"]["syst-pdf"]:    
        fit_results_zg_pdf_variation = []
        
        for i in range(1,32): 
            fit_inputs_zg_pdf_variation = dict(fit_inputs)
            fit_inputs_zg_pdf_variation["label"] = "zg_pdf_variation_"+str(i)
            fit_inputs_zg_pdf_variation["zg"] = labels["zg+jets"]["hists-pdf-variation"+str(i)][mlg_index]
            fit_results_zg_pdf_variation.append(mlg_fit(fit_inputs_zg_pdf_variation))


if "wg+jets" in labels:
    prefire_unc = abs(labels["wg+jets"]["hists-prefire-up"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].Integral())
    pileup_unc = abs(labels["wg+jets"]["hists-pileup-up"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].Integral())
    jes_unc = abs(labels["wg+jets"]["hists-jes-up"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].Integral())
    jer_unc = abs(labels["wg+jets"]["hists-jer-up"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].Integral())
    electron_id_sf_unc = labels["wg+jets"]["hists-electron-id-sf-up"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].Integral()
    electron_reco_sf_unc = labels["wg+jets"]["hists-electron-reco-sf-up"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].Integral()
    electron_hlt_sf_unc = labels["wg+jets"]["hists-electron-hlt-sf-up"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].Integral()
    muon_id_sf_unc = labels["wg+jets"]["hists-muon-id-sf-up"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].Integral()
    muon_iso_sf_unc = labels["wg+jets"]["hists-muon-iso-sf-up"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].Integral()
    muon_hlt_sf_unc = labels["wg+jets"]["hists-muon-hlt-sf-up"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].Integral()
    photon_id_sf_unc = labels["wg+jets"]["hists-photon-id-sf-up"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].Integral()

    print labels["wg+jets"]["hists-muon-iso-sf-up"][mlg_index].Integral()
    print labels["wg+jets"]["hists"][mlg_index].Integral()

    print "(number of wg+jets events run over) = "+str(labels["wg+jets"]["samples"][year][0]["nweightedevents"])

    print "fiducial_region_cuts_efficiency = "+str(fiducial_region_cuts_efficiency)

if options.draw_ewdim6:
    for i in range(1,n_photon_pt_bins+1):
        #hardcoded to use bin 6 of the scaling histogram for now 
        ewdim6["hists"][0].SetBinContent(i,cb_scaling_hists[i].GetBinContent(7)*labels["wg+jets"]["hists"][0].GetBinContent(i))

c1 = ROOT.TCanvas("c1", "c1",5,50,500,500)

for i in range(len(variables)):

    if options.blind:
        data["hists"][i].Scale(0)

#    fake_lepton["hists"][i].Scale(2)

    fake_photon["hists"][i].Scale(1.0)

    data["hists"][i].Print("all")
    fake_photon["hists"][i].Print("all")
    fake_lepton["hists"][i].Print("all")
    if "wg+jets" in labels:
        labels["wg+jets"]["hists"][i].Print("all")
    if "w+jets" in labels:
        labels["w+jets"]["hists"][i].Print("all")

    data["hists"][i].SetMarkerStyle(ROOT.kFullCircle)
    data["hists"][i].SetLineWidth(3)
    data["hists"][i].SetLineColor(ROOT.kBlack)

    ewdim6["hists"][i].SetLineWidth(3)
    ewdim6["hists"][i].SetLineColor(ROOT.kOrange+3)

    fake_photon["hists"][i].SetFillColor(ROOT.kGray+1)
    fake_lepton["hists"][i].SetFillColor(ROOT.kAzure-1)
    double_fake["hists"][i].SetFillColor(ROOT.kMagenta)
    e_to_p["hists"][i].SetFillColor(ROOT.kSpring)
    e_to_p_non_res["hists"][i].SetFillColor(ROOT.kYellow)


    fake_photon["hists"][i].SetLineColor(ROOT.kGray+1)
    fake_lepton["hists"][i].SetLineColor(ROOT.kAzure-1)
    double_fake["hists"][i].SetLineColor(ROOT.kMagenta)
    e_to_p["hists"][i].SetLineColor(ROOT.kSpring)
    e_to_p_non_res["hists"][i].SetLineColor(ROOT.kYellow)


    fake_photon["hists"][i].SetFillStyle(1001)
    fake_lepton["hists"][i].SetFillStyle(1001)
    double_fake["hists"][i].SetFillStyle(1001)
    e_to_p["hists"][i].SetFillStyle(1001)
    e_to_p_non_res["hists"][i].SetFillStyle(1001)

    s=str(totallumi)+" fb^{-1} (13 TeV)"
    lumilabel = ROOT.TLatex (0.95, 0.93, s)
    lumilabel.SetNDC ()
    lumilabel.SetTextAlign (30)
    lumilabel.SetTextFont (42)
    lumilabel.SetTextSize (0.040)

    if "w+jets" in labels:
        wjets_fake_photon_2016["hists"][i].SetFillColor(labels["w+jets"]["color"])
        wjets_fake_photon_2016["hists"][i].SetFillStyle(1001)
        wjets_fake_photon_2016["hists"][i].SetLineColor(labels["w+jets"]["color"])
#
    hsum = data["hists"][i].Clone()
    hsum.Scale(0.0)

    hstack = ROOT.THStack()

    for label in labels.keys():
        if labels[label]["color"] == None:
            continue
        if options.closure_test and label == "wg+jets":
            continue

        if label == "w+jets":
            continue

        hsum.Add(labels[label]["hists"][i])
        hstack.Add(labels[label]["hists"][i])

    if options.use_wjets_for_fake_photon and "w+jets" in labels:
        hsum.Add(labels["w+jets"]["hists"][i])
        hstack.Add(labels["w+jets"]["hists"][i])
#        hsum.Add(wjets_fake_photon_2016["hists"][i])
#        hstack.Add(wjets_fake_photon_2016["hists"][i])

    if data_driven:
        if not options.use_wjets_for_fake_photon:
            hstack.Add(fake_photon["hists"][i])
        if not options.closure_test:
            hstack.Add(fake_lepton["hists"][i])
            hstack.Add(double_fake["hists"][i])

    if not options.closure_test and (lepton_name == "electron" or lepton_name == "both"): 
        if options.closure_test and label == "wg+jets":
            continue
        hsum.Add(e_to_p["hists"][i])
        hstack.Add(e_to_p["hists"][i])

    if not options.closure_test:    
        hsum.Add(e_to_p_non_res["hists"][i])
        hstack.Add(e_to_p_non_res["hists"][i])

    if data_driven:
        if not options.use_wjets_for_fake_photon:
            hsum.Add(fake_photon["hists"][i])
        if not options.closure_test:
            hsum.Add(fake_lepton["hists"][i])
            hsum.Add(double_fake["hists"][i])


    if data["hists"][i].GetMaximum() < hsum.GetMaximum():
        data["hists"][i].SetMaximum(hsum.GetMaximum()*1.55)
#        data["hists"][i].SetMaximum(hsum.GetMaximum()*2.55)
    else:
        data["hists"][i].SetMaximum(data["hists"][i].GetMaximum()*1.55)
#        data["hists"][i].SetMaximum(data["hists"][i].GetMaximum()*2.55)
        

    data["hists"][i].SetMinimum(0)
    hstack.SetMinimum(0)
    hsum.SetMinimum(0)

    data["hists"][i].Draw("")

    hstack.Draw("hist same")

    if options.draw_ewdim6:
        ewdim6["hists"][i].Print("all")
        ewdim6["hists"][i].Draw("same")
#wg_qcd.Draw("hist same")
#fake_lepton_hist.Draw("hist same")
#fake_photon_hist.Draw("hist same")

#wg_ewk_hist.Print("all")

#cmslabel = TLatex (0.18, 0.93, "#bf{CMS} (Unpublished)")
    cmslabel = ROOT.TLatex (0.18, 0.93, "")
    cmslabel.SetNDC ()
    cmslabel.SetTextAlign (10)
    cmslabel.SetTextFont (42)
    cmslabel.SetTextSize (0.040)
    cmslabel.Draw ("same") 
    
    lumilabel.Draw("same")

#wpwpjjewk.Draw("same")

    j=0
    if options.closure_test:
        draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,data["hists"][i],"w+jets","lp")
    else:    
        draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,data["hists"][i],"data","lp")

    if  options.use_wjets_for_fake_photon and "w+jets" in labels:
        j=j+1    
        draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,labels["w+jets"]["hists"][i],"w+jets","f")


    if data_driven :
        if not options.use_wjets_for_fake_photon:
            j=j+1
            draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,fake_photon["hists"][i],"fake photon","f")
        if not options.closure_test:
            j=j+1
            if lepton_name == "muon":
                draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,fake_lepton["hists"][i],"fake muon","f")
            elif lepton_name == "electron":
                draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,fake_lepton["hists"][i],"fake electron","f")
            elif lepton_name == "both":
                draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,fake_lepton["hists"][i],"fake lepton","f")
            else:
                assert(0)
            j=j+1
            draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,double_fake["hists"][i],"double fake","f")

    if (lepton_name == "electron" or lepton_name == "both") and not options.closure_test: 
        j=j+1
        draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,e_to_p["hists"][i],"e->#gamma","f")

    if not options.closure_test:
        j=j+1
        draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,e_to_p_non_res["hists"][i],"e->#gamma non-res","f")

    for label in labels.keys():
        if labels[label]["color"] == None:
            continue

        if options.closure_test and label == "wg+jets":
            continue

        if label == "w+jets":
            continue

        j=j+1    
#        draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,labels[label]["hists"][i],label,"f")
        if len(label) > 10:
            print "Warning: truncating the legend label "+str(label) + " to "+str(label[0:10]) 
            draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,labels[label]["hists"][i],label[0:10],"f")
        else:    
            draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,labels[label]["hists"][i],label,"f")

    if options.draw_ewdim6:
        j=j+1
        draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,ewdim6["hists"][i],"C_{WWW} = 2.0","l")

#set_axis_fonts(hstack,"x","m_{ll} (GeV)")
#set_axis_fonts(hstack,"x","|\Delta \eta_{jj}|")
    set_axis_fonts(data["hists"][i],"x",getXaxisLabel(variables[i]))
#set_axis_fonts(hstack,"x","pt_{l}^{max} (GeV)")
#set_axis_fonts(data_hist,"y","Events / bin")
#set_axis_fonts(hstack,"y","Events / bin")

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

    data["hists"][i].Draw("same")

    c1.Update()
    c1.ForceUpdate()
    c1.Modified()

    c1.SaveAs(options.outputdir + "/" + variables_labels[i] + ".png")

c1.Close()

if options.closure_test:
    sys.exit(0)

wg_jets_integral_error = ROOT.Double()
wg_jets_integral = labels["wg+jets"]["hists"][mlg_index].IntegralAndError(1,labels["wg+jets"]["hists"][mlg_index].GetXaxis().GetNbins(),wg_jets_integral_error)

zg_jets_integral_error = ROOT.Double()
zg_jets_integral = labels["zg+jets"]["hists"][mlg_index].IntegralAndError(1,labels["zg+jets"]["hists"][mlg_index].GetXaxis().GetNbins(),zg_jets_integral_error)

vv_jets_integral_error = ROOT.Double()
vv_jets_integral = labels["vv+jets"]["hists"][mlg_index].IntegralAndError(1,labels["vv+jets"]["hists"][mlg_index].GetXaxis().GetNbins(),vv_jets_integral_error)

top_jets_integral_error = ROOT.Double()
top_jets_integral = labels["top+jets"]["hists"][mlg_index].IntegralAndError(1,labels["top+jets"]["hists"][mlg_index].GetXaxis().GetNbins(),top_jets_integral_error)

fake_lepton_integral_error = ROOT.Double()
fake_lepton_integral = fake_lepton["hists"][mlg_index].IntegralAndError(1,fake_lepton["hists"][mlg_index].GetXaxis().GetNbins(),fake_lepton_integral_error)

fake_photon_integral_error = ROOT.Double()
fake_photon_integral = fake_photon["hists"][mlg_index].IntegralAndError(1,fake_photon["hists"][mlg_index].GetXaxis().GetNbins(),fake_photon_integral_error)

double_fake_integral_error = ROOT.Double()
double_fake_integral = double_fake["hists"][mlg_index].IntegralAndError(1,double_fake["hists"][mlg_index].GetXaxis().GetNbins(),double_fake_integral_error)

data_integral_error = ROOT.Double()
data_integral = data["hists"][mlg_index].IntegralAndError(1,data["hists"][mlg_index].GetXaxis().GetNbins(),data_integral_error)

e_to_p_integral_error = ROOT.Double()
e_to_p_integral = e_to_p["hists"][mlg_index].IntegralAndError(1,e_to_p["hists"][mlg_index].GetXaxis().GetNbins(),e_to_p_integral_error)

e_to_p_non_res_integral_error = ROOT.Double()
e_to_p_non_res_integral = e_to_p_non_res["hists"][mlg_index].IntegralAndError(1,e_to_p_non_res["hists"][mlg_index].GetXaxis().GetNbins(),e_to_p_non_res_integral_error)

fake_signal_contamination_integral_error = ROOT.Double()
fake_signal_contamination_integral = fake_signal_contamination["hists"][mlg_index].IntegralAndError(1,fake_signal_contamination["hists"][mlg_index].GetXaxis().GetNbins(),fake_signal_contamination_integral_error)

print "fake signal contamination = "+str(fake_signal_contamination_integral) + " +/- " +str(fake_signal_contamination_integral_error)

print "wg+jets = "+str(wg_jets_integral)+" +/- "+str(wg_jets_integral_error)
print "zg+jets = "+str(zg_jets_integral)+" +/- "+str(zg_jets_integral_error)
print "vv+jets = "+str(vv_jets_integral)+" +/- "+str(vv_jets_integral_error)
print "top+jets = "+str(top_jets_integral)+" +/- "+str(top_jets_integral_error)
print "fake photon = "+str(fake_photon_integral)+" +/- "+str(fake_photon_integral_error)
print "fake lepton = "+str(fake_lepton_integral)+" +/- "+str(fake_lepton_integral_error)
print "double fake = "+str(double_fake_integral)+" +/- "+str(double_fake_integral_error)
print "data = "+str(data_integral)+" +/- "+str(data_integral_error)
print "e_to_p = "+str(e_to_p_integral)+" +/- "+str(e_to_p_integral_error)
print "e_to_p_non_res = "+str(e_to_p_non_res_integral)+" +/- "+str(e_to_p_non_res_integral_error)

if options.fit:
    print "fit_results[\"bwcb_norm\"] = "+str(fit_results["bwcb_norm"])

n_signal = data_integral - double_fake_integral - fake_photon_integral - fake_lepton_integral - top_jets_integral - vv_jets_integral - zg_jets_integral - e_to_p_non_res_integral

n_signal_error = sqrt(pow(data_integral_error,2) + pow(double_fake_integral_error,2) + pow(fake_lepton_integral_error,2)+ pow(fake_photon_integral_error,2)+pow(top_jets_integral_error,2)+ pow(vv_jets_integral_error,2)+ pow(zg_jets_integral_error,2)+pow(e_to_p_non_res_integral_error,2))

print "n_signal = "+str(n_signal) + " +/- " + str(n_signal_error)

#labels["wg+jets"]["hists"]["photon_pt"].Print("all")

double_fake["hists"][mlg_index].Print("all")
fake_lepton["hists"][mlg_index].Print("all")
fake_photon["hists"][mlg_index].Print("all")
fake_photon_alt["hists"][mlg_index].Print("all")
fake_photon_stat_up["hists"][mlg_index].Print("all")

if lepton_name == "muon":

    xs_times_lumi = 0
    fiducial_xs_times_lumi = 0
    for year in years:
        if year == "2016":
            lumi=35.9
        elif year == "2017":
            lumi=41.5
        elif year == "2018":
            lumi=59.6
        else:
            assert(0)
        xs_times_lumi += labels["wg+jets"]["samples"][year][0]["xs"]*1000*lumi
        fiducial_xs_times_lumi += labels["wg+jets"]["samples"][year][0]["nweightedevents_passfiducial"]*labels["wg+jets"]["samples"][year][0]["xs"]*1000*lumi/labels["wg+jets"]["samples"][year][0]["nweightedevents"]

    xs_inputs_muon = {
        "lumi" : totallumi,
        "fiducial" : fiducial_xs_times_lumi,
        "fiducial_pass" : labels["wg+jets"]["hists-pass-fiducial"][mlg_index].Integral(),
        "xs_times_lumi" : xs_times_lumi,
        "signal_data_muon" : n_signal,
        "signal_mc_xs_data_mc" : labels["wg+jets"]["hists"][mlg_index].Integral(),
        "signal_syst_unc_due_to_pileup" : abs(labels["top+jets"]["hists-pileup-up"][mlg_index].Integral()+ labels["zg+jets"]["hists-pileup-up"][mlg_index].Integral()+labels["vv+jets"]["hists-pileup-up"][mlg_index].Integral()-labels["top+jets"]["hists"][mlg_index].Integral()- labels["zg+jets"]["hists"][mlg_index].Integral()-labels["vv+jets"]["hists"][mlg_index].Integral()),
        "signal_syst_unc_due_to_prefire" : abs(labels["top+jets"]["hists-prefire-up"][mlg_index].Integral()+ labels["zg+jets"]["hists-prefire-up"][mlg_index].Integral()+labels["vv+jets"]["hists-prefire-up"][mlg_index].Integral()-labels["top+jets"]["hists"][mlg_index].Integral()- labels["zg+jets"]["hists"][mlg_index].Integral()-labels["vv+jets"]["hists"][mlg_index].Integral()),
        "signal_syst_unc_due_to_jes" : abs(labels["top+jets"]["hists-jes-up"][mlg_index].Integral()+ labels["zg+jets"]["hists-jes-up"][mlg_index].Integral()+labels["vv+jets"]["hists-jes-up"][mlg_index].Integral()-labels["top+jets"]["hists"][mlg_index].Integral()- labels["zg+jets"]["hists"][mlg_index].Integral()-labels["vv+jets"]["hists"][mlg_index].Integral()),
        "signal_syst_unc_due_to_jer" : abs(labels["top+jets"]["hists-jer-up"][mlg_index].Integral()+ labels["zg+jets"]["hists-jer-up"][mlg_index].Integral()+labels["vv+jets"]["hists-jer-up"][mlg_index].Integral()-labels["top+jets"]["hists"][mlg_index].Integral()- labels["zg+jets"]["hists"][mlg_index].Integral()-labels["vv+jets"]["hists"][mlg_index].Integral()),
        "signal_syst_unc_due_to_fake_photon_alt_muon" : abs(fake_photon_alt["hists"][mlg_index].Integral() - fake_photon["hists"][mlg_index].Integral()),

        "signal_syst_unc_due_to_fake_lepton_muon" : abs(fake_lepton["hists"][mlg_index].Integral()*1.3 - fake_lepton["hists"][mlg_index].Integral()),
        "signal_stat_unc_muon" : n_signal_error,
        "signal_mc_xs_data_mc_syst_unc_due_to_prefire" : prefire_unc,
        "signal_mc_xs_data_mc_syst_unc_due_to_jes" : jes_unc,
        "signal_mc_xs_data_mc_syst_unc_due_to_jer" : jer_unc,
        "signal_mc_xs_data_mc_syst_unc_due_to_pileup" : pileup_unc,
        "signal_mc_xs_data_mc_syst_unc_due_to_muon_id_sf_muon" : muon_id_sf_unc,
        "signal_mc_xs_data_mc_syst_unc_due_to_muon_iso_sf_muon" : muon_iso_sf_unc,
        "signal_mc_xs_data_mc_syst_unc_due_to_muon_hlt_sf_muon" : muon_hlt_sf_unc,
        "signal_mc_xs_data_mc_syst_unc_due_to_photon_id_sf_muon" : photon_id_sf_unc
        }

    if options.no_wjets_for_2017_and_2018:
        xs_inputs_muon["signal_syst_unc_due_to_fake_photon_wjets_muon"] = abs(labels["w+jets"]["hists"][mlg_index].Integral() - fake_photon_2016["hists"][mlg_index].Integral())*fake_photon["hists"][mlg_index].Integral()/fake_photon_2016["hists"][mlg_index].Integral()
    else:    
        xs_inputs_muon["signal_syst_unc_due_to_fake_photon_wjets_muon"] = abs(labels["w+jets"]["hists"][mlg_index].Integral() - fake_photon["hists"][mlg_index].Integral())

    for i in range(1,32):
        xs_inputs_muon["signal_mc_xs_data_mc_pdf_variation"+str(i)] = labels["wg+jets"]["hists-pdf-variation"+str(i)][mlg_index].Integral()
        xs_times_lumi_pdf_variation = 0
        for year in years:
            if year == "2016":
                lumi=35.9
            elif year == "2017":
                lumi=41.5
            elif year == "2018":
                lumi=59.6
            else:
                assert(0)

            if (year == "2017" or year == "2018") and options.no_pdf_var_for_2017_and_2018:
                continue

            xs_times_lumi_pdf_variation += labels["wg+jets"]["samples"][year][0]["xs"]*1000*lumi*labels["wg+jets"]["samples"][year][0]["nweightedevents_pdfweight"+str(i)]/labels["wg+jets"]["samples"][year][0]["nweightedevents"]

        xs_inputs_muon["xs_times_lumi_pdf_variation"+str(i)] = xs_times_lumi_pdf_variation

    for i in range(0,8):
        xs_inputs_muon["signal_mc_xs_data_mc_scale_variation"+str(i)] = labels["wg+jets"]["hists-scale-variation"+str(i)][mlg_index].Integral() 
        xs_times_lumi_scale_variation = 0
        for year in years:
            if year == "2016":
                lumi=35.9
            elif year == "2017":
                lumi=41.5
            elif year == "2018":
                lumi=59.6
            else:
                assert(0)
            
            xs_times_lumi_scale_variation += labels["wg+jets"]["samples"][year][0]["xs"]*1000*lumi*labels["wg+jets"]["samples"][year][0]["nweightedevents_qcdscaleweight"+str(i)]/labels["wg+jets"]["samples"][year][0]["nweightedevents"]

        xs_inputs_muon["xs_times_lumi_scale_variation"+str(i)] = xs_times_lumi_scale_variation        


    for i in range(1,fake_photon["hists"][mlg_index].GetNbinsX()+1): 
        xs_inputs_muon["signal_syst_unc_due_to_fake_photon_stat_up_bin"+str(i)] = fake_photon["hists"][mlg_index].GetBinError(i)

    for i in range(1,fake_lepton["hists"][mlg_index].GetNbinsX()+1): 
        xs_inputs_muon["signal_syst_unc_due_to_fake_lepton_stat_up_bin"+str(i)] = fake_lepton["hists"][mlg_index].GetBinError(i)

    for i in range(1,double_fake["hists"][mlg_index].GetNbinsX()+1): 
        xs_inputs_muon["signal_syst_unc_due_to_double_fake_stat_up_bin"+str(i)] = double_fake["hists"][mlg_index].GetBinError(i)

    for i in range(1,labels["zg+jets"]["hists"][mlg_index].GetNbinsX()+1): 
        xs_inputs_muon["signal_syst_unc_due_to_zg_stat_up_bin"+str(i)] = labels["zg+jets"]["hists"][mlg_index].GetBinError(i)

    for i in range(1,labels["vv+jets"]["hists"][mlg_index].GetNbinsX()+1): 
        xs_inputs_muon["signal_syst_unc_due_to_vv_stat_up_bin"+str(i)] = labels["vv+jets"]["hists"][mlg_index].GetBinError(i)

    for i in range(1,labels["top+jets"]["hists"][mlg_index].GetNbinsX()+1): 
        xs_inputs_muon["signal_syst_unc_due_to_top_stat_up_bin"+str(i)] = labels["top+jets"]["hists"][mlg_index].GetBinError(i)

    if labels["zg+jets"]["syst-scale"]:    
        for i in range(0,8): 
            xs_inputs_muon["signal_syst_unc_due_to_zg_scale_variation"+str(i)] = labels["zg+jets"]["hists"][mlg_index].Integral() - labels["zg+jets"]["hists-scale-variation"+str(i)][mlg_index].Integral()

    if labels["zg+jets"]["syst-pdf"]:    
        for i in range(1,32): 
            xs_inputs_muon["signal_syst_unc_due_to_zg_pdf_variation"+str(i)] = labels["zg+jets"]["hists"][mlg_index].Integral() - labels["zg+jets"]["hists-pdf-variation"+str(i)][mlg_index].Integral()

    xs_inputs_muon["signal_syst_unc_due_to_lumi_up"] = abs(0.026*(labels["zg+jets"]["hists"][mlg_index].Integral()+labels["top+jets"]["hists"][mlg_index].Integral() + labels["vv+jets"]["hists"][mlg_index].Integral()) )

    pprint(xs_inputs_muon)

    import json

    f_muon = open("xs_inputs_muon.txt","w")

    json.dump(xs_inputs_muon,f_muon)

elif lepton_name == "electron":

    if options.fit:

        xs_times_lumi = 0
        for year in years:
            if year == "2016":
                lumi=35.9
            elif year == "2017":
                lumi=41.5
            elif year == "2018":
                lumi=59.6
            else:
                assert(0)
            xs_times_lumi += labels["wg+jets"]["samples"][year][0]["xs"]*1000*lumi

        xs_inputs_electron = {
            "lumi" : totallumi,
            "fiducial_region_cuts_efficiency":fiducial_region_cuts_efficiency,
            "xs_times_lumi" : xs_times_lumi,
            "signal_mc_xs_data_mc" : labels["wg+jets"]["hists"][mlg_index].Integral(),
            "signal_data_electron" : fit_results["wg_norm"],
            "signal_syst_unc_due_to_pileup" : abs(fit_results_pileup_up["wg_norm"]-fit_results["wg_norm"]),
            "signal_syst_unc_due_to_prefire" : abs(fit_results_prefire_up["wg_norm"]-fit_results["wg_norm"]),
            "signal_syst_unc_due_to_jes" : abs(fit_results_jes_up["wg_norm"]-fit_results["wg_norm"]),
            "signal_syst_unc_due_to_jer" : abs(fit_results_jer_up["wg_norm"]-fit_results["wg_norm"]),
            "signal_syst_unc_due_to_fake_photon_alt_electron" : abs(fit_results_fake_photon_alt["wg_norm"]-fit_results["wg_norm"]),
            "signal_syst_unc_due_to_fake_photon_wjets_electron" : abs(fit_results_fake_photon_wjets["wg_norm"]-fit_results["wg_norm"]),
            "signal_syst_unc_due_to_fake_lepton_electron" : abs(fit_results_fake_lepton_syst["wg_norm"]-fit_results["wg_norm"]),
            "signal_stat_unc_electron" : fit_results["wg_norm_err"],
            "signal_mc_xs_data_mc_electron" : labels["wg+jets"]["hists"][mlg_index].Integral(),
            "signal_mc_xs_data_mc_syst_unc_due_to_electron_id_sf_electron" : electron_id_sf_unc,
            "signal_mc_xs_data_mc_syst_unc_due_to_pileup" : pileup_unc,
            "signal_mc_xs_data_mc_syst_unc_due_to_prefire" : prefire_unc,
            "signal_mc_xs_data_mc_syst_unc_due_to_jer" : jer_unc,
            "signal_mc_xs_data_mc_syst_unc_due_to_jes" : jes_unc,
            "signal_mc_xs_data_mc_syst_unc_due_to_electron_reco_sf_electron" : electron_reco_sf_unc,
            "signal_mc_xs_data_mc_syst_unc_due_to_electron_hlt_sf_electron" : electron_hlt_sf_unc,
            "signal_mc_xs_data_mc_syst_unc_due_to_photon_id_sf_electron" : photon_id_sf_unc
            }

        for i in range(1,32):
            xs_inputs_electron["signal_mc_xs_data_mc_pdf_variation"+str(i)] = labels["wg+jets"]["hists-pdf-variation"+str(i)][mlg_index].Integral()
            xs_times_lumi_pdf_variation = 0
            for year in years:
                if year == "2016":
                    lumi=35.9
                elif year == "2017":
                    lumi=41.5
                elif year == "2018":
                    lumi=59.6
                else:
                    assert(0)

                if (year == "2017" or year == "2018") and options.no_pdf_var_for_2017_and_2018:
                    continue

                xs_times_lumi_pdf_variation += labels["wg+jets"]["samples"][year][0]["xs"]*1000*lumi*labels["wg+jets"]["samples"][year][0]["nweightedevents_pdfweight"+str(i)]/labels["wg+jets"]["samples"][year][0]["nweightedevents"]

            xs_inputs_electron["xs_times_lumi_pdf_variation"+str(i)] = xs_times_lumi_pdf_variation

        for i in range(0,8):
            xs_inputs_electron["signal_mc_xs_data_mc_scale_variation"+str(i)] = labels["wg+jets"]["hists-scale-variation"+str(i)][mlg_index].Integral()
            xs_times_lumi_scale_variation = 0
            for year in years:
                if year == "2016":
                    lumi=35.9
                elif year == "2017":
                    lumi=41.5
                elif year == "2018":
                    lumi=59.6
                else:
                    assert(0)

                xs_times_lumi_scale_variation += labels["wg+jets"]["samples"][year][0]["xs"]*1000*lumi*labels["wg+jets"]["samples"][year][0]["nweightedevents_qcdscaleweight"+str(i)]/labels["wg+jets"]["samples"][year][0]["nweightedevents"]

            xs_inputs_electron["xs_times_lumi_scale_variation"+str(i)] = xs_times_lumi_scale_variation        

        for i in range(1,fake_photon["hists"][mlg_index].GetNbinsX()+1): 
            xs_inputs_electron["signal_syst_unc_due_to_fake_photon_stat_up_bin"+str(i)] = abs(fit_results_fake_photon_stat_up[i-1]["wg_norm"] - fit_results["wg_norm"])

        for i in range(1,fake_lepton["hists"][mlg_index].GetNbinsX()+1): 
            xs_inputs_electron["signal_syst_unc_due_to_fake_lepton_stat_up_bin"+str(i)] = abs(fit_results_fake_lepton_stat_up[i-1]["wg_norm"] - fit_results["wg_norm"])

        for i in range(1,double_fake["hists"][mlg_index].GetNbinsX()+1): 
            xs_inputs_electron["signal_syst_unc_due_to_double_fake_stat_up_bin"+str(i)] = abs(fit_results_double_fake_stat_up[i-1]["wg_norm"] - fit_results["wg_norm"])

        for i in range(1,labels["zg+jets"]["hists"][mlg_index].GetNbinsX()+1): 
            xs_inputs_electron["signal_syst_unc_due_to_zg_stat_up_bin"+str(i)] = abs(fit_results_zg_stat_up[i-1]["wg_norm"] - fit_results["wg_norm"])

        for i in range(1,labels["vv+jets"]["hists"][mlg_index].GetNbinsX()+1): 
            xs_inputs_electron["signal_syst_unc_due_to_vv_stat_up_bin"+str(i)] = abs(fit_results_vv_stat_up[i-1]["wg_norm"] - fit_results["wg_norm"])

        for i in range(1,labels["top+jets"]["hists"][mlg_index].GetNbinsX()+1): 
            xs_inputs_electron["signal_syst_unc_due_to_top_stat_up_bin"+str(i)] = abs(fit_results_top_stat_up[i-1]["wg_norm"] - fit_results["wg_norm"])

        if labels["zg+jets"]["syst-scale"]:    
            for i in range(0,8): 
                xs_inputs_electron["signal_syst_unc_due_to_zg_scale_variation"+str(i)] = fit_results_zg_scale_variation[i]["wg_norm"] - fit_results["wg_norm"]

        if labels["zg+jets"]["syst-pdf"]:    
            for i in range(1,32): 
                xs_inputs_electron["signal_syst_unc_due_to_zg_pdf_variation"+str(i)] = fit_results_zg_pdf_variation[i-1]["wg_norm"] - fit_results["wg_norm"]

        xs_inputs_electron["signal_syst_unc_due_to_lumi_up"] = abs(fit_results_lumi_up["wg_norm"] - fit_results["wg_norm"])

    else:

        xs_times_lumi = 0
        fiducial_xs_times_lumi = 0
        for year in years:
            if year == "2016":
                lumi=35.9
            elif year == "2017":
                lumi=41.5
            elif year == "2018":
                lumi=59.6
            else:
                assert(0)
            xs_times_lumi += labels["wg+jets"]["samples"][year][0]["xs"]*1000*lumi
            fiducial_xs_times_lumi += labels["wg+jets"]["samples"][year][0]["nweightedevents_passfiducial"]*labels["wg+jets"]["samples"][year][0]["xs"]*1000*lumi/labels["wg+jets"]["samples"][year][0]["nweightedevents"]

        xs_inputs_electron = {
            "lumi" : totallumi,
            "fiducial" : fiducial_xs_times_lumi,
            "fiducial_pass" : labels["wg+jets"]["hists-pass-fiducial"][mlg_index].Integral(),
            "xs_times_lumi" : xs_times_lumi,
            "signal_data_electron" : n_signal,
            "signal_mc_xs_data_mc" : labels["wg+jets"]["hists"][mlg_index].Integral(),
            "signal_syst_unc_due_to_pileup" : abs(labels["top+jets"]["hists-pileup-up"][mlg_index].Integral()+ labels["zg+jets"]["hists-pileup-up"][mlg_index].Integral()+labels["vv+jets"]["hists-pileup-up"][mlg_index].Integral()-labels["top+jets"]["hists"][mlg_index].Integral()- labels["zg+jets"]["hists"][mlg_index].Integral()-labels["vv+jets"]["hists"][mlg_index].Integral()),
            "signal_syst_unc_due_to_prefire" : abs(labels["top+jets"]["hists-prefire-up"][mlg_index].Integral()+ labels["zg+jets"]["hists-prefire-up"][mlg_index].Integral()+labels["vv+jets"]["hists-prefire-up"][mlg_index].Integral()-labels["top+jets"]["hists"][mlg_index].Integral()- labels["zg+jets"]["hists"][mlg_index].Integral()-labels["vv+jets"]["hists"][mlg_index].Integral()),
            "signal_syst_unc_due_to_jes" : abs(labels["top+jets"]["hists-jes-up"][mlg_index].Integral()+ labels["zg+jets"]["hists-jes-up"][mlg_index].Integral()+labels["vv+jets"]["hists-jes-up"][mlg_index].Integral()-labels["top+jets"]["hists"][mlg_index].Integral()- labels["zg+jets"]["hists"][mlg_index].Integral()-labels["vv+jets"]["hists"][mlg_index].Integral()),
            "signal_syst_unc_due_to_jer" : abs(labels["top+jets"]["hists-jer-up"][mlg_index].Integral()+ labels["zg+jets"]["hists-jer-up"][mlg_index].Integral()+labels["vv+jets"]["hists-jer-up"][mlg_index].Integral()-labels["top+jets"]["hists"][mlg_index].Integral()- labels["zg+jets"]["hists"][mlg_index].Integral()-labels["vv+jets"]["hists"][mlg_index].Integral()),
            "signal_syst_unc_due_to_fake_photon_electron" : abs(fake_photon_alt["hists"][mlg_index].Integral() - fake_photon["hists"][mlg_index].Integral()),
            "signal_syst_unc_due_to_fake_lepton_electron" : abs(fake_lepton["hists"][mlg_index].Integral()*1.3 - fake_lepton["hists"][mlg_index].Integral()),
            "signal_stat_unc_electron" : n_signal_error,
            "signal_mc_xs_data_mc_syst_unc_due_to_pileup" : pileup_unc,
            "signal_mc_xs_data_mc_syst_unc_due_to_pileup" : prefire_unc,
            "signal_mc_xs_data_mc_syst_unc_due_to_jes" : jes_unc,
            "signal_mc_xs_data_mc_syst_unc_due_to_jer" : jer_unc,
            "signal_mc_xs_data_mc_syst_unc_due_to_electron_id_sf_electron" : electron_id_sf_unc,
            "signal_mc_xs_data_mc_syst_unc_due_to_electron_reco_sf_electron" : electron_reco_sf_unc,
            "signal_mc_xs_data_mc_syst_unc_due_to_electron_hlt_sf_electron" : electron_hlt_sf_unc,
            "signal_mc_xs_data_mc_syst_unc_due_to_photon_id_sf_electron" : photon_id_sf_unc
            }

        if options.no_wjets_for_2017_and_2018:
            xs_inputs_electron["signal_syst_unc_due_to_fake_photon_wjets_electron"] = abs(labels["w+jets"]["hists"][mlg_index].Integral() - fake_photon_2016["hists"][mlg_index].Integral())*fake_photon["hists"][mlg_index].Integral()/fake_photon_2016["hists"][mlg_index].Integral()
        else:    
            xs_inputs_electron["signal_syst_unc_due_to_fake_photon_wjets_electron"] = abs(labels["w+jets"]["hists"][mlg_index].Integral() - fake_photon["hists"][mlg_index].Integral())
        
        for i in range(1,32):
            xs_inputs_electron["signal_mc_xs_data_mc_pdf_variation"+str(i)] = labels["wg+jets"]["hists-pdf-variation"+str(i)][mlg_index].Integral()
            xs_times_lumi_pdf_variation = 0
            for year in years:
                if year == "2016":
                    lumi=35.9
                elif year == "2017":
                    lumi=41.5
                elif year == "2018":
                    lumi=59.6
                else:
                    assert(0)

                if (year == "2017" or year == "2018") and options.no_pdf_var_for_2017_and_2018:
                    continue

                xs_times_lumi_pdf_variation += labels["wg+jets"]["samples"][year][0]["xs"]*1000*lumi*labels["wg+jets"]["samples"][year][0]["nweightedevents_pdfweight"+str(i)]/labels["wg+jets"]["samples"][year][0]["nweightedevents"]

            xs_inputs_electron["xs_times_lumi_pdf_variation"+str(i)] = xs_times_lumi_pdf_variation

        for i in range(0,8):
            xs_inputs_electron["signal_mc_xs_data_mc_scale_variation"+str(i)] = labels["wg+jets"]["hists-scale-variation"+str(i)][mlg_index].Integral() 
            xs_times_lumi_scale_variation = 0
            for year in years:
                if year == "2016":
                    lumi=35.9
                elif year == "2017":
                    lumi=41.5
                elif year == "2018":
                    lumi=59.6
                else:
                    assert(0)
            
                xs_times_lumi_scale_variation += labels["wg+jets"]["samples"][year][0]["xs"]*1000*lumi*labels["wg+jets"]["samples"][year][0]["nweightedevents_qcdscaleweight"+str(i)]/labels["wg+jets"]["samples"][year][0]["nweightedevents"]

            xs_inputs_electron["xs_times_lumi_scale_variation"+str(i)] = xs_times_lumi_scale_variation        

        for i in range(1,fake_photon["hists"][mlg_index].GetNbinsX()+1): 
            xs_inputs_electron["signal_syst_unc_due_to_fake_photon_stat_up_bin"+str(i)] = fake_photon["hists"][mlg_index].GetBinError(i)

        for i in range(1,fake_lepton["hists"][mlg_index].GetNbinsX()+1): 
            xs_inputs_electron["signal_syst_unc_due_to_fake_lepton_stat_up_bin"+str(i)] = fake_lepton["hists"][mlg_index].GetBinError(i)

        for i in range(1,double_fake["hists"][mlg_index].GetNbinsX()+1): 
            xs_inputs_electron["signal_syst_unc_due_to_double_fake_stat_up_bin"+str(i)] = double_fake["hists"][mlg_index].GetBinError(i)

        for i in range(1,labels["zg+jets"]["hists"][mlg_index].GetNbinsX()+1): 
            xs_inputs_electron["signal_syst_unc_due_to_zg_stat_up_bin"+str(i)] = labels["zg+jets"]["hists"][mlg_index].GetBinError(i)

        for i in range(1,labels["vv+jets"]["hists"][mlg_index].GetNbinsX()+1): 
            xs_inputs_electron["signal_syst_unc_due_to_vv_stat_up_bin"+str(i)] = labels["vv+jets"]["hists"][mlg_index].GetBinError(i)

        for i in range(1,labels["top+jets"]["hists"][mlg_index].GetNbinsX()+1): 
            xs_inputs_electron["signal_syst_unc_due_to_top_stat_up_bin"+str(i)] = labels["top+jets"]["hists"][mlg_index].GetBinError(i)

        if labels["zg+jets"]["syst-scale"]:    
            for i in range(0,8): 
                xs_inputs_electron["signal_syst_unc_due_to_zg_scale_variation"+str(i)] = labels["zg+jets"]["hists"][mlg_index].Integral() - labels["zg+jets"]["hists-scale-variation"+str(i)][mlg_index].Integral()

        if labels["zg+jets"]["syst-pdf"]:    
            for i in range(1,32): 
                xs_inputs_electron["signal_syst_unc_due_to_zg_pdf_variation"+str(i)] = labels["zg+jets"]["hists"][mlg_index].Integral() - labels["zg+jets"]["hists-pdf-variation"+str(i)][mlg_index].Integral()

        xs_inputs_electron["signal_syst_unc_due_to_lumi_up"] = abs(0.026*(labels["zg+jets"]["hists"][mlg_index].Integral()+labels["top+jets"]["hists"][mlg_index].Integral() + labels["vv+jets"]["hists"][mlg_index].Integral()) )

    pprint(xs_inputs_electron)

    import json

    f_electron = open("xs_inputs_electron.txt","w")

    json.dump(xs_inputs_electron,f_electron)

#for i in range(fake_lepton["hists"][mlg_index].GetNbinsX()+2):
#    if fake_lepton["hists"][mlg_index].GetBinContent(i) < 0:
#        fake_lepton["hists"][mlg_index].SetBinContent(i,0.001)
#    if fake_photon["hists"][mlg_index].GetBinContent(i) < 0:
#        fake_photon["hists"][mlg_index].SetBinContent(i,0.001)
#    if fake_photon_alt["hists"][mlg_index].GetBinContent(i) < 0:
#        fake_photon_alt["hists"][mlg_index].SetBinContent(i,0.001)
#    if double_fake["hists"][mlg_index].GetBinContent(i) < 0:
#        double_fake["hists"][mlg_index].SetBinContent(i,0.001)
#    if e_to_p_non_res["hists"][mlg_index].GetBinContent(i) < 0:
#        e_to_p_non_res["hists"][mlg_index].SetBinContent(i,0.001)
#    if labels["w+jets"]["hists"][mlg_index].GetBinContent(i) < 0:
#        labels["w+jets"]["hists"][mlg_index].SetBinContent(i,0.001)

zgjets_pdf_syst=histogram_models[mlg_index].GetHistogram()

for i in range(labels["zg+jets"]["hists-pdf-variation0"][mlg_index].GetNbinsX()+1):
    mean_pdf=0

    for j in range(1,32):
        mean_pdf += labels["zg+jets"]["hists-pdf-variation"+str(j)][mlg_index].GetBinContent(i)

    mean_pdf = mean_pdf/31

    stddev_pdf = 0

    for j in range(1,32):
        stddev_pdf += pow(labels["zg+jets"]["hists-pdf-variation"+str(j)][mlg_index].GetBinContent(i) - mean_pdf,2)

    stddev_pdf = sqrt(stddev_pdf/(31-1))

    zgjets_pdf_syst.SetBinContent(i,labels["zg+jets"]["hists"][mlg_index].GetBinContent(i)+stddev_pdf)

zgjets_scale_syst=histogram_models[mlg_index].GetHistogram()

for i in range(labels["zg+jets"]["hists-scale-variation0"][mlg_index].GetNbinsX()+2):
    zgjets_scale_syst.SetBinContent(i,labels["zg+jets"]["hists"][mlg_index].GetBinContent(i)+max(
        abs(labels["zg+jets"]["hists-scale-variation0"][mlg_index].GetBinContent(i) - labels["zg+jets"]["hists"][mlg_index].GetBinContent(i)),
        abs(labels["zg+jets"]["hists-scale-variation1"][mlg_index].GetBinContent(i) - labels["zg+jets"]["hists"][mlg_index].GetBinContent(i)),
        abs(labels["zg+jets"]["hists-scale-variation3"][mlg_index].GetBinContent(i) - labels["zg+jets"]["hists"][mlg_index].GetBinContent(i)),
        abs(labels["zg+jets"]["hists-scale-variation4"][mlg_index].GetBinContent(i) - labels["zg+jets"]["hists"][mlg_index].GetBinContent(i)),
        abs(labels["zg+jets"]["hists-scale-variation5"][mlg_index].GetBinContent(i) - labels["zg+jets"]["hists"][mlg_index].GetBinContent(i)),
        abs(labels["zg+jets"]["hists-scale-variation6"][mlg_index].GetBinContent(i) - labels["zg+jets"]["hists"][mlg_index].GetBinContent(i))))

fake_electron_syst_up=histogram_models[mlg_index].GetHistogram()

fake_electron_syst_up.Add(fake_lepton["hists"][mlg_index])

fake_electron_syst_up.Scale(1.3)

trandom=ROOT.TRandom3()
trandom.SetSeed(0)

fake_photon_syst2_up=[]
fake_photon_syst2_up_relative=[]

#print "andrew debug 1"

#nnuisances = 100
nnuisances = histogram_models[mlg_index].GetHistogram().GetNbinsX()

#for i in range(1,fake_photon["hists"][mlg_index].GetNbinsX()+1):
#for i in range(1,histogram_models[mlg_index].GetHistogram().GetNbinsX()+1):
for i in range(1,nnuisances+1):
#for i in range(1,1000+1):
    fake_photon_syst2_up.append(histogram_models[mlg_index].GetHistogram())
    fake_photon_syst2_up_relative.append(histogram_models[mlg_index].GetHistogram())    

    sequence = []
    old = 0
    for j in range(histogram_models[mlg_index].GetHistogram().GetNbinsX()):
        if j == 0:
            old = trandom.Uniform(-1,1)
            sequence.append(old)
        else:
            found = False
            while (not found):
                new = trandom.Uniform(-1,1)

#                if abs(old - new) > 0.01:
                if False:
                    continue
                else:
                    old = new
                    sequence.append(old)
                    found = True


    for j in range(1,fake_photon["hists"][mlg_index].GetNbinsX()+1):
        if i == j:
#            if fake_photon_syst2_up[len(fake_photon_syst2_up)-1].GetXaxis().GetBinCenter(j) < 60:
#                fake_photon_syst2_up[len(fake_photon_syst2_up)-1].SetBinContent(j,fake_photon["hists"][mlg_index].GetBinContent(j)*1.2)
#            elif fake_photon_syst2_up[len(fake_photon_syst2_up)-1].GetXaxis().GetBinCenter(j) > 60 and fake_photon_syst2_up[len(fake_photon_syst2_up)-1].GetXaxis().GetBinCenter(j) < 120:
#                fake_photon_syst2_up[len(fake_photon_syst2_up)-1].SetBinContent(j,fake_photon["hists"][mlg_index].GetBinContent(j)*1.1)
#            elif fake_photon_syst2_up[len(fake_photon_syst2_up)-1].GetXaxis().GetBinCenter(j) > 120:
#                fake_photon_syst2_up[len(fake_photon_syst2_up)-1].SetBinContent(j,fake_photon["hists"][mlg_index].GetBinContent(j)*1.4)
#            else:
#                assert(0)

#        if True:
#        if j >= 0 and j <= 120 :
#            fake_photon_syst2_up[len(fake_photon_syst2_up)-1].SetBinContent(j,fake_photon["hists"][mlg_index].GetBinContent(j)+fake_photon["hists"][mlg_index].GetBinError(j))
#            fake_photon_syst2_up[len(fake_photon_syst2_up)-1].SetBinContent(j,fake_photon["hists"][mlg_index].GetBinContent(j)*1.2)
#            fake_photon_syst2_up[len(fake_photon_syst2_up)-1].SetBinContent(j,fake_photon["hists"][mlg_index].GetBinContent(j)*(1+sequence[j-1]))

#            non_closure.GetBinContent(non_closure[mlg_index].GetXaxis().FindFixBin(fake_photon["hists"][mlg_index].GetXaxis().GetBinCenter(j))

#            fake_photon_syst2_up[len(fake_photon_syst2_up)-1].SetBinContent(j,fake_photon["hists"][mlg_index].GetBinContent(j)*(1+non_closure[28].GetBinContent(non_closure[28].GetXaxis().FindFixBin(fake_photon["hists"][mlg_index].GetXaxis().GetBinCenter(j)))))

            bin =  non_closure[mlg_index].GetXaxis().FindFixBin(fake_photon["hists"][mlg_index].GetXaxis().GetBinCenter(j))

#            fake_photon_syst2_up_relative[len(fake_photon_syst2_up_relative)-1].SetBinContent(j,sequence[j-1]*non_closure[mlg_index].GetBinContent(non_closure[mlg_index].GetXaxis().FindFixBin(fake_photon["hists"][mlg_index].GetXaxis().GetBinCenter(j))))

            fake_photon_syst2_up_relative[len(fake_photon_syst2_up_relative)-1].SetBinContent(j,non_closure[mlg_index].GetBinContent(bin)+sequence[j-1]*non_closure[mlg_index].GetBinError(bin))            

#            fake_photon_syst2_up[len(fake_photon_syst2_up)-1].SetBinContent(j,fake_photon["hists"][mlg_index].GetBinContent(j)*(1+non_closure[mlg_index].GetBinContent(bin)+sequence[j-1]*non_closure[mlg_index].GetBinError(bin)/sqrt(nnuisances)))

#            fake_photon_syst2_up[len(fake_photon_syst2_up)-1].SetBinContent(j,fake_photon["hists"][mlg_index].GetBinContent(j)*(1+non_closure[mlg_index].GetBinContent(bin)+non_closure[mlg_index].GetBinError(bin)))

            fake_photon_syst2_up[len(fake_photon_syst2_up)-1].SetBinContent(j,fake_photon["hists"][mlg_index].GetBinContent(j)*(1+abs(non_closure[mlg_index].GetBinContent(bin))+non_closure[mlg_index].GetBinError(bin)))

#            fake_photon_syst2_up[len(fake_photon_syst2_up)-1].SetBinContent(j,fake_photon["hists"][mlg_index].GetBinContent(j)*(1+non_closure[mlg_index].GetBinContent(bin)))

#            fake_photon["hists"][mlg_index].SetBinError(j,fake_photon["hists"][mlg_index].GetBinContent(j)*(abs(non_closure[mlg_index].GetBinContent(bin))+non_closure[mlg_index].GetBinError(bin)))

#            fake_photon["hists"][mlg_index].SetBinError(j,0)

#            fake_photon["hists"][mlg_index].SetBinError(j,fake_photon["hists"][mlg_index].GetBinContent(j)*2)

        else:
            bin =  non_closure[mlg_index].GetXaxis().FindFixBin(fake_photon["hists"][mlg_index].GetXaxis().GetBinCenter(j))
#            fake_photon_syst2_up[len(fake_photon_syst2_up)-1].SetBinContent(j,fake_photon["hists"][mlg_index].GetBinContent(j)*(1+non_closure[mlg_index].GetBinContent(bin)))
            fake_photon_syst2_up[len(fake_photon_syst2_up)-1].SetBinContent(j,fake_photon["hists"][mlg_index].GetBinContent(j))

        fake_photon_syst2_up[len(fake_photon_syst2_up)-1].SetBinError(j,0)

#    fake_photon_syst2_up[len(fake_photon_syst2_up)-1].Scale(fake_photon["hists"][mlg_index].Integral()/fake_photon_syst2_up[len(fake_photon_syst2_up)-1].Integral())
#    fake_photon_syst2_up[len(fake_photon_syst2_up)-1].Scale(1/sqrt(histogram_models[mlg_index].GetHistogram().GetNbinsX()))

#for i in range(1,histogram_models[mlg_index].GetHistogram().GetNbinsX()+1):
#
#    if i == 1:
#        fake_photon["hists"][mlg_index].SetBinContent(i,fake_photon["hists"][mlg_index].GetBinContent(i)*(1+non_closure[mlg_index].GetBinContent(i)+non_closure[mlg_index].GetBinError(i)))
#    else:
#        fake_photon["hists"][mlg_index].SetBinContent(i,fake_photon["hists"][mlg_index].GetBinContent(i)*(1+non_closure[mlg_index].GetBinContent(i)))

#    fake_photon["hists"][mlg_index].SetBinError(i,fake_photon["hists"][mlg_index].GetBinContent(i)*(non_closure[mlg_index].GetBinError(i)))



fake_photon["hists"][mlg_index].SetLineWidth(2)

if len(fake_photon_syst2_up) > 4:

    fake_photon_syst2_up[0].SetLineColor(ROOT.kRed)
    fake_photon_syst2_up[1].SetLineColor(ROOT.kBlue)
    fake_photon_syst2_up[2].SetLineColor(ROOT.kGreen)
    fake_photon_syst2_up[3].SetLineColor(ROOT.kMagenta)
    fake_photon_syst2_up[4].SetLineColor(ROOT.kPink)
    
    fake_photon_syst2_up[0].SetLineWidth(2)
    fake_photon_syst2_up[1].SetLineWidth(2)
    fake_photon_syst2_up[2].SetLineWidth(2)
    fake_photon_syst2_up[3].SetLineWidth(2)
    fake_photon_syst2_up[4].SetLineWidth(2)

non_closure[mlg_index].SetLineWidth(2)

if len(fake_photon_syst2_up_relative) > 4:

    fake_photon_syst2_up_relative[0].SetLineColor(ROOT.kRed)
    fake_photon_syst2_up_relative[1].SetLineColor(ROOT.kBlue)
    fake_photon_syst2_up_relative[2].SetLineColor(ROOT.kGreen)
    fake_photon_syst2_up_relative[3].SetLineColor(ROOT.kMagenta)
    fake_photon_syst2_up_relative[4].SetLineColor(ROOT.kPink)

    fake_photon_syst2_up_relative[0].SetLineWidth(2)
    fake_photon_syst2_up_relative[1].SetLineWidth(2)
    fake_photon_syst2_up_relative[2].SetLineWidth(2)
    fake_photon_syst2_up_relative[3].SetLineWidth(2)
    fake_photon_syst2_up_relative[4].SetLineWidth(2)

c = ROOT.TCanvas("","")

if len(fake_photon_syst2_up) > 4:

    fake_photon["hists"][mlg_index].Draw()
    fake_photon_syst2_up[0].Draw("same")
    fake_photon_syst2_up[1].Draw("same")
    fake_photon_syst2_up[2].Draw("same")
    fake_photon_syst2_up[3].Draw("same")
    fake_photon_syst2_up[4].Draw("same")

c.SaveAs(options.outputdir + "/"+ "fake_photon_syst2.png")

if len(fake_photon_syst2_up_relative) > 4:

    non_closure[mlg_index].Draw()
    fake_photon_syst2_up_relative[0].Draw("same")
    fake_photon_syst2_up_relative[1].Draw("same")
    fake_photon_syst2_up_relative[2].Draw("same")
    #fake_photon_syst2_up_relative[3].Draw("same")
    #fake_photon_syst2_up_relative[4].Draw("same")

c.SaveAs(options.outputdir + "/"+ "fake_photon_syst2_relative.png")
c.Close()

fake_lepton_syst_up=[]

for i in range(1,fake_lepton["hists"][mlg_index].GetNbinsX()+1):
    fake_lepton_syst_up.append(histogram_models[mlg_index].GetHistogram())
    for j in range(1,fake_lepton["hists"][mlg_index].GetNbinsX()+1):
        if i == j:
#            fake_lepton_syst_up[len(fake_lepton_syst_up)-1].SetBinContent(j,fake_lepton["hists"][mlg_index].GetBinContent(j)+fake_lepton["hists"][mlg_index].GetBinError(j))
            fake_lepton_syst_up[len(fake_lepton_syst_up)-1].SetBinContent(j,1.3*fake_lepton["hists"][mlg_index].GetBinContent(j))
        else:
            fake_lepton_syst_up[len(fake_lepton_syst_up)-1].SetBinContent(j,fake_lepton["hists"][mlg_index].GetBinContent(j))
        fake_lepton_syst_up[len(fake_lepton_syst_up)-1].SetBinError(j,0)

zgjets_stat_up=[]

for i in range(1,labels["zg+jets"]["hists"][mlg_index].GetNbinsX()+1):
    zgjets_stat_up.append(histogram_models[mlg_index].GetHistogram())
    for j in range(1,labels["zg+jets"]["hists"][mlg_index].GetNbinsX()+1):
        if i == j:
            zgjets_stat_up[len(zgjets_stat_up)-1].SetBinContent(j,labels["zg+jets"]["hists"][mlg_index].GetBinContent(j)+labels["zg+jets"]["hists"][mlg_index].GetBinError(j))
        else:
            zgjets_stat_up[len(zgjets_stat_up)-1].SetBinContent(j,labels["zg+jets"]["hists"][mlg_index].GetBinContent(j))
        zgjets_stat_up[len(zgjets_stat_up)-1].SetBinError(j,0)

wg_stat_up=[]

for i in range(1,labels["wg+jets"]["hists"][mlg_index].GetNbinsX()+1):
    wg_stat_up.append(histogram_models[mlg_index].GetHistogram())
    for j in range(1,labels["wg+jets"]["hists"][mlg_index].GetNbinsX()+1):
        if i == j:
            wg_stat_up[len(wg_stat_up)-1].SetBinContent(j,labels["wg+jets"]["hists"][mlg_index].GetBinContent(j)+labels["wg+jets"]["hists"][mlg_index].GetBinError(j))
        else:    
            wg_stat_up[len(wg_stat_up)-1].SetBinContent(j,labels["wg+jets"]["hists"][mlg_index].GetBinContent(j))
        wg_stat_up[len(wg_stat_up)-1].SetBinError(j,0)

if options.make_cut_and_count_datacard:

    if options.lep == "muon":
        dcard = open("wg_dcard_cut_and_count_mu_chan.txt",'w')
    elif options.lep == "electron":
        dcard = open("wg_dcard_cut_and_count_el_chan.txt",'w')
    else:
        assert(0)

    print >> dcard, "imax 1 number of channels"
    print >> dcard, "jmax * number of background"
    print >> dcard, "kmax * number of nuisance parameters"

    print >> dcard, "Observation "+str(data["hists"][mlg_index].Integral())
    dcard.write("bin")

    if options.lep == "muon":
        dcard.write(" mu_chan")
        for label in labels.keys():
            if label == "no label" or label == "wg+jets" or label == "w+jets":
                continue
            dcard.write(" mu_chan")

        dcard.write(" mu_chan")
        dcard.write(" mu_chan")
        dcard.write(" mu_chan")
        dcard.write(" mu_chan")
        dcard.write('\n')    
    elif options.lep == "electron":
        dcard.write(" el_chan")
        for label in labels.keys():
            if label == "no label" or label == "wg+jets" or label == "w+jets":
                continue
            dcard.write(" el_chan")

        dcard.write(" el_chan")
        dcard.write(" el_chan")
        dcard.write(" el_chan")
        dcard.write(" el_chan")
        dcard.write('\n')    
    else:
        assert(0)

    dcard.write("process")
    dcard.write(" Wg")
        
    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" " + label.replace("+",""))

    dcard.write(" fake_photon")
    dcard.write(" fake_lepton")
    dcard.write(" double_fake")
    dcard.write(" e_to_p_non_res")
    dcard.write('\n')    
    dcard.write("process")
    dcard.write(" 0")

    for j in range(1,len(labels.keys())+2):
        dcard.write(" " + str(j))
    dcard.write('\n')    
    dcard.write('rate')
    dcard.write(' '+str(labels["wg+jets"]["hists"][mlg_index].Integral()))

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" "+ str(labels[label]["hists"][mlg_index].Integral()))

    dcard.write(" "+str(fake_photon["hists"][mlg_index].Integral())) 
    dcard.write(" "+str(fake_lepton["hists"][mlg_index].Integral())) 
    dcard.write(" "+str(double_fake["hists"][mlg_index].Integral())) 
    dcard.write(" "+str(e_to_p_non_res["hists"][mlg_index].Integral())) 
   
    dcard.write('\n')    

    dcard.write("lumi_13tev lnN")
    dcard.write(" 1.018")

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" 1.018")

    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" 1.018")
    
    dcard.write('\n')    

    dcard.write("pileup lnN")
    dcard.write(" "+str(labels["wg+jets"]["hists-pileup-up"][mlg_index].Integral()/labels["wg+jets"]["hists"][mlg_index].Integral()))

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" "+str(labels[label]["hists-pileup-up"][mlg_index].Integral()/labels[label]["hists"][mlg_index].Integral()))

    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")

    dcard.write('\n')    

    dcard.write("prefire lnN")
    dcard.write(" "+str(labels["wg+jets"]["hists-prefire-up"][mlg_index].Integral()/labels["wg+jets"]["hists"][mlg_index].Integral()))

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" "+str(labels[label]["hists-prefire-up"][mlg_index].Integral()/labels[label]["hists"][mlg_index].Integral()))

    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")

    dcard.write('\n')    

    dcard.write("jes lnN")
    dcard.write(" "+str(labels["wg+jets"]["hists-jes-up"][mlg_index].Integral()/labels["wg+jets"]["hists"][mlg_index].Integral()))

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" "+str(labels[label]["hists-jes-up"][mlg_index].Integral()/labels[label]["hists"][mlg_index].Integral()))

    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")

    dcard.write('\n')    

    dcard.write("jer lnN")
    dcard.write(" "+str(labels["wg+jets"]["hists-jer-up"][mlg_index].Integral()/labels["wg+jets"]["hists"][mlg_index].Integral()))

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" "+str(labels[label]["hists-jer-up"][mlg_index].Integral()/labels[label]["hists"][mlg_index].Integral()))

    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")

    dcard.write('\n')    

    dcard.write("muonidsf lnN")
    dcard.write(" "+str(labels["wg+jets"]["hists-muon-id-sf-up"][mlg_index].Integral()/labels["wg+jets"]["hists"][mlg_index].Integral()))

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" "+str(labels[label]["hists-muon-id-sf-up"][mlg_index].Integral()/labels[label]["hists"][mlg_index].Integral()))

    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")

    dcard.write('\n')    

    dcard.write("muonisosf lnN")
    dcard.write(" "+str(labels["wg+jets"]["hists-muon-iso-sf-up"][mlg_index].Integral()/labels["wg+jets"]["hists"][mlg_index].Integral()))

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" "+str(labels[label]["hists-muon-iso-sf-up"][mlg_index].Integral()/labels[label]["hists"][mlg_index].Integral()))

    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")

    dcard.write('\n')    

    dcard.write("muonhltsf lnN")
    dcard.write(" "+str(labels["wg+jets"]["hists-muon-hlt-sf-up"][mlg_index].Integral()/labels["wg+jets"]["hists"][mlg_index].Integral()))

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" "+str(labels[label]["hists-muon-hlt-sf-up"][mlg_index].Integral()/labels[label]["hists"][mlg_index].Integral()))

    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")

    dcard.write('\n')    

    dcard.write("fakephotonsyst1 lnN")
    dcard.write(" -")

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" -")

    dcard.write(" "+str(fake_photon_alt["hists"][mlg_index].Integral()/fake_photon["hists"][mlg_index].Integral()))
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")

    dcard.write('\n')    

    dcard.write("fakephotonsyst2 lnN")
    dcard.write(" -")

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" -")

    dcard.write(" "+str(labels["w+jets"]["hists"][mlg_index].Integral()/fake_photon["hists"][mlg_index].Integral()))
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")

    dcard.write('\n')    

    dcard.write("wgscale lnN")
    dcard.write(" "+str(1))

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" -")

    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")

    dcard.write('\n')    

    dcard.write("zgscale lnN")
    dcard.write(" -")

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        
        if label == "zg+jets":
            dcard.write(" "+str(zgjets_scale_syst.Integral()/(labels["zg+jets"]["hists"][mlg_index].Integral())))
        else:    
            dcard.write(" -")

    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")

    dcard.write('\n')    

    dcard.write("zgpdf lnN")
    dcard.write(" -")

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        
        if label == "zg+jets":
            dcard.write(" "+str(zgjets_pdf_syst.Integral()/(labels["zg+jets"]["hists"][mlg_index].Integral())))
        else:    
            dcard.write(" -")

    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")

    dcard.write('\n')    

    dcard.write("fakemuonsyst lnN")
    dcard.write(" -")

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" -")

    dcard.write(" -")
    dcard.write(" 1.3")
    dcard.write(" 1.3")
    dcard.write(" -")
    
    dcard.write('\n')    

if options.make_datacard:

    data["hists"][mlg_index].Scale(0)
    data["hists"][mlg_index].Add(labels["wg+jets"]["hists"][mlg_index])
    data["hists"][mlg_index].Add(labels["top+jets"]["hists"][mlg_index])
    data["hists"][mlg_index].Add(labels["zg+jets"]["hists"][mlg_index])
    data["hists"][mlg_index].Add(labels["vv+jets"]["hists"][mlg_index])
    data["hists"][mlg_index].Add(e_to_p_non_res["hists"][mlg_index])
    if options.lep == "electron":
        data["hists"][mlg_index].Add(e_to_p["hists"][mlg_index])
    data["hists"][mlg_index].Add(fake_photon["hists"][mlg_index])
    data["hists"][mlg_index].Add(fake_lepton["hists"][mlg_index])
    data["hists"][mlg_index].Add(double_fake["hists"][mlg_index])

    tmphist = fake_photon["hists"][mlg_index].Clone("tmphist")

    for i in range(1,histogram_models[mlg_index].GetHistogram().GetNbinsX()+1):
        if i == 1:
            if non_closure[mlg_index].GetBinContent(i) > 0:
                sign = 1
            else:
                sign = -1

#            fake_photon["hists"][mlg_index].SetBinContent(i,fake_photon["hists"][mlg_index].GetBinContent(i)*(1+non_closure[mlg_index].GetBinContent(i)+sign*non_closure[mlg_index].GetBinError(i)))
#        else:
#            fake_photon["hists"][mlg_index].SetBinContent(i,fake_photon["hists"][mlg_index].GetBinContent(i)*(1+non_closure[mlg_index].GetBinContent(i)))


    if options.lep == "muon":
        dcard = open("wg_dcard_mu_chan.txt",'w')
    elif options.lep == "electron":
        dcard = open("wg_dcard_el_chan.txt",'w')
    else:
        assert(0)
        
    print >> dcard, "imax 1 number of channels"
    print >> dcard, "jmax * number of background"
    print >> dcard, "kmax * number of nuisance parameters"

    if options.lep == "muon":
        print >> dcard, "shapes data_obs mu_chan wg_dcard_mu_chan_shapes.root data_obs"
        print >> dcard, "shapes Wg mu_chan wg_dcard_mu_chan_shapes.root wg wg_$SYSTEMATIC" 
    elif options.lep == "electron":
        print >> dcard, "shapes data_obs el_chan wg_dcard_el_chan_shapes.root data_obs"
        print >> dcard, "shapes Wg el_chan wg_dcard_el_chan_shapes.root wg wg_$SYSTEMATIC" 
    else:
        assert(0)    

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        if options.lep == "muon":
            print >> dcard, "shapes "+label.replace("+","")+" mu_chan wg_dcard_mu_chan_shapes.root "+label.replace("+","")+ " " +label.replace("+","") + "_$SYSTEMATIC" 
        elif options.lep == "electron":
            print >> dcard, "shapes "+label.replace("+","")+" el_chan wg_dcard_el_chan_shapes.root "+label.replace("+","")+ " " +label.replace("+","") + "_$SYSTEMATIC" 
        else:
            assert(0)    

    if options.lep == "muon":
        print >> dcard, "shapes fake_photon mu_chan wg_dcard_mu_chan_shapes.root fakephoton fakephoton_$SYSTEMATIC" 
        print >> dcard, "shapes fake_muon mu_chan wg_dcard_mu_chan_shapes.root fakemuon fakemuon_$SYSTEMATIC"
        print >> dcard, "shapes double_fake mu_chan wg_dcard_mu_chan_shapes.root doublefake doublefake_$SYSTEMATIC" 
        print >> dcard, "shapes e_to_p_non_res mu_chan wg_dcard_mu_chan_shapes.root etopnonres etopnonres_$SYSTEMATIC" 
    elif options.lep == "electron":
        print >> dcard, "shapes fake_photon el_chan wg_dcard_el_chan_shapes.root fakephoton fakephoton_$SYSTEMATIC" 
        print >> dcard, "shapes fake_electron el_chan wg_dcard_el_chan_shapes.root fakeelectron fakeelectron_$SYSTEMATIC"
        print >> dcard, "shapes double_fake el_chan wg_dcard_el_chan_shapes.root doublefake doublefake_$SYSTEMATIC" 
        print >> dcard, "shapes e_to_p_non_res el_chan wg_dcard_el_chan_shapes.root etopnonres etopnonres_$SYSTEMATIC" 
        print >> dcard, "shapes e_to_p el_chan wg_dcard_el_chan_shapes.root etop etop_$SYSTEMATIC" 
    else:
        assert(0)    

#    print >> dcard, "shapes data_obs el_chan wg_dcard_el_chan_shapes.root workspace:data_obs"
#    print >> dcard, "shapes Wg el_chan wg_dcard_el_chan_shapes.root workspace:wg workspace:wg_$SYSTEMATIC" 

#    for label in labels.keys():
#        if label == "no label" or label == "wg+jets" or label == "w+jets":
#            continue
#        print >> dcard, "shapes "+label.replace("+","")+" el_chan wg_dcard_el_chan_shapes.root workspace:"+label.replace("+","")+ " workspace:" +label.replace("+","") + "_$SYSTEMATIC" 

#    print >> dcard, "shapes fake_photon el_chan wg_dcard_el_chan_shapes.root workspace:fakephoton workspace:fakephoton_$SYSTEMATIC" 
#    print >> dcard, "shapes fake_electron el_chan wg_dcard_el_chan_shapes.root workspace:fakeelectron workspace:fakeelectron_$SYSTEMATIC"
#    print >> dcard, "shapes double_fake el_chan wg_dcard_el_chan_shapes.root workspace:doublefake workspace:doublefake_$SYSTEMATIC" 
#    print >> dcard, "shapes e_to_p_non_res el_chan wg_dcard_el_chan_shapes.root workspace:etopnonres workspace:etopnonres_$SYSTEMATIC" 
#    print >> dcard, "shapes e_to_p el_chan wg_dcard_el_chan_shapes.root workspace:etop workspace:etop_$SYSTEMATIC" 
    
    print >> dcard, "Observation "+str(data["hists"][mlg_index].Integral())
    dcard.write("bin")
    if options.lep == "muon":
        dcard.write(" mu_chan")
        for label in labels.keys():
            if label == "no label" or label == "wg+jets" or label == "w+jets":
                continue
            dcard.write(" mu_chan")
        dcard.write(" mu_chan")
        dcard.write(" mu_chan")
        dcard.write(" mu_chan")
        dcard.write(" mu_chan")
        dcard.write('\n')    
    elif options.lep == "electron":
        dcard.write(" el_chan")
        for label in labels.keys():
            if label == "no label" or label == "wg+jets" or label == "w+jets":
                continue
            dcard.write(" el_chan")
        dcard.write(" el_chan")
        dcard.write(" el_chan")
        dcard.write(" el_chan")
        dcard.write(" el_chan")
        dcard.write(" el_chan")
        dcard.write('\n')    
    else:
        assert(0)    

    dcard.write("process")
    dcard.write(" Wg")
        
    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" " + label.replace("+",""))

    dcard.write(" fake_photon")
    if options.lep == "muon":
        dcard.write(" fake_muon")
    elif options.lep == "electron":
        dcard.write(" fake_electron")
    else:
        assert(0)    
    dcard.write(" double_fake")
    dcard.write(" e_to_p_non_res")
    if options.lep == "muon":
        pass
    elif options.lep == "electron":
        dcard.write(" e_to_p")
    else:
        assert(0)    
    dcard.write('\n')    
    dcard.write("process")
    dcard.write(" 0")
    if options.lep == "muon":
        for j in range(1,len(labels.keys())+2):
            dcard.write(" " + str(j))
    elif options.lep == "electron":
        for j in range(1,len(labels.keys())+3):
            dcard.write(" " + str(j))
    else:
        assert(0)    
    dcard.write('\n')    
    dcard.write('rate')
    dcard.write(' '+str(labels["wg+jets"]["hists"][mlg_index].Integral()))

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" "+ str(labels[label]["hists"][mlg_index].Integral()))

    dcard.write(" "+str(fake_photon["hists"][mlg_index].Integral())) 
    dcard.write(" "+str(fake_lepton["hists"][mlg_index].Integral())) 
    dcard.write(" "+str(double_fake["hists"][mlg_index].Integral())) 
    dcard.write(" "+str(e_to_p_non_res["hists"][mlg_index].Integral())) 
    if options.lep == "muon":
        pass
    elif options.lep == "electron":
        dcard.write(" "+str(e_to_p["hists"][mlg_index].Integral())) 
    else:
        assert(0)    
    dcard.write('\n')    

    dcard.write("lumi_13tev lnN")
    dcard.write(" 1.018")

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" 1.018")

    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" 1.018")
    if options.lep == "muon":
        pass
    elif options.lep == "electron":
        dcard.write(" -")
    else:
        assert(0)    
    
    dcard.write('\n')    

    dcard.write("pileup shape1")
    dcard.write(" 1.0")

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" 1.0")

    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    if options.lep == "muon":
        pass
    elif options.lep == "electron":
        dcard.write(" -")
    else:
        assert(0)    

    dcard.write('\n')    

    dcard.write("prefire shape1")
    dcard.write(" 1.0")

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" 1.0")

    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    if options.lep == "muon":
        pass
    elif options.lep == "electron":
        dcard.write(" -")
    else:
        assert(0)    

    dcard.write('\n')    
    
    dcard.write("jes shape1")
    dcard.write(" 1.0")

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" 1.0")

    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    if options.lep == "muon":
        pass
    elif options.lep == "electron":
        dcard.write(" -")
    else:
        assert(0)    
    
    dcard.write('\n')    
    
    dcard.write("jer shape1")
    dcard.write(" 1.0")

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" 1.0")

    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    if options.lep == "muon":
        pass
    elif options.lep == "electron":
        dcard.write(" -")
    else:
        assert(0)    
    dcard.write('\n')    
    
    if options.lep == "muon":
        dcard.write("muonidsf shape1")
        dcard.write(" 1.0")
        for label in labels.keys():
            if label == "no label" or label == "wg+jets" or label == "w+jets":
                continue
            dcard.write(" 1.0")
        dcard.write(" -")
        dcard.write(" -")
        dcard.write(" -")
        dcard.write(" -")
        dcard.write('\n')    
        dcard.write("muonhltsf shape1")
        dcard.write(" 1.0")
        for label in labels.keys():
            if label == "no label" or label == "wg+jets" or label == "w+jets":
                continue
            dcard.write(" 1.0")
        dcard.write(" -")
        dcard.write(" -")
        dcard.write(" -")
        dcard.write(" -")
        dcard.write('\n')    
        dcard.write("muonisosf shape1")
        dcard.write(" 1.0")
        for label in labels.keys():
            if label == "no label" or label == "wg+jets" or label == "w+jets":
                continue
            dcard.write(" 1.0")
        dcard.write(" -")
        dcard.write(" -")
        dcard.write(" -")
        dcard.write(" -")
        dcard.write('\n')    
    elif options.lep == "electron":
        dcard.write("electronrecosf shape1")
        dcard.write(" 1.0")
        for label in labels.keys():
            if label == "no label" or label == "wg+jets" or label == "w+jets":
                continue
            dcard.write(" 1.0")
        dcard.write(" -")
        dcard.write(" -")
        dcard.write(" -")
        dcard.write(" -")
        dcard.write(" -")
        dcard.write('\n')    
        dcard.write("electronidsf shape1")
        dcard.write(" 1.0")
        for label in labels.keys():
            if label == "no label" or label == "wg+jets" or label == "w+jets":
                continue
            dcard.write(" 1.0")
        dcard.write(" -")
        dcard.write(" -")
        dcard.write(" -")
        dcard.write(" -")
        dcard.write(" -")
        dcard.write('\n')    
        dcard.write("electronhltsf shape1")
        dcard.write(" 1.0")
        for label in labels.keys():
            if label == "no label" or label == "wg+jets" or label == "w+jets":
                continue
            dcard.write(" 1.0")
        dcard.write(" -")
        dcard.write(" -")
        dcard.write(" -")
        dcard.write(" -")
        dcard.write(" -")
        dcard.write('\n')    
    else:
        assert(0)    
    
    dcard.write("fakephotonsyst1 shape1")
    dcard.write(" -")

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" -")

    dcard.write(" 1.0")
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    if options.lep == "muon":
        pass
    elif options.lep == "electron":
        dcard.write(" -")
    else:
        assert(0)    
    dcard.write('\n')    
    
#    dcard.write("fakephotonsyst2 lnN")
#    dcard.write(" -")

#    for label in labels.keys():
#        if label == "no label" or label == "wg+jets" or label == "w+jets":
#            continue
#        dcard.write(" -")

#    dcard.write(" 1.4")
#    dcard.write(" -")
#    dcard.write(" 1.4")
#    dcard.write(" -")
#    if options.lep == "muon":
#        pass
#    elif options.lep == "electron":
#        dcard.write(" -")
#    else:
#        assert(0)    
#    dcard.write('\n')    

#    dcard.write("fakeelectronsyst lnN")
#    dcard.write(" -")

#    for label in labels.keys():
#        if label == "no label" or label == "wg+jets" or label == "w+jets":
#            continue
#        dcard.write(" -")

#    dcard.write(" -")
#    dcard.write(" 1.3")
#    dcard.write(" 1.3")
#    dcard.write(" -")
#    if options.lep == "muon":
#        pass
#    elif options.lep == "electron":
#        dcard.write(" -")
#    else:
#        assert(0)    
#    dcard.write('\n')    
    
    dcard.write("wgscale shape1")
    dcard.write(" 1.0")

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" -")

    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    if options.lep == "muon":
        pass
    elif options.lep == "electron":
        dcard.write(" -")
    else:
        assert(0)    
    dcard.write('\n')    

    dcard.write("wgpdf shape1")
    dcard.write(" 1.0")

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" -")

    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    if options.lep == "muon":
        pass
    elif options.lep == "electron":
        dcard.write(" -")
    else:
        assert(0)    
    dcard.write('\n')    

    dcard.write("zgscale shape1")
    dcard.write(" -")

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        
        if label == "zg+jets":
            dcard.write(" 1.0")
        else:    
            dcard.write(" -")

    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    if options.lep == "muon":
        pass
    elif options.lep == "electron":
        dcard.write(" -")
    else:
        assert(0)    
    dcard.write('\n')    

    dcard.write("zgpdf shape1")
    dcard.write(" -")

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        
        if label == "zg+jets":
            dcard.write(" 1.0")
        else:    
            dcard.write(" -")

    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    if options.lep == "muon":
        pass
    elif options.lep == "electron":
        dcard.write(" -")
    else:
        assert(0)    
    dcard.write('\n')    

    dcard.write("* autoMCStats 0\n")
    if options.lep == "muon":
        pass
    elif options.lep == "electron":
        dcard.write("etopnorm rateParam el_chan e_to_p 2 [0,10]\n")
    else:
        assert(0)    


#    for i in range(1,labels["wg+jets"]["hists"][mlg_index].GetNbinsX()+1):
#        dcard.write("wgstatbin"+str(i)+" shape1")
#        dcard.write(" 1.0")

#        for label in labels.keys():
#            if label == "no label" or label == "wg+jets" or label == "w+jets":
#                continue
#            dcard.write(" -")
        
#        dcard.write(" -")
#        dcard.write(" -")
#        dcard.write(" -")
#        dcard.write(" -")
#        dcard.write(" -")

#        dcard.write('\n')    

#    for i in range(1,fake_photon["hists"][mlg_index].GetNbinsX()+1):
    for i in range(1,len(fake_photon_syst2_up)+1):
        dcard.write("fakephotonsyst2var"+str(i)+" shape1")
        dcard.write(" -")

        for label in labels.keys():
            if label == "no label" or label == "wg+jets" or label == "w+jets":
                continue
            dcard.write(" -")
        
        dcard.write(" 1.0")
        dcard.write(" -")
        dcard.write(" -")
        dcard.write(" -")
        if options.lep == "muon":
            pass
        elif options.lep == "electron":
            dcard.write(" -")
        else:
            assert(0)    

        dcard.write('\n')    

    for i in range(1,fake_photon["hists"][mlg_index].GetNbinsX()+1):
        if options.lep == "muon":
            dcard.write("fakemuonsystbin"+str(i)+" shape1")
        elif options.lep == "electron":
            dcard.write("fakeelectronsystbin"+str(i)+" shape1")
        else:
            assert(0)

        dcard.write(" -")

        for label in labels.keys():
            if label == "no label" or label == "wg+jets" or label == "w+jets":
                continue
            dcard.write(" -")
        
        dcard.write(" -")
        dcard.write(" 1.0")
        dcard.write(" -")
        dcard.write(" -")
        dcard.write(" -")
        if options.lep == "muon":
            pass
        elif options.lep == "electron":
            dcard.write(" -")
        else:
            assert(0)    

        dcard.write('\n')    

#    for i in range(1,labels["zg+jets"]["hists"][mlg_index].GetNbinsX()+1):
#        dcard.write("zgjetsstatbin"+str(i)+" shape1")
#        dcard.write(" -")

#        for label in labels.keys():
#            if label == "no label" or label == "wg+jets" or label == "w+jets":
#                continue
            
#            if label == "zg+jets":
#                dcard.write(" 1.0")
#            else:    
#                dcard.write(" -")
        
#        dcard.write(" -")
#        dcard.write(" -")
#        dcard.write(" -")
#        dcard.write(" -")
#        dcard.write(" -")

#        dcard.write('\n')    

    dcard.close()

    if options.lep == "muon":
        shapes = ROOT.TFile.Open("wg_dcard_mu_chan_shapes.root","recreate")        
    elif options.lep == "electron":
        shapes = ROOT.TFile.Open("wg_dcard_el_chan_shapes.root","recreate")
    else:
        assert(0)    

    shapes.cd()

    tmphist.Write("tmphist")

    fake_photon["hists"][mlg_index].SetBinContent(fake_photon["hists"][mlg_index].GetNbinsX()+1,0)
    fake_photon["hists"][mlg_index].SetBinError(fake_photon["hists"][mlg_index].GetNbinsX()+1,0)
    fake_photon["hists"][mlg_index].SetBinContent(0,0)
    fake_photon["hists"][mlg_index].SetBinError(0,0)

    data["hists"][mlg_index].Write("data_obs")
    labels["wg+jets"]["hists"][mlg_index].Write("wg")
    labels["top+jets"]["hists"][mlg_index].Write("topjets")
    labels["zg+jets"]["hists"][mlg_index].Write("zgjets")
    labels["vv+jets"]["hists"][mlg_index].Write("vvjets")
    e_to_p_non_res["hists"][mlg_index].Write("etopnonres")
    e_to_p["hists"][mlg_index].Write("etop")

#    tmphist=labels["wg+jets"]["hists"][mlg_index].Clone("")
#    tmphist.Scale(fake_photon["hists"][mlg_index].Integral()/tmphist.Integral())
#    tmphist.Write("fakephoton")
    fake_photon["hists"][mlg_index].Write("fakephoton")
    if options.lep == "muon":
        fake_lepton["hists"][mlg_index].Write("fakemuon")
    elif options.lep == "electron":
        fake_lepton["hists"][mlg_index].Write("fakeelectron")
    else:
        assert(0)    

    double_fake["hists"][mlg_index].Write("doublefake")

    zgjets_scale_syst.Write("zgjets_zgscaleUp")
    makeDownShape(zgjets_scale_syst,labels["zg+jets"]["hists"][mlg_index]).Write("zgjets_zgscaleDown")

    zgjets_pdf_syst.Write("zgjets_zgpdfUp")
    makeDownShape(zgjets_pdf_syst,labels["zg+jets"]["hists"][mlg_index]).Write("zgjets_zgpdfDown")

    wgjets_pdf_syst=histogram_models[mlg_index].GetHistogram()

    for i in range(labels["wg+jets"]["hists-pdf-variation0"][mlg_index].GetNbinsX()+1):
        mean_pdf=0

        for j in range(1,32):
            mean_pdf += labels["wg+jets"]["hists-pdf-variation"+str(j)][mlg_index].GetBinContent(i)*labels["wg+jets"]["hists"][mlg_index].Integral()/labels["wg+jets"]["hists-pdf-variation"+str(j)][mlg_index].Integral()

        mean_pdf = mean_pdf/31

        stddev_pdf = 0

        for j in range(1,32):
            stddev_pdf += pow(labels["wg+jets"]["hists-pdf-variation"+str(j)][mlg_index].GetBinContent(i)*labels["wg+jets"]["hists"][mlg_index].Integral()/labels["wg+jets"]["hists-pdf-variation"+str(j)][mlg_index].Integral() - mean_pdf,2)

        stddev_pdf = sqrt(stddev_pdf/(31-1))

        wgjets_pdf_syst.SetBinContent(i,labels["wg+jets"]["hists"][mlg_index].GetBinContent(i)+stddev_pdf)

    wgjets_scale_syst=histogram_models[mlg_index].GetHistogram()

    for i in range(labels["wg+jets"]["hists-scale-variation0"][mlg_index].GetNbinsX()+1):
        wgjets_scale_syst.SetBinContent(i,labels["wg+jets"]["hists"][mlg_index].GetBinContent(i)+labels["wg+jets"]["hists"][mlg_index].Integral()*max(
            abs(labels["wg+jets"]["hists-scale-variation0"][mlg_index].GetBinContent(i)/labels["wg+jets"]["hists-scale-variation0"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].GetBinContent(i)/labels["wg+jets"]["hists"][mlg_index].Integral()),
            abs(labels["wg+jets"]["hists-scale-variation1"][mlg_index].GetBinContent(i)/labels["wg+jets"]["hists-scale-variation1"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].GetBinContent(i)/labels["wg+jets"]["hists"][mlg_index].Integral()),
            abs(labels["wg+jets"]["hists-scale-variation3"][mlg_index].GetBinContent(i)/labels["wg+jets"]["hists-scale-variation3"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].GetBinContent(i)/labels["wg+jets"]["hists"][mlg_index].Integral()),
            abs(labels["wg+jets"]["hists-scale-variation4"][mlg_index].GetBinContent(i)/labels["wg+jets"]["hists-scale-variation4"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].GetBinContent(i)/labels["wg+jets"]["hists"][mlg_index].Integral()),
            abs(labels["wg+jets"]["hists-scale-variation5"][mlg_index].GetBinContent(i)/labels["wg+jets"]["hists-scale-variation5"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].GetBinContent(i)/labels["wg+jets"]["hists"][mlg_index].Integral()),
            abs(labels["wg+jets"]["hists-scale-variation6"][mlg_index].GetBinContent(i)/labels["wg+jets"]["hists-scale-variation6"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].GetBinContent(i)/labels["wg+jets"]["hists"][mlg_index].Integral())))
    
    for i in range(1,labels["wg+jets"]["hists"][mlg_index].GetNbinsX()+1):
        wg_stat_up[i-1].Write("wg_wgstatbin"+str(i)+"Up")
        makeDownShape(wg_stat_up[i-1],labels["wg+jets"]["hists"][mlg_index]).Write("wg_wgstatbin"+str(i)+"Down")

    for i in range(1,len(fake_photon_syst2_up)+1):
        fake_photon_syst2_up[i-1].Write("fakephoton_fakephotonsyst2var"+str(i)+"Up")
#        fake_photon_syst2_up[i-1].Write("fakephoton_fakephotonsyst2var"+str(i)+"Down")
        fake_photon["hists"][mlg_index].Write("fakephoton_fakephotonsyst2var"+str(i)+"Down")
#        makeDownShape(fake_photon_syst2_up[i-1],fake_photon["hists"][mlg_index]).Write("fakephoton_fakephotonsyst2var"+str(i)+"Down")

    for i in range(1,fake_lepton["hists"][mlg_index].GetNbinsX()+1):
        if options.lep == "electron":
            fake_lepton_syst_up[i-1].Write("fakeelectron_fakeelectronsystbin"+str(i)+"Up")
            makeDownShape(fake_lepton_syst_up[i-1],fake_lepton["hists"][mlg_index]).Write("fakeelectron_fakeelectronsystbin"+str(i)+"Down")
        elif options.lep == "muon":
            fake_lepton_syst_up[i-1].Write("fakemuon_fakemuonsystbin"+str(i)+"Up")
            makeDownShape(fake_lepton_syst_up[i-1],fake_lepton["hists"][mlg_index]).Write("fakemuon_fakemuonsystbin"+str(i)+"Down")
        else:
            assert(0)

    for i in range(1,labels["zg+jets"]["hists"][mlg_index].GetNbinsX()+1):
        zgjets_stat_up[i-1].Write("zgjets_zgjetsstatbin"+str(i)+"Up")
        makeDownShape(zgjets_stat_up[i-1],labels["zg+jets"]["hists"][mlg_index]).Write("zgjets_zgjetsstatbin"+str(i)+"Down")

    wgjets_scale_syst.Write("wg_wgscaleUp")
    makeDownShape(wgjets_scale_syst,labels["wg+jets"]["hists"][mlg_index]).Write("wg_wgscaleDown")

    wgjets_pdf_syst.Write("wg_wgpdfUp")
    makeDownShape(wgjets_pdf_syst,labels["wg+jets"]["hists"][mlg_index]).Write("wg_wgpdfDown")

    fake_photon_alt["hists"][mlg_index].Write("fakephoton_fakephotonsyst1Up")
    makeDownShape(fake_photon_alt["hists"][mlg_index],fake_photon["hists"][mlg_index]).Write("fakephoton_fakephotonsyst1Down")

    labels["w+jets"]["hists"][mlg_index].Write("fakephoton_fakephotonsyst2Up")
    makeDownShape(labels["w+jets"]["hists"][mlg_index],fake_photon["hists"][mlg_index]).Write("fakephoton_fakephotonsyst2Down")

    labels["top+jets"]["hists-pileup-up"][mlg_index].Write("topjets_pileupUp")
    makeDownShape(labels["top+jets"]["hists-pileup-up"][mlg_index],labels["top+jets"]["hists"][mlg_index]).Write("topjets_pileupDown")
    labels["zg+jets"]["hists-pileup-up"][mlg_index].Write("zgjets_pileupUp")
    makeDownShape(labels["zg+jets"]["hists-pileup-up"][mlg_index],labels["zg+jets"]["hists"][mlg_index]).Write("zgjets_pileupDown")
    labels["vv+jets"]["hists-pileup-up"][mlg_index].Write("vvjets_pileupUp")
    makeDownShape(labels["vv+jets"]["hists-pileup-up"][mlg_index],labels["vv+jets"]["hists"][mlg_index]).Write("vvjets_pileupDown")
    labels["wg+jets"]["hists-pileup-up"][mlg_index].Write("wg_pileupUp")
    makeDownShape(labels["wg+jets"]["hists-pileup-up"][mlg_index],labels["wg+jets"]["hists"][mlg_index]).Write("wg_pileupDown")
    
    labels["top+jets"]["hists-prefire-up"][mlg_index].Write("topjets_prefireUp")
    makeDownShape(labels["top+jets"]["hists-prefire-up"][mlg_index],labels["top+jets"]["hists"][mlg_index]).Write("topjets_prefireDown")
    labels["zg+jets"]["hists-prefire-up"][mlg_index].Write("zgjets_prefireUp")
    makeDownShape(labels["zg+jets"]["hists-prefire-up"][mlg_index],labels["zg+jets"]["hists"][mlg_index]).Write("zgjets_prefireDown")
    labels["vv+jets"]["hists-prefire-up"][mlg_index].Write("vvjets_prefireUp")
    makeDownShape(labels["vv+jets"]["hists-prefire-up"][mlg_index],labels["vv+jets"]["hists"][mlg_index]).Write("vvjets_prefireDown")
    labels["wg+jets"]["hists-prefire-up"][mlg_index].Write("wg_prefireUp")
    makeDownShape(labels["wg+jets"]["hists-prefire-up"][mlg_index],labels["wg+jets"]["hists"][mlg_index]).Write("wg_prefireDown")

    labels["top+jets"]["hists-muon-id-sf-up"][mlg_index].Write("topjets_muonidsfUp")
    makeDownShape(labels["top+jets"]["hists-muon-id-sf-up"][mlg_index],labels["top+jets"]["hists"][mlg_index]).Write("topjets_muonidsfDown")
    labels["zg+jets"]["hists-muon-id-sf-up"][mlg_index].Write("zgjets_muonidsfUp")
    makeDownShape(labels["zg+jets"]["hists-muon-id-sf-up"][mlg_index],labels["zg+jets"]["hists"][mlg_index]).Write("zgjets_muonidsfDown")
    labels["vv+jets"]["hists-muon-id-sf-up"][mlg_index].Write("vvjets_muonidsfUp")
    makeDownShape(labels["vv+jets"]["hists-muon-id-sf-up"][mlg_index],labels["vv+jets"]["hists"][mlg_index]).Write("vvjets_muonidsfDown")
    labels["wg+jets"]["hists-muon-id-sf-up"][mlg_index].Write("wg_muonidsfUp")
    makeDownShape(labels["wg+jets"]["hists-muon-id-sf-up"][mlg_index],labels["wg+jets"]["hists"][mlg_index]).Write("wg_muonidsfDown")
    
    labels["top+jets"]["hists-muon-iso-sf-up"][mlg_index].Write("topjets_muonisosfUp")
    makeDownShape(labels["top+jets"]["hists-muon-iso-sf-up"][mlg_index],labels["top+jets"]["hists"][mlg_index]).Write("topjets_muonisosfDown")
    labels["zg+jets"]["hists-muon-iso-sf-up"][mlg_index].Write("zgjets_muonisosfUp")
    makeDownShape(labels["zg+jets"]["hists-muon-iso-sf-up"][mlg_index],labels["zg+jets"]["hists"][mlg_index]).Write("zgjets_muonisosfDown")
    labels["vv+jets"]["hists-muon-iso-sf-up"][mlg_index].Write("vvjets_muonisosfUp")
    makeDownShape(labels["vv+jets"]["hists-muon-iso-sf-up"][mlg_index],labels["vv+jets"]["hists"][mlg_index]).Write("vvjets_muonisosfDown")
    labels["wg+jets"]["hists-muon-iso-sf-up"][mlg_index].Write("wg_muonisosfUp")
    makeDownShape(labels["wg+jets"]["hists-muon-iso-sf-up"][mlg_index],labels["wg+jets"]["hists"][mlg_index]).Write("wg_muonisosfDown")
    
    labels["top+jets"]["hists-muon-hlt-sf-up"][mlg_index].Write("topjets_muonhltsfUp")
    makeDownShape(labels["top+jets"]["hists-muon-hlt-sf-up"][mlg_index],labels["top+jets"]["hists"][mlg_index]).Write("topjets_muonhltsfDown")
    labels["zg+jets"]["hists-muon-hlt-sf-up"][mlg_index].Write("zgjets_muonhltsfUp")
    makeDownShape(labels["zg+jets"]["hists-muon-hlt-sf-up"][mlg_index],labels["zg+jets"]["hists"][mlg_index]).Write("zgjets_muonhltsfDown")
    labels["vv+jets"]["hists-muon-hlt-sf-up"][mlg_index].Write("vvjets_muonhltsfUp")
    makeDownShape(labels["vv+jets"]["hists-muon-hlt-sf-up"][mlg_index],labels["vv+jets"]["hists"][mlg_index]).Write("vvjets_muonhltsfDown")
    labels["wg+jets"]["hists-muon-hlt-sf-up"][mlg_index].Write("wg_muonhltsfUp")
    makeDownShape(labels["wg+jets"]["hists-muon-hlt-sf-up"][mlg_index],labels["wg+jets"]["hists"][mlg_index]).Write("wg_muonhltsfDown")
    
    labels["top+jets"]["hists-electron-reco-sf-up"][mlg_index].Write("topjets_electronrecosfUp")
    makeDownShape(labels["top+jets"]["hists-electron-reco-sf-up"][mlg_index],labels["top+jets"]["hists"][mlg_index]).Write("topjets_electronrecosfDown")
    labels["zg+jets"]["hists-electron-reco-sf-up"][mlg_index].Write("zgjets_electronrecosfUp")
    makeDownShape(labels["vv+jets"]["hists-electron-reco-sf-up"][mlg_index],labels["vv+jets"]["hists"][mlg_index]).Write("zgjets_electronrecosfDown")
    labels["vv+jets"]["hists-electron-reco-sf-up"][mlg_index].Write("vvjets_electronrecosfUp")
    makeDownShape(labels["vv+jets"]["hists-electron-reco-sf-up"][mlg_index],labels["vv+jets"]["hists"][mlg_index]).Write("vvjets_electronrecosfDown")
    labels["wg+jets"]["hists-electron-reco-sf-up"][mlg_index].Write("wg_electronrecosfUp")
    makeDownShape(labels["wg+jets"]["hists-electron-reco-sf-up"][mlg_index],labels["wg+jets"]["hists"][mlg_index]).Write("wg_electronrecosfDown")

    labels["top+jets"]["hists-electron-id-sf-up"][mlg_index].Write("topjets_electronidsfUp")
    makeDownShape(labels["top+jets"]["hists-electron-id-sf-up"][mlg_index],labels["top+jets"]["hists"][mlg_index]).Write("topjets_electronidsfDown")
    labels["zg+jets"]["hists-electron-id-sf-up"][mlg_index].Write("zgjets_electronidsfUp")
    makeDownShape(labels["vv+jets"]["hists-electron-id-sf-up"][mlg_index],labels["vv+jets"]["hists"][mlg_index]).Write("zgjets_electronidsfDown")
    labels["vv+jets"]["hists-electron-id-sf-up"][mlg_index].Write("vvjets_electronidsfUp")
    makeDownShape(labels["vv+jets"]["hists-electron-id-sf-up"][mlg_index],labels["vv+jets"]["hists"][mlg_index]).Write("vvjets_electronidsfDown")
    labels["wg+jets"]["hists-electron-id-sf-up"][mlg_index].Write("wg_electronidsfUp")
    makeDownShape(labels["wg+jets"]["hists-electron-id-sf-up"][mlg_index],labels["wg+jets"]["hists"][mlg_index]).Write("wg_electronidsfDown")

    labels["top+jets"]["hists-electron-hlt-sf-up"][mlg_index].Write("topjets_electronhltsfUp")
    makeDownShape(labels["top+jets"]["hists-electron-hlt-sf-up"][mlg_index],labels["top+jets"]["hists"][mlg_index]).Write("topjets_electronhltsfDown")
    labels["zg+jets"]["hists-electron-hlt-sf-up"][mlg_index].Write("zgjets_electronhltsfUp")
    makeDownShape(labels["vv+jets"]["hists-electron-hlt-sf-up"][mlg_index],labels["vv+jets"]["hists"][mlg_index]).Write("zgjets_electronhltsfDown")
    labels["vv+jets"]["hists-electron-hlt-sf-up"][mlg_index].Write("vvjets_electronhltsfUp")
    makeDownShape(labels["vv+jets"]["hists-electron-hlt-sf-up"][mlg_index],labels["vv+jets"]["hists"][mlg_index]).Write("vvjets_electronhltsfDown")
    labels["wg+jets"]["hists-electron-hlt-sf-up"][mlg_index].Write("wg_electronhltsfUp")
    makeDownShape(labels["wg+jets"]["hists-electron-hlt-sf-up"][mlg_index],labels["wg+jets"]["hists"][mlg_index]).Write("wg_electronhltsfDown")
    
    labels["top+jets"]["hists-jes-up"][mlg_index].Write("topjets_jesUp")
    makeDownShape(labels["top+jets"]["hists-jes-up"][mlg_index],labels["top+jets"]["hists"][mlg_index]).Write("topjets_jesDown")
    labels["zg+jets"]["hists-jes-up"][mlg_index].Write("zgjets_jesUp")
    makeDownShape(labels["zg+jets"]["hists-jes-up"][mlg_index],labels["zg+jets"]["hists"][mlg_index]).Write("zgjets_jesDown")
    labels["vv+jets"]["hists-jes-up"][mlg_index].Write("vvjets_jesUp")
    makeDownShape(labels["vv+jets"]["hists-jes-up"][mlg_index],labels["vv+jets"]["hists"][mlg_index]).Write("vvjets_jesDown")
    labels["wg+jets"]["hists-jes-up"][mlg_index].Write("wg_jesUp")
    makeDownShape(labels["wg+jets"]["hists-jes-up"][mlg_index],labels["wg+jets"]["hists"][mlg_index]).Write("wg_jesDown")
    
    labels["top+jets"]["hists-jer-up"][mlg_index].Write("topjets_jerUp")
    makeDownShape(labels["top+jets"]["hists-jer-up"][mlg_index],labels["top+jets"]["hists"][mlg_index]).Write("topjets_jerDown")
    labels["zg+jets"]["hists-jer-up"][mlg_index].Write("zgjets_jerUp")
    makeDownShape(labels["zg+jets"]["hists-jer-up"][mlg_index],labels["zg+jets"]["hists"][mlg_index]).Write("zgjets_jerDown")
    labels["vv+jets"]["hists-jer-up"][mlg_index].Write("vvjets_jerUp")
    makeDownShape(labels["vv+jets"]["hists-jer-up"][mlg_index],labels["vv+jets"]["hists"][mlg_index]).Write("vvjets_jerDown")
    labels["wg+jets"]["hists-jer-up"][mlg_index].Write("wg_jerUp")
    makeDownShape(labels["wg+jets"]["hists-jer-up"][mlg_index],labels["wg+jets"]["hists"][mlg_index]).Write("wg_jerDown")

    bwcb_norm = ROOT.RooRealVar("bwcb_norm","",152671.0,0,1000000);    
    bwcbbin_norm = ROOT.RooRealVar("bwcbbin_norm","",156180.0,152671.0/2,152671.0*2);    

    m= ROOT.RooRealVar("m","",mlg_fit_lower_bound,mlg_fit_upper_bound)
    m0=ROOT.RooRealVar("m0", "",-0.23326,-3,3)
    sigma=ROOT.RooRealVar("sigma", "",2.1250,0.1,3)
    alpha=ROOT.RooRealVar("alpha", "",2.0087,0,10)
    n=ROOT.RooRealVar("n", "",2.11960,2.11960,2.11960)
    cb = ROOT.RooCBShape("cb", "", m, m0, sigma, alpha, n)
    mass = ROOT.RooRealVar("mass","",91.1876,91.1876,91.1876)
    width = ROOT.RooRealVar("width","",2.4952,2.4952,2.4952);
    bw = ROOT.RooBreitWigner("bw","",m,mass,width)

    RooFFTConvPdf_bwcb = ROOT.RooFFTConvPdf("bwcb","Breit Wigner convolved with a Crystal Ball",m,bw,cb)

    RooParametricShapeBinPdf_bwcb=ROOT.RooParametricShapeBinPdf("bwcbbin","",RooFFTConvPdf_bwcb,m,ROOT.RooArgList(m0,sigma,alpha,n,cb,mass,width,bw,m),histogram_models[mlg_index].GetHistogram())
    
    RooDataHist_wg = ROOT.RooDataHist("wg","",ROOT.RooArgList(m),labels["wg+jets"]["hists"][mlg_index])
#RooHistPdf_wg = ROOT.RooHistPdf("wg","",ROOT.RooArgSet(m),RooDataHist_wg)

    RooDataHist_vvjets = ROOT.RooDataHist("vvjets","",ROOT.RooArgList(m),labels["vv+jets"]["hists"][mlg_index])
#RooHistPdf_vvjets = ROOT.RooHistPdf("vvjets","",ROOT.RooArgSet(m),RooDataHist_vvjets)

    RooDataHist_zgjets = ROOT.RooDataHist("zgjets","",ROOT.RooArgList(m),labels["zg+jets"]["hists"][mlg_index])
#RooHistPdf_zgjets = ROOT.RooHistPdf("zgjets","",ROOT.RooArgSet(m),RooDataHist_zgjets)

    RooDataHist_topjets = ROOT.RooDataHist("topjets","",ROOT.RooArgList(m),labels["top+jets"]["hists"][mlg_index])
#RooHistPdf_topjets = ROOT.RooHistPdf("topjets","",ROOT.RooArgSet(m),RooDataHist_topjets)

    if options.lep == "muon":
        RooDataHist_fake_lepton = ROOT.RooDataHist("fakemuon","",ROOT.RooArgList(m),fake_lepton["hists"][mlg_index])
    elif options.lep == "electron":
        RooDataHist_fake_lepton = ROOT.RooDataHist("fakeelectron","",ROOT.RooArgList(m),fake_lepton["hists"][mlg_index])
    else:
        assert(0)    

#RooHistPdf_fake_lepton = ROOT.RooHistPdf("fakelepton","",ROOT.RooArgSet(m),RooDataHist_fake_lepton)

    RooDataHist_fake_photon = ROOT.RooDataHist("fakephoton","",ROOT.RooArgList(m),fake_photon["hists"][mlg_index])
#RooHistPdf_fake_photon = ROOT.RooHistPdf("fakephoton","",ROOT.RooArgSet(m),RooDataHist_fake_photon)

    RooDataHist_double_fake = ROOT.RooDataHist("doublefake","",ROOT.RooArgList(m),double_fake["hists"][mlg_index])
#RooHistPdf_double_fake = ROOT.RooHistPdf("doublefake","",ROOT.RooArgSet(m),RooDataHist_double_fake)

    RooDataHist_e_to_p_non_res = ROOT.RooDataHist("etopnonres","",ROOT.RooArgList(m),e_to_p_non_res["hists"][mlg_index])
#RooHistPdf_e_to_p_non_res = ROOT.RooHistPdf("etopnonres","",ROOT.RooArgSet(m),RooDataHist_e_to_p_non_res)

#wg scale

    RooDataHist_wg_scale_up = ROOT.RooDataHist("wg_wgscaleUp","",ROOT.RooArgList(m),wgjets_scale_syst)
    RooDataHist_wg_scale_down = ROOT.RooDataHist("wg_wgscaleDown","",ROOT.RooArgList(m),makeDownShape(wgjets_scale_syst,labels["wg+jets"]["hists"][mlg_index]))

    list_RooDataHist_wg_stat_up = []
    list_RooDataHist_wg_stat_down = []
    
    for i in range(1,labels["wg+jets"]["hists"][mlg_index].GetNbinsX()+1):
        list_RooDataHist_wg_stat_up.append(ROOT.RooDataHist("wg_wgstatbin"+str(i)+"Up","",ROOT.RooArgList(m),wg_stat_up[i-1]))
        list_RooDataHist_wg_stat_down.append(ROOT.RooDataHist("wg_wgstatbin"+str(i)+"Down","",ROOT.RooArgList(m),makeDownShape(wg_stat_up[i-1],labels["wg+jets"]["hists"][mlg_index])))

    list_RooDataHist_fake_photon_syst2_up = []
    list_RooDataHist_fake_photon_syst2_down = []

    for i in range(1,len(fake_photon_syst2_up)+1):
        list_RooDataHist_fake_photon_syst2_up.append(ROOT.RooDataHist("fakephoton_fakephotonsyst2var"+str(i)+"Up","",ROOT.RooArgList(m),fake_photon_syst2_up[i-1]))
        list_RooDataHist_fake_photon_syst2_down.append(ROOT.RooDataHist("fakephoton_fakephotonsyst2var"+str(i)+"Down","",ROOT.RooArgList(m),makeDownShape(fake_photon_syst2_up[i-1],fake_photon["hists"][mlg_index])))

    list_RooDataHist_fake_lepton_syst_up = []
    list_RooDataHist_fake_lepton_syst_down = []
    
    for i in range(1,fake_lepton["hists"][mlg_index].GetNbinsX()+1):
        list_RooDataHist_fake_lepton_syst_up.append(ROOT.RooDataHist("fakeelectron_fakeelectronstatbin"+str(i)+"Up","",ROOT.RooArgList(m),fake_lepton_syst_up[i-1]))
        list_RooDataHist_fake_lepton_syst_down.append(ROOT.RooDataHist("fakeelectron_fakeelectronstatbin"+str(i)+"Down","",ROOT.RooArgList(m),makeDownShape(fake_lepton_syst_up[i-1],fake_lepton["hists"][mlg_index])))

    list_RooDataHist_zgjets_stat_up = []
    list_RooDataHist_zgjets_stat_down = []

    for i in range(1,labels["zg+jets"]["hists"][mlg_index].GetNbinsX()+1):
        list_RooDataHist_zgjets_stat_up.append(ROOT.RooDataHist("zgjets_zgjetsstatbin"+str(i)+"Up","",ROOT.RooArgList(m),zgjets_stat_up[i-1]))
        list_RooDataHist_zgjets_stat_down.append(ROOT.RooDataHist("zgjets_zgjetsstatbin"+str(i)+"Down","",ROOT.RooArgList(m),makeDownShape(zgjets_stat_up[i-1],labels["zg+jets"]["hists"][mlg_index])))

#zg scale

    RooDataHist_zg_scale_up = ROOT.RooDataHist("zgjets_zgscaleUp","",ROOT.RooArgList(m),zgjets_scale_syst)
    RooDataHist_zg_scale_down = ROOT.RooDataHist("zgjets_zgscaleDown","",ROOT.RooArgList(m),makeDownShape(zgjets_scale_syst,labels["zg+jets"]["hists"][mlg_index]))

#fake photon syst 1

    RooDataHist_fake_photon_syst1_up = ROOT.RooDataHist("fakephoton_fakephotonsyst1Up","",ROOT.RooArgList(m),fake_photon_alt["hists"][mlg_index])
#RooHistPdf_fake_photon_syst1_up = ROOT.RooHistPdf("fakephoton_fakephotonsyst1Up","",ROOT.RooArgSet(m),RooDataHist_fake_photon_syst1_up)

    RooDataHist_fake_photon_syst1_down = ROOT.RooDataHist("fakephoton_fakephotonsyst1Down","",ROOT.RooArgList(m),makeDownShape(fake_photon_alt["hists"][mlg_index],fake_photon["hists"][mlg_index]))
#RooHistPdf_fake_photon_syst1_down = ROOT.RooHistPdf("fakephoton_fakephotonsyst1Down","",ROOT.RooArgSet(m),RooDataHist_fake_photon_syst1_down)

#fake photon syst 2

    RooDataHist_fake_photon_syst2_up = ROOT.RooDataHist("fakephoton_fakephotonsyst2Up","",ROOT.RooArgList(m),labels["w+jets"]["hists"][mlg_index])
#RooHistPdf_fake_photon_syst2_up = ROOT.RooHistPdf("fakephoton_fakephotonsyst2Up","",ROOT.RooArgSet(m),RooDataHist_fake_photon_syst2_up)

    RooDataHist_fake_photon_syst2_down = ROOT.RooDataHist("fakephoton_fakephotonsyst2Down","",ROOT.RooArgList(m),makeDownShape(labels["w+jets"]["hists"][mlg_index],fake_photon["hists"][mlg_index]))
#RooHistPdf_fake_photon_syst2_down = ROOT.RooHistPdf("fakephoton_fakephotonsyst2Down","",ROOT.RooArgSet(m),RooDataHist_fake_photon_syst2_down)


#pileup

    RooDataHist_wg_pileup_up = ROOT.RooDataHist("wg_pileupUp","",ROOT.RooArgList(m),labels["wg+jets"]["hists-pileup-up"][mlg_index])
#RooHistPdf_wg_pileup_up = ROOT.RooHistPdf("wg_pileupUp","",ROOT.RooArgSet(m),RooDataHist_wg_pileup_up)
    RooDataHist_wg_pileup_down = ROOT.RooDataHist("wg_pileupDown","",ROOT.RooArgList(m),makeDownShape(labels["wg+jets"]["hists-pileup-up"][mlg_index],labels["wg+jets"]["hists"][mlg_index]))
#RooHistPdf_wg_pileup_down = ROOT.RooHistPdf("wg_pileupDown","",ROOT.RooArgSet(m),RooDataHist_wg_pileup_down)

    RooDataHist_topjets_pileup_up = ROOT.RooDataHist("topjets_pileupUp","",ROOT.RooArgList(m),labels["top+jets"]["hists-pileup-up"][mlg_index])
#RooHistPdf_topjets_pileup_up = ROOT.RooHistPdf("topjets_pileupUp","",ROOT.RooArgSet(m),RooDataHist_topjets_pileup_up)
    RooDataHist_topjets_pileup_down = ROOT.RooDataHist("topjets_pileupDown","",ROOT.RooArgList(m),makeDownShape(labels["top+jets"]["hists-pileup-up"][mlg_index],labels["top+jets"]["hists"][mlg_index]))
#RooHistPdf_topjets_pileup_down = ROOT.RooHistPdf("topjets_pileupDown","",ROOT.RooArgSet(m),RooDataHist_topjets_pileup_down)

    RooDataHist_zgjets_pileup_up = ROOT.RooDataHist("zgjets_pileupUp","",ROOT.RooArgList(m),labels["zg+jets"]["hists-pileup-up"][mlg_index])
#RooHistPdf_zgjets_pileup_up = ROOT.RooHistPdf("zgjets_pileupUp","",ROOT.RooArgSet(m),RooDataHist_zgjets_pileup_up)
    RooDataHist_zgjets_pileup_down = ROOT.RooDataHist("zgjets_pileupDown","",ROOT.RooArgList(m),makeDownShape(labels["zg+jets"]["hists-pileup-up"][mlg_index],labels["zg+jets"]["hists"][mlg_index]))
#RooHistPdf_zgjets_pileup_down = ROOT.RooHistPdf("zgjets_pileupDown","",ROOT.RooArgSet(m),RooDataHist_zgjets_pileup_down)

    RooDataHist_vvjets_pileup_up = ROOT.RooDataHist("vvjets_pileupUp","",ROOT.RooArgList(m),labels["vv+jets"]["hists-pileup-up"][mlg_index])
#RooHistPdf_vvjets_pileup_up = ROOT.RooHistPdf("vvjets_pileupUp","",ROOT.RooArgSet(m),RooDataHist_vvjets_pileup_up)
    RooDataHist_vvjets_pileup_down = ROOT.RooDataHist("vvjets_pileupDown","",ROOT.RooArgList(m),makeDownShape(labels["vv+jets"]["hists-pileup-up"][mlg_index],labels["vv+jets"]["hists"][mlg_index]))
#RooHistPdf_vvjets_pileup_down = ROOT.RooHistPdf("vvjets_pileupDown","",ROOT.RooArgSet(m),RooDataHist_vvjets_pileup_down)

#prefire

    RooDataHist_wg_prefire_up = ROOT.RooDataHist("wg_prefireUp","",ROOT.RooArgList(m),labels["wg+jets"]["hists-prefire-up"][mlg_index])
#RooHistPdf_wg_prefire_up = ROOT.RooHistPdf("wg_prefireUp","",ROOT.RooArgSet(m),RooDataHist_wg_prefire_up)
    RooDataHist_wg_prefire_down = ROOT.RooDataHist("wg_prefireDown","",ROOT.RooArgList(m),makeDownShape(labels["wg+jets"]["hists-prefire-up"][mlg_index],labels["wg+jets"]["hists"][mlg_index]))
#RooHistPdf_wg_prefire_down = ROOT.RooHistPdf("wg_prefireDown","",ROOT.RooArgSet(m),RooDataHist_wg_prefire_down)

    RooDataHist_topjets_prefire_up = ROOT.RooDataHist("topjets_prefireUp","",ROOT.RooArgList(m),labels["top+jets"]["hists-prefire-up"][mlg_index])
#RooHistPdf_topjets_prefire_up = ROOT.RooHistPdf("topjets_prefireUp","",ROOT.RooArgSet(m),RooDataHist_topjets_prefire_up)
    RooDataHist_topjets_prefire_down = ROOT.RooDataHist("topjets_prefireDown","",ROOT.RooArgList(m),makeDownShape(labels["top+jets"]["hists-prefire-up"][mlg_index],labels["top+jets"]["hists"][mlg_index]))
#RooHistPdf_topjets_prefire_down = ROOT.RooHistPdf("topjets_prefireDown","",ROOT.RooArgSet(m),RooDataHist_topjets_prefire_down)

    RooDataHist_zgjets_prefire_up = ROOT.RooDataHist("zgjets_prefireUp","",ROOT.RooArgList(m),labels["zg+jets"]["hists-prefire-up"][mlg_index])
#RooHistPdf_zgjets_prefire_up = ROOT.RooHistPdf("zgjets_prefireUp","",ROOT.RooArgSet(m),RooDataHist_zgjets_prefire_up)
    RooDataHist_zgjets_prefire_down = ROOT.RooDataHist("zgjets_prefireDown","",ROOT.RooArgList(m),makeDownShape(labels["zg+jets"]["hists-prefire-up"][mlg_index],labels["zg+jets"]["hists"][mlg_index]))
#RooHistPdf_zgjets_prefire_down = ROOT.RooHistPdf("zgjets_prefireDown","",ROOT.RooArgSet(m),RooDataHist_zgjets_prefire_down)

    RooDataHist_vvjets_prefire_up = ROOT.RooDataHist("vvjets_prefireUp","",ROOT.RooArgList(m),labels["vv+jets"]["hists-prefire-up"][mlg_index])
#RooHistPdf_vvjets_prefire_up = ROOT.RooHistPdf("vvjets_prefireUp","",ROOT.RooArgSet(m),RooDataHist_vvjets_prefire_up)
    RooDataHist_vvjets_prefire_down = ROOT.RooDataHist("vvjets_prefireDown","",ROOT.RooArgList(m),makeDownShape(labels["vv+jets"]["hists-prefire-up"][mlg_index],labels["vv+jets"]["hists"][mlg_index]))
#RooHistPdf_vvjets_prefire_down = ROOT.RooHistPdf("vvjets_prefireDown","",ROOT.RooArgSet(m),RooDataHist_vvjets_prefire_down)

#jes sf

    RooDataHist_wg_jes_up = ROOT.RooDataHist("wg_jesUp","",ROOT.RooArgList(m),labels["wg+jets"]["hists-jes-up"][mlg_index])
#RooHistPdf_wg_jes_up = ROOT.RooHistPdf("wg_jesUp","",ROOT.RooArgSet(m),RooDataHist_wg_jes_up)
    RooDataHist_wg_jes_down = ROOT.RooDataHist("wg_jesDown","",ROOT.RooArgList(m),makeDownShape(labels["wg+jets"]["hists-jes-up"][mlg_index],labels["wg+jets"]["hists"][mlg_index]))
#RooHistPdf_wg_jes_down = ROOT.RooHistPdf("wg_jesDown","",ROOT.RooArgSet(m),RooDataHist_wg_jes_down)

    RooDataHist_topjets_jes_up = ROOT.RooDataHist("topjets_jesUp","",ROOT.RooArgList(m),labels["top+jets"]["hists-jes-up"][mlg_index])
#RooHistPdf_topjets_jes_up = ROOT.RooHistPdf("topjets_jesUp","",ROOT.RooArgSet(m),RooDataHist_topjets_jes_up)
    RooDataHist_topjets_jes_down = ROOT.RooDataHist("topjets_jesDown","",ROOT.RooArgList(m),makeDownShape(labels["top+jets"]["hists-jes-up"][mlg_index],labels["top+jets"]["hists"][mlg_index]))
#RooHistPdf_topjets_jes_down = ROOT.RooHistPdf("topjets_jesDown","",ROOT.RooArgSet(m),RooDataHist_topjets_jes_down)

    RooDataHist_zgjets_jes_up = ROOT.RooDataHist("zgjets_jesUp","",ROOT.RooArgList(m),labels["zg+jets"]["hists-jes-up"][mlg_index])
#RooHistPdf_zgjets_jes_up = ROOT.RooHistPdf("zgjets_jesUp","",ROOT.RooArgSet(m),RooDataHist_zgjets_jes_up)
    RooDataHist_zgjets_jes_down = ROOT.RooDataHist("zgjets_jesDown","",ROOT.RooArgList(m),makeDownShape(labels["zg+jets"]["hists-jes-up"][mlg_index],labels["zg+jets"]["hists"][mlg_index]))
#RooHistPdf_zgjets_jes_down = ROOT.RooHistPdf("zgjets_jesDown","",ROOT.RooArgSet(m),RooDataHist_zgjets_jes_down)

    RooDataHist_vvjets_jes_up = ROOT.RooDataHist("vvjets_jesUp","",ROOT.RooArgList(m),labels["vv+jets"]["hists-jes-up"][mlg_index])
#RooHistPdf_vvjets_jes_up = ROOT.RooHistPdf("vvjets_jesUp","",ROOT.RooArgSet(m),RooDataHist_vvjets_jes_up)
    RooDataHist_vvjets_jes_down = ROOT.RooDataHist("vvjets_jesDown","",ROOT.RooArgList(m),makeDownShape(labels["vv+jets"]["hists-jes-up"][mlg_index],labels["vv+jets"]["hists"][mlg_index]))
#RooHistPdf_vvjets_jes_down = ROOT.RooHistPdf("vvjets_jesDown","",ROOT.RooArgSet(m),RooDataHist_vvjets_jes_down)

#jer sf

    RooDataHist_wg_jer_up = ROOT.RooDataHist("wg_jerUp","",ROOT.RooArgList(m),labels["wg+jets"]["hists-jer-up"][mlg_index])
#RooHistPdf_wg_jer_up = ROOT.RooHistPdf("wg_jerUp","",ROOT.RooArgSet(m),RooDataHist_wg_jer_up)
    RooDataHist_wg_jer_down = ROOT.RooDataHist("wg_jerDown","",ROOT.RooArgList(m),makeDownShape(labels["wg+jets"]["hists-jer-up"][mlg_index],labels["wg+jets"]["hists"][mlg_index]))
#RooHistPdf_wg_jer_down = ROOT.RooHistPdf("wg_jerDown","",ROOT.RooArgSet(m),RooDataHist_wg_jer_down)

    RooDataHist_topjets_jer_up = ROOT.RooDataHist("topjets_jerUp","",ROOT.RooArgList(m),labels["top+jets"]["hists-jer-up"][mlg_index])
#RooHistPdf_topjets_jer_up = ROOT.RooHistPdf("topjets_jerUp","",ROOT.RooArgSet(m),RooDataHist_topjets_jer_up)
    RooDataHist_topjets_jer_down = ROOT.RooDataHist("topjets_jerDown","",ROOT.RooArgList(m),makeDownShape(labels["top+jets"]["hists-jer-up"][mlg_index],labels["top+jets"]["hists"][mlg_index]))
#RooHistPdf_topjets_jer_down = ROOT.RooHistPdf("topjets_jerDown","",ROOT.RooArgSet(m),RooDataHist_topjets_jer_down)

    RooDataHist_zgjets_jer_up = ROOT.RooDataHist("zgjets_jerUp","",ROOT.RooArgList(m),labels["zg+jets"]["hists-jer-up"][mlg_index])
#RooHistPdf_zgjets_jer_up = ROOT.RooHistPdf("zgjets_jerUp","",ROOT.RooArgSet(m),RooDataHist_zgjets_jer_up)
    RooDataHist_zgjets_jer_down = ROOT.RooDataHist("zgjets_jerDown","",ROOT.RooArgList(m),makeDownShape(labels["zg+jets"]["hists-jer-up"][mlg_index],labels["zg+jets"]["hists"][mlg_index]))
#RooHistPdf_zgjets_jer_down = ROOT.RooHistPdf("zgjets_jerDown","",ROOT.RooArgSet(m),RooDataHist_zgjets_jer_down)

    RooDataHist_vvjets_jer_up = ROOT.RooDataHist("vvjets_jerUp","",ROOT.RooArgList(m),labels["vv+jets"]["hists-jer-up"][mlg_index])
#RooHistPdf_vvjets_jer_up = ROOT.RooHistPdf("vvjets_jerUp","",ROOT.RooArgSet(m),RooDataHist_vvjets_jer_up)
    RooDataHist_vvjets_jer_down = ROOT.RooDataHist("vvjets_jerDown","",ROOT.RooArgList(m),makeDownShape(labels["vv+jets"]["hists-jer-up"][mlg_index],labels["vv+jets"]["hists"][mlg_index]))
#RooHistPdf_vvjets_jer_down = ROOT.RooHistPdf("vvjets_jerDown","",ROOT.RooArgSet(m),RooDataHist_vvjets_jer_down)

#electron reco sf

    RooDataHist_wg_electronrecosf_up = ROOT.RooDataHist("wg_electronrecosfUp","",ROOT.RooArgList(m),labels["wg+jets"]["hists-electron-reco-sf-up"][mlg_index])
#RooHistPdf_wg_electronrecosf_up = ROOT.RooHistPdf("wg_electronrecosfUp","",ROOT.RooArgSet(m),RooDataHist_wg_electronrecosf_up)
    RooDataHist_wg_electronrecosf_down = ROOT.RooDataHist("wg_electronrecosfDown","",ROOT.RooArgList(m),makeDownShape(labels["wg+jets"]["hists-electron-reco-sf-up"][mlg_index],labels["wg+jets"]["hists"][mlg_index]))
#RooHistPdf_wg_electronrecosf_down = ROOT.RooHistPdf("wg_electronrecosfDown","",ROOT.RooArgSet(m),RooDataHist_wg_electronrecosf_down)

    RooDataHist_topjets_electronrecosf_up = ROOT.RooDataHist("topjets_electronrecosfUp","",ROOT.RooArgList(m),labels["top+jets"]["hists-electron-reco-sf-up"][mlg_index])
#RooHistPdf_topjets_electronrecosf_up = ROOT.RooHistPdf("topjets_electronrecosfUp","",ROOT.RooArgSet(m),RooDataHist_topjets_electronrecosf_up)
    RooDataHist_topjets_electronrecosf_down = ROOT.RooDataHist("topjets_electronrecosfDown","",ROOT.RooArgList(m),makeDownShape(labels["top+jets"]["hists-electron-reco-sf-up"][mlg_index],labels["top+jets"]["hists"][mlg_index]))
#RooHistPdf_topjets_electronrecosf_down = ROOT.RooHistPdf("topjets_electronrecosfDown","",ROOT.RooArgSet(m),RooDataHist_topjets_electronrecosf_down)

    RooDataHist_zgjets_electronrecosf_up = ROOT.RooDataHist("zgjets_electronrecosfUp","",ROOT.RooArgList(m),labels["zg+jets"]["hists-electron-reco-sf-up"][mlg_index])
#RooHistPdf_zgjets_electronrecosf_up = ROOT.RooHistPdf("zgjets_electronrecosfUp","",ROOT.RooArgSet(m),RooDataHist_zgjets_electronrecosf_up)
    RooDataHist_zgjets_electronrecosf_down = ROOT.RooDataHist("zgjets_electronrecosfDown","",ROOT.RooArgList(m),makeDownShape(labels["zg+jets"]["hists-electron-reco-sf-up"][mlg_index],labels["zg+jets"]["hists"][mlg_index]))
#RooHistPdf_zgjets_electronrecosf_down = ROOT.RooHistPdf("zgjets_electronrecosfDown","",ROOT.RooArgSet(m),RooDataHist_zgjets_electronrecosf_down)

    RooDataHist_vvjets_electronrecosf_up = ROOT.RooDataHist("vvjets_electronrecosfUp","",ROOT.RooArgList(m),labels["vv+jets"]["hists-electron-reco-sf-up"][mlg_index])
#RooHistPdf_vvjets_electronrecosf_up = ROOT.RooHistPdf("vvjets_electronrecosfUp","",ROOT.RooArgSet(m),RooDataHist_vvjets_electronrecosf_up)
    RooDataHist_vvjets_electronrecosf_down = ROOT.RooDataHist("vvjets_electronrecosfDown","",ROOT.RooArgList(m),makeDownShape(labels["vv+jets"]["hists-electron-reco-sf-up"][mlg_index],labels["vv+jets"]["hists"][mlg_index]))
#RooHistPdf_vvjets_electronrecosf_down = ROOT.RooHistPdf("vvjets_electronrecosfDown","",ROOT.RooArgSet(m),RooDataHist_vvjets_electronrecosf_down)


#electron id sf

    RooDataHist_wg_electronidsf_up = ROOT.RooDataHist("wg_electronidsfUp","",ROOT.RooArgList(m),labels["wg+jets"]["hists-electron-id-sf-up"][mlg_index])
#RooHistPdf_wg_electronidsf_up = ROOT.RooHistPdf("wg_electronidsfUp","",ROOT.RooArgSet(m),RooDataHist_wg_electronidsf_up)
    RooDataHist_wg_electronidsf_down = ROOT.RooDataHist("wg_electronidsfDown","",ROOT.RooArgList(m),makeDownShape(labels["wg+jets"]["hists-electron-id-sf-up"][mlg_index],labels["wg+jets"]["hists"][mlg_index]))
#RooHistPdf_wg_electronidsf_down = ROOT.RooHistPdf("wg_electronidsfDown","",ROOT.RooArgSet(m),RooDataHist_wg_electronidsf_down)

    RooDataHist_topjets_electronidsf_up = ROOT.RooDataHist("topjets_electronidsfUp","",ROOT.RooArgList(m),labels["top+jets"]["hists-electron-id-sf-up"][mlg_index])
#RooHistPdf_topjets_electronidsf_up = ROOT.RooHistPdf("topjets_electronidsfUp","",ROOT.RooArgSet(m),RooDataHist_topjets_electronidsf_up)
    RooDataHist_topjets_electronidsf_down = ROOT.RooDataHist("topjets_electronidsfDown","",ROOT.RooArgList(m),makeDownShape(labels["top+jets"]["hists-electron-id-sf-up"][mlg_index],labels["top+jets"]["hists"][mlg_index]))
#RooHistPdf_topjets_electronidsf_down = ROOT.RooHistPdf("topjets_electronidsfDown","",ROOT.RooArgSet(m),RooDataHist_topjets_electronidsf_down)

    RooDataHist_zgjets_electronidsf_up = ROOT.RooDataHist("zgjets_electronidsfUp","",ROOT.RooArgList(m),labels["zg+jets"]["hists-electron-id-sf-up"][mlg_index])
#RooHistPdf_zgjets_electronidsf_up = ROOT.RooHistPdf("zgjets_electronidsfUp","",ROOT.RooArgSet(m),RooDataHist_zgjets_electronidsf_up)
    RooDataHist_zgjets_electronidsf_down = ROOT.RooDataHist("zgjets_electronidsfDown","",ROOT.RooArgList(m),makeDownShape(labels["zg+jets"]["hists-electron-id-sf-up"][mlg_index],labels["zg+jets"]["hists"][mlg_index]))
#RooHistPdf_zgjets_electronidsf_down = ROOT.RooHistPdf("zgjets_electronidsfDown","",ROOT.RooArgSet(m),RooDataHist_zgjets_electronidsf_down)

    RooDataHist_vvjets_electronidsf_up = ROOT.RooDataHist("vvjets_electronidsfUp","",ROOT.RooArgList(m),labels["vv+jets"]["hists-electron-id-sf-up"][mlg_index])
#RooHistPdf_vvjets_electronidsf_up = ROOT.RooHistPdf("vvjets_electronidsfUp","",ROOT.RooArgSet(m),RooDataHist_vvjets_electronidsf_up)
    RooDataHist_vvjets_electronidsf_down = ROOT.RooDataHist("vvjets_electronidsfDown","",ROOT.RooArgList(m),makeDownShape(labels["vv+jets"]["hists-electron-id-sf-up"][mlg_index],labels["vv+jets"]["hists"][mlg_index]))
#RooHistPdf_vvjets_electronidsf_down = ROOT.RooHistPdf("vvjets_electronidsfDown","",ROOT.RooArgSet(m),RooDataHist_vvjets_electronidsf_down)


#electron hlt sf

    RooDataHist_wg_electronhltsf_up = ROOT.RooDataHist("wg_electronhltsfUp","",ROOT.RooArgList(m),labels["wg+jets"]["hists-electron-hlt-sf-up"][mlg_index])
#RooHistPdf_wg_electronhltsf_up = ROOT.RooHistPdf("wg_electronhltsfUp","",ROOT.RooArgSet(m),RooDataHist_wg_electronhltsf_up)
    RooDataHist_wg_electronhltsf_down = ROOT.RooDataHist("wg_electronhltsfDown","",ROOT.RooArgList(m),makeDownShape(labels["wg+jets"]["hists-electron-hlt-sf-up"][mlg_index],labels["wg+jets"]["hists"][mlg_index]))
#RooHistPdf_wg_electronhltsf_down = ROOT.RooHistPdf("wg_electronhltsfDown","",ROOT.RooArgSet(m),RooDataHist_wg_electronhltsf_down)

    RooDataHist_topjets_electronhltsf_up = ROOT.RooDataHist("topjets_electronhltsfUp","",ROOT.RooArgList(m),labels["top+jets"]["hists-electron-hlt-sf-up"][mlg_index])
#RooHistPdf_topjets_electronhltsf_up = ROOT.RooHistPdf("topjets_electronhltsfUp","",ROOT.RooArgSet(m),RooDataHist_topjets_electronhltsf_up)
    RooDataHist_topjets_electronhltsf_down = ROOT.RooDataHist("topjets_electronhltsfDown","",ROOT.RooArgList(m),makeDownShape(labels["top+jets"]["hists-electron-hlt-sf-up"][mlg_index],labels["top+jets"]["hists"][mlg_index]))
#RooHistPdf_topjets_electronhltsf_down = ROOT.RooHistPdf("topjets_electronhltsfDown","",ROOT.RooArgSet(m),RooDataHist_topjets_electronhltsf_down)

    RooDataHist_zgjets_electronhltsf_up = ROOT.RooDataHist("zgjets_electronhltsfUp","",ROOT.RooArgList(m),labels["zg+jets"]["hists-electron-hlt-sf-up"][mlg_index])
#RooHistPdf_zgjets_electronhltsf_up = ROOT.RooHistPdf("zgjets_electronhltsfUp","",ROOT.RooArgSet(m),RooDataHist_zgjets_electronhltsf_up)
    RooDataHist_zgjets_electronhltsf_down = ROOT.RooDataHist("zgjets_electronhltsfDown","",ROOT.RooArgList(m),makeDownShape(labels["zg+jets"]["hists-electron-hlt-sf-up"][mlg_index],labels["zg+jets"]["hists"][mlg_index]))
#RooHistPdf_zgjets_electronhltsf_down = ROOT.RooHistPdf("zgjets_electronhltsfDown","",ROOT.RooArgSet(m),RooDataHist_zgjets_electronhltsf_down)

    RooDataHist_vvjets_electronhltsf_up = ROOT.RooDataHist("vvjets_electronhltsfUp","",ROOT.RooArgList(m),labels["vv+jets"]["hists-electron-hlt-sf-up"][mlg_index])
#RooHistPdf_vvjets_electronhltsf_up = ROOT.RooHistPdf("vvjets_electronhltsfUp","",ROOT.RooArgSet(m),RooDataHist_vvjets_electronhltsf_up)
    RooDataHist_vvjets_electronhltsf_down = ROOT.RooDataHist("vvjets_electronhltsfDown","",ROOT.RooArgList(m),makeDownShape(labels["vv+jets"]["hists-electron-hlt-sf-up"][mlg_index],labels["vv+jets"]["hists"][mlg_index]))
#RooHistPdf_vvjets_electronhltsf_down = ROOT.RooHistPdf("vvjets_electronhltsfDown","",ROOT.RooArgSet(m),RooDataHist_vvjets_electronhltsf_down)

#muon hlt sf

    RooDataHist_wg_muonhltsf_up = ROOT.RooDataHist("wg_muonhltsfUp","",ROOT.RooArgList(m),labels["wg+jets"]["hists-muon-hlt-sf-up"][mlg_index])
#RooHistPdf_wg_muonhltsf_up = ROOT.RooHistPdf("wg_muonhltsfUp","",ROOT.RooArgSet(m),RooDataHist_wg_muonhltsf_up)
    RooDataHist_wg_muonhltsf_down = ROOT.RooDataHist("wg_muonhltsfDown","",ROOT.RooArgList(m),makeDownShape(labels["wg+jets"]["hists-muon-hlt-sf-up"][mlg_index],labels["wg+jets"]["hists"][mlg_index]))
#RooHistPdf_wg_muonhltsf_down = ROOT.RooHistPdf("wg_muonhltsfDown","",ROOT.RooArgSet(m),RooDataHist_wg_muonhltsf_down)

    RooDataHist_topjets_muonhltsf_up = ROOT.RooDataHist("topjets_muonhltsfUp","",ROOT.RooArgList(m),labels["top+jets"]["hists-muon-hlt-sf-up"][mlg_index])
#RooHistPdf_topjets_muonhltsf_up = ROOT.RooHistPdf("topjets_muonhltsfUp","",ROOT.RooArgSet(m),RooDataHist_topjets_muonhltsf_up)
    RooDataHist_topjets_muonhltsf_down = ROOT.RooDataHist("topjets_muonhltsfDown","",ROOT.RooArgList(m),makeDownShape(labels["top+jets"]["hists-muon-hlt-sf-up"][mlg_index],labels["top+jets"]["hists"][mlg_index]))
#RooHistPdf_topjets_muonhltsf_down = ROOT.RooHistPdf("topjets_muonhltsfDown","",ROOT.RooArgSet(m),RooDataHist_topjets_muonhltsf_down)

    RooDataHist_zgjets_muonhltsf_up = ROOT.RooDataHist("zgjets_muonhltsfUp","",ROOT.RooArgList(m),labels["zg+jets"]["hists-muon-hlt-sf-up"][mlg_index])
#RooHistPdf_zgjets_muonhltsf_up = ROOT.RooHistPdf("zgjets_muonhltsfUp","",ROOT.RooArgSet(m),RooDataHist_zgjets_muonhltsf_up)
    RooDataHist_zgjets_muonhltsf_down = ROOT.RooDataHist("zgjets_muonhltsfDown","",ROOT.RooArgList(m),makeDownShape(labels["zg+jets"]["hists-muon-hlt-sf-up"][mlg_index],labels["zg+jets"]["hists"][mlg_index]))
#RooHistPdf_zgjets_muonhltsf_down = ROOT.RooHistPdf("zgjets_muonhltsfDown","",ROOT.RooArgSet(m),RooDataHist_zgjets_muonhltsf_down)

    RooDataHist_vvjets_muonhltsf_up = ROOT.RooDataHist("vvjets_muonhltsfUp","",ROOT.RooArgList(m),labels["vv+jets"]["hists-muon-hlt-sf-up"][mlg_index])
#RooHistPdf_vvjets_muonhltsf_up = ROOT.RooHistPdf("vvjets_muonhltsfUp","",ROOT.RooArgSet(m),RooDataHist_vvjets_muonhltsf_up)
    RooDataHist_vvjets_muonhltsf_down = ROOT.RooDataHist("vvjets_muonhltsfDown","",ROOT.RooArgList(m),makeDownShape(labels["vv+jets"]["hists-muon-hlt-sf-up"][mlg_index],labels["vv+jets"]["hists"][mlg_index]))
#RooHistPdf_vvjets_muonhltsf_down = ROOT.RooHistPdf("vvjets_muonhltsfDown","",ROOT.RooArgSet(m),RooDataHist_vvjets_muonhltsf_down)

#muon iso sf

    RooDataHist_wg_muonisosf_up = ROOT.RooDataHist("wg_muonisosfUp","",ROOT.RooArgList(m),labels["wg+jets"]["hists-muon-iso-sf-up"][mlg_index])
#RooHistPdf_wg_muonisosf_up = ROOT.RooHistPdf("wg_muonisosfUp","",ROOT.RooArgSet(m),RooDataHist_wg_muonisosf_up)
    RooDataHist_wg_muonisosf_down = ROOT.RooDataHist("wg_muonisosfDown","",ROOT.RooArgList(m),makeDownShape(labels["wg+jets"]["hists-muon-iso-sf-up"][mlg_index],labels["wg+jets"]["hists"][mlg_index]))
#RooHistPdf_wg_muonisosf_down = ROOT.RooHistPdf("wg_muonisosfDown","",ROOT.RooArgSet(m),RooDataHist_wg_muonisosf_down)

    RooDataHist_topjets_muonisosf_up = ROOT.RooDataHist("topjets_muonisosfUp","",ROOT.RooArgList(m),labels["top+jets"]["hists-muon-iso-sf-up"][mlg_index])
#RooHistPdf_topjets_muonisosf_up = ROOT.RooHistPdf("topjets_muonisosfUp","",ROOT.RooArgSet(m),RooDataHist_topjets_muonisosf_up)
    RooDataHist_topjets_muonisosf_down = ROOT.RooDataHist("topjets_muonisosfDown","",ROOT.RooArgList(m),makeDownShape(labels["top+jets"]["hists-muon-iso-sf-up"][mlg_index],labels["top+jets"]["hists"][mlg_index]))
#RooHistPdf_topjets_muonisosf_down = ROOT.RooHistPdf("topjets_muonisosfDown","",ROOT.RooArgSet(m),RooDataHist_topjets_muonisosf_down)

    RooDataHist_zgjets_muonisosf_up = ROOT.RooDataHist("zgjets_muonisosfUp","",ROOT.RooArgList(m),labels["zg+jets"]["hists-muon-iso-sf-up"][mlg_index])
#RooHistPdf_zgjets_muonisosf_up = ROOT.RooHistPdf("zgjets_muonisosfUp","",ROOT.RooArgSet(m),RooDataHist_zgjets_muonisosf_up)
    RooDataHist_zgjets_muonisosf_down = ROOT.RooDataHist("zgjets_muonisosfDown","",ROOT.RooArgList(m),makeDownShape(labels["zg+jets"]["hists-muon-iso-sf-up"][mlg_index],labels["zg+jets"]["hists"][mlg_index]))
#RooHistPdf_zgjets_muonisosf_down = ROOT.RooHistPdf("zgjets_muonisosfDown","",ROOT.RooArgSet(m),RooDataHist_zgjets_muonisosf_down)

    RooDataHist_vvjets_muonisosf_up = ROOT.RooDataHist("vvjets_muonisosfUp","",ROOT.RooArgList(m),labels["vv+jets"]["hists-muon-iso-sf-up"][mlg_index])
#RooHistPdf_vvjets_muonisosf_up = ROOT.RooHistPdf("vvjets_muonisosfUp","",ROOT.RooArgSet(m),RooDataHist_vvjets_muonisosf_up)
    RooDataHist_vvjets_muonisosf_down = ROOT.RooDataHist("vvjets_muonisosfDown","",ROOT.RooArgList(m),makeDownShape(labels["vv+jets"]["hists-muon-iso-sf-up"][mlg_index],labels["vv+jets"]["hists"][mlg_index]))
#RooHistPdf_vvjets_muonisosf_down = ROOT.RooHistPdf("vvjets_muonisosfDown","",ROOT.RooArgSet(m),RooDataHist_vvjets_muonisosf_down)

#muon id sf

    RooDataHist_wg_muonidsf_up = ROOT.RooDataHist("wg_muonidsfUp","",ROOT.RooArgList(m),labels["wg+jets"]["hists-muon-id-sf-up"][mlg_index])
#RooHistPdf_wg_muonidsf_up = ROOT.RooHistPdf("wg_muonidsfUp","",ROOT.RooArgSet(m),RooDataHist_wg_muonidsf_up)
    RooDataHist_wg_muonidsf_down = ROOT.RooDataHist("wg_muonidsfDown","",ROOT.RooArgList(m),makeDownShape(labels["wg+jets"]["hists-muon-id-sf-up"][mlg_index],labels["wg+jets"]["hists"][mlg_index]))
#RooHistPdf_wg_muonidsf_down = ROOT.RooHistPdf("wg_muonidsfDown","",ROOT.RooArgSet(m),RooDataHist_wg_muonidsf_down)

    RooDataHist_topjets_muonidsf_up = ROOT.RooDataHist("topjets_muonidsfUp","",ROOT.RooArgList(m),labels["top+jets"]["hists-muon-id-sf-up"][mlg_index])
#RooHistPdf_topjets_muonidsf_up = ROOT.RooHistPdf("topjets_muonidsfUp","",ROOT.RooArgSet(m),RooDataHist_topjets_muonidsf_up)
    RooDataHist_topjets_muonidsf_down = ROOT.RooDataHist("topjets_muonidsfDown","",ROOT.RooArgList(m),makeDownShape(labels["top+jets"]["hists-muon-id-sf-up"][mlg_index],labels["top+jets"]["hists"][mlg_index]))
#RooHistPdf_topjets_muonidsf_down = ROOT.RooHistPdf("topjets_muonidsfDown","",ROOT.RooArgSet(m),RooDataHist_topjets_muonidsf_down)

    RooDataHist_zgjets_muonidsf_up = ROOT.RooDataHist("zgjets_muonidsfUp","",ROOT.RooArgList(m),labels["zg+jets"]["hists-muon-id-sf-up"][mlg_index])
#RooHistPdf_zgjets_muonidsf_up = ROOT.RooHistPdf("zgjets_muonidsfUp","",ROOT.RooArgSet(m),RooDataHist_zgjets_muonidsf_up)
    RooDataHist_zgjets_muonidsf_down = ROOT.RooDataHist("zgjets_muonidsfDown","",ROOT.RooArgList(m),makeDownShape(labels["zg+jets"]["hists-muon-id-sf-up"][mlg_index],labels["zg+jets"]["hists"][mlg_index]))
#RooHistPdf_zgjets_muonidsf_down = ROOT.RooHistPdf("zgjets_muonidsfDown","",ROOT.RooArgSet(m),RooDataHist_zgjets_muonidsf_down)

    RooDataHist_vvjets_muonidsf_up = ROOT.RooDataHist("vvjets_muonidsfUp","",ROOT.RooArgList(m),labels["vv+jets"]["hists-muon-id-sf-up"][mlg_index])
#RooHistPdf_vvjets_muonidsf_up = ROOT.RooHistPdf("vvjets_muonidsfUp","",ROOT.RooArgSet(m),RooDataHist_vvjets_muonidsf_up)
    RooDataHist_vvjets_muonidsf_down = ROOT.RooDataHist("vvjets_muonidsfDown","",ROOT.RooArgList(m),makeDownShape(labels["vv+jets"]["hists-muon-id-sf-up"][mlg_index],labels["vv+jets"]["hists"][mlg_index]))
#RooHistPdf_vvjets_muonidsf_down = ROOT.RooHistPdf("vvjets_muonidsfDown","",ROOT.RooArgSet(m),RooDataHist_vvjets_muonidsf_down)

#print "RooParametricShapeBinPdf_bwcb.getNorm() = " + str(RooParametricShapeBinPdf_bwcb.getNorm()) 

    ws=ROOT.RooWorkspace()

#ws.import(...) does not work because import is a keyword in python

#getattr(ws,"import")(bwcb_norm)

    getattr(ws,"import")(m)
    getattr(ws,"import")(m0)
    getattr(ws,"import")(sigma)
    getattr(ws,"import")(alpha)
    getattr(ws,"import")(n)
    getattr(ws,"import")(width)
    getattr(ws,"import")(mass)
    getattr(ws,"import")(bw)
    getattr(ws,"import")(cb)
    getattr(ws,"import")(RooFFTConvPdf_bwcb,ROOT.RooFit.RecycleConflictNodes())
    getattr(ws,"import")(RooParametricShapeBinPdf_bwcb,ROOT.RooFit.RecycleConflictNodes())
    getattr(ws,"import")(bwcbbin_norm)
    
    getattr(ws,"import")(RooDataHist_wg)
    getattr(ws,"import")(RooDataHist_vvjets)
    getattr(ws,"import")(RooDataHist_zgjets)
    getattr(ws,"import")(RooDataHist_topjets)
    getattr(ws,"import")(RooDataHist_fake_lepton)
    getattr(ws,"import")(RooDataHist_fake_photon)
    getattr(ws,"import")(RooDataHist_double_fake)
    getattr(ws,"import")(RooDataHist_e_to_p_non_res)
    
    getattr(ws,"import")(RooDataHist_fake_photon_syst1_up)
    getattr(ws,"import")(RooDataHist_fake_photon_syst1_down)
    getattr(ws,"import")(RooDataHist_fake_photon_syst2_up)
    getattr(ws,"import")(RooDataHist_fake_photon_syst2_down)

    for i in range(1,labels["wg+jets"]["hists"][mlg_index].GetNbinsX()+1):
        getattr(ws,"import")(list_RooDataHist_wg_stat_up[i-1])
        getattr(ws,"import")(list_RooDataHist_wg_stat_down[i-1])

#    for i in range(1,fake_photon["hists"][mlg_index].GetNbinsX()+1):
#        getattr(ws,"import")(list_RooDataHist_fake_photon_syst2_up[i-1])
#        getattr(ws,"import")(list_RooDataHist_fake_photon_syst2_down[i-1])

    for i in range(1,fake_lepton["hists"][mlg_index].GetNbinsX()+1):
        getattr(ws,"import")(list_RooDataHist_fake_lepton_syst_up[i-1])
        getattr(ws,"import")(list_RooDataHist_fake_lepton_syst_down[i-1])

    for i in range(1,labels["zg+jets"]["hists"][mlg_index].GetNbinsX()+1):
        getattr(ws,"import")(list_RooDataHist_zgjets_stat_up[i-1])
        getattr(ws,"import")(list_RooDataHist_zgjets_stat_down[i-1])


#    getattr(ws,"import")(RooDataHist_fake_electron_syst_up)
#    getattr(ws,"import")(RooDataHist_fake_electron_syst_down)
    getattr(ws,"import")(RooDataHist_wg_scale_up)
    getattr(ws,"import")(RooDataHist_wg_scale_down)
    getattr(ws,"import")(RooDataHist_zg_scale_up)
    getattr(ws,"import")(RooDataHist_zg_scale_down)
    
    getattr(ws,"import")(RooDataHist_wg_pileup_up)
    getattr(ws,"import")(RooDataHist_wg_pileup_down)
    getattr(ws,"import")(RooDataHist_vvjets_pileup_up)
    getattr(ws,"import")(RooDataHist_vvjets_pileup_down)
    getattr(ws,"import")(RooDataHist_zgjets_pileup_up)
    getattr(ws,"import")(RooDataHist_zgjets_pileup_down)
    getattr(ws,"import")(RooDataHist_topjets_pileup_up)
    getattr(ws,"import")(RooDataHist_topjets_pileup_down)
    
    getattr(ws,"import")(RooDataHist_wg_prefire_up)
    getattr(ws,"import")(RooDataHist_wg_prefire_down)
    getattr(ws,"import")(RooDataHist_vvjets_prefire_up)
    getattr(ws,"import")(RooDataHist_vvjets_prefire_down)
    getattr(ws,"import")(RooDataHist_zgjets_prefire_up)
    getattr(ws,"import")(RooDataHist_zgjets_prefire_down)
    getattr(ws,"import")(RooDataHist_topjets_prefire_up)
    getattr(ws,"import")(RooDataHist_topjets_prefire_down)
    
    getattr(ws,"import")(RooDataHist_wg_jes_up)
    getattr(ws,"import")(RooDataHist_wg_jes_down)
    getattr(ws,"import")(RooDataHist_vvjets_jes_up)
    getattr(ws,"import")(RooDataHist_vvjets_jes_down)
    getattr(ws,"import")(RooDataHist_zgjets_jes_up)
    getattr(ws,"import")(RooDataHist_zgjets_jes_down)
    getattr(ws,"import")(RooDataHist_topjets_jes_up)
    getattr(ws,"import")(RooDataHist_topjets_jes_down)
    
    getattr(ws,"import")(RooDataHist_wg_jer_up)
    getattr(ws,"import")(RooDataHist_wg_jer_down)
    getattr(ws,"import")(RooDataHist_vvjets_jer_up)
    getattr(ws,"import")(RooDataHist_vvjets_jer_down)
    getattr(ws,"import")(RooDataHist_zgjets_jer_up)
    getattr(ws,"import")(RooDataHist_zgjets_jer_down)
    getattr(ws,"import")(RooDataHist_topjets_jer_up)
    getattr(ws,"import")(RooDataHist_topjets_jer_down)
    
    getattr(ws,"import")(RooDataHist_wg_electronrecosf_up)
    getattr(ws,"import")(RooDataHist_wg_electronrecosf_down)
    getattr(ws,"import")(RooDataHist_vvjets_electronrecosf_up)
    getattr(ws,"import")(RooDataHist_vvjets_electronrecosf_down)
    getattr(ws,"import")(RooDataHist_zgjets_electronrecosf_up)
    getattr(ws,"import")(RooDataHist_zgjets_electronrecosf_down)
    getattr(ws,"import")(RooDataHist_topjets_electronrecosf_up)
    getattr(ws,"import")(RooDataHist_topjets_electronrecosf_down)
    
    getattr(ws,"import")(RooDataHist_wg_electronidsf_up)
    getattr(ws,"import")(RooDataHist_wg_electronidsf_down)
    getattr(ws,"import")(RooDataHist_vvjets_electronidsf_up)
    getattr(ws,"import")(RooDataHist_vvjets_electronidsf_down)
    getattr(ws,"import")(RooDataHist_zgjets_electronidsf_up)
    getattr(ws,"import")(RooDataHist_zgjets_electronidsf_down)
    getattr(ws,"import")(RooDataHist_topjets_electronidsf_up)
    getattr(ws,"import")(RooDataHist_topjets_electronidsf_down)
    
    getattr(ws,"import")(RooDataHist_wg_electronhltsf_up)
    getattr(ws,"import")(RooDataHist_wg_electronhltsf_down)
    getattr(ws,"import")(RooDataHist_vvjets_electronhltsf_up)
    getattr(ws,"import")(RooDataHist_vvjets_electronhltsf_down)
    getattr(ws,"import")(RooDataHist_zgjets_electronhltsf_up)
    getattr(ws,"import")(RooDataHist_zgjets_electronhltsf_down)
    getattr(ws,"import")(RooDataHist_topjets_electronhltsf_up)
    getattr(ws,"import")(RooDataHist_topjets_electronhltsf_down)
    
    getattr(ws,"import")(RooDataHist_wg_muonidsf_up)
    getattr(ws,"import")(RooDataHist_wg_muonidsf_down)
    getattr(ws,"import")(RooDataHist_vvjets_muonidsf_up)
    getattr(ws,"import")(RooDataHist_vvjets_muonidsf_down)
    getattr(ws,"import")(RooDataHist_zgjets_muonidsf_up)
    getattr(ws,"import")(RooDataHist_zgjets_muonidsf_down)
    getattr(ws,"import")(RooDataHist_topjets_muonidsf_up)
    getattr(ws,"import")(RooDataHist_topjets_muonidsf_down)
    
    getattr(ws,"import")(RooDataHist_wg_muonhltsf_up)
    getattr(ws,"import")(RooDataHist_wg_muonhltsf_down)
    getattr(ws,"import")(RooDataHist_vvjets_muonhltsf_up)
    getattr(ws,"import")(RooDataHist_vvjets_muonhltsf_down)
    getattr(ws,"import")(RooDataHist_zgjets_muonhltsf_up)
    getattr(ws,"import")(RooDataHist_zgjets_muonhltsf_down)
    getattr(ws,"import")(RooDataHist_topjets_muonhltsf_up)
    getattr(ws,"import")(RooDataHist_topjets_muonhltsf_down)
    
    getattr(ws,"import")(RooDataHist_wg_muonisosf_up)
    getattr(ws,"import")(RooDataHist_wg_muonisosf_down)
    getattr(ws,"import")(RooDataHist_vvjets_muonisosf_up)
    getattr(ws,"import")(RooDataHist_vvjets_muonisosf_down)
    getattr(ws,"import")(RooDataHist_zgjets_muonisosf_up)
    getattr(ws,"import")(RooDataHist_zgjets_muonisosf_down)
    getattr(ws,"import")(RooDataHist_topjets_muonisosf_up)
    getattr(ws,"import")(RooDataHist_topjets_muonisosf_down)
    

    RooDataHist_data = ROOT.RooDataHist("","",ROOT.RooArgList(m),data["hists"][mlg_index])

    getattr(ws,"import")(RooDataHist_data.Clone("data_obs"))

    ws.Write("workspace")

    ws.Delete() #if we do not delete the workspace explcitly, there is a crash at the end

    shapes.Close()

if not options.ewdim6:
    sys.exit(0)

wgjets_ewdim6_scale_syst=histogram_models[ewdim6_index].GetHistogram()

for i in range(labels["wg+jets"]["hists-scale-variation0"][ewdim6_index].GetNbinsX()+1):
    wgjets_ewdim6_scale_syst.SetBinContent(i,labels["wg+jets"]["hists"][ewdim6_index].GetBinContent(i)+max(
        abs(labels["wg+jets"]["hists-scale-variation0"][ewdim6_index].GetBinContent(i)-labels["wg+jets"]["hists"][ewdim6_index].GetBinContent(i)),
        abs(labels["wg+jets"]["hists-scale-variation1"][ewdim6_index].GetBinContent(i)-labels["wg+jets"]["hists"][ewdim6_index].GetBinContent(i)),
        abs(labels["wg+jets"]["hists-scale-variation3"][ewdim6_index].GetBinContent(i)-labels["wg+jets"]["hists"][ewdim6_index].GetBinContent(i)),
        abs(labels["wg+jets"]["hists-scale-variation4"][ewdim6_index].GetBinContent(i)-labels["wg+jets"]["hists"][ewdim6_index].GetBinContent(i)),
        abs(labels["wg+jets"]["hists-scale-variation5"][ewdim6_index].GetBinContent(i)-labels["wg+jets"]["hists"][ewdim6_index].GetBinContent(i)),
        abs(labels["wg+jets"]["hists-scale-variation6"][ewdim6_index].GetBinContent(i)-labels["wg+jets"]["hists"][ewdim6_index].GetBinContent(i))))

wgjets_ewdim6_pdf_syst=histogram_models[ewdim6_index].GetHistogram()

for i in range(labels["wg+jets"]["hists-pdf-variation0"][ewdim6_index].GetNbinsX()+1):
    mean_pdf=0

    for j in range(1,32):
        mean_pdf += labels["wg+jets"]["hists-pdf-variation"+str(j)][ewdim6_index].GetBinContent(i)

    mean_pdf = mean_pdf/31

    stddev_pdf = 0

    for j in range(1,32):
        stddev_pdf += pow(labels["wg+jets"]["hists-pdf-variation"+str(j)][ewdim6_index].GetBinContent(i) - mean_pdf,2)

    stddev_pdf = sqrt(stddev_pdf/(31-1))

    wgjets_ewdim6_pdf_syst.SetBinContent(i,labels["wg+jets"]["hists"][ewdim6_index].GetBinContent(i)+stddev_pdf)

zgjets_ewdim6_scale_syst=histogram_models[ewdim6_index].GetHistogram()

for i in range(labels["zg+jets"]["hists-scale-variation0"][ewdim6_index].GetNbinsX()+1):
    zgjets_ewdim6_scale_syst.SetBinContent(i,labels["zg+jets"]["hists"][ewdim6_index].GetBinContent(i)+max(
        abs(labels["zg+jets"]["hists-scale-variation0"][ewdim6_index].GetBinContent(i)-labels["zg+jets"]["hists"][ewdim6_index].GetBinContent(i)),
        abs(labels["zg+jets"]["hists-scale-variation1"][ewdim6_index].GetBinContent(i)-labels["zg+jets"]["hists"][ewdim6_index].GetBinContent(i)),
        abs(labels["zg+jets"]["hists-scale-variation3"][ewdim6_index].GetBinContent(i)-labels["zg+jets"]["hists"][ewdim6_index].GetBinContent(i)),
        abs(labels["zg+jets"]["hists-scale-variation4"][ewdim6_index].GetBinContent(i)-labels["zg+jets"]["hists"][ewdim6_index].GetBinContent(i)),
        abs(labels["zg+jets"]["hists-scale-variation5"][ewdim6_index].GetBinContent(i)-labels["zg+jets"]["hists"][ewdim6_index].GetBinContent(i)),
        abs(labels["zg+jets"]["hists-scale-variation6"][ewdim6_index].GetBinContent(i)-labels["zg+jets"]["hists"][ewdim6_index].GetBinContent(i))))

zgjets_ewdim6_pdf_syst=histogram_models[ewdim6_index].GetHistogram()

for i in range(labels["zg+jets"]["hists-pdf-variation0"][ewdim6_index].GetNbinsX()+1):
    mean_pdf=0

    for j in range(1,32):
        mean_pdf += labels["zg+jets"]["hists-pdf-variation"+str(j)][ewdim6_index].GetBinContent(i)

    mean_pdf = mean_pdf/31

    stddev_pdf = 0

    for j in range(1,32):
        stddev_pdf += pow(labels["zg+jets"]["hists-pdf-variation"+str(j)][ewdim6_index].GetBinContent(i) - mean_pdf,2)

    stddev_pdf = sqrt(stddev_pdf/(31-1))

    zgjets_ewdim6_pdf_syst.SetBinContent(i,labels["zg+jets"]["hists"][ewdim6_index].GetBinContent(i)+stddev_pdf)

for i in range(1,sm_lhe_weight_hist.GetNbinsX()+1):

    dcard = open("wg_dcard_ewdim6_bin"+str(i)+".txt",'w')

    print >> dcard, "imax 1 number of channels"
    print >> dcard, "jmax * number of background"
    print >> dcard, "kmax * number of nuisance parameters"
    print >> dcard, "Observation "+str(data["hists"][ewdim6_index].GetBinContent(i))
    dcard.write("bin")
    dcard.write(" bin1")
    
    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" bin1")

    dcard.write(" bin1")    
    dcard.write(" bin1")    
    dcard.write(" bin1")    
    dcard.write(" bin1")    
    dcard.write('\n')    
    
    dcard.write("process")
    dcard.write(" Wg")
        
    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" " + label)

    dcard.write(" fake_photon")
    dcard.write(" fake_lepton")
    dcard.write(" double_fake")
    dcard.write(" e_to_p_non_res")
    dcard.write('\n')    
    dcard.write("process")
    dcard.write(" 0")
    
    for j in range(1,len(labels.keys())+2):
        dcard.write(" " + str(j))
    dcard.write('\n')    
    dcard.write('rate')
    dcard.write(' '+str(sm_lhe_weight_hist.GetBinContent(i)))
#    dcard.write(' '+str(labels["wg+jets"]["hists"][ewdim6_index].GetBinContent(i)))
    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        if labels[label]["hists"][ewdim6_index].GetBinContent(i) > 0:
            dcard.write(" "+ str(labels[label]["hists"][ewdim6_index].GetBinContent(i)))
        else:
            dcard.write(" 0.0001") 



    if fake_photon["hists"][ewdim6_index].GetBinContent(i) > 0:        
        dcard.write(" "+str(fake_photon["hists"][ewdim6_index].GetBinContent(i))) 
    else:
        if fake_photon["hists"][ewdim6_index].GetBinContent(i) < 0:
            print "Warning: fake photon estimate is "+str(fake_photon["hists"][ewdim6_index].GetBinContent(i))+ " for bin " + str(i) + ". It will be replaced with 0.0001"
        dcard.write(" 0.0001") 

    if fake_lepton["hists"][ewdim6_index].GetBinContent(i) > 0:        
        dcard.write(" "+str(fake_lepton["hists"][ewdim6_index].GetBinContent(i))) 
    else:
        if fake_lepton["hists"][ewdim6_index].GetBinContent(i) < 0:
            print "Warning: fake lepton estimate is "+str(fake_lepton["hists"][ewdim6_index].GetBinContent(i))+ " for bin " + str(i) + ". It will be replaced with 0.0001"
        dcard.write(" 0.0001") 

    if double_fake["hists"][ewdim6_index].GetBinContent(i) > 0:        
        dcard.write(" "+str(double_fake["hists"][ewdim6_index].GetBinContent(i))) 
    else:
        if double_fake["hists"][ewdim6_index].GetBinContent(i) < 0:
            print "Warning: double fake estimate is "+str(double_fake["hists"][ewdim6_index].GetBinContent(i))+ " for bin " + str(i) + ". It will be replaced with 0.0001"
        dcard.write(" 0.0001") 

    if e_to_p["hists"][ewdim6_index].GetBinContent(i) > 0:        
        dcard.write(" "+str(e_to_p["hists"][ewdim6_index].GetBinContent(i))) 
    else:
        dcard.write(" 0.0001") 
   
    dcard.write('\n')    

    dcard.write("lumi_13tev lnN")
    dcard.write(" 1.018")

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" 1.018")

    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" 1.018")

    dcard.write('\n')    

    if sm_lhe_weight_hist.GetBinContent(i) > 0:
        dcard.write("mcstat_ewdim6_bin"+str(i)+" lnN "+str(1+sm_lhe_weight_hist.GetBinError(i)/sm_lhe_weight_hist.GetBinContent(i)))
        
#        dcard.write("mcstat_ewdim6_bin"+str(i)+" lnN "+str(1+labels["wg+jets"]["hists"][ewdim6_index].GetBinError(i)/labels["wg+jets"]["hists"][ewdim6_index].GetBinContent(i)))
        for label in labels.keys():
            if label == "no label" or label == "wg+jets" or label == "w+jets":
                continue
            dcard.write(" -")

        dcard.write(" -")                
        dcard.write(" -")                
        dcard.write(" -")                
        dcard.write(" -")                
        dcard.write("\n")  

    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue

        if labels[label]["hists"][ewdim6_index].GetBinContent(i) > 0:
            dcard.write("mcstat_"+str(label)+"_bin"+str(i)+" lnN ")
            dcard.write(" -")

            for l in labels.keys():
                if l == "no label" or l == "wg+jets" or label == "w+jets":
                    continue
                if l == label:
                    dcard.write(" "+str(1+labels[label]["hists"][ewdim6_index].GetBinError(i)/labels[label]["hists"][ewdim6_index].GetBinContent(i)))
                else:    
                    dcard.write(" -")

            dcard.write(" -")                
            dcard.write(" -")                
            dcard.write(" -")                
            dcard.write(" -")                
            dcard.write("\n")  

    if fake_lepton["hists"][ewdim6_index].GetBinContent(i) > 0:        
        dcard.write("fake_lepton_syst lnN -")
        for label in labels.keys():
            if label == "no label" or label == "wg+jets" or label == "w+jets":
                continue
            dcard.write(" -")

        dcard.write(" -")                
        dcard.write(" 1.3")                
        dcard.write(" -")                
        dcard.write(" -")                
        dcard.write("\n")  

    if fake_lepton["hists"][ewdim6_index].GetBinContent(i) > 0:        
        dcard.write("fake_lepton_stat lnN -")
        for label in labels.keys():
            if label == "no label" or label == "wg+jets" or label == "w+jets":
                continue
            dcard.write(" -")

        dcard.write(" -")                
        dcard.write(" "+str(1+fake_lepton["hists"][ewdim6_index].GetBinError(i)/fake_lepton["hists"][ewdim6_index].GetBinContent(i)))
        dcard.write(" -")                
        dcard.write(" -")                
        dcard.write("\n")  

    if fake_photon["hists"][ewdim6_index].GetBinContent(i) > 0:        
        dcard.write("fake_photon_stat lnN -")
        for label in labels.keys():
            if label == "no label" or label == "wg+jets" or label == "w+jets" :
                continue
            dcard.write(" -")

        dcard.write(" "+str(1+fake_photon["hists"][ewdim6_index].GetBinError(i)/fake_photon["hists"][ewdim6_index].GetBinContent(i)))
        dcard.write(" -")                
        dcard.write(" -")                
        dcard.write(" -")                
        dcard.write("\n")  

    dcard.write("muon_id_sf lnN "+str(labels["wg+jets"]["hists-muon-id-sf-up"][ewdim6_index].GetBinContent(i)/labels["wg+jets"]["hists"][ewdim6_index].GetBinContent(i)))
    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        if labels[label]["hists"][ewdim6_index].GetBinContent(i) > 0:
            dcard.write(" "+str(labels[label]["hists-muon-id-sf-up"][ewdim6_index].GetBinContent(i)/labels[label]["hists"][ewdim6_index].GetBinContent(i)))
        else:    
            dcard.write(" -")

    dcard.write(" -")
    dcard.write(" -")                
    dcard.write(" -")                
    dcard.write(" -")            
    dcard.write("\n")  

    dcard.write("muon_hlt_sf lnN "+str(labels["wg+jets"]["hists-muon-hlt-sf-up"][ewdim6_index].GetBinContent(i)/labels["wg+jets"]["hists"][ewdim6_index].GetBinContent(i)))
    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        if labels[label]["hists"][ewdim6_index].GetBinContent(i) > 0:
            dcard.write(" "+str(labels[label]["hists-muon-hlt-sf-up"][ewdim6_index].GetBinContent(i)/labels[label]["hists"][ewdim6_index].GetBinContent(i)))
        else:    
            dcard.write(" -")

    dcard.write(" -")
    dcard.write(" -")                
    dcard.write(" -")                
    dcard.write(" -")            
    dcard.write("\n")  

    dcard.write("muon_iso_sf lnN "+str(labels["wg+jets"]["hists-muon-iso-sf-up"][ewdim6_index].GetBinContent(i)/labels["wg+jets"]["hists"][ewdim6_index].GetBinContent(i)))
    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        if labels[label]["hists"][ewdim6_index].GetBinContent(i) > 0:
            dcard.write(" "+str(labels[label]["hists-muon-iso-sf-up"][ewdim6_index].GetBinContent(i)/labels[label]["hists"][ewdim6_index].GetBinContent(i)))
        else:    
            dcard.write(" -")

    dcard.write(" -")
    dcard.write(" -")                
    dcard.write(" -")                
    dcard.write(" -")            
    dcard.write("\n")  

    dcard.write("electron_hlt_sf lnN "+str(labels["wg+jets"]["hists-electron-hlt-sf-up"][ewdim6_index].GetBinContent(i)/labels["wg+jets"]["hists"][ewdim6_index].GetBinContent(i)))
    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        if labels[label]["hists"][ewdim6_index].GetBinContent(i) > 0:
            dcard.write(" "+str(labels[label]["hists-electron-hlt-sf-up"][ewdim6_index].GetBinContent(i)/labels[label]["hists"][ewdim6_index].GetBinContent(i)))
        else:    
            dcard.write(" -")

    dcard.write(" -")
    dcard.write(" -")                
    dcard.write(" -")                
    if e_to_p["hists"][ewdim6_index].GetBinContent(i) > 0:
        dcard.write(" "+str(e_to_p["hists-electron-hlt-sf-up"][ewdim6_index].GetBinContent(i)/e_to_p["hists"][ewdim6_index].GetBinContent(i)))
    else:    
        dcard.write(" -")            
    dcard.write("\n")  

    dcard.write("electron_id_sf lnN "+str(labels["wg+jets"]["hists-electron-id-sf-up"][ewdim6_index].GetBinContent(i)/labels["wg+jets"]["hists"][ewdim6_index].GetBinContent(i)))
    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        if labels[label]["hists"][ewdim6_index].GetBinContent(i) > 0:
            dcard.write(" "+str(labels[label]["hists-electron-id-sf-up"][ewdim6_index].GetBinContent(i)/labels[label]["hists"][ewdim6_index].GetBinContent(i)))
        else:    
            dcard.write(" -")

    dcard.write(" -")
    dcard.write(" -")                
    dcard.write(" -")                
    if e_to_p["hists"][ewdim6_index].GetBinContent(i) > 0:
        dcard.write(" "+str(e_to_p["hists-electron-id-sf-up"][ewdim6_index].GetBinContent(i)/e_to_p["hists"][ewdim6_index].GetBinContent(i)))
    else:    
        dcard.write(" -")            
    dcard.write("\n")  

    dcard.write("electron_reco_sf lnN "+str(labels["wg+jets"]["hists-electron-reco-sf-up"][ewdim6_index].GetBinContent(i)/labels["wg+jets"]["hists"][ewdim6_index].GetBinContent(i)))
    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        if labels[label]["hists"][ewdim6_index].GetBinContent(i) > 0:
            dcard.write(" "+str(labels[label]["hists-electron-reco-sf-up"][ewdim6_index].GetBinContent(i)/labels[label]["hists"][ewdim6_index].GetBinContent(i)))
        else:    
            dcard.write(" -")

    dcard.write(" -")
    dcard.write(" -")                
    dcard.write(" -")                
    if e_to_p["hists"][ewdim6_index].GetBinContent(i) > 0:
        dcard.write(" "+str(e_to_p["hists-electron-reco-sf-up"][ewdim6_index].GetBinContent(i)/e_to_p["hists"][ewdim6_index].GetBinContent(i)))
    else:    
        dcard.write(" -")            
    dcard.write("\n")  

    dcard.write("photon_id_sf lnN "+str(labels["wg+jets"]["hists-photon-id-sf-up"][ewdim6_index].GetBinContent(i)/labels["wg+jets"]["hists"][ewdim6_index].GetBinContent(i)))
    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        if labels[label]["hists"][ewdim6_index].GetBinContent(i) > 0:
            dcard.write(" "+str(labels[label]["hists-photon-id-sf-up"][ewdim6_index].GetBinContent(i)/labels[label]["hists"][ewdim6_index].GetBinContent(i)))
        else:    
            dcard.write(" -")

    dcard.write(" -")
    dcard.write(" -")                
    dcard.write(" -")                
    if e_to_p["hists"][ewdim6_index].GetBinContent(i) > 0:
        dcard.write(" "+str(e_to_p["hists-photon-id-sf-up"][ewdim6_index].GetBinContent(i)/e_to_p["hists"][ewdim6_index].GetBinContent(i)))
    else:    
        dcard.write(" -")            
    dcard.write("\n")  

    dcard.write("jes lnN "+str(labels["wg+jets"]["hists-jes-up"][ewdim6_index].GetBinContent(i)/labels["wg+jets"]["hists"][ewdim6_index].GetBinContent(i)))
    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        if labels[label]["hists"][ewdim6_index].GetBinContent(i) > 0:
            dcard.write(" "+str(labels[label]["hists-jes-up"][ewdim6_index].GetBinContent(i)/labels[label]["hists"][ewdim6_index].GetBinContent(i)))
        else:    
            dcard.write(" -")

    dcard.write(" -")
    dcard.write(" -")                
    dcard.write(" -")                
    if e_to_p["hists"][ewdim6_index].GetBinContent(i) > 0:
        dcard.write(" "+str(e_to_p["hists-jes-up"][ewdim6_index].GetBinContent(i)/e_to_p["hists"][ewdim6_index].GetBinContent(i)))
    else:    
        dcard.write(" -")            
    dcard.write("\n")  

    dcard.write("jer lnN "+str(labels["wg+jets"]["hists-jer-up"][ewdim6_index].GetBinContent(i)/labels["wg+jets"]["hists"][ewdim6_index].GetBinContent(i)))
    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        if labels[label]["hists"][ewdim6_index].GetBinContent(i) > 0:
            dcard.write(" "+str(labels[label]["hists-jer-up"][ewdim6_index].GetBinContent(i)/labels[label]["hists"][ewdim6_index].GetBinContent(i)))
        else:    
            dcard.write(" -")

    dcard.write(" -")
    dcard.write(" -")                
    dcard.write(" -")                
    if e_to_p["hists"][ewdim6_index].GetBinContent(i) > 0:
        dcard.write(" "+str(e_to_p["hists-jer-up"][ewdim6_index].GetBinContent(i)/e_to_p["hists"][ewdim6_index].GetBinContent(i)))
    else:    
        dcard.write(" -")            
    dcard.write("\n")  

    dcard.write("prefire lnN "+str(labels["wg+jets"]["hists-prefire-up"][ewdim6_index].GetBinContent(i)/labels["wg+jets"]["hists"][ewdim6_index].GetBinContent(i)))
    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        if labels[label]["hists"][ewdim6_index].GetBinContent(i) > 0:
            dcard.write(" "+str(labels[label]["hists-prefire-up"][ewdim6_index].GetBinContent(i)/labels[label]["hists"][ewdim6_index].GetBinContent(i)))
        else:    
            dcard.write(" -")

    dcard.write(" -")
    dcard.write(" -")                
    dcard.write(" -")            
    if e_to_p["hists"][ewdim6_index].GetBinContent(i) > 0:
        dcard.write(" "+str(e_to_p["hists-prefire-up"][ewdim6_index].GetBinContent(i)/e_to_p["hists"][ewdim6_index].GetBinContent(i)))
    else:    
        dcard.write(" -")            
    dcard.write("\n")  

    dcard.write("pileup lnN "+str(labels["wg+jets"]["hists-pileup-up"][ewdim6_index].GetBinContent(i)/labels["wg+jets"]["hists"][ewdim6_index].GetBinContent(i)))
    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        if labels[label]["hists"][ewdim6_index].GetBinContent(i) > 0:
            dcard.write(" "+str(labels[label]["hists-pileup-up"][ewdim6_index].GetBinContent(i)/labels[label]["hists"][ewdim6_index].GetBinContent(i)))
        else:    
            dcard.write(" -")

    dcard.write(" -")
    dcard.write(" -")                
    dcard.write(" -")        
    if e_to_p["hists"][ewdim6_index].GetBinContent(i) > 0:
        dcard.write(" "+str(e_to_p["hists-pileup-up"][ewdim6_index].GetBinContent(i)/e_to_p["hists"][ewdim6_index].GetBinContent(i)))
    else:    
        dcard.write(" -")        
    dcard.write("\n")  

    dcard.write("wgscale lnN "+str(wgjets_ewdim6_scale_syst.GetBinContent(i)/labels["wg+jets"]["hists"][ewdim6_index].GetBinContent(i)))
    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" -")

    dcard.write(" -")
    dcard.write(" -")                
    dcard.write(" -")        
    dcard.write(" -")        
    dcard.write("\n")  

    dcard.write("wgpdf lnN "+str(wgjets_ewdim6_pdf_syst.GetBinContent(i)/labels["wg+jets"]["hists"][ewdim6_index].GetBinContent(i)))
    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue
        dcard.write(" -")

    dcard.write(" -")
    dcard.write(" -")                
    dcard.write(" -")        
    dcard.write(" -")        
    dcard.write("\n")  

    dcard.write("zgscale lnN -")
    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue

        if label == "zg+jets" and labels["zg+jets"]["hists"][ewdim6_index].GetBinContent(i) > 0:
            dcard.write(" "+str(zgjets_ewdim6_scale_syst.GetBinContent(i)/labels["zg+jets"]["hists"][ewdim6_index].GetBinContent(i)))
        else:    
            dcard.write(" -")

    dcard.write(" -")
    dcard.write(" -")                
    dcard.write(" -")        
    dcard.write(" -")        
    dcard.write("\n")  

    dcard.write("zgpdf lnN -")
    for label in labels.keys():
        if label == "no label" or label == "wg+jets" or label == "w+jets":
            continue

        if label == "zg+jets" and labels["zg+jets"]["hists"][ewdim6_index].GetBinContent(i) > 0:
            dcard.write(" "+str(zgjets_ewdim6_pdf_syst.GetBinContent(i)/labels["zg+jets"]["hists"][ewdim6_index].GetBinContent(i)))
        else:        
            dcard.write(" -")

    dcard.write(" -")
    dcard.write(" -")                
    dcard.write(" -")        
    dcard.write(" -")        
    dcard.write("\n")  
