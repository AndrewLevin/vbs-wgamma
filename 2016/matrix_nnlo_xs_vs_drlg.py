#/afs/cern.ch/work/a/amlevin/matrix_generation/CMSSW_9_3_0/src/MATRIX_v1.0.2/run/ppenexa03_MATRIX//result/run_200/summary/result_summary.dat
#/afs/cern.ch/work/a/amlevin/matrix_generation/CMSSW_9_3_0/src/MATRIX_v1.0.2/run/ppenexa03_MATRIX//result/run_201/summary/result_summary.dat
#/afs/cern.ch/work/a/amlevin/matrix_generation/CMSSW_9_3_0/src/MATRIX_v1.0.2/run/ppenexa03_MATRIX//result/run_202/summary/result_summary.dat
#/afs/cern.ch/work/a/amlevin/matrix_generation/CMSSW_9_3_0/src/MATRIX_v1.0.2/run/ppenexa03_MATRIX//result/run_203/summary/result_summary.dat
#/afs/cern.ch/work/a/amlevin/matrix_generation/CMSSW_9_3_0/src/MATRIX_v1.0.2/run/ppenexa03_MATRIX//result/run_204/summary/result_summary.dat
#/afs/cern.ch/work/a/amlevin/matrix_generation/CMSSW_9_3_0/src/MATRIX_v1.0.2/run/ppenexa03_MATRIX//result/run_205/summary/result_summary.dat
#/afs/cern.ch/work/a/amlevin/matrix_generation/CMSSW_9_3_0/src/MATRIX_v1.0.2/run/ppenexa03_MATRIX//result/run_206/summary/result_summary.dat

#/afs/cern.ch/work/a/amlevin/matrix_generation/CMSSW_9_3_0/src/MATRIX_v1.0.2/run/ppexnea03_MATRIX//result/run_200/summary/result_summary.dat
#/afs/cern.ch/work/a/amlevin/matrix_generation/CMSSW_9_3_0/src/MATRIX_v1.0.2/run/ppexnea03_MATRIX//result/run_201/summary/result_summary.dat
#/afs/cern.ch/work/a/amlevin/matrix_generation/CMSSW_9_3_0/src/MATRIX_v1.0.2/run/ppexnea03_MATRIX//result/run_202/summary/result_summary.dat
#/afs/cern.ch/work/a/amlevin/matrix_generation/CMSSW_9_3_0/src/MATRIX_v1.0.2/run/ppexnea03_MATRIX//result/run_203/summary/result_summary.dat
#/afs/cern.ch/work/a/amlevin/matrix_generation/CMSSW_9_3_0/src/MATRIX_v1.0.2/run/ppexnea03_MATRIX//result/run_204/summary/result_summary.dat
#/afs/cern.ch/work/a/amlevin/matrix_generation/CMSSW_9_3_0/src/MATRIX_v1.0.2/run/ppexnea03_MATRIX//result/run_205/summary/result_summary.dat
#/afs/cern.ch/work/a/amlevin/matrix_generation/CMSSW_9_3_0/src/MATRIX_v1.0.2/run/ppexnea03_MATRIX//result/run_206/summary/result_summary.dat

from ROOT import *
import sys
import time

g_wplus = TGraphErrors()
g_wpluserror = TGraphErrors()
g_wminus = TGraphErrors()
g_wminuserror = TGraphErrors()

g_wplus.SetPoint(0,0.1,3.030e+04)
g_wplus.SetPoint(1,0.2,2.466e+04)
g_wplus.SetPoint(2,0.3,2.103e+04)
g_wplus.SetPoint(3,0.4,2.190e+04)
g_wplus.SetPoint(4,0.5,1.886e+04)
g_wplus.SetPoint(5,0.6,1.784e+04)
g_wplus.SetPoint(6,0.7,1.882e+04)

g_wplus.SetPointError(0,0,2.2e+03)
g_wplus.SetPointError(1,0,1.4e+03)
g_wplus.SetPointError(2,0,7.3e+02)
g_wplus.SetPointError(3,0,1.6e+03)
g_wplus.SetPointError(4,0,4.1e+02)
g_wplus.SetPointError(5,0,1.2e+03)
g_wplus.SetPointError(6,0,2.3e+03)

g_wminus.SetPoint(0,0.1,2.814e+04)
g_wminus.SetPoint(1,0.2,2.273e+04)
g_wminus.SetPoint(2,0.3,2.156e+04)
g_wminus.SetPoint(3,0.4,1.968e+04)
g_wminus.SetPoint(4,0.5,1.823e+04)
g_wminus.SetPoint(5,0.6,1.687e+04)
g_wminus.SetPoint(6,0.7,1.552e+04)

g_wminus.SetPointError(0,0,1e+03)
g_wminus.SetPointError(1,0,1.4e+03)
g_wminus.SetPointError(2,0,8.9e+02)
g_wminus.SetPointError(3,0,8.6e+02)
g_wminus.SetPointError(4,0,7.7e+02)
g_wminus.SetPointError(5,0,5.5e+02)
g_wminus.SetPointError(6,0,1e+03)

g_wplus.SetLineWidth(3)
g_wminus.SetLineWidth(3)

g_wplus.GetYaxis().SetTitleOffset(1.2)
g_wplus.GetYaxis().SetTitle("cross-section (pb)")

leg=TLegend(0.2,0.6,0.4,0.8)

leg.AddEntry(g_wplus,"W^{+}\gamma","l")

#g_wplus.SetMinimum(0)
g_wminus.SetMinimum(0)

#g_wplus.Draw()
g_wminus.Draw()
#leg.Draw("same")

gPad.SetLeftMargin(20)

gPad.Update()
gPad.ForceUpdate()

gPad.SaveAs("/eos/user/a/amlevin/www/tmp/delete_this.png")
