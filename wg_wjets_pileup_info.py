import json

print "Reading input DAS query JSON"

f_wjets_lumis_json=open("wjets_v2_lfns_lumis.txt")

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

f_wjets_events_json=open("wjets_events.v2.txt")

print "Setting filenames"

wjets_events= []

for line in f_wjets_events_json:
    assert(len(line.strip('\n').split(' ')) == 4)
    wjets_events.append({ 
        "lumi" : int(line.strip('\n').split(' ')[0]),
        "event": int(line.strip('\n').split(' ')[1]),
        "photon eta" : float(line.strip('\n').split(' ')[2]),
        "photon phi" : float(line.strip('\n').split(' ')[3]),
        "filename" : "root://cms-xrd-global.cern.ch/"+lumi_to_file[int(line.strip('\n').split(' ')[0])]
    })

print "Adding pileup event info"

for iev,wjets_event in enumerate(wjets_events):

    if iev % 10 == 0:
        print "iev/len(wjets_events) = "+str(iev)+"/"+str(len(wjets_events))

    import ROOT
    import sys
    from DataFormats.FWLite import Events, Handle

    wjets_event["pileup events"] = []

    events = Events ([wjets_event["filename"]])

#    puSummaryInfo,puSummaryInfoLabel = Handle("vector<PileupSummaryInfo>"),("mixData")
    puSummaryInfo,puSummaryInfoLabel = Handle("vector<PileupSummaryInfo>"),("slimmedAddPileupInfo")

    for event in events:

        if event.eventAuxiliary().luminosityBlock() != wjets_event["lumi"]:
            continue

        if event.eventAuxiliary().event() != wjets_event["event"]:
            continue
                
        event.getByLabel(puSummaryInfoLabel, puSummaryInfo)

        for pu in puSummaryInfo.product():
            if pu.getBunchCrossing() != 0:
                continue

            for eventid in pu.getPU_EventID():
                wjets_event["pileup events"].append({ "event" : int(eventid.event()), "lumi" : int(eventid.luminosityBlock()) })

f_wjets_events_info = open("wjets_v2_events_info.txt","w")

json.dump(wjets_events,f_wjets_events_info)
