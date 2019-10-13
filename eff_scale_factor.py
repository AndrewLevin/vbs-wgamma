import ROOT

#from https://twiki.cern.ch/twiki/bin/view/CMS/EgammaIDRecipesRun2#Efficiencies_and_scale_factors and https://twiki.cern.ch/twiki/bin/view/CMS/MuonWorkInProgressAndPagResults

photon_id_sf_filename = "egammaEffi.txt_EGM2D.root.photon.id"

photon_id_sf_file = ROOT.TFile(photon_id_sf_filename,"read")

photon_id_sf = photon_id_sf_file.Get("EGamma_SF2D")

electron_id_sf_filename = "egammaEffi.txt_EGM2D.root.electron.id"

electron_id_sf_file = ROOT.TFile(electron_id_sf_filename,"read")

electron_id_sf = electron_id_sf_file.Get("EGamma_SF2D")

electron_reco_sf_filename = "egammaEffi.txt_EGM2D.root.electron.reco"

electron_reco_sf_file = ROOT.TFile(electron_reco_sf_filename,"read")

electron_reco_sf = electron_reco_sf_file.Get("EGamma_SF2D")

muon_iso_sf_filename = "EfficienciesAndSF_GH.root.iso"

muon_iso_sf_file = ROOT.TFile(muon_iso_sf_filename,"read")

muon_iso_sf_file.cd("TightISO_TightID_pt_eta")

muon_iso_sf = muon_iso_sf_file.Get("TightISO_TightID_pt_eta/abseta_pt_ratio")

muon_id_sf_filename = "EfficienciesAndSF_GH.root.id"

muon_id_sf_file = ROOT.TFile(muon_id_sf_filename,"read")

muon_id_sf_file.cd("MC_NUM_TightID_DEN_genTracks_PAR_pt_eta")

muon_id_sf = muon_id_sf_file.Get("MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio")

def electron_efficiency_scale_factor(pt,eta,id_err_up=False,reco_err_up=False):

    #the reoc 2D histogram is really a 1D histogram

    sf_id=electron_id_sf.GetBinContent(electron_id_sf.GetXaxis().FindFixBin(eta),electron_id_sf.GetYaxis().FindFixBin(pt))
    if id_err_up:
        sf_id+=electron_id_sf.GetBinError(electron_id_sf.GetXaxis().FindFixBin(eta),electron_id_sf.GetYaxis().FindFixBin(pt))

    sf_reco=electron_reco_sf.GetBinContent(electron_reco_sf.GetXaxis().FindFixBin(eta),1)

    if reco_err_up:
        sf_reco+=electron_reco_sf.GetBinError(electron_reco_sf.GetXaxis().FindFixBin(eta),1) 
    
    return sf_id*sf_reco

def photon_efficiency_scale_factor(pt,eta,err_up=False):

    sf = photon_id_sf.GetBinContent(photon_id_sf.GetXaxis().FindFixBin(eta),photon_id_sf.GetYaxis().FindFixBin(pt))

    if err_up:
        sf += photon_id_sf.GetBinError(photon_id_sf.GetXaxis().FindFixBin(eta),photon_id_sf.GetYaxis().FindFixBin(pt))

    return sf

def muon_efficiency_scale_factor(pt,eta,iso_err_up=False,id_err_up=False):

    iso_sf = muon_iso_sf.GetBinContent(muon_iso_sf.GetXaxis().FindFixBin(abs(eta)),muon_iso_sf.GetYaxis().FindFixBin(min(pt,muon_iso_sf.GetYaxis().GetBinCenter(muon_id_sf.GetNbinsY()))))

    if iso_err_up:
        iso_sf += muon_iso_sf.GetBinError(muon_iso_sf.GetXaxis().FindFixBin(abs(eta)),muon_iso_sf.GetYaxis().FindFixBin(min(pt,muon_iso_sf.GetYaxis().GetBinCenter(muon_id_sf.GetNbinsY()))))

    id_sf = muon_id_sf.GetBinContent(muon_id_sf.GetXaxis().FindFixBin(abs(eta)),muon_id_sf.GetYaxis().FindFixBin(min(pt,muon_id_sf.GetYaxis().GetBinCenter(muon_id_sf.GetNbinsY())))) 
    
    if id_err_up:
        id_sf += muon_id_sf.GetBinError(muon_id_sf.GetXaxis().FindFixBin(abs(eta)),muon_id_sf.GetYaxis().FindFixBin(min(pt,muon_id_sf.GetYaxis().GetBinCenter(muon_id_sf.GetNbinsY())))) 

    return iso_sf * id_sf

#print electron_efficiency_scale_factor(25,0.7)
