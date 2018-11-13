import ROOT

f=ROOT.TFile.Open("/eos/user/a/amlevin/tmp/Merged10.wgjets.root")
t=f.Get("Events")

nominal_xs = 178.6

n_total = 0
n_weighted = ROOT.TH1F("n_weighted","n_weighted",1,0,1)
n_weighted.Sumw2()
n_weighted_pdf = []

for i in range(0,102):
    n_weighted_pdf.append(ROOT.TH1F("n_weighted_pdf_variation"+str(i),"n_weighted_pdf_variation"+str(i),1,0,1))
    n_weighted_pdf[i].Sumw2()

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

    for j in range(0,102):
        if t.Generator_weight > 0:
            n_weighted_pdf[j].Fill(0.5,t.LHEPdfWeight[j+1])
        else:    
            n_weighted_pdf[j].Fill(0.5,-t.LHEPdfWeight[j+1])

print "n_weighted.GetBinContent(1) = "+str(n_weighted.GetBinContent(1))
print "n_weighted.GetBinError(1) = " + str(n_weighted.GetBinError(1))

for i in range(0,102):
    print "n_weighted_pdf[i].GetBinContent(1) = " + str(n_weighted_pdf[i].GetBinContent(1))
    print "n_weighted_pdf[i].GetBinError(1) = " + str(n_weighted_pdf[i].GetBinError(1))

    print str(nominal_xs*n_weighted_pdf[i].GetBinContent(1)/n_weighted.GetBinContent(1))
