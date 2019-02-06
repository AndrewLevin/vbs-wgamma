import ROOT

#/uscms_data/d3/qliphy/andrew/CMSSW_9_3_0/src/MATRIX_v1.0.2/run/ppexnea03_MATRIX/result/run_03/summary/result_summary.dat
matrix_lo_xs_eplus = 1.613*pow(10,4)
matrix_nlo_xs_eplus = 2.643*pow(10,4)
matrix_nnlo_xs_eplus = 2.992*pow(10,4)

#/uscms_data/d3/qliphy/andrew/CMSSW_9_3_0/src/MATRIX_v1.0.2/run/ppenexa03_MATRIX/result/run_03/summary/result_summary.dat
matrix_lo_xs_eminus = 1.366*pow(10,4)
matrix_nlo_xs_eminus = 2.336*pow(10,4)
matrix_nnlo_xs_eminus = 2.638*pow(10,4)

matrix_lo_xs=3*(matrix_lo_xs_eplus+matrix_lo_xs_eminus)
matrix_nlo_xs=3*(matrix_nlo_xs_eplus+matrix_nlo_xs_eminus)
matrix_nnlo_xs=3*(matrix_nnlo_xs_eplus+matrix_nnlo_xs_eminus)

print "matrix_lo_xs = " + str(matrix_lo_xs)
print "matrix_nlo_xs = " + str(matrix_nlo_xs)
print "matrix_nnlo_xs = " + str(matrix_nnlo_xs)

mg5amc_wgjets_filename = "/afs/cern.ch/work/a/amlevin/data/wg/2016/wgjets.root"

mg5amc_wgjets_file =  ROOT.TFile(mg5amc_wgjets_filename)

n_weighted_mg5amc_pass_lhe_selection = mg5amc_wgjets_file.Get("nWeightedEventsPassLHESelection").GetBinContent(1)
n_weighted_mg5amc_pass_lhe_and_gen_selection = mg5amc_wgjets_file.Get("nWeightedEventsPassLHEAndGenSelection").GetBinContent(1)

lhe_to_gen_efficiency = n_weighted_mg5amc_pass_lhe_and_gen_selection/n_weighted_mg5amc_pass_lhe_selection

print "lhe_to_gen_efficiency = "+str(lhe_to_gen_efficiency)

fiducial_lo_xs = matrix_lo_xs*lhe_to_gen_efficiency 
fiducial_nlo_xs = matrix_nlo_xs*lhe_to_gen_efficiency
fiducial_nnlo_xs = matrix_nnlo_xs*lhe_to_gen_efficiency

print "fiducial_lo_xs = "+str(fiducial_lo_xs/1000.) + " pb"
print "fiducial_nlo_xs = "+str(fiducial_nlo_xs/1000.)+ " pb"
print "fiducial_nnlo_xs = "+str(fiducial_nnlo_xs/1000.)+ " pb"

matrix_nnlo_xs_eplus_scale_up=2.7 #in percent  
matrix_nnlo_xs_eplus_scale_down=2.6 #in percent

matrix_nnlo_xs_eminus_scale_up = 2.6 #in percent
matrix_nnlo_xs_eminus_scale_down = 2.6 #in percent

matrix_nnlo_xs_eplus_rcut_extrapolation_unc = 2.0*pow(10,2) #in fb
matrix_nnlo_xs_eminus_rcut_extrapolation_unc = 1.7*pow(10,2) #in fb

from math import sqrt

matrix_nnlo_xs_err_due_to_rcut_extrapolation = 3*sqrt(pow(matrix_nnlo_xs_eplus_rcut_extrapolation_unc,2) + pow(matrix_nnlo_xs_eminus_rcut_extrapolation_unc,2) )

matrix_nnlo_xs_err_due_to_scale_up = 3*sqrt(pow(matrix_nnlo_xs_eplus*matrix_nnlo_xs_eplus_scale_up/100,2) + pow(matrix_nnlo_xs_eminus*matrix_nnlo_xs_eminus_scale_up/100,2))

matrix_nnlo_xs_err_due_to_scale_down = 3*sqrt(pow(matrix_nnlo_xs_eplus*matrix_nnlo_xs_eplus_scale_down/100,2) + pow(matrix_nnlo_xs_eminus*matrix_nnlo_xs_eminus_scale_down/100,2) )

print "xs: \\sigma = %.2f \pm %.2f \\text{ (rcut/stat)} \pm ^{%.2f}_{%.2f} \\text{ (scale) pb}"%(matrix_nnlo_xs/1000.,matrix_nnlo_xs_err_due_to_rcut_extrapolation/1000,matrix_nnlo_xs_err_due_to_scale_up/1000.,matrix_nnlo_xs_err_due_to_scale_down/1000.)

pdf_unc_from_mg5aMC_sample = 1.51454829623 #in percent

fiducial_nnlo_xs_err_due_to_scale_up = matrix_nnlo_xs_err_due_to_scale_up*lhe_to_gen_efficiency

fiducial_nnlo_xs_err_due_to_scale_down = matrix_nnlo_xs_err_due_to_scale_down*lhe_to_gen_efficiency

print "fiducial_nnlo_xs_err_due_to_scale_up = " + str(fiducial_nnlo_xs_err_due_to_scale_up)

print "fiducial_nnlo_xs_err_due_to_scale_down = " + str(fiducial_nnlo_xs_err_due_to_scale_down)

fiducial_nnlo_xs_err_due_to_rcut_extrapolation = matrix_nnlo_xs_err_due_to_rcut_extrapolation*lhe_to_gen_efficiency

print "fiducial_nnlo_xs_err_due_to_rcut_extrapolation = "+ str(fiducial_nnlo_xs_err_due_to_rcut_extrapolation)

print "xs: \\sigma = %.2f \pm %.2f \\text{ (rcut)} \pm ^{%.2f}_{%.2f} \\text{ (scale)} \pm %.2f \\text{ (PDF) pb}"%(fiducial_nnlo_xs/1000.,fiducial_nnlo_xs_err_due_to_rcut_extrapolation/1000,fiducial_nnlo_xs_err_due_to_scale_up/1000.,fiducial_nnlo_xs_err_due_to_scale_down/1000.,pdf_unc_from_mg5aMC_sample*fiducial_nnlo_xs/100./1000.)
