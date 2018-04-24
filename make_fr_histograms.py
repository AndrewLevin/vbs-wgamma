#if running on a dtmit machine, you need to move to root version 5.34.20 or higher
#source /afs/cern.ch/sw/lcg/external/gcc/4.7.2/x86_64-slc5-gcc47-opt/setup.sh
#source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.20/x86_64-slc5-gcc47-opt/root/bin/thisroot.sh

import math

import json

import optparse

parser = optparse.OptionParser()

parser.add_option('--muon_data_input_filename', help='filename of the input muon ntuple', dest='finmuondataname')
parser.add_option('--electron_data_input_filename', help='filename of the input electron ntuple', dest='finelectrondataname')
parser.add_option('--electron_mc_input_filename', help='filename of the input mc electron ntuple', dest='finelectronmcname')
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

fout=TFile(foutname,"recreate")

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

        if options.debug:
            print "andrew debug "+str(muon_tree.run)+" "+str(muon_tree.lumi)+" "+str(muon_tree.event)+" "+str(bool(muon_tree.flags & LepTightSelectionV1))

        if type(muon_tree.GetListOfBranches().FindObject("xsWeight")) == TBranch:
            weight = muon_tree.xsWeight
        else:
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

    for entry in range(muon_mc_tree1.GetEntries()):
        muon_mc_tree1.GetEntry(entry)

        if entry % 100000 == 0:
            print entry

        if entry % int(options.mod) != 0:
            continue

        #weight = (4963.0*1000/1917073)*mu17_lumi
        weight = (60430.0*1000/21315325)*mu17_lumi

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

    for entry in range(muon_mc_tree2.GetEntries()):
        muon_mc_tree2.GetEntry(entry)

        if entry % 100000 == 0:
            print entry

        if entry % int(options.mod) != 0:
            continue

        weight = (4963.0*1000/48664884)*mu17_lumi
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


#tight_muon_th2d.Print("all")
#loose_muon_th2d.Print("all")

#tight_muon_th2d.Print("all")
#loose_muon_th2d.Print("all")

if options.finelectrondataname != None:

    finelectronname=options.finelectrondataname

    finelectron=TFile(finelectronname)

    electron_tree=finelectron.Get("loose_electrons")

    electron_ptbins=array('d', [20,25,30,40,50])
    electron_etabins=array('d', [0,0.5,1,1.479,2.0,2.5])

    loose_electron_th2d=TH2F("loose_electron_hist","loose_electron_hist",len(electron_etabins)-1,electron_etabins,len(electron_ptbins)-1,electron_ptbins)
    tight_electron_th2d=TH2F("tight_electron_hist","tight_electron_hist",len(electron_etabins)-1,electron_etabins,len(electron_ptbins)-1,electron_ptbins)

    loose_electron_th2d.Sumw2()
    tight_electron_th2d.Sumw2()

    for entry in range(electron_tree.GetEntries()):
        electron_tree.GetEntry(entry)

    #if entry >= options.n_events:
    #    break

        if entry % 100000 == 0:
            print entry

        if entry % int(options.mod) != 0:
            continue

        if not (electron_tree.flags & PassTriggerV1):
            continue

        if electron_tree.electron_4mom.Pt() < 20:
            continue        

        #if electron_tree.run > run2016B[1] or electron_tree.run < run2016B[0]:
        #    continue

        #if electron_tree.event != 319630862:
        #    continue

        #if not pass_json(electron_tree.run,electron_tree.lumi):
        #    continue

        if electron_tree.metpt > 30:
            continue

        dphi = abs(electron_tree.metphi - electron_tree.electron_4mom.phi())

        if dphi > math.pi:
            dphi = 2*math.pi - dphi

        mt = sqrt(2*electron_tree.electron_4mom.pt()*electron_tree.metpt*(1 - cos(dphi)) )

        if mt > 20:
            continue

        if electron_tree.ptjetaway < 30:
            continue

    #if electron_tree.nearestparton_4mom.pt() > 20:
    #   continue    

    #if electron_tree.nearestparton_pdgid != 5:
    #    continue    


        if abs(electron_tree.electron_4mom.Eta()) > 2.5:
            continue

        if type(electron_tree.GetListOfBranches().FindObject("xsWeight")) == TBranch:
            weight = electron_tree.xsWeight
        else:
            weight = 1


        if options.debug:
            #print "andrew debug "+str(electron_tree.run)+" "+str(electron_tree.lumi)+" "+str(electron_tree.event)+" "+str(bool(electron_tree.flags & LepTightSelectionV5))
            print "andrew debug "+str(electron_tree.run)+" "+str(electron_tree.lumi)+" "+str(bool(electron_tree.flags & LepTightSelectionV5))

        #use the xsWeight if it exists, otherwise all events have weight 1
        if type(electron_tree.GetListOfBranches().FindObject("xsWeight")) == TBranch:
            weight = electron_tree.xsWeight

        if (electron_tree.flags & LepTightSelectionV4):

            if electron_tree.electron_4mom.Pt() > tight_electron_th2d.GetYaxis().GetBinUpEdge(tight_electron_th2d.GetYaxis().GetNbins()):
                tight_electron_th2d.Fill(abs(electron_tree.electron_4mom.Eta()),tight_electron_th2d.GetYaxis().GetBinCenter(tight_electron_th2d.GetYaxis().GetNbins()),weight)
            else:    
                tight_electron_th2d.Fill(abs(electron_tree.electron_4mom.Eta()),electron_tree.electron_4mom.Pt(),weight)
        elif (electron_tree.flags & LepLooseSelectionV2):
            if electron_tree.electron_4mom.Pt() > loose_electron_th2d.GetYaxis().GetBinUpEdge(loose_electron_th2d.GetYaxis().GetNbins()):
                loose_electron_th2d.Fill(abs(electron_tree.electron_4mom.Eta()),loose_electron_th2d.GetYaxis().GetBinCenter(loose_electron_th2d.GetYaxis().GetNbins()),weight)
            else:
                loose_electron_th2d.Fill(abs(electron_tree.electron_4mom.Eta()),electron_tree.electron_4mom.Pt(),weight)
#    loose_electron_th2d.Fill(electron_tree.electron_4mom.Eta(),electron_tree.electron_4mom.Pt())


#    if electron_tree.pass_full_electron_id:
#        tight_electron_th2d.Fill(electron_tree.electron_4mom.Eta(),electron_tree.electron_4mom.Pt())  

if options.finelectronmcname != None:

    #ele12_lumi = 10.57/1000.0
    #ele33_lumi = 4.98/1000.0
    #ele12_lumi = 5/1000.0
    #ele12_lumi=35.9*0.0008
    #ele12_lumi=35.9*0.0006
    ele12_lumi=35.9*0.0005    
    
    finelectronmc = TFile(options.finelectronmcname)
    electron_mc_tree=finelectronmc.Get("loose_electrons")

    for entry in range(electron_mc_tree.GetEntries()):
        electron_mc_tree.GetEntry(entry)

        if entry % 100000 == 0:
            print entry

        if entry % int(options.mod) != 0:
            continue

        if not (electron_mc_tree.flags & PassTriggerV1):
            continue

        if electron_mc_tree.electron_4mom.Pt() < 20:
            continue        

        if electron_mc_tree.metpt > 30:
            continue

        dphi = abs(electron_mc_tree.metphi - electron_mc_tree.electron_4mom.phi())

        if dphi > math.pi:
            dphi = 2*math.pi - dphi

        mt = sqrt(2*electron_mc_tree.electron_4mom.pt()*electron_mc_tree.metpt*(1 - cos(dphi)) )

        if mt > 20:
            continue

        if electron_mc_tree.ptjetaway < 30:
            continue


        if abs(electron_mc_tree.electron_4mom.Eta()) > 2.5:
            continue

        weight = electron_mc_tree.xsWeight*ele12_lumi

        if electron_mc_tree.gen_weight < 0:
            weight = -weight         

        if (electron_mc_tree.flags & LepTightSelectionV4):

            if electron_mc_tree.electron_4mom.Pt() > tight_electron_th2d.GetYaxis().GetBinUpEdge(tight_electron_th2d.GetYaxis().GetNbins()):
                tight_electron_th2d.Fill(abs(electron_mc_tree.electron_4mom.Eta()),tight_electron_th2d.GetYaxis().GetBinCenter(tight_electron_th2d.GetYaxis().GetNbins()),-weight)
            else:    
                tight_electron_th2d.Fill(abs(electron_mc_tree.electron_4mom.Eta()),electron_mc_tree.electron_4mom.Pt(),-weight)
        elif (electron_mc_tree.flags & LepLooseSelectionV2):

            if electron_mc_tree.electron_4mom.Pt() > loose_electron_th2d.GetYaxis().GetBinUpEdge(loose_electron_th2d.GetYaxis().GetNbins()):
                loose_electron_th2d.Fill(abs(electron_mc_tree.electron_4mom.Eta()),loose_electron_th2d.GetYaxis().GetBinCenter(loose_electron_th2d.GetYaxis().GetNbins()),-weight)
            else:
                loose_electron_th2d.Fill(abs(electron_mc_tree.electron_4mom.Eta()),electron_mc_tree.electron_4mom.Pt(),-weight)





fout.cd()

if options.finmuondataname != None or options.finmuonmcname != None:

    tight_muon_th2d.Clone().Write()
    loose_muon_th2d.Clone().Write()

    loose_muon_th2d.Add(tight_muon_th2d)

    tight_muon_th2d.Divide(loose_muon_th2d)
    tight_muon_th2d.Clone("muon_frs").Write()

if options.finelectrondataname != None or options.finelectronmcname != None:

    tight_electron_th2d.Clone().Write()
    loose_electron_th2d.Clone().Write()

    loose_electron_th2d.Add(tight_electron_th2d)
    
    tight_electron_th2d.Divide(loose_electron_th2d)
#tight_electron_th2d.Draw("lego")
    tight_electron_th2d.Clone("electron_frs").Write()

#raw_input()

