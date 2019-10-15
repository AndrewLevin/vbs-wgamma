import ROOT

#from https://twiki.cern.ch/twiki/bin/view/CMS/EgammaIDRecipesRun2#Efficiencies_and_scale_factors and https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffsRun2

photon_id_2016_sf_filename = "eff_scale_factors/2016/Fall17V2_2016_Medium_photons.root"
photon_id_2016_sf_file = ROOT.TFile(photon_id_2016_sf_filename,"read")
photon_id_2016_sf = photon_id_2016_sf_file.Get("EGamma_SF2D")

photon_id_2017_sf_filename = "eff_scale_factors/2017/2017_PhotonsMedium.root"
photon_id_2017_sf_file = ROOT.TFile(photon_id_2017_sf_filename,"read")
photon_id_2017_sf = photon_id_2017_sf_file.Get("EGamma_SF2D")

photon_id_2018_sf_filename = "eff_scale_factors/2018/2018_PhotonsMedium.root"
photon_id_2018_sf_file = ROOT.TFile(photon_id_2018_sf_filename,"read")
photon_id_2018_sf = photon_id_2018_sf_file.Get("EGamma_SF2D")

electron_id_2016_sf_filename = "eff_scale_factors/2016/2016LegacyReReco_ElectronMedium_Fall17V2.root"
electron_id_2016_sf_file = ROOT.TFile(electron_id_2016_sf_filename,"read")
electron_id_2016_sf = electron_id_2016_sf_file.Get("EGamma_SF2D")

electron_id_2017_sf_filename = "eff_scale_factors/2017/2017_ElectronMedium.root"
electron_id_2017_sf_file = ROOT.TFile(electron_id_2017_sf_filename,"read")
electron_id_2017_sf = electron_id_2017_sf_file.Get("EGamma_SF2D")

electron_id_2018_sf_filename = "eff_scale_factors/2018/2018_ElectronMedium.root"
electron_id_2018_sf_file = ROOT.TFile(electron_id_2018_sf_filename,"read")
electron_id_2018_sf = electron_id_2018_sf_file.Get("EGamma_SF2D")

electron_reco_2016_sf_filename = "eff_scale_factors/2016/EGM2D_BtoH_GT20GeV_RecoSF_Legacy2016.root"
electron_reco_2016_sf_file = ROOT.TFile(electron_reco_2016_sf_filename,"read")
electron_reco_2016_sf = electron_reco_2016_sf_file.Get("EGamma_SF2D")

electron_reco_2017_sf_filename = "eff_scale_factors/2017/egammaEffi.txt_EGM2D_runBCDEF_passingRECO.root"
electron_reco_2017_sf_file = ROOT.TFile(electron_reco_2017_sf_filename,"read")
electron_reco_2017_sf = electron_reco_2017_sf_file.Get("EGamma_SF2D")

electron_reco_2018_sf_filename = "eff_scale_factors/2018/egammaEffi.txt_EGM2D_updatedAll.root"
electron_reco_2018_sf_file = ROOT.TFile(electron_reco_2018_sf_filename,"read")
electron_reco_2018_sf = electron_reco_2018_sf_file.Get("EGamma_SF2D")

muon_iso_2016_sf_filename = "eff_scale_factors/2016/RunBCDEF_SF_ISO.root"
muon_iso_2016_sf_file = ROOT.TFile(muon_iso_2016_sf_filename,"read")
muon_iso_2016 = muon_iso_2016_sf_file.Get("NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta")


muon_id_2016_sf_filename = "eff_scale_factors/2016/RunBCDEF_SF_ID.root"
muon_id_2016_sf_file = ROOT.TFile(muon_id_2016_sf_filename,"read")
muon_id_2016 = muon_id_2016_sf_file.Get("NUM_TightID_DEN_genTracks_pt_abseta")


muon_iso_2017_sf_filename = "eff_scale_factors/2017/RunBCDEF_SF_ISO.root"
muon_iso_2017_sf_file = ROOT.TFile(muon_iso_2017_sf_filename,"read")
muon_iso_2017 = muon_iso_2017_sf_file.Get("NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta")


muon_id_2017_sf_filename = "eff_scale_factors/2017/RunBCDEF_SF_ID.root"
muon_id_2017_sf_file = ROOT.TFile(muon_id_2017_sf_filename,"read")
muon_id_2017 = muon_id_2017_sf_file.Get("NUM_TightID_DEN_genTracks_pt_abseta")


muon_iso_2018_sf_filename = "eff_scale_factors/2018/RunABCD_SF_ISO.root"
muon_iso_2018_sf_file = ROOT.TFile(muon_iso_2018_sf_filename,"read")
muon_iso_2018 = muon_iso_2018_sf_file.Get("NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta")


muon_id_2018_sf_filename = "eff_scale_factors/2018/RunABCD_SF_ID.root"
muon_id_2018_sf_file = ROOT.TFile(muon_id_2018_sf_filename,"read")
muon_id_2018 = muon_id_2018_sf_file.Get("NUM_TightID_DEN_genTracks_pt_abseta")




def electron_efficiency_scale_factor(pt,eta,year,id_err_up=False,reco_err_up=False):

    if year == "2016":
        electron_reco_sf = electron_reco_2016_sf
        electron_id_sf = electron_id_2016_sf
    elif year == "2017":
        electron_reco_sf = electron_reco_2017_sf
        electron_id_sf = electron_id_2017_sf
    elif year == "2018":
        electron_reco_sf = electron_reco_2018_sf
        electron_id_sf = electron_id_2018_sf
    else:
        assert(0)


    #the reco 2D histogram is really a 1D histogram
    sf_id=electron_id_sf.GetBinContent(electron_id_sf.GetXaxis().FindFixBin(eta),electron_id_sf.GetYaxis().FindFixBin(pt))
    if id_err_up:
        sf_id+=electron_id_sf.GetBinError(electron_id_sf.GetXaxis().FindFixBin(eta),electron_id_sf.GetYaxis().FindFixBin(pt))

    sf_reco=electron_reco_sf.GetBinContent(electron_reco_sf.GetXaxis().FindFixBin(eta),1)

    if reco_err_up:
        sf_reco+=electron_reco_sf.GetBinError(electron_reco_sf.GetXaxis().FindFixBin(eta),1) 
    
    return sf_id*sf_reco

def photon_efficiency_scale_factor(pt,eta,year,err_up=False):

    if year == "2016":
        photon_id_sf = photon_id_2016_sf
    elif year == "2017":
        photon_id_sf = photon_id_2017_sf
    elif year == "2018":
        photon_id_sf = photon_id_2018_sf
    else:
        assert(0)

    sf = photon_id_sf.GetBinContent(photon_id_sf.GetXaxis().FindFixBin(eta),photon_id_sf.GetYaxis().FindFixBin(pt))

    if err_up:
        sf += photon_id_sf.GetBinError(photon_id_sf.GetXaxis().FindFixBin(eta),photon_id_sf.GetYaxis().FindFixBin(pt))

    return sf

def muon_efficiency_scale_factor(pt,eta,year,iso_err_up=False,id_err_up=False):

    if year == "2016":
        muon_iso_sf = muon_iso_2016_sf
        muon_id_sf = muon_id_2016_sf
    elif year == "2017":
        muon_iso_sf = muon_iso_2017_sf
        muon_id_sf = muon_id_2017_sf
    elif year == "2018":
        muon_iso_sf = muon_iso_2018_sf
        muon_id_sf = muon_id_2018_sf
    else:
        assert(0)

    iso_sf = muon_iso_sf.GetBinContent(muon_iso_sf.GetXaxis().FindFixBin(abs(eta)),muon_iso_sf.GetYaxis().FindFixBin(min(pt,muon_iso_sf.GetYaxis().GetBinCenter(muon_id_sf.GetNbinsY()))))

    if iso_err_up:
        iso_sf += muon_iso_sf.GetBinError(muon_iso_sf.GetXaxis().FindFixBin(abs(eta)),muon_iso_sf.GetYaxis().FindFixBin(min(pt,muon_iso_sf.GetYaxis().GetBinCenter(muon_id_sf.GetNbinsY()))))

    id_sf = muon_id_sf.GetBinContent(muon_id_sf.GetXaxis().FindFixBin(abs(eta)),muon_id_sf.GetYaxis().FindFixBin(min(pt,muon_id_sf.GetYaxis().GetBinCenter(muon_id_sf.GetNbinsY())))) 
    
    if id_err_up:
        id_sf += muon_id_sf.GetBinError(muon_id_sf.GetXaxis().FindFixBin(abs(eta)),muon_id_sf.GetYaxis().FindFixBin(min(pt,muon_id_sf.GetYaxis().GetBinCenter(muon_id_sf.GetNbinsY())))) 

    return iso_sf * id_sf

#print electron_efficiency_scale_factor(25,0.7)
