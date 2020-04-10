import ROOT
from DataFormats.FWLite import Events, Handle
import json

from math import hypot, pi

def deltaPhi(phi1,phi2):
    ## Catch if being called with two objects

    if type(phi1) != float and type(phi1) != int:
        phi1 = phi1.phi
    if type(phi2) != float and type(phi2) != int:
        phi2 = phi2.phi
    # Otherwise

    dphi = (phi1-phi2)
    while dphi >  pi: dphi -= 2*pi
    while dphi < -pi: dphi += 2*pi
    return dphi

def deltaR(eta1,phi1,eta2=None,phi2=None):
    ## catch if called with objects

    if eta2 == None:
        return deltaR(eta1.eta,eta1.phi,phi1.eta,phi1.phi)
    ## otherwise

    return hypot(eta1-eta2, deltaPhi(phi1,phi2))


print "Reading input DAS query JSON"

f_minbias_lumis_json=open("minbias_lfns_lumis.txt")

minbias_lumis_json=json.loads(f_minbias_lumis_json.read())

print "Creating lumi to filename mapping"

lumi_to_file = {}

for i in range(len(minbias_lumis_json)):
    assert(len(minbias_lumis_json[i]['lumi']) == 1)
    assert(len(minbias_lumis_json[i]['lumi'][0].keys()) == 1)
    assert(len(minbias_lumis_json[i]['file']) == 1)
    for j in range(len(minbias_lumis_json[i]['lumi'][0]['number'])):
        lumi_to_file[minbias_lumis_json[i]['lumi'][0]['number'][j]] = str(minbias_lumis_json[i]['file'][0]['name'])

print "Reading input event json"

f_wjets_events_json=open("wjets_v1_events_info.txt")

wjets_events=json.loads(f_wjets_events_json.read())

print "Setting filenames"

for wjets_event in wjets_events:

    wjets_event["pileup filenames"] = []

    for pu_event in wjets_event["pileup events"]:
        if "root://cms-xrd-global.cern.ch/"+lumi_to_file[pu_event["lumi"]] not in wjets_event["pileup filenames"]:
            wjets_event["pileup filenames"].append("root://cms-xrd-global.cern.ch/"+lumi_to_file[pu_event["lumi"]])

print "Setting photon promptness flags"
        
for iev,wjets_event in enumerate(wjets_events):

    while(True):

        if iev % 1 == 0:
            print "iev/len(wjets_events) = "+str(iev)+"/"+str(len(wjets_events))

        infilelist = []    

        for pu_filename in wjets_event["pileup filenames"]:
            infilelist.append(pu_filename)

        try:    
    
            events = Events (infilelist)    

            genparticles, genParticlesLabel = Handle("vector<reco::GenParticle>"), "genParticles"
        
            for event in events:
                if not {"lumi" : event.eventAuxiliary().luminosityBlock(), "event" : event.eventAuxiliary().event()} in wjets_event["pileup events"]:
                    continue

                event.getByLabel(genParticlesLabel, genparticles)

                for genparticle in genparticles.product():
            
                    if genparticle.status() != 1:
                        continue

                    dr_genpart_photon = deltaR(genparticle.eta(),genparticle.phi(),wjets_event["photon eta"],wjets_event["photon phi"])

                    if dr_genpart_photon > 0.5:
                        continue

                    if genparticle.pt() < 5:
                        continue

                    print str(genparticle.status())+" "+str(genparticle.pdgId())+" "+str(genparticle.pt())+" "+str(dr_genpart_photon)+" "+str(genparticle.mother(0).pdgId())    

            break
                    
        except:

            pass

