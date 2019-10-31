import ROOT

labels = { 
    "top+jets" : {
        "syst-pdf" : False, 
        "syst-scale" : False, 
        "color" : ROOT.kRed, 
        "samples" : 
        {
            "2016":
                [
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019/ttwjets.root", "xs" : 0.2001, "non_fsr" : True, "e_to_p_non_res" : True, "fsr" : True, "e_to_p": True , "e_to_p_for_fake" : True},
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019/stschanneljets.root", "xs" : 6.35, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True},
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019/sttchanneltopjets.root", "xs" : 136.02, "non_fsr" : False, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True},             
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019/sttchannelantitopjets.root", "xs" : 80.95, "non_fsr" : False, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True },           
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019/sttwtopjets.root", "xs" : 71.7/2, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True },
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019/sttwantitopjets.root", "xs" : 71.7/2, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True },
                { "filename":  '/afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019/ttsemijets.root', 'xs' : 365.4, "non_fsr" : False, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True,  "e_to_p_for_fake" : True },
                { "filename":  '/afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019/tt2l2nujets.root', 'xs' : 88.28, "non_fsr" : False, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True },
                {"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019/ttgjets.root", "xs" : 3.795, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True , "fsr" : True, "e_to_p_for_fake" : True}, 
                {"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019/tgjets.root", "xs" : 0.98882289, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True , "fsr" : True, "e_to_p_for_fake" : True} #tgjets cross section * branching ratio to leptons = 2.97 * 0.332937 = 0.98882289  
                
                ],
            "2017":
                [
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019/ttwjets.root", "xs" : 0.2001, "non_fsr" : True, "e_to_p_non_res" : True, "fsr" : True, "e_to_p": True , "e_to_p_for_fake" : True},
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019/stschanneljets.root", "xs" : 6.35, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True},
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019/sttchanneltopjets.root", "xs" : 136.02, "non_fsr" : False, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True},             
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019/sttchannelantitopjets.root", "xs" : 80.95, "non_fsr" : False, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True },           
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019/sttwtopjets.root", "xs" : 71.7/2, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True },
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019/sttwantitopjets.root", "xs" : 71.7/2, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True },
                { "filename":  '/afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019/ttsemijets.root', 'xs' : 365.4, "non_fsr" : False, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True,  "e_to_p_for_fake" : True },
                { "filename":  '/afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019/tt2l2nujets.root', 'xs' : 88.28, "non_fsr" : False, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True },
                {"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019/ttgjets.root", "xs" : 3.795, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True , "fsr" : True, "e_to_p_for_fake" : True} ,
                {"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019/tgjets.root", "xs" : 0.98882289, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True , "fsr" : True, "e_to_p_for_fake" : True} 

                
                ],
            "2018":
                [
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019/ttwjets.root", "xs" : 0.2001, "non_fsr" : True, "e_to_p_non_res" : True, "fsr" : True, "e_to_p": True , "e_to_p_for_fake" : True},
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019/stschanneljets.root", "xs" : 6.35, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True},
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019/sttchanneltopjets.root", "xs" : 136.02, "non_fsr" : False, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True},             
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019/sttchannelantitopjets.root", "xs" : 80.95, "non_fsr" : False, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True },           
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019/sttwtopjets.root", "xs" : 71.7/2, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True },
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019/sttwantitopjets.root", "xs" : 71.7/2, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True },
                { "filename":  '/afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019/ttsemijets.root', 'xs' : 365.4, "non_fsr" : False, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True,  "e_to_p_for_fake" : True },
                { "filename":  '/afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019/tt2l2nujets.root', 'xs' : 88.28, "non_fsr" : False, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True },
                {"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019/ttgjets.root", "xs" : 3.795, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True , "fsr" : True, "e_to_p_for_fake" : True} ,
                {"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019/tgjets.root", "xs" : 0.98882289, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True , "fsr" : True, "e_to_p_for_fake" : True} 
                
                ]
            }
        },
    "vv+jets" : {
        "syst-pdf" : False, 
        "syst-scale" : False, 
        "color" : ROOT.kGreen+3, 
        "samples" : 
        {
            "2016":
                [
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019/wwjets.root", "xs" : 64.3, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True },
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019/wzjets.root", "xs" : 23.43, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True },
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019/zzjets.root", "xs" : 10.16, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True }
                ],
            "2017":
                [
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019/wwjets.root", "xs" : 64.3, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True },
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019/wzjets.root", "xs" : 23.43, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True },
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019/zzjets.root", "xs" : 10.16, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True }

                ],
            "2018":
                [
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019/wwjets.root", "xs" : 64.3, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True },
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019/wzjets.root", "xs" : 23.43, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True },
                { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019/zzjets.root", "xs" : 10.16, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True }

                ]
            }
        },

    "wg+jets" : {
#        "syst-pdf": True, 
#        "syst-scale": True, 
        "syst-pdf": False, 
        "syst-scale": False, 
        "color": ROOT.kCyan, 
        "samples" : {
            "2016":
                [
                {"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019/wgjets.root", "xs" : 178.6, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True} 
#            {"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019/powhegwplusg.root", "xs" : 33420., "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True}, 
#            {"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019/powhegwminusg.root", "xs" : 24780., "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True} 
                ], 
            "2017":
                [
                {"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019/wgjets.root", "xs" : 178.6, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True} 
#            {"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019/powhegwplusg.root", "xs" : 33420., "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True}, 
#            {"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019/powhegwminusg.root", "xs" : 24780., "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True} 
                ], 
            "2018":
                [
                {"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019/wgjets.root", "xs" : 178.6, "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True} 
#            {"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019/powhegwplusg.root", "xs" : 33420., "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True}, 
#            {"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019/powhegwminusg.root", "xs" : 24780., "non_fsr" : True, "e_to_p_non_res" : True, "e_to_p" : True, "fsr" : True, "e_to_p_for_fake" : True} 
                ] 
            }
        }, 
    "zg+jets" : {
        "syst-pdf" : False, 
        "syst-scale" : False, 
        "color" : ROOT.kOrange, 
        "samples" : {
            "2016":
                [
                ##            {"filename": "/afs/cern.ch/work/a/amlevin/data/wg/2016/zglowmlljets.root", "xs" : 96.75, "non_fsr" : True, "e_to_p_non_res" : False, "e_to_p" : False, "fsr" : True, "e_to_p_for_fake" : True} 
                #            {"filename": "/afs/cern.ch/work/a/amlevin/data/wg/2016/14Dec2018/zglowmlljets.root", "xs" : 96.75, "non_fsr" : True, "e_to_p_non_res" : False, "e_to_p" : False, "fsr" : True, "e_to_p_for_fake" : True} 
                {"filename": "/afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019/zglowmlljets.root", "xs" : 96.75/3, "non_fsr" : True, "e_to_p_non_res" : False, "e_to_p" : False, "fsr" : True, "e_to_p_for_fake" : True} 
                ], 
            "2017":
                [
                ##            {"filename": "/afs/cern.ch/work/a/amlevin/data/wg/2016/zglowmlljets.root", "xs" : 96.75, "non_fsr" : True, "e_to_p_non_res" : False, "e_to_p" : False, "fsr" : True, "e_to_p_for_fake" : True} 
                #            {"filename": "/afs/cern.ch/work/a/amlevin/data/wg/2016/14Dec2018/zglowmlljets.root", "xs" : 96.75, "non_fsr" : True, "e_to_p_non_res" : False, "e_to_p" : False, "fsr" : True, "e_to_p_for_fake" : True} 
                {"filename": "/afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019/zglowmlljets.root", "xs" : 96.75/3, "non_fsr" : True, "e_to_p_non_res" : False, "e_to_p" : False, "fsr" : True, "e_to_p_for_fake" : True} 
                ] ,
            "2018":
                [
                ##            {"filename": "/afs/cern.ch/work/a/amlevin/data/wg/2016/zglowmlljets.root", "xs" : 96.75, "non_fsr" : True, "e_to_p_non_res" : False, "e_to_p" : False, "fsr" : True, "e_to_p_for_fake" : True} 
                #            {"filename": "/afs/cern.ch/work/a/amlevin/data/wg/2016/14Dec2018/zglowmlljets.root", "xs" : 96.75, "non_fsr" : True, "e_to_p_non_res" : False, "e_to_p" : False, "fsr" : True, "e_to_p_for_fake" : True} 
                {"filename": "/afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019/zglowmlljets.root", "xs" : 96.75/3, "non_fsr" : True, "e_to_p_non_res" : False, "e_to_p" : False, "fsr" : True, "e_to_p_for_fake" : True} 
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
                {"filename": "/afs/cern.ch/work/a/amlevin/data/wg/2016/1June2019/zjets.root", "xs" : 6225.42, "non_fsr" : False, "e_to_p_non_res" : False, "e_to_p" : True, "fsr" : False, "e_to_p_for_fake" : True} ##6225.42 is the nnlo cross-section
                ], 
            "2017":
        
            [
                {"filename": "/afs/cern.ch/work/a/amlevin/data/wg/2017/1June2019/zjets.root", "xs" : 6225.42, "non_fsr" : False, "e_to_p_non_res" : False, "e_to_p" : True, "fsr" : False, "e_to_p_for_fake" : True} ##6225.42 is the nnlo cross-section

                ], 
            "2018":
        
            [
                {"filename": "/afs/cern.ch/work/a/amlevin/data/wg/2018/1June2019/zjets.root", "xs" : 6225.42, "non_fsr" : False, "e_to_p_non_res" : False, "e_to_p" : True, "fsr" : False, "e_to_p_for_fake" : True} ##6225.42 is the nnlo cross-section

                ] 
            }
        }, 
    }

#labels = { 
#    "ttw+jets" : {
#        "syst-pdf" : False, 
#        "syst-scale" : False, 
#        "color" : ROOT.kOrange+3, 
#        "samples" : [
#            { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/ttwjets.root", "xs" : 0.2001, "non_fsr" : True, "e_to_p_non_res" : True, "fsr" : True, "e_to_p_for_fake" : True }
#            ]
#        },
#    "ww+jets" : {
#        "syst-pdf" : False, 
#        "syst-scale" : False, 
#        "color" : ROOT.kOrange+3, 
#        "samples" : [
#            { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/wwjets.root", "xs" : 64.3, "non_fsr" : True, "e_to_p_non_res" : True, "fsr" : True, "e_to_p_for_fake" : True }
#            ]
#        },
#    "wz+jets" : {
#        "syst-pdf" : False, 
#        "syst-scale" : False, 
#        "color" : ROOT.kOrange+3, 
#        "samples" : [
#            { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/wzjets.root", "xs" : 23.43, "non_fsr" : True, "e_to_p_non_res" : True, "fsr" : True, "e_to_p_for_fake" : True }
#            ]
#        },
#    "zz+jets" : {
#        "syst-pdf" : False, 
#        "syst-scale" : False, 
#        "color" : ROOT.kOrange+3, 
#        "samples" : [
#            { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/zzjets.root", "xs" : 10.16, "non_fsr" : True, "e_to_p_non_res" : True, "fsr" : True, "e_to_p_for_fake" : True }
#            ]
#        },
#    "stschannel+jets" : {
#        "syst-pdf" : False, 
#        "syst-scale" : False, 
#        "color" : ROOT.kOrange+3, 
#        "samples" : [
#            { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/stschanneljets.root", "xs" : 6.35, "non_fsr" : True, "e_to_p_non_res" : True, "fsr" : True, "e_to_p_for_fake" : True }
#            ]
#        },
#    "sttchanneltop+jets" : {
#        "syst-pdf" : False, 
#        "syst-scale" : False, 
#        "color" : ROOT.kOrange+3, 
#        "samples" : [
#            { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/sttchanneltopjets.root", "xs" : 136.02, "non_fsr" : True, "e_to_p_non_res" : True, "fsr" : True, "e_to_p_for_fake" : True }
#            ]
#        },
#    "sttchannelantitop+jets" : {
#        "syst-pdf" : False, 
#        "syst-scale" : False, 
#        "color" : ROOT.kOrange+3, 
#        "samples" : [
#            { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/sttchannelantitopjets.root", "xs" : 80.95, "non_fsr" : True, "e_to_p_non_res" : True, "fsr" : True, "e_to_p_for_fake" : True }
#            ]
#        },
#    "sttwtop+jets" : {
#        "syst-pdf" : False, 
#        "syst-scale" : False, 
#        "color" : ROOT.kOrange+3, 
#        "samples" : [
#            { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/sttwtopjets.root", "xs" : 71.7/2, "non_fsr" : True, "e_to_p_non_res" : True, "fsr" : True, "e_to_p_for_fake" : True }
#            ]
#        },
#    "sttwantitop+jets" : {
#        "syst-pdf" : False, 
#        "syst-scale" : False, 
#        "color" : ROOT.kOrange+3, 
#        "samples" : [
#            { "filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/sttwantitopjets.root", "xs" : 71.7/2, "non_fsr" : True, "e_to_p_non_res" : True, "fsr" : True, "e_to_p_for_fake" : True }
#            ]
#        },
#
#    "tt2l2nu+jets" : {
#        "syst-pdf" : False, 
#        "syst-scale" : False, 
#        "color" : ROOT.kRed, 
#        "samples" : [
#            { 'filename':  '/afs/cern.ch/work/a/amlevin/data/wg/2016/tt2l2nujets.root', 'xs' : 88.28, "non_fsr" : False, "e_to_p_non_res" : True, "fsr" : True, "e_to_p_for_fake" : True } 
#            ]
#     }, 
#    "ttsemi+jets" : {
#        "syst-pdf" : False, 
#        "syst-scale" : False, 
#        "color" : ROOT.kSpring, 
#        "samples" : [
#            {'filename':  '/afs/cern.ch/work/a/amlevin/data/wg/2016/ttsemijets.root', 'xs' : 365.4, "non_fsr" : False, "e_to_p_non_res" : True, "fsr" : True,  "e_to_p_for_fake" : True } 
#            ] 
#        }, 
#    "wg+jets" : {
#        "syst-pdf": True, 
#        "syst-scale": True, 
#        "color": ROOT.kCyan, 
#        "samples" : [
#            {"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/wgjets.root", "xs" : 178.6, "non_fsr" : True, "e_to_p_non_res" : True,"fsr" : True, "e_to_p_for_fake" : True} 
#            ] 
#        }, 
#    "zg+jets" : {
#        "syst-pdf" : False, 
#        "syst-scale" : False, 
#        "color" : ROOT.kOrange, 
#        "samples" : [
#            {"filename": "/afs/cern.ch/work/a/amlevin/data/wg/2016/zglowmlljets.root", "xs" : 96.75, "non_fsr" : True, "e_to_p_non_res" : False, "fsr" : True, "e_to_p_for_fake" : True} 
#            ] 
#        }, 
#    "no label" : {
#        "syst-pdf" : False, 
#        "syst-scale" : False, 
#        "color" : None, 
#        "samples" : [
#            {"filename": "/afs/cern.ch/work/a/amlevin/data/wg/2016/zjets.root", "xs" : 4963.0, "non_fsr" : False, "e_to_p_non_res" : False, "fsr" : False, "e_to_p_for_fake" : True}
#            ] 
#        }, 
#    "ttg+jets" : {
#        "syst-pdf" : False, 
#        "syst-scale" : False,  
#        "color" : ROOT.kGreen+2, 
#        "samples" : [ 
#            {"filename" : "/afs/cern.ch/work/a/amlevin/data/wg/2016/ttgjets.root", "xs" : 3.795, "non_fsr" : True, "e_to_p_non_res" : True, "fsr" : True, "e_to_p_for_fake" : True} 
#            ] 
#        } 
#    }
