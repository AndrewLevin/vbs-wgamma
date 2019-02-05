import json
import math

xs_inputs_muon = json.load(open("xs_inputs_muon.txt"))
xs_inputs_electron = json.load(open("xs_inputs_electron.txt"))

#xs_inputs_muon = json.load(open("xs_inputs_muon.txt.bak"))
#xs_inputs_electron = json.load(open("xs_inputs_electron.txt.bak"))

#xs_inputs_muon = json.load(open("xs_inputs/xs_inputs_muon.txt"))
#xs_inputs_electron = json.load(open("xs_inputs/xs_inputs_electron.txt"))

#xs_inputs_muon = json.load(open("xs_inputs/xs_inputs_muon.binned.txt"))
#xs_inputs_electron = json.load(open("xs_inputs/xs_inputs_electron.binned.txt"))

#xs_inputs_muon = json.load(open("xs_inputs/xs_inputs_muon.unbinned.txt"))
#xs_inputs_electron = json.load(open("xs_inputs/xs_inputs_electron.unbinned.txt"))

from pprint import pprint

#pprint(xs_inputs_muon)
#pprint(xs_inputs_electron)

assert(xs_inputs_muon["fiducial_region_cuts_efficiency"] == xs_inputs_electron["fiducial_region_cuts_efficiency"])
assert(xs_inputs_muon["n_weighted_run_over"] == xs_inputs_electron["n_weighted_run_over"])

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

    if xs_inputs_muon["n_signal_syst_unc_due_to_fake_photon_stat_up_bin"+str(i)] < 100:
        sum_muon_photon_stat = sum_muon_photon_stat + pow(xs_inputs_muon["n_signal_syst_unc_due_to_fake_photon_stat_up_bin"+str(i)],2)
    else:
        print i
        print xs_inputs_muon["n_signal_syst_unc_due_to_fake_photon_stat_up_bin"+str(i)]

    if xs_inputs_electron["n_signal_syst_unc_due_to_fake_photon_stat_up_bin"+str(i)] < 100:
        sum_electron_photon_stat = sum_electron_photon_stat + pow(xs_inputs_electron["n_signal_syst_unc_due_to_fake_photon_stat_up_bin"+str(i)],2)
    else:
        print i
        print xs_inputs_electron["n_signal_syst_unc_due_to_fake_photon_stat_up_bin"+str(i)]

    if xs_inputs_muon["n_signal_syst_unc_due_to_fake_lepton_stat_up_bin"+str(i)] < 100:
        sum_muon_lepton_stat = sum_muon_lepton_stat + pow(xs_inputs_muon["n_signal_syst_unc_due_to_fake_lepton_stat_up_bin"+str(i)],2)
    else:
        print i
        print xs_inputs_muon["n_signal_syst_unc_due_to_fake_lepton_stat_up_bin"+str(i)]

    if xs_inputs_electron["n_signal_syst_unc_due_to_fake_lepton_stat_up_bin"+str(i)] < 100:
        sum_electron_lepton_stat = sum_electron_lepton_stat + pow(xs_inputs_electron["n_signal_syst_unc_due_to_fake_lepton_stat_up_bin"+str(i)],2)
    else:
        print i
        print xs_inputs_electron["n_signal_syst_unc_due_to_fake_lepton_stat_up_bin"+str(i)]

    if xs_inputs_muon["n_signal_syst_unc_due_to_double_fake_stat_up_bin"+str(i)] < 100:
        sum_muon_double_stat = sum_muon_double_stat + pow(xs_inputs_muon["n_signal_syst_unc_due_to_double_fake_stat_up_bin"+str(i)],2)
    else:
        print i
        print xs_inputs_muon["n_signal_syst_unc_due_to_double_fake_stat_up_bin"+str(i)]

    if xs_inputs_electron["n_signal_syst_unc_due_to_double_fake_stat_up_bin"+str(i)] < 100:
        sum_electron_double_stat = sum_electron_double_stat + pow(xs_inputs_electron["n_signal_syst_unc_due_to_double_fake_stat_up_bin"+str(i)],2)
    else:
        print i
        print xs_inputs_electron["n_signal_syst_unc_due_to_double_fake_stat_up_bin"+str(i)]

    if xs_inputs_muon["n_signal_syst_unc_due_to_zg_stat_up_bin"+str(i)] < 100:
        sum_muon_zg_stat = sum_muon_zg_stat + pow(xs_inputs_muon["n_signal_syst_unc_due_to_zg_stat_up_bin"+str(i)],2)
    else:
        print i
        print xs_inputs_muon["n_signal_syst_unc_due_to_zg_stat_up_bin"+str(i)]

    if xs_inputs_electron["n_signal_syst_unc_due_to_zg_stat_up_bin"+str(i)] < 100:
        sum_electron_zg_stat = sum_electron_zg_stat + pow(xs_inputs_electron["n_signal_syst_unc_due_to_zg_stat_up_bin"+str(i)],2)
    else:
        print i
        print xs_inputs_electron["n_signal_syst_unc_due_to_zg_stat_up_bin"+str(i)]

    if xs_inputs_muon["n_signal_syst_unc_due_to_vv_stat_up_bin"+str(i)] < 100:
        sum_muon_vv_stat = sum_muon_vv_stat + pow(xs_inputs_muon["n_signal_syst_unc_due_to_vv_stat_up_bin"+str(i)],2)
    else:
        print i
        print xs_inputs_muon["n_signal_syst_unc_due_to_vv_stat_up_bin"+str(i)]

    if xs_inputs_electron["n_signal_syst_unc_due_to_vv_stat_up_bin"+str(i)] < 100:
        sum_electron_vv_stat = sum_electron_vv_stat + pow(xs_inputs_electron["n_signal_syst_unc_due_to_vv_stat_up_bin"+str(i)],2)
    else:
        print i
        print xs_inputs_electron["n_signal_syst_unc_due_to_vv_stat_up_bin"+str(i)]

    if xs_inputs_muon["n_signal_syst_unc_due_to_top_stat_up_bin"+str(i)] < 100:
        sum_muon_top_stat = sum_muon_top_stat + pow(xs_inputs_muon["n_signal_syst_unc_due_to_top_stat_up_bin"+str(i)],2)
    else:
        print i
        print xs_inputs_muon["n_signal_syst_unc_due_to_top_stat_up_bin"+str(i)]

    if xs_inputs_electron["n_signal_syst_unc_due_to_top_stat_up_bin"+str(i)] < 100:
        sum_electron_top_stat = sum_electron_top_stat + pow(xs_inputs_electron["n_signal_syst_unc_due_to_top_stat_up_bin"+str(i)],2)
    else:
        print i
        print xs_inputs_electron["n_signal_syst_unc_due_to_top_stat_up_bin"+str(i)]


mean_pdf=0
for i in range(1,32):
    mean_pdf += xs_inputs_muon["n_signal_syst_unc_due_to_zg_pdf_variation"+str(i)]+xs_inputs_muon["n_signal_muon"]+xs_inputs_electron["n_signal_syst_unc_due_to_zg_pdf_variation"+str(i)]+xs_inputs_electron["n_signal_electron"]

mean_pdf = mean_pdf/31

stddev_pdf = 0

for i in range(1,32):
    stddev_pdf += pow(xs_inputs_muon["n_signal_syst_unc_due_to_zg_pdf_variation"+str(i)]+xs_inputs_muon["n_signal_muon"]+xs_inputs_electron["n_signal_syst_unc_due_to_zg_pdf_variation"+str(i)]+xs_inputs_electron["n_signal_electron"] - mean_pdf,2)

stddev_pdf = math.sqrt(stddev_pdf/(31-1))

mean_pdf_muon=0
for i in range(1,32):
    mean_pdf_muon += xs_inputs_muon["n_signal_syst_unc_due_to_zg_pdf_variation"+str(i)]+xs_inputs_muon["n_signal_muon"]

mean_pdf_muon = mean_pdf_muon/31

stddev_pdf_muon = 0

for i in range(1,32):
    stddev_pdf_muon += pow(xs_inputs_muon["n_signal_syst_unc_due_to_zg_pdf_variation"+str(i)]+xs_inputs_muon["n_signal_muon"]- mean_pdf_muon,2)

stddev_pdf_muon = math.sqrt(stddev_pdf_muon/(31-1))


mean_pdf_electron=0
for i in range(1,32):
    mean_pdf_electron += xs_inputs_electron["n_signal_syst_unc_due_to_zg_pdf_variation"+str(i)]+xs_inputs_electron["n_signal_electron"]

mean_pdf_electron = mean_pdf_electron/31

stddev_pdf_electron = 0

for i in range(1,32):
    stddev_pdf_electron += pow(xs_inputs_electron["n_signal_syst_unc_due_to_zg_pdf_variation"+str(i)]+xs_inputs_electron["n_signal_electron"]- mean_pdf_electron,2)

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

n_signal_unc_due_to_qcd_scale_muon = max(abs(xs_inputs_muon["n_signal_syst_unc_due_to_zg_scale_variation0"]),abs(xs_inputs_muon["n_signal_syst_unc_due_to_zg_scale_variation1"]),abs(xs_inputs_muon["n_signal_syst_unc_due_to_zg_scale_variation3"]),abs(xs_inputs_muon["n_signal_syst_unc_due_to_zg_scale_variation4"]),abs(xs_inputs_muon["n_signal_syst_unc_due_to_zg_scale_variation6"]),abs(xs_inputs_muon["n_signal_syst_unc_due_to_zg_scale_variation7"]))

n_signal_unc_due_to_qcd_scale_electron = max(abs(xs_inputs_electron["n_signal_syst_unc_due_to_zg_scale_variation0"]),abs(xs_inputs_electron["n_signal_syst_unc_due_to_zg_scale_variation1"]),abs(xs_inputs_electron["n_signal_syst_unc_due_to_zg_scale_variation3"]),abs(xs_inputs_electron["n_signal_syst_unc_due_to_zg_scale_variation4"]),abs(xs_inputs_electron["n_signal_syst_unc_due_to_zg_scale_variation6"]),abs(xs_inputs_electron["n_signal_syst_unc_due_to_zg_scale_variation7"]))

n_signal_unc_due_to_qcd_scale = max(abs(xs_inputs_electron["n_signal_syst_unc_due_to_zg_scale_variation0"]+xs_inputs_muon["n_signal_syst_unc_due_to_zg_scale_variation0"]),abs(xs_inputs_electron["n_signal_syst_unc_due_to_zg_scale_variation1"]+xs_inputs_muon["n_signal_syst_unc_due_to_zg_scale_variation1"]),abs(xs_inputs_electron["n_signal_syst_unc_due_to_zg_scale_variation3"]+xs_inputs_muon["n_signal_syst_unc_due_to_zg_scale_variation3"]),abs(xs_inputs_electron["n_signal_syst_unc_due_to_zg_scale_variation4"]+xs_inputs_muon["n_signal_syst_unc_due_to_zg_scale_variation4"]),abs(xs_inputs_electron["n_signal_syst_unc_due_to_zg_scale_variation6"]+xs_inputs_muon["n_signal_syst_unc_due_to_zg_scale_variation6"]),abs(xs_inputs_electron["n_signal_syst_unc_due_to_zg_scale_variation7"]+xs_inputs_muon["n_signal_syst_unc_due_to_zg_scale_variation7"]))

fiducial_region_cuts_efficiency  =  xs_inputs_muon["fiducial_region_cuts_efficiency"]
n_weighted_run_over  =  xs_inputs_muon["n_weighted_run_over"]

n_signal_muon  =  xs_inputs_muon["n_signal_muon"]
n_signal_syst_unc_due_to_fake_photon_muon  =  xs_inputs_muon["n_signal_syst_unc_due_to_fake_photon_muon"]
n_signal_syst_unc_due_to_fake_lepton_muon  =  xs_inputs_muon["n_signal_syst_unc_due_to_fake_lepton_muon"]
n_signal_stat_unc_muon  =  xs_inputs_muon["n_signal_stat_unc_muon"]
n_weighted_selected_data_mc_sf_muon  =  xs_inputs_muon["n_weighted_selected_data_mc_sf_muon"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_id_sf_muon  =  xs_inputs_muon["n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_id_sf_muon"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_iso_sf_muon  =  xs_inputs_muon["n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_iso_sf_muon"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_muon  =  xs_inputs_muon["n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_muon"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_pdf_muon  =  0
n_weighted_selected_data_mc_sf_syst_unc_due_to_qcd_scale_muon  =  0

n_signal_electron  =  xs_inputs_electron["n_signal_electron"]
n_signal_syst_unc_due_to_fake_photon_electron  =  xs_inputs_electron["n_signal_syst_unc_due_to_fake_photon_electron"]
n_signal_syst_unc_due_to_fake_lepton_electron  =  xs_inputs_electron["n_signal_syst_unc_due_to_fake_lepton_electron"]
n_signal_stat_unc_electron  =  xs_inputs_electron["n_signal_stat_unc_electron"]
n_weighted_selected_data_mc_sf_electron  =  xs_inputs_electron["n_weighted_selected_data_mc_sf_electron"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_id_sf_electron  =  xs_inputs_electron["n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_id_sf_electron"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_reco_sf_electron  =  xs_inputs_electron["n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_reco_sf_electron"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_electron =   xs_inputs_electron["n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_electron"]
n_weighted_selected_data_mc_sf_syst_unc_due_to_pdf_electron  =  0
n_weighted_selected_data_mc_sf_syst_unc_due_to_qcd_scale_electron  =  0

n_signal = n_signal_muon+n_signal_electron

n_signal_syst_unc_due_to_fake_photon = n_signal_syst_unc_due_to_fake_photon_electron+n_signal_syst_unc_due_to_fake_photon_muon

n_signal_syst_unc_due_to_fake_lepton = n_signal_syst_unc_due_to_fake_lepton_electron+n_signal_syst_unc_due_to_fake_lepton_muon

n_weighted_selected_data_mc_sf = n_weighted_selected_data_mc_sf_electron + n_weighted_selected_data_mc_sf_muon

n_signal_stat_unc = math.sqrt(pow(n_signal_stat_unc_electron,2) + pow(n_signal_stat_unc_muon,2))

n_weighted_selected_data_mc_sf_syst_unc = math.sqrt(pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_id_sf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_iso_sf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_pdf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_qcd_scale_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_id_sf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_reco_sf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_pdf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_qcd_scale_electron,2)+pow(unc_due_to_mc_stat_muon,2)+pow(unc_due_to_data_driven_stat_muon,2)+pow(unc_due_to_mc_stat_electron,2)+pow(unc_due_to_data_driven_stat_electron,2))

n_weighted_selected_data_mc_sf_syst_unc_muon = math.sqrt(pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_id_sf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_iso_sf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_pdf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_qcd_scale_muon,2)+pow(unc_due_to_mc_stat_muon,2)+pow(unc_due_to_data_driven_stat_muon,2))

n_weighted_selected_data_mc_sf_syst_unc_electron = math.sqrt(pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_id_sf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_reco_sf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_pdf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_qcd_scale_electron,2)+pow(unc_due_to_mc_stat_electron,2)+pow(unc_due_to_data_driven_stat_electron,2))

xs =  n_signal/(n_weighted_selected_data_mc_sf*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency)

xs_electron =  n_signal_electron/(n_weighted_selected_data_mc_sf_electron*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency)

xs_muon =  n_signal_muon/(n_weighted_selected_data_mc_sf_muon*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency)

lumi_err =  n_signal/(n_weighted_selected_data_mc_sf*35.9*0.975*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs

lumi_err_electron =  n_signal_electron/(n_weighted_selected_data_mc_sf_electron*35.9*0.975*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs_electron

lumi_err_muon =  n_signal_muon/(n_weighted_selected_data_mc_sf_muon*35.9*0.975*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs_muon

stat_err = (n_signal+n_signal_stat_unc)/(n_weighted_selected_data_mc_sf*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs

stat_err_electron = (n_signal_electron+n_signal_stat_unc_electron)/(n_weighted_selected_data_mc_sf_electron*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs_electron

stat_err_muon = (n_signal_muon+n_signal_stat_unc_muon)/(n_weighted_selected_data_mc_sf_muon*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs_muon

syst_err_acc = n_signal/((n_weighted_selected_data_mc_sf - n_weighted_selected_data_mc_sf_syst_unc)*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs

syst_err_acc_muon = n_signal_muon/((n_weighted_selected_data_mc_sf_muon - n_weighted_selected_data_mc_sf_syst_unc_muon)*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs_muon

syst_err_acc_electron = n_signal_electron/((n_weighted_selected_data_mc_sf_electron - n_weighted_selected_data_mc_sf_syst_unc_electron)*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs_electron

syst_err_n_signal_fake_photon = (n_signal+n_signal_syst_unc_due_to_fake_photon)/(n_weighted_selected_data_mc_sf*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs

syst_err_n_signal_fake_photon_muon = (n_signal_muon+n_signal_syst_unc_due_to_fake_photon_muon)/(n_weighted_selected_data_mc_sf_muon*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs_muon

syst_err_n_signal_fake_photon_electron = (n_signal_electron+n_signal_syst_unc_due_to_fake_photon_electron)/(n_weighted_selected_data_mc_sf_electron*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs_electron

syst_err_n_signal_fake_lepton = (n_signal+n_signal_syst_unc_due_to_fake_lepton)/(n_weighted_selected_data_mc_sf*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs

syst_err_n_signal_fake_lepton_muon = (n_signal_muon+n_signal_syst_unc_due_to_fake_lepton_muon)/(n_weighted_selected_data_mc_sf_muon*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs_muon

syst_err_n_signal_fake_lepton_electron = (n_signal_electron+n_signal_syst_unc_due_to_fake_lepton_electron)/(n_weighted_selected_data_mc_sf_electron*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs_electron




syst_err_n_signal_qcd_scale = (n_signal+n_signal_unc_due_to_qcd_scale)/(n_weighted_selected_data_mc_sf*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs

syst_err_n_signal_qcd_scale_muon = (n_signal_muon+n_signal_unc_due_to_qcd_scale_muon)/(n_weighted_selected_data_mc_sf_muon*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs_muon

syst_err_n_signal_qcd_scale_electron = (n_signal_electron+n_signal_unc_due_to_qcd_scale_electron)/(n_weighted_selected_data_mc_sf_electron*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs_electron



syst_err_n_signal_pdf = (n_signal+stddev_pdf)/(n_weighted_selected_data_mc_sf*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs

syst_err_n_signal_pdf_muon = (n_signal_muon+stddev_pdf_muon)/(n_weighted_selected_data_mc_sf_muon*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs_muon

syst_err_n_signal_pdf_electron = (n_signal_electron+stddev_pdf_electron)/(n_weighted_selected_data_mc_sf_electron*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs_electron




syst_err_n_signal_data_driven_stat = (n_signal+unc_due_to_data_driven_stat)/(n_weighted_selected_data_mc_sf*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs

syst_err_n_signal_data_driven_stat_muon = (n_signal_muon+unc_due_to_data_driven_stat_muon)/(n_weighted_selected_data_mc_sf_muon*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs_muon

syst_err_n_signal_data_driven_stat_electron = (n_signal_electron+unc_due_to_data_driven_stat_electron)/(n_weighted_selected_data_mc_sf_electron*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs_electron

 
syst_err_n_signal_mc_stat = (n_signal+unc_due_to_mc_stat)/(n_weighted_selected_data_mc_sf*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs

syst_err_n_signal_mc_stat_muon = (n_signal_muon+unc_due_to_mc_stat_muon)/(n_weighted_selected_data_mc_sf_muon*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs_muon

syst_err_n_signal_mc_stat_electron = (n_signal_electron+unc_due_to_mc_stat_electron)/(n_weighted_selected_data_mc_sf_electron*35.9*1000/n_weighted_run_over/fiducial_region_cuts_efficiency) - xs_electron





syst_err_n_signal = math.sqrt(pow(syst_err_n_signal_fake_photon,2)+pow(syst_err_n_signal_fake_lepton,2) + pow(syst_err_n_signal_data_driven_stat,2)+pow(syst_err_n_signal_mc_stat,2) + pow(syst_err_n_signal_qcd_scale,2) + pow(syst_err_n_signal_pdf,2))

syst_err_n_signal_muon = math.sqrt(pow(syst_err_n_signal_fake_photon_muon,2)+pow(syst_err_n_signal_fake_lepton_muon,2) + pow(syst_err_n_signal_data_driven_stat_muon,2)+pow(syst_err_n_signal_mc_stat_muon,2) + pow(syst_err_n_signal_qcd_scale_muon,2) + pow(syst_err_n_signal_pdf_muon,2))

syst_err_n_signal_electron = math.sqrt(pow(syst_err_n_signal_fake_photon_electron,2)+pow(syst_err_n_signal_fake_lepton_electron,2) + pow(syst_err_n_signal_data_driven_stat_electron,2)+pow(syst_err_n_signal_mc_stat_electron,2) + pow(syst_err_n_signal_qcd_scale_electron,2) + pow(syst_err_n_signal_pdf_electron,2))

syst_err = math.sqrt(pow(syst_err_n_signal,2)+pow(syst_err_acc,2))

syst_err_electron = math.sqrt(pow(syst_err_n_signal_electron,2)+pow(syst_err_acc_electron,2))

syst_err_muon = math.sqrt(pow(syst_err_n_signal_muon,2)+pow(syst_err_acc_muon,2))

acc = n_weighted_selected_data_mc_sf/n_weighted_run_over/fiducial_region_cuts_efficiency

acc_electron = n_weighted_selected_data_mc_sf_electron/n_weighted_run_over/fiducial_region_cuts_efficiency

acc_muon = n_weighted_selected_data_mc_sf_muon/n_weighted_run_over/fiducial_region_cuts_efficiency

for i in range(1,102):
    assert(xs_inputs_muon["n_weighted_run_over_pdf_variation"+str(i)] == xs_inputs_electron["n_weighted_run_over_pdf_variation"+str(i)])

mean_pdf_acc=0
for i in range(1,102):
    mean_pdf_acc += (xs_inputs_muon["n_weighted_selected_data_mc_sf_pdf_variation"+str(i)]+xs_inputs_electron["n_weighted_selected_data_mc_sf_pdf_variation"+str(i)])/xs_inputs_muon["n_weighted_run_over_pdf_variation"+str(i)]/fiducial_region_cuts_efficiency

mean_pdf_acc = mean_pdf_acc/101.0

stddev_pdf_acc = 0

for i in range(1,102):
    stddev_pdf_acc += pow(((xs_inputs_muon["n_weighted_selected_data_mc_sf_pdf_variation"+str(i)]+xs_inputs_electron["n_weighted_selected_data_mc_sf_pdf_variation"+str(i)])/xs_inputs_muon["n_weighted_run_over_pdf_variation"+str(i)]/fiducial_region_cuts_efficiency - mean_pdf_acc),2)

stddev_pdf_acc = math.sqrt(stddev_pdf_acc/(101-1))

qcd_up_acc = (xs_inputs_muon["n_weighted_selected_data_mc_sf_scale_variation3"]+xs_inputs_electron["n_weighted_selected_data_mc_sf_scale_variation3"])/xs_inputs_muon["n_weighted_run_over_scale_variation3"]/fiducial_region_cuts_efficiency
qcd_down_acc = (xs_inputs_muon["n_weighted_selected_data_mc_sf_scale_variation7"]+xs_inputs_electron["n_weighted_selected_data_mc_sf_scale_variation7"])/xs_inputs_muon["n_weighted_run_over_scale_variation7"]/fiducial_region_cuts_efficiency

qcd_unc_acc=0.5*max(abs(qcd_up_acc - acc),abs(qcd_up_acc-qcd_down_acc),abs(acc-qcd_down_acc))






mean_pdf_acc_muon=0
for i in range(1,102):
    mean_pdf_acc_muon += (xs_inputs_muon["n_weighted_selected_data_mc_sf_pdf_variation"+str(i)])/xs_inputs_muon["n_weighted_run_over_pdf_variation"+str(i)]/fiducial_region_cuts_efficiency

mean_pdf_acc_muon = mean_pdf_acc_muon/101.0

stddev_pdf_acc_muon = 0

for i in range(1,102):
    stddev_pdf_acc_muon += pow(((xs_inputs_muon["n_weighted_selected_data_mc_sf_pdf_variation"+str(i)])/xs_inputs_muon["n_weighted_run_over_pdf_variation"+str(i)]/fiducial_region_cuts_efficiency - mean_pdf_acc_muon),2)

stddev_pdf_acc_muon = math.sqrt(stddev_pdf_acc_muon/(101-1))


qcd_up_acc_muon = (xs_inputs_muon["n_weighted_selected_data_mc_sf_scale_variation3"])/xs_inputs_muon["n_weighted_run_over_scale_variation3"]/fiducial_region_cuts_efficiency
qcd_down_acc_muon = (xs_inputs_muon["n_weighted_selected_data_mc_sf_scale_variation7"])/xs_inputs_muon["n_weighted_run_over_scale_variation7"]/fiducial_region_cuts_efficiency

qcd_unc_acc_muon=0.5*max(abs(qcd_up_acc_muon - acc_muon),abs(qcd_up_acc_muon-qcd_down_acc_muon),abs(acc_muon-qcd_down_acc_muon))






mean_pdf_acc_electron=0
for i in range(1,102):
    mean_pdf_acc_electron += (xs_inputs_electron["n_weighted_selected_data_mc_sf_pdf_variation"+str(i)])/xs_inputs_electron["n_weighted_run_over_pdf_variation"+str(i)]/fiducial_region_cuts_efficiency

mean_pdf_acc_electron = mean_pdf_acc_electron/101.0

stddev_pdf_acc_electron = 0

for i in range(1,102):
    stddev_pdf_acc_electron += pow(((xs_inputs_electron["n_weighted_selected_data_mc_sf_pdf_variation"+str(i)])/xs_inputs_electron["n_weighted_run_over_pdf_variation"+str(i)]/fiducial_region_cuts_efficiency - mean_pdf_acc_electron),2)

stddev_pdf_acc_electron = math.sqrt(stddev_pdf_acc_electron/(101-1))


qcd_up_acc_electron = (xs_inputs_electron["n_weighted_selected_data_mc_sf_scale_variation3"])/xs_inputs_electron["n_weighted_run_over_scale_variation3"]/fiducial_region_cuts_efficiency
qcd_down_acc_electron = (xs_inputs_electron["n_weighted_selected_data_mc_sf_scale_variation7"])/xs_inputs_electron["n_weighted_run_over_scale_variation7"]/fiducial_region_cuts_efficiency

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

err_on_acc_due_to_photon_id_sf = (((n_weighted_selected_data_mc_sf + n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_muon)/n_weighted_run_over/fiducial_region_cuts_efficiency) - acc)

err_on_acc_due_to_photon_id_sf_electron = (((n_weighted_selected_data_mc_sf_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_electron)/n_weighted_run_over/fiducial_region_cuts_efficiency) - acc_electron)

err_on_acc_due_to_photon_id_sf_muon = (((n_weighted_selected_data_mc_sf_muon +n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_muon)/n_weighted_run_over/fiducial_region_cuts_efficiency) - acc_muon)

err_on_acc_due_to_electron_reco_sf = (((n_weighted_selected_data_mc_sf + n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_reco_sf_electron)/n_weighted_run_over/fiducial_region_cuts_efficiency) - acc)

err_on_acc_due_to_electron_reco_sf_electron = (((n_weighted_selected_data_mc_sf_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_reco_sf_electron)/n_weighted_run_over/fiducial_region_cuts_efficiency) - acc_electron)

err_on_acc_due_to_electron_id_sf = (((n_weighted_selected_data_mc_sf + n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_id_sf_electron)/n_weighted_run_over/fiducial_region_cuts_efficiency) - acc)

err_on_acc_due_to_electron_id_sf_electron = (((n_weighted_selected_data_mc_sf_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_id_sf_electron)/n_weighted_run_over/fiducial_region_cuts_efficiency) - acc_electron)

err_on_acc_due_to_muon_id_sf = (((n_weighted_selected_data_mc_sf + n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_id_sf_muon)/n_weighted_run_over/fiducial_region_cuts_efficiency) - acc)

err_on_acc_due_to_muon_id_sf_muon = (((n_weighted_selected_data_mc_sf_muon + n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_id_sf_muon)/n_weighted_run_over/fiducial_region_cuts_efficiency) - acc_muon)

err_on_acc_due_to_muon_iso_sf = (((n_weighted_selected_data_mc_sf + n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_iso_sf_muon)/n_weighted_run_over/fiducial_region_cuts_efficiency) - acc)

err_on_acc_due_to_muon_iso_sf_muon = (((n_weighted_selected_data_mc_sf_muon + n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_iso_sf_muon)/n_weighted_run_over/fiducial_region_cuts_efficiency) - acc_muon)

err_on_acc = math.sqrt(pow(err_on_acc_due_to_qcd_scale,2)+pow(err_on_acc_due_to_pdf,2)+pow(err_on_acc_due_to_electron_id_sf,2) + pow(err_on_acc_due_to_electron_reco_sf,2)+pow(err_on_acc_due_to_muon_id_sf,2)+pow(err_on_acc_due_to_muon_iso_sf,2)+pow(err_on_acc_due_to_photon_id_sf,2))

err_on_acc_muon = math.sqrt(pow(err_on_acc_due_to_qcd_scale_muon,2)+pow(err_on_acc_due_to_pdf_muon,2)+pow(err_on_acc_due_to_muon_id_sf_muon,2)+pow(err_on_acc_due_to_muon_iso_sf_muon,2)+pow(err_on_acc_due_to_photon_id_sf_muon,2))

err_on_acc_electron = math.sqrt(pow(err_on_acc_due_to_qcd_scale_electron,2)+pow(err_on_acc_due_to_pdf_electron,2)+pow(err_on_acc_due_to_electron_id_sf_electron,2) + pow(err_on_acc_due_to_electron_reco_sf_electron,2)+pow(err_on_acc_due_to_photon_id_sf_electron,2))

print "acc = %.6f \pm %.6f "%(acc,err_on_acc)
print "acc_muon = %.6f \pm %.6f "%(acc_muon,err_on_acc_muon)
print "acc_electron = %.6f \pm %.6f "%(acc_electron,err_on_acc_electron)

print "xs = " +str(xs) + " +/- " + str(stat_err) + " (stat) +/- " + str(syst_err) + " (syst) +/- " + str(lumi_err) + " (lumi)"

print "xs based on electron channel = " +str(xs_electron) + " +/- " + str(stat_err_electron) + " (stat) +/- " + str(syst_err_electron) + " (syst) +/- "  + str(lumi_err_electron) + " (lumi)"

print "xs based on muon channel = " +str(xs_muon) + " +/- "+ str(stat_err_muon) + " (stat) +/- " + str(syst_err_muon) + " (syst) +/- "  + str(lumi_err_muon) + " (lumi)" 

print "xs: \\sigma = %.2f \pm %.2f \\text{ (stat)} \pm %.2f \\text{ (syst)} \pm %.2f \\text{ (lumi) pb}" % (xs,stat_err,syst_err,lumi_err)

print "xs based on electron channel: \\sigma = %.2f \pm %.2f \\text{ (stat)} \pm %.2f \\text{ (syst)} \pm %.2f \\text{ (lumi) pb}" % (xs_electron,stat_err_electron,syst_err_electron,lumi_err_electron)

print "xs based on muon channel: \\sigma = %.2f \pm %.2f \\text{ (stat)} \pm %.2f \\text{ (syst)} \pm %.2f \\text{ (lumi) pb}" % (xs_muon,stat_err_muon,syst_err_muon,lumi_err_muon)

print """
\\begin{table}[htbp]
\\begin{center}
\\begin{tabular}{|c|c|c|c|}
\\hline
   & total & muon & electron  \\\\
\\hline \\hline
electron ID SF & %0.2f & 0 &  %0.2f \\\\
\\hline
electron reconstruction SF & %0.2f & 0 & %0.2f \\\\
\\hline
muon ID SF & %0.2f & %0.2f & 0 \\\\
\\hline
muon isolation SF &  %0.2f & %0.2f & 0 \\\\
\\hline
photon ID SF & %0.2f & %0.2f & %0.2f \\\\
\\hline
PDF & %0.2f & %0.2f & %0.2f \\\\
\\hline
QCD Scale & %0.2f & %0.2f & %0.2f \\\\
\\hline
\\end{tabular}
\\end{center}
\\caption{Uncertainties on the acceptance times efficiency (in percent).}
\\label{tab:wg_acc_eff_unc}
\\end{table}
"""%(
100*err_on_acc_due_to_electron_id_sf/acc,
100*err_on_acc_due_to_electron_id_sf_electron/acc_electron,
100*err_on_acc_due_to_electron_reco_sf/acc,
100*err_on_acc_due_to_electron_reco_sf_electron/acc_electron,
100*err_on_acc_due_to_muon_id_sf/acc,
100*err_on_acc_due_to_muon_id_sf_muon/acc_muon,
100*err_on_acc_due_to_muon_iso_sf/acc,
100*err_on_acc_due_to_muon_iso_sf_muon/acc_muon,
100*err_on_acc_due_to_photon_id_sf/acc,
100*err_on_acc_due_to_photon_id_sf_muon/acc_muon,
100*err_on_acc_due_to_photon_id_sf_electron/acc_electron,
100*err_on_acc_due_to_pdf/acc,
100*err_on_acc_due_to_pdf_muon/acc_muon,
100*err_on_acc_due_to_pdf_electron/acc_electron,
100*err_on_acc_due_to_qcd_scale/acc,
100*err_on_acc_due_to_qcd_scale_muon/acc_muon,
100*err_on_acc_due_to_qcd_scale_electron/acc_electron,
)


print """
\\begin{table}[htbp]
\\begin{center}
\\begin{tabular}{|c|c|c|c|}
\\hline
   & total & muon & electron  \\\\
\\hline \\hline
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
\\end{tabular}
\\end{center}
\\caption{Uncertainties on the number of signal events (in percent of the number of signal events).}
\\label{tab:wg_n_sig_unc}
\\end{table}
"""%(
100*n_signal_syst_unc_due_to_fake_photon/n_signal,
100*n_signal_syst_unc_due_to_fake_photon_muon/n_signal_muon,
100*n_signal_syst_unc_due_to_fake_photon_electron/n_signal_electron,
100*n_signal_syst_unc_due_to_fake_lepton/n_signal,
100*n_signal_syst_unc_due_to_fake_lepton_muon/n_signal_muon,
100*n_signal_syst_unc_due_to_fake_lepton_electron/n_signal_electron,
100*unc_due_to_data_driven_stat/n_signal,
100*unc_due_to_data_driven_stat_muon/n_signal_muon,
100*unc_due_to_data_driven_stat_electron/n_signal_electron,
100*unc_due_to_mc_stat/n_signal,
100*unc_due_to_mc_stat_muon/n_signal_muon,
100*unc_due_to_mc_stat_electron/n_signal_electron,
100*n_signal_unc_due_to_qcd_scale/n_signal,
100*n_signal_unc_due_to_qcd_scale_muon/n_signal_muon,
100*n_signal_unc_due_to_qcd_scale_electron/n_signal_electron,
100*stddev_pdf/n_signal,
100*stddev_pdf_muon/n_signal_muon,
100*stddev_pdf_electron/n_signal_electron,
)
