#if running on a dtmit machine, you need to move to root version 5.34.20 or higher
#source /afs/cern.ch/sw/lcg/external/gcc/4.7.2/x86_64-slc5-gcc47-opt/setup.sh
#source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.20/x86_64-slc5-gcc47-opt/root/bin/thisroot.sh

import math

import json

import sys

#otherwise, root will parse the command line options, see here http://root.cern.ch/phpBB3/viewtopic.php?f=14&t=18637
sys.argv = []

from ROOT import *

from array import array

gStyle.SetOptStat(0)

felectronout=TFile("electron_frs.root","recreate")
fmuonout=TFile("muon_frs.root","recreate")

electron_data_samples = []

#electron_data_samples = [{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/single_electron_fake_electron.root"}]

#electron_data_samples = [{"filename" : "/eos/cms/store/user/amlevin/SingleElectron/wg-fake-lepton-2016/190831_122802/0000/tree_11.root"}]

electron_mc_samples = []

#electron_mc_samples = [{"filename" : "/afs/cern.ch/work/a/amlevin/tmp/wjets_fake_lepton.root", "xs" : 60430.0, "subtract" : True},{"filename" : "/afs/cern.ch/work/a/amlevin/tmp/zjets_fake_lepton.root", "xs" : 4963.0, "subtract" : True}]

#electron_mc_samples = [{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/wjets_fake_electron.root", "xs" : 60430.0, "subtract" : True},{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/zjets_fake_electron.root", "xs" : 4963.0, "subtract" : True}]

#electron_mc_samples = [{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/qcd_bctoe_170250.root", "xs" : 2608, "subtract" : False},{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/qcd_bctoe_2030.root", "xs" : 363100, "subtract" : False},{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/qcd_bctoe_250.root", "xs" : 722.6, "subtract" : False},{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/qcd_bctoe_3080.root", "xs" : 417800, "subtract" : False},{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/qcd_bctoe_80170.root", "xs" : 39860, "subtract" : False}]

muon_data_samples = [{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/single_muon_fake_lepton.root"}]

muon_mc_samples = []

#muon_data_samples = [{"filename" : "/afs/cern.ch/work/a/amlevin/tmp/single_muon_fake_lepton.root"}]

#muon_mc_samples = [{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/wjets_fake_lepton.root", "xs" : 60430.0, "subtract" : True},{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/zjets_fake_lepton.root", "xs" : 4963.0, "subtract" : True}]

#muon_mc_samples = [{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/wjets_fake_muon.root", "xs" : 60430.0, "subtract" : True},{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/zjets_fake_muon.root", "xs" : 4963.0, "subtract" : True}]

#muon_mc_samples = [{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/wjets_fake_muon.root", "xs" : 60430.0, "subtract" : True},{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/zjets_fake_muon.root", "xs" : 4963.0, "subtract" : True}]

#muon_mc_samples = [{"filename" : "/afs/cern.ch/work/a/amlevin/tmp/wjets_fake_lepton.root", "xs" : 60430.0, "subtract" : True},{"filename" : "/afs/cern.ch/work/a/amlevin/tmp/zjets_fake_lepton.root", "xs" : 4963.0, "subtract" : True}]

electron_ptbins=array('d', [30,40,50])
electron_etabins=array('d', [0,0.5,1,1.479,2.0,2.5])

loose_electron_th2d=TH2F("loose_electron_hist","loose_electron_hist",len(electron_etabins)-1,electron_etabins,len(electron_ptbins)-1,electron_ptbins)
tight_electron_th2d=TH2F("tight_electron_hist","tight_electron_hist",len(electron_etabins)-1,electron_etabins,len(electron_ptbins)-1,electron_ptbins)

loose_electron_th2d.Sumw2()
tight_electron_th2d.Sumw2()

muon_ptbins=array('d', [25,30,40,50])    
muon_etabins=array('d', [0,0.5,1.0,1.479,2.0,2.5])

loose_muon_th2d=TH2F("loose_muon_hist","loose_muon_hist",len(muon_etabins)-1,muon_etabins,len(muon_ptbins)-1,muon_ptbins)
tight_muon_th2d=TH2F("tight_muon_hist","tight_muon_hist",len(muon_etabins)-1,muon_etabins,len(muon_ptbins)-1,muon_ptbins)

loose_muon_th2d.Sumw2()
tight_muon_th2d.Sumw2()

def fill_loose_and_tight_th2ds(tree,tight_th2d,loose_th2d,abspdgid,xs_weight = None):
    for entry in range(tree.GetEntries()):
        tree.GetEntry(entry)

        if entry % 100000 == 0:
            print entry

        if abs(tree.lepton_pdgid) != abspdgid:
            continue

        if tree.met > 30 or tree.mt > 20:
            continue

        if xs_weight:
            weight = xs_weight
        else:
            weight = 1.0

        if tree.gen_weight < 0:
            weight = -weight

        if (tree.is_lepton_tight == '\x01'):

#            print str(tree.run) + " " + str(tree.lumi) + " " + str(tree.event)

            if tree.lepton_pt > tight_th2d.GetYaxis().GetBinUpEdge(tight_th2d.GetYaxis().GetNbins()):
                tight_th2d.Fill(abs(tree.lepton_eta),tight_th2d.GetYaxis().GetBinCenter(tight_th2d.GetYaxis().GetNbins()),weight)
            else:
                tight_th2d.Fill(abs(tree.lepton_eta),tree.lepton_pt,weight)

        else:
            
            if tree.lepton_pt > loose_th2d.GetYaxis().GetBinUpEdge(loose_th2d.GetYaxis().GetNbins()):
                loose_th2d.Fill(abs(tree.lepton_eta),loose_th2d.GetYaxis().GetBinCenter(loose_th2d.GetYaxis().GetNbins()),weight)
            else:    
                loose_th2d.Fill(abs(tree.lepton_eta),tree.lepton_pt,weight)

for sample in electron_data_samples:
    f = TFile.Open(sample["filename"])
    t = f.Get("Events")
    fill_loose_and_tight_th2ds(t,tight_electron_th2d,loose_electron_th2d,11)

for sample in electron_mc_samples:
    f = TFile.Open(sample["filename"])
    t = f.Get("Events")
    n_weighted_events = f.Get("nEventsGenWeighted").GetBinContent(1)
    if sample["subtract"]:
        fill_loose_and_tight_th2ds(t,tight_electron_th2d,loose_electron_th2d,11,-sample["xs"]*1000*35.9/n_weighted_events)
    else:
        fill_loose_and_tight_th2ds(t,tight_electron_th2d,loose_electron_th2d,11,sample["xs"]*1000*35.9/n_weighted_events)

for sample in muon_data_samples:
    f = TFile.Open(sample["filename"])
    t = f.Get("Events")
    fill_loose_and_tight_th2ds(t,tight_muon_th2d,loose_muon_th2d,13)

for sample in muon_mc_samples:
    f = TFile.Open(sample["filename"])
    t = f.Get("Events")
    n_weighted_events = f.Get("nEventsGenWeighted").GetBinContent(1)
    if sample["subtract"]:
        fill_loose_and_tight_th2ds(t,tight_muon_th2d,loose_muon_th2d,13,-sample["xs"]*1000*35.9/n_weighted_events)
    else:
        fill_loose_and_tight_th2ds(t,tight_muon_th2d,loose_muon_th2d,13,sample["xs"]*1000*35.9/n_weighted_events)

felectronout.cd()

tight_electron_th2d.Clone().Write()
loose_electron_th2d.Clone().Write()

loose_electron_th2d.Add(tight_electron_th2d)
    
tight_electron_th2d.Divide(loose_electron_th2d)
tight_electron_th2d.Clone("electron_frs").Write()

fmuonout.cd()

tight_muon_th2d.Clone().Write()
loose_muon_th2d.Clone().Write()

loose_muon_th2d.Add(tight_muon_th2d)
    
tight_muon_th2d.Divide(loose_muon_th2d)
tight_muon_th2d.Clone("muon_frs").Write()
