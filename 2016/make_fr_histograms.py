#if running on a dtmit machine, you need to move to root version 5.34.20 or higher
#source /afs/cern.ch/sw/lcg/external/gcc/4.7.2/x86_64-slc5-gcc47-opt/setup.sh
#source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.20/x86_64-slc5-gcc47-opt/root/bin/thisroot.sh

import math

import json

import optparse

parser = optparse.OptionParser()

parser.add_option('--muon_data_input_filename', help='filename of the input muon ntuple', dest='finmuondataname')
parser.add_option('--electron_data_input_filename', help='filename of the input electron ntuple', dest='finelectrondataname')
parser.add_option('--electron_mc_input_filename1', help='filename of the input mc electron ntuple', dest='finelectronmcname1')
parser.add_option('--electron_mc_input_filename2', help='filename of the input mc electron ntuple', dest='finelectronmcname2')
parser.add_option('--muon_mc_input_filename1', help='filename of the input mc muon ntuple', dest='finmuonmcname1')
parser.add_option('--muon_mc_input_filename2', help='filename of the input mc muon ntuple', dest='finmuonmcname2')
parser.add_option('-o', '--output_filename', help='filename of the output ntuple', dest='foutname', default='my_file.root')
parser.add_option('--mod', help='only use every mod events', dest='mod', default=1)
parser.add_option('--debug', help='print out information about the events that pass', dest='debug', default=False)

(options,args) = parser.parse_args()

#assert(options.finmuondataname != None)
#assert(options.finelectrondataname != None)

import sys

#otherwise, root will parse the command line options, see here http://root.cern.ch/phpBB3/viewtopic.php?f=14&t=18637
sys.argv = []

from ROOT import *

from array import array

gStyle.SetOptStat(0)

foutname=options.foutname

fout=TFile("electron_closure_test_frs.root","recreate")

electron_data_samples = [{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/single_electron_fake_electron.root"}]

electron_mc_samples = [{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/wjets_fake_electron.root", "xs" : 60430.0, "subtract" : True},{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/zjets_fake_electron.root", "xs" : 4963.0, "subtract" : True}]

#electron_mc_samples = [{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/qcd_bctoe_170250.root", "xs" : 2608, "subtract" : False},{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/qcd_bctoe_2030.root", "xs" : 363100, "subtract" : False},{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/qcd_bctoe_250.root", "xs" : 722.6, "subtract" : False},{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/qcd_bctoe_3080.root", "xs" : 417800, "subtract" : False},{"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/qcd_bctoe_80170.root", "xs" : 39860, "subtract" : False}]

electron_ptbins=array('d', [30,40,50])
electron_etabins=array('d', [0,0.5,1,1.479,2.0,2.5])

loose_electron_th2d=TH2F("loose_electron_hist","loose_electron_hist",len(electron_etabins)-1,electron_etabins,len(electron_ptbins)-1,electron_ptbins)
tight_electron_th2d=TH2F("tight_electron_hist","tight_electron_hist",len(electron_etabins)-1,electron_etabins,len(electron_ptbins)-1,electron_ptbins)

loose_electron_th2d.Sumw2()
tight_electron_th2d.Sumw2()

def fill_loose_and_tight_th2ds(tree,tight_th2d,loose_th2d,xs_weight = None):
    for entry in range(tree.GetEntries()):
        tree.GetEntry(entry)

        if entry % 100000 == 0:
            print entry

        if entry % int(options.mod) != 0:
            continue

        if xs_weight:
            weight = xs_weight
        else:
            weight = 1

        if tree.gen_weight < 0:
            weight = -weight

        if (tree.is_lepton_tight == '\x01'):
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
    fill_loose_and_tight_th2ds(t,tight_electron_th2d,loose_electron_th2d,1.0)

for sample in electron_mc_samples:
    f = TFile.Open(sample["filename"])
    t = f.Get("Events")
    n_weighted_events = f.Get("nWeightedEvents").GetBinContent(1)
    if sample["subtract"]:
        fill_loose_and_tight_th2ds(t,tight_electron_th2d,loose_electron_th2d,-sample["xs"]*1000*35.9/n_weighted_events)
    else:
        fill_loose_and_tight_th2ds(t,tight_electron_th2d,loose_electron_th2d,sample["xs"]*1000*35.9/n_weighted_events)

fout.cd()

tight_electron_th2d.Clone().Write()
loose_electron_th2d.Clone().Write()

loose_electron_th2d.Add(tight_electron_th2d)
    
tight_electron_th2d.Divide(loose_electron_th2d)
tight_electron_th2d.Clone("electron_frs").Write()

if options.finmuondataname != None:

    #muon_ptbins=array('d', [10,15,20,25,30,40,50])
    muon_ptbins=array('d', [25,30,40,50])    
    #muon_etabins=array('d', [0,1,1.479,2.0,2.5])
    muon_etabins=array('d', [0,0.5,1.0,1.479,2.0,2.5])

    loose_muon_th2d=TH2F("loose_muon_hist","loose_muon_hist",len(muon_etabins)-1,muon_etabins,len(muon_ptbins)-1,muon_ptbins)
    tight_muon_th2d=TH2F("tight_muon_hist","tight_muon_hist",len(muon_etabins)-1,muon_etabins,len(muon_ptbins)-1,muon_ptbins)

    loose_muon_th2d.Sumw2()
    tight_muon_th2d.Sumw2()

    finmuonname=options.finmuondataname

    finmuon=TFile(finmuonname)

    gROOT.cd()

    muon_tree=finmuon.Get("Events")

    for entry in range(muon_tree.GetEntries()):
        muon_tree.GetEntry(entry)

        if entry % 100000 == 0:
            print entry

        if entry % int(options.mod) != 0:
            continue

        weight = 1

        if (muon_tree.is_lepton_tight == '\x01'):
            if muon_tree.lepton_pt > tight_muon_th2d.GetYaxis().GetBinUpEdge(tight_muon_th2d.GetYaxis().GetNbins()):
                tight_muon_th2d.Fill(abs(muon_tree.lepton_eta),tight_muon_th2d.GetYaxis().GetBinCenter(tight_muon_th2d.GetYaxis().GetNbins()),weight)
            else:
                tight_muon_th2d.Fill(abs(muon_tree.lepton_eta),muon_tree.lepton_pt,weight)

        else:
            
            if muon_tree.lepton_pt > loose_muon_th2d.GetYaxis().GetBinUpEdge(loose_muon_th2d.GetYaxis().GetNbins()):
                loose_muon_th2d.Fill(abs(muon_tree.lepton_eta),loose_muon_th2d.GetYaxis().GetBinCenter(loose_muon_th2d.GetYaxis().GetNbins()),weight)
            else:    
                loose_muon_th2d.Fill(abs(muon_tree.lepton_eta),muon_tree.lepton_pt,weight)

#tight_muon_th2d.Print("all")
#loose_muon_th2d.Print("all")

if options.finmuonmcname1 != None:

    mu17_lumi = 35.9

    finmuonmcname1=options.finmuonmcname1

    finmuonmc1=TFile(finmuonmcname1)

    gROOT.cd()

    muon_mc_tree1=finmuonmc1.Get("Events")
    muon_mc_n_weighted_event_hist1=finmuonmc1.Get("nWeightedEvents")
    muon_mc_n_weighted_events1=muon_mc_n_weighted_event_hist1.GetBinContent(1)

    for entry in range(muon_mc_tree1.GetEntries()):
        muon_mc_tree1.GetEntry(entry)

        if entry % 100000 == 0:
            print entry

        if entry % int(options.mod) != 0:
            continue

        #weight = (4963.0*1000/1917073)*mu17_lumi
        weight = (60430.0*1000/muon_mc_n_weighted_events1)*mu17_lumi

        if muon_mc_tree1.gen_weight < 0:
            weight = -weight         

        if (muon_mc_tree1.is_lepton_tight == '\x01'):
            if muon_mc_tree1.lepton_pt > tight_muon_th2d.GetYaxis().GetBinUpEdge(tight_muon_th2d.GetYaxis().GetNbins()):
                tight_muon_th2d.Fill(abs(muon_mc_tree1.lepton_eta),tight_muon_th2d.GetYaxis().GetBinCenter(tight_muon_th2d.GetYaxis().GetNbins()),-weight)
            else:
                tight_muon_th2d.Fill(abs(muon_mc_tree1.lepton_eta),muon_mc_tree1.lepton_pt,-weight)

        else:

            if muon_mc_tree1.lepton_pt > loose_muon_th2d.GetYaxis().GetBinUpEdge(loose_muon_th2d.GetYaxis().GetNbins()):
                loose_muon_th2d.Fill(abs(muon_mc_tree1.lepton_eta),loose_muon_th2d.GetYaxis().GetBinCenter(loose_muon_th2d.GetYaxis().GetNbins()),-weight)
            else:    
                loose_muon_th2d.Fill(abs(muon_mc_tree1.lepton_eta),muon_mc_tree1.lepton_pt,-weight)


if options.finmuonmcname2 != None:

    mu17_lumi = 35.9

    finmuonmcname2=options.finmuonmcname2

    finmuonmc2=TFile(finmuonmcname2)

    gROOT.cd()

    muon_mc_tree2=finmuonmc2.Get("Events")
    muon_mc_n_weighted_event_hist2=finmuonmc2.Get("nWeightedEvents")
    muon_mc_n_weighted_events2=muon_mc_n_weighted_event_hist2.GetBinContent(1)

    for entry in range(muon_mc_tree2.GetEntries()):
        muon_mc_tree2.GetEntry(entry)

        if entry % 100000 == 0:
            print entry

        if entry % int(options.mod) != 0:
            continue

        weight = (4963.0*1000/muon_mc_n_weighted_events2)*mu17_lumi
        #weight = (60430.0*1000/21315325)*mu17_lumi

        if muon_mc_tree2.gen_weight < 0:
            weight = -weight         

        if (muon_mc_tree2.is_lepton_tight == '\x01'):
            if muon_mc_tree2.lepton_pt > tight_muon_th2d.GetYaxis().GetBinUpEdge(tight_muon_th2d.GetYaxis().GetNbins()):
                tight_muon_th2d.Fill(abs(muon_mc_tree2.lepton_eta),tight_muon_th2d.GetYaxis().GetBinCenter(tight_muon_th2d.GetYaxis().GetNbins()),-weight)
            else:
                tight_muon_th2d.Fill(abs(muon_mc_tree2.lepton_eta),muon_mc_tree2.lepton_pt,-weight)

        else:

            if muon_mc_tree2.lepton_pt > loose_muon_th2d.GetYaxis().GetBinUpEdge(loose_muon_th2d.GetYaxis().GetNbins()):
                loose_muon_th2d.Fill(abs(muon_mc_tree2.lepton_eta),loose_muon_th2d.GetYaxis().GetBinCenter(loose_muon_th2d.GetYaxis().GetNbins()),-weight)
            else:    
                loose_muon_th2d.Fill(abs(muon_mc_tree2.lepton_eta),muon_mc_tree2.lepton_pt,-weight)

if options.finelectrondataname != None:

    finelectronname=options.finelectrondataname

    finelectron=TFile(finelectronname)
    
    gROOT.cd()

    electron_tree=finelectron.Get("Events")

    fill_loose_and_tight_th2ds(electron_tree,tight_electron_th2d,loose_electron_th2d)

if options.finelectronmcname1 != None:

    finelectronmc1 = TFile(options.finelectronmcname1)

    gROOT.cd()

    electron_mc_tree1=finelectronmc1.Get("Events")
    electron_mc_n_weighted_event_hist1=finelectronmc1.Get("nWeightedEvents")
    electron_mc_n_weighted_events1=electron_mc_n_weighted_event_hist1.GetBinContent(1)

    for entry in range(electron_mc_tree1.GetEntries()):
        electron_mc_tree1.GetEntry(entry)

        if entry % 100000 == 0:
            print entry

        if entry % int(options.mod) != 0:
            continue

        if electron_mc_tree1.gen_weight < 0:
            weight = -weight         

        weight = (60430.0*1000/electron_mc_n_weighted_events1)*35.9

        if electron_mc_tree1.gen_weight < 0:
            weight = -weight         

        if (electron_mc_tree1.is_lepton_tight == '\x01'):
            if electron_mc_tree1.lepton_pt > tight_electron_th2d.GetYaxis().GetBinUpEdge(tight_electron_th2d.GetYaxis().GetNbins()):
                tight_electron_th2d.Fill(abs(electron_mc_tree1.lepton_eta),tight_electron_th2d.GetYaxis().GetBinCenter(tight_electron_th2d.GetYaxis().GetNbins()),-weight)
            else:
                tight_electron_th2d.Fill(abs(electron_mc_tree1.lepton_eta),electron_mc_tree1.lepton_pt,-weight)

        else:

            if electron_mc_tree1.lepton_pt > loose_electron_th2d.GetYaxis().GetBinUpEdge(loose_electron_th2d.GetYaxis().GetNbins()):
                loose_electron_th2d.Fill(abs(electron_mc_tree1.lepton_eta),loose_electron_th2d.GetYaxis().GetBinCenter(loose_electron_th2d.GetYaxis().GetNbins()),-weight)
            else:    
                loose_electron_th2d.Fill(abs(electron_mc_tree1.lepton_eta),electron_mc_tree1.lepton_pt,-weight)

if options.finelectronmcname2 != None:

    finelectronmc2 = TFile(options.finelectronmcname2)

    gROOT.cd()

    electron_mc_tree2=finelectronmc2.Get("Events")
    electron_mc_n_weighted_event_hist2=finelectronmc2.Get("nWeightedEvents")
    electron_mc_n_weighted_events2=electron_mc_n_weighted_event_hist2.GetBinContent(1)

    for entry in range(electron_mc_tree2.GetEntries()):
        electron_mc_tree2.GetEntry(entry)

        if entry % 100000 == 0:
            print entry

        if entry % int(options.mod) != 0:
            continue

        if electron_mc_tree2.gen_weight < 0:
            weight = -weight         

        weight = (4963.0*1000/electron_mc_n_weighted_events2)*35.9

        if electron_mc_tree2.gen_weight < 0:
            weight = -weight         

        if (electron_mc_tree2.is_lepton_tight == '\x01'):
            if electron_mc_tree2.lepton_pt > tight_electron_th2d.GetYaxis().GetBinUpEdge(tight_electron_th2d.GetYaxis().GetNbins()):
                tight_electron_th2d.Fill(abs(electron_mc_tree2.lepton_eta),tight_electron_th2d.GetYaxis().GetBinCenter(tight_electron_th2d.GetYaxis().GetNbins()),-weight)
            else:
                tight_electron_th2d.Fill(abs(electron_mc_tree2.lepton_eta),electron_mc_tree2.lepton_pt,-weight)

        else:

            if electron_mc_tree2.lepton_pt > loose_electron_th2d.GetYaxis().GetBinUpEdge(loose_electron_th2d.GetYaxis().GetNbins()):
                loose_electron_th2d.Fill(abs(electron_mc_tree2.lepton_eta),loose_electron_th2d.GetYaxis().GetBinCenter(loose_electron_th2d.GetYaxis().GetNbins()),-weight)
            else:    
                loose_electron_th2d.Fill(abs(electron_mc_tree2.lepton_eta),electron_mc_tree2.lepton_pt,-weight)


fout.cd()

if options.finmuondataname != None or options.finmuonmcname1 != None or options.finmuonmcname2 != None:

    tight_muon_th2d.Clone().Write()
    loose_muon_th2d.Clone().Write()

    loose_muon_th2d.Add(tight_muon_th2d)

    tight_muon_th2d.Divide(loose_muon_th2d)
    tight_muon_th2d.Clone("muon_frs").Write()


