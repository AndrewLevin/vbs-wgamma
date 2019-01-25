import ROOT

muon_fr_file = ROOT.TFile("/afs/cern.ch/user/a/amlevin/wg/2016/muon_frs_data_subtract_wjets_zjets.root")
electron_fr_file = ROOT.TFile("/afs/cern.ch/user/a/amlevin/wg/2016/electron_frs_data_subtract_wjets_zjets.root")

muon_fr_hist=muon_fr_file.Get("muon_frs")
electron_fr_hist=electron_fr_file.Get("electron_frs")

def fake_muon_event_weight(eta,pt,syst):

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

def fake_electron_event_weight(eta,pt,syst):
    
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

def fake_lepton_event_weight(lepton_abs_pdg_id,eta,pt,syst):
    if lepton_abs_pdg_id == 11:
        return fake_electron_event_weight(eta,pt,syst)
    elif lepton_abs_pdg_id == 13:
        return fake_muon_event_weight(eta,pt,syst)
    else:
        assert(0)
