from ROOT import *

import style

style.GoodStyle().cd()

gROOT.cd()

c = TCanvas("c", "c",5,50,500,500);

sieie_histogram_file = TFile.Open("delete_this.root")

sieie_hist = sieie_histogram_file.Get("sieie_10")

sieie_hist.SetTitle("")

sieie_hist.GetXaxis().SetNdivisions(505)
sieie_hist.GetYaxis().SetNdivisions(505)

sieie_hist.Draw()

c.SaveAs("/eos/user/a/amlevin/www/tmp/delete_this.png")
