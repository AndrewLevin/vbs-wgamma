import ROOT

#/afs/cern.ch/work/a/amlevin/matrix_generation/CMSSW_9_3_0/src/MATRIX_v1.0.2/run/ppexnea03_MATRIX/result/run_200
matrix_lo_xs_eplus = 1.614*pow(10,4)
matrix_nlo_xs_eplus = 2.650*pow(10,4)
matrix_nnlo_xs_eplus = 3.030*pow(10,4)

#/afs/cern.ch/work/a/amlevin/matrix_generation/CMSSW_9_3_0/src/MATRIX_v1.0.2/run/ppenexa03_MATRIX/result/run_200
matrix_lo_xs_eminus = 1.368*pow(10,4)
matrix_nlo_xs_eminus = 2.340*pow(10,4)
matrix_nnlo_xs_eminus = 2.814*pow(10,4)

matrix_lo_xs=3*(matrix_lo_xs_eplus+matrix_lo_xs_eminus)
matrix_nlo_xs=3*(matrix_nlo_xs_eplus+matrix_nlo_xs_eminus)
matrix_nnlo_xs=3*(matrix_nnlo_xs_eplus+matrix_nnlo_xs_eminus)

mg5amc_wgjets_filename = "/afs/cern.ch/work/a/amlevin/data/wg/2016/wgjets.root"

mg5amc_wgjets_file =  ROOT.TFile(mg5amc_wgjets_filename)

n_weighted_mg5amc_pass_lhe_selection = mg5amc_wgjets_file.Get("nWeightedEventsPassLHESelection").GetBinContent(1)
n_weighted_mg5amc_pass_lhe_and_gen_selection = mg5amc_wgjets_file.Get("nWeightedEventsPassLHEAndGenSelection").GetBinContent(1)

lhe_to_gen_efficiency = n_weighted_mg5amc_pass_gen_selection/n_weighted_mg5amc_pass_lhe_and_gen_selection

print "lhe_to_gen_efficiency = "+str(lhe_to_gen_efficiency)

fiducial_lo_xs = matrix_lo_xs*lhe_to_gen_efficiency 
fiducial_nlo_xs = matrix_nlo_xs*lhe_to_gen_efficiency
fiducial_nnlo_xs = matrix_nnlo_xs*lhe_to_gen_efficiency

print "fiducial_lo_xs = "+str(fiducial_lo_xs/1000.) + " pb"
print "fiducial_nlo_xs = "+str(fiducial_nlo_xs/1000.)+ " pb"
print "fiducial_nnlo_xs = "+str(fiducial_nnlo_xs/1000.)+ " pb"
