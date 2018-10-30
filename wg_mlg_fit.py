import sys
import random
import ROOT

met_hist=ROOT.TH1F("","",100,0,100)

m= ROOT.RooRealVar("m","m",0,100)
m0=ROOT.RooRealVar("m0",    "m0",0,-10,10)
sigma=ROOT.RooRealVar("sigma",  "sigma",1,0.1,5)
alpha=ROOT.RooRealVar("alpha",  "alpha",5,0,20)
n=ROOT.RooRealVar("n",          "n",1,0,10)

cb = ROOT.RooCBShape("cb", "Crystal Ball", m, m0, sigma, alpha, n)

mass = ROOT.RooRealVar("mass","mass",50,0,100)
width = ROOT.RooRealVar("width","width",5,0.1,10);    

bw = ROOT.RooBreitWigner("bw","Breit Wigner",m,mass,width)

bwcb = ROOT.RooFFTConvPdf("bwcb","Breit Wigner convolved with a Crystal Ball",m,bw,cb)

#x1= ROOT.RooRealVar("x1","",-10,10) 
#beta1= ROOT.RooRealVar("beta1","beta1",0.1,3.1) 
#data1= ROOT.RooDataHist("data1","dataset with x 1",ROOT.RooArgList(x1),degree_hist) 
#powerlaw1= ROOT.RooGenericPdf("powerlaw1","x1^(-beta1)",ROOT.RooArgList(x1,beta1)) 

#c=ROOT.TCanvas("c","c")

#powerlaw1.fitTo(data1)

hist_mlg_data = ROOT.TH1F("mlg","mlg",100,0,100)

f_data=ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/single_electron.root")

t_data=f_data.Get("Events")

for i in range(0,t_data.GetEntries()):
    hist_mlg_data.Fill(t_data.mlg)

hist_mlg_wg = ROOT.TH1F("mlg wg","mlg wg",100,0,100)

f_wg=ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/wgjets.root")

t_wg=f_wg.Get("Events")

for i in range(0,t_wg.GetEntries()):
    if t_wg.gen_weight > 0:
        hist_mlg_wg.Fill(t_wg.mlg)
    else:    
        hist_mlg_wg.Fill(t_wg.mlg,-1)

RooDataHist_mlg_wg = ROOT.RooDataHist("wg data hist","wg data hist",ROOT.RooArgList(m),hist_mlg_wg)

data = ROOT.RooDataHist("data","dataset",ROOT.RooArgList(m),hist_mlg_data)

wg = ROOT.RooHistPdf("wg","wg",ROOT.RooArgSet(m),RooDataHist_mlg_wg)

n1=ROOT.RooRealVar("n1","n1",0.1,0.01,100000)
n2=ROOT.RooRealVar("n2","n2",0.1,0.01,100000)

f= ROOT.RooRealVar("f","f",0.5,0.,1.) ;

#sum=ROOT.RooAddPdf("sum","sum",ROOT.RooArgList(wg,bwcb),RooArgList(n1,n2))
sum=ROOT.RooAddPdf("sum","sum",wg,bwcb,f)

sum.fitTo(data)
