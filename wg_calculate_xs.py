import ROOT

mg5amc_nlo_xs = 178.6

mg5amc_wgjets_filename = "/afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019/wgjets.root"

mg5amc_wgjets_file = ROOT.TFile(mg5amc_wgjets_filename)

n_weighted_mg5amc_pass_fid_selection = mg5amc_wgjets_file.Get("nEventsGenWeighted_PassFidSelection").GetBinContent(1)

n_weighted_mg5amc = mg5amc_wgjets_file.Get("nEventsGenWeighted").GetBinContent(1)

mg5amc_nlo_fiducial_xs = mg5amc_nlo_xs*n_weighted_mg5amc_pass_fid_selection/n_weighted_mg5amc

rexp = 1  
rexpdown = 0.044618
rexpup = 0.0444708

rexpmuon = 1  
rexpmuondown = 0.0478512
rexpmuonup = 0.0476602 

rexpelectron = 1  
rexpelectrondown = 0.0661628
rexpelectronup = 0.0724796

print "xs = " + str(mg5amc_nlo_fiducial_xs * rexp) + " + " + str(mg5amc_nlo_fiducial_xs * rexpup) + " - " + str(mg5amc_nlo_fiducial_xs * rexpdown)

print "xs based on muon channel = " + str(mg5amc_nlo_fiducial_xs * rexpmuon) + " + " + str(mg5amc_nlo_fiducial_xs * rexpmuonup) + " - " + str(mg5amc_nlo_fiducial_xs * rexpmuondown)

print "xs based on electron channel = " + str(mg5amc_nlo_fiducial_xs * rexpelectron) + " + " + str(mg5amc_nlo_fiducial_xs * rexpelectronup) + " - " + str(mg5amc_nlo_fiducial_xs * rexpelectrondown)
