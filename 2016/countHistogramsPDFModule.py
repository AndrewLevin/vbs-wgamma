import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class countHistogramsPDFProducer(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.h_nweightedevents_pdfweight1=ROOT.TH1D('nWeightedEvents_PDFWeight1',   'nWeightedEvents_PDFWeight1',   1, 0, 1)
        self.h_nweightedevents_pdfweight2=ROOT.TH1D('nWeightedEvents_PDFWeight2',   'nWeightedEvents_PDFWeight2',   1, 0, 1)
        self.h_nweightedevents_pdfweight3=ROOT.TH1D('nWeightedEvents_PDFWeight3',   'nWeightedEvents_PDFWeight3',   1, 0, 1)
        self.h_nweightedevents_pdfweight4=ROOT.TH1D('nWeightedEvents_PDFWeight4',   'nWeightedEvents_PDFWeight4',   1, 0, 1)
        self.h_nweightedevents_pdfweight5=ROOT.TH1D('nWeightedEvents_PDFWeight5',   'nWeightedEvents_PDFWeight5',   1, 0, 1)
        self.h_nweightedevents_pdfweight6=ROOT.TH1D('nWeightedEvents_PDFWeight6',   'nWeightedEvents_PDFWeight6',   1, 0, 1)
        self.h_nweightedevents_pdfweight7=ROOT.TH1D('nWeightedEvents_PDFWeight7',   'nWeightedEvents_PDFWeight7',   1, 0, 1)
        self.h_nweightedevents_pdfweight8=ROOT.TH1D('nWeightedEvents_PDFWeight8',   'nWeightedEvents_PDFWeight8',   1, 0, 1)
        self.h_nweightedevents_pdfweight9=ROOT.TH1D('nWeightedEvents_PDFWeight9',   'nWeightedEvents_PDFWeight9',   1, 0, 1)
        self.h_nweightedevents_pdfweight10=ROOT.TH1D('nWeightedEvents_PDFWeight10',   'nWeightedEvents_PDFWeight10',   1, 0, 1)
        self.h_nweightedevents_pdfweight11=ROOT.TH1D('nWeightedEvents_PDFWeight11',   'nWeightedEvents_PDFWeight11',   1, 0, 1)
        self.h_nweightedevents_pdfweight12=ROOT.TH1D('nWeightedEvents_PDFWeight12',   'nWeightedEvents_PDFWeight12',   1, 0, 1)
        self.h_nweightedevents_pdfweight13=ROOT.TH1D('nWeightedEvents_PDFWeight13',   'nWeightedEvents_PDFWeight13',   1, 0, 1)
        self.h_nweightedevents_pdfweight14=ROOT.TH1D('nWeightedEvents_PDFWeight14',   'nWeightedEvents_PDFWeight14',   1, 0, 1)
        self.h_nweightedevents_pdfweight15=ROOT.TH1D('nWeightedEvents_PDFWeight15',   'nWeightedEvents_PDFWeight15',   1, 0, 1)
        self.h_nweightedevents_pdfweight16=ROOT.TH1D('nWeightedEvents_PDFWeight16',   'nWeightedEvents_PDFWeight16',   1, 0, 1)
        self.h_nweightedevents_pdfweight17=ROOT.TH1D('nWeightedEvents_PDFWeight17',   'nWeightedEvents_PDFWeight17',   1, 0, 1)
        self.h_nweightedevents_pdfweight18=ROOT.TH1D('nWeightedEvents_PDFWeight18',   'nWeightedEvents_PDFWeight18',   1, 0, 1)
        self.h_nweightedevents_pdfweight19=ROOT.TH1D('nWeightedEvents_PDFWeight19',   'nWeightedEvents_PDFWeight19',   1, 0, 1)
        self.h_nweightedevents_pdfweight20=ROOT.TH1D('nWeightedEvents_PDFWeight20',   'nWeightedEvents_PDFWeight20',   1, 0, 1)
        self.h_nweightedevents_pdfweight21=ROOT.TH1D('nWeightedEvents_PDFWeight21',   'nWeightedEvents_PDFWeight21',   1, 0, 1)
        self.h_nweightedevents_pdfweight22=ROOT.TH1D('nWeightedEvents_PDFWeight22',   'nWeightedEvents_PDFWeight22',   1, 0, 1)
        self.h_nweightedevents_pdfweight23=ROOT.TH1D('nWeightedEvents_PDFWeight23',   'nWeightedEvents_PDFWeight23',   1, 0, 1)
        self.h_nweightedevents_pdfweight24=ROOT.TH1D('nWeightedEvents_PDFWeight24',   'nWeightedEvents_PDFWeight24',   1, 0, 1)
        self.h_nweightedevents_pdfweight25=ROOT.TH1D('nWeightedEvents_PDFWeight25',   'nWeightedEvents_PDFWeight25',   1, 0, 1)
        self.h_nweightedevents_pdfweight26=ROOT.TH1D('nWeightedEvents_PDFWeight26',   'nWeightedEvents_PDFWeight26',   1, 0, 1)
        self.h_nweightedevents_pdfweight27=ROOT.TH1D('nWeightedEvents_PDFWeight27',   'nWeightedEvents_PDFWeight27',   1, 0, 1)
        self.h_nweightedevents_pdfweight28=ROOT.TH1D('nWeightedEvents_PDFWeight28',   'nWeightedEvents_PDFWeight28',   1, 0, 1)
        self.h_nweightedevents_pdfweight29=ROOT.TH1D('nWeightedEvents_PDFWeight29',   'nWeightedEvents_PDFWeight29',   1, 0, 1)
        self.h_nweightedevents_pdfweight30=ROOT.TH1D('nWeightedEvents_PDFWeight30',   'nWeightedEvents_PDFWeight30',   1, 0, 1)
        self.h_nweightedevents_pdfweight31=ROOT.TH1D('nWeightedEvents_PDFWeight31',   'nWeightedEvents_PDFWeight31',   1, 0, 1)
        self.h_nweightedevents_pdfweight32=ROOT.TH1D('nWeightedEvents_PDFWeight32',   'nWeightedEvents_PDFWeight32',   1, 0, 1)
        self.h_nweightedevents_pdfweight33=ROOT.TH1D('nWeightedEvents_PDFWeight33',   'nWeightedEvents_PDFWeight33',   1, 0, 1)
        self.h_nweightedevents_pdfweight34=ROOT.TH1D('nWeightedEvents_PDFWeight34',   'nWeightedEvents_PDFWeight34',   1, 0, 1)
        self.h_nweightedevents_pdfweight35=ROOT.TH1D('nWeightedEvents_PDFWeight35',   'nWeightedEvents_PDFWeight35',   1, 0, 1)
        self.h_nweightedevents_pdfweight36=ROOT.TH1D('nWeightedEvents_PDFWeight36',   'nWeightedEvents_PDFWeight36',   1, 0, 1)
        self.h_nweightedevents_pdfweight37=ROOT.TH1D('nWeightedEvents_PDFWeight37',   'nWeightedEvents_PDFWeight37',   1, 0, 1)
        self.h_nweightedevents_pdfweight38=ROOT.TH1D('nWeightedEvents_PDFWeight38',   'nWeightedEvents_PDFWeight38',   1, 0, 1)
        self.h_nweightedevents_pdfweight39=ROOT.TH1D('nWeightedEvents_PDFWeight39',   'nWeightedEvents_PDFWeight39',   1, 0, 1)
        self.h_nweightedevents_pdfweight40=ROOT.TH1D('nWeightedEvents_PDFWeight40',   'nWeightedEvents_PDFWeight40',   1, 0, 1)
        self.h_nweightedevents_pdfweight41=ROOT.TH1D('nWeightedEvents_PDFWeight41',   'nWeightedEvents_PDFWeight41',   1, 0, 1)
        self.h_nweightedevents_pdfweight42=ROOT.TH1D('nWeightedEvents_PDFWeight42',   'nWeightedEvents_PDFWeight42',   1, 0, 1)
        self.h_nweightedevents_pdfweight43=ROOT.TH1D('nWeightedEvents_PDFWeight43',   'nWeightedEvents_PDFWeight43',   1, 0, 1)
        self.h_nweightedevents_pdfweight44=ROOT.TH1D('nWeightedEvents_PDFWeight44',   'nWeightedEvents_PDFWeight44',   1, 0, 1)
        self.h_nweightedevents_pdfweight45=ROOT.TH1D('nWeightedEvents_PDFWeight45',   'nWeightedEvents_PDFWeight45',   1, 0, 1)
        self.h_nweightedevents_pdfweight46=ROOT.TH1D('nWeightedEvents_PDFWeight46',   'nWeightedEvents_PDFWeight46',   1, 0, 1)
        self.h_nweightedevents_pdfweight47=ROOT.TH1D('nWeightedEvents_PDFWeight47',   'nWeightedEvents_PDFWeight47',   1, 0, 1)
        self.h_nweightedevents_pdfweight48=ROOT.TH1D('nWeightedEvents_PDFWeight48',   'nWeightedEvents_PDFWeight48',   1, 0, 1)
        self.h_nweightedevents_pdfweight49=ROOT.TH1D('nWeightedEvents_PDFWeight49',   'nWeightedEvents_PDFWeight49',   1, 0, 1)
        self.h_nweightedevents_pdfweight50=ROOT.TH1D('nWeightedEvents_PDFWeight50',   'nWeightedEvents_PDFWeight50',   1, 0, 1)
        self.h_nweightedevents_pdfweight51=ROOT.TH1D('nWeightedEvents_PDFWeight51',   'nWeightedEvents_PDFWeight51',   1, 0, 1)
        self.h_nweightedevents_pdfweight52=ROOT.TH1D('nWeightedEvents_PDFWeight52',   'nWeightedEvents_PDFWeight52',   1, 0, 1)
        self.h_nweightedevents_pdfweight53=ROOT.TH1D('nWeightedEvents_PDFWeight53',   'nWeightedEvents_PDFWeight53',   1, 0, 1)
        self.h_nweightedevents_pdfweight54=ROOT.TH1D('nWeightedEvents_PDFWeight54',   'nWeightedEvents_PDFWeight54',   1, 0, 1)
        self.h_nweightedevents_pdfweight55=ROOT.TH1D('nWeightedEvents_PDFWeight55',   'nWeightedEvents_PDFWeight55',   1, 0, 1)
        self.h_nweightedevents_pdfweight56=ROOT.TH1D('nWeightedEvents_PDFWeight56',   'nWeightedEvents_PDFWeight56',   1, 0, 1)
        self.h_nweightedevents_pdfweight57=ROOT.TH1D('nWeightedEvents_PDFWeight57',   'nWeightedEvents_PDFWeight57',   1, 0, 1)
        self.h_nweightedevents_pdfweight58=ROOT.TH1D('nWeightedEvents_PDFWeight58',   'nWeightedEvents_PDFWeight58',   1, 0, 1)
        self.h_nweightedevents_pdfweight59=ROOT.TH1D('nWeightedEvents_PDFWeight59',   'nWeightedEvents_PDFWeight59',   1, 0, 1)
        self.h_nweightedevents_pdfweight60=ROOT.TH1D('nWeightedEvents_PDFWeight60',   'nWeightedEvents_PDFWeight60',   1, 0, 1)
        self.h_nweightedevents_pdfweight61=ROOT.TH1D('nWeightedEvents_PDFWeight61',   'nWeightedEvents_PDFWeight61',   1, 0, 1)
        self.h_nweightedevents_pdfweight62=ROOT.TH1D('nWeightedEvents_PDFWeight62',   'nWeightedEvents_PDFWeight62',   1, 0, 1)
        self.h_nweightedevents_pdfweight63=ROOT.TH1D('nWeightedEvents_PDFWeight63',   'nWeightedEvents_PDFWeight63',   1, 0, 1)
        self.h_nweightedevents_pdfweight64=ROOT.TH1D('nWeightedEvents_PDFWeight64',   'nWeightedEvents_PDFWeight64',   1, 0, 1)
        self.h_nweightedevents_pdfweight65=ROOT.TH1D('nWeightedEvents_PDFWeight65',   'nWeightedEvents_PDFWeight65',   1, 0, 1)
        self.h_nweightedevents_pdfweight66=ROOT.TH1D('nWeightedEvents_PDFWeight66',   'nWeightedEvents_PDFWeight66',   1, 0, 1)
        self.h_nweightedevents_pdfweight67=ROOT.TH1D('nWeightedEvents_PDFWeight67',   'nWeightedEvents_PDFWeight67',   1, 0, 1)
        self.h_nweightedevents_pdfweight68=ROOT.TH1D('nWeightedEvents_PDFWeight68',   'nWeightedEvents_PDFWeight68',   1, 0, 1)
        self.h_nweightedevents_pdfweight69=ROOT.TH1D('nWeightedEvents_PDFWeight69',   'nWeightedEvents_PDFWeight69',   1, 0, 1)
        self.h_nweightedevents_pdfweight70=ROOT.TH1D('nWeightedEvents_PDFWeight70',   'nWeightedEvents_PDFWeight70',   1, 0, 1)
        self.h_nweightedevents_pdfweight71=ROOT.TH1D('nWeightedEvents_PDFWeight71',   'nWeightedEvents_PDFWeight71',   1, 0, 1)
        self.h_nweightedevents_pdfweight72=ROOT.TH1D('nWeightedEvents_PDFWeight72',   'nWeightedEvents_PDFWeight72',   1, 0, 1)
        self.h_nweightedevents_pdfweight73=ROOT.TH1D('nWeightedEvents_PDFWeight73',   'nWeightedEvents_PDFWeight73',   1, 0, 1)
        self.h_nweightedevents_pdfweight74=ROOT.TH1D('nWeightedEvents_PDFWeight74',   'nWeightedEvents_PDFWeight74',   1, 0, 1)
        self.h_nweightedevents_pdfweight75=ROOT.TH1D('nWeightedEvents_PDFWeight75',   'nWeightedEvents_PDFWeight75',   1, 0, 1)
        self.h_nweightedevents_pdfweight76=ROOT.TH1D('nWeightedEvents_PDFWeight76',   'nWeightedEvents_PDFWeight76',   1, 0, 1)
        self.h_nweightedevents_pdfweight77=ROOT.TH1D('nWeightedEvents_PDFWeight77',   'nWeightedEvents_PDFWeight77',   1, 0, 1)
        self.h_nweightedevents_pdfweight78=ROOT.TH1D('nWeightedEvents_PDFWeight78',   'nWeightedEvents_PDFWeight78',   1, 0, 1)
        self.h_nweightedevents_pdfweight79=ROOT.TH1D('nWeightedEvents_PDFWeight79',   'nWeightedEvents_PDFWeight79',   1, 0, 1)
        self.h_nweightedevents_pdfweight80=ROOT.TH1D('nWeightedEvents_PDFWeight80',   'nWeightedEvents_PDFWeight80',   1, 0, 1)
        self.h_nweightedevents_pdfweight81=ROOT.TH1D('nWeightedEvents_PDFWeight81',   'nWeightedEvents_PDFWeight81',   1, 0, 1)
        self.h_nweightedevents_pdfweight82=ROOT.TH1D('nWeightedEvents_PDFWeight82',   'nWeightedEvents_PDFWeight82',   1, 0, 1)
        self.h_nweightedevents_pdfweight83=ROOT.TH1D('nWeightedEvents_PDFWeight83',   'nWeightedEvents_PDFWeight83',   1, 0, 1)
        self.h_nweightedevents_pdfweight84=ROOT.TH1D('nWeightedEvents_PDFWeight84',   'nWeightedEvents_PDFWeight84',   1, 0, 1)
        self.h_nweightedevents_pdfweight85=ROOT.TH1D('nWeightedEvents_PDFWeight85',   'nWeightedEvents_PDFWeight85',   1, 0, 1)
        self.h_nweightedevents_pdfweight86=ROOT.TH1D('nWeightedEvents_PDFWeight86',   'nWeightedEvents_PDFWeight86',   1, 0, 1)
        self.h_nweightedevents_pdfweight87=ROOT.TH1D('nWeightedEvents_PDFWeight87',   'nWeightedEvents_PDFWeight87',   1, 0, 1)
        self.h_nweightedevents_pdfweight88=ROOT.TH1D('nWeightedEvents_PDFWeight88',   'nWeightedEvents_PDFWeight88',   1, 0, 1)
        self.h_nweightedevents_pdfweight89=ROOT.TH1D('nWeightedEvents_PDFWeight89',   'nWeightedEvents_PDFWeight89',   1, 0, 1)
        self.h_nweightedevents_pdfweight90=ROOT.TH1D('nWeightedEvents_PDFWeight90',   'nWeightedEvents_PDFWeight90',   1, 0, 1)
        self.h_nweightedevents_pdfweight91=ROOT.TH1D('nWeightedEvents_PDFWeight91',   'nWeightedEvents_PDFWeight91',   1, 0, 1)
        self.h_nweightedevents_pdfweight92=ROOT.TH1D('nWeightedEvents_PDFWeight92',   'nWeightedEvents_PDFWeight92',   1, 0, 1)
        self.h_nweightedevents_pdfweight93=ROOT.TH1D('nWeightedEvents_PDFWeight93',   'nWeightedEvents_PDFWeight93',   1, 0, 1)
        self.h_nweightedevents_pdfweight94=ROOT.TH1D('nWeightedEvents_PDFWeight94',   'nWeightedEvents_PDFWeight94',   1, 0, 1)
        self.h_nweightedevents_pdfweight95=ROOT.TH1D('nWeightedEvents_PDFWeight95',   'nWeightedEvents_PDFWeight95',   1, 0, 1)
        self.h_nweightedevents_pdfweight96=ROOT.TH1D('nWeightedEvents_PDFWeight96',   'nWeightedEvents_PDFWeight96',   1, 0, 1)
        self.h_nweightedevents_pdfweight97=ROOT.TH1D('nWeightedEvents_PDFWeight97',   'nWeightedEvents_PDFWeight97',   1, 0, 1)
        self.h_nweightedevents_pdfweight98=ROOT.TH1D('nWeightedEvents_PDFWeight98',   'nWeightedEvents_PDFWeight98',   1, 0, 1)
        self.h_nweightedevents_pdfweight99=ROOT.TH1D('nWeightedEvents_PDFWeight99',   'nWeightedEvents_PDFWeight99',   1, 0, 1)
        self.h_nweightedevents_pdfweight100=ROOT.TH1D('nWeightedEvents_PDFWeight100',   'nWeightedEvents_PDFWeight100',   1, 0, 1)
        self.h_nweightedevents_pdfweight101=ROOT.TH1D('nWeightedEvents_PDFWeight101',   'nWeightedEvents_PDFWeight101',   1, 0, 1)
        self.h_nweightedevents_pdfweight102=ROOT.TH1D('nWeightedEvents_PDFWeight102',   'nWeightedEvents_PDFWeight102',   1, 0, 1)

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        prevdir = ROOT.gDirectory
        outputFile.cd()
        self.h_nweightedevents_pdfweight1.Write()
        self.h_nweightedevents_pdfweight2.Write()
        self.h_nweightedevents_pdfweight3.Write()
        self.h_nweightedevents_pdfweight4.Write()
        self.h_nweightedevents_pdfweight5.Write()
        self.h_nweightedevents_pdfweight6.Write()
        self.h_nweightedevents_pdfweight7.Write()
        self.h_nweightedevents_pdfweight8.Write()
        self.h_nweightedevents_pdfweight9.Write()
        self.h_nweightedevents_pdfweight10.Write()
        self.h_nweightedevents_pdfweight11.Write()
        self.h_nweightedevents_pdfweight12.Write()
        self.h_nweightedevents_pdfweight13.Write()
        self.h_nweightedevents_pdfweight14.Write()
        self.h_nweightedevents_pdfweight15.Write()
        self.h_nweightedevents_pdfweight16.Write()
        self.h_nweightedevents_pdfweight17.Write()
        self.h_nweightedevents_pdfweight18.Write()
        self.h_nweightedevents_pdfweight19.Write()
        self.h_nweightedevents_pdfweight20.Write()
        self.h_nweightedevents_pdfweight21.Write()
        self.h_nweightedevents_pdfweight22.Write()
        self.h_nweightedevents_pdfweight23.Write()
        self.h_nweightedevents_pdfweight24.Write()
        self.h_nweightedevents_pdfweight25.Write()
        self.h_nweightedevents_pdfweight26.Write()
        self.h_nweightedevents_pdfweight27.Write()
        self.h_nweightedevents_pdfweight28.Write()
        self.h_nweightedevents_pdfweight29.Write()
        self.h_nweightedevents_pdfweight30.Write()
        self.h_nweightedevents_pdfweight31.Write()
        self.h_nweightedevents_pdfweight32.Write()
        self.h_nweightedevents_pdfweight33.Write()
        self.h_nweightedevents_pdfweight34.Write()
        self.h_nweightedevents_pdfweight35.Write()
        self.h_nweightedevents_pdfweight36.Write()
        self.h_nweightedevents_pdfweight37.Write()
        self.h_nweightedevents_pdfweight38.Write()
        self.h_nweightedevents_pdfweight39.Write()
        self.h_nweightedevents_pdfweight40.Write()
        self.h_nweightedevents_pdfweight41.Write()
        self.h_nweightedevents_pdfweight42.Write()
        self.h_nweightedevents_pdfweight43.Write()
        self.h_nweightedevents_pdfweight44.Write()
        self.h_nweightedevents_pdfweight45.Write()
        self.h_nweightedevents_pdfweight46.Write()
        self.h_nweightedevents_pdfweight47.Write()
        self.h_nweightedevents_pdfweight48.Write()
        self.h_nweightedevents_pdfweight49.Write()
        self.h_nweightedevents_pdfweight50.Write()
        self.h_nweightedevents_pdfweight51.Write()
        self.h_nweightedevents_pdfweight52.Write()
        self.h_nweightedevents_pdfweight53.Write()
        self.h_nweightedevents_pdfweight54.Write()
        self.h_nweightedevents_pdfweight55.Write()
        self.h_nweightedevents_pdfweight56.Write()
        self.h_nweightedevents_pdfweight57.Write()
        self.h_nweightedevents_pdfweight58.Write()
        self.h_nweightedevents_pdfweight59.Write()
        self.h_nweightedevents_pdfweight60.Write()
        self.h_nweightedevents_pdfweight61.Write()
        self.h_nweightedevents_pdfweight62.Write()
        self.h_nweightedevents_pdfweight63.Write()
        self.h_nweightedevents_pdfweight64.Write()
        self.h_nweightedevents_pdfweight65.Write()
        self.h_nweightedevents_pdfweight66.Write()
        self.h_nweightedevents_pdfweight67.Write()
        self.h_nweightedevents_pdfweight68.Write()
        self.h_nweightedevents_pdfweight69.Write()
        self.h_nweightedevents_pdfweight70.Write()
        self.h_nweightedevents_pdfweight71.Write()
        self.h_nweightedevents_pdfweight72.Write()
        self.h_nweightedevents_pdfweight73.Write()
        self.h_nweightedevents_pdfweight74.Write()
        self.h_nweightedevents_pdfweight75.Write()
        self.h_nweightedevents_pdfweight76.Write()
        self.h_nweightedevents_pdfweight77.Write()
        self.h_nweightedevents_pdfweight78.Write()
        self.h_nweightedevents_pdfweight79.Write()
        self.h_nweightedevents_pdfweight80.Write()
        self.h_nweightedevents_pdfweight81.Write()
        self.h_nweightedevents_pdfweight82.Write()
        self.h_nweightedevents_pdfweight83.Write()
        self.h_nweightedevents_pdfweight84.Write()
        self.h_nweightedevents_pdfweight85.Write()
        self.h_nweightedevents_pdfweight86.Write()
        self.h_nweightedevents_pdfweight87.Write()
        self.h_nweightedevents_pdfweight88.Write()
        self.h_nweightedevents_pdfweight89.Write()
        self.h_nweightedevents_pdfweight90.Write()
        self.h_nweightedevents_pdfweight91.Write()
        self.h_nweightedevents_pdfweight92.Write()
        self.h_nweightedevents_pdfweight93.Write()
        self.h_nweightedevents_pdfweight94.Write()
        self.h_nweightedevents_pdfweight95.Write()
        self.h_nweightedevents_pdfweight96.Write()
        self.h_nweightedevents_pdfweight97.Write()
        self.h_nweightedevents_pdfweight98.Write()
        self.h_nweightedevents_pdfweight99.Write()
        self.h_nweightedevents_pdfweight100.Write()
        self.h_nweightedevents_pdfweight101.Write()
        self.h_nweightedevents_pdfweight102.Write()
        prevdir.cd()        
    def analyze(self, event):
        try:
            if event.Generator_weight > 0:
                self.h_nweightedevents_pdfweight1.Fill(0.5,event.LHEPdfWeight[1]*2)
                self.h_nweightedevents_pdfweight2.Fill(0.5,event.LHEPdfWeight[2]*2)
                self.h_nweightedevents_pdfweight3.Fill(0.5,event.LHEPdfWeight[3]*2)
                self.h_nweightedevents_pdfweight4.Fill(0.5,event.LHEPdfWeight[4]*2)
                self.h_nweightedevents_pdfweight5.Fill(0.5,event.LHEPdfWeight[5]*2)
                self.h_nweightedevents_pdfweight6.Fill(0.5,event.LHEPdfWeight[6]*2)
                self.h_nweightedevents_pdfweight7.Fill(0.5,event.LHEPdfWeight[7]*2)
                self.h_nweightedevents_pdfweight8.Fill(0.5,event.LHEPdfWeight[8]*2)
                self.h_nweightedevents_pdfweight9.Fill(0.5,event.LHEPdfWeight[9]*2)
                self.h_nweightedevents_pdfweight10.Fill(0.5,event.LHEPdfWeight[10]*2)
                self.h_nweightedevents_pdfweight11.Fill(0.5,event.LHEPdfWeight[11]*2)
                self.h_nweightedevents_pdfweight12.Fill(0.5,event.LHEPdfWeight[12]*2)
                self.h_nweightedevents_pdfweight13.Fill(0.5,event.LHEPdfWeight[13]*2)
                self.h_nweightedevents_pdfweight14.Fill(0.5,event.LHEPdfWeight[14]*2)
                self.h_nweightedevents_pdfweight15.Fill(0.5,event.LHEPdfWeight[15]*2)
                self.h_nweightedevents_pdfweight16.Fill(0.5,event.LHEPdfWeight[16]*2)
                self.h_nweightedevents_pdfweight17.Fill(0.5,event.LHEPdfWeight[17]*2)
                self.h_nweightedevents_pdfweight18.Fill(0.5,event.LHEPdfWeight[18]*2)
                self.h_nweightedevents_pdfweight19.Fill(0.5,event.LHEPdfWeight[19]*2)
                self.h_nweightedevents_pdfweight20.Fill(0.5,event.LHEPdfWeight[20]*2)
                self.h_nweightedevents_pdfweight21.Fill(0.5,event.LHEPdfWeight[21]*2)
                self.h_nweightedevents_pdfweight22.Fill(0.5,event.LHEPdfWeight[22]*2)
                self.h_nweightedevents_pdfweight23.Fill(0.5,event.LHEPdfWeight[23]*2)
                self.h_nweightedevents_pdfweight24.Fill(0.5,event.LHEPdfWeight[24]*2)
                self.h_nweightedevents_pdfweight25.Fill(0.5,event.LHEPdfWeight[25]*2)
                self.h_nweightedevents_pdfweight26.Fill(0.5,event.LHEPdfWeight[26]*2)
                self.h_nweightedevents_pdfweight27.Fill(0.5,event.LHEPdfWeight[27]*2)
                self.h_nweightedevents_pdfweight28.Fill(0.5,event.LHEPdfWeight[28]*2)
                self.h_nweightedevents_pdfweight29.Fill(0.5,event.LHEPdfWeight[29]*2)
                self.h_nweightedevents_pdfweight30.Fill(0.5,event.LHEPdfWeight[30]*2)
                self.h_nweightedevents_pdfweight31.Fill(0.5,event.LHEPdfWeight[31]*2)
                self.h_nweightedevents_pdfweight32.Fill(0.5,event.LHEPdfWeight[32]*2)
                self.h_nweightedevents_pdfweight33.Fill(0.5,event.LHEPdfWeight[33]*2)
                self.h_nweightedevents_pdfweight34.Fill(0.5,event.LHEPdfWeight[34]*2)
                self.h_nweightedevents_pdfweight35.Fill(0.5,event.LHEPdfWeight[35]*2)
                self.h_nweightedevents_pdfweight36.Fill(0.5,event.LHEPdfWeight[36]*2)
                self.h_nweightedevents_pdfweight37.Fill(0.5,event.LHEPdfWeight[37]*2)
                self.h_nweightedevents_pdfweight38.Fill(0.5,event.LHEPdfWeight[38]*2)
                self.h_nweightedevents_pdfweight39.Fill(0.5,event.LHEPdfWeight[39]*2)
                self.h_nweightedevents_pdfweight40.Fill(0.5,event.LHEPdfWeight[40]*2)
                self.h_nweightedevents_pdfweight41.Fill(0.5,event.LHEPdfWeight[41]*2)
                self.h_nweightedevents_pdfweight42.Fill(0.5,event.LHEPdfWeight[42]*2)
                self.h_nweightedevents_pdfweight43.Fill(0.5,event.LHEPdfWeight[43]*2)
                self.h_nweightedevents_pdfweight44.Fill(0.5,event.LHEPdfWeight[44]*2)
                self.h_nweightedevents_pdfweight45.Fill(0.5,event.LHEPdfWeight[45]*2)
                self.h_nweightedevents_pdfweight46.Fill(0.5,event.LHEPdfWeight[46]*2)
                self.h_nweightedevents_pdfweight47.Fill(0.5,event.LHEPdfWeight[47]*2)
                self.h_nweightedevents_pdfweight48.Fill(0.5,event.LHEPdfWeight[48]*2)
                self.h_nweightedevents_pdfweight49.Fill(0.5,event.LHEPdfWeight[49]*2)
                self.h_nweightedevents_pdfweight50.Fill(0.5,event.LHEPdfWeight[50]*2)
                self.h_nweightedevents_pdfweight51.Fill(0.5,event.LHEPdfWeight[51]*2)
                self.h_nweightedevents_pdfweight52.Fill(0.5,event.LHEPdfWeight[52]*2)
                self.h_nweightedevents_pdfweight53.Fill(0.5,event.LHEPdfWeight[53]*2)
                self.h_nweightedevents_pdfweight54.Fill(0.5,event.LHEPdfWeight[54]*2)
                self.h_nweightedevents_pdfweight55.Fill(0.5,event.LHEPdfWeight[55]*2)
                self.h_nweightedevents_pdfweight56.Fill(0.5,event.LHEPdfWeight[56]*2)
                self.h_nweightedevents_pdfweight57.Fill(0.5,event.LHEPdfWeight[57]*2)
                self.h_nweightedevents_pdfweight58.Fill(0.5,event.LHEPdfWeight[58]*2)
                self.h_nweightedevents_pdfweight59.Fill(0.5,event.LHEPdfWeight[59]*2)
                self.h_nweightedevents_pdfweight60.Fill(0.5,event.LHEPdfWeight[60]*2)
                self.h_nweightedevents_pdfweight61.Fill(0.5,event.LHEPdfWeight[61]*2)
                self.h_nweightedevents_pdfweight62.Fill(0.5,event.LHEPdfWeight[62]*2)
                self.h_nweightedevents_pdfweight63.Fill(0.5,event.LHEPdfWeight[63]*2)
                self.h_nweightedevents_pdfweight64.Fill(0.5,event.LHEPdfWeight[64]*2)
                self.h_nweightedevents_pdfweight65.Fill(0.5,event.LHEPdfWeight[65]*2)
                self.h_nweightedevents_pdfweight66.Fill(0.5,event.LHEPdfWeight[66]*2)
                self.h_nweightedevents_pdfweight67.Fill(0.5,event.LHEPdfWeight[67]*2)
                self.h_nweightedevents_pdfweight68.Fill(0.5,event.LHEPdfWeight[68]*2)
                self.h_nweightedevents_pdfweight69.Fill(0.5,event.LHEPdfWeight[69]*2)
                self.h_nweightedevents_pdfweight70.Fill(0.5,event.LHEPdfWeight[70]*2)
                self.h_nweightedevents_pdfweight71.Fill(0.5,event.LHEPdfWeight[71]*2)
                self.h_nweightedevents_pdfweight72.Fill(0.5,event.LHEPdfWeight[72]*2)
                self.h_nweightedevents_pdfweight73.Fill(0.5,event.LHEPdfWeight[73]*2)
                self.h_nweightedevents_pdfweight74.Fill(0.5,event.LHEPdfWeight[74]*2)
                self.h_nweightedevents_pdfweight75.Fill(0.5,event.LHEPdfWeight[75]*2)
                self.h_nweightedevents_pdfweight76.Fill(0.5,event.LHEPdfWeight[76]*2)
                self.h_nweightedevents_pdfweight77.Fill(0.5,event.LHEPdfWeight[77]*2)
                self.h_nweightedevents_pdfweight78.Fill(0.5,event.LHEPdfWeight[78]*2)
                self.h_nweightedevents_pdfweight79.Fill(0.5,event.LHEPdfWeight[79]*2)
                self.h_nweightedevents_pdfweight80.Fill(0.5,event.LHEPdfWeight[80]*2)
                self.h_nweightedevents_pdfweight81.Fill(0.5,event.LHEPdfWeight[81]*2)
                self.h_nweightedevents_pdfweight82.Fill(0.5,event.LHEPdfWeight[82]*2)
                self.h_nweightedevents_pdfweight83.Fill(0.5,event.LHEPdfWeight[83]*2)
                self.h_nweightedevents_pdfweight84.Fill(0.5,event.LHEPdfWeight[84]*2)
                self.h_nweightedevents_pdfweight85.Fill(0.5,event.LHEPdfWeight[85]*2)
                self.h_nweightedevents_pdfweight86.Fill(0.5,event.LHEPdfWeight[86]*2)
                self.h_nweightedevents_pdfweight87.Fill(0.5,event.LHEPdfWeight[87]*2)
                self.h_nweightedevents_pdfweight88.Fill(0.5,event.LHEPdfWeight[88]*2)
                self.h_nweightedevents_pdfweight89.Fill(0.5,event.LHEPdfWeight[89]*2)
                self.h_nweightedevents_pdfweight90.Fill(0.5,event.LHEPdfWeight[90]*2)
                self.h_nweightedevents_pdfweight91.Fill(0.5,event.LHEPdfWeight[91]*2)
                self.h_nweightedevents_pdfweight92.Fill(0.5,event.LHEPdfWeight[92]*2)
                self.h_nweightedevents_pdfweight93.Fill(0.5,event.LHEPdfWeight[93]*2)
                self.h_nweightedevents_pdfweight94.Fill(0.5,event.LHEPdfWeight[94]*2)
                self.h_nweightedevents_pdfweight95.Fill(0.5,event.LHEPdfWeight[95]*2)
                self.h_nweightedevents_pdfweight96.Fill(0.5,event.LHEPdfWeight[96]*2)
                self.h_nweightedevents_pdfweight97.Fill(0.5,event.LHEPdfWeight[97]*2)
                self.h_nweightedevents_pdfweight98.Fill(0.5,event.LHEPdfWeight[98]*2)
                self.h_nweightedevents_pdfweight99.Fill(0.5,event.LHEPdfWeight[99]*2)
                self.h_nweightedevents_pdfweight100.Fill(0.5,event.LHEPdfWeight[100]*2)
                self.h_nweightedevents_pdfweight101.Fill(0.5,event.LHEPdfWeight[101]*2)
                self.h_nweightedevents_pdfweight102.Fill(0.5,event.LHEPdfWeight[102]*2)
            else:
                self.h_nweightedevents_pdfweight1.Fill(0.5,-event.LHEPdfWeight[1]*2)
                self.h_nweightedevents_pdfweight2.Fill(0.5,-event.LHEPdfWeight[2]*2)
                self.h_nweightedevents_pdfweight3.Fill(0.5,-event.LHEPdfWeight[3]*2)
                self.h_nweightedevents_pdfweight4.Fill(0.5,-event.LHEPdfWeight[4]*2)
                self.h_nweightedevents_pdfweight5.Fill(0.5,-event.LHEPdfWeight[5]*2)
                self.h_nweightedevents_pdfweight6.Fill(0.5,-event.LHEPdfWeight[6]*2)
                self.h_nweightedevents_pdfweight7.Fill(0.5,-event.LHEPdfWeight[7]*2)
                self.h_nweightedevents_pdfweight8.Fill(0.5,-event.LHEPdfWeight[8]*2)
                self.h_nweightedevents_pdfweight9.Fill(0.5,-event.LHEPdfWeight[9]*2)
                self.h_nweightedevents_pdfweight10.Fill(0.5,-event.LHEPdfWeight[10]*2)
                self.h_nweightedevents_pdfweight11.Fill(0.5,-event.LHEPdfWeight[11]*2)
                self.h_nweightedevents_pdfweight12.Fill(0.5,-event.LHEPdfWeight[12]*2)
                self.h_nweightedevents_pdfweight13.Fill(0.5,-event.LHEPdfWeight[13]*2)
                self.h_nweightedevents_pdfweight14.Fill(0.5,-event.LHEPdfWeight[14]*2)
                self.h_nweightedevents_pdfweight15.Fill(0.5,-event.LHEPdfWeight[15]*2)
                self.h_nweightedevents_pdfweight16.Fill(0.5,-event.LHEPdfWeight[16]*2)
                self.h_nweightedevents_pdfweight17.Fill(0.5,-event.LHEPdfWeight[17]*2)
                self.h_nweightedevents_pdfweight18.Fill(0.5,-event.LHEPdfWeight[18]*2)
                self.h_nweightedevents_pdfweight19.Fill(0.5,-event.LHEPdfWeight[19]*2)
                self.h_nweightedevents_pdfweight20.Fill(0.5,-event.LHEPdfWeight[20]*2)
                self.h_nweightedevents_pdfweight21.Fill(0.5,-event.LHEPdfWeight[21]*2)
                self.h_nweightedevents_pdfweight22.Fill(0.5,-event.LHEPdfWeight[22]*2)
                self.h_nweightedevents_pdfweight23.Fill(0.5,-event.LHEPdfWeight[23]*2)
                self.h_nweightedevents_pdfweight24.Fill(0.5,-event.LHEPdfWeight[24]*2)
                self.h_nweightedevents_pdfweight25.Fill(0.5,-event.LHEPdfWeight[25]*2)
                self.h_nweightedevents_pdfweight26.Fill(0.5,-event.LHEPdfWeight[26]*2)
                self.h_nweightedevents_pdfweight27.Fill(0.5,-event.LHEPdfWeight[27]*2)
                self.h_nweightedevents_pdfweight28.Fill(0.5,-event.LHEPdfWeight[28]*2)
                self.h_nweightedevents_pdfweight29.Fill(0.5,-event.LHEPdfWeight[29]*2)
                self.h_nweightedevents_pdfweight30.Fill(0.5,-event.LHEPdfWeight[30]*2)
                self.h_nweightedevents_pdfweight31.Fill(0.5,-event.LHEPdfWeight[31]*2)
                self.h_nweightedevents_pdfweight32.Fill(0.5,-event.LHEPdfWeight[32]*2)
                self.h_nweightedevents_pdfweight33.Fill(0.5,-event.LHEPdfWeight[33]*2)
                self.h_nweightedevents_pdfweight34.Fill(0.5,-event.LHEPdfWeight[34]*2)
                self.h_nweightedevents_pdfweight35.Fill(0.5,-event.LHEPdfWeight[35]*2)
                self.h_nweightedevents_pdfweight36.Fill(0.5,-event.LHEPdfWeight[36]*2)
                self.h_nweightedevents_pdfweight37.Fill(0.5,-event.LHEPdfWeight[37]*2)
                self.h_nweightedevents_pdfweight38.Fill(0.5,-event.LHEPdfWeight[38]*2)
                self.h_nweightedevents_pdfweight39.Fill(0.5,-event.LHEPdfWeight[39]*2)
                self.h_nweightedevents_pdfweight40.Fill(0.5,-event.LHEPdfWeight[40]*2)
                self.h_nweightedevents_pdfweight41.Fill(0.5,-event.LHEPdfWeight[41]*2)
                self.h_nweightedevents_pdfweight42.Fill(0.5,-event.LHEPdfWeight[42]*2)
                self.h_nweightedevents_pdfweight43.Fill(0.5,-event.LHEPdfWeight[43]*2)
                self.h_nweightedevents_pdfweight44.Fill(0.5,-event.LHEPdfWeight[44]*2)
                self.h_nweightedevents_pdfweight45.Fill(0.5,-event.LHEPdfWeight[45]*2)
                self.h_nweightedevents_pdfweight46.Fill(0.5,-event.LHEPdfWeight[46]*2)
                self.h_nweightedevents_pdfweight47.Fill(0.5,-event.LHEPdfWeight[47]*2)
                self.h_nweightedevents_pdfweight48.Fill(0.5,-event.LHEPdfWeight[48]*2)
                self.h_nweightedevents_pdfweight49.Fill(0.5,-event.LHEPdfWeight[49]*2)
                self.h_nweightedevents_pdfweight50.Fill(0.5,-event.LHEPdfWeight[50]*2)
                self.h_nweightedevents_pdfweight51.Fill(0.5,-event.LHEPdfWeight[51]*2)
                self.h_nweightedevents_pdfweight52.Fill(0.5,-event.LHEPdfWeight[52]*2)
                self.h_nweightedevents_pdfweight53.Fill(0.5,-event.LHEPdfWeight[53]*2)
                self.h_nweightedevents_pdfweight54.Fill(0.5,-event.LHEPdfWeight[54]*2)
                self.h_nweightedevents_pdfweight55.Fill(0.5,-event.LHEPdfWeight[55]*2)
                self.h_nweightedevents_pdfweight56.Fill(0.5,-event.LHEPdfWeight[56]*2)
                self.h_nweightedevents_pdfweight57.Fill(0.5,-event.LHEPdfWeight[57]*2)
                self.h_nweightedevents_pdfweight58.Fill(0.5,-event.LHEPdfWeight[58]*2)
                self.h_nweightedevents_pdfweight59.Fill(0.5,-event.LHEPdfWeight[59]*2)
                self.h_nweightedevents_pdfweight60.Fill(0.5,-event.LHEPdfWeight[60]*2)
                self.h_nweightedevents_pdfweight61.Fill(0.5,-event.LHEPdfWeight[61]*2)
                self.h_nweightedevents_pdfweight62.Fill(0.5,-event.LHEPdfWeight[62]*2)
                self.h_nweightedevents_pdfweight63.Fill(0.5,-event.LHEPdfWeight[63]*2)
                self.h_nweightedevents_pdfweight64.Fill(0.5,-event.LHEPdfWeight[64]*2)
                self.h_nweightedevents_pdfweight65.Fill(0.5,-event.LHEPdfWeight[65]*2)
                self.h_nweightedevents_pdfweight66.Fill(0.5,-event.LHEPdfWeight[66]*2)
                self.h_nweightedevents_pdfweight67.Fill(0.5,-event.LHEPdfWeight[67]*2)
                self.h_nweightedevents_pdfweight68.Fill(0.5,-event.LHEPdfWeight[68]*2)
                self.h_nweightedevents_pdfweight69.Fill(0.5,-event.LHEPdfWeight[69]*2)
                self.h_nweightedevents_pdfweight70.Fill(0.5,-event.LHEPdfWeight[70]*2)
                self.h_nweightedevents_pdfweight71.Fill(0.5,-event.LHEPdfWeight[71]*2)
                self.h_nweightedevents_pdfweight72.Fill(0.5,-event.LHEPdfWeight[72]*2)
                self.h_nweightedevents_pdfweight73.Fill(0.5,-event.LHEPdfWeight[73]*2)
                self.h_nweightedevents_pdfweight74.Fill(0.5,-event.LHEPdfWeight[74]*2)
                self.h_nweightedevents_pdfweight75.Fill(0.5,-event.LHEPdfWeight[75]*2)
                self.h_nweightedevents_pdfweight76.Fill(0.5,-event.LHEPdfWeight[76]*2)
                self.h_nweightedevents_pdfweight77.Fill(0.5,-event.LHEPdfWeight[77]*2)
                self.h_nweightedevents_pdfweight78.Fill(0.5,-event.LHEPdfWeight[78]*2)
                self.h_nweightedevents_pdfweight79.Fill(0.5,-event.LHEPdfWeight[79]*2)
                self.h_nweightedevents_pdfweight80.Fill(0.5,-event.LHEPdfWeight[80]*2)
                self.h_nweightedevents_pdfweight81.Fill(0.5,-event.LHEPdfWeight[81]*2)
                self.h_nweightedevents_pdfweight82.Fill(0.5,-event.LHEPdfWeight[82]*2)
                self.h_nweightedevents_pdfweight83.Fill(0.5,-event.LHEPdfWeight[83]*2)
                self.h_nweightedevents_pdfweight84.Fill(0.5,-event.LHEPdfWeight[84]*2)
                self.h_nweightedevents_pdfweight85.Fill(0.5,-event.LHEPdfWeight[85]*2)
                self.h_nweightedevents_pdfweight86.Fill(0.5,-event.LHEPdfWeight[86]*2)
                self.h_nweightedevents_pdfweight87.Fill(0.5,-event.LHEPdfWeight[87]*2)
                self.h_nweightedevents_pdfweight88.Fill(0.5,-event.LHEPdfWeight[88]*2)
                self.h_nweightedevents_pdfweight89.Fill(0.5,-event.LHEPdfWeight[89]*2)
                self.h_nweightedevents_pdfweight90.Fill(0.5,-event.LHEPdfWeight[90]*2)
                self.h_nweightedevents_pdfweight91.Fill(0.5,-event.LHEPdfWeight[91]*2)
                self.h_nweightedevents_pdfweight92.Fill(0.5,-event.LHEPdfWeight[92]*2)
                self.h_nweightedevents_pdfweight93.Fill(0.5,-event.LHEPdfWeight[93]*2)
                self.h_nweightedevents_pdfweight94.Fill(0.5,-event.LHEPdfWeight[94]*2)
                self.h_nweightedevents_pdfweight95.Fill(0.5,-event.LHEPdfWeight[95]*2)
                self.h_nweightedevents_pdfweight96.Fill(0.5,-event.LHEPdfWeight[96]*2)
                self.h_nweightedevents_pdfweight97.Fill(0.5,-event.LHEPdfWeight[97]*2)
                self.h_nweightedevents_pdfweight98.Fill(0.5,-event.LHEPdfWeight[98]*2)
                self.h_nweightedevents_pdfweight99.Fill(0.5,-event.LHEPdfWeight[99]*2)
                self.h_nweightedevents_pdfweight100.Fill(0.5,-event.LHEPdfWeight[100]*2)
                self.h_nweightedevents_pdfweight101.Fill(0.5,-event.LHEPdfWeight[101]*2)
                self.h_nweightedevents_pdfweight102.Fill(0.5,-event.LHEPdfWeight[102]*2)
        except:
            pass
        return True

countHistogramsPDFModule = lambda : countHistogramsPDFProducer() 

