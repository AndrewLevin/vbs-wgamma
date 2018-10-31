import sys
import random
import ROOT

photon_eta_cutstring = "abs(photon_eta) < 1.4442"

lepton_name = "electron"

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

hist_mlg_data = ROOT.TH1F("mlg","mlg",100,0,150)

f_data=ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/single_electron.root")

t_data=f_data.Get("Events")

for i in range(0,t_data.GetEntries()):

    t_data.GetEntry(i)

    if not pass_selection(t_data):
        continue

    hist_mlg_data.Fill(t_data.mlg)

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

f_zg=ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/zgjets.root")

t_zg=f_wg.Get("Events")

for i in range(0,t_zg.GetEntries()):

    t_zg.GetEntry(i)

    if not pass_selection(t_zg):
        continue

    if t_zg.gen_weight > 0:
        hist_mlg_wg.Fill(t_zg.mlg)
    else:    
        hist_mlg_wg.Fill(t_zg.mlg,-1)

data = ROOT.RooDataHist("data","dataset",ROOT.RooArgList(m),hist_mlg_data)

RooDataHist_mlg_wg = ROOT.RooDataHist("wg data hist","wg data hist",ROOT.RooArgList(m),hist_mlg_wg)

RooHistPdf_wg = ROOT.RooHistPdf("wg","wg",ROOT.RooArgSet(m),RooDataHist_mlg_wg)

RooDataHist_mlg_zg = ROOT.RooDataHist("zg data hist","zg data hist",ROOT.RooArgList(m),hist_mlg_zg)

RooHistPdf_zg = ROOT.RooHistPdf("zg","zg",ROOT.RooArgSet(m),RooDataHist_mlg_zg)

wg_norm = ROOT.RooRealVar("wg_norm","wg_norm",0,1000000);    
zg_norm = ROOT.RooRealVar("zg_norm","zg_norm",0,1000000);    
bwcb_norm = ROOT.RooRealVar("bwcb_norm","bwcb_norm",0,1000000);    

#wg = ROOT.RooExtendPdf("wg","wg",RooHistPdf_wg,wg_norm)

#zg = ROOT.RooExtendPdf("wg","wg",RooHistPdf_zg,zg_norm)

#bwcb = ROOT.RooExtendPdf("bwcb","bwcb",RooFFTConvPdf_bwcb,bwcb_norm)

n1=ROOT.RooRealVar("n1","n1",0.1,0.01,100000)
n2=ROOT.RooRealVar("n2","n2",0.1,0.01,100000)

f= ROOT.RooRealVar("f","f",0.5,0.,1.) ;

#sum=ROOT.RooAddPdf("sum","sum",ROOT.RooArgList(wg,bwcb),RooArgList(n1,n2))
#sum=ROOT.RooAddPdf("sum","sum",wg,bwcb,f)

#sum=ROOT.RooAddPdf("sum","sum",ROOT.RooArgList(wg,zg,bwcb),RooArgList(wg_norm,zg_norm,bwcb_norm))
sum=ROOT.RooAddPdf("sum","sum",ROOT.RooArgList(RooHistPdf_wg,RooHistPdf_zg,RooFFTConvPdf_bwcb),ROOT.RooArgList(wg_norm,zg_norm,bwcb_norm))

sum.fitTo(data,ROOT.RooFit.Extended())

frame = m.frame()

print "andrew debug 1"

sum.Print("all")

print "andrew debug 2"

sum.printCompactTree()

print "andrew debug 3"

sum.getComponents().Print("all")

print "andrew debug 4"

sum.getComponents()["wg"].Print("all")

print "andrew debug 5"

sum.getComponents()["zg"].Print("all")

print "andrew debug 6"

data.plotOn(frame)
sum.plotOn(frame)
#sum.plotOn(frame, ROOT.RooFit.Components(ROOT.RooArgSet(sum.getComponents()["zg"])),ROOT.RooFit.LineStyle(ROOT.kDashed)) 
#sum.plotOn(frame, ROOT.RooFit.Components("zg,wg,bwcb"),ROOT.RooFit.LineStyle(ROOT.kDashed)) 
sum.plotOn(frame, ROOT.RooFit.Components("bwcb"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kRed)) 


frame.SetTitle("")
frame.GetYaxis().SetTitle("")
frame.Draw()


raw_input()
