import ROOT

muon_2016_fr_file = ROOT.TFile("/afs/cern.ch/user/a/amlevin/wg/fake_lepton_weights/muon_2016_frs.root")
electron_2016_fr_file = ROOT.TFile("/afs/cern.ch/user/a/amlevin/wg/fake_lepton_weights/electron_2016_frs.root")

muon_2017_fr_file = ROOT.TFile("/afs/cern.ch/user/a/amlevin/wg/fake_lepton_weights/muon_2017_frs.root")
electron_2017_fr_file = ROOT.TFile("/afs/cern.ch/user/a/amlevin/wg/fake_lepton_weights/electron_2017_frs.root")

muon_2018_fr_file = ROOT.TFile("/afs/cern.ch/user/a/amlevin/wg/fake_lepton_weights/muon_2018_frs.root")
electron_2018_fr_file = ROOT.TFile("/afs/cern.ch/user/a/amlevin/wg/fake_lepton_weights/electron_2018_frs.root")

muon_2016_fr_hist=muon_2016_fr_file.Get("muon_frs")
electron_2016_fr_hist=electron_2016_fr_file.Get("electron_frs")

muon_2017_fr_hist=muon_2017_fr_file.Get("muon_frs")
electron_2017_fr_hist=electron_2017_fr_file.Get("electron_frs")

muon_2018_fr_hist=muon_2018_fr_file.Get("muon_frs")
electron_2018_fr_hist=electron_2018_fr_file.Get("electron_frs")

def fake_muon_weight(eta,pt,year,syst):

    if year == "2016":
        muon_fr_hist = muon_2016_fr_hist
    elif year == "2017":    
        muon_fr_hist = muon_2017_fr_hist
    elif year == "2018":    
        muon_fr_hist = muon_2018_fr_hist
    else:
        assert(0)

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

def fake_electron_weight(eta,pt,year,syst):
    
    if year == "2016":
        electron_fr_hist = electron_2016_fr_hist
    elif year == "2017":    
        electron_fr_hist = electron_2017_fr_hist
    elif year == "2018":    
        electron_fr_hist = electron_2018_fr_hist
    else:
        assert(0)

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

def fake_lepton_weight(lepton_abs_pdg_id,eta,pt,year,syst):
    if lepton_abs_pdg_id == 11:
        return fake_electron_weight(eta,pt,year,syst)
    elif lepton_abs_pdg_id == 13:
        return fake_muon_weight(eta,pt,year,syst)
    else:
        assert(0)
