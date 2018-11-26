import ROOT
import math

from math import hypot, pi
def deltaR(eta1,phi1,eta2,phi2):
    dphi = abs(phi1-phi2);
    if dphi > pi: dphi = 2*pi-dphi
    return hypot(eta1-eta2,dphi)

f=ROOT.TFile.Open("/eos/user/a/amlevin/tmp/wgjets.1.root")
t=f.Get("Events")

nominal_xs = 178.6

n_total = 0
n_weighted = ROOT.TH1F("n_weighted","n_weighted",1,0,1)
n_weighted.Sumw2()
n_weighted_nlo = ROOT.TH1F("n_weighted_nlo","n_weighted_nlo",1,0,1)
n_weighted_nlo.Sumw2()
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

    n_w_plus = 0
    n_w_minus = 0
    n_photon = 0

    

    for j in range(0,t.nLHEPart):
        if t.LHEPart_pdgId[j] == -11 or t.LHEPart_pdgId[j] == -13 or t.LHEPart_pdgId[j] == -15:
            n_w_plus+=1
            lepton_eta = t.LHEPart_eta[j]
            lepton_phi = t.LHEPart_phi[j]
        elif t.LHEPart_pdgId[j] == 11 or t.LHEPart_pdgId[j] == 13 or t.LHEPart_pdgId[j] == 15:
            n_w_minus+=1
            lepton_eta = t.LHEPart_eta[j]
            lepton_phi = t.LHEPart_phi[j]
        elif t.LHEPart_pdgId[j] == 22:
            n_photon += 1 
            photon_phi = t.LHEPart_phi[j]
            photon_eta = t.LHEPart_eta[j]
            photon_pt = t.LHEPart_pt[j]

    assert(n_w_minus == 1 or n_w_plus == 1)        

    assert(n_photon == 1)

    weight = 1

    if t.Generator_weight > 0:
        n_weighted.Fill(0.5)
    else:    
        n_weighted.Fill(0.5,-1)

    if deltaR(lepton_eta,lepton_phi,photon_eta,photon_phi) < 0.7:
        continue

    if t.Generator_weight > 0:
        n_weighted_nlo.Fill(0.5,weight)
    else:    
        n_weighted_nlo.Fill(0.5,-weight)

    for j in range(0,8):
        if t.Generator_weight > 0:
            n_weighted_scale[j].Fill(0.5,t.LHEScaleWeight[j]*2*weight)
        else:    
            n_weighted_scale[j].Fill(0.5,-t.LHEScaleWeight[j]*2*weight)
    for j in range(0,102):
        if t.Generator_weight > 0:
            n_weighted_pdf[j].Fill(0.5,t.LHEPdfWeight[j+1]*weight)
        else:    
            n_weighted_pdf[j].Fill(0.5,-t.LHEPdfWeight[j+1]*weight)

pdf_mean = 0
pdf_stddev = 0
scale_mean = 0
scale_stddev = 0

print "n_weighted.GetBinContent(1) = "+str(n_weighted.GetBinContent(1))
print "n_weighted.GetBinError(1) = " + str(n_weighted.GetBinError(1))

for i in range(0,102):
    #print "n_weighted_pdf[i].GetBinContent(1) = " + str(n_weighted_pdf[i].GetBinContent(1))
    #print "n_weighted_pdf[i].GetBinError(1) = " + str(n_weighted_pdf[i].GetBinError(1))

#    print "pdf variation "+str(i)+" xs: "+str(nominal_xs*n_weighted_pdf[i].GetBinContent(1)/n_weighted.GetBinContent(1))
    pdf_mean+=n_weighted_pdf[i].GetBinContent(1)

pdf_mean += n_weighted.GetBinContent(1)

pdf_mean /= 103

for i in range(0,102):
    pdf_stddev+= pow(n_weighted_pdf[i].GetBinContent(1)-pdf_mean,2)

pdf_stddev += pow(n_weighted_nlo.GetBinContent(1)-pdf_mean,2)

pdf_stddev /= (103-1)

pdf_stddev = math.sqrt(pdf_stddev)

for i in range(0,8):
    if i == 6 or i == 4:
        continue

    scale_mean += n_weighted_scale[i].GetBinContent(1)

    #print "n_weighted_scale[i].GetBinContent(1) = " + str(n_weighted_scale[i].GetBinContent(1))
    #print "n_weighted_scale[i].GetBinError(1) = " + str(n_weighted_scale[i].GetBinError(1))

#    print "scale variation "+str(i)+" xs: "+ str(nominal_xs*n_weighted_scale[i].GetBinContent(1)/n_weighted.GetBinContent(1))

scale_mean += n_weighted_nlo.GetBinContent(1)

scale_mean /= 7

for i in range(0,8):
    if i == 6 or i == 4:
        continue

    scale_stddev += pow(n_weighted_scale[i].GetBinContent(1)-scale_mean,2)

scale_stddev += pow(n_weighted_nlo.GetBinContent(1)-scale_mean,2)

scale_stddev /= (7-1)

scale_stddev = math.sqrt(scale_stddev)

nlo_xs = n_weighted_nlo.GetBinContent(1) * nominal_xs / n_weighted.GetBinContent(1)

pdf_unc = pdf_stddev * nominal_xs / n_weighted.GetBinContent(1)

scale_unc = scale_stddev * nominal_xs / n_weighted.GetBinContent(1)

print "nlo xs = " + str(nlo_xs) + " +/- " + str(scale_unc) + " (scale) +/- " + str(pdf_unc) + " (pdf)" 
