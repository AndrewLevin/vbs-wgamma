import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--muon_inputs",type=str,help="Cross section inputs for muon channel",default="/afs/cern.ch/user/a/amlevin/wg/xs_inputs/xs_inputs_muon.txt") 
parser.add_argument("--electron_inputs",type=str,help="Cross section inputs for electron channel",default="/afs/cern.ch/user/a/amlevin/wg/xs_inputs/xs_inputs_electron.txt") 

args = parser.parse_args()

import json
import math

xs_inputs_muon = json.load(open(args.muon_inputs))
xs_inputs_electron = json.load(open(args.electron_inputs))

from pprint import pprint

#pprint(xs_inputs_muon)
#pprint(xs_inputs_electron)

assert(xs_inputs_muon["xs_times_lumi"] == xs_inputs_electron["xs_times_lumi"])
assert(xs_inputs_muon["lumi"] == xs_inputs_electron["lumi"])

lumi = xs_inputs_muon["lumi"]
lumi*=1000

fiducial = xs_inputs_muon["fiducial"]  

sum_muon_photon_stat = 0
sum_electron_photon_stat = 0
sum_muon_lepton_stat = 0
sum_electron_lepton_stat = 0
sum_muon_double_stat = 0
sum_electron_double_stat = 0
sum_muon_zg_stat = 0
sum_electron_zg_stat = 0
sum_muon_top_stat = 0
sum_electron_top_stat = 0
sum_muon_vv_stat = 0
sum_electron_vv_stat = 0

for i in range(1,201):

    if xs_inputs_muon["signal_syst_unc_due_to_fake_photon_stat_up_bin"+str(i)] < 100:
        sum_muon_photon_stat = sum_muon_photon_stat + pow(xs_inputs_muon["signal_syst_unc_due_to_fake_photon_stat_up_bin"+str(i)],2)
    else:
        print "Muon fake photon bin "+str(i)+ " stat uncertainty causes n_signal to change by more than 100" 
        print xs_inputs_muon["signal_syst_unc_due_to_fake_photon_stat_up_bin"+str(i)]

    if xs_inputs_electron["signal_syst_unc_due_to_fake_photon_stat_up_bin"+str(i)] < 100:
        sum_electron_photon_stat = sum_electron_photon_stat + pow(xs_inputs_electron["signal_syst_unc_due_to_fake_photon_stat_up_bin"+str(i)],2)
    else:
        print "Electron fake photon bin "+str(i)+ " stat uncertainty causes n_signal to change by more than 100" 
        print xs_inputs_electron["signal_syst_unc_due_to_fake_photon_stat_up_bin"+str(i)]

    if xs_inputs_muon["signal_syst_unc_due_to_fake_lepton_stat_up_bin"+str(i)] < 100:
        sum_muon_lepton_stat = sum_muon_lepton_stat + pow(xs_inputs_muon["signal_syst_unc_due_to_fake_lepton_stat_up_bin"+str(i)],2)
    else:
        print "Fake muon bin "+str(i)+ " syst uncertainty causes n_signal to change by more than 100" 
        print xs_inputs_muon["signal_syst_unc_due_to_fake_lepton_stat_up_bin"+str(i)]

    if xs_inputs_electron["signal_syst_unc_due_to_fake_lepton_stat_up_bin"+str(i)] < 100:
        sum_electron_lepton_stat = sum_electron_lepton_stat + pow(xs_inputs_electron["signal_syst_unc_due_to_fake_lepton_stat_up_bin"+str(i)],2)
    else:
        print "Fake electron bin "+str(i)+ " syst uncertainty causes n_signal to change by more than 100" 
        print xs_inputs_electron["signal_syst_unc_due_to_fake_lepton_stat_up_bin"+str(i)]

    if xs_inputs_muon["signal_syst_unc_due_to_double_fake_stat_up_bin"+str(i)] < 100:
        sum_muon_double_stat = sum_muon_double_stat + pow(xs_inputs_muon["signal_syst_unc_due_to_double_fake_stat_up_bin"+str(i)],2)
    else:
        print "Muon double fake bin "+str(i)+ " syst uncertainty causes n_signal to change by more than 100" 
        print xs_inputs_muon["signal_syst_unc_due_to_double_fake_stat_up_bin"+str(i)]

    if xs_inputs_electron["signal_syst_unc_due_to_double_fake_stat_up_bin"+str(i)] < 100:
        sum_electron_double_stat = sum_electron_double_stat + pow(xs_inputs_electron["signal_syst_unc_due_to_double_fake_stat_up_bin"+str(i)],2)
    else:
        print "Electron double fake bin "+str(i)+ " syst uncertainty causes n_signal to change by more than 100" 
        print xs_inputs_electron["signal_syst_unc_due_to_double_fake_stat_up_bin"+str(i)]

    if xs_inputs_muon["signal_syst_unc_due_to_zg_stat_up_bin"+str(i)] < 100:
        sum_muon_zg_stat = sum_muon_zg_stat + pow(xs_inputs_muon["signal_syst_unc_due_to_zg_stat_up_bin"+str(i)],2)
    else:
        print "Muon ZG bin "+str(i)+" stat uncertainty causes n_signal to change by more than 100"
        print xs_inputs_muon["signal_syst_unc_due_to_zg_stat_up_bin"+str(i)]

    if xs_inputs_electron["signal_syst_unc_due_to_zg_stat_up_bin"+str(i)] < 100:
        sum_electron_zg_stat = sum_electron_zg_stat + pow(xs_inputs_electron["signal_syst_unc_due_to_zg_stat_up_bin"+str(i)],2)
    else:
        print "Electron ZG bin "+str(i)+" stat uncertainty causes n_signal to change by more than 100"
        print xs_inputs_electron["signal_syst_unc_due_to_zg_stat_up_bin"+str(i)]

    if xs_inputs_muon["signal_syst_unc_due_to_vv_stat_up_bin"+str(i)] < 100:
        sum_muon_vv_stat = sum_muon_vv_stat + pow(xs_inputs_muon["signal_syst_unc_due_to_vv_stat_up_bin"+str(i)],2)
    else:
        print "Muon VV bin "+str(i)+" stat uncertainty causes n_signal to change by more than 100"
        print xs_inputs_muon["signal_syst_unc_due_to_vv_stat_up_bin"+str(i)]

    if xs_inputs_electron["signal_syst_unc_due_to_vv_stat_up_bin"+str(i)] < 100:
        sum_electron_vv_stat = sum_electron_vv_stat + pow(xs_inputs_electron["signal_syst_unc_due_to_vv_stat_up_bin"+str(i)],2)
    else:
        print "Electron VV bin "+str(i)+" stat uncertainty causes n_signal to change by more than 100"
        print xs_inputs_electron["signal_syst_unc_due_to_vv_stat_up_bin"+str(i)]

    if xs_inputs_muon["signal_syst_unc_due_to_top_stat_up_bin"+str(i)] < 100:
        sum_muon_top_stat = sum_muon_top_stat + pow(xs_inputs_muon["signal_syst_unc_due_to_top_stat_up_bin"+str(i)],2)
    else:
        print "Muon Top bin "+str(i)+" stat uncertainty causes n_signal to change by more than 100"
        print xs_inputs_muon["signal_syst_unc_due_to_top_stat_up_bin"+str(i)]

    if xs_inputs_electron["signal_syst_unc_due_to_top_stat_up_bin"+str(i)] < 100:
        sum_electron_top_stat = sum_electron_top_stat + pow(xs_inputs_electron["signal_syst_unc_due_to_top_stat_up_bin"+str(i)],2)
    else:
        print "Electron Top bin "+str(i)+" stat uncertainty causes n_signal to change by more than 100"
        print xs_inputs_electron["signal_syst_unc_due_to_top_stat_up_bin"+str(i)]


mean_pdf=0
for i in range(1,32):
    mean_pdf += xs_inputs_muon["signal_syst_unc_due_to_zg_pdf_variation"+str(i)]+xs_inputs_muon["signal_data_muon"]+xs_inputs_electron["signal_syst_unc_due_to_zg_pdf_variation"+str(i)]+xs_inputs_electron["signal_data_electron"]

mean_pdf = mean_pdf/31

stddev_pdf = 0

for i in range(1,32):
    stddev_pdf += pow(xs_inputs_muon["signal_syst_unc_due_to_zg_pdf_variation"+str(i)]+xs_inputs_muon["signal_data_muon"]+xs_inputs_electron["signal_syst_unc_due_to_zg_pdf_variation"+str(i)]+xs_inputs_electron["signal_data_electron"] - mean_pdf,2)

stddev_pdf = math.sqrt(stddev_pdf/(31-1))

mean_pdf_muon=0
for i in range(1,32):
    mean_pdf_muon += xs_inputs_muon["signal_syst_unc_due_to_zg_pdf_variation"+str(i)]+xs_inputs_muon["signal_data_muon"]

mean_pdf_muon = mean_pdf_muon/31

stddev_pdf_muon = 0

for i in range(1,32):
    stddev_pdf_muon += pow(xs_inputs_muon["signal_syst_unc_due_to_zg_pdf_variation"+str(i)]+xs_inputs_muon["signal_data_muon"]- mean_pdf_muon,2)

stddev_pdf_muon = math.sqrt(stddev_pdf_muon/(31-1))


mean_pdf_electron=0
for i in range(1,32):
    mean_pdf_electron += xs_inputs_electron["signal_syst_unc_due_to_zg_pdf_variation"+str(i)]+xs_inputs_electron["signal_data_electron"]

mean_pdf_electron = mean_pdf_electron/31

stddev_pdf_electron = 0

for i in range(1,32):
    stddev_pdf_electron += pow(xs_inputs_electron["signal_syst_unc_due_to_zg_pdf_variation"+str(i)]+xs_inputs_electron["signal_data_electron"]- mean_pdf_electron,2)

stddev_pdf_electron = math.sqrt(stddev_pdf_electron/(31-1))

unc_due_to_fake_photon_stat_electron = math.sqrt(sum_electron_photon_stat)
unc_due_to_fake_photon_stat_muon = math.sqrt(sum_muon_photon_stat)

unc_due_to_fake_lepton_stat_electron = math.sqrt(sum_electron_lepton_stat)
unc_due_to_fake_lepton_stat_muon = math.sqrt(sum_muon_lepton_stat)

unc_due_to_double_fake_stat_electron = math.sqrt(sum_electron_double_stat)
unc_due_to_double_fake_stat_muon = math.sqrt(sum_muon_double_stat)

unc_due_to_zg_stat_electron = math.sqrt(sum_electron_zg_stat)
unc_due_to_zg_stat_muon = math.sqrt(sum_muon_zg_stat)

unc_due_to_vv_stat_electron = math.sqrt(sum_electron_vv_stat)
unc_due_to_vv_stat_muon = math.sqrt(sum_muon_vv_stat)

unc_due_to_top_stat_electron = math.sqrt(sum_electron_top_stat)
unc_due_to_top_stat_muon = math.sqrt(sum_muon_top_stat)

unc_due_to_mc_stat_electron = math.sqrt(sum_electron_zg_stat+sum_electron_vv_stat+sum_electron_top_stat)
unc_due_to_mc_stat_muon = math.sqrt(sum_muon_zg_stat+sum_muon_vv_stat+sum_muon_top_stat)

unc_due_to_data_driven_stat_electron = math.sqrt(sum_electron_double_stat+sum_electron_lepton_stat+sum_electron_photon_stat)
unc_due_to_data_driven_stat_muon = math.sqrt(sum_muon_double_stat+sum_muon_lepton_stat+sum_muon_photon_stat)

unc_due_to_data_driven_stat = math.sqrt(sum_electron_double_stat+sum_electron_lepton_stat+sum_electron_photon_stat + sum_muon_double_stat+sum_muon_lepton_stat+sum_muon_photon_stat)

unc_due_to_mc_stat = math.sqrt(sum_electron_zg_stat+sum_electron_vv_stat+sum_electron_top_stat + sum_muon_zg_stat+sum_muon_vv_stat+sum_muon_top_stat)

#unc_due_to_mc_stat_electron = 0
#unc_due_to_mc_stat_muon = 0
#unc_due_to_data_driven_stat_electron = 0
#unc_due_to_data_driven_stat_muon = 0

#print "unc_due_to_fake_photon_stat_electron = "+str(unc_due_to_fake_photon_stat_electron)
#print "unc_due_to_fake_photon_stat_muon = "+str(unc_due_to_fake_photon_stat_muon)

#print "unc_due_to_fake_lepton_stat_electron = "+str(unc_due_to_fake_lepton_stat_electron)
#print "unc_due_to_fake_lepton_stat_muon = "+str(unc_due_to_fake_lepton_stat_muon)

#print "unc_due_to_double_fake_stat_electron = "+str(unc_due_to_double_fake_stat_electron)
#print "unc_due_to_double_fake_stat_muon = "+str(unc_due_to_double_fake_stat_muon)

#print "unc_due_to_zg_stat_electron = "+str(unc_due_to_zg_stat_electron)
#print "unc_due_to_zg_stat_muon = "+str(unc_due_to_zg_stat_muon)

#print "unc_due_to_vv_stat_electron = "+str(unc_due_to_vv_stat_electron)
#print "unc_due_to_vv_stat_muon = "+str(unc_due_to_vv_stat_muon)

#print "unc_due_to_top_stat_electron = "+str(unc_due_to_top_stat_electron)
#print "unc_due_to_top_stat_muon = "+str(unc_due_to_top_stat_muon)

#print "unc_due_to_mc_stat_electron = "+str(unc_due_to_mc_stat_electron)
#print "unc_due_to_mc_stat_muon = "+str(unc_due_to_mc_stat_muon)

#print "unc_due_to_data_driven_stat_electron = "+str(unc_due_to_data_driven_stat_electron)
#print "unc_due_to_data_driven_stat_muon = "+str(unc_due_to_data_driven_stat_muon)

signal_unc_due_to_qcd_scale_muon = max(abs(xs_inputs_muon["signal_syst_unc_due_to_zg_scale_variation0"]),abs(xs_inputs_muon["signal_syst_unc_due_to_zg_scale_variation1"]),abs(xs_inputs_muon["signal_syst_unc_due_to_zg_scale_variation3"]),abs(xs_inputs_muon["signal_syst_unc_due_to_zg_scale_variation4"]),abs(xs_inputs_muon["signal_syst_unc_due_to_zg_scale_variation6"]),abs(xs_inputs_muon["signal_syst_unc_due_to_zg_scale_variation7"]))

signal_unc_due_to_qcd_scale_electron = max(abs(xs_inputs_electron["signal_syst_unc_due_to_zg_scale_variation0"]),abs(xs_inputs_electron["signal_syst_unc_due_to_zg_scale_variation1"]),abs(xs_inputs_electron["signal_syst_unc_due_to_zg_scale_variation3"]),abs(xs_inputs_electron["signal_syst_unc_due_to_zg_scale_variation4"]),abs(xs_inputs_electron["signal_syst_unc_due_to_zg_scale_variation6"]),abs(xs_inputs_electron["signal_syst_unc_due_to_zg_scale_variation7"]))

signal_unc_due_to_qcd_scale = max(abs(xs_inputs_electron["signal_syst_unc_due_to_zg_scale_variation0"]+xs_inputs_muon["signal_syst_unc_due_to_zg_scale_variation0"]),abs(xs_inputs_electron["signal_syst_unc_due_to_zg_scale_variation1"]+xs_inputs_muon["signal_syst_unc_due_to_zg_scale_variation1"]),abs(xs_inputs_electron["signal_syst_unc_due_to_zg_scale_variation3"]+xs_inputs_muon["signal_syst_unc_due_to_zg_scale_variation3"]),abs(xs_inputs_electron["signal_syst_unc_due_to_zg_scale_variation4"]+xs_inputs_muon["signal_syst_unc_due_to_zg_scale_variation4"]),abs(xs_inputs_electron["signal_syst_unc_due_to_zg_scale_variation6"]+xs_inputs_muon["signal_syst_unc_due_to_zg_scale_variation6"]),abs(xs_inputs_electron["signal_syst_unc_due_to_zg_scale_variation7"]+xs_inputs_muon["signal_syst_unc_due_to_zg_scale_variation7"]))

xs_times_lumi  =  xs_inputs_muon["xs_times_lumi"]

signal_muon  =  xs_inputs_muon["signal_data_muon"]

signal_unc_due_to_lumi_muon = xs_inputs_muon["signal_syst_unc_due_to_lumi_up"]
signal_syst_unc_due_to_pileup_muon = xs_inputs_muon["signal_syst_unc_due_to_pileup"]
signal_syst_unc_due_to_prefire_muon = xs_inputs_muon["signal_syst_unc_due_to_prefire"]
signal_syst_unc_due_to_jer_muon = xs_inputs_muon["signal_syst_unc_due_to_jer"]
signal_syst_unc_due_to_jes_muon = xs_inputs_muon["signal_syst_unc_due_to_jes"]
signal_syst_unc_due_to_fake_photon_alt_muon  =  xs_inputs_muon["signal_syst_unc_due_to_fake_photon_alt_muon"]
signal_syst_unc_due_to_fake_photon_wjets_muon  =  xs_inputs_muon["signal_syst_unc_due_to_fake_photon_wjets_muon"]
signal_syst_unc_due_to_fake_lepton_muon  =  xs_inputs_muon["signal_syst_unc_due_to_fake_lepton_muon"]
signal_stat_unc_muon  =  xs_inputs_muon["signal_stat_unc_muon"]
n_weighted_selected_data_mc_sf_muon  =  xs_inputs_muon["signal_mc_xs_data_mc"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_id_sf_muon  =  xs_inputs_muon["signal_mc_xs_data_mc_syst_unc_due_to_muon_id_sf_muon"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_iso_sf_muon  =  xs_inputs_muon["signal_mc_xs_data_mc_syst_unc_due_to_muon_iso_sf_muon"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_hlt_sf_muon  =  xs_inputs_muon["signal_mc_xs_data_mc_syst_unc_due_to_muon_hlt_sf_muon"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_muon  =  xs_inputs_muon["signal_mc_xs_data_mc_syst_unc_due_to_photon_id_sf_muon"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_pdf_muon  =  0
n_weighted_selected_data_mc_sf_syst_unc_due_to_qcd_scale_muon  =  0

signal_syst_unc_due_to_fake_photon_muon = math.sqrt(pow(signal_syst_unc_due_to_fake_photon_alt_muon,2) + pow(signal_syst_unc_due_to_fake_photon_wjets_muon,2))

signal_electron  =  xs_inputs_electron["signal_data_electron"]
signal_syst_unc_due_to_fake_photon_alt_electron  =  xs_inputs_electron["signal_syst_unc_due_to_fake_photon_alt_electron"]
signal_syst_unc_due_to_fake_photon_wjets_electron  =  xs_inputs_electron["signal_syst_unc_due_to_fake_photon_wjets_electron"]
signal_unc_due_to_lumi_electron = xs_inputs_electron["signal_syst_unc_due_to_lumi_up"]
signal_syst_unc_due_to_pileup_electron = xs_inputs_electron["signal_syst_unc_due_to_pileup"]
signal_syst_unc_due_to_prefire_electron = xs_inputs_electron["signal_syst_unc_due_to_prefire"]
signal_syst_unc_due_to_jer_electron = xs_inputs_electron["signal_syst_unc_due_to_jer"]
signal_syst_unc_due_to_jes_electron = xs_inputs_electron["signal_syst_unc_due_to_jes"]

signal_syst_unc_due_to_fake_photon_electron = math.sqrt(pow(signal_syst_unc_due_to_fake_photon_alt_electron,2) + pow(signal_syst_unc_due_to_fake_photon_wjets_electron,2))

signal_syst_unc_due_to_fake_lepton_electron  =  xs_inputs_electron["signal_syst_unc_due_to_fake_lepton_electron"]
signal_stat_unc_electron  =  xs_inputs_electron["signal_stat_unc_electron"]
n_weighted_selected_data_mc_sf_electron  =  xs_inputs_electron["signal_mc_xs_data_mc"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_id_sf_electron  =  xs_inputs_electron["signal_mc_xs_data_mc_syst_unc_due_to_electron_id_sf_electron"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_reco_sf_electron  =  xs_inputs_electron["signal_mc_xs_data_mc_syst_unc_due_to_electron_reco_sf_electron"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_hlt_sf_electron  =  xs_inputs_electron["signal_mc_xs_data_mc_syst_unc_due_to_electron_hlt_sf_electron"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_electron =   xs_inputs_electron["signal_mc_xs_data_mc_syst_unc_due_to_photon_id_sf_electron"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_pdf_electron  =  0
n_weighted_selected_data_mc_sf_syst_unc_due_to_qcd_scale_electron  =  0


n_weighted_selected_data_mc_sf_syst_unc_due_to_pileup_muon = xs_inputs_muon["signal_mc_xs_data_mc_syst_unc_due_to_pileup"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_pileup_electron = xs_inputs_electron["signal_mc_xs_data_mc_syst_unc_due_to_pileup"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_pileup = xs_inputs_muon["signal_mc_xs_data_mc_syst_unc_due_to_pileup"]+xs_inputs_electron["signal_mc_xs_data_mc_syst_unc_due_to_pileup"]

n_weighted_selected_data_mc_sf_syst_unc_due_to_prefire_muon = xs_inputs_muon["signal_mc_xs_data_mc_syst_unc_due_to_prefire"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_prefire_electron = xs_inputs_electron["signal_mc_xs_data_mc_syst_unc_due_to_prefire"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_prefire = xs_inputs_muon["signal_mc_xs_data_mc_syst_unc_due_to_prefire"]+xs_inputs_electron["signal_mc_xs_data_mc_syst_unc_due_to_prefire"]

n_weighted_selected_data_mc_sf_syst_unc_due_to_jer_muon = xs_inputs_muon["signal_mc_xs_data_mc_syst_unc_due_to_jer"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_jer_electron = xs_inputs_electron["signal_mc_xs_data_mc_syst_unc_due_to_jer"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_jer = xs_inputs_muon["signal_mc_xs_data_mc_syst_unc_due_to_jer"]+xs_inputs_electron["signal_mc_xs_data_mc_syst_unc_due_to_jer"]

n_weighted_selected_data_mc_sf_syst_unc_due_to_jes_muon = xs_inputs_muon["signal_mc_xs_data_mc_syst_unc_due_to_jes"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_jes_electron = xs_inputs_electron["signal_mc_xs_data_mc_syst_unc_due_to_jes"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_jes = xs_inputs_muon["signal_mc_xs_data_mc_syst_unc_due_to_jes"]+xs_inputs_electron["signal_mc_xs_data_mc_syst_unc_due_to_jes"]


signal = signal_muon+signal_electron

signal_syst_unc_due_to_pileup = signal_syst_unc_due_to_pileup_electron+signal_syst_unc_due_to_pileup_muon
signal_syst_unc_due_to_prefire = signal_syst_unc_due_to_pileup_electron+signal_syst_unc_due_to_prefire_muon
signal_syst_unc_due_to_jer = signal_syst_unc_due_to_pileup_electron+signal_syst_unc_due_to_jer_muon
signal_syst_unc_due_to_jes = signal_syst_unc_due_to_pileup_electron+signal_syst_unc_due_to_jes_muon

signal_syst_unc_due_to_lumi = signal_unc_due_to_lumi_electron + signal_unc_due_to_lumi_muon

signal_syst_unc_due_to_fake_photon = signal_syst_unc_due_to_fake_photon_electron+signal_syst_unc_due_to_fake_photon_muon

signal_syst_unc_due_to_fake_lepton = signal_syst_unc_due_to_fake_lepton_electron+signal_syst_unc_due_to_fake_lepton_muon

n_weighted_selected_data_mc_sf = n_weighted_selected_data_mc_sf_electron + n_weighted_selected_data_mc_sf_muon

signal_stat_unc = math.sqrt(pow(signal_stat_unc_electron,2) + pow(signal_stat_unc_muon,2))

n_weighted_selected_data_mc_sf_syst_unc = math.sqrt(pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_pileup,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_id_sf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_iso_sf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_hlt_sf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_pdf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_qcd_scale_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_id_sf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_reco_sf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_hlt_sf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_pdf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_qcd_scale_electron,2)+pow(unc_due_to_mc_stat_muon,2)+pow(unc_due_to_data_driven_stat_muon,2)+pow(unc_due_to_mc_stat_electron,2)+pow(unc_due_to_data_driven_stat_electron,2))

n_weighted_selected_data_mc_sf_syst_unc_muon = math.sqrt(pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_id_sf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_iso_sf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_hlt_sf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_pdf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_qcd_scale_muon,2)+pow(unc_due_to_mc_stat_muon,2)+pow(unc_due_to_data_driven_stat_muon,2)  + pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_pileup_muon,2) )

n_weighted_selected_data_mc_sf_syst_unc_electron = math.sqrt(pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_id_sf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_reco_sf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_reco_sf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_pdf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_qcd_scale_electron,2)+pow(unc_due_to_mc_stat_electron,2)+pow(unc_due_to_data_driven_stat_electron,2) + pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_pileup_electron,2))

xs =  signal/(n_weighted_selected_data_mc_sf/fiducial)/lumi

xs_electron =  signal_electron/(n_weighted_selected_data_mc_sf_electron/fiducial)/lumi

xs_muon =  signal_muon/(n_weighted_selected_data_mc_sf_muon/fiducial)/lumi

lumi_err =  signal/(n_weighted_selected_data_mc_sf*0.982/fiducial)/lumi - xs

lumi_err_electron =  signal_electron/(n_weighted_selected_data_mc_sf_electron*0.982/fiducial)/lumi - xs_electron

lumi_err_muon =  signal_muon/(n_weighted_selected_data_mc_sf_muon*0.982/fiducial)/lumi - xs_muon

stat_err = (signal+signal_stat_unc)/(n_weighted_selected_data_mc_sf/fiducial)/lumi - xs

stat_err_electron = (signal_electron+signal_stat_unc_electron)/(n_weighted_selected_data_mc_sf_electron/fiducial)/lumi - xs_electron

stat_err_muon = (signal_muon+signal_stat_unc_muon)/(n_weighted_selected_data_mc_sf_muon/fiducial)/lumi - xs_muon

syst_err_acc = signal/((n_weighted_selected_data_mc_sf - n_weighted_selected_data_mc_sf_syst_unc)/fiducial)/lumi - xs

syst_err_acc_muon = signal_muon/((n_weighted_selected_data_mc_sf_muon - n_weighted_selected_data_mc_sf_syst_unc_muon)/fiducial)/lumi - xs_muon

syst_err_acc_electron = signal_electron/((n_weighted_selected_data_mc_sf_electron - n_weighted_selected_data_mc_sf_syst_unc_electron)/fiducial)/lumi - xs_electron

syst_err_signal_fake_photon = (signal+signal_syst_unc_due_to_fake_photon)/(n_weighted_selected_data_mc_sf/fiducial)/lumi - xs

syst_err_signal_fake_photon_muon = (signal_muon+signal_syst_unc_due_to_fake_photon_muon)/(n_weighted_selected_data_mc_sf_muon/fiducial)/lumi - xs_muon

syst_err_signal_fake_photon_electron = (signal_electron+signal_syst_unc_due_to_fake_photon_electron)/(n_weighted_selected_data_mc_sf_electron/fiducial)/lumi - xs_electron

syst_err_signal_fake_lepton = (signal+signal_syst_unc_due_to_fake_lepton)/(n_weighted_selected_data_mc_sf/fiducial)/lumi - xs

syst_err_signal_fake_lepton_muon = (signal_muon+signal_syst_unc_due_to_fake_lepton_muon)/(n_weighted_selected_data_mc_sf_muon/fiducial)/lumi - xs_muon

syst_err_signal_fake_lepton_electron = (signal_electron+signal_syst_unc_due_to_fake_lepton_electron)/(n_weighted_selected_data_mc_sf_electron/fiducial)/lumi - xs_electron




syst_err_signal_qcd_scale = (signal+signal_unc_due_to_qcd_scale)/(n_weighted_selected_data_mc_sf/fiducial)/lumi - xs

syst_err_signal_qcd_scale_muon = (signal_muon+signal_unc_due_to_qcd_scale_muon)/(n_weighted_selected_data_mc_sf_muon/fiducial)/lumi - xs_muon

syst_err_signal_qcd_scale_electron = (signal_electron+signal_unc_due_to_qcd_scale_electron)/(n_weighted_selected_data_mc_sf_electron/fiducial)/lumi - xs_electron



syst_err_signal_pdf = (signal+stddev_pdf)/(n_weighted_selected_data_mc_sf/fiducial)/lumi - xs

syst_err_signal_pdf_muon = (signal_muon+stddev_pdf_muon)/(n_weighted_selected_data_mc_sf_muon/fiducial)/lumi - xs_muon

syst_err_signal_pdf_electron = (signal_electron+stddev_pdf_electron)/(n_weighted_selected_data_mc_sf_electron/fiducial)/lumi - xs_electron




syst_err_signal_data_driven_stat = (signal+unc_due_to_data_driven_stat)/(n_weighted_selected_data_mc_sf/fiducial)/lumi - xs

syst_err_signal_data_driven_stat_muon = (signal_muon+unc_due_to_data_driven_stat_muon)/(n_weighted_selected_data_mc_sf_muon/fiducial)/lumi - xs_muon

syst_err_signal_data_driven_stat_electron = (signal_electron+unc_due_to_data_driven_stat_electron)/(n_weighted_selected_data_mc_sf_electron/fiducial)/lumi - xs_electron

 
syst_err_signal_mc_stat = (signal+unc_due_to_mc_stat)/(n_weighted_selected_data_mc_sf/fiducial)/lumi - xs

syst_err_signal_mc_stat_muon = (signal_muon+unc_due_to_mc_stat_muon)/(n_weighted_selected_data_mc_sf_muon/fiducial)/lumi - xs_muon

syst_err_signal_mc_stat_electron = (signal_electron+unc_due_to_mc_stat_electron)/(n_weighted_selected_data_mc_sf_electron/fiducial)/lumi - xs_electron

syst_err_signal_pileup = (signal+signal_syst_unc_due_to_pileup)/(n_weighted_selected_data_mc_sf/fiducial)/lumi - xs

syst_err_signal_pileup_muon = (signal_muon+signal_syst_unc_due_to_pileup_muon)/(n_weighted_selected_data_mc_sf_muon/fiducial)/lumi - xs_muon

syst_err_signal_pileup_electron = (signal_electron+signal_syst_unc_due_to_pileup_electron)/(n_weighted_selected_data_mc_sf_electron/fiducial)/lumi - xs_electron

syst_err_signal_prefire = (signal+signal_syst_unc_due_to_prefire)/(n_weighted_selected_data_mc_sf/fiducial)/lumi - xs

syst_err_signal_prefire_muon = (signal_muon+signal_syst_unc_due_to_prefire_muon)/(n_weighted_selected_data_mc_sf_muon/fiducial)/lumi - xs_muon

syst_err_signal_prefire_electron = (signal_electron+signal_syst_unc_due_to_prefire_electron)/(n_weighted_selected_data_mc_sf_electron/fiducial)/lumi - xs_electron

syst_err_signal_jer = (signal+signal_syst_unc_due_to_jer)/(n_weighted_selected_data_mc_sf/fiducial)/lumi - xs

syst_err_signal_jer_muon = (signal_muon+signal_syst_unc_due_to_jer_muon)/(n_weighted_selected_data_mc_sf_muon/fiducial)/lumi - xs_muon

syst_err_signal_jer_electron = (signal_electron+signal_syst_unc_due_to_jer_electron)/(n_weighted_selected_data_mc_sf_electron/fiducial)/lumi - xs_electron

syst_err_signal_jes = (signal+signal_syst_unc_due_to_jes)/(n_weighted_selected_data_mc_sf/fiducial)/lumi - xs

syst_err_signal_jes_muon = (signal_muon+signal_syst_unc_due_to_jes_muon)/(n_weighted_selected_data_mc_sf_muon/fiducial)/lumi - xs_muon

syst_err_signal_jes_electron = (signal_electron+signal_syst_unc_due_to_jes_electron)/(n_weighted_selected_data_mc_sf_electron/fiducial)/lumi - xs_electron

syst_err_signal_lumi = (signal+signal_syst_unc_due_to_lumi)/(n_weighted_selected_data_mc_sf/fiducial)/lumi - xs

syst_err_signal_lumi_muon = (signal_muon+signal_unc_due_to_lumi_muon)/(n_weighted_selected_data_mc_sf_muon/fiducial)/lumi - xs_muon

syst_err_signal_lumi_electron = (signal_electron+signal_unc_due_to_lumi_electron)/(n_weighted_selected_data_mc_sf_electron/fiducial)/lumi - xs_electron



syst_err_signal = math.sqrt(pow(syst_err_signal_fake_photon,2)+pow(syst_err_signal_fake_lepton,2) + pow(syst_err_signal_data_driven_stat,2)+pow(syst_err_signal_mc_stat,2) + pow(syst_err_signal_qcd_scale,2) + pow(syst_err_signal_pdf,2) + pow(syst_err_signal_lumi,2) + pow(syst_err_signal_pileup,2))

syst_err_signal_muon = math.sqrt(pow(syst_err_signal_fake_photon_muon,2)+pow(syst_err_signal_fake_lepton_muon,2) + pow(syst_err_signal_data_driven_stat_muon,2)+pow(syst_err_signal_mc_stat_muon,2) + pow(syst_err_signal_qcd_scale_muon,2) + pow(syst_err_signal_pdf_muon,2) + pow(syst_err_signal_lumi_muon,2) + pow(syst_err_signal_pileup_muon,2))

syst_err_signal_electron = math.sqrt(pow(syst_err_signal_fake_photon_electron,2)+pow(syst_err_signal_fake_lepton_electron,2) + pow(syst_err_signal_data_driven_stat_electron,2)+pow(syst_err_signal_mc_stat_electron,2) + pow(syst_err_signal_qcd_scale_electron,2) + pow(syst_err_signal_pdf_electron,2) + pow(syst_err_signal_lumi_electron,2) + pow(syst_err_signal_pileup_electron,2))

syst_err = math.sqrt(pow(syst_err_signal,2)+pow(syst_err_acc,2))

syst_err_electron = math.sqrt(pow(syst_err_signal_electron,2)+pow(syst_err_acc_electron,2))

syst_err_muon = math.sqrt(pow(syst_err_signal_muon,2)+pow(syst_err_acc_muon,2))

acc = n_weighted_selected_data_mc_sf/fiducial

acc_electron = n_weighted_selected_data_mc_sf_electron/fiducial

print "acc_electron = "+str(acc_electron)

acc_muon = n_weighted_selected_data_mc_sf_muon/fiducial

for i in range(1,32):
    print xs_inputs_muon["xs_times_lumi_pdf_variation"+str(i)] 
    print xs_inputs_electron["xs_times_lumi_pdf_variation"+str(i)] 
    assert(xs_inputs_muon["xs_times_lumi_pdf_variation"+str(i)] == xs_inputs_electron["xs_times_lumi_pdf_variation"+str(i)])

mean_pdf_acc=0
for i in range(1,32):
    mean_pdf_acc += (xs_inputs_muon["signal_mc_xs_data_mc_pdf_variation"+str(i)]+xs_inputs_electron["signal_mc_xs_data_mc_pdf_variation"+str(i)])/xs_inputs_muon["xs_times_lumi_pdf_variation"+str(i)]

mean_pdf_acc = mean_pdf_acc/31.0

stddev_pdf_acc = 0

for i in range(1,32):
    stddev_pdf_acc += pow(((xs_inputs_muon["signal_mc_xs_data_mc_pdf_variation"+str(i)]+xs_inputs_electron["signal_mc_xs_data_mc_pdf_variation"+str(i)])/xs_inputs_muon["xs_times_lumi_pdf_variation"+str(i)] - mean_pdf_acc),2)

stddev_pdf_acc = math.sqrt(stddev_pdf_acc/(31-1))

qcd_up_acc = (xs_inputs_muon["signal_mc_xs_data_mc_scale_variation3"]+xs_inputs_electron["signal_mc_xs_data_mc_scale_variation3"])/xs_inputs_muon["xs_times_lumi_scale_variation3"]
qcd_down_acc = (xs_inputs_muon["signal_mc_xs_data_mc_scale_variation7"]+xs_inputs_electron["signal_mc_xs_data_mc_scale_variation7"])/xs_inputs_muon["xs_times_lumi_scale_variation7"]

qcd_unc_acc=0.5*max(abs(qcd_up_acc - acc),abs(qcd_up_acc-qcd_down_acc),abs(acc-qcd_down_acc))






mean_pdf_acc_muon=0
for i in range(1,32):
    mean_pdf_acc_muon += (xs_inputs_muon["signal_mc_xs_data_mc_pdf_variation"+str(i)])/xs_inputs_muon["xs_times_lumi_pdf_variation"+str(i)]

mean_pdf_acc_muon = mean_pdf_acc_muon/31.0

stddev_pdf_acc_muon = 0

for i in range(1,32):
    stddev_pdf_acc_muon += pow(((xs_inputs_muon["signal_mc_xs_data_mc_pdf_variation"+str(i)])/xs_inputs_muon["xs_times_lumi_pdf_variation"+str(i)] - mean_pdf_acc_muon),2)

stddev_pdf_acc_muon = math.sqrt(stddev_pdf_acc_muon/(31-1))


qcd_up_acc_muon = (xs_inputs_muon["signal_mc_xs_data_mc_scale_variation3"])/xs_inputs_muon["xs_times_lumi_scale_variation3"]
qcd_down_acc_muon = (xs_inputs_muon["signal_mc_xs_data_mc_scale_variation7"])/xs_inputs_muon["xs_times_lumi_scale_variation7"]

qcd_unc_acc_muon=0.5*max(abs(qcd_up_acc_muon - acc_muon),abs(qcd_up_acc_muon-qcd_down_acc_muon),abs(acc_muon-qcd_down_acc_muon))



mean_pdf_acc_electron=0
for i in range(1,32):
    mean_pdf_acc_electron += (xs_inputs_electron["signal_mc_xs_data_mc_pdf_variation"+str(i)])/xs_inputs_electron["xs_times_lumi_pdf_variation"+str(i)]

mean_pdf_acc_electron = mean_pdf_acc_electron/31.0

stddev_pdf_acc_electron = 0

for i in range(1,32):
    stddev_pdf_acc_electron += pow(((xs_inputs_electron["signal_mc_xs_data_mc_pdf_variation"+str(i)])/xs_inputs_electron["xs_times_lumi_pdf_variation"+str(i)] - mean_pdf_acc_electron),2)

stddev_pdf_acc_electron = math.sqrt(stddev_pdf_acc_electron/(31-1))

qcd_up_acc_electron = (xs_inputs_electron["signal_mc_xs_data_mc_scale_variation3"])/xs_inputs_electron["xs_times_lumi_scale_variation3"]
qcd_down_acc_electron = (xs_inputs_electron["signal_mc_xs_data_mc_scale_variation7"])/xs_inputs_electron["xs_times_lumi_scale_variation7"]

qcd_unc_acc_electron=0.5*max(abs(qcd_up_acc_electron - acc_electron),abs(qcd_up_acc_electron-qcd_down_acc_electron),abs(acc_electron-qcd_down_acc_electron))

print qcd_unc_acc
print qcd_unc_acc_muon
print qcd_unc_acc_electron

print stddev_pdf_acc
print stddev_pdf_acc_muon
print stddev_pdf_acc_electron

err_on_acc_due_to_qcd_scale = qcd_unc_acc
err_on_acc_due_to_qcd_scale_muon = qcd_unc_acc_muon
err_on_acc_due_to_qcd_scale_electron = qcd_unc_acc_electron

err_on_acc_due_to_pdf = stddev_pdf_acc
err_on_acc_due_to_pdf_muon = stddev_pdf_acc_muon
err_on_acc_due_to_pdf_electron = stddev_pdf_acc_electron

err_on_acc_due_to_pileup = (((n_weighted_selected_data_mc_sf + n_weighted_selected_data_mc_sf_syst_unc_due_to_pileup_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_pileup_muon)/fiducial) - acc)

err_on_acc_due_to_pileup_electron = (((n_weighted_selected_data_mc_sf_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_pileup_electron)/fiducial) - acc_electron)

err_on_acc_due_to_pileup_muon = (((n_weighted_selected_data_mc_sf_muon +n_weighted_selected_data_mc_sf_syst_unc_due_to_pileup_muon)/fiducial) - acc_muon)

err_on_acc_due_to_prefire = (((n_weighted_selected_data_mc_sf + n_weighted_selected_data_mc_sf_syst_unc_due_to_prefire_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_prefire_muon)/fiducial) - acc)

err_on_acc_due_to_prefire_electron = (((n_weighted_selected_data_mc_sf_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_prefire_electron)/fiducial) - acc_electron)

err_on_acc_due_to_prefire_muon = (((n_weighted_selected_data_mc_sf_muon +n_weighted_selected_data_mc_sf_syst_unc_due_to_prefire_muon)/fiducial) - acc_muon)

err_on_acc_due_to_jer = (((n_weighted_selected_data_mc_sf + n_weighted_selected_data_mc_sf_syst_unc_due_to_jer_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_jer_muon)/fiducial) - acc)

err_on_acc_due_to_jer_electron = (((n_weighted_selected_data_mc_sf_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_jer_electron)/fiducial) - acc_electron)

err_on_acc_due_to_jer_muon = (((n_weighted_selected_data_mc_sf_muon +n_weighted_selected_data_mc_sf_syst_unc_due_to_jer_muon)/fiducial) - acc_muon)

err_on_acc_due_to_jes = (((n_weighted_selected_data_mc_sf + n_weighted_selected_data_mc_sf_syst_unc_due_to_jes_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_jes_muon)/fiducial) - acc)

err_on_acc_due_to_jes_electron = (((n_weighted_selected_data_mc_sf_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_jes_electron)/fiducial) - acc_electron)

err_on_acc_due_to_jes_muon = (((n_weighted_selected_data_mc_sf_muon +n_weighted_selected_data_mc_sf_syst_unc_due_to_jes_muon)/fiducial) - acc_muon)

err_on_acc_due_to_photon_id_sf = (((n_weighted_selected_data_mc_sf + n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_muon)/fiducial) - acc)

err_on_acc_due_to_photon_id_sf_electron = (((n_weighted_selected_data_mc_sf_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_electron)/fiducial) - acc_electron)

err_on_acc_due_to_photon_id_sf_muon = (((n_weighted_selected_data_mc_sf_muon +n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_muon)/fiducial) - acc_muon)

err_on_acc_due_to_electron_reco_sf = (((n_weighted_selected_data_mc_sf + n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_reco_sf_electron)/fiducial) - acc)

err_on_acc_due_to_electron_reco_sf_electron = (((n_weighted_selected_data_mc_sf_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_reco_sf_electron)/fiducial) - acc_electron)

err_on_acc_due_to_electron_hlt_sf = (((n_weighted_selected_data_mc_sf + n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_hlt_sf_electron)/fiducial) - acc)

err_on_acc_due_to_electron_hlt_sf_electron = (((n_weighted_selected_data_mc_sf_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_hlt_sf_electron)/fiducial) - acc_electron)

err_on_acc_due_to_electron_id_sf = (((n_weighted_selected_data_mc_sf + n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_id_sf_electron)/fiducial) - acc)

err_on_acc_due_to_electron_id_sf_electron = (((n_weighted_selected_data_mc_sf_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_id_sf_electron)/fiducial) - acc_electron)

err_on_acc_due_to_muon_id_sf = (((n_weighted_selected_data_mc_sf + n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_id_sf_muon)/fiducial) - acc)

err_on_acc_due_to_muon_id_sf_muon = (((n_weighted_selected_data_mc_sf_muon + n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_id_sf_muon)/fiducial) - acc_muon)

err_on_acc_due_to_muon_iso_sf = (((n_weighted_selected_data_mc_sf + n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_iso_sf_muon)/fiducial) - acc)

err_on_acc_due_to_muon_iso_sf_muon = (((n_weighted_selected_data_mc_sf_muon + n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_iso_sf_muon)/fiducial) - acc_muon)

err_on_acc_due_to_muon_hlt_sf = (((n_weighted_selected_data_mc_sf + n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_hlt_sf_muon)/fiducial) - acc)

err_on_acc_due_to_muon_hlt_sf_muon = (((n_weighted_selected_data_mc_sf_muon + n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_hlt_sf_muon)/fiducial) - acc_muon)

err_on_acc = math.sqrt(pow(err_on_acc_due_to_qcd_scale,2)+pow(err_on_acc_due_to_pdf,2)+pow(err_on_acc_due_to_electron_id_sf,2) + pow(err_on_acc_due_to_electron_reco_sf,2)+pow(err_on_acc_due_to_electron_hlt_sf,2)+pow(err_on_acc_due_to_muon_id_sf,2)+pow(err_on_acc_due_to_muon_iso_sf,2)+pow(err_on_acc_due_to_muon_hlt_sf,2)+pow(err_on_acc_due_to_photon_id_sf,2) + pow(err_on_acc_due_to_pileup,2))

print err_on_acc_due_to_muon_id_sf
print n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_id_sf_muon
print n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_iso_sf_muon
#import sys
#sys.exit(0)

err_on_acc_muon = math.sqrt(pow(err_on_acc_due_to_qcd_scale_muon,2)+pow(err_on_acc_due_to_pdf_muon,2)+pow(err_on_acc_due_to_muon_id_sf_muon,2)+pow(err_on_acc_due_to_muon_iso_sf_muon,2)++pow(err_on_acc_due_to_muon_hlt_sf_muon,2)+pow(err_on_acc_due_to_photon_id_sf_muon,2) + pow(err_on_acc_due_to_pileup_muon,2))

err_on_acc_electron = math.sqrt(pow(err_on_acc_due_to_qcd_scale_electron,2)+pow(err_on_acc_due_to_pdf_electron,2)+pow(err_on_acc_due_to_electron_id_sf_electron,2) + pow(err_on_acc_due_to_electron_reco_sf_electron,2)+pow(err_on_acc_due_to_electron_hlt_sf_electron,2)+pow(err_on_acc_due_to_photon_id_sf_electron,2) + pow(err_on_acc_due_to_pileup_electron,2))

print "acc = %.6f \pm %.6f "%(acc,err_on_acc)
print "acc_muon = %.6f \pm %.6f "%(acc_muon,err_on_acc_muon)
print "acc_electron = %.6f \pm %.6f "%(acc_electron,err_on_acc_electron)

print """
\\begin{table}[htbp]
\\begin{center}
\\begin{tabular}{|c|c|}
\\hline
Category & $A\\epsilon$  \\\\
\\hline \\hline
total & $%0.3f$ \\%% \\\\
\\hline
electron & $%0.3f$ \\%% \\\\
\\hline
muon & $%0.3f$ \\%% \\\\
\\hline
\\end{tabular}
\\end{center}
\\caption{Acceptance times efficiency for the $W\\gamma$+jets process.}
\\label{tab:wg_acc_eff}
\\end{table}
"""%(
acc*100,
acc_electron*100,
acc_muon*100,
)


print """
\\begin{table}[htbp]
\\begin{center}
\\begin{tabular}{|c|c|c|c|}
\\hline
   & total & muon & electron  \\\\
\\hline \\hline
pileup & %0.2f & %0.2f &  %0.2f \\\\
\\hline
prefire & %0.2f & %0.2f &  %0.2f \\\\
\\hline
jer & %0.2f & %0.2f &  %0.2f \\\\
\\hline
jes & %0.2f & %0.2f &  %0.2f \\\\
\\hline
electron ID SF & %0.2f & 0 &  %0.2f \\\\
\\hline
electron reconstruction SF & %0.2f & 0 & %0.2f \\\\
\\hline
electron HLT SF & %0.2f & 0 & %0.2f \\\\
\\hline
muon ID SF & %0.2f & %0.2f & 0 \\\\
\\hline
muon isolation SF &  %0.2f & %0.2f & 0 \\\\
\\hline
muon HLT SF &  %0.2f & %0.2f & 0 \\\\
\\hline
photon ID SF & %0.2f & %0.2f & %0.2f \\\\
\\hline
QCD Scale & %0.2f & %0.2f & %0.2f \\\\
\\hline
PDF & %0.2f & %0.2f & %0.2f \\\\
\\hline
\\end{tabular}
\\end{center}
\\caption{Uncertainties on the acceptance times efficiency (in percent).}
\\label{tab:wg_acc_eff_unc}
\\end{table}
"""%(
100*err_on_acc_due_to_pileup/acc,
100*err_on_acc_due_to_pileup_muon/acc_muon,
100*err_on_acc_due_to_pileup_electron/acc_electron,
100*err_on_acc_due_to_prefire/acc,
100*err_on_acc_due_to_prefire_muon/acc_muon,
100*err_on_acc_due_to_prefire_electron/acc_electron,
100*err_on_acc_due_to_jer/acc,
100*err_on_acc_due_to_jer_muon/acc_muon,
100*err_on_acc_due_to_jer_electron/acc_electron,
100*err_on_acc_due_to_jes/acc,
100*err_on_acc_due_to_jes_muon/acc_muon,
100*err_on_acc_due_to_jes_electron/acc_electron,
100*err_on_acc_due_to_electron_id_sf/acc,
100*err_on_acc_due_to_electron_id_sf_electron/acc_electron,
100*err_on_acc_due_to_electron_reco_sf/acc,
100*err_on_acc_due_to_electron_reco_sf_electron/acc_electron,
100*err_on_acc_due_to_electron_hlt_sf/acc,
100*err_on_acc_due_to_electron_hlt_sf_electron/acc_electron,
100*err_on_acc_due_to_muon_id_sf/acc,
100*err_on_acc_due_to_muon_id_sf_muon/acc_muon,
100*err_on_acc_due_to_muon_iso_sf/acc,
100*err_on_acc_due_to_muon_iso_sf_muon/acc_muon,
100*err_on_acc_due_to_muon_hlt_sf/acc,
100*err_on_acc_due_to_muon_hlt_sf_muon/acc_muon,
100*err_on_acc_due_to_photon_id_sf/acc,
100*err_on_acc_due_to_photon_id_sf_muon/acc_muon,
100*err_on_acc_due_to_photon_id_sf_electron/acc_electron,
100*err_on_acc_due_to_qcd_scale/acc,
100*err_on_acc_due_to_qcd_scale_muon/acc_muon,
100*err_on_acc_due_to_qcd_scale_electron/acc_electron,
100*err_on_acc_due_to_pdf/acc,
100*err_on_acc_due_to_pdf_muon/acc_muon,
100*err_on_acc_due_to_pdf_electron/acc_electron
)

print """
\\begin{table}[htbp]
\\begin{center}
\\begin{tabular}{|c|c|c|c|}
\\hline
   & total & muon & electron  \\\\
\\hline \\hline
pileup & %0.2f & %0.2f &  %0.2f \\\\
\\hline
prefire & %0.2f & %0.2f &  %0.2f \\\\
\\hline
jer & %0.2f & %0.2f &  %0.2f \\\\
\\hline
jes & %0.2f & %0.2f &  %0.2f \\\\
\\hline
fake photon method & %0.2f & %0.2f &  %0.2f \\\\
\\hline
fake lepton method & %0.2f & %0.2f & %0.2f \\\\
\\hline
data-driven stat & %0.2f & %0.2f & %0.2f \\\\
\\hline
simulation stat &  %0.2f & %0.2f & %0.2f \\\\
\\hline
QCD scale &  %0.2f & %0.2f & %0.2f \\\\
\\hline
PDF &  %0.2f & %0.2f & %0.2f \\\\
\\hline
lumi &  %0.2f & %0.2f & %0.2f \\\\
\\hline
\\end{tabular}
\\end{center}
\\caption{Uncertainties on the number of signal events (in percent of the number of signal events).}
\\label{tab:wg_n_sig_unc}
\\end{table}
"""%(
100*signal_syst_unc_due_to_pileup/signal,
100*signal_syst_unc_due_to_pileup_muon/signal_muon,
100*signal_syst_unc_due_to_pileup_electron/signal_electron,
100*signal_syst_unc_due_to_prefire/signal,
100*signal_syst_unc_due_to_prefire_muon/signal_muon,
100*signal_syst_unc_due_to_prefire_electron/signal_electron,
100*signal_syst_unc_due_to_jer/signal,
100*signal_syst_unc_due_to_jer_muon/signal_muon,
100*signal_syst_unc_due_to_jer_electron/signal_electron,
100*signal_syst_unc_due_to_jes/signal,
100*signal_syst_unc_due_to_jes_muon/signal_muon,
100*signal_syst_unc_due_to_jes_electron/signal_electron,
100*signal_syst_unc_due_to_fake_photon/signal,
100*signal_syst_unc_due_to_fake_photon_muon/signal_muon,
100*signal_syst_unc_due_to_fake_photon_electron/signal_electron,
100*signal_syst_unc_due_to_fake_lepton/signal,
100*signal_syst_unc_due_to_fake_lepton_muon/signal_muon,
100*signal_syst_unc_due_to_fake_lepton_electron/signal_electron,
100*unc_due_to_data_driven_stat/signal,
100*unc_due_to_data_driven_stat_muon/signal_muon,
100*unc_due_to_data_driven_stat_electron/signal_electron,
100*unc_due_to_mc_stat/signal,
100*unc_due_to_mc_stat_muon/signal_muon,
100*unc_due_to_mc_stat_electron/signal_electron,
100*signal_unc_due_to_qcd_scale/signal,
100*signal_unc_due_to_qcd_scale_muon/signal_muon,
100*signal_unc_due_to_qcd_scale_electron/signal_electron,
100*stddev_pdf/signal,
100*stddev_pdf_muon/signal_muon,
100*stddev_pdf_electron/signal_electron,
100*signal_syst_unc_due_to_lumi/signal,
100*signal_unc_due_to_lumi_muon/signal_muon,
100*signal_unc_due_to_lumi_electron/signal_electron,
)

print "xs = " +str(xs) + " +/- " + str(stat_err) + " (stat) +/- " + str(syst_err) + " (syst) +/- " + str(lumi_err) + " (lumi)"

print "xs based on electron channel = " +str(xs_electron) + " +/- " + str(stat_err_electron) + " (stat) +/- " + str(syst_err_electron) + " (syst) +/- "  + str(lumi_err_electron) + " (lumi)"

print "xs based on muon channel = " +str(xs_muon) + " +/- "+ str(stat_err_muon) + " (stat) +/- " + str(syst_err_muon) + " (syst) +/- "  + str(lumi_err_muon) + " (lumi)" 

print "xs: \\sigma = %.2f \pm %.2f \\text{ (stat)} \pm %.2f \\text{ (syst)} \pm %.2f \\text{ (lumi) pb}" % (xs,stat_err,syst_err,lumi_err)

print "xs based on electron channel: \\sigma = %.2f \pm %.2f \\text{ (stat)} \pm %.2f \\text{ (syst)} \pm %.2f \\text{ (lumi) pb}" % (xs_electron,stat_err_electron,syst_err_electron,lumi_err_electron)

print "xs based on muon channel: \\sigma = %.2f \pm %.2f \\text{ (stat)} \pm %.2f \\text{ (syst)} \pm %.2f \\text{ (lumi) pb}" % (xs_muon,stat_err_muon,syst_err_muon,lumi_err_muon)

