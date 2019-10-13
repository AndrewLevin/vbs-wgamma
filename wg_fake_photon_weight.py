import ROOT

from array import array

#photon_ptbins=array('d', [20,25,30,40,50,70,100,135,400])
photon_ptbins=array('d', [20,25,30,40,50,400])

import json

import numpy as np

#fake_photon_weights = json.load(open("fake_photon_weights/fake_photon_weights_data.txt"))
#fake_photon_weights = json.load(open("fake_photon_weights_data_recoil.txt"))
#fake_photon_weights = json.load(open("fake_photon_weights_data_recoil.txt"))
#fake_photon_weights = json.load(open("fake_photon_weights_data.txt"))
#fake_photon_weights = json.load(open("fake_photon_weights_data_0jets.txt"))
fake_photon_weights = json.load(open("fake_photon_weights_data_0jets_recoil.txt"))

fake_photon_weights_wjets_wgjets_as_data = json.load(open("fake_photon_weights/fake_photon_weights_wjets_wgjets_as_data.txt"))

fake_photon_weights_wjets_wgjets = json.load(open("fake_photon_weights/fake_photon_weights_wjets_wgjets.txt"))

#fake_photon_weights_wjets_wgjets_as_data = json.load(open("fake_photon_weights_data.txt"))

#fake_photon_weights_wjets_wgjets = json.load(open("fake_photon_weights_data.txt"))

fake_photon_weights_muon_barrel_recoil0 = list(np.array(fake_photon_weights["muon_barrel_recoil0"])[:,0])

fake_photon_weights_muon_barrel_recoil0_stat_err = list(np.array(fake_photon_weights["muon_barrel_recoil0"])[:,1])

fake_photon_weights_muon_endcap_recoil0 = list(np.array(fake_photon_weights["muon_endcap_recoil0"])[:,0])

fake_photon_weights_muon_endcap_recoil0_stat_err = list(np.array(fake_photon_weights["muon_endcap_recoil0"])[:,1])

fake_photon_weights_electron_barrel_recoil0 = list(np.array(fake_photon_weights["electron_barrel_recoil0"])[:,0])

fake_photon_weights_electron_barrel_recoil0_stat_err = list(np.array(fake_photon_weights["electron_barrel_recoil0"])[:,1])

fake_photon_weights_electron_endcap_recoil0 = list(np.array(fake_photon_weights["electron_endcap_recoil0"])[:,0])

fake_photon_weights_electron_endcap_recoil0_stat_err = list(np.array(fake_photon_weights["electron_endcap_recoil0"])[:,1])

fake_photon_weights_muon_barrel_recoil1 = list(np.array(fake_photon_weights["muon_barrel_recoil1"])[:,0])

fake_photon_weights_muon_barrel_recoil1_stat_err = list(np.array(fake_photon_weights["muon_barrel_recoil1"])[:,1])

fake_photon_weights_muon_endcap_recoil1 = list(np.array(fake_photon_weights["muon_endcap_recoil1"])[:,0])

fake_photon_weights_muon_endcap_recoil1_stat_err = list(np.array(fake_photon_weights["muon_endcap_recoil1"])[:,1])

fake_photon_weights_electron_barrel_recoil1 = list(np.array(fake_photon_weights["electron_barrel_recoil1"])[:,0])

fake_photon_weights_electron_barrel_recoil1_stat_err = list(np.array(fake_photon_weights["electron_barrel_recoil1"])[:,1])

fake_photon_weights_electron_endcap_recoil1 = list(np.array(fake_photon_weights["electron_endcap_recoil1"])[:,0])

fake_photon_weights_electron_endcap_recoil1_stat_err = list(np.array(fake_photon_weights["electron_endcap_recoil1"])[:,1])

fake_photon_weights_muon_barrel_recoil2 = list(np.array(fake_photon_weights["muon_barrel_recoil2"])[:,0])

fake_photon_weights_muon_barrel_recoil2_stat_err = list(np.array(fake_photon_weights["muon_barrel_recoil2"])[:,1])

fake_photon_weights_muon_endcap_recoil2 = list(np.array(fake_photon_weights["muon_endcap_recoil2"])[:,0])

fake_photon_weights_muon_endcap_recoil2_stat_err = list(np.array(fake_photon_weights["muon_endcap_recoil2"])[:,1])

fake_photon_weights_electron_barrel_recoil2 = list(np.array(fake_photon_weights["electron_barrel_recoil2"])[:,0])

fake_photon_weights_electron_barrel_recoil2_stat_err = list(np.array(fake_photon_weights["electron_barrel_recoil2"])[:,1])

fake_photon_weights_electron_endcap_recoil2 = list(np.array(fake_photon_weights["electron_endcap_recoil2"])[:,0])

fake_photon_weights_electron_endcap_recoil2_stat_err = list(np.array(fake_photon_weights["electron_endcap_recoil2"])[:,1])

fake_photon_weights_muon_barrel_recoil3 = list(np.array(fake_photon_weights["muon_barrel_recoil3"])[:,0])

fake_photon_weights_muon_barrel_recoil3_stat_err = list(np.array(fake_photon_weights["muon_barrel_recoil3"])[:,1])

fake_photon_weights_muon_endcap_recoil3 = list(np.array(fake_photon_weights["muon_endcap_recoil3"])[:,0])

fake_photon_weights_muon_endcap_recoil3_stat_err = list(np.array(fake_photon_weights["muon_endcap_recoil3"])[:,1])

fake_photon_weights_electron_barrel_recoil3 = list(np.array(fake_photon_weights["electron_barrel_recoil3"])[:,0])

fake_photon_weights_electron_barrel_recoil3_stat_err = list(np.array(fake_photon_weights["electron_barrel_recoil3"])[:,1])

fake_photon_weights_electron_endcap_recoil3 = list(np.array(fake_photon_weights["electron_endcap_recoil3"])[:,0])

fake_photon_weights_electron_endcap_recoil3_stat_err = list(np.array(fake_photon_weights["electron_endcap_recoil3"])[:,1])

fake_photon_weights_muon_barrel_recoil0_hist=ROOT.TH1F("fake_photon_weights_muon_barrel_recoil0_hist","fake_photon_weights_muon_barrel_recoil0_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_weights_electron_barrel_recoil0_hist=ROOT.TH1F("fake_photon_weights_electron_barrel_recoil0_hist","fake_photon_weights_electron_barrel_recoil0_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_weights_muon_endcap_recoil0_hist=ROOT.TH1F("fake_photon_weights_muon_endcap_recoil0_hist","fake_photon_weights_muon_endcap_recoil0_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_weights_electron_endcap_recoil0_hist=ROOT.TH1F("fake_photon_weights_electron_endcap_recoil0_hist","fake_photon_weights_electron_endcap_recoil0_hist",len(photon_ptbins)-1,photon_ptbins)

fake_photon_weights_muon_barrel_recoil1_hist=ROOT.TH1F("fake_photon_weights_muon_barrel_recoil1_hist","fake_photon_weights_muon_barrel_recoil1_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_weights_electron_barrel_recoil1_hist=ROOT.TH1F("fake_photon_weights_electron_barrel_recoil1_hist","fake_photon_weights_electron_barrel_recoil1_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_weights_muon_endcap_recoil1_hist=ROOT.TH1F("fake_photon_weights_muon_endcap_recoil1_hist","fake_photon_weights_muon_endcap_recoil1_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_weights_electron_endcap_recoil1_hist=ROOT.TH1F("fake_photon_weights_electron_endcap_recoil1_hist","fake_photon_weights_electron_endcap_recoil1_hist",len(photon_ptbins)-1,photon_ptbins)

fake_photon_weights_muon_barrel_recoil2_hist=ROOT.TH1F("fake_photon_weights_muon_barrel_recoil2_hist","fake_photon_weights_muon_barrel_recoil2_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_weights_electron_barrel_recoil2_hist=ROOT.TH1F("fake_photon_weights_electron_barrel_recoil2_hist","fake_photon_weights_electron_barrel_recoil2_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_weights_muon_endcap_recoil2_hist=ROOT.TH1F("fake_photon_weights_muon_endcap_recoil2_hist","fake_photon_weights_muon_endcap_recoil2_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_weights_electron_endcap_recoil2_hist=ROOT.TH1F("fake_photon_weights_electron_endcap_recoil2_hist","fake_photon_weights_electron_endcap_recoil2_hist",len(photon_ptbins)-1,photon_ptbins)

fake_photon_weights_muon_barrel_recoil3_hist=ROOT.TH1F("fake_photon_weights_muon_barrel_recoil3_hist","fake_photon_weights_muon_barrel_recoil3_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_weights_electron_barrel_recoil3_hist=ROOT.TH1F("fake_photon_weights_electron_barrel_recoil3_hist","fake_photon_weights_electron_barrel_recoil3_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_weights_muon_endcap_recoil3_hist=ROOT.TH1F("fake_photon_weights_muon_endcap_recoil3_hist","fake_photon_weights_muon_endcap_recoil3_hist",len(photon_ptbins)-1,photon_ptbins)
fake_photon_weights_electron_endcap_recoil3_hist=ROOT.TH1F("fake_photon_weights_electron_endcap_recoil3_hist","fake_photon_weights_electron_endcap_recoil3_hist",len(photon_ptbins)-1,photon_ptbins)

for i in range(fake_photon_weights_muon_barrel_recoil0_hist.GetNbinsX()):
    fake_photon_weights_muon_barrel_recoil0_hist.SetBinContent(i+1,fake_photon_weights_muon_barrel_recoil0[i])
    fake_photon_weights_muon_barrel_recoil0_hist.SetBinError(i+1,fake_photon_weights_muon_barrel_recoil0_stat_err[i])

for i in range(fake_photon_weights_electron_barrel_recoil0_hist.GetNbinsX()):
    fake_photon_weights_electron_barrel_recoil0_hist.SetBinContent(i+1,fake_photon_weights_electron_barrel_recoil0[i])
    fake_photon_weights_electron_barrel_recoil0_hist.SetBinError(i+1,fake_photon_weights_electron_barrel_recoil0_stat_err[i])

for i in range(fake_photon_weights_muon_endcap_recoil0_hist.GetNbinsX()):
    fake_photon_weights_muon_endcap_recoil0_hist.SetBinContent(i+1,fake_photon_weights_muon_endcap_recoil0[i])
    fake_photon_weights_muon_endcap_recoil0_hist.SetBinError(i+1,fake_photon_weights_muon_endcap_recoil0_stat_err[i])

for i in range(fake_photon_weights_electron_endcap_recoil0_hist.GetNbinsX()):
    fake_photon_weights_electron_endcap_recoil0_hist.SetBinContent(i+1,fake_photon_weights_electron_endcap_recoil0[i])
    fake_photon_weights_electron_endcap_recoil0_hist.SetBinError(i+1,fake_photon_weights_electron_endcap_recoil0_stat_err[i])

for i in range(fake_photon_weights_muon_barrel_recoil1_hist.GetNbinsX()):
    fake_photon_weights_muon_barrel_recoil1_hist.SetBinContent(i+1,fake_photon_weights_muon_barrel_recoil1[i])
    fake_photon_weights_muon_barrel_recoil1_hist.SetBinError(i+1,fake_photon_weights_muon_barrel_recoil1_stat_err[i])

for i in range(fake_photon_weights_electron_barrel_recoil1_hist.GetNbinsX()):
    fake_photon_weights_electron_barrel_recoil1_hist.SetBinContent(i+1,fake_photon_weights_electron_barrel_recoil1[i])
    fake_photon_weights_electron_barrel_recoil1_hist.SetBinError(i+1,fake_photon_weights_electron_barrel_recoil1_stat_err[i])

for i in range(fake_photon_weights_muon_endcap_recoil1_hist.GetNbinsX()):
    fake_photon_weights_muon_endcap_recoil1_hist.SetBinContent(i+1,fake_photon_weights_muon_endcap_recoil1[i])
    fake_photon_weights_muon_endcap_recoil1_hist.SetBinError(i+1,fake_photon_weights_muon_endcap_recoil1_stat_err[i])

for i in range(fake_photon_weights_electron_endcap_recoil1_hist.GetNbinsX()):
    fake_photon_weights_electron_endcap_recoil1_hist.SetBinContent(i+1,fake_photon_weights_electron_endcap_recoil1[i])
    fake_photon_weights_electron_endcap_recoil1_hist.SetBinError(i+1,fake_photon_weights_electron_endcap_recoil1_stat_err[i])

for i in range(fake_photon_weights_muon_barrel_recoil2_hist.GetNbinsX()):
    fake_photon_weights_muon_barrel_recoil2_hist.SetBinContent(i+1,fake_photon_weights_muon_barrel_recoil2[i])
    fake_photon_weights_muon_barrel_recoil2_hist.SetBinError(i+1,fake_photon_weights_muon_barrel_recoil2_stat_err[i])

for i in range(fake_photon_weights_electron_barrel_recoil2_hist.GetNbinsX()):
    fake_photon_weights_electron_barrel_recoil2_hist.SetBinContent(i+1,fake_photon_weights_electron_barrel_recoil2[i])
    fake_photon_weights_electron_barrel_recoil2_hist.SetBinError(i+1,fake_photon_weights_electron_barrel_recoil2_stat_err[i])

for i in range(fake_photon_weights_muon_endcap_recoil2_hist.GetNbinsX()):
    fake_photon_weights_muon_endcap_recoil2_hist.SetBinContent(i+1,fake_photon_weights_muon_endcap_recoil2[i])
    fake_photon_weights_muon_endcap_recoil2_hist.SetBinError(i+1,fake_photon_weights_muon_endcap_recoil2_stat_err[i])

for i in range(fake_photon_weights_electron_endcap_recoil2_hist.GetNbinsX()):
    fake_photon_weights_electron_endcap_recoil2_hist.SetBinContent(i+1,fake_photon_weights_electron_endcap_recoil2[i])
    fake_photon_weights_electron_endcap_recoil2_hist.SetBinError(i+1,fake_photon_weights_electron_endcap_recoil2_stat_err[i])

for i in range(fake_photon_weights_muon_barrel_recoil3_hist.GetNbinsX()):
    fake_photon_weights_muon_barrel_recoil3_hist.SetBinContent(i+1,fake_photon_weights_muon_barrel_recoil3[i])
    fake_photon_weights_muon_barrel_recoil3_hist.SetBinError(i+1,fake_photon_weights_muon_barrel_recoil3_stat_err[i])

for i in range(fake_photon_weights_electron_barrel_recoil3_hist.GetNbinsX()):
    fake_photon_weights_electron_barrel_recoil3_hist.SetBinContent(i+1,fake_photon_weights_electron_barrel_recoil3[i])
    fake_photon_weights_electron_barrel_recoil3_hist.SetBinError(i+1,fake_photon_weights_electron_barrel_recoil3_stat_err[i])

for i in range(fake_photon_weights_muon_endcap_recoil3_hist.GetNbinsX()):
    fake_photon_weights_muon_endcap_recoil3_hist.SetBinContent(i+1,fake_photon_weights_muon_endcap_recoil3[i])
    fake_photon_weights_muon_endcap_recoil3_hist.SetBinError(i+1,fake_photon_weights_muon_endcap_recoil3_stat_err[i])

for i in range(fake_photon_weights_electron_endcap_recoil3_hist.GetNbinsX()):
    fake_photon_weights_electron_endcap_recoil3_hist.SetBinContent(i+1,fake_photon_weights_electron_endcap_recoil3[i])
    fake_photon_weights_electron_endcap_recoil3_hist.SetBinError(i+1,fake_photon_weights_electron_endcap_recoil3_stat_err[i])

def fake_photon_weight(eta,pt,year,recoil,lepton_pdg_id,use_alt=False,stat_err_up = False):

    assert(year == "2016" or year == "2017" or year == "2018")

    if use_alt:
        return 0

    if abs(lepton_pdg_id) == 11:
        if abs(eta) < 1.4442:
            mypt   = min(pt,399.999)

            if not use_alt:
                if recoil < 0:
                    fr = fake_photon_weights_electron_barrel_recoil0_hist.GetBinContent(fake_photon_weights_electron_barrel_recoil0_hist.GetXaxis().FindFixBin(mypt))
                    if stat_err_up:
                        fr += fake_photon_weights_electron_barrel_recoil0_hist.GetBinError(fake_photon_weights_electron_barrel_recoil0_hist.GetXaxis().FindFixBin(mypt))
                elif recoil > 0 and recoil < 25:
                    fr = fake_photon_weights_electron_barrel_recoil1_hist.GetBinContent(fake_photon_weights_electron_barrel_recoil1_hist.GetXaxis().FindFixBin(mypt))
                    if stat_err_up:
                        fr += fake_photon_weights_electron_barrel_recoil1_hist.GetBinError(fake_photon_weights_electron_barrel_recoil1_hist.GetXaxis().FindFixBin(mypt))
                elif recoil > 25 and recoil < 10000:
                    fr = fake_photon_weights_electron_barrel_recoil2_hist.GetBinContent(fake_photon_weights_electron_barrel_recoil2_hist.GetXaxis().FindFixBin(mypt))
                    if stat_err_up:
                        fr += fake_photon_weights_electron_barrel_recoil2_hist.GetBinError(fake_photon_weights_electron_barrel_recoil2_hist.GetXaxis().FindFixBin(mypt))
                elif recoil > 10000:
                    fr = fake_photon_weights_electron_barrel_recoil3_hist.GetBinContent(fake_photon_weights_electron_barrel_recoil3_hist.GetXaxis().FindFixBin(mypt))
                    if stat_err_up:
                        fr += fake_photon_weights_electron_barrel_recoil3_hist.GetBinError(fake_photon_weights_electron_barrel_recoil3_hist.GetXaxis().FindFixBin(mypt))
                else:
                    assert(0)
                        
        elif 1.566 < abs(eta) and abs(eta) < 2.5:
            mypt   = min(pt,399.999)

            if not use_alt:
                if recoil < 0:
                    fr = fake_photon_weights_electron_endcap_recoil0_hist.GetBinContent(fake_photon_weights_electron_endcap_recoil0_hist.GetXaxis().FindFixBin(mypt))
                    if stat_err_up:
                        fr += fake_photon_weights_electron_endcap_recoil0_hist.GetBinError(fake_photon_weights_electron_endcap_recoil0_hist.GetXaxis().FindFixBin(mypt)) 
                elif recoil > 0 and recoil < 25:
                    fr = fake_photon_weights_electron_endcap_recoil1_hist.GetBinContent(fake_photon_weights_electron_endcap_recoil1_hist.GetXaxis().FindFixBin(mypt))
                    if stat_err_up:
                        fr += fake_photon_weights_electron_endcap_recoil1_hist.GetBinError(fake_photon_weights_electron_endcap_recoil1_hist.GetXaxis().FindFixBin(mypt)) 
                elif recoil > 25 and recoil < 10000:
                    fr = fake_photon_weights_electron_endcap_recoil2_hist.GetBinContent(fake_photon_weights_electron_endcap_recoil2_hist.GetXaxis().FindFixBin(mypt))
                    if stat_err_up:
                        fr += fake_photon_weights_electron_endcap_recoil2_hist.GetBinError(fake_photon_weights_electron_endcap_recoil2_hist.GetXaxis().FindFixBin(mypt)) 
                elif recoil > 10000:
                    fr = fake_photon_weights_electron_endcap_recoil3_hist.GetBinContent(fake_photon_weights_electron_endcap_recoil3_hist.GetXaxis().FindFixBin(mypt))
                    if stat_err_up:
                        fr += fake_photon_weights_electron_endcap_recoil3_hist.GetBinError(fake_photon_weights_electron_endcap_recoil3_hist.GetXaxis().FindFixBin(mypt)) 
                else:
                    assert(0)

        else:

            assert(0)
    elif abs(lepton_pdg_id) == 13:
        if abs(eta) < 1.4442:
            mypt   = min(pt,399.999)

            if not use_alt:
                if recoil < 0:
                    fr = fake_photon_weights_muon_barrel_recoil0_hist.GetBinContent(fake_photon_weights_muon_barrel_recoil0_hist.GetXaxis().FindFixBin(mypt))
                    if stat_err_up:
                        fr += fake_photon_weights_muon_barrel_recoil0_hist.GetBinError(fake_photon_weights_muon_barrel_recoil0_hist.GetXaxis().FindFixBin(mypt))
                elif recoil > 0 and recoil < 25:
                    fr = fake_photon_weights_muon_barrel_recoil1_hist.GetBinContent(fake_photon_weights_muon_barrel_recoil1_hist.GetXaxis().FindFixBin(mypt))

                    if stat_err_up:
                        fr += fake_photon_weights_muon_barrel_recoil1_hist.GetBinError(fake_photon_weights_muon_barrel_recoil1_hist.GetXaxis().FindFixBin(mypt))
                elif recoil > 25 and recoil < 10000:
                    fr = fake_photon_weights_muon_barrel_recoil2_hist.GetBinContent(fake_photon_weights_muon_barrel_recoil2_hist.GetXaxis().FindFixBin(mypt))
                    if stat_err_up:
                        fr += fake_photon_weights_muon_barrel_recoil2_hist.GetBinError(fake_photon_weights_muon_barrel_recoil2_hist.GetXaxis().FindFixBin(mypt))
                elif recoil > 10000:
                    fr = fake_photon_weights_muon_barrel_recoil3_hist.GetBinContent(fake_photon_weights_muon_barrel_recoil3_hist.GetXaxis().FindFixBin(mypt))
                    if stat_err_up:
                        fr += fake_photon_weights_muon_barrel_recoil3_hist.GetBinError(fake_photon_weights_muon_barrel_recoil3_hist.GetXaxis().FindFixBin(mypt))
                else:
                    assert(0)
                    
        elif 1.566 < abs(eta) and abs(eta) < 2.5:
            mypt   = min(pt,399.999)

            if not use_alt:
                if recoil < 0:
                    fr = fake_photon_weights_muon_endcap_recoil0_hist.GetBinContent(fake_photon_weights_muon_endcap_recoil0_hist.GetXaxis().FindFixBin(mypt))
                    if stat_err_up:
                        fr += fake_photon_weights_muon_endcap_recoil0_hist.GetBinError(fake_photon_weights_muon_endcap_recoil0_hist.GetXaxis().FindFixBin(mypt))
                elif recoil > 0 and recoil < 25:
                    fr = fake_photon_weights_muon_endcap_recoil1_hist.GetBinContent(fake_photon_weights_muon_endcap_recoil1_hist.GetXaxis().FindFixBin(mypt))
                    if stat_err_up:
                        fr += fake_photon_weights_muon_endcap_recoil1_hist.GetBinError(fake_photon_weights_muon_endcap_recoil1_hist.GetXaxis().FindFixBin(mypt))
                elif recoil > 25 and recoil < 10000:
                    fr = fake_photon_weights_muon_endcap_recoil2_hist.GetBinContent(fake_photon_weights_muon_endcap_recoil2_hist.GetXaxis().FindFixBin(mypt))
                    if stat_err_up:
                        fr += fake_photon_weights_muon_endcap_recoil2_hist.GetBinError(fake_photon_weights_muon_endcap_recoil2_hist.GetXaxis().FindFixBin(mypt))
                elif recoil > 10000:
                    fr = fake_photon_weights_muon_endcap_recoil3_hist.GetBinContent(fake_photon_weights_muon_endcap_recoil3_hist.GetXaxis().FindFixBin(mypt))
                    if stat_err_up:
                        fr += fake_photon_weights_muon_endcap_recoil3_hist.GetBinError(fake_photon_weights_muon_endcap_recoil3_hist.GetXaxis().FindFixBin(mypt))
                else:
                    assert(0)

        else:
            assert(0)

    else:
        assert(0)

#    if recoil < -40:
#        fr *= 0.5
#    elif recoil < -30:
#        fr *= 0.5
#    elif recoil < 0:
#        fr *= 0.5
#    elif recoil < 10:
#        fr *= 1.5
#    elif recoil < 20:
#        fr *= 1.2
#    elif recoil < 30:
#        fr *= 2
#    elif recoil < 40:
#        fr *= 1.2
#    elif recoil < 50:
#        fr *= 2
#    elif recoil < 30:
#        fr *= 1.5
#    elif recoil < 70:
#        fr *= 1.6

#    fr = 2.5   # < 0
#    fr = 1   # 0 to 25
#    fr = 0.1   # > 25


#    if abs(eta) > 1.44420:
#        fr *= 0




#    if recoil > 10000000:
#        fr*=0

#    print fr    

    if recoil > 50:
        fr = 0.5
    else:
        fr= 6
    fr = 3    
#    fr = 0.3    

    if pt < 30 and pt > 20:
        fr = 0.14729547518579378
    elif pt > 30 and pt < 40:
        fr = 0.11421925541775203
    elif pt > 40 and pt < 50:    
        fr = 0.08524097588993211
    elif pt > 50 and pt < 70:    
        fr = 0.06762542220878368
    elif pt > 70 and pt < 100:    
        fr = 0.05914284150149269
    elif pt > 100 and pt < 135:    
        fr = 0.05021945953690191
    elif pt > 135:    
        fr = 0.034507727771907866
    else:
        assert(0)

#    if pt < 30 and pt > 20:
#        fr = 0.15815616294972137
#    elif pt > 30 and pt < 40:
#        fr = 0.11842631687103078
#    elif pt > 40 and pt < 50:    
#        fr = 0.09497972627136668
#    elif pt > 50 and pt < 70:    
#        fr = 0.07704098055808917
#    elif pt > 70 and pt < 100:    
#        fr = 0.06705033604293814
#    elif pt > 100 and pt < 135:    
#        fr = 0.04910700253820312
#    elif pt > 135:    
#        fr = 0.037116405772666686
#    else:
#        assert(0)

#    fr = 0.5    


    if year == "2016":    
        #endcap    
        if pt < 25 and pt > 20:
            fr = 1.5383973288814694
        elif pt > 25 and pt < 30:
            fr = 1.4621359223300974
        elif pt > 30 and pt < 40:    
            fr = 1.6657681940700806
        elif pt > 40 and pt < 50:    
            fr = 1.6692307692307695
        elif pt > 50:
            fr = 1.7142857142857144
        else:
            assert(0)

        #barrel    
        if pt < 25 and pt > 20:
            fr = 0.64333202972233083
        elif pt > 25 and pt < 30:
            fr = 0.78677685950413223
        elif pt > 30 and pt < 40:    
            fr = 0.88131515637530078
        elif pt > 40 and pt < 50:    
            fr = 0.82677165354330717
        elif pt > 50:
            fr = 0.6672694394213381
        else:
            assert(0)
    if year == "2017" or year == "2018":        
        #endcap    
        if pt < 25 and pt > 20:
            fr = 0.58333333333333337
        elif pt > 25 and pt < 30:
            fr = 0.77329192546583847
        elif pt > 30 and pt < 40:    
            fr = 0.7567567567567568
        elif pt > 40 and pt < 50:    
            fr = 0.70114942528735624
        elif pt > 50:
            fr = 0.91228070175438603
        else:
            assert(0)

        #barrel    
        if pt < 25 and pt > 20:
            fr = 0.62626801922050179
        elif pt > 25 and pt < 30:
            fr = 0.77074542897327702
        elif pt > 30 and pt < 40:    
            fr = 0.94819819819819828
        elif pt > 40 and pt < 50:    
            fr = 0.90853658536585358
        elif pt > 50:
            fr = 0.72781065088757391
        else:
            assert(0)

#    fr *= 1.50    

#    fr *= 15    

    return fr
