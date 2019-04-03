import ROOT
import math


mg5amc_nlo_xs =  178.6

mg5amc_wgjets_filename = "/afs/cern.ch/work/a/amlevin/data/wg/2016/wgjets.root"

mg5amc_wgjets_file =  ROOT.TFile(mg5amc_wgjets_filename)

n_weighted_mg5amc_pass_lhe_selection = mg5amc_wgjets_file.Get("nWeightedEventsPassLHESelection").GetBinContent(1)
n_weighted_mg5amc_pass_gen_selection = mg5amc_wgjets_file.Get("nWeightedEventsPassGenSelection").GetBinContent(1)
n_weighted_mg5amc = mg5amc_wgjets_file.Get("nEventsGenWeighted").GetBinContent(1)
n_weighted_mg5amc_pass_lhe_and_gen_selection = mg5amc_wgjets_file.Get("nWeightedEventsPassLHEAndGenSelection").GetBinContent(1)

powheg_plus_nlo_xs =  33420.0
powheg_minus_nlo_xs =  24780.0

print "powheg_nlo_xs = " + str(powheg_plus_nlo_xs + powheg_minus_nlo_xs)

print "m5amc_nlo_xs = " + str(mg5amc_nlo_xs)

powheg_plus_wgjets_filename = "/afs/cern.ch/work/a/amlevin/data/wg/2016/powhegwplusg.root"
powheg_minus_wgjets_filename = "/afs/cern.ch/work/a/amlevin/data/wg/2016/powhegwminusg.root"

powheg_plus_wgjets_file =  ROOT.TFile(powheg_plus_wgjets_filename)
powheg_minus_wgjets_file =  ROOT.TFile(powheg_minus_wgjets_filename)

n_weighted_powheg_plus_pass_lhe_selection = powheg_plus_wgjets_file.Get("nWeightedEventsPassLHESelection").GetBinContent(1)
n_weighted_powheg_minus_pass_lhe_selection = powheg_minus_wgjets_file.Get("nWeightedEventsPassLHESelection").GetBinContent(1)

n_weighted_powheg_plus = powheg_plus_wgjets_file.Get("nEventsGenWeighted").GetBinContent(1)
n_weighted_powheg_minus = powheg_minus_wgjets_file.Get("nEventsGenWeighted").GetBinContent(1)

n_weighted_powheg_plus_pass_lhe_and_gen_selection = powheg_plus_wgjets_file.Get("nWeightedEventsPassLHEAndGenSelection").GetBinContent(1)
n_weighted_powheg_minus_pass_lhe_and_gen_selection = powheg_minus_wgjets_file.Get("nWeightedEventsPassLHEAndGenSelection").GetBinContent(1)

n_weighted_powheg_plus_pass_gen_selection = powheg_plus_wgjets_file.Get("nWeightedEventsPassGenSelection").GetBinContent(1)
n_weighted_powheg_minus_pass_gen_selection = powheg_minus_wgjets_file.Get("nWeightedEventsPassGenSelection").GetBinContent(1)

mg5amc_nlo_fiducial_xs =  mg5amc_nlo_xs*mg5amc_wgjets_file.Get("nWeightedEventsPassGenSelection").GetBinContent(1)/mg5amc_wgjets_file.Get("nEventsGenWeighted").GetBinContent(1)

powheg_nlo_fiducial_xs = powheg_plus_nlo_xs*n_weighted_powheg_plus_pass_gen_selection/n_weighted_powheg_plus + powheg_minus_nlo_xs*n_weighted_powheg_minus_pass_gen_selection/n_weighted_powheg_minus

print "mg5amc_nlo_fiducial_xs = "+str(mg5amc_nlo_fiducial_xs)
print "powheg_nlo_fiducial_xs = "+str(powheg_nlo_fiducial_xs)

mg5amc_nlo_fiducial_xs_qcd_scale_unc = -1
powheg_nlo_fiducial_xs_qcd_scale_unc = -1

for i in range(0,8):

    if i == 2 or i == 5:
        continue

    mg5amc_nlo_fiducial_xs_qcd_scale_i = mg5amc_nlo_xs*2*mg5amc_wgjets_file.Get("nWeightedEventsPassGenSelection_QCDScaleWeight"+str(i)).GetBinContent(1)/mg5amc_wgjets_file.Get("nEventsGenWeighted").GetBinContent(1)

    powheg_nlo_fiducial_xs_qcd_scale_i = powheg_plus_nlo_xs*3*powheg_plus_wgjets_file.Get("nWeightedEventsPassGenSelection_QCDScaleWeight"+str(i)).GetBinContent(1)/powheg_plus_wgjets_file.Get("nEventsGenWeighted").GetBinContent(1)+powheg_minus_nlo_xs*3*powheg_minus_wgjets_file.Get("nWeightedEventsPassGenSelection_QCDScaleWeight"+str(i)).GetBinContent(1)/powheg_minus_wgjets_file.Get("nEventsGenWeighted").GetBinContent(1) 

    if abs(mg5amc_nlo_fiducial_xs_qcd_scale_i - mg5amc_nlo_fiducial_xs) > mg5amc_nlo_fiducial_xs_qcd_scale_unc:
        mg5amc_nlo_fiducial_xs_qcd_scale_unc = abs(mg5amc_nlo_fiducial_xs_qcd_scale_i - mg5amc_nlo_fiducial_xs)

    if abs(powheg_nlo_fiducial_xs_qcd_scale_i - powheg_nlo_fiducial_xs) > powheg_nlo_fiducial_xs_qcd_scale_unc:
        powheg_nlo_fiducial_xs_qcd_scale_unc = abs(powheg_nlo_fiducial_xs_qcd_scale_i - powheg_nlo_fiducial_xs)


assert(mg5amc_nlo_fiducial_xs_qcd_scale_unc != -1)
assert(powheg_nlo_fiducial_xs_qcd_scale_unc != -1)

print "powheg_nlo_fiducial_xs_qcd_scale_unc = "+str(powheg_nlo_fiducial_xs_qcd_scale_unc)
print "mg5amc_nlo_fiducial_xs_qcd_scale_unc = "+str(mg5amc_nlo_fiducial_xs_qcd_scale_unc)

mg5amc_nlo_fiducial_xs_mean_pdf=0
powheg_nlo_fiducial_xs_mean_pdf=0

for i in range(1,102):
    mg5amc_nlo_fiducial_xs_mean_pdf+=mg5amc_nlo_xs*mg5amc_wgjets_file.Get("nWeightedEventsPassGenSelection_PDFWeight"+str(i)).GetBinContent(1)/mg5amc_wgjets_file.Get("nEventsGenWeighted").GetBinContent(1)
    powheg_nlo_fiducial_xs_mean_pdf+=powheg_plus_nlo_xs*3*powheg_plus_wgjets_file.Get("nWeightedEventsPassGenSelection_PDFWeight"+str(i)).GetBinContent(1)/powheg_plus_wgjets_file.Get("nEventsGenWeighted").GetBinContent(1)+powheg_minus_nlo_xs*3*powheg_minus_wgjets_file.Get("nWeightedEventsPassGenSelection_PDFWeight"+str(i)).GetBinContent(1)/powheg_minus_wgjets_file.Get("nEventsGenWeighted").GetBinContent(1)

mg5amc_nlo_fiducial_xs_mean_pdf=mg5amc_nlo_fiducial_xs_mean_pdf/101
powheg_nlo_fiducial_xs_mean_pdf=powheg_nlo_fiducial_xs_mean_pdf/101

mg5amc_nlo_fiducial_xs_stddev_pdf=0
powheg_nlo_fiducial_xs_stddev_pdf=0

for i in range(1,102):
    mg5amc_nlo_fiducial_xs_stddev_pdf += pow(mg5amc_nlo_xs*mg5amc_wgjets_file.Get("nWeightedEventsPassGenSelection_PDFWeight"+str(i)).GetBinContent(1)/mg5amc_wgjets_file.Get("nEventsGenWeighted").GetBinContent(1) - mg5amc_nlo_fiducial_xs_mean_pdf,2)
    powheg_nlo_fiducial_xs_stddev_pdf += pow(powheg_plus_nlo_xs*3*powheg_plus_wgjets_file.Get("nWeightedEventsPassGenSelection_PDFWeight"+str(i)).GetBinContent(1)/powheg_plus_wgjets_file.Get("nEventsGenWeighted").GetBinContent(1)+powheg_minus_nlo_xs*3*powheg_minus_wgjets_file.Get("nWeightedEventsPassGenSelection_PDFWeight"+str(i)).GetBinContent(1)/powheg_minus_wgjets_file.Get("nEventsGenWeighted").GetBinContent(1) - powheg_nlo_fiducial_xs_mean_pdf,2)

mg5amc_nlo_fiducial_xs_stddev_pdf = math.sqrt(mg5amc_nlo_fiducial_xs_stddev_pdf/(101-1))
powheg_nlo_fiducial_xs_stddev_pdf = math.sqrt(powheg_nlo_fiducial_xs_stddev_pdf/(101-1))

print "mg5amc_nlo_fiducial_xs_stddev_pdf = "+str(mg5amc_nlo_fiducial_xs_stddev_pdf)
print "powheg_nlo_fiducial_xs_stddev_pdf = "+str(powheg_nlo_fiducial_xs_stddev_pdf)

print "powheg nlo fiducial xs: \\sigma = %.2f \pm %.2f \\text{ (scale) pb}"%(powheg_nlo_fiducial_xs,powheg_nlo_fiducial_xs_qcd_scale_unc)
print "mg5amc nlo fiducial xs: \\sigma = %.2f \pm %.2f \\text{ (scale) pb}"%(mg5amc_nlo_fiducial_xs,mg5amc_nlo_fiducial_xs_qcd_scale_unc)

