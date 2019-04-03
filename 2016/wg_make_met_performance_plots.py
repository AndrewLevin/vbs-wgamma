import ROOT

import style

style.GoodStyle().cd()

xoffsetstart = 0.0;
yoffsetstart = 0.0;
xoffset = 0.20;
yoffset = 0.05;

xpositions = [0.53,0.53,0.53,0.53]
ypositions = [0,1,2,3]

def set_axis_fonts(thstack, coordinate, title):

    if coordinate == "x":
        axis = thstack.GetXaxis();
    elif coordinate == "y":
        axis = thstack.GetYaxis();
    else:
        assert(0)
    
    axis.SetLabelFont  (   42)
    axis.SetLabelOffset(0.015)
    axis.SetLabelSize  (0.050)
    axis.SetNdivisions (  505)
    axis.SetTitleFont  (   42)
    axis.SetTitleOffset(  1.5)
    axis.SetTitleSize  (0.050)
    if (coordinate == "y"):
        axis.SetTitleOffset(1.6)
    axis.SetTitle(title)    

def draw_legend(x1,y1,hist,label,options):

    legend = ROOT.TLegend(x1+xoffsetstart,y1+yoffsetstart,x1+xoffsetstart + xoffset,y1+yoffsetstart + yoffset)

    legend.SetBorderSize(     0)
    legend.SetFillColor (     0)
    legend.SetTextAlign (    12)
    legend.SetTextFont  (    42)
    legend.SetTextSize  ( 0.040)

    legend.AddEntry(hist,label,options)

    legend.Draw("same")

    #otherwise the legend goes out of scope and is deleted once the function finishes
    hist.label = legend


f = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/wg/2016/zglowmlljets.root")
t = f.Get("Events")

h_npu = ROOT.TH1F("h_npu","",100,0,100)
h_npu_puppimet = ROOT.TH1F("h_npu_puppimet","",100,0,100)
h_npu_met = ROOT.TH1F("h_npu_met","",100,0,100)

t.Draw("npu >> h_npu","npu < 100")
t.Draw("npu >> h_npu_puppimet","npu < 100 && puppimet > 60 ")
t.Draw("npu >> h_npu_met","npu < 100 && met > 70")

h_npu.Scale(1/h_npu.Integral())
h_npu_puppimet.Scale(1/h_npu_puppimet.Integral())
h_npu_met.Scale(1/h_npu_met.Integral())

h_npu.SetLineColor(ROOT.kBlack)
h_npu_puppimet.SetLineColor(ROOT.kBlue)
h_npu_met.SetLineColor(ROOT.kRed)

set_axis_fonts(h_npu,"x","true number of interactions")

c = ROOT.TCanvas("c1", "c1",5,50,500,500)

h_npu.Draw()
h_npu_puppimet.Draw("same")
h_npu_met.Draw("same")

j=0
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,h_npu,"no MET cut","l")
j=1
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,h_npu_met,"MET > 70 GeV","l")
j=2
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,h_npu_puppimet,"PuppiMET > 60 GeV","l")

c.SaveAs("/eos/user/a/amlevin/www/tmp/delete_this.png")
