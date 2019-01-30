import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class countHistogramsQCDScaleProducer(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.h_nweightedevents_qcdscaleweight0=ROOT.TH1D('nWeightedEvents_QCDScaleWeight0',   'nWeightedEvents_QCDScaleWeight0',   1, 0, 1)
        self.h_nweightedevents_qcdscaleweight1=ROOT.TH1D('nWeightedEvents_QCDScaleWeight1',   'nWeightedEvents_QCDScaleWeight1',   1, 0, 1)
        self.h_nweightedevents_qcdscaleweight2=ROOT.TH1D('nWeightedEvents_QCDScaleWeight2',   'nWeightedEvents_QCDScaleWeight2',   1, 0, 1)
        self.h_nweightedevents_qcdscaleweight3=ROOT.TH1D('nWeightedEvents_QCDScaleWeight3',   'nWeightedEvents_QCDScaleWeight3',   1, 0, 1)
        self.h_nweightedevents_qcdscaleweight4=ROOT.TH1D('nWeightedEvents_QCDScaleWeight4',   'nWeightedEvents_QCDScaleWeight4',   1, 0, 1)
        self.h_nweightedevents_qcdscaleweight5=ROOT.TH1D('nWeightedEvents_QCDScaleWeight5',   'nWeightedEvents_QCDScaleWeight5',   1, 0, 1)
        self.h_nweightedevents_qcdscaleweight6=ROOT.TH1D('nWeightedEvents_QCDScaleWeight6',   'nWeightedEvents_QCDScaleWeight6',   1, 0, 1)
        self.h_nweightedevents_qcdscaleweight7=ROOT.TH1D('nWeightedEvents_QCDScaleWeight7',   'nWeightedEvents_QCDScaleWeight7',   1, 0, 1)

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        prevdir = ROOT.gDirectory
        outputFile.cd()
        self.h_nweightedevents_qcdscaleweight0.Write()
        self.h_nweightedevents_qcdscaleweight1.Write()
        self.h_nweightedevents_qcdscaleweight2.Write()
        self.h_nweightedevents_qcdscaleweight3.Write()
        self.h_nweightedevents_qcdscaleweight4.Write()
        self.h_nweightedevents_qcdscaleweight5.Write()
        self.h_nweightedevents_qcdscaleweight6.Write()
        self.h_nweightedevents_qcdscaleweight7.Write()
        prevdir.cd()        
    def analyze(self, event):
        try:
            if event.Generator_weight > 0:
                self.h_nweightedevents_qcdscaleweight0.Fill(0.5,event.LHEScaleWeight[0]*2)
                self.h_nweightedevents_qcdscaleweight1.Fill(0.5,event.LHEScaleWeight[1]*2)
                self.h_nweightedevents_qcdscaleweight2.Fill(0.5,event.LHEScaleWeight[2]*2)
                self.h_nweightedevents_qcdscaleweight3.Fill(0.5,event.LHEScaleWeight[3]*2)
                self.h_nweightedevents_qcdscaleweight4.Fill(0.5,event.LHEScaleWeight[4]*2)
                self.h_nweightedevents_qcdscaleweight5.Fill(0.5,event.LHEScaleWeight[5]*2)
                self.h_nweightedevents_qcdscaleweight6.Fill(0.5,event.LHEScaleWeight[6]*2)
                self.h_nweightedevents_qcdscaleweight7.Fill(0.5,event.LHEScaleWeight[7]*2)
            else:
                self.h_nweightedevents_qcdscaleweight0.Fill(0.5,-event.LHEScaleWeight[0]*2)
                self.h_nweightedevents_qcdscaleweight1.Fill(0.5,-event.LHEScaleWeight[1]*2)
                self.h_nweightedevents_qcdscaleweight2.Fill(0.5,-event.LHEScaleWeight[2]*2)
                self.h_nweightedevents_qcdscaleweight3.Fill(0.5,-event.LHEScaleWeight[3]*2)
                self.h_nweightedevents_qcdscaleweight4.Fill(0.5,-event.LHEScaleWeight[4]*2)
                self.h_nweightedevents_qcdscaleweight5.Fill(0.5,-event.LHEScaleWeight[5]*2)
                self.h_nweightedevents_qcdscaleweight6.Fill(0.5,-event.LHEScaleWeight[6]*2)
                self.h_nweightedevents_qcdscaleweight7.Fill(0.5,-event.LHEScaleWeight[7]*2)
        except:
            pass

        return True

countHistogramsQCDScaleModule = lambda : countHistogramsQCDScaleProducer() 

