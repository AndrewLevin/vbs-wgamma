#!/usr/bin/env python
from ROOT import *
import sys
import time

gb = TGraph() #nnlo over nlo factors as a function of photon pt for the barrel
ge = TGraph() #nnlo over nlo factors as a function of photon pt for the endcap

gb.SetPoint(0,27.5,0.1465633350156374)
gb.SetPoint(1,35.0,0.10659503275136101)
gb.SetPoint(2,45.0,0.08366693471349625)
gb.SetPoint(3,60.0,0.06604377238571527)
gb.SetPoint(4,85.0,0.0548938614256607)
gb.SetPoint(5,117.5,0.045549075729087965)
gb.SetPoint(6,267.5,0.0287425297394385)

gb.SetMarkerStyle(21)

gb.SetMinimum(1)

gb.GetXaxis().SetTitle("photon pt (GeV)")
gb.GetYaxis().SetTitle("fake photon extrapolation weight ")

gb.GetXaxis().SetTitleSize(0.055)
gb.GetYaxis().SetTitleSize(0.055)

gb.GetXaxis().SetTitleOffset(0.75)
gb.GetYaxis().SetTitleOffset(0.75)

ge.SetPoint(0,27.5,0.19848704149567134)
ge.SetPoint(1,35.0,0.15927761402175133)
ge.SetPoint(2,45.0,0.1259625150980935)
ge.SetPoint(3,60.0,0.1024070694786739)
ge.SetPoint(4,85.0,0.07696444018690847)
ge.SetPoint(5,117.5,0.06278537807297754)
ge.SetPoint(6,267.5,0.002814088634222858)

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

ge.Draw("ALP")

raw_input("hit a key")
