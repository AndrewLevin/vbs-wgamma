data_driven = True

def fillHistogram(hist,value,weight=1):
    if options.overflow:
        if value > hist.GetBinLowEdge(hist.GetNbinsX()):
            value = hist.GetBinCenter(hist.GetNbinsX())
    hist.Fill(value,weight)

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
parser.add_option('--overflow',dest='overflow',action='store_true',default=False)
parser.add_option('--ewdim6',dest='ewdim6',action='store_true',default=False)
parser.add_option('--ewdim6_scaling_only',dest='ewdim6_scaling_only',action='store_true',default=False)

parser.add_option('--blinding_cut',dest='blinding_cut',default=1000000)
parser.add_option('--lumi',dest='lumi')
parser.add_option('--variable',dest='variable')
parser.add_option('--xaxislabel',dest='xaxislabel',default='m_{jj} (GeV)')

parser.add_option('-i',dest='inputfile')
parser.add_option('-o',dest='outputdir',default="/eos/user/a/amlevin/www/tmp/")

(options,args) = parser.parse_args()

blinding_cut = float(options.blinding_cut)

if options.ewdim6_scaling_only and not options.ewdim6:
    assert(0)

if options.lep == "muon":
    lepton_name = "muon"
elif options.lep == "electron":
    lepton_name = "electron"
elif options.lep == "both":
    lepton_name = "both"
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



labels = { "tt2l2nu+jets" : {"syst-pdf" : False, "syst-scale" : False, "color" : ROOT.kRed, "samples" : [{'filename':  '/afs/cern.ch/work/a/amlevin/data/wg/2016/tt2l2nujets.root', 'xs' : 88.28, "non_fsr" : False , "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True } ] }, "ttsemi+jets" : {"syst-pdf" : False, "syst-scale" : False, "color" : ROOT.kSpring, "samples" : [{'filename':  '/afs/cern.ch/work/a/amlevin/data/wg/2016/ttsemijets.root', 'xs' : 365.4, "non_fsr" : False , "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True } ] }, "wg+jets" : {"syst-pdf": True, "syst-scale": True, "color": ROOT.kCyan, "samples" : [{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/wgjets.root.bak", "xs" : 178.6, "non_fsr" : True , "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True } ] }, "zg+jets" : {"syst-pdf" : False, "syst-scale" : False, "color" : ROOT.kOrange, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wg/2016/zglowmlljets.root", "xs" : 96.75, "non_fsr" : True , "e_to_p" : False, "fsr" : True, "e_to_p_for_fake" : True } ] }, "no label" : {"syst-pdf" : False, "syst-scale" : False, "color" : None, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wg/2016/zjets.root", "xs" : 4963.0, "non_fsr" : False , "e_to_p" : False, "fsr" : False, "e_to_p_for_fake" : True }] }, "ttg+jets" : {"syst-pdf" : False, "syst-scale" : False,  "color" : ROOT.kGreen+2, "samples" : [ {"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/ttgjets.root", "xs" : 3.795, "non_fsr" : True , "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True } ] } }

#labels = { "tt2l2nu+jets" : {"syst-pdf" : False, "syst-scale" : False, "color" : ROOT.kRed, "samples" : [{'filename':  '/afs/cern.ch/work/a/amlevin/data/wg/2016/tt2l2nujets.root', 'xs' : 88.28, "non_fsr" : False , "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True } ] }, "ttsemi+jets" : {"syst-pdf" : False, "syst-scale" : False, "color" : ROOT.kSpring, "samples" : [{'filename':  '/afs/cern.ch/work/a/amlevin/data/wg/2016/ttsemijets.root', 'xs' : 365.4, "non_fsr" : False , "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True } ] }, "wg+jets" : {"syst-pdf": True, "syst-scale": True, "color": ROOT.kCyan, "samples" : [{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/wgjetsewdim6.root", "xs" : 178.6, "non_fsr" : True , "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True } ] }, "zg+jets" : {"syst-pdf" : False, "syst-scale" : False, "color" : ROOT.kOrange, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wg/2016/zglowmlljets.root", "xs" : 96.75, "non_fsr" : True , "e_to_p" : False, "fsr" : True, "e_to_p_for_fake" : True } ] }, "no label" : {"syst-pdf" : False, "syst-scale" : False, "color" : None, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wg/2016/zjets.root", "xs" : 4963.0, "non_fsr" : False , "e_to_p" : False, "fsr" : False, "e_to_p_for_fake" : True }] }, "ttg+jets" : {"syst-pdf" : False, "syst-scale" : False,  "color" : ROOT.kGreen+2, "samples" : [ {"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/ttgjets.root", "xs" : 3.795, "non_fsr" : True , "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True } ] } }



#the first variable is for the ewdim6 analysis
variables = ["photon_pt","dphilg","met","lepton_pt","lepton_eta","photon_pt","photon_eta","mlg","lepton_phi","photon_phi","njets","mt","npvs","drlg"]

histogram_templates = [ROOT.TH1F('', '', 5, 100., 600 ),ROOT.TH1F('','',8,pi/2,pi), ROOT.TH1F("met", "", 15 , 0., 300 ), ROOT.TH1F('lepton_pt', '', 8, 20., 180 ), ROOT.TH1F('lepton_eta', '', 10, -2.5, 2.5 ), ROOT.TH1F('photon_pt', '', 3, 300., 600 ), ROOT.TH1F('photon_eta', '', 10, -2.5, 2.5 ), ROOT.TH1F("mlg","",100,0,200) , ROOT.TH1F("lepton_phi","",14,-3.5,3.5), ROOT.TH1F("photon_phi","",14,-3.5,3.5), ROOT.TH1F("njets","",7,-0.5,6.5), ROOT.TH1F("mt","",20,0,200), ROOT.TH1F("npvs","",51,-0.5,50.5), ROOT.TH1F("drlg","",60,0,6)] 

assert(len(variables) == len(histogram_templates))

mlg_index = 7

#ewdim6_filename = "/afs/cern.ch/work/a/amlevin/data/wg/2016/wgjetsewdim6.root.bak"
ewdim6_filename = "/afs/cern.ch/work/a/amlevin/data/wg/2016/wgjetsewdim6.root"

ewdim6_file = ROOT.TFile(ewdim6_filename)

ewdim6_tree = ewdim6_file.Get("Events")

#ewdim6_xs = 5.519
ewdim6_xs = 4.318

ewdim6_nweightedevents = ewdim6_file.Get("nWeightedEvents").GetBinContent(1)

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
    elif varname == "dphilg":
        return deltaPhi(tree.lepton_phi,tree.photon_phi)
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
    elif varname == "dphilg":
        return "#Delta #phi(l,g)"
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


    if lepton_name == "electron":    
#        if not (tree.mlg > 60.0 and tree.mlg < 120.0):
        if True:
            pass_mlg = True
        else:
            pass_mlg = False
    elif lepton_name == "muon":        
#       if not (tree.mlg > 60.0 and tree.mlg < 100.0):
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

#    if tree.met > 35:
    if tree.met > 70:
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
            
    if tree.photon_pt > 25:
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

muon_fr_file = ROOT.TFile("/afs/cern.ch/user/a/amlevin/wg/2016/muon_frs_data_subtract_wjets_zjets.root")
electron_fr_file = ROOT.TFile("/afs/cern.ch/user/a/amlevin/wg/2016/electron_frs_data_subtract_wjets_zjets.root")

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

fake_photon_event_weights_muon_endcap_MC = [0.1806019035114771, 0.15311103027403922, 0.15233748095550786, 0.10218335724427745, 0.08042243448043745, 0.055938368551824685, 0.050546201223890336]
fake_photon_event_weights_electron_endcap_MC = [0.18332860514318766, 0.1616009980967483, 0.12983990825613295, 0.0981657727656512, 0.060477729032748916, 0.07938848306929441, 0.06301416429185958]
fake_photon_event_weights_electron_barrel_MC = [0.1302818647040204, 0.0965989567886929, 0.07417185775597872, 0.06789639958741521, 0.058415672189706405, 0.04557617137218626, 0.03559569695093213]
fake_photon_event_weights_muon_barrel_MC = [0.144381599700443, 0.10333082134361173, 0.09148841286300782, 0.06344235311379792, 0.05953962237263142, 0.06388880919077376, 0.04631086033174329]

fake_photon_event_weights_muon_barrel_hist=ROOT.TH1F("fake_photon_event_weights_muon_barrel_hist","fake_photon_event_weights_muon_barrel_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_event_weights_electron_barrel_hist=ROOT.TH1F("fake_photon_event_weights_electron_barrel_hist","fake_photon_event_weights_electron_barrel_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_event_weights_muon_endcap_hist=ROOT.TH1F("fake_photon_event_weights_muon_endcap_hist","fake_photon_event_weights_muon_endcap_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_event_weights_electron_endcap_hist=ROOT.TH1F("fake_photon_event_weights_electron_endcap_hist","fake_photon_event_weights_electron_endcap_hist",len(photon_ptbins)-1,photon_ptbins)

fake_photon_event_weights_muon_barrel_MC_hist=ROOT.TH1F("fake_photon_event_weights_muon_barrel_hist","fake_photon_event_weights_muon_barrel_MC_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_event_weights_electron_barrel_MC_hist=ROOT.TH1F("fake_photon_event_weights_electron_barrel_hist","fake_photon_event_weights_electron_barrel_MC_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_event_weights_muon_endcap_MC_hist=ROOT.TH1F("fake_photon_event_weights_muon_endcap_hist","fake_photon_event_weights_muon_endcap_MC_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_event_weights_electron_endcap_MC_hist=ROOT.TH1F("fake_photon_event_weights_electron_endcap_hist","fake_photon_event_weights_electron_endcap_MC_hist",len(photon_ptbins)-1,photon_ptbins)


for i in range(fake_photon_event_weights_muon_barrel_hist.GetNbinsX()):
    fake_photon_event_weights_muon_barrel_hist.SetBinContent(i+1,fake_photon_event_weights_muon_barrel[i])
    fake_photon_event_weights_muon_barrel_MC_hist.SetBinContent(i+1,fake_photon_event_weights_muon_barrel_MC[i])

for i in range(fake_photon_event_weights_electron_barrel_hist.GetNbinsX()):
    fake_photon_event_weights_electron_barrel_hist.SetBinContent(i+1,fake_photon_event_weights_electron_barrel[i])
    fake_photon_event_weights_electron_barrel_MC_hist.SetBinContent(i+1,fake_photon_event_weights_electron_barrel_MC[i])

for i in range(fake_photon_event_weights_muon_endcap_hist.GetNbinsX()):
    fake_photon_event_weights_muon_endcap_hist.SetBinContent(i+1,fake_photon_event_weights_muon_endcap[i])
    fake_photon_event_weights_muon_endcap_MC_hist.SetBinContent(i+1,fake_photon_event_weights_muon_endcap_MC[i])

for i in range(fake_photon_event_weights_electron_endcap_hist.GetNbinsX()):
    fake_photon_event_weights_electron_endcap_hist.SetBinContent(i+1,fake_photon_event_weights_electron_endcap[i])
    fake_photon_event_weights_electron_endcap_MC_hist.SetBinContent(i+1,fake_photon_event_weights_electron_endcap_MC[i])

def photonfakerate(eta,pt,lepton_pdg_id,for_syst=False):

    if abs(lepton_pdg_id) == 11:
        if abs(eta) < 1.4442:
            myeta  = min(abs(eta),2.4999)
            mypt   = min(pt,399.999)

            if not for_syst:
                fr = fake_photon_event_weights_electron_barrel_hist.GetBinContent(fake_photon_event_weights_electron_barrel_hist.GetXaxis().FindFixBin(mypt))
            else:    
                fr = fake_photon_event_weights_electron_barrel_MC_hist.GetBinContent(fake_photon_event_weights_electron_barrel_hist.GetXaxis().FindFixBin(mypt))

            return fr

        elif 1.566 < abs(eta) and abs(eta) < 2.5:
            myeta  = min(abs(eta),2.4999)
            mypt   = min(pt,399.999)

            if not for_syst:
                fr = fake_photon_event_weights_electron_endcap_hist.GetBinContent(fake_photon_event_weights_electron_endcap_hist.GetXaxis().FindFixBin(mypt))
            else:
                fr = fake_photon_event_weights_electron_endcap_MC_hist.GetBinContent(fake_photon_event_weights_electron_endcap_MC_hist.GetXaxis().FindFixBin(mypt))

            return fr

        else:

            assert(0)
    elif abs(lepton_pdg_id) == 13:
        if abs(eta) < 1.4442:
            myeta  = min(abs(eta),2.4999)
            mypt   = min(pt,399.999)

            if not for_syst:
                fr = fake_photon_event_weights_muon_barrel_hist.GetBinContent(fake_photon_event_weights_muon_barrel_hist.GetXaxis().FindFixBin(mypt))
            else:    
                fr = fake_photon_event_weights_muon_barrel_MC_hist.GetBinContent(fake_photon_event_weights_muon_barrel_MC_hist.GetXaxis().FindFixBin(mypt))

            return fr

        elif 1.566 < abs(eta) and abs(eta) < 2.5:
            myeta  = min(abs(eta),2.4999)
            mypt   = min(pt,399.999)

            if not for_syst:
                fr = fake_photon_event_weights_muon_endcap_hist.GetBinContent(fake_photon_event_weights_muon_endcap_hist.GetXaxis().FindFixBin(mypt))
            else:    
                fr = fake_photon_event_weights_muon_endcap_MC_hist.GetBinContent(fake_photon_event_weights_muon_endcap_MC_hist.GetXaxis().FindFixBin(mypt))

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
    data_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/2016/single_muon.root")
elif lepton_name == "electron":
#    data_file = ROOT.TFile.Open("/afs/cern.ch/project/afs/var/ABS/recover/R.1935065321.08020759/data/wg/single_electron.root")
    data_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/2016/single_electron.root")
elif lepton_name == "both":
    data_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/2016/single_lepton.root")
else:
    assert(0)

for label in labels.keys():

    labels[label]["hists"] = {}

    labels[label]["hists-electron-id-sf-variation"] = {}
    labels[label]["hists-electron-reco-sf-variation"] = {}
    labels[label]["hists-muon-id-sf-variation"] = {}
    labels[label]["hists-muon-iso-sf-variation"] = {}
    labels[label]["hists-photon-id-sf-variation"] = {}

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
            

    for sample in labels[label]["samples"]:
        sample["file"] = ROOT.TFile.Open(sample["filename"])
        sample["tree"] = sample["file"].Get("Events")
        sample["nweightedevents"] = sample["file"].Get("nWeightedEvents").GetBinContent(1)

data = {}
fake_photon = {}
fake_photon_syst = {}
fake_lepton = {}
double_fake = {}
electron_to_photon = {}

data["hists"] = []
fake_photon["hists"] = []
fake_photon_syst["hists"] = []
fake_lepton["hists"] = []
double_fake["hists"] = []
electron_to_photon["hists"] = []

for i in range(len(variables)):
    data["hists"].append(histogram_templates[i].Clone("data " + variables[i]))
    fake_photon["hists"].append(histogram_templates[i].Clone("fake photon " + variables[i]))
    fake_photon_syst["hists"].append(histogram_templates[i].Clone("fake photon sys " + variables[i]))
    fake_lepton["hists"].append(histogram_templates[i].Clone("fake electron " + variables[i]))
    double_fake["hists"].append(histogram_templates[i].Clone("double fake " + variables[i]))
    electron_to_photon["hists"].append(histogram_templates[i].Clone("electron to photon " + variables[i]))

for i in range(len(variables)):
    data["hists"][i].Sumw2()
    fake_photon["hists"][i].Sumw2()
    fake_photon_syst["hists"][i].Sumw2()
    fake_lepton["hists"][i].Sumw2()
    double_fake["hists"][i].Sumw2()
    electron_to_photon["hists"][i].Sumw2()

data_events_tree = data_file.Get("Events")

c1 = ROOT.TCanvas("c1", "c1",5,50,500,500);

ROOT.gROOT.cd()

def fillHistogramMC(label,sample):

    for i in range(sample["tree"].GetEntries()):

        sample["tree"].GetEntry(i)

        if sample["tree"].is_lepton_real == '\x01':
            pass_is_lepton_real = True
        else:
            pass_is_lepton_real = False

        if (bool(sample["tree"].photon_gen_matching & int('010',2)) and sample["e_to_p"]) or (bool(sample["tree"].photon_gen_matching & int('1000',2)) and sample["fsr"]) or (bool(sample["tree"].photon_gen_matching & int('0100',2)) and sample["non_fsr"]) :
            pass_photon_gen_matching = True
        else:
            pass_photon_gen_matching = False    

        if (bool(sample["tree"].photon_gen_matching & int('010',2)) and sample["e_to_p_for_fake"]) or (bool(sample["tree"].photon_gen_matching & int('1000',2)) and sample["fsr"]) or (bool(sample["tree"].photon_gen_matching & int('0100',2)) and sample["non_fsr"]) :
            pass_photon_gen_matching_for_fake = True
        else:
            pass_photon_gen_matching_for_fake = False    

        if pass_photon_gen_matching_for_fake and pass_is_lepton_real:
            if pass_selection(sample["tree"],options.phoeta,True,False):

                weight =-leptonfakerate(sample["tree"].lepton_pdg_id,sample["tree"].lepton_eta, sample["tree"].lepton_pt,"nominal")* sample["xs"] * 1000 * 35.9 / sample["nweightedevents"]

                if sample["tree"].gen_weight < 0:
                    weight = -weight

                for j in range(len(variables)):
                    fillHistogram(fake_lepton["hists"][j],getVariable(variables[j],sample["tree"]),weight)

            if pass_selection(sample["tree"],options.phoeta,False,True):

                weight = -photonfakerate(sample["tree"].photon_eta, sample["tree"].photon_pt,sample["tree"].lepton_pdg_id, "nominal")* sample["xs"] * 1000 * 35.9 / sample["nweightedevents"]
                weight_fake_photon_syst = -photonfakerate(sample["tree"].photon_eta, sample["tree"].photon_pt,sample["tree"].lepton_pdg_id, True)* sample["xs"] * 1000 * 35.9 / sample["nweightedevents"]

                if sample["tree"].gen_weight < 0:
                    weight = -weight
                    weight_fake_photon_syst = -weight_fake_photon_syst

                for j in range(len(variables)):
                    fillHistogram(fake_photon["hists"][j],getVariable(variables[j],sample["tree"]),weight)
                    fillHistogram(fake_photon_syst["hists"][j],getVariable(variables[j],sample["tree"]),weight_fake_photon_syst)

        if not pass_selection(sample["tree"],options.phoeta,False,False):
            continue

        weight = sample["xs"]*1000*35.9/sample["nweightedevents"]

#        if sample["filename"] == "/afs/cern.ch/work/a/amlevin/data/wg/wgjetsewdim6.root":
#            weight *= sample["tree"].LHEWeight_rwgt_3

        weight *= pu_weight_hist.GetBinContent(pu_weight_hist.FindFixBin(sample["tree"].npu))

        weight_photon_id_sf_variation = weight * eff_scale_factor.photon_efficiency_scale_factor(sample["tree"].photon_pt,sample["tree"].photon_eta,True)
        weight *= eff_scale_factor.photon_efficiency_scale_factor(sample["tree"].photon_pt,sample["tree"].photon_eta)

         
        if sample["tree"].lepton_pdg_id == 11:
            weight_electron_id_sf_variation = weight * eff_scale_factor.electron_efficiency_scale_factor(sample["tree"].lepton_pt,sample["tree"].lepton_eta,True,False)
            weight_electron_reco_sf_variation = weight * eff_scale_factor.electron_efficiency_scale_factor(sample["tree"].lepton_pt,sample["tree"].lepton_eta,False,True)
            weight *= eff_scale_factor.electron_efficiency_scale_factor(sample["tree"].lepton_pt,sample["tree"].lepton_eta)
            weight_photon_id_sf_variation *= eff_scale_factor.electron_efficiency_scale_factor(sample["tree"].lepton_pt,sample["tree"].lepton_eta)
            weight_muon_id_sf_variation = weight
            weight_muon_iso_sf_variation = weight
        elif sample["tree"].lepton_pdg_id == 13:
            weight_muon_id_sf_variation = weight * eff_scale_factor.muon_efficiency_scale_factor(sample["tree"].lepton_pt,sample["tree"].lepton_eta,False,True)
            weight_muon_iso_sf_variation = weight * eff_scale_factor.muon_efficiency_scale_factor(sample["tree"].lepton_pt,sample["tree"].lepton_eta,True,False)
            weight *= eff_scale_factor.muon_efficiency_scale_factor(sample["tree"].lepton_pt,sample["tree"].lepton_eta)
            weight_photon_id_sf_variation *= eff_scale_factor.muon_efficiency_scale_factor(sample["tree"].lepton_pt,sample["tree"].lepton_eta)
            weight_electron_id_sf_variation = weight
            weight_electron_reco_sf_variation = weight
        else:
            assert(0)

        if sample["tree"].gen_weight < 0:
            weight = -weight
            weight_electron_id_sf_variation = -weight_electron_id_sf_variation
            weight_electron_reco_sf_variation = -weight_electron_reco_sf_variation
            weight_muon_id_sf_variation = -weight_muon_id_sf_variation
            weight_muon_iso_sf_variation = -weight_muon_iso_sf_variation
            weight_photon_id_sf_variation = -weight_photon_id_sf_variation

#        if sample["filename"] == "/afs/cern.ch/work/a/amlevin/data/wg/wgjets.root":
#            weight = weight * nnlo_scale_factor(sample["tree"].photon_pt,sample["tree"].photon_eta)

#        pass_is_lepton_real = True    

        if pass_is_lepton_real:

            if bool(sample["tree"].photon_gen_matching & int('0010',2)):
                if sample["e_to_p"]:
                    for j in range(len(variables)):
                        electron_to_photon["hists"][j].Fill(getVariable(variables[j],sample["tree"]),weight)
            elif bool(sample["tree"].photon_gen_matching & int('1000',2)):
                if sample["fsr"]:
                    for j in range(len(variables)):
                        fillHistogram(label["hists"][j],getVariable(variables[j],sample["tree"]),weight)
                        fillHistogram(label["hists-electron-id-sf-variation"][j],getVariable(variables[j],sample["tree"]),weight_electron_id_sf_variation)
                        fillHistogram(label["hists-electron-reco-sf-variation"][j],getVariable(variables[j],sample["tree"]),weight_electron_reco_sf_variation)
                        fillHistogram(label["hists-muon-id-sf-variation"][j],getVariable(variables[j],sample["tree"]),weight_muon_id_sf_variation)
                        fillHistogram(label["hists-muon-iso-sf-variation"][j],getVariable(variables[j],sample["tree"]),weight_muon_iso_sf_variation)
                        fillHistogram(label["hists-photon-id-sf-variation"][j],getVariable(variables[j],sample["tree"]),weight_photon_id_sf_variation)
                        if label["syst-pdf"]:
                            for k in range(0,102):
                                fillHistogram(label["hists-pdf-variation"+str(k)][j],getVariable(variables[j],sample["tree"]),weight*sample["tree"].LHEPdfWeight[k+1])
                        if label["syst-scale"]:
                            for k in range(0,8):
                                fillHistogram(label["hists-scale-variation"+str(k)][j],getVariable(variables[j],sample["tree"]),weight*sample["tree"].LHEScaleWeight[k]*2)
                        
            elif bool(sample["tree"].photon_gen_matching & int('0100',2)):
                if sample["non_fsr"]:
                    for j in range(len(variables)):
                        fillHistogram(label["hists"][j],getVariable(variables[j],sample["tree"]),weight)
                        fillHistogram(label["hists-electron-id-sf-variation"][j],getVariable(variables[j],sample["tree"]),weight_electron_id_sf_variation)
                        fillHistogram(label["hists-electron-reco-sf-variation"][j],getVariable(variables[j],sample["tree"]),weight_electron_reco_sf_variation)
                        fillHistogram(label["hists-muon-id-sf-variation"][j],getVariable(variables[j],sample["tree"]),weight_muon_id_sf_variation)
                        fillHistogram(label["hists-muon-iso-sf-variation"][j],getVariable(variables[j],sample["tree"]),weight_muon_iso_sf_variation)
                        fillHistogram(label["hists-photon-id-sf-variation"][j],getVariable(variables[j],sample["tree"]),weight_photon_id_sf_variation)
                        if label["syst-pdf"]:
                            for k in range(0,102):
                                fillHistogram(label["hists-pdf-variation"+str(k)][j],getVariable(variables[j],sample["tree"]),weight*sample["tree"].LHEPdfWeight[k+1])
                        if label["syst-scale"]:
                            for k in range(0,8):
                                fillHistogram(label["hists-scale-variation"+str(k)][j],getVariable(variables[j],sample["tree"]),weight*sample["tree"].LHEScaleWeight[k]*2)

#    if len(variables) > 0  and not (sample["e_to_p"] and not sample["fsr"] and not sample["non_fsr"]):
#        label["hists"][variables[0]].Print("all")

if options.ewdim6:

    sm_lhe_weight = 373

    sm_lhe_weight_hist = ROOT.TH1F('', '', 5, 100., 600 )

    sm_hist = ROOT.TH1F('', '', 5, 100., 600 )

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
        cwww_hists.append(ROOT.TH1F('', '', 5, 100., 600 ))

    for i in range(0,len(cw_reweights)):
        cw_hists.append(ROOT.TH1F('', '', 5, 100., 600 ))

    for i in range(0,len(cb_reweights)):
        cb_hists.append(ROOT.TH1F('', '', 5, 100., 600 ))

    for i in range(0,len(cpwww_reweights)):
        cpwww_hists.append(ROOT.TH1F('', '', 5, 100., 600 ))

    for i in range(0,len(cpw_reweights)):
        cpw_hists.append(ROOT.TH1F('', '', 5, 100., 600 ))

    for i in range(labels["wg+jets"]["samples"][0]["tree"].GetEntries()):
        labels["wg+jets"]["samples"][0]["tree"].GetEntry(i)

        w = labels["wg+jets"]["samples"][0]["xs"]*1000*35.9/labels["wg+jets"]["samples"][0]["nweightedevents"]

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

        if pass_selection(labels["wg+jets"]["samples"][0]["tree"],options.phoeta):
            fillHistogram(sm_hist,getVariable(variables[0],labels["wg+jets"]["samples"][0]["tree"]),w)

    sm_hist.Print("all")

    for i in range(ewdim6_tree.GetEntries()):
        ewdim6_tree.GetEntry(i)

        w = ewdim6_xs*1000*35.9/ewdim6_nweightedevents

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

        if pass_selection(ewdim6_tree,options.phoeta):
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

    for i in range(1,cwww_hists[0].GetNbinsX()+1):
        cwww_scaling_hist=ROOT.TH1D("ewdim6_scaling_bin_"+str(i),"ewdim6_scaling_bin_"+str(i),len(cwww_coefficients),cwww_hist_min,cwww_hist_max);

        for j in range(0,len(cwww_hists)):
            assert(sm_lhe_weight_hist.GetBinContent(i) > 0)

            cwww_scaling_hist.SetBinContent(cwww_scaling_hist.GetXaxis().FindFixBin(cwww_coefficients[j]), cwww_hists[j].GetBinContent(i)/sm_lhe_weight_hist.GetBinContent(i))
        
        cwww_scaling_outfile.cd()
        cwww_scaling_hist.Write()

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

for i in range(data_events_tree.GetEntries()):
    data_events_tree.GetEntry(i)

#    if not pass_json(data_events_tree.run,data_events_tree.lumi):
#        continue

    if pass_selection(data_events_tree,options.phoeta):
        for j in range(len(variables)):
            fillHistogram(data["hists"][j],getVariable(variables[j],data_events_tree))

    if pass_selection(data_events_tree,options.phoeta,True,False):

        weight = leptonfakerate(data_events_tree.lepton_pdg_id,data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")

        if data_events_tree.photon_pt > blinding_cut:
            continue

        for j in range(len(variables)):
            fillHistogram(fake_lepton["hists"][j],getVariable(variables[j],data_events_tree),weight)

    if pass_selection(data_events_tree,options.phoeta,False,True):

        weight = photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id )
        weight_fake_photon_syst = photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, True)

        for j in range(len(variables)):
            fillHistogram(fake_photon["hists"][j],getVariable(variables[j],data_events_tree),weight)
            fillHistogram(fake_photon_syst["hists"][j],getVariable(variables[j],data_events_tree),weight_fake_photon_syst)
    if pass_selection(data_events_tree,options.phoeta,True,True):

        weight = leptonfakerate(data_events_tree.lepton_pdg_id,data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")*photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id)
        weight_fake_photon_syst = leptonfakerate(data_events_tree.lepton_pdg_id,data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")*photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, True)

        for j in range(len(variables)):
            fillHistogram(double_fake["hists"][j],getVariable(variables[j],data_events_tree),weight)
            fillHistogram(fake_lepton["hists"][j],getVariable(variables[j],data_events_tree),-weight)
            fillHistogram(fake_photon["hists"][j],getVariable(variables[j],data_events_tree),-weight)
            fillHistogram(fake_photon_syst["hists"][j],getVariable(variables[j],data_events_tree),-weight_fake_photon_syst)

for label in labels.keys():

    for sample in labels[label]["samples"]:
        fillHistogramMC(labels[label],sample)

    for i in range(len(variables)):    

        if labels[label]["color"] == None:
            continue

        labels[label]["hists"][i].SetFillColor(labels[label]["color"])
        labels[label]["hists"][i].SetFillStyle(1001)
        labels[label]["hists"][i].SetLineColor(labels[label]["color"])
    
#labels["wg+jets"]["hists"][mlg_index].Print("all")
#labels["wg+jets"]["hists"]["photon_pt"].Print("all")

fake_photon["hists"][mlg_index].Print("all")
fake_photon_syst["hists"][mlg_index].Print("all")

#subtractRealMCFromFakeEstimateFromData(mc_samples[0]["tree"],fake_photon_hist,fake_muon_hist,fake_lepton_hist,mc_samples[0]["xs"],mc_samples[0]["nweightedevents"])



#    if variable == "mlg":
#
#        ndata = data["hists"][mlg_index].GetBinContent(data["hists"][mlg_index].GetXaxis().FindFixBin(85.0))+ data["hists"][mlg_index].GetBinContent(data["hists"][mlg_index].GetXaxis().FindFixBin(95.0))

#        nzjets = labels["z+jets"]["hists"][mlg_index].GetBinContent(labels["z+jets"]["hists"][mlg_index].GetXaxis().FindFixBin(85.0))+ labels["z+jets"]["hists"][mlg_index].GetBinContent(labels["z+jets"]["hists"][mlg_index].GetXaxis().FindFixBin(95.0))

#        nprediction =hsum.GetBinContent(hsum.GetXaxis().FindFixBin(85.0))+ hsum.GetBinContent(hsum.GetXaxis().FindFixBin(95.0))

#        print ndata

#        print nzjets

#        print nprediction

#        print (ndata - nprediction + nzjets)/nzjets

m= ROOT.RooRealVar("m","m",0,200)
m0=ROOT.RooRealVar("m0",    "m0",0,-10,10)
sigma=ROOT.RooRealVar("sigma",  "sigma",1,0.1,5)
alpha=ROOT.RooRealVar("alpha",  "alpha",5,0,20)
n=ROOT.RooRealVar("n",          "n",1,0,10)

cb = ROOT.RooCBShape("cb", "Crystal Ball", m, m0, sigma, alpha, n)

mass = ROOT.RooRealVar("mass","mass",90,0,200)
width = ROOT.RooRealVar("width","width",5,0.1,10);

bw = ROOT.RooBreitWigner("bw","Breit Wigner",m,mass,width)

RooFFTConvPdf_bwcb = ROOT.RooFFTConvPdf("bwcb","Breit Wigner convolved with a Crystal Ball",m,bw,cb)

RooDataHist_mlg_data = ROOT.RooDataHist("data","dataset",ROOT.RooArgList(m),data["hists"][mlg_index])

RooDataHist_mlg_etog = ROOT.RooDataHist("etog data hist","etog data hist",ROOT.RooArgList(m),electron_to_photon["hists"][mlg_index])

RooHistPdf_etog = ROOT.RooHistPdf("etog","etog",ROOT.RooArgSet(m),RooDataHist_mlg_etog)

RooDataHist_mlg_wg = ROOT.RooDataHist("wg data hist","wg data hist",ROOT.RooArgList(m),labels["wg+jets"]["hists"][mlg_index])

RooHistPdf_wg = ROOT.RooHistPdf("wg","wg",ROOT.RooArgSet(m),RooDataHist_mlg_wg)

RooDataHist_mlg_ttsemi = ROOT.RooDataHist("ttsemi data hist","ttsemi data hist",ROOT.RooArgList(m),labels["ttsemi+jets"]["hists"][mlg_index])

RooHistPdf_ttsemi = ROOT.RooHistPdf("ttsemi","ttsemi",ROOT.RooArgSet(m),RooDataHist_mlg_ttsemi)

RooDataHist_mlg_tt2l2nu = ROOT.RooDataHist("tt2l2nu data hist","tt2l2nu data hist",ROOT.RooArgList(m),labels["tt2l2nu+jets"]["hists"][mlg_index])

RooHistPdf_tt2l2nu = ROOT.RooHistPdf("tt2l2nu","tt2l2nu",ROOT.RooArgSet(m),RooDataHist_mlg_tt2l2nu)

RooDataHist_mlg_ttg = ROOT.RooDataHist("ttg data hist","ttg data hist",ROOT.RooArgList(m),labels["ttg+jets"]["hists"][mlg_index])

RooHistPdf_ttg = ROOT.RooHistPdf("ttg","ttg",ROOT.RooArgSet(m),RooDataHist_mlg_ttg)

top_mlg_hist = labels["ttg+jets"]["hists"][mlg_index].Clone("top")

top_mlg_hist.Add(labels["tt2l2nu+jets"]["hists"][mlg_index])
top_mlg_hist.Add(labels["ttsemi+jets"]["hists"][mlg_index])

RooDataHist_mlg_top = ROOT.RooDataHist("top data hist","top data hist",ROOT.RooArgList(m),top_mlg_hist)

RooHistPdf_top = ROOT.RooHistPdf("top","top",ROOT.RooArgSet(m),RooDataHist_mlg_top)

RooDataHist_mlg_zg = ROOT.RooDataHist("zg data hist","zg data hist",ROOT.RooArgList(m),labels["zg+jets"]["hists"][mlg_index])

RooHistPdf_zg = ROOT.RooHistPdf("zg","zg",ROOT.RooArgSet(m),RooDataHist_mlg_zg)

RooDataHist_mlg_fake_lepton = ROOT.RooDataHist("zg data hist","zg data hist",ROOT.RooArgList(m),fake_lepton["hists"][mlg_index])

RooHistPdf_fake_lepton = ROOT.RooHistPdf("fake lepton","fake lepton",ROOT.RooArgSet(m),RooDataHist_mlg_fake_lepton)

TH1F_fake_lepton_mlg_syst=fake_lepton["hists"][mlg_index].Clone("fake lepton syst")

if lepton_name == "electron":
    TH1F_fake_lepton_mlg_syst.Scale(1.48)
elif lepton_name == "muon":
    TH1F_fake_lepton_mlg_syst.Scale(1.12)

RooDataHist_mlg_fake_lepton_syst = ROOT.RooDataHist("zg data hist","zg data hist",ROOT.RooArgList(m),TH1F_fake_lepton_mlg_syst)

RooHistPdf_fake_lepton_syst = ROOT.RooHistPdf("fake lepton","fake lepton",ROOT.RooArgSet(m),RooDataHist_mlg_fake_lepton_syst)

RooDataHist_mlg_fake_photon = ROOT.RooDataHist("zg data hist","zg data hist",ROOT.RooArgList(m),fake_photon["hists"][mlg_index])

RooHistPdf_fake_photon = ROOT.RooHistPdf("fake photon","fake photon",ROOT.RooArgSet(m),RooDataHist_mlg_fake_photon)

RooDataHist_mlg_fake_photon_syst = ROOT.RooDataHist("fake photon hist","fake photon hist",ROOT.RooArgList(m),fake_photon_syst["hists"][mlg_index])

RooHistPdf_fake_photon_syst = ROOT.RooHistPdf("fake photon","fake photon",ROOT.RooArgSet(m),RooDataHist_mlg_fake_photon_syst)

RooDataHist_mlg_double_fake = ROOT.RooDataHist("zg data hist","zg data hist",ROOT.RooArgList(m),double_fake["hists"][mlg_index])

RooHistPdf_double_fake = ROOT.RooHistPdf("double fake","double fake",ROOT.RooArgSet(m),RooDataHist_mlg_double_fake)


etog_norm = ROOT.RooRealVar("etog_norm","etog_norm",electron_to_photon["hists"][mlg_index].Integral(),electron_to_photon["hists"][mlg_index].Integral());    

ttsemi_norm = ROOT.RooRealVar("ttsemi_norm","ttsemi_norm",labels["ttsemi+jets"]["hists"][mlg_index].Integral(),labels["ttsemi+jets"]["hists"][mlg_index].Integral());    
tt2l2nu_norm = ROOT.RooRealVar("tt2l2nu_norm","tt2l2nu_norm",labels["tt2l2nu+jets"]["hists"][mlg_index].Integral(),labels["tt2l2nu+jets"]["hists"][mlg_index].Integral()); 
ttg_norm = ROOT.RooRealVar("ttg_norm","ttg_norm",labels["ttg+jets"]["hists"][mlg_index].Integral(),labels["ttg+jets"]["hists"][mlg_index].Integral());    

top_norm = ROOT.RooRealVar("top_norm","top_norm",top_mlg_hist.Integral(),top_mlg_hist.Integral());    


wg_norm = ROOT.RooRealVar("wg_norm","wg_norm",0,1000000);    
zg_norm = ROOT.RooRealVar("zg_norm","zg_norm",0,1000000);    
bwcb_norm = ROOT.RooRealVar("bwcb_norm","bwcb_norm",0,1000000);    
fake_lepton_norm = ROOT.RooRealVar("fake_lepton_norm","fake_lepton_norm",fake_lepton["hists"][mlg_index].Integral(),fake_lepton["hists"][mlg_index].Integral());    
fake_photon_norm = ROOT.RooRealVar("fake_photon_norm","fake_photon_norm",fake_photon["hists"][mlg_index].Integral(),fake_photon["hists"][mlg_index].Integral());    
fake_photon_syst_norm = ROOT.RooRealVar("fake_photon_syst_norm","fake_photon_syst_norm",fake_photon_syst["hists"][mlg_index].Integral(),fake_photon_syst["hists"][mlg_index].Integral());    
fake_lepton_syst_norm = ROOT.RooRealVar("fake_lepton_syst_norm","fake_lepton_syst_norm",TH1F_fake_lepton_mlg_syst.Integral(),TH1F_fake_lepton_mlg_syst.Integral());    
double_fake_norm = ROOT.RooRealVar("double_fake_norm","double_fake_norm",double_fake["hists"][mlg_index].Integral(),double_fake["hists"][mlg_index].Integral());    

#wg = ROOT.RooExtendPdf("wg","wg",RooHistPdf_wg,wg_norm)

#zg = ROOT.RooExtendPdf("wg","wg",RooHistPdf_zg,zg_norm)

#bwcb = ROOT.RooExtendPdf("bwcb","bwcb",RooFFTConvPdf_bwcb,bwcb_norm)

n1=ROOT.RooRealVar("n1","n1",0.1,0.01,100000)
n2=ROOT.RooRealVar("n2","n2",0.1,0.01,100000)

f= ROOT.RooRealVar("f","f",0.5,0.,1.) ;

#sum=ROOT.RooAddPdf("sum","sum",ROOT.RooArgList(wg,bwcb),RooArgList(n1,n2))
#sum=ROOT.RooAddPdf("sum","sum",wg,bwcb,f)

#sum=ROOT.RooAddPdf("sum","sum",ROOT.RooArgList(wg,zg,bwcb),RooArgList(wg_norm,zg_norm,bwcb_norm))

if lepton_name == "electron" or lepton_name == "both":
    sum=ROOT.RooAddPdf("sum","sum",ROOT.RooArgList(RooHistPdf_wg,RooHistPdf_zg,RooFFTConvPdf_bwcb,RooHistPdf_fake_lepton,RooHistPdf_fake_photon,RooHistPdf_double_fake,RooHistPdf_top,RooHistPdf_etog),ROOT.RooArgList(wg_norm,zg_norm,bwcb_norm,fake_lepton_norm,fake_photon_norm,double_fake_norm,top_norm,etog_norm))
    sum_fake_photon_syst=ROOT.RooAddPdf("sum","sum",ROOT.RooArgList(RooHistPdf_wg,RooHistPdf_zg,RooFFTConvPdf_bwcb,RooHistPdf_fake_lepton,RooHistPdf_fake_photon_syst,RooHistPdf_double_fake,RooHistPdf_top,RooHistPdf_etog),ROOT.RooArgList(wg_norm,zg_norm,bwcb_norm,fake_lepton_norm,fake_photon_syst_norm,double_fake_norm,top_norm,etog_norm))
    sum_fake_lepton_syst=ROOT.RooAddPdf("sum","sum",ROOT.RooArgList(RooHistPdf_wg,RooHistPdf_zg,RooFFTConvPdf_bwcb,RooHistPdf_fake_lepton_syst,RooHistPdf_fake_photon,RooHistPdf_double_fake,RooHistPdf_top,RooHistPdf_etog),ROOT.RooArgList(wg_norm,zg_norm,bwcb_norm,fake_lepton_syst_norm,fake_photon_norm,double_fake_norm,top_norm,etog_norm))
elif lepton_name == "muon":
    sum=ROOT.RooAddPdf("sum","sum",ROOT.RooArgList(RooHistPdf_wg,RooHistPdf_zg,RooHistPdf_fake_lepton,RooHistPdf_fake_photon,RooHistPdf_double_fake,RooHistPdf_top),ROOT.RooArgList(wg_norm,zg_norm,fake_lepton_norm,fake_photon_norm,double_fake_norm,top_norm))
    sum_fake_photon_syst=ROOT.RooAddPdf("sum","sum",ROOT.RooArgList(RooHistPdf_wg,RooHistPdf_zg,RooHistPdf_fake_lepton,RooHistPdf_fake_photon_syst,RooHistPdf_double_fake,RooHistPdf_top),ROOT.RooArgList(wg_norm,zg_norm,fake_lepton_norm,fake_photon_syst_norm,double_fake_norm,top_norm))
    sum_fake_lepton_syst=ROOT.RooAddPdf("sum","sum",ROOT.RooArgList(RooHistPdf_wg,RooHistPdf_zg,RooHistPdf_fake_lepton_syst,RooHistPdf_fake_photon,RooHistPdf_double_fake,RooHistPdf_top),ROOT.RooArgList(wg_norm,zg_norm,fake_lepton_syst_norm,fake_photon_norm,double_fake_norm,top_norm))
else:
    assert(0)

sum.fitTo(RooDataHist_mlg_data,ROOT.RooFit.Extended())


frame1 = m.frame()

RooDataHist_mlg_data.plotOn(frame1)
sum.plotOn(frame1)
#sum.plotOn(frame, ROOT.RooFit.Components(ROOT.RooArgSet(sum.getComponents()["zg"])),ROOT.RooFit.LineStyle(ROOT.kDashed)) 
#sum.plotOn(frame, ROOT.RooFit.Components("zg,wg,bwcb"),ROOT.RooFit.LineStyle(ROOT.kDashed)) 

red_th1f=ROOT.TH1F("red_th1f","red_th1f",1,0,1)
red_th1f.SetLineColor(ROOT.kRed)
red_th1f.SetLineWidth(3)
red_th1f.SetLineStyle(ROOT.kDashed)
green_th1f=ROOT.TH1F("green_th1f","green_th1f",1,0,1)
green_th1f.SetLineColor(ROOT.kGreen)
green_th1f.SetLineWidth(3)
green_th1f.SetLineStyle(ROOT.kDashed)
magenta_th1f=ROOT.TH1F("magenta_th1f","magenta_th1f",1,0,1)
magenta_th1f.SetLineColor(ROOT.kMagenta)
magenta_th1f.SetLineWidth(3)
magenta_th1f.SetLineStyle(ROOT.kDashed)
orangeminus1_th1f=ROOT.TH1F("orangeminus1_th1f","orangeminus_th1f",1,0,1)
orangeminus1_th1f.SetLineColor(ROOT.kOrange-1)
orangeminus1_th1f.SetLineWidth(3)
orangeminus1_th1f.SetLineStyle(ROOT.kDashed)

if lepton_name == "both" or lepton_name == "electron":
    sum.plotOn(frame1, ROOT.RooFit.Components("wg"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kRed)) 
    sum.plotOn(frame1, ROOT.RooFit.Components("zg"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kGreen)) 
    sum.plotOn(frame1, ROOT.RooFit.Components("bwcb"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kMagenta)) 

    legend1 = ROOT.TLegend(0.6, 0.7, 0.89, 0.89)
    legend1.SetBorderSize(0)  # no border
    legend1.SetFillStyle(0)  # make transparent
    legend1.AddEntry(red_th1f,"wg","lp")
    legend1.AddEntry(green_th1f,"zg","lp")
    legend1.AddEntry(magenta_th1f,"bwcb","lp")
elif lepton_name == "muon":
    sum.plotOn(frame1, ROOT.RooFit.Components("wg"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kRed)) 
    sum.plotOn(frame1, ROOT.RooFit.Components("zg"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kGreen)) 

    legend1 = ROOT.TLegend(0.6, 0.7, 0.89, 0.89)
    legend1.SetBorderSize(0)  # no border
    legend1.SetFillStyle(0)  # make transparent
    legend1.AddEntry(red_th1f,"wg","lp")
    legend1.AddEntry(green_th1f,"zg","lp")
else:
    assert(0)

top_norm.Print("all")
etog_norm.Print("all")
wg_norm.Print("all")
zg_norm.Print("all")
bwcb_norm.Print("all")
fake_lepton_norm.Print("all")
fake_photon_norm.Print("all")
double_fake_norm.Print("all")
ttsemi_norm.Print("all")
tt2l2nu_norm.Print("all")
ttg_norm.Print("all")

frame1.SetTitle("")
frame1.GetYaxis().SetTitle("")
frame1.GetXaxis().SetTitle("m_{lg} (GeV)")

c2 = ROOT.TCanvas("c2", "c2",5,50,500,500)

frame1.Draw()

legend1.Draw("same")

c2.Update()
c2.ForceUpdate()
c2.Modified()

c2.SaveAs(options.outputdir + "/" +"frame1.png")

c2.Close()

frame2 = m.frame()

RooDataHist_mlg_data.plotOn(frame2)
sum.plotOn(frame2)

sum.plotOn(frame2, ROOT.RooFit.Components("fake photon"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kRed)) 
sum.plotOn(frame2, ROOT.RooFit.Components("fake lepton"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kGreen)) 
sum.plotOn(frame2, ROOT.RooFit.Components("double fake"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kMagenta)) 

if lepton_name == "electron" or lepton_name == "both":
    sum.plotOn(frame2, ROOT.RooFit.Components("etog"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kOrange-1)) 

frame2.SetTitle("")
frame2.GetYaxis().SetTitle("")
frame2.GetXaxis().SetTitle("m_{lg} (GeV)")

c3 = ROOT.TCanvas("c3", "c3",5,50,500,500)

legend2 = ROOT.TLegend(0.6, 0.7, 0.89, 0.89)
legend2.SetBorderSize(0)  # no border
legend2.SetFillStyle(0)  # make transparent
legend2.AddEntry(red_th1f,"fake photon","lp")
legend2.AddEntry(green_th1f,"fake lepton","lp")
legend2.AddEntry(magenta_th1f,"double fake","lp")
if lepton_name == "electron" or lepton_name == "both":
    legend2.AddEntry(orangeminus1_th1f,"e->g non-res","lp")


frame2.Draw()

legend2.Draw("same")

c3.Update()
c3.ForceUpdate()
c3.Modified()

c3.SaveAs(options.outputdir + "/" +"frame2.png")

c3.Close()

wg_norm_val = wg_norm.getVal()
wg_norm_stat_unc = wg_norm.getError()

print "wg_norm_val = " + str(wg_norm_val)
print "wg_norm_stat_unc = " + str(wg_norm_stat_unc)

sum_fake_photon_syst.fitTo(RooDataHist_mlg_data,ROOT.RooFit.Extended())

wg_norm_fake_photon_syst_val = wg_norm.getVal()
wg_norm_fake_photon_syst_stat_unc = wg_norm.getError()

print "wg_norm_fake_photon_syst_val = " + str(wg_norm_fake_photon_syst_val)
print "wg_norm_fake_photon_syst_stat_unc = " + str(wg_norm_fake_photon_syst_stat_unc)
print "wg_norm_syst_unc_due_to_fake_photon_unc = " + str(wg_norm_fake_photon_syst_val-wg_norm_val)

sum_fake_lepton_syst.fitTo(RooDataHist_mlg_data,ROOT.RooFit.Extended())

wg_norm_fake_lepton_syst_val = wg_norm.getVal()
wg_norm_fake_lepton_syst_stat_unc = wg_norm.getError()

print "wg_norm_fake_lepton_syst_val = " + str(wg_norm_fake_lepton_syst_val)
print "wg_norm_fake_lepton_syst_stat_unc = " + str(wg_norm_fake_lepton_syst_stat_unc)
print "wg_norm_syst_unc_due_to_fake_lepton_unc = " + str(wg_norm_val-wg_norm_fake_lepton_syst_val)

print "(number of selected wg+jets events) * (data/MC eff scale factor) * (wg+jets xs) * (2016 integrated luminosity) / (number of wg+jets events run over) = "+str(labels["wg+jets"]["hists"][mlg_index].Integral())

mean_pdf=0
for i in range(0,102):
    mean_pdf += labels["wg+jets"]["hists-pdf-variation"+str(i)][mlg_index].Integral() 

mean_pdf = mean_pdf/102.0

print "mean_pdf = "+str(mean_pdf)

stddev_pdf = 0
for i in range(0,102):
    stddev_pdf += pow((labels["wg+jets"]["hists-pdf-variation"+str(i)][mlg_index].Integral() - mean_pdf),2)

stddev_pdf = sqrt(stddev_pdf/(102-1))

print "stddev_pdf = "+str(mean_pdf/102.0)

electron_id_sf_unc = labels["wg+jets"]["hists-electron-id-sf-variation"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].Integral()
electron_reco_sf_unc = labels["wg+jets"]["hists-electron-reco-sf-variation"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].Integral()
muon_id_sf_unc = labels["wg+jets"]["hists-muon-id-sf-variation"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].Integral()
muon_iso_sf_unc = labels["wg+jets"]["hists-muon-iso-sf-variation"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].Integral()
photon_id_sf_unc = labels["wg+jets"]["hists-photon-id-sf-variation"][mlg_index].Integral() - labels["wg+jets"]["hists"][mlg_index].Integral()

print "electron_id_sf_unc = "+str(electron_id_sf_unc)
print "electron_reco_sf_unc = "+str(electron_reco_sf_unc)
print "muon_id_sf_unc = "+str(muon_id_sf_unc)
print "muon_iso_sf_unc = "+str(muon_iso_sf_unc)
print "photon_id_sf_unc = "+str(photon_id_sf_unc)

if labels["wg+jets"]["syst-scale"]:
    qcd_up = labels["wg+jets"]["hists-scale-variation3"][mlg_index].Integral()
    qcd_nom = labels["wg+jets"]["hists"][mlg_index].Integral()
    qcd_down = labels["wg+jets"]["hists-scale-variation7"][mlg_index].Integral()

    qcd_unc=0.5*max(abs(qcd_up - qcd_nom),abs(qcd_up-qcd_down),abs(qcd_nom-qcd_down))

    print "qcd_unc = " + str(qcd_unc)

print "(number of selected wg+jets events) * (data/MC eff scale factor) = "+str(labels["wg+jets"]["hists"][mlg_index].Integral()*labels["wg+jets"]["samples"][0]["nweightedevents"]/(labels["wg+jets"]["samples"][0]["xs"]*1000*35.9))

print "(number of wg+jets events run over) = "+str(labels["wg+jets"]["samples"][0]["nweightedevents"])

fiducial_region_cuts_efficiency = 0.51649677698712206047032474804031

Aepsilon = labels["wg+jets"]["hists"][mlg_index].Integral()/(labels["wg+jets"]["samples"][0]["xs"]*fiducial_region_cuts_efficiency*1000*35.9)

Aepsilon_pdf = (labels["wg+jets"]["hists"][mlg_index].Integral()-stddev_pdf)/(labels["wg+jets"]["samples"][0]["xs"]*fiducial_region_cuts_efficiency*1000*35.9)

if labels["wg+jets"]["syst-scale"]:
    Aepsilon_scale = (labels["wg+jets"]["hists"][mlg_index].Integral()-qcd_unc)/(labels["wg+jets"]["samples"][0]["xs"]*fiducial_region_cuts_efficiency*1000*35.9)

Aepsilon_electron_id_sf = (labels["wg+jets"]["hists"][mlg_index].Integral()-electron_id_sf_unc)/(labels["wg+jets"]["samples"][0]["xs"]*fiducial_region_cuts_efficiency*1000*35.9)

Aepsilon_electron_reco_sf = (labels["wg+jets"]["hists"][mlg_index].Integral()-electron_reco_sf_unc)/(labels["wg+jets"]["samples"][0]["xs"]*fiducial_region_cuts_efficiency*1000*35.9)

Aepsilon_muon_id_sf = (labels["wg+jets"]["hists"][mlg_index].Integral()-muon_id_sf_unc)/(labels["wg+jets"]["samples"][0]["xs"]*fiducial_region_cuts_efficiency*1000*35.9)

Aepsilon_muon_iso_sf = (labels["wg+jets"]["hists"][mlg_index].Integral()-muon_iso_sf_unc)/(labels["wg+jets"]["samples"][0]["xs"]*fiducial_region_cuts_efficiency*1000*35.9)

Aepsilon_photon_id_sf = (labels["wg+jets"]["hists"][mlg_index].Integral()-photon_id_sf_unc)/(labels["wg+jets"]["samples"][0]["xs"]*fiducial_region_cuts_efficiency*1000*35.9)
 
print "Aepsilon = (number of selected wg+jets events) * (data/MC eff scale factor) / (number of wg+jets events run over)= "+str(Aepsilon)

print "wg_norm_val/Aepsilon/35.9/1000.0 = " + str(wg_norm_val/Aepsilon/35.9/1000.0)

print "stat uncertainty = " + str(wg_norm_stat_unc/Aepsilon/35.9/1000.0)

print "lumi uncertainty = " + str(wg_norm_val/Aepsilon/(35.9*0.975)/1000.0 - wg_norm_val/Aepsilon/35.9/1000.0)

print "pdf uncertainty   = " + str(wg_norm_val/Aepsilon_pdf/35.9/1000.0 - wg_norm_val/Aepsilon/35.9/1000.0)

if labels["wg+jets"]["syst-scale"]:
    print "scale uncertainty = " + str(wg_norm_val/Aepsilon_scale/35.9/1000.0 - wg_norm_val/Aepsilon/35.9/1000.0)

print "electron id sf uncertainty = " + str(wg_norm_val/Aepsilon_electron_id_sf/35.9/1000.0 - wg_norm_val/Aepsilon/35.9/1000.0)

print "electron reco sf uncertainty = " + str(wg_norm_val/Aepsilon_electron_reco_sf/35.9/1000.0 - wg_norm_val/Aepsilon/35.9/1000.0)

print "muon id sf uncertainty = " + str(wg_norm_val/Aepsilon_muon_id_sf/35.9/1000.0 - wg_norm_val/Aepsilon/35.9/1000.0)

print "muon iso sf uncertainty = " + str(wg_norm_val/Aepsilon_muon_iso_sf/35.9/1000.0 - wg_norm_val/Aepsilon/35.9/1000.0)

print "photon id sf uncertainty = " + str(wg_norm_val/Aepsilon_photon_id_sf/35.9/1000.0 - wg_norm_val/Aepsilon/35.9/1000.0)

for i in range(len(variables)):

    #i = 0 is for the ewdim6 analysis
    if i == 0:
        continue

    data["hists"][i].Print("all")

    data["hists"][i].SetMarkerStyle(ROOT.kFullCircle)
    data["hists"][i].SetLineWidth(3)
    data["hists"][i].SetLineColor(ROOT.kBlack)

    fake_photon["hists"][i].SetFillColor(ROOT.kGray+1)
    fake_lepton["hists"][i].SetFillColor(ROOT.kAzure-1)
    double_fake["hists"][i].SetFillColor(ROOT.kMagenta)
    electron_to_photon["hists"][i].SetFillColor(ROOT.kYellow)

    fake_photon["hists"][i].SetLineColor(ROOT.kGray+1)
    fake_lepton["hists"][i].SetLineColor(ROOT.kAzure-1)
    double_fake["hists"][i].SetLineColor(ROOT.kMagenta)
    electron_to_photon["hists"][i].SetLineColor(ROOT.kYellow)
    

    fake_photon["hists"][i].SetFillStyle(1001)
    fake_lepton["hists"][i].SetFillStyle(1001)
    double_fake["hists"][i].SetFillStyle(1001)
    electron_to_photon["hists"][i].SetFillStyle(1001)

    s=str(options.lumi)+" fb^{-1} (13 TeV)"
    lumilabel = ROOT.TLatex (0.95, 0.93, s)
    lumilabel.SetNDC ()
    lumilabel.SetTextAlign (30)
    lumilabel.SetTextFont (42)
    lumilabel.SetTextSize (0.040)

#
    hsum = data["hists"][i].Clone()
    hsum.Scale(0.0)

    hstack = ROOT.THStack()

    if lepton_name == "electron" or lepton_name == "both": 
        hsum.Add(electron_to_photon["hists"][i])
        hstack.Add(electron_to_photon["hists"][i])

    for label in labels.keys():
        if labels[label]["color"] == None:
            continue
        hsum.Add(labels[label]["hists"][i])
        hstack.Add(labels[label]["hists"][i])

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
    else:
        data["hists"][i].SetMaximum(data["hists"][i].GetMaximum()*1.55)
        

    data["hists"][i].SetMinimum(0)
    hstack.SetMinimum(0)
    hsum.SetMinimum(0)

    data["hists"][i].Draw("")

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
        draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,electron_to_photon["hists"][i],"e->g","f")

    for label in labels.keys():
        if labels[label]["color"] == None:
            continue
        j=j+1    
        draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,labels[label]["hists"][i],label,"f")
    

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

    c1.SaveAs(options.outputdir + "/" + variables[i] + ".png")

c1.Close()

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
    dcard.write(" electron_to_photon")
    dcard.write('\n')    
    dcard.write("process")
    dcard.write(" 0")
    
    for j in range(1,len(labels.keys())+3):
        dcard.write(" " + str(j))
    dcard.write('\n')    
    dcard.write('rate')
    dcard.write(' '+str(sm_lhe_weight_hist.GetBinContent(i)))
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
        dcard.write(" 0.0001") 

    if fake_lepton["hists"][0].GetBinContent(i) > 0:        
        dcard.write(" "+str(fake_lepton["hists"][0].GetBinContent(i))) 
    else:
        dcard.write(" 0.0001") 

    if double_fake["hists"][0].GetBinContent(i) > 0:        
        dcard.write(" "+str(double_fake["hists"][0].GetBinContent(i))) 
    else:
        dcard.write(" 0.0001") 

    if electron_to_photon["hists"][0].GetBinContent(i) > 0:        
        dcard.write(" "+str(electron_to_photon["hists"][0].GetBinContent(i))) 
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
        dcard.write("mcstat_ewdim6_bin"+str(i)+" lnN "+str(1+sm_lhe_weight_hist.GetBinError(i)/sm_lhe_weight_hist.GetBinContent(i)))
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
