import ROOT

f=ROOT.TFile.Open("for_sync_with_qianming.root")
t=f.Get("Events")

t.SetScanField(0)

t.Scan("run:lumi:event")
