import math

n_signal_electron = 10158.782842 

n_signal_muon = 17335.345719

n_signal_stat_unc_electron = 146.684973647

n_signal_stat_unc_muon = 268.75772812

n_weighted_selected_data_mc_sf_electron = 19363.7797862

n_weighted_selected_data_mc_sf_muon = 33287.8325007

n_weighted_run_over = 13700559.0

n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_id_sf_muon = 120.21169281

n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_iso_sf_muon = 9.05431938171

n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_muon = 198.763269424

#n_weighted_selected_data_mc_sf_syst_unc_due_to_pdf_muon = 152.724895832

#n_weighted_selected_data_mc_sf_syst_unc_due_to_qcd_scale_muon = 1103.22212791

n_weighted_selected_data_mc_sf_syst_unc_due_to_pdf_muon = 0

n_weighted_selected_data_mc_sf_syst_unc_due_to_qcd_scale_muon = 0

n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_id_sf_electron = 113.694311142

n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_reco_sf_electron = 50.9384012222

n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_electron = 115.788023949

#n_weighted_selected_data_mc_sf_syst_unc_due_to_pdf_electron = 88.8418873308

#n_weighted_selected_data_mc_sf_syst_unc_due_to_qcd_scale_electron = 721.746954918

n_weighted_selected_data_mc_sf_syst_unc_due_to_pdf_electron = 0

n_weighted_selected_data_mc_sf_syst_unc_due_to_qcd_scale_electron = 0

n_signal = n_signal_muon+n_signal_electron

n_weighted_selected_data_mc_sf = n_weighted_selected_data_mc_sf_electron + n_weighted_selected_data_mc_sf_muon

n_signal_stat_unc = math.sqrt(pow(n_signal_stat_unc_electron,2) + pow(n_signal_stat_unc_muon,2))

n_weighted_selected_data_mc_sf_syst_unc = math.sqrt(pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_id_sf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_iso_sf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_pdf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_qcd_scale_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_id_sf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_reco_sf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_pdf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_qcd_scale_electron,2))

n_weighted_selected_data_mc_sf_syst_unc_muon = math.sqrt(pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_id_sf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_iso_sf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_pdf_muon,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_qcd_scale_muon,2))

n_weighted_selected_data_mc_sf_syst_unc_electron = math.sqrt(pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_id_sf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_reco_sf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_pdf_electron,2)+pow(n_weighted_selected_data_mc_sf_syst_unc_due_to_qcd_scale_electron,2))

xs =  n_signal/(n_weighted_selected_data_mc_sf*35.9*1000/n_weighted_run_over)

xs_electron =  n_signal_electron/(n_weighted_selected_data_mc_sf_electron*35.9*1000/n_weighted_run_over)

xs_muon =  n_signal_muon/(n_weighted_selected_data_mc_sf_muon*35.9*1000/n_weighted_run_over)

lumi_err =  n_signal/(n_weighted_selected_data_mc_sf*35.9*0.975*1000/n_weighted_run_over) - xs

lumi_err_electron =  n_signal_electron/(n_weighted_selected_data_mc_sf_electron*35.9*0.975*1000/n_weighted_run_over) - xs

lumi_err_muon =  n_signal_muon/(n_weighted_selected_data_mc_sf_muon*35.9*0.975*1000/n_weighted_run_over) - xs

stat_err = (n_signal+n_signal_stat_unc)/(n_weighted_selected_data_mc_sf*35.9*1000/n_weighted_run_over) - xs

stat_err_electron = (n_signal_electron+n_signal_stat_unc_electron)/(n_weighted_selected_data_mc_sf_electron*35.9*1000/n_weighted_run_over) - xs_electron

stat_err_muon = (n_signal_muon+n_signal_stat_unc_muon)/(n_weighted_selected_data_mc_sf_muon*35.9*1000/n_weighted_run_over) - xs_muon

syst_err = n_signal/((n_weighted_selected_data_mc_sf - n_weighted_selected_data_mc_sf_syst_unc)*35.9*1000/n_weighted_run_over) - xs

syst_err_muon = n_signal_muon/((n_weighted_selected_data_mc_sf_muon - n_weighted_selected_data_mc_sf_syst_unc_muon)*35.9*1000/n_weighted_run_over) - xs

syst_err_electron = n_signal_electron/((n_weighted_selected_data_mc_sf_electron - n_weighted_selected_data_mc_sf_syst_unc_electron)*35.9*1000/n_weighted_run_over) - xs

acc = n_weighted_selected_data_mc_sf/n_weighted_run_over

acc_electron = n_weighted_selected_data_mc_sf_electron/n_weighted_run_over

acc_muon = n_weighted_selected_data_mc_sf_muon/n_weighted_run_over

fractional_err_on_acc_due_to_pdf = (((n_weighted_selected_data_mc_sf + n_weighted_selected_data_mc_sf_syst_unc_due_to_pdf_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_pdf_muon)/n_weighted_run_over) - acc)/acc

fractional_err_on_acc_due_to_pdf_electron = (((n_weighted_selected_data_mc_sf_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_pdf_electron)/n_weighted_run_over) - acc_electron)/acc_electron

fractional_err_on_acc_due_to_pdf_muon = (((n_weighted_selected_data_mc_sf_muon + n_weighted_selected_data_mc_sf_syst_unc_due_to_pdf_muon)/n_weighted_run_over) - acc_muon)/acc_muon

fractional_err_on_acc_due_to_qcd_scale = (((n_weighted_selected_data_mc_sf + n_weighted_selected_data_mc_sf_syst_unc_due_to_qcd_scale_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_qcd_scale_muon)/n_weighted_run_over) - acc)/acc

fractional_err_on_acc_due_to_qcd_scale_electron = (((n_weighted_selected_data_mc_sf_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_qcd_scale_electron)/n_weighted_run_over) - acc_electron)/acc_electron

fractional_err_on_acc_due_to_qcd_scale_muon = (((n_weighted_selected_data_mc_sf_muon + n_weighted_selected_data_mc_sf_syst_unc_due_to_qcd_scale_muon)/n_weighted_run_over) - acc_muon)/acc_muon

fractional_err_on_acc_due_to_photon_id_sf = (((n_weighted_selected_data_mc_sf + n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_muon)/n_weighted_run_over) - acc)/acc

fractional_err_on_acc_due_to_photon_id_sf_electron = (((n_weighted_selected_data_mc_sf_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_electron)/n_weighted_run_over) - acc_electron)/acc_electron

fractional_err_on_acc_due_to_photon_id_sf_muon = (((n_weighted_selected_data_mc_sf_muon +n_weighted_selected_data_mc_sf_syst_unc_due_to_photon_id_sf_muon)/n_weighted_run_over) - acc_muon)/acc_muon

fractional_err_on_acc_due_to_electron_reco_sf = (((n_weighted_selected_data_mc_sf + n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_reco_sf_electron)/n_weighted_run_over) - acc)/acc

fractional_err_on_acc_due_to_electron_reco_sf_electron = (((n_weighted_selected_data_mc_sf_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_reco_sf_electron)/n_weighted_run_over) - acc_electron)/acc_electron

fractional_err_on_acc_due_to_electron_id_sf = (((n_weighted_selected_data_mc_sf + n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_id_sf_electron)/n_weighted_run_over) - acc)/acc

fractional_err_on_acc_due_to_electron_id_sf_electron = (((n_weighted_selected_data_mc_sf_electron + n_weighted_selected_data_mc_sf_syst_unc_due_to_electron_id_sf_electron)/n_weighted_run_over) - acc_electron)/acc_electron

fractional_err_on_acc_due_to_muon_id_sf = (((n_weighted_selected_data_mc_sf + n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_id_sf_muon)/n_weighted_run_over) - acc)/acc

fractional_err_on_acc_due_to_muon_id_sf_muon = (((n_weighted_selected_data_mc_sf_muon + n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_id_sf_muon)/n_weighted_run_over) - acc_muon)/acc_muon

fractional_err_on_acc_due_to_muon_iso_sf = (((n_weighted_selected_data_mc_sf + n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_iso_sf_muon)/n_weighted_run_over) - acc)/acc

fractional_err_on_acc_due_to_muon_iso_sf_muon = (((n_weighted_selected_data_mc_sf_muon + n_weighted_selected_data_mc_sf_syst_unc_due_to_muon_iso_sf_muon)/n_weighted_run_over) - acc_muon)/acc_muon

print "xs = " +str(xs) + " +/- " + str(stat_err) + " (stat) +/- " + str(syst_err) + " (syst) +/- " + str(lumi_err) + " (lumi)"

print "xs based on electron channel = " +str(xs_electron) + " +/- " + str(stat_err_electron) + " (stat) +/- " + str(syst_err_electron) + " (syst) +/- "  + str(lumi_err_electron) + " (lumi)"

print "xs based on muon channel = " +str(xs_muon) + " +/- "+ str(stat_err_muon) + " (stat) +/- " + str(syst_err_muon) + " (syst) +/- "  + str(lumi_err_muon) + " (lumi)" 

print "fractional_err_on_acc_due_to_pdf = " + str(fractional_err_on_acc_due_to_pdf)

print "fractional_err_on_acc_due_to_pdf_muon = " + str(fractional_err_on_acc_due_to_pdf_muon)

print "fractional_err_on_acc_due_to_pdf_electron = " + str(fractional_err_on_acc_due_to_pdf_electron)

print "fractional_err_on_acc_due_to_qcd_scale = " + str(fractional_err_on_acc_due_to_qcd_scale)

print "fractional_err_on_acc_due_to_qcd_scale_electron = " + str(fractional_err_on_acc_due_to_qcd_scale_electron)

print "fractional_err_on_acc_due_to_qcd_scale_muon = " + str(fractional_err_on_acc_due_to_qcd_scale_muon)

print "fractional_err_on_acc_due_to_photon_id_sf = "+ str(fractional_err_on_acc_due_to_photon_id_sf)

print "fractional_err_on_acc_due_to_photon_id_sf_electron = "+ str(fractional_err_on_acc_due_to_photon_id_sf_electron)

print "fractional_err_on_acc_due_to_photon_id_sf_muon = "+ str(fractional_err_on_acc_due_to_photon_id_sf_muon)

print "fractional_err_on_acc_due_to_electron_reco_sf = " + str(fractional_err_on_acc_due_to_electron_reco_sf)

print "fractional_err_on_acc_due_to_electron_reco_sf_electron = " + str(fractional_err_on_acc_due_to_electron_reco_sf_electron)

print "fractional_err_on_acc_due_to_electron_id_sf = " + str(fractional_err_on_acc_due_to_electron_id_sf)

print "fractional_err_on_acc_due_to_electron_id_sf_electron = " + str(fractional_err_on_acc_due_to_electron_id_sf_electron)

print "fractional_err_on_acc_due_to_muon_id_sf = " + str(fractional_err_on_acc_due_to_muon_id_sf)

print "fractional_err_on_acc_due_to_muon_id_sf_muon = " + str(fractional_err_on_acc_due_to_muon_id_sf_muon)

print "fractional_err_on_acc_due_to_muon_iso_sf = " + str(fractional_err_on_acc_due_to_muon_iso_sf)

print "fractional_err_on_acc_due_to_muon_iso_sf_muon = " + str(fractional_err_on_acc_due_to_muon_iso_sf_muon)
