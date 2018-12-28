
from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'wg_15'
config.General.transferLogs=False
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/afs/cern.ch/user/a/amlevin/wg/2017/CMSSW_10_2_9/src/PhysicsTools/NanoAODTools/crab/PSet.py'
config.JobType.scriptExe = 'wg_crab_script.sh'
config.JobType.inputFiles = ['crab_script.py','/afs/cern.ch/user/a/amlevin/wg/2017/CMSSW_10_2_9/src/PhysicsTools/NanoAODTools/scripts/haddnanocrab.py','/afs/cern.ch/user/a/amlevin/wg/2017/keep_and_drop.txt','/afs/cern.ch/user/a/amlevin/wg/2017/output_branch_selection.txt','/afs/cern.ch/user/a/amlevin/wg/2017/wgModule.py','/afs/cern.ch/user/a/amlevin/wg/2017/countHistogramsModule.py','/afs/cern.ch/user/a/amlevin/wg/2017/wg_postproc.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True
config.section_("Data")

#config.Data.inputDataset = '/SingleElectron/Run2017B-31Mar2018-v1/NANOAOD'
#config.Data.inputDataset = '/SingleElectron/Run2017C-31Mar2018-v1/NANOAOD'
#config.Data.inputDataset = '/SingleElectron/Run2017D-31Mar2018-v1/NANOAOD'
#config.Data.inputDataset = '/SingleElectron/Run2017E-31Mar2018-v1/NANOAOD'
#config.Data.inputDataset = '/SingleElectron/Run2017F-31Mar2018-v1/NANOAOD'

#config.Data.inputDataset = '/SingleMuon/Run2017B-31Mar2018-v1/NANOAOD'
#config.Data.inputDataset = '/SingleMuon/Run2017C-31Mar2018-v1/NANOAOD'
#config.Data.inputDataset = '/SingleMuon/Run2017D-31Mar2018-v1/NANOAOD'
#config.Data.inputDataset = '/SingleMuon/Run2017E-31Mar2018-v1/NANOAOD'
config.Data.inputDataset = '/SingleMuon/Run2017F-31Mar2018-v1/NANOAOD'

config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
#config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 1
#config.Data.totalUnits = 2000
#config.Data.inputDBS='phys03'
config.Data.outLFNDirBase = '/store/user/amlevin/'
config.Data.publication = False
config.Data.outputDatasetTag = 'wg-2017'
config.section_("Site")
config.Site.storageSite = "T2_CH_CERN"

#config.Data.ignoreLocality = True

config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt'

#config.Site.whitelist = ['T2_CH_CSCS','T2_US_MIT','T2_US_Wisconsin','T2_US_Purdue','T2_US_UCSD','T2_US_Florida','T2_US_Caltech','T1_US_FNAL','T2_US_Nebraska']

#config.Data.lumiMask = 'lumi_mask_JSON.txt'
#config.Site.blacklist = ['T2_PT_NCG_Lisbon ']
