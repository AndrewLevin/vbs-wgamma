data_driven = True

import json

import sys
import style

import optparse

from math import hypot, pi

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


parser.add_option('--lep',dest='lep',default='muon')
parser.add_option('--phoeta',dest='phoeta',default='barrel')

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

if options.phoeta == "barrel":
    photon_eta_cutstring = "abs(photon_eta) < 1.4442"
elif options.phoeta == "endcap":
    photon_eta_cutstring = "1.566 < abs(photon_eta) && abs(photon_eta) < 2.5"
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

f_pu_weights = ROOT.TFile("/afs/cern.ch/user/a/amlevin/PileupWeights2016.root")

pu_weight_hist = f_pu_weights.Get("ratio")

#labels = { "z+jets" : {"color" : ROOT.kOrange, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wg/zjets.root", "xs" : 6025.2 }] }, "tt+jets" : {"color" : ROOT.kGreen+2, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wg/ttjets.root", "xs" : 831.76 } ] }, "wg+jets" : {"color": ROOT.kCyan, "samples" : [{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/wgjets.root", "xs" : 178.6}] } } 

#labels = { "z+jets" : {"color" : ROOT.kOrange, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wg/zjets.root", "xs" : 6025.2 }] }, "tt+jets" : {"color" : ROOT.kGreen+2, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wg/ttjets.root", "xs" : 831.76 } ] }, "w+jets" : {"color": ROOT.kCyan, "samples" : [{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/wjets.root", "xs" : 60430.0}] } } 

#labels = { "z+jets" : {"color" : ROOT.kOrange, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wg/zjets.root.bak", "xs" : 6025.2 }] }, "tt+jets" : {"color" : ROOT.kGreen+2, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wg/ttjets.root.bak", "xs" : 831.76 } ] }, "w+jets" : {"color": ROOT.kCyan, "samples" : [{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/wjets.root.bak", "xs" : 60430.0}] } } 

#labels = { "z+jets" : {"color" : ROOT.kOrange, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wg/zjets.root", "xs" : 4963.0 }] } } 

#labels = { "zg+jets" : {"color" : ROOT.kOrange, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wg/zgjets.root", "xs" : 47.46 } ] } } 

#labels = { "wg+jets" : {"color": ROOT.kCyan, "samples" : [{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/wgjets.root", "xs" : 178.6} ] }, "zg+jets" : {"color" : ROOT.kOrange, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wg/zgjets.root", "xs" : 47.46 } ] }, "ttg+jets" : {"color" : ROOT.kGreen+2, "samples" : [ {"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/ttgjets.root", "xs" : 3.795 } ] } } 

#labels = { "ttg+jets" : {"color" : ROOT.kGreen+2, "samples" : [ {'filename':  '/afs/cern.ch/work/a/amlevin/data/wg/tt2l2nu.root', 'xs' : 88.28 } ] } }


labels = { "tt2l2nu+jets" : {"color" : ROOT.kRed, "samples" : [{'filename':  '/afs/cern.ch/work/a/amlevin/data/wg/tt2l2nujets.root', 'xs' : 88.28, "non_fsr" : False , "e_to_p" : True, "fsr" : True } ] }, "ttsemi+jets" : {"color" : ROOT.kSpring, "samples" : [{'filename':  '/afs/cern.ch/work/a/amlevin/data/wg/ttsemijets.root', 'xs' : 365.4, "non_fsr" : False , "e_to_p" : True, "fsr" : True } ] }, "wg+jets" : {"color": ROOT.kCyan, "samples" : [{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/wgjets.root", "xs" : 178.6, "non_fsr" : True , "e_to_p" : True, "fsr" : True } ] }, "zg+jets" : {"color" : ROOT.kOrange, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wg/zgjets.root", "xs" : 47.46, "non_fsr" : True , "e_to_p" : True, "fsr" : True } ] }, "no label" : {"color" : None, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wg/zjets.root", "xs" : 4963.0, "non_fsr" : False , "e_to_p" : True, "fsr" : False  }] }, "ttg+jets" : {"color" : ROOT.kGreen+2, "samples" : [ {"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/ttgjets.root", "xs" : 3.795, "non_fsr" : True , "e_to_p" : True, "fsr" : True } ] } }

#labels = { "w+jets" : {"color": ROOT.kCyan, "samples" : [{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/wjets.root", "xs" : 60430.0}] } } 

variables = ["met","lepton_pt","lepton_eta","photon_pt","photon_eta","mlg","lepton_phi","photon_phi","njets","mt","npvs","drlg"]

histogram_templates = { "met" : ROOT.TH1F("met", "", 15 , 0., 300 ), "lepton_pt" : ROOT.TH1F('lepton_pt', '', 8, 20., 180 ), "lepton_eta" : ROOT.TH1F('lepton_eta', '', 10, -2.5, 2.5 ), "photon_pt" : ROOT.TH1F('photon_pt', '', 8, 20., 180 ), "photon_eta" : ROOT.TH1F('photon_eta', '', 10, -2.5, 2.5 ), "mlg" : ROOT.TH1F("mlg","",20,0,200) , "lepton_phi" : ROOT.TH1F("lepton_phi","",14,-3.5,3.5), "photon_phi" : ROOT.TH1F("photon_phi","",14,-3.5,3.5), "njets" : ROOT.TH1F("njets","",7,-0.5,6.5), "mt" : ROOT.TH1F("mt","",20,0,200), "npvs" : ROOT.TH1F("npvs","",51,-0.5,50.5), "drlg" : ROOT.TH1F("drlg","",60,0,6)} 

def nnlo_scale_factor(photon_eta,photon_pt):
    if abs(photon_eta) < 1.4442:
        if photon_pt < 17.5:
            return 1.147377962
        elif photon_pt < 22.5:
            return 1.178472286
        elif photon_pt < 27.5: 
            return 1.189477952
        elif photon_pt < 32.5:
            return 1.201940155
        elif photon_pt < 37.5:
            return 1.207208243 
        elif photon_pt < 42.5:
            return 1.223341402
        elif photon_pt < 50:
            return 1.236597991
        elif photon_pt < 75:
            return 1.251381290
        elif photon_pt < 105:
            return 1.276937808
        elif photon_pt < 310:
            return 1.313879553  
        elif photon_pt < 3500:
            return 1.342758655
        else:
            return 1.342758655 
    else:
        if photon_pt < 17.5:
            return 1.162640195
        elif photon_pt < 22.5:
            return 1.177382848
        elif photon_pt < 27.5:
            return 1.184751650
        elif photon_pt < 32.5:
            return 1.199851869
        elif photon_pt < 37.5:
            return 1.211113026
        elif photon_pt < 42.5:
            return 1.224040300
        elif photon_pt < 50:
            return 1.216979438
        elif photon_pt < 75:
            return 1.238354632
        elif photon_pt < 105:
            return 1.272419215
        elif photon_pt < 310:
            return 1.305852580
        elif photon_pt < 3500:
            return 1.296100451
        else:
            return 1.296100451
        


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

def pass_selection(tree, fake_lepton = False , fake_photon = False):
    if photon_eta_cutstring == "abs(photon_eta) < 1.4442":        
        if abs(tree.photon_eta) < 1.4442:
            pass_photon_eta = True
        else:
            pass_photon_eta = False
    elif photon_eta_cutstring == "1.566 < abs(photon_eta) && abs(photon_eta) < 2.5":        
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
        
#    if tree.npvs < 20:
#        pass_lepton_flavor = False
        
#    if not (tree.mlg > 61.2 and tree.mlg < 101.2):
#    if (tree.mlg > 61.2 and tree.mlg < 101.2):
#    if not (tree.mlg > 71.2 and tree.mlg < 111.2):
#    if (tree.mlg > 80.0 and tree.mlg < 100.0):

#    if True:    


    if lepton_abs_pdg_id == 11:    
        if not (tree.mlg > 60.0 and tree.mlg < 120.0):
            pass_mlg = True
        else:
            pass_mlg = False
    else:        
#        if not (tree.mlg > 60.0 and tree.mlg < 100.0):
        if True:
            pass_mlg = True
        else:
            pass_mlg = False

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

    if tree.met > 35:
#    if tree.met > 0:
        pass_met = True
    else:
        pass_met = False

    if tree.mt > 30:
#    if tree.mt > 0:
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
#    if tree.photon_pt > 25 and tree.photon_pt < 40:
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
xpositions = [0.65,0.65,0.65,0.65,0.45,0.45,0.45,0.45,0.25,0.25,0.25,0.25]
#ypositions = [0,1,2,3,4,5,0,1,2]
ypositions = [0,1,2,3,0,1,2,3,0,1,2,3]

style.GoodStyle().cd()

muon_fr_file = ROOT.TFile("/afs/cern.ch/user/a/amlevin/wg/muon_frs.root")
electron_fr_file = ROOT.TFile("/afs/cern.ch/user/a/amlevin/wg/electron_frs.root")

muon_fr_hist=muon_fr_file.Get("muon_frs")
electron_fr_hist=electron_fr_file.Get("electron_frs")

from array import array

photon_ptbins=array('d', [25,30,40,50,70,100,135,400])

fake_photon_event_weights_muon_barrel = [0.15329930173972148, 0.11323733203855359, 0.09117719159670651, 0.07375576546817071, 0.06366277563724594, 0.04515651675501986, 0.03477211224548741]

fake_photon_event_weights_electron_barrel = [0.1465633350156374, 0.10659503275136101, 0.08366693471349625, 0.06604377238571527, 0.0548938614256607, 0.045549075729087965, 0.0287425297394385]

#fake_photon_event_weights_electron_barrel = fake_photon_event_weights_muon_barrel

fake_photon_event_weights_muon_endcap = [0.2084973866790522, 0.17098260300188028, 0.13640944937286087, 0.10599407480309059, 0.09338109345797625, 0.06862344638393743, 0.059755163473597696]
#fake_photon_event_weights_electron_endcap = fake_photon_event_weights_muon_endcap

fake_photon_event_weights_electron_endcap = [0.19848704149567134, 0.15927761402175133, 0.1259625150980935, 0.1024070694786739, 0.07696444018690847, 0.06278537807297754, 0.002814088634222858]

fake_photon_event_weights_muon_barrel_hist=ROOT.TH1F("fake_photon_event_weights_muon_barrel_hist","fake_photon_event_weights_muon_barrel_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_event_weights_electron_barrel_hist=ROOT.TH1F("fake_photon_event_weights_electron_barrel_hist","fake_photon_event_weights_electron_barrel_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_event_weights_muon_endcap_hist=ROOT.TH1F("fake_photon_event_weights_muon_endcap_hist","fake_photon_event_weights_muon_endcap_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_event_weights_electron_endcap_hist=ROOT.TH1F("fake_photon_event_weights_electron_endcap_hist","fake_photon_event_weights_electron_endcap_hist",len(photon_ptbins)-1,photon_ptbins)

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

def leptonfakerate(lepton_abs_pdg_id,eta,pt,syst):
    if lepton_abs_pdg_id == 11:
        return electronfakerate(eta,pt,syst)
    elif lepton_abs_pdg_id == 13:
        return muonfakerate(eta,pt,syst)
    else:
        assert(0)

def subtractRealMCFromFakeEstimateFromData(mc_tree,data_fake_photon,data_fake_lepton,xs,n_weighted_events):

    #if sample["label"] == "tt+jets":
    #    return

    for i in range(mc_tree.GetEntries()):

        mc_tree.GetEntry(i)

        if sample["tree"].photon_gen_matching > 0:
#        if sample["tree"].photon_gen_matching > -1:
            pass_photon_gen_matching = True
        else:
            pass_photon_gen_matching = False

        if sample["tree"].is_lepton_real == '\x01':
            pass_is_lepton_real = True
        else:
            pass_is_lepton_real = False

        if (bool(sample["tree"].photon_gen_matching & int('010',2)) and sample["e_to_p"]) or (bool(sample["tree"].photon_gen_matching & int('1000',2)) and sample["fsr"]) or (bool(sample["tree"].photon_gen_matching & int('0100',2)) and sample["non_fsr"]) :
            pass_photon_gen_matching = True
        else:
            pass_photon_gen_matching = False    

        if not pass_photon_gen_matching or not pass_is_lepton_real or not pass_photon_gen_matching:
            continue

        if pass_selection(mc_tree,True,False):

            weight =-leptonfakerate(mc_tree.lepton_pdg_id,mc_tree.lepton_eta, mc_tree.lepton_pt,"nominal")* xs * 1000 * 36.15 / n_weighted_events

            if mc_tree.gen_weight < 0:
                weight = -weight

            for variable in variables:
                data_fake_lepton["hists"][variable].Fill(getVariable(variable,mc_tree),weight)  

        if pass_selection(mc_tree,False,True):

            weight = -photonfakerate(mc_tree.photon_eta, mc_tree.photon_pt,mc_tree.lepton_pdg_id, "nominal")* xs * 1000 * 36.15 / n_weighted_events

            if mc_tree.gen_weight < 0:
                weight = -weight

            for variable in variables:
                data_fake_photon["hists"][variable].Fill(getVariable(variable,mc_tree),weight)  
                


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

if lepton_name == "muon":
#    data_file = ROOT.TFile.Open("/afs/cern.ch/project/afs/var/ABS/recover/R.1935065321.08020759/data/wg/single_muon.root")
    data_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/single_muon.root")
elif lepton_name == "electron":
#    data_file = ROOT.TFile.Open("/afs/cern.ch/project/afs/var/ABS/recover/R.1935065321.08020759/data/wg/single_electron.root")
    data_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/single_electron.root")
else:
    assert(0)

for label in labels.keys():

    labels[label]["hists"] = {}

    for variable in variables:
        if labels[label]["color"] == None:
            continue

        labels[label]["hists"][variable] = histogram_templates[variable].Clone(label + " " + variable)
        labels[label]["hists"][variable].Sumw2()

    for sample in labels[label]["samples"]:
        sample["file"] = ROOT.TFile.Open(sample["filename"])
        sample["tree"] = sample["file"].Get("Events")
        sample["nweightedevents"] = sample["file"].Get("nWeightedEvents").GetBinContent(1)



data = {}
fake_photon = {}
fake_lepton = {}
double_fake = {}
electron_to_photon = {}

data["hists"] = {}
fake_photon["hists"] = {}
fake_lepton["hists"] = {}
double_fake["hists"] = {}
electron_to_photon["hists"] = {}

for variable in variables:
    data["hists"][variable] = histogram_templates[variable].Clone("data " + variable)
    fake_photon["hists"][variable] = histogram_templates[variable].Clone("fake photon " + variable)
    fake_lepton["hists"][variable] = histogram_templates[variable].Clone("fake electron " + variable)
    double_fake["hists"][variable] = histogram_templates[variable].Clone("double fake " + variable)
    electron_to_photon["hists"][variable] = histogram_templates[variable].Clone("electron to photon " + variable)
    data["hists"][variable].Sumw2()
    fake_photon["hists"][variable].Sumw2()
    fake_lepton["hists"][variable].Sumw2()
    double_fake["hists"][variable].Sumw2()
    electron_to_photon["hists"][variable].Sumw2()

data_events_tree = data_file.Get("Events")

c1 = ROOT.TCanvas("c1", "c1",5,50,500,500);

ROOT.gROOT.cd()

def fillHistogramMC(sample,histograms,e_to_p_histograms):

    for i in range(sample["tree"].GetEntries()):

        sample["tree"].GetEntry(i)

        if not pass_selection(sample["tree"]):
            continue

        if sample["tree"].is_lepton_real == '\x01':
            pass_is_lepton_real = True
        else:
            pass_is_lepton_real = False

        weight = sample["xs"]*1000*36.15/sample["nweightedevents"]

        weight *= pu_weight_hist.GetBinContent(pu_weight_hist.FindFixBin(sample["tree"].npu))
        
        weight *= eff_scale_factor.photon_efficiency_scale_factor(sample["tree"].photon_pt,sample["tree"].photon_eta)
         
        if lepton_abs_pdg_id == 11:
            weight *= eff_scale_factor.electron_efficiency_scale_factor(sample["tree"].lepton_pt,sample["tree"].lepton_eta)
        elif lepton_abs_pdg_id == 13:
            weight *= eff_scale_factor.muon_efficiency_scale_factor(sample["tree"].lepton_pt,sample["tree"].lepton_eta)
        else:
            assert(0)

        if sample["tree"].gen_weight < 0:
            weight = -weight

        if sample["filename"] == "/afs/cern.ch/work/a/amlevin/data/wg/wgjets.root":
            weight = weight * nnlo_scale_factor(sample["tree"].photon_pt,sample["tree"].photon_eta)

#        pass_is_lepton_real = True    

        if pass_is_lepton_real:

            if bool(sample["tree"].photon_gen_matching & int('0010',2)):
                if sample["e_to_p"]:
                    for variable in variables:
                        e_to_p_histograms[variable].Fill(getVariable(variable,sample["tree"]),weight)
            elif bool(sample["tree"].photon_gen_matching & int('1000',2)):
                if sample["fsr"]:
                    for variable in variables:
                        histograms[variable].Fill(getVariable(variable,sample["tree"]),weight)
            elif bool(sample["tree"].photon_gen_matching & int('0100',2)):
                if sample["non_fsr"]:
                    for variable in variables:
                        histograms[variable].Fill(getVariable(variable,sample["tree"]),weight)

    if len(variables) > 0  and not (sample["e_to_p"] and not sample["fsr"] and not sample["non_fsr"]):
        histograms[variables[0]].Print("all")


for i in range(data_events_tree.GetEntries()):
    data_events_tree.GetEntry(i)

#    if not pass_json(data_events_tree.run,data_events_tree.lumi):
#        continue

    if pass_selection(data_events_tree):
        for variable in variables:
            data["hists"][variable].Fill(getVariable(variable,data_events_tree))        


    if pass_selection(data_events_tree,True,False):

        weight = leptonfakerate(data_events_tree.lepton_pdg_id,data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")

        for variable in variables:
            fake_lepton["hists"][variable].Fill(getVariable(variable,data_events_tree),weight)

    if pass_selection(data_events_tree,False,True):

        weight = photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal")

        for variable in variables:
            fake_photon["hists"][variable].Fill(getVariable(variable,data_events_tree),weight)

    if pass_selection(data_events_tree,True,True):

        weight = leptonfakerate(data_events_tree.lepton_pdg_id,data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")*photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal")

        for variable in variables:
            
            double_fake["hists"][variable].Fill(getVariable(variable,data_events_tree),weight)
            fake_lepton["hists"][variable].Fill(getVariable(variable,data_events_tree),-weight)
            fake_photon["hists"][variable].Fill(getVariable(variable,data_events_tree),-weight)
        
for label in labels.keys():

    for sample in labels[label]["samples"]:
        fillHistogramMC(sample,labels[label]["hists"],electron_to_photon["hists"])
        if data_driven and (sample["fsr"] or sample["non_fsr"]):
            subtractRealMCFromFakeEstimateFromData(sample["tree"],fake_photon,fake_lepton,sample["xs"],sample["nweightedevents"])
        
    for variable in variables:    

        if labels[label]["color"] == None:
            continue

        labels[label]["hists"][variable].SetFillColor(labels[label]["color"])
        labels[label]["hists"][variable].SetFillStyle(1001)
        labels[label]["hists"][variable].SetLineColor(labels[label]["color"])
    
#subtractRealMCFromFakeEstimateFromData(mc_samples[0]["tree"],fake_photon_hist,fake_muon_hist,fake_lepton_hist,mc_samples[0]["xs"],mc_samples[0]["nweightedevents"])

for variable in variables:

    data["hists"][variable].Print("all")

    data["hists"][variable].SetMarkerStyle(ROOT.kFullCircle)
    data["hists"][variable].SetLineWidth(3)
    data["hists"][variable].SetLineColor(ROOT.kBlack)

    fake_photon["hists"][variable].SetFillColor(ROOT.kGray+1)
    fake_lepton["hists"][variable].SetFillColor(ROOT.kAzure-1)
    double_fake["hists"][variable].SetFillColor(ROOT.kMagenta)
    electron_to_photon["hists"][variable].SetFillColor(ROOT.kYellow)

    fake_photon["hists"][variable].SetLineColor(ROOT.kGray+1)
    fake_lepton["hists"][variable].SetLineColor(ROOT.kAzure-1)
    double_fake["hists"][variable].SetLineColor(ROOT.kMagenta)
    electron_to_photon["hists"][variable].SetLineColor(ROOT.kYellow)
    

    fake_photon["hists"][variable].SetFillStyle(1001)
    fake_lepton["hists"][variable].SetFillStyle(1001)
    double_fake["hists"][variable].SetFillStyle(1001)
    electron_to_photon["hists"][variable].SetFillStyle(1001)

    s=str(options.lumi)+" fb^{-1} (13 TeV)"
    lumilabel = ROOT.TLatex (0.95, 0.93, s)
    lumilabel.SetNDC ()
    lumilabel.SetTextAlign (30)
    lumilabel.SetTextFont (42)
    lumilabel.SetTextSize (0.040)

#
    hsum = data["hists"][variable].Clone()
    hsum.Scale(0.0)

    hstack = ROOT.THStack()

    if lepton_abs_pdg_id == 11: 
        hsum.Add(electron_to_photon["hists"][variable])
        hstack.Add(electron_to_photon["hists"][variable])

    for label in labels.keys():
        if labels[label]["color"] == None:
            continue
        hsum.Add(labels[label]["hists"][variable])
        hstack.Add(labels[label]["hists"][variable])

    if data_driven:
        hsum.Add(fake_lepton["hists"][variable])
        hsum.Add(fake_photon["hists"][variable])
        hsum.Add(double_fake["hists"][variable])

    if data_driven:
        hstack.Add(fake_lepton["hists"][variable])
        hstack.Add(fake_photon["hists"][variable])
        hstack.Add(double_fake["hists"][variable])


    if data["hists"][variable].GetMaximum() < hsum.GetMaximum():
        data["hists"][variable].SetMaximum(hsum.GetMaximum()*1.55)
    else:
        data["hists"][variable].SetMaximum(data["hists"][variable].GetMaximum()*1.55)
        

    data["hists"][variable].SetMinimum(0)
    hstack.SetMinimum(0)
    hsum.SetMinimum(0)

    data["hists"][variable].Draw("")

    hstack.Draw("hist same")

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
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,data["hists"][variable],"data","lp")

    if data_driven :
        j=j+1
        if lepton_name == "muon":
            draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,fake_lepton["hists"][variable],"fake muon","f")
        elif lepton_name == "electron":
            draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,fake_lepton["hists"][variable],"fake electron","f")
        else:
            assert(0)
        j=j+1
        draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,fake_photon["hists"][variable],"fake photon","f")
        j=j+1
        draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,double_fake["hists"][variable],"double fake","f")

    if lepton_abs_pdg_id == 11:
        j=j+1
        draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,electron_to_photon["hists"][variable],"e->g","f")

    for label in labels.keys():
        if labels[label]["color"] == None:
            continue
        j=j+1    
        draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,labels[label]["hists"][variable],label,"f")
    

#set_axis_fonts(hstack,"x","m_{ll} (GeV)")
#set_axis_fonts(hstack,"x","|\Delta \eta_{jj}|")
    set_axis_fonts(data["hists"][variable],"x",getXaxisLabel(variable))
    set_axis_fonts(hstack,"x",options.xaxislabel)
#set_axis_fonts(hstack,"x","pt_{l}^{max} (GeV)")
#set_axis_fonts(data_hist,"y","Events / bin")
#set_axis_fonts(hstack,"y","Events / bin")

    gstat = ROOT.TGraphAsymmErrors(hsum);

    for i in range(0,gstat.GetN()):
        gstat.SetPointEYlow (i, hsum.GetBinError(i+1));
        gstat.SetPointEYhigh(i, hsum.GetBinError(i+1));

    gstat.SetFillColor(12);
    gstat.SetFillStyle(3345);
    gstat.SetMarkerSize(0);
    gstat.SetLineWidth(0);
    gstat.SetLineColor(ROOT.kWhite);
    gstat.Draw("E2same");

    data["hists"][variable].Draw("same")

    c1.Update()
    c1.ForceUpdate()
    c1.Modified()

    c1.SaveAs(options.outputdir + "/" + variable + ".png")

#    if variable == "mlg":
#
#        ndata = data["hists"]["mlg"].GetBinContent(data["hists"]["mlg"].GetXaxis().FindFixBin(85.0))+ data["hists"]["mlg"].GetBinContent(data["hists"]["mlg"].GetXaxis().FindFixBin(95.0))

#        nzjets = labels["z+jets"]["hists"]["mlg"].GetBinContent(labels["z+jets"]["hists"]["mlg"].GetXaxis().FindFixBin(85.0))+ labels["z+jets"]["hists"]["mlg"].GetBinContent(labels["z+jets"]["hists"]["mlg"].GetXaxis().FindFixBin(95.0))

#        nprediction =hsum.GetBinContent(hsum.GetXaxis().FindFixBin(85.0))+ hsum.GetBinContent(hsum.GetXaxis().FindFixBin(95.0))

#        print ndata

#        print nzjets

#        print nprediction

#        print (ndata - nprediction + nzjets)/nzjets

