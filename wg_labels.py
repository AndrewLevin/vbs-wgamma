import ROOT

labels = { 
    "w+jets" : {
        "legend" : "W+jets",
        "syst-pdf" : False, 
        "syst-scale" : False, 
        "color" : ROOT.kGray+1,
        "samples" :
        {
            "2016" : [
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019/wjets.root", "xs" : 61526.7, "non_fsr" : False, "e_to_p_non_res" : False, "fsr" : False, "e_to_p": False , "e_to_p_for_fake" : False, "non-prompt" : True} #xs from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
                ],
            "2017" : [
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019/wjets.root", "xs" : 61526.7, "non_fsr" : False, "e_to_p_non_res" : False, "fsr" : False, "e_to_p": False , "e_to_p_for_fake" : False, "non-prompt" : True} #xs from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
                ],
            "2018" : [
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019/wjets.root", "xs" : 61526.7, "non_fsr" : False, "e_to_p_non_res" : False, "fsr" : False, "e_to_p": False , "e_to_p_for_fake" : False, "non-prompt" : True} #xs from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
                ]
        }
    },
    "top+jets" : {
        "legend" : "top+jets",
        "syst-pdf" : False, 
        "syst-scale" : False, 
        "color" : ROOT.kRed, 
        "samples" : 
        {
            "2016":
                [
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019jetunc/ttwjets.root", "xs" : 0.2007, "non_fsr" : True, "e_to_p_non_res" : True, "fsr" : True, "e_to_p": True , "e_to_p_for_fake" : True, "non-prompt" : False}, #gen xs analyzer
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019jetunc/stschanneljets.root", "xs" : 10.32, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True, "non-prompt" : False},#https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019jetunc/sttchanneltopjets.root", "xs" : 136.02, "non_fsr" : False, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True, "non-prompt" : False},#https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019jetunc/sttchannelantitopjets.root", "xs" : 80.95, "non_fsr" : False, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True , "non-prompt" : False},#https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019jetunc/sttwtopjets.root", "xs" : 71.7/2, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True , "non-prompt" : False}, #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019jetunc/sttwantitopjets.root", "xs" : 71.7/2, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True , "non-prompt" : False}, #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
                { "filename":  ' /afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019jetunc/ttsemijets.root', 'xs' : 365.35, "non_fsr" : False, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True,  "e_to_p_for_fake" : True , "non-prompt" : False}, #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO, 831.76 * 2 * 3 * 0.1086 * 0.6741 = 365.35
                { "filename":  ' /afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019jetunc/tt2l2nujets.root', 'xs' : 88.29, "non_fsr" : False, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True , "non-prompt" : False}, #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO, 831.76 * (3 * 0.1086)^2 = 88.29
                {"filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019jetunc/ttgjets.root", "xs" : 3.766, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True , "fsr" : True, "e_to_p_for_fake" : True, "non-prompt" : False}, #gen xs analyzer
                    {"filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019jetunc/tgjets.root", "xs" : 0.98882289, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True , "fsr" : True, "e_to_p_for_fake" : True, "non-prompt" : False} #TGJets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8 cross section * branching ratio to leptons = 2.97 * 0.332937 = 0.98882289
                
                ],
            "2017":
                [
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019jetunc/ttwjets.root", "xs" : 0.2141, "non_fsr" : True, "e_to_p_non_res" : True, "fsr" : True, "e_to_p": True , "e_to_p_for_fake" : True, "non-prompt" : False}, #gen xs analyzer
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019jetunc/stschanneljets.root", "xs" : 10.32, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True, "non-prompt" : False},#https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019jetunc/sttchanneltopjets.root", "xs" : 136.02, "non_fsr" : False, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True, "non-prompt" : False},#https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019jetunc/sttchannelantitopjets.root", "xs" : 80.95, "non_fsr" : False, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True , "non-prompt" : False},#https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019jetunc/sttwtopjets.root", "xs" : 71.7/2, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True , "non-prompt" : False}, #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019jetunc/sttwantitopjets.root", "xs" : 71.7/2, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True , "non-prompt" : False}, #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
                { "filename":  ' /afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019jetunc/ttsemijets.root', 'xs' : 365.35, "non_fsr" : False, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True,  "e_to_p_for_fake" : True , "non-prompt" : False}, #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO, 831.76 * 2 * 3 * 0.1086 * 0.6741 = 365.35
                { "filename":  ' /afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019jetunc/tt2l2nujets.root', 'xs' : 88.29, "non_fsr" : False, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True , "non-prompt" : False}, #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO, 831.76 * (3 * 0.1086)^2 = 88.29
                {"filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019jetunc/ttgjets.root", "xs" : 4.124, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True , "fsr" : True, "e_to_p_for_fake" : True, "non-prompt" : False}, #gen xs analyzer
                {"filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019jetunc/tgjets.root", "xs" : 1.017122535, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True , "fsr" : True, "e_to_p_for_fake" : True, "non-prompt" : False} #TGJets_TuneCP5_13TeV_amcatnlo_madspin_pythia8 cross section * branching ratio to leptons = 3.055 * 0.332937 =  1.017122535

                
                ],
            "2018":
                [
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019jetunc/ttwjets.root", "xs" : 0.2141, "non_fsr" : True, "e_to_p_non_res" : True, "fsr" : True, "e_to_p": True , "e_to_p_for_fake" : True, "non-prompt" : False}, #gen xs analyzer
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019jetunc/stschanneljets.root", "xs" : 10.32, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True, "non-prompt" : False},#https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019jetunc/sttchanneltopjets.root", "xs" : 136.02, "non_fsr" : False, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True, "non-prompt" : False},#https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019jetunc/sttchannelantitopjets.root", "xs" : 80.95, "non_fsr" : False, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True , "non-prompt" : False},#https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019jetunc/sttwtopjets.root", "xs" : 71.7/2, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True , "non-prompt" : False}, #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019jetunc/sttwantitopjets.root", "xs" : 71.7/2, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True , "non-prompt" : False}, #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
                { "filename":  ' /afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019jetunc/ttsemijets.root', 'xs' : 365.35, "non_fsr" : False, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True,  "e_to_p_for_fake" : True , "non-prompt" : False}, #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO, 831.76 * 2 * 3 * 0.1086 * 0.6741 = 365.35
                { "filename":  ' /afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019jetunc/tt2l2nujets.root', 'xs' : 88.29, "non_fsr" : False, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True , "non-prompt" : False}, #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO, 831.76 * (3 * 0.1086)^2 = 88.29
                {"filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019jetunc/ttgjets.root", "xs" : 4.124, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True , "fsr" : True, "e_to_p_for_fake" : True, "non-prompt" : False}, #gen xs analyzer
                {"filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019jetunc/tgjets.root", "xs" : 1.017122535, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True , "fsr" : True, "e_to_p_for_fake" : True, "non-prompt" : False} #TGJets_TuneCP5_13TeV_amcatnlo_madspin_pythia8 cross section * branching ratio to leptons = 3.055 * 0.332937 = 1.017122535  
                
                ]
            }
        },
    "vv+jets" : {
        "legend" : "VV+jets",
        "syst-pdf" : False, 
        "syst-scale" : False, 
        "color" : ROOT.kGreen+3, 
        "samples" : 
        {
            "2016":
                [
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019jetunc/wwjets.root", "xs" : 64.3, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True , "non-prompt" : False}, #gen xs analyzer
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019jetunc/wzjets.root", "xs" : 23.43, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True , "non-prompt" : False}, #gen xs analyzer
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019jetunc/zzjets.root", "xs" : 10.15, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True , "non-prompt" : False} #gen xs analyzer
                ],
            "2017":
                [
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019jetunc/wwjets.root", "xs" : 75.91, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True , "non-prompt" : False}, #gen xs analyzer
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019jetunc/wzjets.root", "xs" : 27.57, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True , "non-prompt" : False}, #gen xs analyzer
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019jetunc/zzjets.root", "xs" : 12.14, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True , "non-prompt" : False} #gen xs analyzer

                ],
            "2018":
                [
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019jetunc/wwjets.root", "xs" : 75.91, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True , "non-prompt" : False}, #gen xs analyzer
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019jetunc/wzjets.root", "xs" : 27.57, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True , "non-prompt" : False}, #gen xs analyzer
                { "filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019jetunc/zzjets.root", "xs" : 12.14, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True , "non-prompt" : False} #gen xs analyzer

                ]
            }
        },

    "wg+jets" : {
        "legend" : "W#gamma+jets",
        "syst-pdf": True, 
        "syst-scale": True, 
#        "syst-pdf": False, 
#        "syst-scale": False, 
        "color": ROOT.kCyan, 
        "color-fid" : ROOT.kCyan,
        "color-non-fid" : ROOT.kRed-7,
        "samples" : {
            "2016":
                [
                {"filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019jetunc/wgjets.root", "xs" : 178.7, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True, "non-prompt" : False} #gen xs analyzer
#            {"filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019jetunc/powhegwplusg.root", "xs" : , "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True, "non-prompt" : False}, 
#            {"filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019jetunc/powhegwminusg.root", "xs" : , "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True} 
                ], 
            "2017":
                [
                {"filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019jetunc/wgjets.root", "xs" : 190.9, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True, "non-prompt" : False} #gen xs analyzer
#            {"filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019jetunc/powhegwplusg.root", "xs" : , "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True, "non-prompt" : False}, 
#            {"filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019jetunc/powhegwminusg.root", "xs" : , "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True} 
                ], 
            "2018":
                [
                {"filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019jetunc/wgjets.root", "xs" : 190.9, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True, "non-prompt" : False} #gen xs analyzer
#            {"filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019jetunc/powhegwplusg.root", "xs" : , "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True, "non-prompt" : False}, 
#            {"filename" : " /afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019jetunc/powhegwminusg.root", "xs" : , "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True} 
                ] 
            }
        }, 
    "zg+jets" : {
        "legend" : "Z#gamma+jets",
#        "syst-pdf" : False, 
#        "syst-scale" : False, 
        "syst-pdf" : True, 
        "syst-scale" : True, 
        "color" : ROOT.kOrange, 
        "samples" : {
            "2016":
                [
                {"filename": " /afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019jetunc/zglowmlljets.root", "xs" : 98.22, "non_fsr" : True, "e_to_p_non_res" : False, "e_to_p" : False, "fsr" : True, "e_to_p_for_fake" : True, "non-prompt" : False} #gen xs analyzer 
                ], 
            "2017":
                [
                {"filename": " /afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019jetunc/zglowmlljets.root", "xs" : 105.6, "non_fsr" : True, "e_to_p_non_res" : False, "e_to_p" : False, "fsr" : True, "e_to_p_for_fake" : True, "non-prompt" : False} #gen xs analyzer
                ] ,
            "2018":
                [
                {"filename": " /afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019jetunc/zglowmlljets.root", "xs" : 105.6, "non_fsr" : True, "e_to_p_non_res" : False, "e_to_p" : False, "fsr" : True, "e_to_p_for_fake" : True, "non-prompt" : False} #gen xs analyzer 
                ] 

            }
        }, 
    "no label" : {
        "syst-pdf" : False, 
        "syst-scale" : False, 
        "color" : None, 
        "samples" : 
        {
            "2016":
        
            [
                {"filename": " /afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019jetunc/zjets.root", "xs" : 6225.42, "non_fsr" : False, "e_to_p_non_res" : False, "e_to_p" : True, "fsr" : False, "e_to_p_for_fake" : True, "non-prompt" : False} #https://hypernews.cern.ch/HyperNews/CMS/get/generators/4072/1/1/1/1/1/1/2/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1.html
                ], 
            "2017":
        
            [
                {"filename": " /afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019jetunc/zjets.root", "xs" : 6225.42, "non_fsr" : False, "e_to_p_non_res" : False, "e_to_p" : True, "fsr" : False, "e_to_p_for_fake" : True, "non-prompt" : False} #https://hypernews.cern.ch/HyperNews/CMS/get/generators/4072/1/1/1/1/1/1/2/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1.html

                ], 
            "2018":
        
            [
                {"filename": " /afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019jetunc/zjets.root", "xs" : 6225.42, "non_fsr" : False, "e_to_p_non_res" : False, "e_to_p" : True, "fsr" : False, "e_to_p_for_fake" : True, "non-prompt" : False} #https://hypernews.cern.ch/HyperNews/CMS/get/generators/4072/1/1/1/1/1/1/2/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1.html

                ] 
            }
        }, 
    }

