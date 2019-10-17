data_driven = True
data_driven_correction = True
closure_test = False
use_wjets_mc_for_fake_photon = False

metlow = 0
methigh = 1000000

puppimetlow = 60
puppimethigh = 1000000

njets40min = 0
njets40max = 10000

def fillHistogram(hist,value,weight=1):
    if options.overflow:
       if value > hist.GetBinLowEdge(hist.GetNbinsX()):
            value = hist.GetBinCenter(hist.GetNbinsX())
    hist.Fill(value,weight)

import ctypes

import json

import sys
import style

import optparse

from math import hypot, pi, sqrt, acos, cos, sin, atan2

from pprint import pprint

from wg_fake_photon_weight import fake_photon_weight
from wg_fake_lepton_weight import fake_lepton_weight

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


parser = optparse.OptionParser()


parser.add_option('--lep',dest='lep',default='both')
parser.add_option('--year',dest='year',default='all')
parser.add_option('--phoeta',dest='phoeta',default='both')
parser.add_option('--overflow',dest='overflow',action='store_true',default=False)
parser.add_option('--ewdim6',dest='ewdim6',action='store_true',default=False)
parser.add_option('--float_fake_sig_cont',dest='float_fake_sig_cont',action='store_true',default=False)
parser.add_option('--draw_ewdim6',dest='draw_ewdim6',action='store_true',default=False)
parser.add_option('--ewdim6_scaling_only',dest='ewdim6_scaling_only',action='store_true',default=False)
parser.add_option('--make_recoil_trees',dest='make_recoil_trees',action='store_true',default=False)
parser.add_option('--make_plots',dest='make_plots',action='store_true',default=False)
parser.add_option('--blinding_cut',dest='blinding_cut',default=1000000)
parser.add_option('--variable',dest='variable')
parser.add_option('--xaxislabel',dest='xaxislabel',default='m_{jj} (GeV)')

parser.add_option('-i',dest='inputfile')
parser.add_option('-o',dest='outputdir',default="/eos/user/a/amlevin/www/tmp/")

(options,args) = parser.parse_args()

blinding_cut = float(options.blinding_cut)

if options.ewdim6_scaling_only and not options.ewdim6:
    assert(0)

if options.year == "2016":
    years = ["2016"]
    totallumi=35.9
elif options.year == "2017":
    years=["2017"]
    totallumi=41.5
elif options.year == "2018":
    years=["2018"]
    totallumi=59.6
elif options.year == "run2":
    years=["2016","2017","2018"]
    totallumi=137.1
else:
    assert(0)

sieie_cut_2016_barrel = 0.01022
sieie_cut_2016_endcap = 0.03001
sieie_cut_2017_barrel = 0.01015
sieie_cut_2017_endcap = 0.0272
sieie_cut_2018_barrel = 0.01015
sieie_cut_2018_endcap = 0.0272

if options.lep == "muon":
    lepton_name = "muon"
    lepton_abspdgids = [13]
elif options.lep == "electron":
    lepton_name = "electron"
    lepton_abspdgids = [11]
elif options.lep == "both":
    lepton_name = "both"
    lepton_abspdgids = [11,13]
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


f_json=open("/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt")
#f_json=open("delete_this_JSON.txt")

good_run_lumis=json.loads(f_json.read())

def pass_json(run,lumi):

    if str(run) not in good_run_lumis.keys():
        return False

    for lumi_pair in good_run_lumis[str(run)]:
        if lumi < lumi_pair[1] and lumi > lumi_pair[0]:
            return True

    return False    

import eff_scale_factor

import ROOT

ROOT.gROOT.cd()

if options.make_recoil_trees:

    from array import array

    recoil_outfile = ROOT.TFile("recoil.root",'recreate')

    mc_recoil_tree = ROOT.TTree("mc_recoil_tree","mc recoil tree")

    mc_u1= array( 'f', [ 0 ] )
    mc_recoil_tree.Branch( 'u1', mc_u1, 'u1/F')

    mc_u2= array( 'f', [ 0 ] )
    mc_recoil_tree.Branch( 'u2', mc_u2, 'u2/F')

    mc_zpt= array( 'f', [ 0 ] )
    mc_recoil_tree.Branch( 'zpt', mc_zpt, 'zpt/F')

    mc_weight= array( 'f', [ 0 ] )
    mc_recoil_tree.Branch( 'weight', mc_weight, 'weight/F')



ROOT.gROOT.ProcessLine("#include \"/afs/cern.ch/user/a/amlevin/recoil_corrections/MetTools/RecoilCorrections/RecoilCorrector.hh\"")

#recoilCorrector = ROOT.RecoilCorrector("/afs/cern.ch/user/a/amlevin/recoil_corrections/MetTools/RecoilCorrections/mcweightsmyptbinning/fits_pf.root","grPF")
wgrecoilCorrector = ROOT.RecoilCorrector("/afs/cern.ch/user/a/amlevin/recoil_corrections/MetTools/RecoilCorrections/wgmcweightsmyptbinning/fits_pf.root","grPF")
wgrecoilCorrector.addMCFile("/afs/cern.ch/user/a/amlevin/recoil_corrections/MetTools/RecoilCorrections/mcweightsmyptbinning/fits_pf.root")
wgrecoilCorrector.addDataFile("/afs/cern.ch/user/a/amlevin/recoil_corrections/MetTools/RecoilCorrections/datamyptbinning/fits_pf.root")
wgrecoilCorrector.addFileWithGraph("/afs/cern.ch/user/a/amlevin/recoil_corrections/MetTools/RecoilCorrections/datamyptbinning/fits_pf.root")

zgrecoilCorrector = ROOT.RecoilCorrector("/afs/cern.ch/user/a/amlevin/recoil_corrections/MetTools/RecoilCorrections/zgmcweightsmyptbinning/fits_pf.root","grPF")
zgrecoilCorrector.addMCFile("/afs/cern.ch/user/a/amlevin/recoil_corrections/MetTools/RecoilCorrections/mcweightsmyptbinning/fits_pf.root")
zgrecoilCorrector.addDataFile("/afs/cern.ch/user/a/amlevin/recoil_corrections/MetTools/RecoilCorrections/datamyptbinning/fits_pf.root")
zgrecoilCorrector.addFileWithGraph("/afs/cern.ch/user/a/amlevin/recoil_corrections/MetTools/RecoilCorrections/datamyptbinning/fits_pf.root")

#when the TMinuit object is reused, the random seed is not reset after each fit, so the fit result can change when it is run on the same input 
ROOT.TMinuitMinimizer.UseStaticMinuit(False)

if closure_test:
    from wg_labels_closuretest import labels
elif use_wjets_mc_for_fake_photon:
    from wg_labels_wjets import labels
else:
    from wg_labels import labels
#    from wg_labels_wjets import labels
#from wg_labels_recoil_tree import labels

mlg_fit_upper_bound = 400

#the first variable is for the ewdim6 analysis
#variables = ["photon_pt","dphilg","met","lepton_pt","lepton_eta","photon_pt","photon_eta","mlg","lepton_phi","photon_phi","njets40","mt","npvs","drlg"]
#variables_labels = ["ewdim6_photon_pt","dphilg","met","lepton_pt","lepton_eta","photon_pt","photon_eta","mlg","lepton_phi","photon_phi","njets40","mt","npvs","drlg"]

variables = ["photon_pt","detalg","dphilmet","dphilg","puppimet","lepton_pt","lepton_eta","photon_pt","photon_eta","mlg","mlg","lepton_phi","photon_phi","njets40","mt","npvs","drlg","photon_pt","met","corrmet","corrdphilmet","corrmt","photon_recoil"]
variables_labels = ["ewdim6_photon_pt","detalg","dphilmet","dphilg","puppimet","lepton_pt","lepton_eta","photon_pt","photon_eta","fit_mlg","mlg","lepton_phi","photon_phi","njets40","mt","npvs","drlg","photon_pt_20to180","met","corrmet","corrdphilmet","corrmt","photon_recoil"]

assert(len(variables) == len(variables_labels))

from array import array

binning_photon_pt = array('f',[400,500,600,900,1500])
#binning_photon_pt = array('f',[300,500,750,1000,1500])
#binning_photon_pt = array('f',[100,200,300,400,500,600])

n_photon_pt_bins = len(binning_photon_pt)-1

histogram_templates = [ROOT.TH1D('', '', n_photon_pt_bins, binning_photon_pt ),ROOT.TH1D('','',16,0,6),ROOT.TH1D('','',16,0,pi),ROOT.TH1D('','',16,0,pi), ROOT.TH1D("met", "", 15 , 0., 300 ), ROOT.TH1D('lepton_pt', '', 8, 20., 180 ), ROOT.TH1D('lepton_eta', '', 10, -2.5, 2.5 ), ROOT.TH1D('photon_pt', '', n_photon_pt_bins, binning_photon_pt ), ROOT.TH1D('photon_eta', '', 10, -2.5, 2.5 ), ROOT.TH1D("mlg","",mlg_fit_upper_bound/2,0,mlg_fit_upper_bound), ROOT.TH1D("mlg","",100,0,200),ROOT.TH1D("lepton_phi","",14,-3.5,3.5), ROOT.TH1D("photon_phi","",14,-3.5,3.5), ROOT.TH1D("njets40","",7,-0.5,6.5), ROOT.TH1D("mt","",10,0,200), ROOT.TH1D("npvs","",51,-0.5,50.5), ROOT.TH1D("drlg","",16,0,5), ROOT.TH1D('photon_pt', '', 8, 20., 180 ),ROOT.TH1D("met", "", 15 , 0., 300 ),ROOT.TH1D("corrmet", "", 15 , 0., 300 ),ROOT.TH1D('','',16,0,pi),ROOT.TH1D("corr mt","",10,0,200),ROOT.TH1D('photon_recoil', '', 20, -70., 130 )] 

assert(len(variables) == len(histogram_templates))

mlg_index = 9

#ewdim6_filename = "/afs/cern.ch/work/a/amlevin/data/wg/2016/wgjetsewdim6.root.bak"
ewdim6_filename = "/afs/cern.ch/work/a/amlevin/data/wg/2016/wgjetsewdim6.root"

ewdim6_file = ROOT.TFile(ewdim6_filename)

ewdim6_tree = ewdim6_file.Get("Events")

#ewdim6_xs = 5.519
ewdim6_xs = 4.318

#ewdim6_nweightedevents = ewdim6_file.Get("nEventsGenWeighted").GetBinContent(1)
ewdim6_nweightedevents = ewdim6_file.Get("nWeightedEvents").GetBinContent(1)

def getVariable(varname, tree, corrmet = None, corrmetphi = None):
    if varname == "mlg":
        return tree.mlg
    elif varname == "detalg":
        return abs(tree.lepton_eta-tree.photon_eta)
    elif varname == "drlg":
        return deltaR(tree.lepton_eta,tree.lepton_phi,tree.photon_eta,tree.photon_phi)
    elif varname == "dphilmet":
        return acos(max(min(-(pow(tree.mt,2)/2/tree.lepton_pt/tree.met-1),1),-1))
    elif varname == "dphilg":
        return abs(deltaPhi(tree.lepton_phi,tree.photon_phi))
    elif varname == "mt":
        return tree.puppimt
    elif varname == "corrmt":
        if corrmet and corrmetphi:
            return sqrt(2*tree.lepton_pt*corrmet*(1 - cos(corrmetphi - tree.lepton_phi)))
        else:
            return tree.mt
    elif varname == "njets40":
        return float(tree.njets40)
    elif varname == "npvs":
        return float(tree.npvs)
    elif varname == "puppimet":
        return tree.puppimet
    elif varname == "met":
        return tree.met
    elif varname == "corrmet":
        if corrmet:
            return corrmet
        else:
            return tree.met
    elif varname == "corrdphilmet":
        if corrmetphi:
            return abs(deltaPhi(corrmetphi,tree.lepton_phi))
        else:
            return acos(max(min(-(pow(tree.mt,2)/2/tree.lepton_pt/tree.met-1),1),-1))
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
    elif varname == "photon_recoil":
#        if hasattr(tree,"gen_neutrinos_pt"):
        if False:
#            return cos(tree.photon_phi)*(-tree.lepton_pt*cos(tree.lepton_phi)-tree.gen_neutrinos_pt*cos(tree.gen_neutrinos_phi)) + sin(tree.photon_phi)*(-tree.lepton_pt*sin(tree.lepton_phi) -tree.gen_neutrinos_pt*sin(tree.gen_neutrinos_phi))
            return cos(tree.photon_phi)*(-tree.gen_leptons_pt*cos(tree.gen_leptons_phi)-tree.gen_neutrinos_pt*cos(tree.gen_neutrinos_phi)) + sin(tree.photon_phi)*(-tree.gen_leptons_pt*sin(tree.gen_leptons_phi) -tree.gen_neutrinos_pt*sin(tree.gen_neutrinos_phi))
#            return cos(tree.photon_phi)*(-tree.gen_leptons_pt*cos(tree.gen_leptons_phi)-tree.puppimet*cos(tree.puppimetphi)) + sin(tree.photon_phi)*(-tree.gen_leptons_pt*sin(tree.gen_leptons_phi) -tree.puppimet*sin(tree.puppimetphi))
        else:
            return cos(tree.photon_phi)*(-tree.lepton_pt*cos(tree.lepton_phi)-tree.puppimet*cos(tree.puppimetphi)) + sin(tree.photon_phi)*(-tree.lepton_pt*sin(tree.lepton_phi) -tree.puppimet*sin(tree.puppimetphi))
#            return cos(tree.photon_phi)*(-tree.lepton_pt*cos(tree.lepton_phi)-tree.met*cos(tree.metphi)) + sin(tree.photon_phi)*(-tree.lepton_pt*sin(tree.lepton_phi) -tree.met*sin(tree.metphi))
    else:
        assert(0)

def getXaxisLabel(varname):
    if varname == "njets40":
        return "number of jets"
    elif varname == "detalg":
        return "#Delta #eta(l,g)"
    elif varname == "dphilmet":
        return "#Delta #phi(l,MET)"
    elif varname == "corrdphilmet":
        return "corrected #Delta #phi(l,MET)"
    elif varname == "drlg":
        return "#Delta R(l,g)"
    elif varname == "dphilg":
        return "#Delta #phi(l,g)"
    elif varname == "npvs":
        return "number of PVs"
    elif varname == "mt":
        return "m_{t} (GeV)"
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
    elif varname == "photon_eta":
        return "photon #eta"    
    elif varname == "photon_phi":
        return "photon #phi"
    elif varname == "photon_recoil":
        return "photon recoil (GeV)"

    else:
        assert(0)

def pass_selection(tree, year, barrel_or_endcap_or_both = "both", fake_lepton = False , fake_photon = False):

    assert(year == "2016" or year == "2017" or year == "2018")

    if year == "2016":
        sieie_cut_barrel = sieie_cut_2016_barrel
        sieie_cut_endcap = sieie_cut_2016_endcap
    elif year == "2017":
        sieie_cut_barrel = sieie_cut_2017_barrel
        sieie_cut_endcap = sieie_cut_2017_endcap
    elif year == "2018":
        sieie_cut_barrel = sieie_cut_2017_barrel
        sieie_cut_endcap = sieie_cut_2017_endcap
    else:
        assert(0)

    fake_photon_sieie_cut_barrel = sieie_cut_barrel*1.75
    fake_photon_sieie_cut_endcap = sieie_cut_endcap*1.75

    if barrel_or_endcap_or_both == "both":
        pass_photon_eta = True    
    elif barrel_or_endcap_or_both == "barrel":        
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


    if lepton_name == "electron":
        if tree.lepton_pdg_id == 11:
            pass_lepton_flavor = True
        else:
            pass_lepton_flavor = False
    elif lepton_name == "muon":
        if tree.lepton_pdg_id == 13:
            pass_lepton_flavor = True
        else:
            pass_lepton_flavor = False
    elif lepton_name == "both":
        assert(tree.lepton_pdg_id == 11 or tree.lepton_pdg_id == 13)
        pass_lepton_flavor = True
    else:
        assert(0)

        
#    if tree.npvs < 20:
#        pass_lepton_flavor = False
        
#    if not (tree.mlg > 61.2 and tree.mlg < 101.2):
#    if (tree.mlg > 61.2 and tree.mlg < 101.2):
#    if not (tree.mlg > 71.2 and tree.mlg < 111.2):
#    if (tree.mlg > 80.0 and tree.mlg < 100.0):

#    if True:    


    if (lepton_name == "electron") or (lepton_name == "both" and abs(tree.lepton_pdg_id) == 11):    
        if not (tree.mlg > 60.0 and tree.mlg < 120.0):
#        if True:
            pass_mlg = True
        else:
            pass_mlg = False
    elif lepton_name == "muon":        
#        if not (tree.mlg > 60.0 and tree.mlg < 100.0):
#        if tree.mlg > 80.0 and tree.mlg < 90.0:
        if True:
            pass_mlg = True
        else:
            pass_mlg = False
    elif lepton_name == "both":
        if True:
            pass_mlg = True
        else:
            pass_mlg = False
    else:
        assert(0)

#    if lepton_abs_pdg_id == 11:    
#        if True:
#        if (tree.mlg > 81.2 and tree.mlg < 101.2):
#        if not (tree.mlg > 76.2 and tree.mlg < 106.2):
#        if (tree.mlg > 61.2 and tree.mlg < 121.2):
#            pass_mlg = True
#        else:
#            pass_mlg = False
#    else:
#        pass_mlg = True



#    if "corrMet" in vars():
    if False:
        met = float(corrMet)
    else:
        met = tree.met
#    if tree.met > 35:
#    if tree.met > 70 :
#    if tree.puppimet > 60:
    if met > 0:
        pass_met = True
    else:
        pass_met = False

    if tree.mt > 0:
#    if tree.mt > 30:
#    if tree.mt > 0:
        pass_mt = True
    else:
        pass_mt = False

#    if deltaR(tree.lepton_eta,tree.lepton_phi,tree.photon_eta,tree.photon_phi) > 0.5 and deltaPhi(tree.lepton_phi,tree.photon_phi) < 1.4 and acoxs(max(min(-(pow(tree.mt,2)/2/tree.lepton_pt/tree.met-1),1),-1)) > 2:
#    if deltaR(tree.lepton_eta,tree.lepton_phi,tree.photon_eta,tree.photon_phi) > 0.5 and acos(max(min(-(pow(tree.mt,2)/2/tree.lepton_pt/tree.met-1),1),-1)) > 2:
#    if deltaR(tree.lepton_eta,tree.lepton_phi,tree.photon_eta,tree.photon_phi) > 0.5 and tree.njets40 > 0:
#######    if deltaR(tree.lepton_eta,tree.lepton_phi,tree.photon_eta,tree.photon_phi) > 0.5 and deltaPhi(tree.lepton_phi,tree.photon_phi) > pi - pi/16 and tree.njets40 == 0 and tree.mlg < 100:
#    if deltaR(tree.lepton_eta,tree.lepton_phi,tree.photon_eta,tree.photon_phi) > 0.5 and (tree.mlg > 100 or tree.mlg < 60) and tree.njets40 == 0 and deltaPhi(tree.lepton_phi,tree.photon_phi) > pi - 6*pi/16 and tree.photon_pt < 120:
#    if deltaR(tree.lepton_eta,tree.lepton_phi,tree.photon_eta,tree.photon_phi) > 0.5 and tree.photon_pt > 120:
#    if deltaR(tree.lepton_eta,tree.lepton_phi,tree.photon_eta,tree.photon_phi) > 0.5 and tree.mlg < 100 and tree.photon_pt > 120:
#    if deltaR(tree.lepton_eta,tree.lepton_phi,tree.photon_eta,tree.photon_phi) > 0.5 and tree.njets40 == 0:
#    if deltaR(tree.lepton_eta,tree.lepton_phi,tree.photon_eta,tree.photon_phi) > 0.5 and deltaPhi(tree.lepton_phi,tree.photon_phi) > pi - 6*pi/16 and tree.njets40 == 0 and tree.mlg < 100:
#    if deltaR(tree.lepton_eta,tree.lepton_phi,tree.photon_eta,tree.photon_phi) > 0.5 and tree.njets40 == 0 and tree.mlg < 100:
    if deltaR(tree.lepton_eta,tree.lepton_phi,tree.photon_eta,tree.photon_phi) > 0.5 and tree.njets40 >= njets40min and tree.njets40 <= njets40max:
        pass_drlg = True
    else:
        pass_drlg = False

    if fake_photon:    
        if abs(tree.photon_eta) < 1.5:
            fake_photon_sieie_cut = fake_photon_sieie_cut_barrel
        else:    
            fake_photon_sieie_cut = fake_photon_sieie_cut_endcap
        if tree.photon_selection == 4 and tree.photon_sieie < fake_photon_sieie_cut:
            pass_photon_selection = True
        else:
            pass_photon_selection = False
    else:    
        if tree.photon_selection == 0:
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
            
#    if tree.photon_pt < 30 and tree.lepton_pt > 35:
#    if tree.photon_pt < 25 and tree.lepton_pt > 35:
#    if tree.photon_pt > 20 and tree.photon_pt < 30 and tree.lepton_pt > 25 and getVariable("dphilg",tree) < 1*pi/16 and getVariable("dphilg",tree) > 0*pi/16:
#    if tree.photon_pt > 25 and tree.lepton_pt > 30 and tree.photon_pt < 50:
    if tree.photon_pt > 30 and tree.photon_pt < 1000000 and ((tree.lepton_pt > 30 && (year == "2016" or abs(tree.lepton_pdg_id) == 13))) or (tree.lepton_pt > 35 and ((year == "2017" or year == "2018") and abs(tree.lepton_pdg_id) == 11)): 
        pass_photon_pt =True
    else:
        pass_photon_pt = False

    if pass_drlg and pass_photon_pt and pass_lepton_selection and pass_photon_selection and pass_mlg and pass_photon_eta and pass_lepton_flavor and pass_met and pass_mt:
        return True
    else:
        return False

#def fillHistograms(tree,hists):

xoffsetstart = 0.0;
yoffsetstart = 0.0;
xoffset = 0.20;
yoffset = 0.05;

xpositions = [0.68,0.68,0.68,0.68,0.445,0.445,0.445,0.445,0.21,0.21,0.21,0.21]
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

    labels[label]["hists-electron-id-sf-variation"] = {}
    labels[label]["hists-electron-reco-sf-variation"] = {}
    labels[label]["hists-muon-id-sf-variation"] = {}
    labels[label]["hists-muon-iso-sf-variation"] = {}
    labels[label]["hists-photon-id-sf-variation"] = {}
    labels[label]["hists-pileup-up"] = {}

    if labels[label]["syst-pdf"]:
        for i in range(0,102):
            labels[label]["hists-pdf-variation"+str(i)] = {}

    if labels[label]["syst-scale"]:
        for i in range(0,8):
            labels[label]["hists-scale-variation"+str(i)] = {}

    for i in range(len(variables)):    
        if labels[label]["color"] == None:
            continue

        labels[label]["hists"][i] = histogram_templates[i].Clone(label + " " + variables[i])
        labels[label]["hists"][i].Sumw2()

        labels[label]["hists-pileup-up"][i] = histogram_templates[i].Clone(label + " " + variables[i])
        labels[label]["hists-electron-id-sf-variation"][i] = histogram_templates[i].Clone(label + " " + variables[i])
        labels[label]["hists-electron-reco-sf-variation"][i] = histogram_templates[i].Clone(label + " " + variables[i])
        labels[label]["hists-muon-id-sf-variation"][i] = histogram_templates[i].Clone(label + " " + variables[i])
        labels[label]["hists-muon-iso-sf-variation"][i] = histogram_templates[i].Clone(label + " " + variables[i])
        labels[label]["hists-photon-id-sf-variation"][i] = histogram_templates[i].Clone(label + " " + variables[i])
        labels[label]["hists-electron-id-sf-variation"][i].Sumw2()
        labels[label]["hists-electron-reco-sf-variation"][i].Sumw2()
        labels[label]["hists-muon-id-sf-variation"][i].Sumw2()
        labels[label]["hists-muon-iso-sf-variation"][i].Sumw2()
        labels[label]["hists-photon-id-sf-variation"][i].Sumw2()

        if labels[label]["syst-pdf"]:
            for j in range(0,102):
                labels[label]["hists-pdf-variation"+str(j)][i] = histogram_templates[i].Clone(label + " " + variables[i])
                labels[label]["hists-pdf-variation"+str(j)][i].Sumw2()

        if labels[label]["syst-scale"]:
            for j in range(0,8):
                labels[label]["hists-scale-variation"+str(j)][i] = histogram_templates[i].Clone(label + " " + variables[i])
                labels[label]["hists-scale-variation"+str(j)][i].Sumw2()
            
    for year in years:            
        for sample in labels[label]["samples"][year]:
            sample["file"] = ROOT.TFile.Open(sample["filename"])
            sample["tree"] = sample["file"].Get("Events")
            sample["nweightedevents"] = sample["file"].Get("nEventsGenWeighted").GetBinContent(1)


if "wg+jets" in labels:
    if labels["wg+jets"]["syst-scale"]:
        for i in range(0,8):
            labels["wg+jets"]["samples"][year][0]["nweightedevents_qcdscaleweight"+str(i)]=labels["wg+jets"]["samples"][year][0]["file"].Get("nWeightedEvents_QCDScaleWeight"+str(i)).GetBinContent(1)

            if labels["wg+jets"]["samples"][year][0]["filename"] == "/afs/cern.ch/work/a/amlevin/data/wg/2016/wgjets.root":
                labels["wg+jets"]["samples"][year][0]["nweightedevents_qcdscaleweight"+str(i)] *= 2

    if labels["wg+jets"]["syst-pdf"]:
        for i in range(1,102):
            labels["wg+jets"]["samples"][year][0]["nweightedevents_pdfweight"+str(i)]=labels["wg+jets"]["samples"][year][0]["file"].Get("nWeightedEvents_PDFWeight"+str(i)).GetBinContent(1)

#labels["wg+jets"]["samples"][0]["nweightedeventspassgenselection"]=labels["wg+jets"]["samples"][0]["file"].Get("nWeightedEventsPassGenSelection").GetBinContent(1)
    labels["wg+jets"]["samples"][year][0]["nweightedeventspassgenselection"]=1

    fiducial_region_cuts_efficiency = float(labels["wg+jets"]["samples"][year][0]["nweightedeventspassgenselection"])/float(labels["wg+jets"]["samples"][year][0]["nweightedevents"])

data = {}
fake_signal_contamination = {}
fake_photon = {}
fake_photon_alt = {}
fake_photon_stat_up = {}
fake_lepton = {}
fake_lepton_stat_down = {}
fake_lepton_stat_up = {}
double_fake = {}
e_to_p = {}
e_to_p_non_res = {}
ewdim6 = {}

data["hists"] = []
fake_signal_contamination["hists"] = []
fake_photon["hists"] = []
fake_photon_alt["hists"] = []
fake_photon_stat_up["hists"] = []
fake_lepton["hists"] = []
fake_lepton_stat_down["hists"] = []
fake_lepton_stat_up["hists"] = []
double_fake["hists"] = []
e_to_p_non_res["hists"] = []
e_to_p["hists"] = []
ewdim6["hists"] = []

for i in range(len(variables)):
    data["hists"].append(histogram_templates[i].Clone("data " + variables[i]))
    fake_signal_contamination["hists"].append(histogram_templates[i].Clone("fake signal " + variables[i]))
    fake_photon["hists"].append(histogram_templates[i].Clone("fake photon " + variables[i]))
    fake_photon_stat_up["hists"].append(histogram_templates[i].Clone("fake photon stat up" + variables[i]))
    fake_photon_alt["hists"].append(histogram_templates[i].Clone("fake photon sys " + variables[i]))
    fake_lepton["hists"].append(histogram_templates[i].Clone("fake lepton " + variables[i]))
    fake_lepton_stat_up["hists"].append(histogram_templates[i].Clone("fake lepton stat up" + variables[i]))
    fake_lepton_stat_down["hists"].append(histogram_templates[i].Clone("fake lepton stat down" + variables[i]))
    double_fake["hists"].append(histogram_templates[i].Clone("double fake " + variables[i]))
    e_to_p_non_res["hists"].append(histogram_templates[i].Clone("electron to photon " + variables[i]))
    e_to_p["hists"].append(histogram_templates[i].Clone("electron to photon " + variables[i]))
    ewdim6["hists"].append(histogram_templates[i].Clone("ewdim6 " + variables[i]))

for i in range(len(variables)):
    data["hists"][i].Sumw2()
    fake_signal_contamination["hists"][i].Sumw2()
    fake_photon["hists"][i].Sumw2()
    fake_photon_stat_up["hists"][i].Sumw2()
    fake_photon_alt["hists"][i].Sumw2()
    fake_lepton["hists"][i].Sumw2()
    fake_lepton_stat_up["hists"][i].Sumw2()
    fake_lepton_stat_down["hists"][i].Sumw2()
    double_fake["hists"][i].Sumw2()
    e_to_p_non_res["hists"][i].Sumw2()
    e_to_p["hists"][i].Sumw2()
    ewdim6["hists"][i].Sumw2()

c1 = ROOT.TCanvas("c1", "c1",5,50,500,500);

ROOT.gROOT.cd()

def fillHistogramMC(label,sample,labelname,year):

    if year == "2016":
        lumi=35.9
    elif year == "2017":
        lumi=41.5
    elif year == "2018":
        lumi=59.6
    else:
        assert(0)

    print "Running over sample " + str(sample["filename"])
    print "sample[\"tree\"].GetEntries() = " + str(sample["tree"].GetEntries())

    for i in range(sample["tree"].GetEntries()):

        if i > 0 and i % 100000 == 0:
#        if i > 0 and i % 100 == 0:
            print "Processed " + str(i) + " out of " + str(sample["tree"].GetEntries()) + " events"

        sample["tree"].GetEntry(i)

#        if (sample["tree"].met < 70 and "wgjets" not in sample["filename"]) or ("wgjets"  in sample["filename"] and  sample["tree"].metup < 70) or sample["tree"].mt < 30:
        if sample["tree"].puppimet < puppimetlow or sample["tree"].puppimet > puppimethigh or sample["tree"].met < metlow or sample["tree"].met > methigh or abs(sample["tree"].lepton_pdg_id) not in lepton_abspdgids or abs(sample["tree"].photon_eta) < photon_eta_min or abs(sample["tree"].photon_eta) > photon_eta_max:
#        if corrMet < 60 or sample["tree"].mt < 0:
#        if sample["tree"].puppimet < 60 or sample["tree"].puppimt < 30:
            continue

        if hasattr(sample["tree"],"gen_leptons_phi"):
#        if False:

            corrMet = ROOT.Double(sample["tree"].met)
            corrMetPhi = ROOT.Double(sample["tree"].metphi)
            genVPt = ROOT.Double(sqrt(pow(sample["tree"].gen_photons_pt*cos(sample["tree"].gen_photons_phi) + sample["tree"].gen_leptons_pt*cos(sample["tree"].gen_leptons_phi) + sample["tree"].gen_neutrinos_pt*cos(sample["tree"].gen_neutrinos_phi),2) + pow(sample["tree"].gen_photons_pt*sin(sample["tree"].gen_photons_phi) + sample["tree"].gen_leptons_pt*sin(sample["tree"].gen_leptons_phi) + sample["tree"].gen_neutrinos_pt*sin(sample["tree"].gen_neutrinos_phi),2)))
            genVPhi = ROOT.Double(atan2(sample["tree"].gen_photons_pt*sin(sample["tree"].gen_photons_phi) + sample["tree"].gen_leptons_pt*sin(sample["tree"].gen_leptons_phi) + sample["tree"].gen_neutrinos_pt*sin(sample["tree"].gen_neutrinos_phi),sample["tree"].gen_photons_pt*cos(sample["tree"].gen_photons_phi) + sample["tree"].gen_leptons_pt*cos(sample["tree"].gen_leptons_phi) + sample["tree"].gen_neutrinos_pt*cos(sample["tree"].gen_neutrinos_phi)))
            #        dileptonPt = ROOT.Double(sqrt(pow(sample["tree"].gen_photons_pt*cos(sample["tree"].gen_photons_phi) + sample["tree"].gen_leptons_pt*cos(sample["tree"].gen_leptons_phi)+sample["tree"].gen_neutrinos_pt*cos(sample["tree"].gen_neutrinos_phi),2) + pow(sample["tree"].gen_photons_pt*sin(sample["tree"].gen_photons_phi) + sample["tree"].gen_leptons_pt*sin(sample["tree"].gen_leptons_phi) + sample["tree"].gen_neutrinos_pt*sin(sample["tree"].gen_neutrinos_phi),2))) 
            #        dileptonPhi = ROOT.Double(atan2(sample["tree"].gen_photons_pt*sin(sample["tree"].gen_photons_phi) + sample["tree"].gen_leptons_pt*sin(sample["tree"].gen_leptons_phi) + sample["tree"].gen_neutrinos_pt*sin(sample["tree"].gen_neutrinos_phi),sample["tree"].gen_photons_pt*cos(sample["tree"].gen_photons_phi) + sample["tree"].gen_leptons_pt*cos(sample["tree"].gen_leptons_phi) + sample["tree"].gen_neutrinos_pt*cos(sample["tree"].gen_neutrinos_phi))) 

            pu1= ROOT.Double()
            pu2= ROOT.Double()

            if sample["tree"].n_gen_neutrinos > 0:
#                dileptonPt = ROOT.Double(sqrt(pow(sample["tree"].gen_photons_pt*cos(sample["tree"].gen_photons_phi) + sample["tree"].gen_leptons_pt*cos(sample["tree"].gen_leptons_phi),2) + pow(sample["tree"].gen_photons_pt*sin(sample["tree"].gen_photons_phi) + sample["tree"].gen_leptons_pt*sin(sample["tree"].gen_leptons_phi),2))) 
#                dileptonPhi = ROOT.Double(atan2(sample["tree"].gen_photons_pt*sin(sample["tree"].gen_photons_phi) + sample["tree"].gen_leptons_pt*sin(sample["tree"].gen_leptons_phi),sample["tree"].gen_photons_pt*cos(sample["tree"].gen_photons_phi) + sample["tree"].gen_leptons_pt*cos(sample["tree"].gen_leptons_phi))) 
#                wgrecoilCorrector.CorrectType2FromGraph(corrMet,corrMetPhi,genVPt,genVPhi,dileptonPt,dileptonPhi,pu1,pu2,0)
                pass
            else:    
#                dileptonPt = ROOT.Double(sqrt(pow(sample["tree"].gen_photons_pt*cos(sample["tree"].gen_photons_phi) + sample["tree"].gen_leptons_pt*cos(sample["tree"].gen_leptons_phi) + sample["tree"].gen_neutrinos_pt*cos(sample["tree"].gen_neutrinos_phi),2) + pow(sample["tree"].gen_photons_pt*sin(sample["tree"].gen_photons_phi) + sample["tree"].gen_leptons_pt*sin(sample["tree"].gen_leptons_phi) + sample["tree"].gen_neutrinos_pt*sin(sample["tree"].gen_neutrinos_phi),2)))
#                dileptonPhi = ROOT.Double(atan2(sample["tree"].gen_photons_pt*sin(sample["tree"].gen_photons_phi) + sample["tree"].gen_leptons_pt*sin(sample["tree"].gen_leptons_phi) + sample["tree"].gen_neutrinos_pt*sin(sample["tree"].gen_neutrinos_phi),sample["tree"].gen_photons_pt*cos(sample["tree"].gen_photons_phi) + sample["tree"].gen_leptons_pt*cos(sample["tree"].gen_leptons_phi) + sample["tree"].gen_neutrinos_pt*cos(sample["tree"].gen_neutrinos_phi)))
#                zgrecoilCorrector.CorrectType2FromGraph(corrMet,corrMetPhi,genVPt,genVPhi,dileptonPt,dileptonPhi,pu1,pu2,0)
#                zgrecoilCorrector.CorrectType0(corrMet,corrMetPhi,genVPt,genVPhi,dileptonPt,dileptonPhi,pu1,pu2,0)
                pass

#            recoilCorrector.CorrectType0(corrMet,corrMetPhi,genVPt,genVPhi,dileptonPt,dileptonPhi,pu1,pu2,0)
            corrMet = float(corrMet)
            corrMetPhi = float(corrMetPhi) 
        else:
            corrMet = sample["tree"].met
            corrMetPhi = None
#        corrMet = sqrt(pow(tree.met*cos(tree.metphi) - tree.gen_neutrinos_pt*cos(tree.gen_neutrinos_phi),2) + pow(tree.met*sin(tree.metphi) - tree.gen_neutrinos_pt*sin(tree.gen_neutrinos_phi),2))

#        corrMet = tree.gen_neutrinos_pt

            


        if sample["tree"].is_lepton_real == '\x01':
            pass_is_lepton_real = True
        else:
            pass_is_lepton_real = False

#        if ((sample["tree"].photon_gen_matching == 1) and sample["e_to_p"]) or ((sample["tree"].photon_gen_matching ==4) and sample["fsr"]) or ((sample["tree"].photon_gen_matching == 5) and sample["non_fsr"]) :
#        if ((sample["tree"].photon_gen_matching == 1) and sample["e_to_p"]) or ((sample["tree"].photon_gen_matching ==4) and sample["fsr"]) or ((sample["tree"].photon_gen_matching == 5) and sample["non_fsr"]) or ((sample["tree"].photon_gen_matching == 6) and sample["non_fsr"] and sample["filename"] == "/afs/cern.ch/work/a/amlevin/data/wg/2016/wgjets.root"):
        if ((sample["tree"].photon_gen_matching == 1) and sample["e_to_p"])  or (sample["tree"].photon_gen_matching ==4 and sample["fsr"]) or (sample["tree"].photon_gen_matching == 6 and sample["non_fsr"]):
#        if True:    
#        if (bool(sample["tree"].photon_gen_matching_old & int('010',2)) and sample["e_to_p"]) or (bool(sample["tree"].photon_gen_matching_old & int('1000',2)) and sample["fsr"]) or (bool(sample["tree"].photon_gen_matching_old & int('0100',2)) and sample["non_fsr"]) :
            pass_photon_gen_matching = True
        else:
            pass_photon_gen_matching = False    

        if ((sample["tree"].photon_gen_matching == 1) and sample["e_to_p_for_fake"])  or (sample["tree"].photon_gen_matching ==4 and sample["fsr"]) or (sample["tree"].photon_gen_matching == 6 and sample["non_fsr"]):
#        if True:    
#        if ((sample["tree"].photon_gen_matching == 1) and sample["e_to_p_for_fake"]) or ((sample["tree"].photon_gen_matching ==4) and sample["fsr"]) or ((sample["tree"].photon_gen_matching == 5) and sample["non_fsr"]) :
#        if (bool(sample["tree"].photon_gen_matching_old & int('010',2)) and sample["e_to_p_for_fake"]) or (bool(sample["tree"].photon_gen_matching_old & int('1000',2)) and sample["fsr"]) or (bool(sample["tree"].photon_gen_matching_old & int('0100',2)) and sample["non_fsr"]) :
            pass_photon_gen_matching_for_fake = True
        else:
            pass_photon_gen_matching_for_fake = False    

        weight = sample["xs"] * 1000 * lumi / sample["nweightedevents"]
        
        if year == "2016" or year == "2017":
            weight *= sample["tree"].PrefireWeight

#        if sample["filename"] == "/afs/cern.ch/work/a/amlevin/data/wg/2016/wgjetsewdim6.root":
#            weight *= sample["tree"].LHEWeight_rwgt_373

#        if hasattr(sample["tree"],"gen_leptons_phi") and genVPt > 5 and sample["tree"].n_gen_neutrinos == 0:
#            weight *= 0

        if sample["tree"].gen_weight < 0:
            weight = - weight

        weight_pu_up = weight
        weight_double_fake = weight
        weight_fake_lepton = weight
        weight_fake_photon = weight
        weight_fake_lepton_stat_up = weight
        weight_fake_lepton_stat_down = weight
        weight_fake_photon_alt = weight
        weight_fake_photon_stat_up = weight 
        weight_photon_id_sf_variation = weight
        weight_electron_id_sf_variation = weight
        weight_electron_reco_sf_variation = weight
        weight_muon_id_sf_variation = weight 
        weight_muon_iso_sf_variation = weight

        weight *= sample["tree"].puWeight    
        weight_pu_up *= sample["tree"].puWeightUp    
        weight_double_fake *= sample["tree"].puWeight    
        weight_fake_lepton *= sample["tree"].puWeight    
        weight_fake_photon *= sample["tree"].puWeight    
        weight_fake_lepton_stat_up *= sample["tree"].puWeight    
        weight_fake_lepton_stat_down *= sample["tree"].puWeight    
        weight_fake_photon_alt *= sample["tree"].puWeight    
        weight_fake_photon_stat_up *= sample["tree"].puWeight    
        weight_photon_id_sf_variation *= sample["tree"].puWeight    
        weight_electron_id_sf_variation *= sample["tree"].puWeight    
        weight_electron_reco_sf_variation *= sample["tree"].puWeight    
        weight_muon_id_sf_variation *= sample["tree"].puWeight    
        weight_muon_iso_sf_variation *= sample["tree"].puWeight    

        if pass_photon_gen_matching_for_fake and pass_is_lepton_real:
            if pass_selection(sample["tree"],year,options.phoeta,True,False):

                weight_fake_lepton *= -fake_lepton_weight(sample["tree"].lepton_pdg_id,sample["tree"].lepton_eta, sample["tree"].lepton_pt, year, "nominal")
                weight_fake_lepton_stat_up *= -fake_lepton_weight(sample["tree"].lepton_pdg_id,sample["tree"].lepton_eta, sample["tree"].lepton_pt, year, "up")
                weight_fake_lepton_stat_down *= -fake_lepton_weight(sample["tree"].lepton_pdg_id,sample["tree"].lepton_eta, sample["tree"].lepton_pt,year, "down")

                if labelname == "w+jets" and use_wjets_mc_for_fake_photon: 
                    weight_fake_lepton = 0
                    weight_fake_lepton_stat_up = 0
                    weight_fake_lepton_stat_down = 0

                if not data_driven_correction:
                    weight_fake_lepton = 0
                    weight_fake_lepton_stat_up = 0
                    weight_fake_lepton_stat_down = 0

                for j in range(len(variables)):
                    if sample["filename"] == "/afs/cern.ch/work/a/amlevin/data/wg/2016/wgjets.root" and options.float_fake_sig_cont:
                        fillHistogram(fake_signal_contamination["hists"][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight_fake_lepton)
                        pass
                    else:    
                        fillHistogram(fake_lepton["hists"][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight_fake_lepton)
                        fillHistogram(fake_lepton_stat_up["hists"][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight_fake_lepton_stat_up)
                        fillHistogram(fake_lepton_stat_down["hists"][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight_fake_lepton_stat_down)
                        pass

            if pass_selection(sample["tree"],year,options.phoeta,False,True):

                weight_fake_photon *= -fake_photon_weight(sample["tree"].photon_eta, sample["tree"].photon_pt,year,getVariable("photon_recoil",sample["tree"]),sample["tree"].lepton_pdg_id)
                weight_fake_photon_alt *= -fake_photon_weight(sample["tree"].photon_eta, sample["tree"].photon_pt,year,getVariable("photon_recoil",sample["tree"]),sample["tree"].lepton_pdg_id, True)
                weight_fake_photon_stat_up *= -fake_photon_weight(sample["tree"].photon_eta, sample["tree"].photon_pt,year,getVariable("photon_recoil",sample["tree"]),sample["tree"].lepton_pdg_id, False,True)

                if not data_driven_correction:
                    weight_fake_photon = 0
                    weight_fake_photon_alt = 0
                    weight_fake_photon_stat_up = 0

                for j in range(len(variables)):
                    if sample["filename"] == "/afs/cern.ch/work/a/amlevin/data/wg/2016/wgjets.root" and options.float_fake_sig_cont:
                        fillHistogram(fake_signal_contamination["hists"][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight_fake_photon)
                    else:
                        fillHistogram(fake_photon["hists"][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight_fake_photon)
                        fillHistogram(fake_photon_alt["hists"][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight_fake_photon_alt)
                        fillHistogram(fake_photon_stat_up["hists"][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight_fake_photon_stat_up)

        if not pass_selection(sample["tree"],year,options.phoeta,False,False):
            continue

        weight_photon_id_sf_variation *= eff_scale_factor.photon_efficiency_scale_factor(sample["tree"].photon_pt,sample["tree"].photon_eta,year,True)
        weight *= eff_scale_factor.photon_efficiency_scale_factor(sample["tree"].photon_pt,sample["tree"].photon_eta,year)
        weight_pu_up *= eff_scale_factor.photon_efficiency_scale_factor(sample["tree"].photon_pt,sample["tree"].photon_eta,year)
        weight_electron_id_sf_variation *= eff_scale_factor.photon_efficiency_scale_factor(sample["tree"].photon_pt,sample["tree"].photon_eta,year)
        weight_electron_reco_sf_variation *= eff_scale_factor.photon_efficiency_scale_factor(sample["tree"].photon_pt,sample["tree"].photon_eta,year)
        weight_muon_id_sf_variation *= eff_scale_factor.photon_efficiency_scale_factor(sample["tree"].photon_pt,sample["tree"].photon_eta,year)
        weight_muon_iso_sf_variation *= eff_scale_factor.photon_efficiency_scale_factor(sample["tree"].photon_pt,sample["tree"].photon_eta,year)

        if sample["tree"].lepton_pdg_id == 11:
            weight *= eff_scale_factor.electron_efficiency_scale_factor(sample["tree"].lepton_pt,sample["tree"].lepton_eta,year)
            weight_pu_up *= eff_scale_factor.electron_efficiency_scale_factor(sample["tree"].lepton_pt,sample["tree"].lepton_eta,year)
            weight_electron_id_sf_variation *= eff_scale_factor.electron_efficiency_scale_factor(sample["tree"].lepton_pt,sample["tree"].lepton_eta,year,True,False)
            weight_electron_reco_sf_variation *= eff_scale_factor.electron_efficiency_scale_factor(sample["tree"].lepton_pt,sample["tree"].lepton_eta,year,False,True)
            weight_photon_id_sf_variation *= eff_scale_factor.electron_efficiency_scale_factor(sample["tree"].lepton_pt,sample["tree"].lepton_eta,year)
        elif sample["tree"].lepton_pdg_id == 13:
            weight *= eff_scale_factor.muon_efficiency_scale_factor(sample["tree"].lepton_pt,sample["tree"].lepton_eta,year)
            weight_pu_up *= eff_scale_factor.muon_efficiency_scale_factor(sample["tree"].lepton_pt,sample["tree"].lepton_eta,year)
            weight_muon_id_sf_variation *= eff_scale_factor.muon_efficiency_scale_factor(sample["tree"].lepton_pt,sample["tree"].lepton_eta,year,False,True)
            weight_muon_iso_sf_variation *= eff_scale_factor.muon_efficiency_scale_factor(sample["tree"].lepton_pt,sample["tree"].lepton_eta,year,True,False)
            weight_photon_id_sf_variation *= eff_scale_factor.muon_efficiency_scale_factor(sample["tree"].lepton_pt,sample["tree"].lepton_eta,year)
        else:
            assert(0)

        if options.make_recoil_trees and pass_is_lepton_real:
            mc_zpt[0] = sqrt(pow(sample["tree"].gen_photons_pt*cos(sample["tree"].gen_photons_phi) + sample["tree"].gen_leptons_pt*cos(sample["tree"].gen_leptons_phi) + sample["tree"].gen_neutrinos_pt*cos(sample["tree"].gen_neutrinos_phi),2) + pow(sample["tree"].gen_photons_pt*sin(sample["tree"].gen_photons_phi) + sample["tree"].gen_leptons_pt*sin(sample["tree"].gen_leptons_phi) + sample["tree"].gen_neutrinos_pt*sin(sample["tree"].gen_neutrinos_phi),2))
            genwphi = atan2(sample["tree"].gen_photons_pt*sin(sample["tree"].gen_photons_phi) + sample["tree"].gen_leptons_pt*sin(sample["tree"].gen_leptons_phi) + sample["tree"].gen_neutrinos_pt*sin(sample["tree"].gen_neutrinos_phi),sample["tree"].gen_photons_pt*cos(sample["tree"].gen_photons_phi) + sample["tree"].gen_leptons_pt*cos(sample["tree"].gen_leptons_phi) + sample["tree"].gen_neutrinos_pt*cos(sample["tree"].gen_neutrinos_phi))
            mc_u1[0] =  cos(genwphi)*(-sample["tree"].met*cos(sample["tree"].metphi) - sample["tree"].gen_photons_pt*cos(sample["tree"].gen_photons_phi) - sample["tree"].gen_leptons_pt*cos(sample["tree"].gen_leptons_phi)) + sin(genwphi)*(-sample["tree"].met*sin(sample["tree"].metphi) - sample["tree"].gen_photons_pt*sin(sample["tree"].gen_photons_phi) - sample["tree"].gen_leptons_pt*sin(sample["tree"].gen_leptons_phi))
            mc_u2[0] =  -sin(genwphi)*(-sample["tree"].met*cos(sample["tree"].metphi) - sample["tree"].gen_photons_pt*cos(sample["tree"].gen_photons_phi) - sample["tree"].gen_leptons_pt*cos(sample["tree"].gen_leptons_phi)) + cos(genwphi)*(-sample["tree"].met*sin(sample["tree"].metphi) - sample["tree"].gen_photons_pt*sin(sample["tree"].gen_photons_phi) - sample["tree"].gen_leptons_pt*sin(sample["tree"].gen_leptons_phi))
            mc_weight[0] = weight
            mc_recoil_tree.Fill()

        if not options.make_plots:
            continue

        if pass_is_lepton_real:
#            if bool(sample["tree"].photon_gen_matching_old & int('0010',2)):
            if sample["tree"].photon_gen_matching == 1:
                if sample["e_to_p_non_res"]:
                    for j in range(len(variables)):
                        e_to_p_non_res["hists"][j].Fill(getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight)
                if sample["e_to_p"]:
                    for j in range(len(variables)):
                        e_to_p["hists"][j].Fill(getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight)
#            elif bool(sample["tree"].photon_gen_matching_old & int('1000',2)):
#            elif sample["tree"].photon_gen_matching == 4:
            elif (((sample["tree"].photon_gen_matching == 4) or (sample["tree"].photon_gen_matching == 5)) and "w+jets" not in labelname) or ("w+jets" in labelname and sample["tree"].photon_gen_matching == 0):
#            elif True:
#            elif sample["tree"].photon_gen_matching > -1:
#            elif (sample["tree"].photon_gen_matching > 0 and "wg" in labelname) or (sample["tree"].photon_gen_matching == 0 and "w+jets" in labelname) or (sample["tree"].photon_gen_matching > 0 and "zg" in labelname) or (sample["tree"].photon_gen_matching > 0 and "top" in labelname):
                
                if sample["fsr"]:

#                    if "wjets" in sample["filename"]:
#                        print str(getVariable("dphilg",sample["tree"])) + " " + str(sample["tree"].photon_gen_matching) + " " + str(sample["tree"].photon_gen_matching_old)+ " " + str(sample["tree"].run) + " "+str(sample["tree"].lumi)+" "+str(sample["tree"].event)
           


                    for j in range(len(variables)):
                        fillHistogram(label["hists"][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight)
                        fillHistogram(label["hists-pileup-up"][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight_pu_up)
                        fillHistogram(label["hists-electron-id-sf-variation"][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight_electron_id_sf_variation)
                        fillHistogram(label["hists-electron-reco-sf-variation"][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight_electron_reco_sf_variation)
                        fillHistogram(label["hists-muon-id-sf-variation"][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight_muon_id_sf_variation)
                        fillHistogram(label["hists-muon-iso-sf-variation"][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight_muon_iso_sf_variation)
                        fillHistogram(label["hists-photon-id-sf-variation"][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight_photon_id_sf_variation)
                        if label["syst-pdf"]:
                            for k in range(0,102):
                                fillHistogram(label["hists-pdf-variation"+str(k)][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight*sample["tree"].LHEPdfWeight[k+1])
                        if label["syst-scale"]:
                            for k in range(0,8):
                                #this sample has a bug that causes the scale weight to be 1/2 the correct value
                                if sample["filename"] == "/afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019/wgjets.root":
                                    fillHistogram(label["hists-scale-variation"+str(k)][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight*sample["tree"].LHEScaleWeight[k]*2)
                                else:
                                    fillHistogram(label["hists-scale-variation"+str(k)][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight*sample["tree"].LHEScaleWeight[k])
                        
#            elif sample["tree"].photon_gen_matching == 5 or (sample["tree"].photon_gen_matching == 6 and sample["filename"] == "/afs/cern.ch/work/a/amlevin/data/wg/2016/wgjets.root"):
            elif (sample["tree"].photon_gen_matching == 6 and "w+jets" not in labelname) or ("w+jets" in labelname and sample["tree"].photon_gen_matching == 0):
#            elif True:    
#            elif sample["tree"].photon_gen_matching > -1:
#            elif (sample["tree"].photon_gen_matching > 0 and "wg" in labelname) or (sample["tree"].photon_gen_matching == 0 and "w+jets" in labelname) or (sample["tree"].photon_gen_matching > 0 and "zg" in labelname) or (sample["tree"].photon_gen_matching > 0 and "top" in labelname):
#            elif bool(sample["tree"].photon_gen_matching & int('0100',2)):
                if sample["non_fsr"]:

#                    if "wjets" in sample["filename"]:
#                        print str(getVariable("dphilg",sample["tree"])) + " " + str(sample["tree"].photon_gen_matching) + " " + str(sample["tree"].photon_gen_matching_old)+ " " + str(sample["tree"].run) + " "+str(sample["tree"].lumi)+" "+str(sample["tree"].event)

#                    if sample["filename"] == "/afs/cern.ch/work/a/amlevin/data/wg/2016/zglowmlljets.root":
#                        print str(getVariable("dphilg",sample["tree"])) + " " + str(sample["tree"].run) + " "+str(sample["tree"].lumi)+" "+str(sample["tree"].event)

                    for j in range(len(variables)):
                        fillHistogram(label["hists"][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight)
                        fillHistogram(label["hists-pileup-up"][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight_pu_up)
                        fillHistogram(label["hists-electron-id-sf-variation"][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight_electron_id_sf_variation)
                        fillHistogram(label["hists-electron-reco-sf-variation"][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight_electron_reco_sf_variation)
                        fillHistogram(label["hists-muon-id-sf-variation"][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight_muon_id_sf_variation)
                        fillHistogram(label["hists-muon-iso-sf-variation"][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight_muon_iso_sf_variation)
                        fillHistogram(label["hists-photon-id-sf-variation"][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight_photon_id_sf_variation)
                        if label["syst-pdf"]:
                            for k in range(0,102):
                                fillHistogram(label["hists-pdf-variation"+str(k)][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight*sample["tree"].LHEPdfWeight[k+1])
                        if label["syst-scale"]:
                            for k in range(0,8):
                                #this sample has a bug that causes the scale weight to be 1/2 the correct value
                                if sample["filename"] == "/afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019/wgjets.root":
                                    fillHistogram(label["hists-scale-variation"+str(k)][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight*sample["tree"].LHEScaleWeight[k]*2)
                                else:    
                                    fillHistogram(label["hists-scale-variation"+str(k)][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight*sample["tree"].LHEScaleWeight[k])

#    if len(variables) > 0  and not (sample["e_to_p"] and not sample["fsr"] and not sample["non_fsr"]):
#        label["hists"][variables[0]].Print("all")

if options.ewdim6:

    sm_lhe_weight = 373

    sm_lhe_weight_hist = ROOT.TH1D('', '', n_photon_pt_bins, binning_photon_pt )

    sm_hist = ROOT.TH1D('', '', n_photon_pt_bins, binning_photon_pt )

    cwww_reweights = [373,1,2,3,4,5,6]

    #cwww_coefficients = [0.0, 10.0,-10.0,20.0,-20.0,-30.0,30.0]

    cwww_coefficients = [0.0, 1.0,-1.0,2.0,-2.0,-3.0,3.0]

    cwww_hists = []

    cw_reweights = [373,7,8,9,10,11,12]

    #cw_coefficients = [0.0, 80.0,-80.0,160.0,-160.0,240.0,-240.0]

    cw_coefficients = [0.0, 17.0,-17.0,34.0,-34.0,51.0,-51.0]

    cw_hists = []

    cb_reweights = [373,13,14,15,16,17,18]

    #cb_coefficients = [0.0, 80.0,-80.0,160.0,-160.0,240.0,-240.0]

    cb_coefficients = [0.0, 17.0,-17.0,34.0,-34.0,51.0,-51.0]

    cb_hists = []

    cpwww_reweights = [373,19,20,21,22,23,24]

    #cpwww_coefficients = [0.0, 4.0,-4.0,8.0,-8.0,12.0,-12.0]

    cpwww_coefficients = [0.0, 0.5,-0.5,1.0,-1.0,1.5,-1.5]

    cpwww_hists = []

    cpw_reweights = [373,25,26,27,28,29,30]

    #cpw_coefficients = [0.0, 40.0,-40.0,80.0,-80.0,120.0,-120.0]

    cpw_coefficients = [0.0, 8.0,-8.0,16.0,-16.0,24.0,-24.0]

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

    for i in range(labels["wg+jets"]["samples"][0]["tree"].GetEntries()):
        labels["wg+jets"]["samples"][0]["tree"].GetEntry(i)

        w = labels["wg+jets"]["samples"][0]["xs"]*1000*lumi/labels["wg+jets"]["samples"][0]["nweightedevents"]

        w *= pu_weight_hist.GetBinContent(pu_weight_hist.FindFixBin(labels["wg+jets"]["samples"][0]["tree"].npu))

        w *= eff_scale_factor.photon_efficiency_scale_factor(labels["wg+jets"]["samples"][0]["tree"].photon_pt,labels["wg+jets"]["samples"][0]["tree"].photon_eta)

        if labels["wg+jets"]["samples"][0]["tree"].lepton_pdg_id == 13:
            w *= eff_scale_factor.muon_efficiency_scale_factor(labels["wg+jets"]["samples"][0]["tree"].lepton_pt,labels["wg+jets"]["samples"][0]["tree"].lepton_eta)
        elif labels["wg+jets"]["samples"][0]["tree"].lepton_pdg_id == 11:    
            w *= eff_scale_factor.electron_efficiency_scale_factor(labels["wg+jets"]["samples"][0]["tree"].lepton_pt,labels["wg+jets"]["samples"][0]["tree"].lepton_eta)
        else:
            assert(0)

        if labels["wg+jets"]["samples"][0]["tree"].gen_weight < 0:
            w = -w

        if pass_selection(labels["wg+jets"]["samples"][0]["tree"],year,options.phoeta):
            fillHistogram(sm_hist,getVariable(variables[0],labels["wg+jets"]["samples"][0]["tree"]),w)

    sm_hist.Print("all")

    for i in range(ewdim6_tree.GetEntries()):
        ewdim6_tree.GetEntry(i)

        w = ewdim6_xs*1000*lumi/ewdim6_nweightedevents

        w *= pu_weight_hist.GetBinContent(pu_weight_hist.FindFixBin(ewdim6_tree.npu))

        w *= eff_scale_factor.photon_efficiency_scale_factor(ewdim6_tree.photon_pt,ewdim6_tree.photon_eta)

        if ewdim6_tree.lepton_pdg_id == 13:
            w *= eff_scale_factor.muon_efficiency_scale_factor(ewdim6_tree.lepton_pt,ewdim6_tree.lepton_eta)
        elif ewdim6_tree.lepton_pdg_id == 11:    
            w *= eff_scale_factor.electron_efficiency_scale_factor(ewdim6_tree.lepton_pt,ewdim6_tree.lepton_eta)
        else:
            assert(0)

        if ewdim6_tree.gen_weight < 0:
            w = -w

        if pass_selection(ewdim6_tree,year,options.phoeta):
            for j in range(len(cwww_reweights)):
                fillHistogram(cwww_hists[j],getVariable(variables[0],ewdim6_tree),w*getattr(ewdim6_tree, 'LHEWeight_rwgt_'+str(cwww_reweights[j])))

            for j in range(len(cw_reweights)):
                fillHistogram(cw_hists[j],getVariable(variables[0],ewdim6_tree),w*getattr(ewdim6_tree, 'LHEWeight_rwgt_'+str(cw_reweights[j])))

            for j in range(len(cb_reweights)):
                fillHistogram(cb_hists[j],getVariable(variables[0],ewdim6_tree),w*getattr(ewdim6_tree, 'LHEWeight_rwgt_'+str(cb_reweights[j])))

            for j in range(len(cpwww_reweights)):
                fillHistogram(cpwww_hists[j],getVariable(variables[0],ewdim6_tree),w*getattr(ewdim6_tree, 'LHEWeight_rwgt_'+str(cpwww_reweights[j])))

            for j in range(len(cpw_reweights)):
                fillHistogram(cpw_hists[j],getVariable(variables[0],ewdim6_tree),w*getattr(ewdim6_tree, 'LHEWeight_rwgt_'+str(cpw_reweights[j])))

            fillHistogram(sm_lhe_weight_hist,getVariable(variables[0],ewdim6_tree),w*getattr(ewdim6_tree, 'LHEWeight_rwgt_'+str(sm_lhe_weight)))

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

    cwww_scaling_hists = {}

    for i in range(1,cwww_hists[0].GetNbinsX()+1):
        ROOT.gROOT.cd() #so that the histogram created in the next line is not put in a file that is closed
        cwww_scaling_hists[i]=ROOT.TH1D("ewdim6_scaling_bin_"+str(i),"ewdim6_scaling_bin_"+str(i),len(cwww_coefficients),cwww_hist_min,cwww_hist_max);

        for j in range(0,len(cwww_hists)):
            assert(sm_lhe_weight_hist.GetBinContent(i) > 0)

            cwww_scaling_hists[i].SetBinContent(cwww_scaling_hists[i].GetXaxis().FindFixBin(cwww_coefficients[j]), cwww_hists[j].GetBinContent(i)/sm_lhe_weight_hist.GetBinContent(i))
        
        cwww_scaling_outfile.cd()
        cwww_scaling_hists[i].Write()

    cwww_scaling_outfile.Close()

    for i in range(1,cw_hists[0].GetNbinsX()+1):
        cw_scaling_hist=ROOT.TH1D("ewdim6_scaling_bin_"+str(i),"ewdim6_scaling_bin_"+str(i),len(cw_coefficients),cw_hist_min,cw_hist_max);

        for j in range(0,len(cw_hists)):
            assert(sm_lhe_weight_hist.GetBinContent(i) > 0)

            cw_scaling_hist.SetBinContent(cw_scaling_hist.GetXaxis().FindFixBin(cw_coefficients[j]), cw_hists[j].GetBinContent(i)/sm_lhe_weight_hist.GetBinContent(i))
        
        cw_scaling_outfile.cd()
        cw_scaling_hist.Write()

    cw_scaling_outfile.Close()

    for i in range(1,cb_hists[0].GetNbinsX()+1):
        cb_scaling_hist=ROOT.TH1D("ewdim6_scaling_bin_"+str(i),"ewdim6_scaling_bin_"+str(i),len(cb_coefficients),cb_hist_min,cb_hist_max);

        for j in range(0,len(cb_hists)):
            assert(sm_lhe_weight_hist.GetBinContent(i) > 0)

            cb_scaling_hist.SetBinContent(cb_scaling_hist.GetXaxis().FindFixBin(cb_coefficients[j]), cb_hists[j].GetBinContent(i)/sm_lhe_weight_hist.GetBinContent(i))
        
        cb_scaling_outfile.cd()
        cb_scaling_hist.Write()

    cb_scaling_outfile.Close()

    for i in range(1,cpwww_hists[0].GetNbinsX()+1):
        cpwww_scaling_hist=ROOT.TH1D("ewdim6_scaling_bin_"+str(i),"ewdim6_scaling_bin_"+str(i),len(cpwww_coefficients),cpwww_hist_min,cpwww_hist_max);

        for j in range(0,len(cpwww_hists)):
            assert(sm_lhe_weight_hist.GetBinContent(i) > 0)

            cpwww_scaling_hist.SetBinContent(cpwww_scaling_hist.GetXaxis().FindFixBin(cpwww_coefficients[j]), cpwww_hists[j].GetBinContent(i)/sm_lhe_weight_hist.GetBinContent(i))
        
        cpwww_scaling_outfile.cd()
        cpwww_scaling_hist.Write()

    cpwww_scaling_outfile.Close()

    for i in range(1,cpw_hists[0].GetNbinsX()+1):
        cpw_scaling_hist=ROOT.TH1D("ewdim6_scaling_bin_"+str(i),"ewdim6_scaling_bin_"+str(i),len(cpw_coefficients),cpw_hist_min,cpw_hist_max);

        for j in range(0,len(cpw_hists)):
            assert(sm_lhe_weight_hist.GetBinContent(i) > 0)

            cpw_scaling_hist.SetBinContent(cpw_scaling_hist.GetXaxis().FindFixBin(cpw_coefficients[j]), cpw_hists[j].GetBinContent(i)/sm_lhe_weight_hist.GetBinContent(i))
        
        cpw_scaling_outfile.cd()
        cpw_scaling_hist.Write()

    cpw_scaling_outfile.Close()

if options.ewdim6_scaling_only:
    sys.exit(1)

data_mlg_tree = ROOT.TTree()

array_data_mlg=array('f',[0])

data_mlg_tree.Branch('m',array_data_mlg,'m/F')

for year in years:

    if lepton_name == "muon":
        if not closure_test:
            data_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/"+year+"/1June2019/single_muon.root")
        else:
            data_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/"+year+"/1June2019/wjets.root")
    elif lepton_name == "electron":
        if not closure_test:
            if year != "2018":
                data_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/"+year+"/1June2019/single_electron.root")
            else:    
                data_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/"+year+"/1June2019/egamma.root")
        else:
            data_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/"+year+"/1June2019/wjets.root")
    elif lepton_name == "both":
        if not closure_test:
            if year != "2018":
                data_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/"+year+"/1June2019/data.root")
            else:
                data_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/"+year+"/1June2019/data.root")
        else:
            data_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/"+year+"/1June2019/wjets.root")
    else:
        assert(0)

    data_events_tree = data_file.Get("Events")

    print "Running over "+year+" data"
    print "data_events_tree.GetEntries() = " + str(data_events_tree.GetEntries())

    for i in range(data_events_tree.GetEntries()):

        data_events_tree.GetEntry(i)

        if i > 0 and i % 100000 == 0:
            print "Processed " + str(i) + " out of " + str(data_events_tree.GetEntries()) + " events"

#    if data_events_tree.event != 3041956875:
#        continue

#    if data_events_tree.puppimet < 60 or data_events_tree.puppimt < 30:
        if data_events_tree.puppimet < puppimetlow or data_events_tree.puppimet > puppimethigh or data_events_tree.met < metlow or data_events_tree.met > methigh or abs(data_events_tree.lepton_pdg_id) not in lepton_abspdgids or abs(data_events_tree.photon_eta) < photon_eta_min or abs(data_events_tree.photon_eta) > photon_eta_max:
            continue

#    if not pass_json(data_events_tree.run,data_events_tree.lumi):
#        continue

        if closure_test and data_events_tree.photon_gen_matching != 0 :
            continue
    
        if getVariable("photon_recoil",data_events_tree) > 1000000 or getVariable("photon_recoil",data_events_tree) < -1000000:
            continue

        if pass_selection(data_events_tree,year,options.phoeta):

            if data_events_tree.photon_pt > blinding_cut:
                pass
            else:

                weight = 1

                if closure_test and data_events_tree.gen_weight < 0:
                    weight = -1
#                pass

#            print str(data_events_tree.njets40)+" "+str(data_events_tree.run) + " "+str(data_events_tree.lumi)+" "+str(data_events_tree.event)

                

                for j in range(len(variables)):
                    fillHistogram(data["hists"][j],getVariable(variables[j],data_events_tree),weight)

                array_data_mlg[0] = getVariable("mlg",data_events_tree)
                data_mlg_tree.Fill()

        if pass_selection(data_events_tree,year,options.phoeta,True,False):

            weight = fake_lepton_weight(data_events_tree.lepton_pdg_id,data_events_tree.lepton_eta, data_events_tree.lepton_pt,year, "nominal")
            weight_fake_lepton_stat_up = fake_lepton_weight(data_events_tree.lepton_pdg_id,data_events_tree.lepton_eta, data_events_tree.lepton_pt,year,"up")
            weight_fake_lepton_stat_down = fake_lepton_weight(data_events_tree.lepton_pdg_id,data_events_tree.lepton_eta, data_events_tree.lepton_pt,year,"down")

            if closure_test:
                weight = 0

            for j in range(len(variables)):
                fillHistogram(fake_lepton["hists"][j],getVariable(variables[j],data_events_tree),weight)
                fillHistogram(fake_lepton_stat_up["hists"][j],getVariable(variables[j],data_events_tree),weight_fake_lepton_stat_up)
                fillHistogram(fake_lepton_stat_down["hists"][j],getVariable(variables[j],data_events_tree),weight_fake_lepton_stat_down)

        if pass_selection(data_events_tree,year,options.phoeta,False,True):
            weight = fake_photon_weight(data_events_tree.photon_eta, data_events_tree.photon_pt,year,getVariable("photon_recoil",data_events_tree),data_events_tree.lepton_pdg_id )
            weight_fake_photon_alt = fake_photon_weight(data_events_tree.photon_eta, data_events_tree.photon_pt,year,getVariable("photon_recoil",data_events_tree),data_events_tree.lepton_pdg_id, True)
            weight_fake_photon_stat_up = fake_photon_weight(data_events_tree.photon_eta, data_events_tree.photon_pt,year,getVariable("photon_recoil",data_events_tree),data_events_tree.lepton_pdg_id, False, True)

            if closure_test and data_events_tree.gen_weight < 0:
                weight *= -1
#            pass


            for j in range(len(variables)):
                fillHistogram(fake_photon["hists"][j],getVariable(variables[j],data_events_tree),weight)
                fillHistogram(fake_photon_alt["hists"][j],getVariable(variables[j],data_events_tree),weight_fake_photon_alt)
                fillHistogram(fake_photon_stat_up["hists"][j],getVariable(variables[j],data_events_tree),weight_fake_photon_stat_up)


#        print fake_photon_weight(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id )

        if pass_selection(data_events_tree,year,options.phoeta,True,True):

            weight = fake_lepton_weight(data_events_tree.lepton_pdg_id,data_events_tree.lepton_eta, data_events_tree.lepton_pt, year, "nominal")*fake_photon_weight(data_events_tree.photon_eta, data_events_tree.photon_pt,year,getVariable("photon_recoil",data_events_tree),data_events_tree.lepton_pdg_id)
            weight_fake_photon_alt = fake_lepton_weight(data_events_tree.lepton_pdg_id,data_events_tree.lepton_eta, data_events_tree.lepton_pt, year, "nominal")*fake_photon_weight(data_events_tree.photon_eta, data_events_tree.photon_pt, year, getVariable("photon_recoil",data_events_tree),data_events_tree.lepton_pdg_id, True)
            weight_fake_photon_stat_up = fake_lepton_weight(data_events_tree.lepton_pdg_id,data_events_tree.lepton_eta, data_events_tree.lepton_pt, year, "nominal")*fake_photon_weight (data_events_tree.photon_eta, data_events_tree.photon_pt, year, getVariable("photon_recoil",data_events_tree),data_events_tree.lepton_pdg_id, False,True)

            if closure_test:
                weight = 0

#        weight = 0    

            for j in range(len(variables)):
                fillHistogram(double_fake["hists"][j],getVariable(variables[j],data_events_tree),weight)
                fillHistogram(fake_lepton["hists"][j],getVariable(variables[j],data_events_tree),-weight)
                fillHistogram(fake_photon["hists"][j],getVariable(variables[j],data_events_tree),-weight)
                fillHistogram(fake_photon_alt["hists"][j],getVariable(variables[j],data_events_tree),-weight_fake_photon_alt)
                fillHistogram(fake_photon_stat_up["hists"][j],getVariable(variables[j],data_events_tree),-weight_fake_photon_stat_up)


#import sys
#sys.exit(1)

#data_mlg_tree.Scan("*")


for year in years:
    for label in labels.keys():

        for sample in labels[label]["samples"][year]:
            fillHistogramMC(labels[label],sample,label,year)

        for i in range(len(variables)):    

            if labels[label]["color"] == None:
                continue

            labels[label]["hists"][i].SetFillColor(labels[label]["color"])
            labels[label]["hists"][i].SetFillStyle(1001)
            labels[label]["hists"][i].SetLineColor(labels[label]["color"])

if options.make_recoil_trees:

    recoil_outfile.cd()

    mc_recoil_tree.Write()

    recoil_outfile.Close()

def mlg_fit(inputs):

    m= ROOT.RooRealVar("m","m",0,mlg_fit_upper_bound)
    m0=ROOT.RooRealVar("m0",    "m0",1.55915,-2.5,2.5)
    sigma=ROOT.RooRealVar("sigma",  "sigma",1.75029,0.1,3)
    alpha=ROOT.RooRealVar("alpha",  "alpha",2.26024,0,10)
#    alpha=ROOT.RooRealVar("alpha",  "alpha",4.45779,4.45779-2,4.45779+2)
#    alpha=ROOT.RooRealVar("alpha",  "alpha",,0,10)
#    alpha=ROOT.RooRealVar("alpha",  "alpha",4.27560,4.27560,4.27560)
#    n=ROOT.RooRealVar("n",          "n",2.11960,1,3)
    n=ROOT.RooRealVar("n",          "n",2.11960,2.11960,2.11960)
    cb = ROOT.RooCBShape("cb", "Crystal Ball", m, m0, sigma, alpha, n)

    mass = ROOT.RooRealVar("mass","mass",89.855,89.855-5,89.855+5)
    width = ROOT.RooRealVar("width","width",3.85825,3.0*3.85825/4.0,5*3.85825/3.0);
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
    wg_norm = ROOT.RooRealVar("wg_norm","wg_norm",13234.2,0.5*13234.2,2*13234.2);    
    wg_plus_fake_wg_contamination_norm = ROOT.RooRealVar("wg_plus_fake_wg_contamination_norm","wg_plus_fake_wg_contamination_norm",13234.2,0.5*13234.2,2*13234.2);    
#    zg_norm = ROOT.RooRealVar("zg_norm","zg_norm",0,1000000);    
    zg_norm = ROOT.RooRealVar("zg_norm","zg_norm",inputs["zg"].Integral(),inputs["zg"].Integral());    
    vv_norm = ROOT.RooRealVar("vv_norm","vv_norm",inputs["vv"].Integral(),inputs["vv"].Integral());    
    bwcb_norm = ROOT.RooRealVar("bwcb_norm","bwcb_norm",3488.71,0.5*3488.71,2*3488.71);    
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

    sum.fitTo(RooDataHist_mlg_data,ROOT.RooFit.Extended(),ROOT.RooFit.Strategy(2))
    #sum.fitTo(RooDataSet_mlg_data,ROOT.RooFit.Extended())

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

    if options.float_fake_sig_cont:
        mlg_fit_results["wg_norm"] = wg_plus_fake_wg_contamination_norm.getVal()*inputs["wg"].Integral()/(inputs["wg"].Integral() + inputs["fake-wg-contamination"].Integral())
        mlg_fit_results["wg_norm_err"] = wg_plus_fake_wg_contamination_norm.getError()*inputs["wg"].Integral()/(inputs["wg"].Integral() + inputs["fake-wg-contamination"].Integral())
    else:
        mlg_fit_results["wg_norm"] = wg_norm.getVal()
        mlg_fit_results["wg_norm_err"] = wg_norm.getError()

#instead of resetting after each fit, turn the static minuit feature off (see above near "import ROOT")
#    ROOT.gMinuit.mncler()
#    ROOT.gMinuit.mnrn15(ROOT.Double(3),ctypes.c_int(12345))

    return mlg_fit_results

#if lepton_name == "electron":
if False:

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

    fit_inputs_fake_lepton_stat_down = dict(fit_inputs)
    fit_inputs_fake_lepton_stat_down["label"] = "fake_lepton_stat_down"
    fit_inputs_fake_lepton_stat_down["fake_lepton"] = fake_lepton_stat_down["hists"][mlg_index]
    fit_results_fake_lepton_stat_down = mlg_fit(fit_inputs_fake_lepton_stat_down)

    fit_inputs_fake_photon_alt = dict(fit_inputs)
    fit_inputs_fake_photon_alt["fake_photon"] = fake_photon_alt["hists"][mlg_index]
    fit_inputs_fake_photon_alt["label"] = "fake_photon_alt"
    fit_results_fake_photon_alt = mlg_fit(fit_inputs_fake_photon_alt)

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

    fit_results_zg_scale_variation = []

    for i in range(0,8): 
        fit_inputs_zg_scale_variation = dict(fit_inputs)
        fit_inputs_zg_scale_variation["label"] = "zg_scale_variation_"+str(i)
        fit_inputs_zg_scale_variation["zg"] = labels["zg+jets"]["hists-scale-variation"+str(i)][mlg_index]
        fit_results_zg_scale_variation.append(mlg_fit(fit_inputs_zg_scale_variation))

    fit_results_zg_pdf_variation = []

    for i in range(1,102): 
        fit_inputs_zg_pdf_variation = dict(fit_inputs)
        fit_inputs_zg_pdf_variation["label"] = "zg_pdf_variation_"+str(i)
        fit_inputs_zg_pdf_variation["zg"] = labels["zg+jets"]["hists-pdf-variation"+str(i)][mlg_index]
        fit_results_zg_pdf_variation.append(mlg_fit(fit_inputs_zg_pdf_variation))

pileup_unc = abs(labels["wg+jets"]["hists-pileup-up"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].Integral())
electron_id_sf_unc = labels["wg+jets"]["hists-electron-id-sf-variation"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].Integral()
electron_reco_sf_unc = labels["wg+jets"]["hists-electron-reco-sf-variation"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].Integral()
muon_id_sf_unc = labels["wg+jets"]["hists-muon-id-sf-variation"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].Integral()
muon_iso_sf_unc = labels["wg+jets"]["hists-muon-iso-sf-variation"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].Integral()
photon_id_sf_unc = labels["wg+jets"]["hists-photon-id-sf-variation"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].Integral()

print "(number of wg+jets events run over) = "+str(labels["wg+jets"]["samples"][year][0]["nweightedevents"])

print "fiducial_region_cuts_efficiency = "+str(fiducial_region_cuts_efficiency)

if options.draw_ewdim6:
    for i in range(1,n_photon_pt_bins+1):
        #hardcoded to use bin 6 of the scaling histogram for now 
        ewdim6["hists"][0].SetBinContent(i,cwww_scaling_hists[i].GetBinContent(6)*labels["wg+jets"]["hists"][0].GetBinContent(i))

for i in range(len(variables)):

#    fake_lepton["hists"][i].Scale(2)

    fake_photon["hists"][i].Scale(1.0)

    if use_wjets_mc_for_fake_photon:
        fake_photon["hists"][i].Scale(0)

    data["hists"][i].Print("all")
    fake_photon["hists"][i].Print("all")
    labels["wg+jets"]["hists"][i].Print("all")



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

#
    hsum = data["hists"][i].Clone()
    hsum.Scale(0.0)

    hstack = ROOT.THStack()

    for label in labels.keys():
        if labels[label]["color"] == None:
            continue
        hsum.Add(labels[label]["hists"][i])
        hstack.Add(labels[label]["hists"][i])

    if lepton_name == "electron" or lepton_name == "both": 
        hsum.Add(e_to_p["hists"][i])
        hstack.Add(e_to_p["hists"][i])

    hsum.Add(e_to_p_non_res["hists"][i])
    hstack.Add(e_to_p_non_res["hists"][i])

    if data_driven:
        hsum.Add(fake_lepton["hists"][i])
        hsum.Add(fake_photon["hists"][i])
        hsum.Add(double_fake["hists"][i])

    if data_driven:
        hstack.Add(fake_lepton["hists"][i])
        hstack.Add(fake_photon["hists"][i])
        hstack.Add(double_fake["hists"][i])


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
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,data["hists"][i],"data","lp")

    if data_driven :
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
        draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,fake_photon["hists"][i],"fake photon","f")
        j=j+1
        draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,double_fake["hists"][i],"double fake","f")

    if lepton_name == "electron" or lepton_name == "both": 
        j=j+1
        draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,e_to_p["hists"][i],"e->#gamma","f")

    j=j+1
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,e_to_p_non_res["hists"][i],"e->#gamma non-res","f")

    for label in labels.keys():
        if labels[label]["color"] == None:
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
    set_axis_fonts(hstack,"x",options.xaxislabel)
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

n_signal = data_integral - double_fake_integral - fake_photon_integral - fake_lepton_integral - top_jets_integral - vv_jets_integral - zg_jets_integral

n_signal_error = sqrt(pow(data_integral_error,2) + pow(double_fake_integral_error,2) + pow(fake_lepton_integral_error,2)+ pow(fake_photon_integral_error,2)+pow(top_jets_integral_error,2)+ pow(vv_jets_integral_error,2)+ pow(zg_jets_integral_error,2))

print "n_signal = "+str(n_signal) + " +/- " + str(n_signal_error)

#labels["wg+jets"]["hists"]["photon_pt"].Print("all")

double_fake["hists"][mlg_index].Print("all")
fake_lepton["hists"][mlg_index].Print("all")
fake_photon["hists"][mlg_index].Print("all")
fake_photon_alt["hists"][mlg_index].Print("all")
fake_photon_stat_up["hists"][mlg_index].Print("all")

if lepton_name == "muon":

    xs_inputs_muon = {
        "fiducial_region_cuts_efficiency":fiducial_region_cuts_efficiency,
        "n_weighted_run_over" : labels["wg+jets"]["samples"][year][0]["nweightedevents"],
        "n_signal_muon" : n_signal,
        "n_signal_syst_unc_due_to_pileup" : abs(labels["top+jets"]["hists-pileup-up"][mlg_index].Integral()+ labels["zg+jets"]["hists-pileup-up"][mlg_index].Integral()+labels["vv+jets"]["hists-pileup-up"][mlg_index].Integral()-labels["top+jets"]["hists"][mlg_index].Integral()- labels["zg+jets"]["hists"][mlg_index].Integral()-labels["vv+jets"]["hists"][mlg_index].Integral()),
        "n_signal_syst_unc_due_to_fake_photon_muon" : abs(fake_photon_alt["hists"][mlg_index].Integral() - fake_photon["hists"][mlg_index].Integral()),
        "n_signal_syst_unc_due_to_fake_lepton_muon" : abs(fake_lepton["hists"][mlg_index].Integral()*1.3 - fake_lepton["hists"][mlg_index].Integral()),
        "n_signal_stat_unc_muon" : n_signal_error,
        "n_weighted_selected_data_mc_sf_muon" : labels["wg+jets"]["hists"][mlg_index].Integral()*labels["wg+jets"]["samples"][year][0]["nweightedevents"]/(labels["wg+jets"]["samples"][year][0]["xs"]*1000*lumi),
        "n_weighted_selected_data_mc_sf_syst_unc_due_to_pileup" : pileup_unc,
        "n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_id_sf_muon" : muon_id_sf_unc,
        "n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_iso_sf_muon" : muon_iso_sf_unc,
        "n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_muon" : photon_id_sf_unc
        }

    for i in range(1,102):
        xs_inputs_muon["n_weighted_selected_data_mc_sf_pdf_variation"+str(i)] = labels["wg+jets"]["hists-pdf-variation"+str(i)][mlg_index].Integral()*labels["wg+jets"]["samples"][0]["nweightedevents"]/(labels["wg+jets"]["samples"][year][0]["xs"]*1000*lumi)
        xs_inputs_muon["n_weighted_run_over_pdf_variation"+str(i)] = labels["wg+jets"]["samples"][year][0]["nweightedevents_pdfweight"+str(i)]

    for i in range(0,8):
        xs_inputs_muon["n_weighted_selected_data_mc_sf_scale_variation"+str(i)] = labels["wg+jets"]["hists-scale-variation"+str(i)][mlg_index].Integral()*labels["wg+jets"]["samples"][year][0]["nweightedevents"]/(labels["wg+jets"]["samples"][year][0]["xs"]*1000*lumi) 
        xs_inputs_muon["n_weighted_run_over_scale_variation"+str(i)] = labels["wg+jets"]["samples"][year][0]["nweightedevents_qcdscaleweight"+str(i)]
        
    for i in range(1,fake_photon["hists"][mlg_index].GetNbinsX()+1): 
        xs_inputs_muon["n_signal_syst_unc_due_to_fake_photon_stat_up_bin"+str(i)] = fake_photon["hists"][mlg_index].GetBinError(i)

    for i in range(1,fake_lepton["hists"][mlg_index].GetNbinsX()+1): 
        xs_inputs_muon["n_signal_syst_unc_due_to_fake_lepton_stat_up_bin"+str(i)] = fake_lepton["hists"][mlg_index].GetBinError(i)

    for i in range(1,double_fake["hists"][mlg_index].GetNbinsX()+1): 
        xs_inputs_muon["n_signal_syst_unc_due_to_double_fake_stat_up_bin"+str(i)] = double_fake["hists"][mlg_index].GetBinError(i)

    for i in range(1,labels["zg+jets"]["hists"][mlg_index].GetNbinsX()+1): 
        xs_inputs_muon["n_signal_syst_unc_due_to_zg_stat_up_bin"+str(i)] = labels["zg+jets"]["hists"][mlg_index].GetBinError(i)

    for i in range(1,labels["vv+jets"]["hists"][mlg_index].GetNbinsX()+1): 
        xs_inputs_muon["n_signal_syst_unc_due_to_vv_stat_up_bin"+str(i)] = labels["vv+jets"]["hists"][mlg_index].GetBinError(i)

    for i in range(1,labels["top+jets"]["hists"][mlg_index].GetNbinsX()+1): 
        xs_inputs_muon["n_signal_syst_unc_due_to_top_stat_up_bin"+str(i)] = labels["top+jets"]["hists"][mlg_index].GetBinError(i)

    for i in range(0,8): 
        xs_inputs_muon["n_signal_syst_unc_due_to_zg_scale_variation"+str(i)] = labels["zg+jets"]["hists"][mlg_index].Integral() - labels["zg+jets"]["hists-scale-variation"+str(i)][mlg_index].Integral()

    for i in range(1,102): 
        xs_inputs_muon["n_signal_syst_unc_due_to_zg_pdf_variation"+str(i)] = labels["zg+jets"]["hists"][mlg_index].Integral() - labels["zg+jets"]["hists-pdf-variation"+str(i)][mlg_index].Integral()

    xs_inputs_muon["n_signal_syst_unc_due_to_lumi_up"] = abs(0.026*(labels["zg+jets"]["hists"][mlg_index].Integral()+labels["top+jets"]["hists"][mlg_index].Integral() + labels["vv+jets"]["hists"][mlg_index].Integral()) )

    pprint(xs_inputs_muon)

    import json

    f_muon = open("xs_inputs_muon.txt","w")

    json.dump(xs_inputs_muon,f_muon)

elif lepton_name == "electron":

    xs_inputs_electron = {
        "fiducial_region_cuts_efficiency":fiducial_region_cuts_efficiency,
        "n_weighted_run_over" : labels["wg+jets"]["samples"][0]["nweightedevents"],
        "n_signal_electron" : fit_results["wg_norm"],
        "n_signal_syst_unc_due_to_pileup" : abs(fit_results_pileup_up["wg_norm"]-fit_results["wg_norm"]),
        "n_signal_syst_unc_due_to_fake_photon_electron" : abs(fit_results_fake_photon_alt["wg_norm"]-fit_results["wg_norm"]),
        "n_signal_syst_unc_due_to_fake_lepton_electron" : abs(fit_results_fake_lepton_syst["wg_norm"]-fit_results["wg_norm"]),
        "n_signal_stat_unc_electron" : fit_results["wg_norm_err"],
        "n_weighted_selected_data_mc_sf_electron" : labels["wg+jets"]["hists"][mlg_index].Integral()*labels["wg+jets"]["samples"][year][0]["nweightedevents"]/(labels["wg+jets"]["samples"][year][0]["xs"]*1000*lumi), 
        "n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_id_sf_electron" : electron_id_sf_unc,
        "n_weighted_selected_data_mc_sf_syst_unc_due_to_pileup" : pileup_unc,
        "n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_reco_sf_electron" : electron_reco_sf_unc,
        "n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_electron" : photon_id_sf_unc
        }

    for i in range(1,102):
        xs_inputs_electron["n_weighted_selected_data_mc_sf_pdf_variation"+str(i)] = labels["wg+jets"]["hists-pdf-variation"+str(i)][mlg_index].Integral()*labels["wg+jets"]["samples"][year][0]["nweightedevents"]/(labels["wg+jets"]["samples"][year][0]["xs"]*1000*lumi) 
        xs_inputs_electron["n_weighted_run_over_pdf_variation"+str(i)] = labels["wg+jets"]["samples"][0]["nweightedevents_pdfweight"+str(i)]

    for i in range(0,8):
        xs_inputs_electron["n_weighted_selected_data_mc_sf_scale_variation"+str(i)] = labels["wg+jets"]["hists-scale-variation"+str(i)][mlg_index].Integral()*labels["wg+jets"]["samples"][year][0]["nweightedevents"]/(labels["wg+jets"]["samples"][year][0]["xs"]*1000*lumi) 
        xs_inputs_electron["n_weighted_run_over_scale_variation"+str(i)] = labels["wg+jets"]["samples"][0]["nweightedevents_qcdscaleweight"+str(i)]

    for i in range(1,fake_photon["hists"][mlg_index].GetNbinsX()+1): 
        xs_inputs_electron["n_signal_syst_unc_due_to_fake_photon_stat_up_bin"+str(i)] = abs(fit_results_fake_photon_stat_up[i-1]["wg_norm"] - fit_results["wg_norm"])

    for i in range(1,fake_lepton["hists"][mlg_index].GetNbinsX()+1): 
        xs_inputs_electron["n_signal_syst_unc_due_to_fake_lepton_stat_up_bin"+str(i)] = abs(fit_results_fake_lepton_stat_up[i-1]["wg_norm"] - fit_results["wg_norm"])

    for i in range(1,double_fake["hists"][mlg_index].GetNbinsX()+1): 
        xs_inputs_electron["n_signal_syst_unc_due_to_double_fake_stat_up_bin"+str(i)] = abs(fit_results_double_fake_stat_up[i-1]["wg_norm"] - fit_results["wg_norm"])

    for i in range(1,labels["zg+jets"]["hists"][mlg_index].GetNbinsX()+1): 
        xs_inputs_electron["n_signal_syst_unc_due_to_zg_stat_up_bin"+str(i)] = abs(fit_results_zg_stat_up[i-1]["wg_norm"] - fit_results["wg_norm"])

    for i in range(1,labels["vv+jets"]["hists"][mlg_index].GetNbinsX()+1): 
        xs_inputs_electron["n_signal_syst_unc_due_to_vv_stat_up_bin"+str(i)] = abs(fit_results_vv_stat_up[i-1]["wg_norm"] - fit_results["wg_norm"])

    for i in range(1,labels["top+jets"]["hists"][mlg_index].GetNbinsX()+1): 
        xs_inputs_electron["n_signal_syst_unc_due_to_top_stat_up_bin"+str(i)] = abs(fit_results_top_stat_up[i-1]["wg_norm"] - fit_results["wg_norm"])

    for i in range(0,8): 
        xs_inputs_electron["n_signal_syst_unc_due_to_zg_scale_variation"+str(i)] = fit_results_zg_scale_variation[i]["wg_norm"] - fit_results["wg_norm"]

    for i in range(1,102): 
        xs_inputs_electron["n_signal_syst_unc_due_to_zg_pdf_variation"+str(i)] = fit_results_zg_pdf_variation[i-1]["wg_norm"] - fit_results["wg_norm"]

    xs_inputs_electron["n_signal_syst_unc_due_to_lumi_up"] = abs(fit_results_lumi_up["wg_norm"] - fit_results["wg_norm"])

    pprint(xs_inputs_electron)

    import json

    f_electron = open("xs_inputs_electron.txt","w")

    json.dump(xs_inputs_electron,f_electron)

if not options.ewdim6:
    sys.exit(0)

for i in range(1,sm_lhe_weight_hist.GetNbinsX()+1):

    dcard = open("photon_pt_bin"+str(i)+".txt",'w')

    print >> dcard, "imax 1 number of channels"
    print >> dcard, "jmax * number of background"
    print >> dcard, "kmax * number of nuisance parameters"
    print >> dcard, "Observation "+str(data["hists"][0].GetBinContent(i))
    dcard.write("bin")
    dcard.write(" bin1")
    
    for label in labels.keys():
        if label == "no label" or label == "wg+jets":
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
        if label == "no label" or label == "wg+jets":
            continue
        dcard.write(" " + label)

    dcard.write(" fake_photon")
    dcard.write(" fake_lepton")
    dcard.write(" double_fake")
    dcard.write(" e_to_p_non_res")
    dcard.write('\n')    
    dcard.write("process")
    dcard.write(" 0")
    
    for j in range(1,len(labels.keys())+3):
        dcard.write(" " + str(j))
    dcard.write('\n')    
    dcard.write('rate')
#    dcard.write(' '+str(sm_lhe_weight_hist.GetBinContent(i)))
    dcard.write(' '+str(labels["wg+jets"]["hists"][0].GetBinContent(i)))
    for label in labels.keys():
        if label == "no label" or label == "wg+jets":
            continue
        if labels[label]["hists"][0].GetBinContent(i) > 0:
            dcard.write(" "+ str(labels[label]["hists"][0].GetBinContent(i)))
        else:
            dcard.write(" 0.0001") 



    if fake_photon["hists"][0].GetBinContent(i) > 0:        
        dcard.write(" "+str(fake_photon["hists"][0].GetBinContent(i))) 
    else:
        if fake_photon["hists"][0].GetBinContent(i) < 0:
            print "Warning: fake photon estimate is "+str(fake_photon["hists"][0].GetBinContent(i))+ " for bin " + str(i) + ". It will be replaced with 0.0001"
        dcard.write(" 0.0001") 

    if fake_lepton["hists"][0].GetBinContent(i) > 0:        
        dcard.write(" "+str(fake_lepton["hists"][0].GetBinContent(i))) 
    else:
        if fake_lepton["hists"][0].GetBinContent(i) < 0:
            print "Warning: fake lepton estimate is "+str(fake_lepton["hists"][0].GetBinContent(i))+ " for bin " + str(i) + ". It will be replaced with 0.0001"
        dcard.write(" 0.0001") 

    if double_fake["hists"][0].GetBinContent(i) > 0:        
        dcard.write(" "+str(double_fake["hists"][0].GetBinContent(i))) 
    else:
        if double_fake["hists"][0].GetBinContent(i) < 0:
            print "Warning: double fake estimate is "+str(double_fake["hists"][0].GetBinContent(i))+ " for bin " + str(i) + ". It will be replaced with 0.0001"
        dcard.write(" 0.0001") 

    if e_to_p["hists"][0].GetBinContent(i) > 0:        
        dcard.write(" "+str(e_to_p["hists"][0].GetBinContent(i))) 
    else:
        dcard.write(" 0.0001") 
   
    dcard.write('\n')    

    dcard.write("lumi_13tev lnN")
    dcard.write(" 1.027")

    for label in labels.keys():
        if label == "no label" or label == "wg+jets":
            continue
        dcard.write(" 1.027")

    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" -")
    dcard.write(" 1.027")

    dcard.write('\n')    

    if sm_lhe_weight_hist.GetBinContent(i) > 0:
#        dcard.write("mcstat_ewdim6_bin"+str(i)+" lnN "+str(1+sm_lhe_weight_hist.GetBinError(i)/sm_lhe_weight_hist.GetBinContent(i)))
        dcard.write("mcstat_ewdim6_bin"+str(i)+" lnN "+str(1+labels["wg+jets"]["hists"][0].GetBinError(i)/labels["wg+jets"]["hists"][0].GetBinContent(i)))
        for label in labels.keys():
            if label == "no label" or label == "wg+jets":
                continue
            dcard.write(" -")

        dcard.write(" -")                
        dcard.write(" -")                
        dcard.write(" -")                
        dcard.write(" -")                
        dcard.write("\n")  

    for label in labels.keys():
        if label == "no label" or label == "wg+jets":
            continue

        if labels[label]["hists"][0].GetBinContent(i) > 0:
            dcard.write("mcstat_"+str(label)+"_bin"+str(i)+" lnN ")
            dcard.write(" -")

            for l in labels.keys():
                if l == "no label" or l == "wg+jets":
                    continue
                if l == label:
                    dcard.write(" "+str(1+labels[label]["hists"][0].GetBinError(i)/labels[label]["hists"][0].GetBinContent(i)))
                else:    
                    dcard.write(" -")

            dcard.write(" -")                
            dcard.write(" -")                
            dcard.write(" -")                
            dcard.write(" -")                
            dcard.write("\n")  

    if fake_lepton["hists"][0].GetBinContent(i) > 0:        
        dcard.write("fake_lepton_syst lnN -")
        for label in labels.keys():
            if label == "no label" or label == "wg+jets":
                continue
            dcard.write(" -")

        dcard.write(" -")                
        dcard.write(" 1.3")                
        dcard.write(" -")                
        dcard.write(" -")                
        dcard.write("\n")  

    if fake_lepton["hists"][0].GetBinContent(i) > 0:        
        dcard.write("fake_lepton_stat lnN -")
        for label in labels.keys():
            if label == "no label" or label == "wg+jets":
                continue
            dcard.write(" -")

        dcard.write(" -")                
        dcard.write(" "+str(1+fake_lepton["hists"][0].GetBinError(i)/fake_lepton["hists"][0].GetBinContent(i)))
        dcard.write(" -")                
        dcard.write(" -")                
        dcard.write("\n")  

    if fake_photon["hists"][0].GetBinContent(i) > 0:        
        dcard.write("fake_photon_stat lnN -")
        for label in labels.keys():
            if label == "no label" or label == "wg+jets":
                continue
            dcard.write(" -")

        dcard.write(" "+str(1+fake_photon["hists"][0].GetBinError(i)/fake_photon["hists"][0].GetBinContent(i)))
        dcard.write(" -")                
        dcard.write(" -")                
        dcard.write(" -")                
        dcard.write("\n")  
