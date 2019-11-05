import ROOT
import math

from math import hypot, pi
def deltaR(eta1,phi1,eta2,phi2):
    dphi = abs(phi1-phi2);
    if dphi > pi: dphi = 2*pi-dphi
    return hypot(eta1-eta2,dphi)

f=ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/tmp/BD10FEDE-2447-174B-8426-4BE7869483C4.root")
t=f.Get("Events")

#sample_xs = 178.6
sample_xs = 33420.0 
#sample_xs = 24780.0

n_total = 0
n_weighted = ROOT.TH1F("n_weighted","n_weighted",1,0,1)
n_weighted.Sumw2()
n_weighted_pass_fiducial = ROOT.TH1F("n_weighted_pass_fiducial","n_weighted_fiducial",1,0,1)
n_weighted_pass_fiducial.Sumw2()
n_weighted_pdf = []
n_weighted_scale = []
n_weighted_pdf_pass_fiducial = []
n_weighted_scale_pass_fiducial = []

for i in range(0,32):
    n_weighted_pdf.append(ROOT.TH1F("n_weighted_pdf_variation"+str(i),"n_weighted_pdf_variation"+str(i),1,0,1))
    n_weighted_pdf[i].Sumw2()
    n_weighted_pdf_pass_fiducial.append(ROOT.TH1F("n_weighted_pdf_pass_fiducial_variation"+str(i),"n_weighted_pdf_pass_fiducial_variation"+str(i),1,0,1))
    n_weighted_pdf_pass_fiducial[i].Sumw2()

for i in range(0,8):
    n_weighted_scale.append(ROOT.TH1F("n_weighted_scale_variation"+str(i),"n_weighted_scale_variation"+str(i),1,0,1))
    n_weighted_scale[i].Sumw2()
    n_weighted_scale_pass_fiducial.append(ROOT.TH1F("n_weighted_scale_pass_fiducial_variation"+str(i),"n_weighted_scale_pass_fiducial_variation"+str(i),1,0,1))
    n_weighted_scale_pass_fiducial[i].Sumw2()

isprompt_mask = (1 << 0) #isPrompt                                                                                                                           
isfromhardprocess_mask = (1 << 8) #isFromHardProcess                                                                                                         
isprompttaudecayproduct_mask = (1 << 4) #isPromptTauDecayProduct

print "t.GetEntries() = "+str(t.GetEntries())
for i in range(0,t.GetEntries()):
    if n_total % 10000 == 0:
        print "n_total = "+str(n_total)
    n_total+=1
    t.GetEntry(i)

    n_gen_leptons = 0
    n_gen_photons = 0
    for i in range(0,t.nGenPart):
        if t.GenPart_pt[i] > 5 and t.GenPart_status[i] == 1 and (abs(t.GenPart_pdgId[i]) == 11 or abs(t.GenPart_pdgId[i]) == 13 or abs(t.GenPart_pdgId[i]) == 15) and (t.GenPart_statusFlags[i] & isfromhardprocess_mask == isfromhardprocess_mask) and ((t.GenPart_statusFlags[i] & isprompt_mask == isprompt_mask) or (t.GenPart_statusFlags[i] & isprompttaudecayproduct_mask == isprompttaudecayproduct_mask)):
            gen_lepton_index = i
            n_gen_leptons +=  1
        if t.GenPart_pt[i] > 5 and t.GenPart_status[i] == 1 and t.GenPart_pdgId[i] == 22 and (t.GenPart_statusFlags[i] & isfromhardprocess_mask == isfromhardprocess_mask) and (t.GenPart_statusFlags[i] & isprompt_mask == isprompt_mask):
            gen_photon_index = i
            n_gen_photons +=1

    pass_fiducial = False

    if n_gen_leptons == 1 and n_gen_photons == 1:
        if deltaR(t.GenPart_eta[gen_lepton_index],t.GenPart_phi[gen_lepton_index],t.GenPart_eta[gen_photon_index],t.GenPart_phi[gen_photon_index]) > 0.5 and t.GenPart_pt[gen_lepton_index] > 20 and t.GenPart_pt[gen_photon_index] > 20 and abs(t.GenPart_eta[gen_photon_index]) < 2.5:
            pass_fiducial = True

    assert(n_gen_leptons == 1 or n_gen_leptons == 0)
    assert(n_gen_photons == 1 or n_gen_photons == 0)

    if t.Generator_weight > 0:
        n_weighted.Fill(0.5)
    else:    
        n_weighted.Fill(0.5,-1)

    for j in range(0,8):
        if t.Generator_weight > 0:
            n_weighted_scale[j].Fill(0.5,t.LHEScaleWeight[j]*2)
        else:    
            n_weighted_scale[j].Fill(0.5,-t.LHEScaleWeight[j]*2)
    for j in range(0,32):
        if t.Generator_weight > 0:
            n_weighted_pdf[j].Fill(0.5,t.LHEPdfWeight[j+1])
        else:    
            n_weighted_pdf[j].Fill(0.5,-t.LHEPdfWeight[j+1])


    if pass_fiducial:        
        if t.Generator_weight > 0:
            n_weighted_pass_fiducial.Fill(0.5)
        else:    
            n_weighted_pass_fiducial.Fill(0.5,-1)

        for j in range(0,8):
            if t.Generator_weight > 0:
                n_weighted_scale_pass_fiducial[j].Fill(0.5,t.LHEScaleWeight[j]*2)
            else:    
                n_weighted_scale_pass_fiducial[j].Fill(0.5,-t.LHEScaleWeight[j]*2)
        for j in range(0,32):
            if t.Generator_weight > 0:
                n_weighted_pdf_pass_fiducial[j].Fill(0.5,t.LHEPdfWeight[j+1])
            else:    
                n_weighted_pdf_pass_fiducial[j].Fill(0.5,-t.LHEPdfWeight[j+1])


print "fiducial_region_cuts_efficiency = " + str(n_weighted_pass_fiducial.GetBinContent(1)/n_weighted.GetBinContent(1))

print "n_weighted.GetBinContent(1) = "+str(n_weighted.GetBinContent(1))
print "n_weighted.GetBinError(1) = " + str(n_weighted.GetBinError(1))

pdf_mean = 0
pdf_stddev = 0
scale_mean = 0
scale_stddev = 0

pdf_pass_fiducial_mean = 0
pdf_pass_fiducial_stddev = 0
scale_pass_fiducial_mean = 0
scale_pass_fiducial_stddev = 0

for i in range(0,32):
    pdf_mean+=n_weighted_pdf[i].GetBinContent(1)
    pdf_pass_fiducial_mean+=n_weighted_pdf_pass_fiducial[i].GetBinContent(1)

pdf_mean += n_weighted.GetBinContent(1)
pdf_pass_fiducial_mean += n_weighted_pass_fiducial.GetBinContent(1)

pdf_mean /= 33
pdf_pass_fiducial_mean /= 33

for i in range(0,32):
    pdf_stddev+= pow(n_weighted_pdf[i].GetBinContent(1)-pdf_mean,2)
    pdf_pass_fiducial_stddev+= pow(n_weighted_pdf_pass_fiducial[i].GetBinContent(1)-pdf_pass_fiducial_mean,2)

pdf_stddev += pow(n_weighted.GetBinContent(1)-pdf_mean,2)
pdf_pass_fiducial_stddev += pow(n_weighted_pass_fiducial.GetBinContent(1)-pdf_pass_fiducial_mean,2)

pdf_stddev /= (33-1)
pdf_pass_fiducial_stddev /= (33-1)

pdf_stddev = math.sqrt(pdf_stddev)
pdf_pass_fiducial_stddev = math.sqrt(pdf_pass_fiducial_stddev)

for i in range(0,8):
    if i == 6 or i == 4:
        continue

    scale_mean += n_weighted_scale[i].GetBinContent(1)
    scale_pass_fiducial_mean += n_weighted_scale_pass_fiducial[i].GetBinContent(1)

scale_mean += n_weighted.GetBinContent(1)
scale_pass_fiducial_mean += n_weighted_pass_fiducial.GetBinContent(1)

scale_mean /= 7
scale_pass_fiducial_mean /= 7

for i in range(0,8):
    if i == 6 or i == 4:
        continue

    scale_stddev += pow(n_weighted_scale[i].GetBinContent(1)-scale_mean,2)
    scale_pass_fiducial_stddev += pow(n_weighted_scale_pass_fiducial[i].GetBinContent(1)-scale_pass_fiducial_mean,2)

scale_stddev += pow(n_weighted.GetBinContent(1)-scale_mean,2)
scale_pass_fiducial_stddev += pow(n_weighted_pass_fiducial.GetBinContent(1)-scale_pass_fiducial_mean,2)

scale_stddev /= (7-1)
scale_pass_fiducial_stddev /= (7-1)

scale_stddev = math.sqrt(scale_stddev)
scale_pass_fiducial_stddev = math.sqrt(scale_pass_fiducial_stddev)

nlo_xs = sample_xs

pass_fiducial_nlo_xs = sample_xs * n_weighted_pass_fiducial.GetBinContent(1) / n_weighted.GetBinContent(1)

pdf_unc = pdf_stddev * sample_xs / n_weighted.GetBinContent(1)
pdf_pass_fiducial_unc = pdf_pass_fiducial_stddev * sample_xs / n_weighted.GetBinContent(1)

scale_unc = scale_stddev * sample_xs / n_weighted.GetBinContent(1)
scale_pass_fiducial_unc = scale_pass_fiducial_stddev * sample_xs / n_weighted.GetBinContent(1)

print "efficiency of fiducal region cuts = " + str(n_weighted_pass_fiducial.GetBinContent(1) / n_weighted.GetBinContent(1))

print "nlo xs = " + str(nlo_xs) + " +/- " + str(scale_unc) + " (scale) +/- " + str(pdf_unc) + " (pdf)" 

print "pass fiducial nlo xs = " + str(pass_fiducial_nlo_xs) + " +/- " + str(scale_pass_fiducial_unc) + " (scale) +/- " + str(pdf_pass_fiducial_unc) + " (pdf)" 

print "100*scale_pass_fiducial_unc/pass_fiducial_nlo_xs = "+str(100*scale_pass_fiducial_unc/pass_fiducial_nlo_xs)

print "100*pdf_pass_fiducial_unc/pass_fiducial_nlo_xs = "+str(100*pdf_pass_fiducial_unc/pass_fiducial_nlo_xs)
