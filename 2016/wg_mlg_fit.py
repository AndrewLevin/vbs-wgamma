import sys
import random
import ROOT

photon_eta_cutstring = "abs(photon_eta) < 1.4442"

#photon_eta_cutstring = "1.566 < abs(photon_eta) && abs(photon_eta) < 2.5"

#lepton_name = "electron"

lepton_name = "muon"

if lepton_name == "muon":
    lepton_abs_pdg_id = 13
else:
    lepton_abs_pdg_id = 11

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
#        if not (tree.mlg > 60.0 and tree.mlg < 120.0):
        if True:
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


m= ROOT.RooRealVar("m","m",0,150)
m0=ROOT.RooRealVar("m0",    "m0",0,-10,10)
sigma=ROOT.RooRealVar("sigma",  "sigma",1,0.1,5)
alpha=ROOT.RooRealVar("alpha",  "alpha",5,0,20)
n=ROOT.RooRealVar("n",          "n",1,0,10)

cb = ROOT.RooCBShape("cb", "Crystal Ball", m, m0, sigma, alpha, n)

mass = ROOT.RooRealVar("mass","mass",50,0,150)
width = ROOT.RooRealVar("width","width",5,0.1,10);    

bw = ROOT.RooBreitWigner("bw","Breit Wigner",m,mass,width)

RooFFTConvPdf_bwcb = ROOT.RooFFTConvPdf("bwcb","Breit Wigner convolved with a Crystal Ball",m,bw,cb)

#x1= ROOT.RooRealVar("x1","",-10,10) 
#beta1= ROOT.RooRealVar("beta1","beta1",0.1,3.1) 
#data1= ROOT.RooDataHist("data1","dataset with x 1",ROOT.RooArgList(x1),degree_hist) 
#powerlaw1= ROOT.RooGenericPdf("powerlaw1","x1^(-beta1)",ROOT.RooArgList(x1,beta1)) 

#c=ROOT.TCanvas("c","c")

#powerlaw1.fitTo(data1)

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

hist_mlg_data = ROOT.TH1F("mlg","mlg",100,0,150)

hist_mlg_fake_photon = ROOT.TH1F("mlg","mlg",100,0,150)

hist_mlg_fake_lepton = ROOT.TH1F("mlg","mlg",100,0,150)

hist_mlg_double_fake = ROOT.TH1F("mlg","mlg",100,0,150)

#f_data=ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/single_electron.root")

f_data=ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/single_muon.root")

t_data=f_data.Get("Events")

for i in range(0,t_data.GetEntries()):

    t_data.GetEntry(i)

    if pass_selection(t_data):
        hist_mlg_data.Fill(t_data.mlg)

    if pass_selection(t_data,True,False):

        weight = leptonfakerate(t_data.lepton_pdg_id,t_data.lepton_eta, t_data.lepton_pt,"nominal")

        hist_mlg_fake_lepton.Fill(t_data.mlg,weight)

    if pass_selection(t_data,False,True):

        weight = photonfakerate(t_data.photon_eta, t_data.photon_pt,t_data.lepton_pdg_id, "nominal")

        hist_mlg_fake_photon.Fill(t_data.mlg,weight)

    if pass_selection(t_data,True,True):

        weight = leptonfakerate(t_data.lepton_pdg_id,t_data.lepton_eta, t_data.lepton_pt,"nominal")*photonfakerate(t_data.photon_eta, t_data.photon_pt,t_data.lepton_pdg_id, "nominal")

        hist_mlg_double_fake.Fill(t_data.mlg,weight)
        hist_mlg_fake_lepton.Fill(t_data.mlg,-weight)
        hist_mlg_fake_photon.Fill(t_data.mlg,-weight)

hist_mlg_wg = ROOT.TH1F("mlg wg","mlg wg",150,0,150)

f_wg=ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/wgjets.root")

t_wg=f_wg.Get("Events")

for i in range(0,t_wg.GetEntries()):

    t_wg.GetEntry(i)

    if not pass_selection(t_wg):
        continue

    if t_wg.gen_weight > 0:
        hist_mlg_wg.Fill(t_wg.mlg)
    else:    
        hist_mlg_wg.Fill(t_wg.mlg,-1)

hist_mlg_zg = ROOT.TH1F("mlg zg","mlg zg",150,0,150)

f_zg=ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/zglowmlljets.root")

t_zg=f_zg.Get("Events")

for i in range(0,t_zg.GetEntries()):

    t_zg.GetEntry(i)

    if not pass_selection(t_zg):
        continue

    if t_zg.gen_weight > 0:
        hist_mlg_zg.Fill(t_zg.mlg)
    else:    
        hist_mlg_zg.Fill(t_zg.mlg,-1)

data = ROOT.RooDataHist("data","dataset",ROOT.RooArgList(m),hist_mlg_data)

RooDataHist_mlg_wg = ROOT.RooDataHist("wg data hist","wg data hist",ROOT.RooArgList(m),hist_mlg_wg)

RooHistPdf_wg = ROOT.RooHistPdf("wg","wg",ROOT.RooArgSet(m),RooDataHist_mlg_wg)

RooDataHist_mlg_zg = ROOT.RooDataHist("zg data hist","zg data hist",ROOT.RooArgList(m),hist_mlg_zg)

RooHistPdf_zg = ROOT.RooHistPdf("zg","zg",ROOT.RooArgSet(m),RooDataHist_mlg_zg)

RooDataHist_mlg_fake_lepton = ROOT.RooDataHist("zg data hist","zg data hist",ROOT.RooArgList(m),hist_mlg_fake_lepton)

RooHistPdf_fake_lepton = ROOT.RooHistPdf("fake lepton","fake lepton",ROOT.RooArgSet(m),RooDataHist_mlg_fake_lepton)

RooDataHist_mlg_fake_photon = ROOT.RooDataHist("zg data hist","zg data hist",ROOT.RooArgList(m),hist_mlg_fake_photon)

RooHistPdf_fake_photon = ROOT.RooHistPdf("fake photon","fake photon",ROOT.RooArgSet(m),RooDataHist_mlg_fake_photon)

RooDataHist_mlg_double_fake = ROOT.RooDataHist("zg data hist","zg data hist",ROOT.RooArgList(m),hist_mlg_double_fake)

RooHistPdf_double_fake = ROOT.RooHistPdf("double fake","double fake",ROOT.RooArgSet(m),RooDataHist_mlg_double_fake)


wg_norm = ROOT.RooRealVar("wg_norm","wg_norm",0,1000000);    
zg_norm = ROOT.RooRealVar("zg_norm","zg_norm",0,1000000);    
bwcb_norm = ROOT.RooRealVar("bwcb_norm","bwcb_norm",0,1000000);    
fake_lepton_norm = ROOT.RooRealVar("fake_lepton_norm","fake_lepton_norm",hist_mlg_fake_lepton.Integral(),hist_mlg_fake_lepton.Integral());    
fake_photon_norm = ROOT.RooRealVar("fake_photon_norm","fake_photon_norm",hist_mlg_fake_photon.Integral(),hist_mlg_fake_photon.Integral());    
double_fake_norm = ROOT.RooRealVar("double_fake_norm","double_fake_norm",hist_mlg_double_fake.Integral(),hist_mlg_double_fake.Integral());    

#wg = ROOT.RooExtendPdf("wg","wg",RooHistPdf_wg,wg_norm)

#zg = ROOT.RooExtendPdf("wg","wg",RooHistPdf_zg,zg_norm)

#bwcb = ROOT.RooExtendPdf("bwcb","bwcb",RooFFTConvPdf_bwcb,bwcb_norm)

n1=ROOT.RooRealVar("n1","n1",0.1,0.01,100000)
n2=ROOT.RooRealVar("n2","n2",0.1,0.01,100000)

f= ROOT.RooRealVar("f","f",0.5,0.,1.) ;

#sum=ROOT.RooAddPdf("sum","sum",ROOT.RooArgList(wg,bwcb),RooArgList(n1,n2))
#sum=ROOT.RooAddPdf("sum","sum",wg,bwcb,f)

#sum=ROOT.RooAddPdf("sum","sum",ROOT.RooArgList(wg,zg,bwcb),RooArgList(wg_norm,zg_norm,bwcb_norm))
#sum=ROOT.RooAddPdf("sum","sum",ROOT.RooArgList(RooHistPdf_wg,RooHistPdf_zg,RooFFTConvPdf_bwcb,RooHistPdf_fake_lepton,RooHistPdf_fake_photon,RooHistPdf_double_fake),ROOT.RooArgList(wg_norm,zg_norm,bwcb_norm,fake_lepton_norm,fake_photon_norm,double_fake_norm))

sum=ROOT.RooAddPdf("sum","sum",ROOT.RooArgList(RooHistPdf_wg,RooHistPdf_zg,RooHistPdf_fake_lepton,RooHistPdf_fake_photon,RooHistPdf_double_fake),ROOT.RooArgList(wg_norm,zg_norm,fake_lepton_norm,fake_photon_norm,double_fake_norm))

sum.fitTo(data,ROOT.RooFit.Extended())

frame = m.frame()

data.plotOn(frame)
sum.plotOn(frame)
#sum.plotOn(frame, ROOT.RooFit.Components(ROOT.RooArgSet(sum.getComponents()["zg"])),ROOT.RooFit.LineStyle(ROOT.kDashed)) 
#sum.plotOn(frame, ROOT.RooFit.Components("zg,wg,bwcb"),ROOT.RooFit.LineStyle(ROOT.kDashed)) 
sum.plotOn(frame, ROOT.RooFit.Components("wg"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kRed)) 
sum.plotOn(frame, ROOT.RooFit.Components("zg"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kGreen)) 

wg_norm.Print("all")
zg_norm.Print("all")
bwcb_norm.Print("all")
fake_lepton_norm.Print("all")
fake_photon_norm.Print("all")
double_fake_norm.Print("all")

frame.SetTitle("")
frame.GetYaxis().SetTitle("")
frame.Draw()


raw_input()
