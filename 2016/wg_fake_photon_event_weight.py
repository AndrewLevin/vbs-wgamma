import ROOT

from array import array

photon_ptbins=array('d', [25,30,40,50,70,100,135,400])

import json

import numpy as np

#fake_photon_event_weights = json.load(open("fake_photon_event_weights/fake_photon_event_weights_data.txt"))
fake_photon_event_weights = json.load(open("fake_photon_event_weights_data.txt"))

fake_photon_event_weights_wjets_wgjets_as_data = json.load(open("fake_photon_event_weights/fake_photon_event_weights_wjets_wgjets_as_data.txt"))

fake_photon_event_weights_wjets_wgjets = json.load(open("fake_photon_event_weights/fake_photon_event_weights_wjets_wgjets.txt"))

fake_photon_event_weights_muon_barrel = list(np.array(fake_photon_event_weights["muon_barrel"])[:,0])

fake_photon_event_weights_muon_barrel_stat_err = list(np.array(fake_photon_event_weights["muon_barrel"])[:,1])

fake_photon_event_weights_muon_endcap = list(np.array(fake_photon_event_weights["muon_endcap"])[:,0])

fake_photon_event_weights_muon_endcap_stat_err = list(np.array(fake_photon_event_weights["muon_endcap"])[:,1])

fake_photon_event_weights_electron_barrel = list(np.array(fake_photon_event_weights["electron_barrel"])[:,0])

fake_photon_event_weights_electron_barrel_stat_err = list(np.array(fake_photon_event_weights["electron_barrel"])[:,1])

fake_photon_event_weights_electron_endcap = list(np.array(fake_photon_event_weights["electron_endcap"])[:,0])

fake_photon_event_weights_electron_endcap_stat_err = list(np.array(fake_photon_event_weights["electron_endcap"])[:,1])

fake_photon_event_weights_muon_endcap_syst = [(fake_photon_event_weights_wjets_wgjets["both_endcap"][i] - fake_photon_event_weights_wjets_wgjets_as_data["both_endcap"][i] + fake_photon_event_weights_muon_endcap[i]) for i in range(0,len(fake_photon_event_weights_wjets_wgjets["both_endcap"])) ]

fake_photon_event_weights_electron_endcap_syst = [(fake_photon_event_weights_wjets_wgjets["both_endcap"][i] - fake_photon_event_weights_wjets_wgjets_as_data["both_endcap"][i] + fake_photon_event_weights_electron_endcap[i]) for i in range(0,len(fake_photon_event_weights_wjets_wgjets["both_endcap"])) ]

fake_photon_event_weights_muon_barrel_syst = [(fake_photon_event_weights_wjets_wgjets["both_barrel"][i] - fake_photon_event_weights_wjets_wgjets_as_data["both_barrel"][i] + fake_photon_event_weights_muon_barrel[i]) for i in range(0,len(fake_photon_event_weights_wjets_wgjets["both_barrel"])) ]

fake_photon_event_weights_electron_barrel_syst = [(fake_photon_event_weights_wjets_wgjets["both_barrel"][i] - fake_photon_event_weights_wjets_wgjets_as_data["both_barrel"][i] + fake_photon_event_weights_electron_barrel[i]) for i in range(0,len(fake_photon_event_weights_wjets_wgjets["both_barrel"])) ]

fake_photon_event_weights_muon_barrel_hist=ROOT.TH1F("fake_photon_event_weights_muon_barrel_hist","fake_photon_event_weights_muon_barrel_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_event_weights_electron_barrel_hist=ROOT.TH1F("fake_photon_event_weights_electron_barrel_hist","fake_photon_event_weights_electron_barrel_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_event_weights_muon_endcap_hist=ROOT.TH1F("fake_photon_event_weights_muon_endcap_hist","fake_photon_event_weights_muon_endcap_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_event_weights_electron_endcap_hist=ROOT.TH1F("fake_photon_event_weights_electron_endcap_hist","fake_photon_event_weights_electron_endcap_hist",len(photon_ptbins)-1,photon_ptbins)

fake_photon_event_weights_muon_barrel_syst_hist=ROOT.TH1F("fake_photon_event_weights_muon_barrel_syst_hist","fake_photon_event_weights_muon_barrel_syst_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_event_weights_electron_barrel_syst_hist=ROOT.TH1F("fake_photon_event_weights_electron_barrel_syst_hist","fake_photon_event_weights_electron_barrel_syst_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_event_weights_muon_endcap_syst_hist=ROOT.TH1F("fake_photon_event_weights_muon_endcap_syst_hist","fake_photon_event_weights_muon_endcap_syst_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_event_weights_electron_endcap_syst_hist=ROOT.TH1F("fake_photon_event_weights_electron_endcap_syst_hist","fake_photon_event_weights_electron_endcap_syst_hist",len(photon_ptbins)-1,photon_ptbins)

for i in range(fake_photon_event_weights_muon_barrel_hist.GetNbinsX()):
    fake_photon_event_weights_muon_barrel_hist.SetBinContent(i+1,fake_photon_event_weights_muon_barrel[i])
    fake_photon_event_weights_muon_barrel_hist.SetBinError(i+1,fake_photon_event_weights_muon_barrel_stat_err[i])
    fake_photon_event_weights_muon_barrel_syst_hist.SetBinContent(i+1,fake_photon_event_weights_muon_barrel_syst[i])

for i in range(fake_photon_event_weights_electron_barrel_hist.GetNbinsX()):
    fake_photon_event_weights_electron_barrel_hist.SetBinContent(i+1,fake_photon_event_weights_electron_barrel[i])
    fake_photon_event_weights_electron_barrel_hist.SetBinError(i+1,fake_photon_event_weights_electron_barrel_stat_err[i])
    fake_photon_event_weights_electron_barrel_syst_hist.SetBinContent(i+1,fake_photon_event_weights_electron_barrel_syst[i])

for i in range(fake_photon_event_weights_muon_endcap_hist.GetNbinsX()):
    fake_photon_event_weights_muon_endcap_hist.SetBinContent(i+1,fake_photon_event_weights_muon_endcap[i])
    fake_photon_event_weights_muon_endcap_hist.SetBinError(i+1,fake_photon_event_weights_muon_endcap_stat_err[i])
    fake_photon_event_weights_muon_endcap_syst_hist.SetBinContent(i+1,fake_photon_event_weights_muon_endcap_syst[i])

for i in range(fake_photon_event_weights_electron_endcap_hist.GetNbinsX()):
    fake_photon_event_weights_electron_endcap_hist.SetBinContent(i+1,fake_photon_event_weights_electron_endcap[i])
    fake_photon_event_weights_electron_endcap_hist.SetBinError(i+1,fake_photon_event_weights_electron_endcap_stat_err[i])
    fake_photon_event_weights_electron_endcap_syst_hist.SetBinContent(i+1,fake_photon_event_weights_electron_endcap_syst[i])

def fake_photon_event_weight(eta,pt,lepton_pdg_id,use_alt=False,stat_err_up = False):

    if abs(lepton_pdg_id) == 11:
        if abs(eta) < 1.4442:
            mypt   = min(pt,399.999)

            if not use_alt:
                fr = fake_photon_event_weights_electron_barrel_hist.GetBinContent(fake_photon_event_weights_electron_barrel_hist.GetXaxis().FindFixBin(mypt))
                if stat_err_up:
                    fr += fake_photon_event_weights_electron_barrel_hist.GetBinError(fake_photon_event_weights_electron_barrel_hist.GetXaxis().FindFixBin(mypt))
            else:    
                fr = fake_photon_event_weights_electron_barrel_syst_hist.GetBinContent(fake_photon_event_weights_electron_barrel_hist.GetXaxis().FindFixBin(mypt))
                if stat_err_up:
                    fr += fake_photon_event_weights_electron_barrel_syst_hist.GetBinError(fake_photon_event_weights_electron_barrel_hist.GetXaxis().FindFixBin(mypt))

            return fr

        elif 1.566 < abs(eta) and abs(eta) < 2.5:
            mypt   = min(pt,399.999)

            if not use_alt:
                fr = fake_photon_event_weights_electron_endcap_hist.GetBinContent(fake_photon_event_weights_electron_endcap_hist.GetXaxis().FindFixBin(mypt))
                if stat_err_up:
                    fr += fake_photon_event_weights_electron_endcap_hist.GetBinError(fake_photon_event_weights_electron_endcap_hist.GetXaxis().FindFixBin(mypt)) 
            else:
                fr = fake_photon_event_weights_electron_endcap_syst_hist.GetBinContent(fake_photon_event_weights_electron_endcap_syst_hist.GetXaxis().FindFixBin(mypt))
                if stat_err_up:
                    fr += fake_photon_event_weights_electron_endcap_syst_hist.GetBinError(fake_photon_event_weights_electron_endcap_syst_hist.GetXaxis().FindFixBin(mypt))
            return fr

        else:

            assert(0)
    elif abs(lepton_pdg_id) == 13:
        if abs(eta) < 1.4442:
            mypt   = min(pt,399.999)

            if not use_alt:
                fr = fake_photon_event_weights_muon_barrel_hist.GetBinContent(fake_photon_event_weights_muon_barrel_hist.GetXaxis().FindFixBin(mypt))
                if stat_err_up:
                    fr += fake_photon_event_weights_muon_barrel_hist.GetBinError(fake_photon_event_weights_muon_barrel_hist.GetXaxis().FindFixBin(mypt))
            else:    
                fr = fake_photon_event_weights_muon_barrel_syst_hist.GetBinContent(fake_photon_event_weights_muon_barrel_syst_hist.GetXaxis().FindFixBin(mypt))
                if stat_err_up:
                    fr = fake_photon_event_weights_muon_barrel_syst_hist.GetBinError(fake_photon_event_weights_muon_barrel_syst_hist.GetXaxis().FindFixBin(mypt))

            return fr

        elif 1.566 < abs(eta) and abs(eta) < 2.5:
            mypt   = min(pt,399.999)

            if not use_alt:
                fr = fake_photon_event_weights_muon_endcap_hist.GetBinContent(fake_photon_event_weights_muon_endcap_hist.GetXaxis().FindFixBin(mypt))
                if stat_err_up:
                    fr += fake_photon_event_weights_muon_endcap_hist.GetBinError(fake_photon_event_weights_muon_endcap_hist.GetXaxis().FindFixBin(mypt))
            else:    
                fr = fake_photon_event_weights_muon_endcap_syst_hist.GetBinContent(fake_photon_event_weights_muon_endcap_syst_hist.GetXaxis().FindFixBin(mypt))
                if stat_err_up:
                    fr += fake_photon_event_weights_muon_endcap_syst_hist.GetBinError(fake_photon_event_weights_muon_endcap_syst_hist.GetXaxis().FindFixBin(mypt))

            return fr

        else:

            assert(0)

    else:

        assert(0)
