//root -l -b -q add_puppimet_uncertainties.C++\(\"/afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019/zglowmlljets.root\",\"/afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019jetunc/zglowmlljets.root\",\"/eos/user/y/yangli/andrew/data/nano/zglowmlljets/2016/zglowmlljets.*.root\"\)

#include "TChain.h"
#include "TFile.h"
#include "TH1D.h"
#include <iostream>
#include <map>
#include <vector>

void add_puppimet_uncertainties (TString infile, TString outfile, TString puppimetfiles) {

    TFile fin(infile,"read");

    TTree * torig = (TTree*) fin.Get("Events");

    TFile fout(outfile,"recreate");

    fout.cd();

    TH1D * nEvents;
    TH1D * nEventsGenWeighted;

    fin.GetObject("nEvents",nEvents);
    
    fout.WriteObject(nEvents,"nEvents");

    fin.GetObject("nEventsGenWeighted",nEventsGenWeighted);
    
    fout.WriteObject(nEventsGenWeighted,"nEventsGenWeighted");

    TTree * tnew  = torig->CloneTree();

    Float_t puppimetJESUp = -1;
    Float_t puppimetJERUp = -1;
    Float_t puppimetphiJESUp = -1;
    Float_t puppimetphiJERUp = -1;

    TBranch * br1 = tnew->Branch("puppimetJESUp",&puppimetJESUp,"puppimetJESUp/F");
    TBranch * br2 = tnew->Branch("puppimetJERUp",&puppimetJESUp,"puppimetJERUp/F");
    TBranch * br3 = tnew->Branch("puppimetphiJESUp",&puppimetJESUp,"puppimetphiJESUp/F");
    TBranch * br4 = tnew->Branch("puppimetphiJERUp",&puppimetJESUp,"puppimetphiJERUp/F");

    for(UInt_t j = 0; j < tnew->GetEntries(); j++){
        tnew->GetEntry(j);
        br1->Fill();
        br2->Fill();
        br3->Fill();
        br4->Fill();
    }

    tnew->Write("",TObject::kOverwrite);

    TTree * told = tnew;

    std::map<std::pair<std::pair<UInt_t,UInt_t>,ULong64_t>,std::vector<Float_t> > map_puppimet;

    TChain tchain("Events");

    tchain.Add(puppimetfiles);

    UInt_t tchain_entries = tchain.GetEntries();

    std::cout << "tchain_entries = " << tchain_entries << std::endl;

    Float_t puppimet_pt;
    Float_t puppimet_ptJESUp;
    Float_t puppimet_ptJERUp;
    Float_t puppimet_phiJESUp;
    Float_t puppimet_phiJERUp;
    Float_t puppimet;
    UInt_t run;
    UInt_t lumi;
    ULong64_t event;

    for(UInt_t i = 0; i < (tchain_entries/100000000)+1; i++){
        std::cout << "i = " << i << std::endl;

        tchain.SetBranchAddress("PuppiMET_pt",&puppimet_pt);
        tchain.SetBranchAddress("PuppiMET_ptJESUp",&puppimet_ptJESUp);
        tchain.SetBranchAddress("PuppiMET_ptJERUp",&puppimet_ptJERUp);
        tchain.SetBranchAddress("PuppiMET_phiJESUp",&puppimet_phiJESUp);
        tchain.SetBranchAddress("PuppiMET_phiJERUp",&puppimet_phiJERUp);
        tchain.SetBranchAddress("run",&run);
        tchain.SetBranchAddress("luminosityBlock",&lumi);
        tchain.SetBranchAddress("event",&event);

        for(UInt_t j = i*100000000; j < (i+1)*100000000; j++){

            if (j > tchain_entries)
                continue;

            if(j % 1000000 == 0)
                std::cout << "j = " << j << std::endl;

            tchain.GetEntry(j);

            std::vector<Float_t> puppimet_vector;
            puppimet_vector.push_back(puppimet_pt);
            puppimet_vector.push_back(puppimet_ptJESUp);
            puppimet_vector.push_back(puppimet_ptJERUp);
            puppimet_vector.push_back(puppimet_phiJESUp);
            puppimet_vector.push_back(puppimet_phiJERUp);

            map_puppimet.insert(std::make_pair(std::pair(std::make_pair(run,lumi),event), puppimet_vector));
        }

        Float_t oldpuppimetJESUp;
        Float_t oldpuppimetJERUp;
        Float_t oldpuppimetphiJESUp;
        Float_t oldpuppimetphiJERUp;

        told->SetBranchAddress("run",&run);
        told->SetBranchAddress("lumi",&lumi);
        told->SetBranchAddress("event",&event);
        told->SetBranchAddress("puppimet",&puppimet);
        told->SetBranchAddress("puppimetJESUp",&oldpuppimetJESUp);
        told->SetBranchAddress("puppimetJERUp",&oldpuppimetJERUp);
        told->SetBranchAddress("puppimetphiJESUp",&oldpuppimetphiJESUp);
        told->SetBranchAddress("puppimetphiJERUp",&oldpuppimetphiJERUp);

        fout.cd();

        tnew  = torig->CloneTree();

        TBranch * br1 = tnew->Branch("puppimetJESUp",&puppimetJESUp,"puppimetJESUp/F");
        TBranch * br2 = tnew->Branch("puppimetJERUp",&puppimetJERUp,"puppimetJERUp/F");
        TBranch * br3 = tnew->Branch("puppimetphiJESUp",&puppimetphiJESUp,"puppimetphiJESUp/F");
        TBranch * br4 = tnew->Branch("puppimetphiJERUp",&puppimetphiJERUp,"puppimetphiJERUp/F");

        for(UInt_t j = 0; j < told->GetEntries(); j++){
            told->GetEntry(j);
            std::vector<Float_t> puppimet_vector = map_puppimet[std::pair(std::make_pair(run,lumi),event)];

            if (oldpuppimetJESUp != -1){
                puppimetJESUp = oldpuppimetJESUp;
                puppimetJERUp = oldpuppimetJERUp;
                puppimetphiJESUp = oldpuppimetphiJESUp;
                puppimetphiJERUp = oldpuppimetphiJERUp;
            }
            else if (puppimet_vector.size() != 0) {
                //                std::cout << puppimet << " " << map_puppimet[std::pair(std::make_pair(run,lumi),event)] << " " << map_puppimetJESUp[std::pair(std::make_pair(run,lumi),event)] << std::endl;

                puppimetJESUp = puppimet_vector[1];
                puppimetJERUp = puppimet_vector[2];
                puppimetphiJESUp = puppimet_vector[3];
                puppimetphiJERUp = puppimet_vector[4];
            }
            else {
                puppimetJESUp = -1;
                puppimetJERUp = -1;
                puppimetphiJESUp = -1;
                puppimetphiJERUp = -1;
            }
            br1->Fill();
            br2->Fill();
            br3->Fill();
            br4->Fill();
        
        }

        tnew->Write("",TObject::kOverwrite);

        told  = tnew;

        map_puppimet.clear();
            
    }

    std::cout << "tnew->GetEntries(\"puppimetJESUp == -1\") = " << tnew->GetEntries("puppimetJESUp == -1") << std::endl;

}

