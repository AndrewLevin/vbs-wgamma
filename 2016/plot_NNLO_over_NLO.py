#!/usr/bin/env python
from ROOT import *
import sys
import time

gb = TGraphErrors() #nnlo over nlo factors as a function of photon pt for the barrel
ge = TGraphErrors() #nnlo over nlo factors as a function of photon pt for the endcap

gb.SetPoint(0,15.0,1.147377962)
gb.SetPointError(0,0,0.004841147)

gb.SetPoint(1,20.0,1.178472286)
gb.SetPointError(1,0,0.004394965)

gb.SetPoint(2,25.0,1.189477952)
gb.SetPointError(2,0,0.004111348)

gb.SetPoint(3,30.0,1.201940155)
gb.SetPointError(3,0,0.003941842)

gb.SetPoint(4,35.0,1.207208243)
gb.SetPointError(4,0,0.003888700)

gb.SetPoint(5,40.0,1.223341402)
gb.SetPointError(5,0,0.003948126)

gb.SetPoint(6,45.0,1.236597991)
gb.SetPointError(6,0,0.002482772)

gb.SetPoint(7,60.0,1.251381290)
gb.SetPointError(7,0,0.002571184)

gb.SetPoint(8,90.0,1.276937808)
gb.SetPointError(8,0,0.003196969)

gb.SetPoint(9,120.0,1.313879553)
gb.SetPointError(9,0,0.001807062)

#gb.SetPoint(10,500.0,1.342758655)
#gb.SetPoint(11,6500.00,1.342758655)

#gb.SetMarkerStyle(3)
#gb.SetMarkerSize(2)

#gb.SetLineWidth(0)

gb.SetMarkerStyle(21)

gb.SetMinimum(1)

gb.GetXaxis().SetTitle("photon pt (GeV)")
gb.GetYaxis().SetTitle("NNLO/NLO")

gb.GetXaxis().SetTitleSize(0.055)
gb.GetYaxis().SetTitleSize(0.055)

gb.GetXaxis().SetTitleOffset(0.75)
gb.GetYaxis().SetTitleOffset(0.75)

ge.SetPoint(0,15.0,1.162640195)
ge.SetPointError(0,0,0.004771453)

ge.SetPoint(1,20.0,1.177382848 )
ge.SetPointError(1,0,0.004518002 )

ge.SetPoint(2,25.0,1.184751650)
ge.SetPointError(2,0,0.003997075)

ge.SetPoint(3,30.0,1.199851869)
ge.SetPointError(3,0,0.004064817 )

ge.SetPoint(4,35.0,1.211113026)
ge.SetPointError(4,0,0.003928583)

ge.SetPoint(5,40.0,1.224040300)
ge.SetPointError(5,0,0.004709437)

ge.SetPoint(6,45.0,1.216979438)
ge.SetPointError(6,0,0.003330156)

ge.SetPoint(7,60.0,1.238354632 )
ge.SetPointError(7,0,0.003215218 )

ge.SetPoint(8,90.0,1.272419215)
ge.SetPointError(8,0,0.003054057)

ge.SetPoint(9,120.0,1.305852580 )
ge.SetPointError(9,0,0.002204904)

#ge.SetPoint(10,500.0,1.296100451,0.012903564)
#ge.SetPoint(11,6500.00,1.296100451,0.012903564)

#ge.SetMarkerStyle(3)
#ge.SetMarkerSize(2)

ge.SetMarkerStyle(21)

ge.SetMinimum(1)

ge.GetXaxis().SetTitle("photon pt (GeV)")
ge.GetYaxis().SetTitle("NNLO/NLO")

#ge.GetXaxis().CenterTitle()
#ge.GetYaxis().CenterTitle()

ge.GetXaxis().SetTitleSize(0.055)
ge.GetYaxis().SetTitleSize(0.055)

ge.GetXaxis().SetTitleOffset(0.75)
ge.GetYaxis().SetTitleOffset(0.75)

gb.Draw("ALP")

raw_input("hit a key")
