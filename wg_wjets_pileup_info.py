import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-w',dest='wjetsdasquery',required=True)
parser.add_argument('-i',dest='inevtlist',required=True)
parser.add_argument('-o',dest='outevtlist',required=True)

args = parser.parse_args()

import json

print "Reading input DAS query JSON"

f_wjets_lumis_json=open(args.wjetsdasquery)

wjets_lumis_json=json.loads(f_wjets_lumis_json.read())

print "Creating lumi to filename mapping"

lumi_to_file = {}

for i in range(len(wjets_lumis_json)):
    assert(len(wjets_lumis_json[i]['lumi']) == 1)
    assert(len(wjets_lumis_json[i]['lumi'][0].keys()) == 1)
    assert(len(wjets_lumis_json[i]['file']) == 1)
    for j in range(len(wjets_lumis_json[i]['lumi'][0]['number'])):
        lumi_to_file[wjets_lumis_json[i]['lumi'][0]['number'][j]] = str(wjets_lumis_json[i]['file'][0]['name'])

print "Reading input event JSON"

f_wjets_events_json=open(args.inevtlist)

print "Setting filenames"

wjets_events_pileup_info = []

for line in f_wjets_events_json:
    assert(len(line.strip('\n').split(' ')) == 4)
    wjets_events_pileup_info.append({ 
        "lumi" : int(line.strip('\n').split(' ')[0]),
        "event": int(line.strip('\n').split(' ')[1]),
        "photon eta" : float(line.strip('\n').split(' ')[2]),
        "photon phi" : float(line.strip('\n').split(' ')[3]),
        "filename" : "root://cms-xrd-global.cern.ch/"+lumi_to_file[int(line.strip('\n').split(' ')[0])]
    })

print "Adding pileup event info"

from DataFormats.FWLite import Events, Handle

for iev,wjets_event_pileup_info in enumerate(wjets_events_pileup_info):

    if iev % 10 == 0:
        print "iev/len(wjets_events_pileup_info) = "+str(iev)+"/"+str(len(wjets_events_pileup_info))

    wjets_event_pileup_info["pileup events"] = []

    while True:
        try:

            events = Events ([wjets_event_pileup_info["filename"]])

#            puSummaryInfo,puSummaryInfoLabel = Handle("vector<PileupSummaryInfo>"),("mixData")
            puSummaryInfo,puSummaryInfoLabel = Handle("vector<PileupSummaryInfo>"),("slimmedAddPileupInfo")

            for event in events:

                if event.eventAuxiliary().luminosityBlock() != wjets_event_pileup_info["lumi"]:
                    continue

                if event.eventAuxiliary().event() != wjets_event_pileup_info["event"]:
                    continue
                
                event.getByLabel(puSummaryInfoLabel, puSummaryInfo)

                for pu in puSummaryInfo.product():
                    if pu.getBunchCrossing() != 0:
                        continue

                    for eventid in pu.getPU_EventID():
                        wjets_event_pileup_info["pileup events"].append({ "event" : int(eventid.event()), "lumi" : int(eventid.luminosityBlock()) })

                break

            break

        except:

            pass

f_wjets_events_pileup_info = open(args.outevtlist,"w")

json.dump(wjets_events_pileup_info,f_wjets_events_pileup_info)
