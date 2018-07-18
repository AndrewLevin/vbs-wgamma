data_driven = True

import json

import sys
import style

import optparse

parser = optparse.OptionParser()


parser.add_option('--lep',dest='lep',default='muon')
parser.add_option('--phoeta',dest='phoeta',default='barrel')
parser.add_option('--btagged',dest='btagged', default=False,  action = 'store_true')

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

if options.btagged:
    btagging_selection = 0
else:
    btagging_selection = 1

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

#labels = { "z+jets" : {"color" : ROOT.kOrange, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy1j_m1050.root", "xs" : 729.726349},{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy2j_m1050.root", "xs" : 387.472359},{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy3j_m1050.root" , "xs" : 95.033555},{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy4j_m1050.root", "xs" : 36.698502 },{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy1j_m50.root", "xs" : 1012.296845 },{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy2j_m50.root", "xs" : 334.717838},{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy3j_m50.root", "xs" : 102.462800},{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy4j_m50.root", "xs" : 54.481360} ] }, "tt+jets" : {"color" : ROOT.kGreen+2, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_ttjets.root", "xs" : 831.76 } ] }, "zg+jets" : { "color" : ROOT.kYellow, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_qcd_zg.root", "xs" : 47.46} ] }, "wg+jets" : { "color" : ROOT.kRed, "samples" : [{"filename" : "/afs/cern.ch/work/a/amlevin/data/wgamma_wjets.root", "xs" : 60430.0 } ]  }} 

labels = { "z+jets" : {"color" : ROOT.kOrange, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy1j_m50.root", "xs" : 1012.296845 },{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy2j_m50.root", "xs" : 334.717838},{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy3j_m50.root", "xs" : 102.462800},{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy4j_m50.root", "xs" : 54.481360} ] }, "tt+jets" : {"color" : ROOT.kGreen+2, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_ttjets.root", "xs" : 831.76 } ] }, "zg+jets" : { "color" : ROOT.kYellow, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_qcd_zg.root", "xs" : 47.46} ] }, "wg+jets" : { "color" : ROOT.kRed, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_qcd_wg.root", "xs" : 178.6}]  } } 

#labels = { "wjets" : { "color" : ROOT.kOrange, "samples" : [ { "filename" : "/afs/cern.ch/work/a/amlevin/data/wgamma_w2j.root", "xs" : 3161.0},{ "filename" : "/afs/cern.ch/work/a/amlevin/data/wgamma_w3j.root", "xs" : 947.9},{ "filename" : "/afs/cern.ch/work/a/amlevin/data/wgamma_w4j.root", "xs" : 493.8} ] } }

#labels ={ "zjets" : {"color": ROOT.kOrange, "samples" : [{"filename" : "/afs/cern.ch/work/a/amlevin/data/wgamma_zjets.root", "xs" : 4963.0}] }}

#labels ={ "wjets" : {"color": ROOT.kOrange, "samples" : [{"filename" : "/afs/cern.ch/work/a/amlevin/data/wgamma_wjets.root", "xs" : 60430.0}] }}


######labels = { "z+jets" : {"color" : ROOT.kOrange, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy1j_m1050.root", "xs" : 729.726349},{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy2j_m1050.root", "xs" : 387.472359},{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy3j_m1050.root" , "xs" : 95.033555},{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy4j_m1050.root", "xs" : 36.698502 },{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy1j_m50_zmassrange30.root", "xs" : 1012.296845 },{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy2j_m50_zmassrange30.root", "xs" : 334.717838},{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy3j_m50_zmassrange30.root", "xs" : 102.462800},{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy4j_m50_zmassrange30.root", "xs" : 54.481360} ] }, "wg+jets" : { "color" : ROOT.kRed, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_qcd_wg.root", "xs" : 178.6}]  }, "zg+jets" : { "color" : ROOT.kYellow, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_qcd_zg.root", "xs" : 47.46} ] }, "tt+jets" : {"color" : ROOT.kGreen+2, "samples" : [{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_ttjets.root", "xs" : 831.76 } ] } } 

#mc_samples = [ {"filename" : '/afs/cern.ch/work/a/amlevin/data/wgamma_wwlnlnu.root', "label" : "ww" , "xs" : 12.178, "color" : ROOT.kGreen+2} ]

#mc_samples = [{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy1j_m1050.root", "label": "dy+jets", "xs" : 729.726349, "color" : ROOT.kGreen+2},{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy2j_m1050.root", "label": "dy+jets", "xs" : 387.472359, "color" : ROOT.kGreen+2},{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy3j_m1050.root", "label": "dy+jets", "xs" : 95.033555, "color" : ROOT.kGreen+2},{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy4j_m1050.root", "label": "dy+jets", "xs" : 36.698502, "color" : ROOT.kGreen+2},{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy1j_m50.root", "label": "dy+jets", "xs" : 1012.296845, "color" : ROOT.kGreen+2},{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy2j_m50.root", "label": "dy+jets", "xs" : 334.717838, "color" : ROOT.kGreen+2},{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy3j_m50.root", "label": "dy+jets", "xs" : 102.462800, "color" : ROOT.kGreen+2},{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_dy4j_m50.root", "label": "dy+jets", "xs" : 54.481360, "color" : ROOT.kGreen+2}]


#mc_samples = [{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_wjets.root", "label": "w+jets", "xs" : 60430.0, "color" : ROOT.kGreen+2},{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_zjets.root", "label": "z+jets", "xs" : 4963.0, "color" : ROOT.kGray+1},{"filename": "/afs/cern.ch/work/a/amlevin/data/wgamma_ttjets.root", "label": "tt+jets", "xs" : 831.76, "color" : ROOT.kRed}]

#mc_samples ={}

variables = ["mjj","met","lepton_pt","lepton_eta","photon_pt","photon_eta","mlg","lepton_phi","photon_phi","njets","mt"]

histogram_templates = { "mjj" : ROOT.TH1F("mjj","",18,200,2000), "met" : ROOT.TH1F("met", "", 13 , 40., 300 ), "lepton_pt" : ROOT.TH1F('lepton_pt', '', 8, 20., 180 ), "lepton_eta" : ROOT.TH1F('lepton_eta', '', 10, -2.5, 2.5 ), "photon_pt" : ROOT.TH1F('photon_pt', '', 8, 20., 180 ), "photon_eta" : ROOT.TH1F('photon_eta', '', 10, -2.5, 2.5 ), "mlg" : ROOT.TH1F("mlg","",20,0,200) , "lepton_phi" : ROOT.TH1F("lepton_phi","",14,-3.5,3.5), "photon_phi" : ROOT.TH1F("photon_phi","",14,-3.5,3.5), "njets" : ROOT.TH1F("njets","",21,-0.5,20.5), "mt" : ROOT.TH1F("mt","",20,0,200)} 

def getVariable(varname, tree):
    if varname == "mjj":
        return tree.mjj
    elif varname == "mlg":
        return tree.mlg
    elif varname == "mt":
        return tree.mt
    elif varname == "njets":
        return float(tree.njets)
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
    if varname == "mjj":
        return "m_{jj} (GeV)"
    elif varname == "njets":
        return "number of jets"
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

#def fillHistograms(tree,hists):

xoffsetstart = 0.0;
yoffsetstart = 0.0;
xoffset = 0.20;
yoffset = 0.05;

#xpositions = [0.60,0.60,0.60,0.60,0.60,0.60,0.40,0.40,0.40]
xpositions = [0.65,0.65,0.65,0.65,0.45,0.45,0.45,0.45,0.45]
#ypositions = [0,1,2,3,4,5,0,1,2]
ypositions = [0,1,2,3,0,1,2,3,4]

style.GoodStyle().cd()

muon_fr_file = ROOT.TFile("/afs/cern.ch/user/a/amlevin/vbs-wgamma/muon_frs.root")
electron_fr_file = ROOT.TFile("/afs/cern.ch/user/a/amlevin/vbs-wgamma/electron_frs.root")

muon_fr_hist=muon_fr_file.Get("muon_frs")
electron_fr_hist=electron_fr_file.Get("electron_frs")

from array import array

photon_ptbins=array('d', [25,30,40,50,70,100,135,400])

fake_photon_event_weights_muon_barrel = [0.15815616294972137, 0.11842631687103078, 0.09497972627136668, 0.07704098055808917, 0.06705033604293814, 0.04910700253820312, 0.037116405772666686]

fake_photon_event_weights_electron_barrel = [0.14729547518579378, 0.11421925541775203, 0.08524097588993211, 0.06762542220878368, 0.05914284150149269, 0.05021945953690191, 0.034507727771907866] 

#fake_photon_event_weights_electron_barrel = fake_photon_event_weights_muon_barrel

fake_photon_event_weights_muon_endcap = [0.23225810711393494, 0.19728970137188945, 0.16344824834297003, 0.13139089595151318, 0.11400432064564872, 0.07789504259755933, 0.07276783779540584]
#fake_photon_event_weights_electron_endcap = fake_photon_event_weights_muon_endcap

fake_photon_event_weights_electron_endcap = [0.21275745018679257, 0.17094337839234355, 0.14557855446095005, 0.1286923484383003, 0.09655739377138799, 0.06315470308370295, 0.04184691085481931] 

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

def subtractRealMCFromFakeEstimateFromData(mc_tree,data_fake_photon,data_fake_muon,data_fake_electron,xs,n_weighted_events):

    #if sample["label"] == "tt+jets":
    #    return

    for i in range(mc_tree.GetEntries()):

        mc_tree.GetEntry(i)
        
        if photon_eta_cutstring == "abs(photon_eta) < 1.4442":  
            
            if mc_tree.lepton_pdg_id == lepton_abs_pdg_id and mc_tree.is_lepton_tight == '\x01' and abs(mc_tree.photon_eta) < 1.4442 and (mc_tree.photon_selection == 1 or mc_tree.photon_selection == 0) and mc_tree.photon_pt > 25 and mc_tree.photon_pt < 70 and mc_tree.btagging_selection == btagging_selection and mc_tree.is_lepton_real == '\x01' and mc_tree.photon_gen_matching > 0 and mc_tree.mjj < 400 and not (mc_tree.mlg > 81.2 and mc_tree.mlg < 101.2):
                for variable in variables:
                    data_fake_photon["hists"][variable].Fill(getVariable(variable,mc_tree),-photonfakerate(mc_tree.photon_eta, mc_tree.photon_pt,mc_tree.lepton_pdg_id, "nominal")* xs * 1000 * 36.15 / n_weighted_events)  
        elif photon_eta_cutstring == "1.566 < abs(photon_eta) && abs(photon_eta) < 2.5":   
            if mc_tree.lepton_pdg_id == lepton_abs_pdg_id and mc_tree.is_lepton_tight == '\x01' and 1.566 < abs(mc_tree.photon_eta) and abs(mc_tree.photon_eta) < 2.5 and (mc_tree.photon_selection == 1 or mc_tree.photon_selection == 0) and mc_tree.photon_pt > 25 and mc_tree.photon_pt < 70 and mc_tree.btagging_selection == btagging_selection and mc_tree.is_lepton_real == '\x01' and mc_tree.photon_gen_matching > 0 and mc_tree.mjj < 400 and not (mc_tree.mlg > 81.2 and mc_tree.mlg < 101.2):
                for variable in variables:
                    data_fake_photon["hists"][variable].Fill(getVariable(variable,mc_tree),-photonfakerate(mc_tree.photon_eta, mc_tree.photon_pt,mc_tree.lepton_pdg_id, "nominal")* xs * 1000 * 36.15 / n_weighted_events)  
        else:
            assert(0)

        if photon_eta_cutstring == "abs(photon_eta) < 1.4442":
            if mc_tree.lepton_pdg_id == lepton_abs_pdg_id and mc_tree.is_lepton_tight == '\x00' and abs(mc_tree.photon_eta) < 1.4442 and mc_tree.photon_selection == 2 and mc_tree.photon_pt > 25 and mc_tree.photon_pt < 70 and mc_tree.btagging_selection == btagging_selection and mc_tree.is_lepton_real == '\x01' and mc_tree.photon_gen_matching > 0 and mc_tree.mjj < 400 and not (mc_tree.mlg > 81.2 and mc_tree.mlg < 101.2):
                if lepton_name == "muon":
                    if mc_tree.gen_weight > 0:
                        for variable in variables:
                            data_fake_muon["hists"][variable].Fill(getVariable(variable,mc_tree),-muonfakerate(mc_tree.lepton_eta, mc_tree.lepton_pt,"nominal")* xs * 1000 * 36.15 / n_weighted_events)
                    else:
                        for variable in variables:
                            data_fake_muon["hists"][variable].Fill(getVariable(variable,mc_tree),muonfakerate(mc_tree.lepton_eta, mc_tree.lepton_pt,"nominal")* xs * 1000 * 36.15 / n_weighted_events)
                elif lepton_name == "electron":

                    if mc_tree.gen_weight > 0:
                        for variable in variables:
                            data_fake_electron["hists"][variable].Fill(getVariable(variable,mc_tree),-electronfakerate(mc_tree.lepton_eta, mc_tree.lepton_pt,"nominal")* xs * 1000 * 36.15 / n_weighted_events)
                    else:
                        for variable in variables:
                            data_fake_electron["hists"][variable].Fill(getVariable(variable,mc_tree),electronfakerate(mc_tree.lepton_eta, mc_tree.lepton_pt,"nominal")* xs * 1000 * 36.15 / n_weighted_events)
                else:
                    assert(0)

        elif photon_eta_cutstring == "1.566 < abs(photon_eta) && abs(photon_eta) < 2.5":
             if mc_tree.lepton_pdg_id == lepton_abs_pdg_id and mc_tree.is_lepton_tight == '\x00' and 1.566 < abs(mc_tree.photon_eta) and abs(mc_tree.photon_eta) < 2.5 and mc_tree.photon_selection == 2 and mc_tree.photon_pt > 25 and mc_tree.photon_pt < 70 and mc_tree.btagging_selection == btagging_selection and mc_tree.is_lepton_real == '\x01' and mc_tree.photon_gen_matching > 0 and mc_tree.mjj < 400 and not (mc_tree.mlg > 81.2 and mc_tree.mlg < 101.2):
                 if lepton_name == "muon":
                     if mc_tree.gen_weight > 0:
                         for variable in variables:
                             data_fake_muon["hists"][variable].Fill(getVariable(variable,mc_tree),-muonfakerate(mc_tree.lepton_eta, mc_tree.lepton_pt,"nominal")* xs * 1000 * 36.15 / n_weighted_events)

                     else:
                         for variable in variables:
                             data_fake_muon["hists"][variable].Fill(getVariable(variable,mc_tree),muonfakerate(mc_tree.lepton_eta, mc_tree.lepton_pt,"nominal")* xs * 1000 * 36.15 / n_weighted_events)
                 elif lepton_name == "electron":

                     if mc_tree.gen_weight > 0:
                         for variable in variables:
                             data_fake_electron["hists"][variable].Fill(getVariable(variable, mc_tree),-electronfakerate(mc_tree.lepton_eta, mc_tree.lepton_pt,"nominal")* xs * 1000 * 36.15 / n_weighted_events)
                     else:
                         for variable in variables:
                             data_fake_electron["hists"][variable].Fill(getVariable(variable,mc_tree),electronfakerate(mc_tree.lepton_eta, mc_tree.lepton_pt,"nominal")* xs * 1000 * 36.15 / n_weighted_events)
                 else:
                     assert(0)
        else:
            assert(0)

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
    data_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wgamma_single_muon.root")
elif lepton_name == "electron":
    data_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wgamma_single_electron.root")
else:
    assert(0)

for label in labels.keys():

    labels[label]["hists"] = {}

    for variable in variables:
        labels[label]["hists"][variable] = histogram_templates[variable].Clone(label + " " + variable)
        labels[label]["hists"][variable].Sumw2()

    for sample in labels[label]["samples"]:
        sample["file"] = ROOT.TFile.Open(sample["filename"])
        sample["tree"] = sample["file"].Get("Events")
        sample["nweightedevents"] = sample["file"].Get("nWeightedEvents").GetBinContent(1)



data = {}
fake_photon = {}
fake_electron = {}
fake_muon = {}
double_fake = {}

data["hists"] = {}
fake_photon["hists"] = {}
fake_electron["hists"] = {}
fake_muon["hists"] = {}
double_fake["hists"] = {}

for variable in variables:
    data["hists"][variable] = histogram_templates[variable].Clone("data " + variable)
    fake_photon["hists"][variable] = histogram_templates[variable].Clone("fake photon " + variable)
    fake_electron["hists"][variable] = histogram_templates[variable].Clone("fake electron " + variable)
    fake_muon["hists"][variable] = histogram_templates[variable].Clone("fake muon " + variable)
    double_fake["hists"][variable] = histogram_templates[variable].Clone("double fake " + variable)
    data["hists"][variable].Sumw2()
    fake_photon["hists"][variable].Sumw2()
    fake_electron["hists"][variable].Sumw2()
    fake_muon["hists"][variable].Sumw2()
    double_fake["hists"][variable].Sumw2()

data_events_tree = data_file.Get("Events")

c1 = ROOT.TCanvas("c1", "c1",5,50,500,500);

ROOT.gROOT.cd()

def fillHistogramMC(sample,histograms):

    for i in range(sample["tree"].GetEntries()):

        sample["tree"].GetEntry(i)

        if photon_eta_cutstring == "abs(photon_eta) < 1.4442":        
#            if tree.lepton_pdg_id == lepton_abs_pdg_id and tree.is_lepton_tight == '\x01' and abs(tree.photon_eta) < 1.4442 and tree.photon_selection == 2 and tree.photon_pt > 25 and tree.photon_pt < 70 and tree.btagging_selection == btagging_selection:
            if sample["tree"].lepton_pdg_id == lepton_abs_pdg_id and sample["tree"].is_lepton_tight == '\x01' and abs(sample["tree"].photon_eta) < 1.4442 and sample["tree"].photon_selection == 2 and sample["tree"].photon_pt > 25 and sample["tree"].photon_pt < 70 and sample["tree"].btagging_selection == btagging_selection and sample["tree"].is_lepton_real == '\x01' and sample["tree"].photon_gen_matching > 0 and sample["tree"].mjj < 400 and not (sample["tree"].mlg > 81.2 and sample["tree"].mlg < 101.2):

                if sample["tree"].gen_weight > 0:

                    for variable in variables:

                        histograms[variable].Fill(getVariable(variable,sample["tree"]),eff_scale_factor.photon_efficiency_scale_factor(sample["tree"].photon_pt,sample["tree"].photon_eta)*eff_scale_factor.electron_efficiency_scale_factor(sample["tree"].lepton_pt,sample["tree"].lepton_eta)*sample["xs"]*1000*36.15/sample["nweightedevents"])
                    #hist.Fill(tree.mjj,xs*1000*36.15/n_weighted_events)
                else:
                    for variable in variables:
                        histograms[variable].Fill(getVariable(variable,sample["tree"]),-eff_scale_factor.photon_efficiency_scale_factor(sample["tree"].photon_pt,sample["tree"].photon_eta)*eff_scale_factor.electron_efficiency_scale_factor(sample["tree"].lepton_pt,sample["tree"].lepton_eta)*sample["xs"]*1000*36.15/sample["nweightedevents"])
                    #hist.Fill(tree.mjj,-xs*1000*36.15/n_weighted_events)
        elif photon_eta_cutstring == "1.566 < abs(photon_eta) && abs(photon_eta) < 2.5":    

            if sample["tree"].lepton_pdg_id == lepton_abs_pdg_id and sample["tree"].is_lepton_tight == '\x01' and 1.566 < abs(sample["tree"].photon_eta) and abs(sample["tree"].photon_eta) < 2.5 and sample["tree"].photon_selection == 2 and sample["tree"].photon_pt > 25 and sample["tree"].photon_pt < 70 and sample["tree"].btagging_selection == btagging_selection and sample["tree"].is_lepton_real == '\x01' and sample["tree"].photon_gen_matching > 0 and sample["tree"].mjj < 400 and not (sample["tree"].mlg > 81.2 and sample["tree"].mlg < 101.2):
#            if tree.lepton_pdg_id == lepton_abs_pdg_id and tree.is_lepton_tight == '\x01' and 1.566 < abs(tree.photon_eta) and abs(tree.photon_eta) < 2.5 and tree.photon_selection == 2 and tree.photon_pt > 25 and tree.photon_pt < 70 and tree.btagging_selection == btagging_selection:

                if sample["tree"].gen_weight > 0:

                    for variable in variables:
                        histograms[variable].Fill(getVariable(variable,sample["tree"]),eff_scale_factor.photon_efficiency_scale_factor(sample["tree"].photon_pt,sample["tree"].photon_eta)*eff_scale_factor.electron_efficiency_scale_factor(sample["tree"].lepton_pt,sample["tree"].lepton_eta)*sample["xs"]*1000*36.15/sample["nweightedevents"])
#                    hist.Fill(tree.mjj,xs*1000*36.15/n_weighted_events)
                else:
                    for variable in variables:
                        histograms[variable].Fill(getVariable(variable,sample["tree"]),-eff_scale_factor.photon_efficiency_scale_factor(sample["tree"].photon_pt,sample["tree"].photon_eta)*eff_scale_factor.electron_efficiency_scale_factor(sample["tree"].lepton_pt,sample["tree"].lepton_eta)*sample["xs"]*1000*36.15/sample["nweightedevents"])
#                    hist.Fill(tree.mjj,-xs*1000*36.15/n_weighted_events)
        else:
            assert(0)

    if len(variables) > 0:        
        histograms[variables[0]].Print("all")

for i in range(data_events_tree.GetEntries()):
    data_events_tree.GetEntry(i)

#    if not pass_json(data_events_tree.run,data_events_tree.lumi):
#        continue

    if photon_eta_cutstring == "abs(photon_eta) < 1.4442":    
        if data_events_tree.lepton_pdg_id == lepton_abs_pdg_id and data_events_tree.is_lepton_tight == '\x01' and abs(data_events_tree.photon_eta) < 1.4442 and data_events_tree.photon_selection == 2 and data_events_tree.photon_pt > 25 and data_events_tree.photon_pt < 70 and data_events_tree.btagging_selection == btagging_selection and data_events_tree.mjj < 400 and not (data_events_tree.mlg > 81.2 and data_events_tree.mlg < 101.2):
            for variable in variables:
                data["hists"][variable].Fill(getVariable(variable,data_events_tree))
    elif photon_eta_cutstring == "1.566 < abs(photon_eta) && abs(photon_eta) < 2.5":    
        if data_events_tree.lepton_pdg_id == lepton_abs_pdg_id and data_events_tree.is_lepton_tight == '\x01' and 1.566 < abs(data_events_tree.photon_eta) and abs(data_events_tree.photon_eta) < 2.5 and data_events_tree.photon_selection == 2 and data_events_tree.photon_pt > 25 and data_events_tree.photon_pt < 70 and data_events_tree.btagging_selection == btagging_selection and data_events_tree.mjj < 400 and not (data_events_tree.mlg > 81.2 and data_events_tree.mlg < 101.2):
            for variable in variables:
                data["hists"][variable].Fill(getVariable(variable,data_events_tree))
    else:
        assert(0)


    if photon_eta_cutstring == "abs(photon_eta) < 1.4442":
        if data_events_tree.lepton_pdg_id == lepton_abs_pdg_id and data_events_tree.is_lepton_tight == '\x00' and abs(data_events_tree.photon_eta) < 1.4442 and (data_events_tree.photon_selection == 1 or data_events_tree.photon_selection == 0) and data_events_tree.photon_pt > 25 and data_events_tree.photon_pt < 70 and data_events_tree.btagging_selection == btagging_selection and data_events_tree.mjj < 400 and not (data_events_tree.mlg > 81.2 and data_events_tree.mlg < 101.2):        
            if lepton_name == "muon":
                for variable in variables:
                    double_fake["hists"][variable].Fill(getVariable(variable,data_events_tree),muonfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")*photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
                    fake_muon["hists"][variable].Fill(getVariable(variable,data_events_tree),-muonfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")*photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
                    fake_photon["hists"][variable].Fill(getVariable(variable,data_events_tree),-muonfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")*photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
            elif lepton_name == "electron":

                for variable in variables:
                    double_fake["hists"][variable].Fill(getVariable(variable,data_events_tree),electronfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")*photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
                    fake_electron["hists"][variable].Fill(getVariable(variable,data_events_tree),-electronfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")*photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
                    fake_photon["hists"][variable].Fill(getVariable(variable,data_events_tree),-electronfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")*photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
            else:
                assert(0)
    elif photon_eta_cutstring == "1.566 < abs(photon_eta) && abs(photon_eta) < 2.5":
        if data_events_tree.lepton_pdg_id == lepton_abs_pdg_id and data_events_tree.is_lepton_tight == '\x00' and 1.566 < abs(data_events_tree.photon_eta) and abs(data_events_tree.photon_eta) < 2.5 and (data_events_tree.photon_selection == 1 or data_events_tree.photon_selection == 0) and data_events_tree.photon_pt > 25 and data_events_tree.photon_pt < 70 and data_events_tree.btagging_selection == btagging_selection  and data_events_tree.mjj < 400 and not (data_events_tree.mlg > 81.2 and data_events_tree.mlg < 101.2):        
            if lepton_name == "muon":
                for variable in variables:
                    double_fake["hists"][variable].Fill(getVariable(variable,data_events_tree),muonfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")*photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
                    fake_muon["hists"][variable].Fill(getVariable(variable,data_events_tree),-muonfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")*photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
                    fake_photon["hists"][variable].Fill(getVariable(variable,data_events_tree),-muonfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")*photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
            elif lepton_name == "electron":

                for variable in variables:
                    double_fake["hists"][variable].Fill(getVariable(variable,data_events_tree),electronfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")*photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
                    fake_electron["hists"][variable].Fill(getVariable(variable,data_events_tree),-electronfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")*photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
                    fake_photon["hists"][variable].Fill(getVariable(variable,data_events_tree),-electronfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal")*photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
            else:
                assert(0)
    else:
        assert(0)
    
    if photon_eta_cutstring == "abs(photon_eta) < 1.4442":        
        if data_events_tree.lepton_pdg_id == lepton_abs_pdg_id and data_events_tree.is_lepton_tight == '\x00' and abs(data_events_tree.photon_eta) < 1.4442 and data_events_tree.photon_selection == 2 and data_events_tree.photon_pt > 25 and data_events_tree.photon_pt < 70  and data_events_tree.btagging_selection == btagging_selection and data_events_tree.mjj < 400 and not (data_events_tree.mlg > 81.2 and data_events_tree.mlg < 101.2):
            if lepton_name == "muon":
                for variable in variables:
                    fake_muon["hists"][variable].Fill(getVariable(variable,data_events_tree),muonfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal"))
            elif lepton_name == "electron":

                for variable in variables:
                    fake_electron["hists"][variable].Fill(getVariable(variable,data_events_tree),electronfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal"))
            else:
                assert(0)
    elif photon_eta_cutstring == "1.566 < abs(photon_eta) && abs(photon_eta) < 2.5":            
        if data_events_tree.lepton_pdg_id == lepton_abs_pdg_id and data_events_tree.is_lepton_tight == '\x00' and 1.566 < abs(data_events_tree.photon_eta) and abs(data_events_tree.photon_eta) < 2.5 and data_events_tree.photon_selection == 2 and data_events_tree.photon_pt > 25 and data_events_tree.photon_pt < 70 and data_events_tree.btagging_selection == btagging_selection  and data_events_tree.mjj < 400 and not (data_events_tree.mlg > 81.2 and data_events_tree.mlg < 101.2):
            if lepton_name == "muon":
                for variable in variables:
                    fake_muon["hists"][variable].Fill(getVariable(variable,data_events_tree),muonfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal"))
            elif lepton_name == "electron":
                for variable in variables:
                    fake_electron["hists"][variable].Fill(getVariable(variable,data_events_tree),electronfakerate(data_events_tree.lepton_eta, data_events_tree.lepton_pt,"nominal"))
            else:
                assert(0)
    else:
        assert(0)

    if photon_eta_cutstring == "abs(photon_eta) < 1.4442":        
        if data_events_tree.lepton_pdg_id == lepton_abs_pdg_id and data_events_tree.is_lepton_tight == '\x01' and abs(data_events_tree.photon_eta) < 1.4442 and (data_events_tree.photon_selection == 1 or data_events_tree.photon_selection == 0) and data_events_tree.photon_pt > 25 and data_events_tree.photon_pt < 70 and data_events_tree.btagging_selection == btagging_selection  and data_events_tree.mjj < 400 and not (data_events_tree.mlg > 81.2 and data_events_tree.mlg < 101.2):
            for variable in variables:            
                fake_photon["hists"][variable].Fill(getVariable(variable,data_events_tree),photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
    elif photon_eta_cutstring == "1.566 < abs(photon_eta) && abs(photon_eta) < 2.5":    
        if data_events_tree.lepton_pdg_id == lepton_abs_pdg_id and data_events_tree.is_lepton_tight == '\x01' and 1.566 < abs(data_events_tree.photon_eta) and abs(data_events_tree.photon_eta) < 2.5 and (data_events_tree.photon_selection == 1 or data_events_tree.photon_selection == 0) and data_events_tree.photon_pt > 25 and data_events_tree.photon_pt < 70 and data_events_tree.btagging_selection == btagging_selection  and data_events_tree.mjj < 400 and not (data_events_tree.mlg > 81.2 and data_events_tree.mlg < 101.2):
            for variable in variables:            
                fake_photon["hists"][variable].Fill(getVariable(variable,data_events_tree),photonfakerate(data_events_tree.photon_eta, data_events_tree.photon_pt,data_events_tree.lepton_pdg_id, "nominal"))
    else:
        assert(0)

for label in labels.keys():

    for sample in labels[label]["samples"]:
        fillHistogramMC(sample,labels[label]["hists"])
        if data_driven:
            subtractRealMCFromFakeEstimateFromData(sample["tree"],fake_photon,fake_muon,fake_electron,sample["xs"],sample["nweightedevents"])
        
    for variable in variables:    
        labels[label]["hists"][variable].SetFillColor(labels[label]["color"])
        labels[label]["hists"][variable].SetFillStyle(1001)
        labels[label]["hists"][variable].SetLineColor(labels[label]["color"])
    
#subtractRealMCFromFakeEstimateFromData(mc_samples[0]["tree"],fake_photon_hist,fake_muon_hist,fake_electron_hist,mc_samples[0]["xs"],mc_samples[0]["nweightedevents"])

for variable in variables:

    data["hists"][variable].Print("all")

    data["hists"][variable].SetMarkerStyle(ROOT.kFullCircle)
    data["hists"][variable].SetLineWidth(3)
    data["hists"][variable].SetLineColor(ROOT.kBlack)

    fake_photon["hists"][variable].SetFillColor(ROOT.kGray+1)
    fake_electron["hists"][variable].SetFillColor(ROOT.kAzure-1)
    fake_muon["hists"][variable].SetFillColor(ROOT.kAzure-1)
    double_fake["hists"][variable].SetFillColor(ROOT.kMagenta)

    fake_photon["hists"][variable].SetLineColor(ROOT.kGray+1)
    fake_electron["hists"][variable].SetLineColor(ROOT.kAzure-1)
    fake_muon["hists"][variable].SetLineColor(ROOT.kAzure-1)
    double_fake["hists"][variable].SetLineColor(ROOT.kMagenta)

    fake_photon["hists"][variable].SetFillStyle(1001)
    fake_electron["hists"][variable].SetFillStyle(1001)
    fake_muon["hists"][variable].SetFillStyle(1001)
    double_fake["hists"][variable].SetFillStyle(1001)

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

    for label in labels.keys():
        hsum.Add(labels[label]["hists"][variable])
        hstack.Add(labels[label]["hists"][variable])

    if data_driven:
        if lepton_name == "muon":
            hsum.Add(fake_muon["hists"][variable])
        elif lepton_name == "electron":
            hsum.Add(fake_electron["hists"][variable])
        else:
            assert(0)
        hsum.Add(fake_photon["hists"][variable])
        hsum.Add(double_fake["hists"][variable])

    if data_driven:
        if lepton_name == "muon":
            hstack.Add(fake_muon["hists"][variable])
        elif lepton_name == "electron":
            hstack.Add(fake_electron["hists"][variable])
        else:
            assert(0)
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
#fake_electron_hist.Draw("hist same")
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
            draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,fake_muon["hists"][variable],"fake muon","f")
        elif lepton_name == "electron":
            draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,fake_electron["hists"][variable],"fake electron","f")
        else:
            assert(0)
        j=j+1
        draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,fake_photon["hists"][variable],"fake photon","f")
        j=j+1
        draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,double_fake["hists"][variable],"double fake","f")

    for label in labels:
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
