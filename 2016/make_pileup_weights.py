import ROOT

fmc = ROOT.TFile("PileupWeights2016.root","NEW")
fdata = ROOT.TFile("/afs/cern.ch/user/a/amlevin/PileupData2016Observed.root","READ") #pileupCalc.py -i /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt --inputLumiJSON /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/pileup_latest.txt  --calcMode observed --minBiasXsec 69200 --maxPileupBin 70 --numPileupBins 70  PileupData2016Observed.root


data_hist = fdata.Get("pileup") 

mc_hist=ROOT.TH1D("mc","mc",70,0,70)

mc_hist.Sumw2()
data_hist.Sumw2()

tchain = ROOT.TChain("Events")

tchain.Add("/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/00CB3868-B166-E811-926C-A0369FD0B1FE.root")
tchain.Add("/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/0252C3ED-9F66-E811-9E46-0025905B85DE.root")
tchain.Add("/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/08F74682-9B66-E811-A6F5-0CC47A4D75F4.root")
tchain.Add("/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/12B7972F-B066-E811-94CF-002590E7DDE6.root")
tchain.Add("/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/20D2E131-6366-E811-A2F9-0CC47ABD6C6C.root")
tchain.Add("/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/2CB977C4-D366-E811-B0E7-F4E9D4AEC940.root")
tchain.Add("/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/8CF45655-D266-E811-AFB0-0CC47A1DF806.root")
tchain.Add("/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/927F1543-6366-E811-84E9-0025905A6070.root")
tchain.Add("/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/A0BF21E0-7A66-E811-A6A0-0CC47A7C3636.root")
tchain.Add("/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/BCB6497A-9B66-E811-88B7-0CC47A7C349C.root")
tchain.Add("/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/C4D0FA76-5D66-E811-A00C-0CC47A4D76C6.root")
tchain.Add("/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/C689CE02-C066-E811-BE54-0CC47A7C3628.root")
tchain.Add("/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/C8DFB777-7366-E811-890F-0CC47A4D7674.root")
tchain.Add("/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/D4E600EA-9F66-E811-9E19-A0369FE2C0D0.root")
tchain.Add("/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/DA3D01B4-5066-E811-AC03-0025905A497A.root")
tchain.Add("/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/E675F33F-4D66-E811-9A8D-0025905B85DC.root")
tchain.Add("/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/E6F2574C-D766-E811-B047-0CC47ABB518A.root")

#tchain.Add("/afs/cern.ch/work/a/amlevin/data/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/DA18896D-9B13-E811-9130-FA163E250C6C.root") 
#tchain.Add("/afs/cern.ch/work/a/amlevin/data/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/CAAD3AD2-6913-E811-BC8B-FA163E4B02D6.root") 
#tchain.Add("/afs/cern.ch/work/a/amlevin/data/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/D2F703D8-AC13-E811-A914-02163E017C6D.root") 

tchain.Draw("Pileup_nPU >> mc")

fmc.cd()

mc_hist2 = mc_hist.Clone("mc")
data_hist2 = data_hist.Clone("data")

data_hist2.Write()

data_hist3 = data_hist.Clone("ratio")

mc_hist2.Scale(1/mc_hist2.Integral())
data_hist3.Scale(1/data_hist3.Integral())

data_hist3.Divide(mc_hist2)

data_hist3.Write()
mc_hist2.Write()
