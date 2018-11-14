import ROOT
import math

f=ROOT.TFile.Open("/eos/user/a/amlevin/tmp/Merged15.wgjets.root")
t=f.Get("Events")

nominal_xs = 178.6

n_total = 0
n_weighted = ROOT.TH1F("n_weighted","n_weighted",1,0,1)
n_weighted.Sumw2()
n_weighted_pdf = []
n_weighted_scale = []

for i in range(0,102):
    n_weighted_pdf.append(ROOT.TH1F("n_weighted_pdf_variation"+str(i),"n_weighted_pdf_variation"+str(i),1,0,1))
    n_weighted_pdf[i].Sumw2()

for i in range(0,8):
    n_weighted_scale.append(ROOT.TH1F("n_weighted_scale_variation"+str(i),"n_weighted_scale_variation"+str(i),1,0,1))
    n_weighted_scale[i].Sumw2()

print "t.GetEntries() = "+str(t.GetEntries())

for i in range(0,t.GetEntries()):
    if n_total % 100000 == 0:
        print "n_total = "+str(n_total)
    n_total+=1
    t.GetEntry(i)
    if t.Generator_weight > 0:
        n_weighted.Fill(0.5)
    else:    
        n_weighted.Fill(0.5,-1)

    for j in range(0,8):
        if t.Generator_weight > 0:
            n_weighted_scale[j].Fill(0.5,t.LHEScaleWeight[j]*2)
        else:    
            n_weighted_scale[j].Fill(0.5,-t.LHEScaleWeight[j]*2)
    for j in range(0,102):
        if t.Generator_weight > 0:
            n_weighted_pdf[j].Fill(0.5,t.LHEPdfWeight[j+1])
        else:    
            n_weighted_pdf[j].Fill(0.5,-t.LHEPdfWeight[j+1])

pdf_mean = 0
pdf_stddev = 0
scale_mean = 0
scale_stddev = 0

print "n_weighted.GetBinContent(1) = "+str(n_weighted.GetBinContent(1))
print "n_weighted.GetBinError(1) = " + str(n_weighted.GetBinError(1))

for i in range(0,102):
    #print "n_weighted_pdf[i].GetBinContent(1) = " + str(n_weighted_pdf[i].GetBinContent(1))
    #print "n_weighted_pdf[i].GetBinError(1) = " + str(n_weighted_pdf[i].GetBinError(1))

    print "pdf variation "+str(i)+" xs: "+str(nominal_xs*n_weighted_pdf[i].GetBinContent(1)/n_weighted.GetBinContent(1))
    pdf_mean+=n_weighted_pdf[i].GetBinContent(1)

pdf_mean += n_weighted.GetBinContent(1)

pdf_mean /= 103

for i in range(0,102):
    pdf_stddev+= pow(n_weighted_pdf[i].GetBinContent(1)-pdf_mean,2)

pdf_stddev += pow(n_weighted.GetBinContent(1)-pdf_mean,2)

pdf_stddev /= (103-1)

pdf_stddev = math.sqrt(pdf_stddev)

for i in range(0,8):
    if i == 6 or i == 4:
        continue

    scale_mean += n_weighted_scale[i].GetBinContent(1)

    #print "n_weighted_scale[i].GetBinContent(1) = " + str(n_weighted_scale[i].GetBinContent(1))
    #print "n_weighted_scale[i].GetBinError(1) = " + str(n_weighted_scale[i].GetBinError(1))

    print "scale variation "+str(i)+" xs: "+ str(nominal_xs*n_weighted_scale[i].GetBinContent(1)/n_weighted.GetBinContent(1))

scale_mean += n_weighted.GetBinContent(1)

scale_mean /= 7

for i in range(0,8):
    if i == 6 or i == 4:
        continue

    scale_stddev += pow(n_weighted_scale[i].GetBinContent(1)-scale_mean,2)

scale_stddev += pow(n_weighted.GetBinContent(1)-scale_mean,2)

scale_stddev /= (7-1)

scale_stddev = math.sqrt(scale_stddev)

print "xs = "+str(n_weighted.GetBinContent(1) * nominal_xs / n_weighted.GetBinContent(1))

print "pdf unc = "+ str(pdf_stddev * nominal_xs / n_weighted.GetBinContent(1))

print "scale unc = "+ str(scale_stddev * nominal_xs / n_weighted.GetBinContent(1))
