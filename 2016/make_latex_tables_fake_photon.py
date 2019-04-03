import sys
import json

fake_photon_event_weights = json.load(open("fake_photon_event_weights/fake_photon_event_weights_data.txt"))

fake_photon_event_weights_wjets_wgjets_as_data = json.load(open("fake_photon_event_weights/fake_photon_event_weights_wjets_wgjets_as_data.txt"))

fake_photon_event_weights_wjets_wgjets = json.load(open("fake_photon_event_weights/fake_photon_event_weights_wjets_wgjets.txt"))

import pprint

pprint.pprint(fake_photon_event_weights)

print """
\\begin{table}[htbp]
\\begin{center}
\\begin{tabular}{|c|c|c|c|c|}
\\hline
photon $p_T$ bin & muon endcap & electron endcap & muon barrel & electron barrel  \\\\   
\\hline
\\hline
25-30 GeV & %0.3f $\pm$ %0.3f & %0.3f $\pm$ %0.3f & %0.3f $\pm$ %0.3f & %0.3f $\pm$ %0.3f  \\\\   
\\hline
30-40 GeV & %0.3f $\pm$ %0.3f & %0.3f $\pm$ %0.3f & %0.3f $\pm$ %0.3f & %0.3f $\pm$ %0.3f \\\\   
\\hline
40-50 GeV & %0.3f $\pm$ %0.3f & %0.3f $\pm$ %0.3f & %0.3f $\pm$ %0.3f & %0.3f $\pm$ %0.3f \\\\   
\\hline
50-70 GeV & %0.3f $\pm$ %0.3f & %0.3f $\pm$ %0.3f & %0.3f $\pm$ %0.3f & %0.3f $\pm$ %0.3f  \\\\   
\\hline
70-100 GeV & %0.3f $\pm$ %0.3f & %0.3f $\pm$ %0.3f & %0.3f $\pm$ %0.3f & %0.3f $\pm$ %0.3f  \\\\   
\\hline
100-135 GeV & %0.3f $\pm$ %0.3f & %0.3f $\pm$ %0.3f & %0.3f $\pm$ %0.3f & %0.3f $\pm$ %0.3f  \\\\   
\\hline
\\end{tabular}
\\end{center}
\\caption{Fake photon weights calculated from data.}
\\label{tab:fake_photon_event_weights}
\end{table}
"""%(
fake_photon_event_weights["muon_endcap"][0][0],
fake_photon_event_weights["muon_endcap"][0][1],
fake_photon_event_weights["electron_endcap"][0][0],
fake_photon_event_weights["electron_endcap"][0][1],
fake_photon_event_weights["muon_barrel"][0][0],
fake_photon_event_weights["muon_barrel"][0][1],
fake_photon_event_weights["electron_barrel"][0][0],
fake_photon_event_weights["electron_barrel"][0][1],
fake_photon_event_weights["muon_endcap"][1][0],
fake_photon_event_weights["muon_endcap"][1][1],
fake_photon_event_weights["electron_endcap"][1][0],
fake_photon_event_weights["electron_endcap"][1][1],
fake_photon_event_weights["muon_barrel"][1][0],
fake_photon_event_weights["muon_barrel"][1][1],
fake_photon_event_weights["electron_barrel"][1][0],
fake_photon_event_weights["electron_barrel"][1][1],
fake_photon_event_weights["muon_endcap"][2][0],
fake_photon_event_weights["muon_endcap"][2][1],
fake_photon_event_weights["electron_endcap"][2][0],
fake_photon_event_weights["electron_endcap"][2][1],
fake_photon_event_weights["muon_barrel"][2][0],
fake_photon_event_weights["muon_barrel"][2][1],
fake_photon_event_weights["electron_barrel"][2][0],
fake_photon_event_weights["electron_barrel"][2][1],
fake_photon_event_weights["muon_endcap"][3][0],
fake_photon_event_weights["muon_endcap"][3][1],
fake_photon_event_weights["electron_endcap"][3][0],
fake_photon_event_weights["electron_endcap"][3][1],
fake_photon_event_weights["muon_barrel"][3][0],
fake_photon_event_weights["muon_barrel"][3][1],
fake_photon_event_weights["electron_barrel"][3][0],
fake_photon_event_weights["electron_barrel"][3][1],
fake_photon_event_weights["muon_endcap"][4][0],
fake_photon_event_weights["muon_endcap"][4][1],
fake_photon_event_weights["electron_endcap"][4][0],
fake_photon_event_weights["electron_endcap"][4][1],
fake_photon_event_weights["muon_barrel"][4][0],
fake_photon_event_weights["muon_barrel"][4][1],
fake_photon_event_weights["electron_barrel"][4][0],
fake_photon_event_weights["electron_barrel"][4][1],
fake_photon_event_weights["muon_endcap"][5][0],
fake_photon_event_weights["muon_endcap"][5][1],
fake_photon_event_weights["electron_endcap"][5][0],
fake_photon_event_weights["electron_endcap"][5][1],
fake_photon_event_weights["muon_barrel"][5][0],
fake_photon_event_weights["muon_barrel"][5][1],
fake_photon_event_weights["electron_barrel"][5][0],
fake_photon_event_weights["electron_barrel"][5][1]
)

sys.exit(0)

print """
\\begin{table}[htbp]
\\begin{center}
\\begin{tabular}{|c|c|c|}
\\hline
photon $p_T$ bin & endcap & barrel \\\\   
\\hline
\\hline
25-30 GeV & %0.3f/%0.3f & %0.3f/%0.3f  \\\\   
\\hline
30-40 GeV & %0.3f/%0.3f & %0.3f/%0.3f  \\\\   
\\hline
40-50 GeV & %0.3f/%0.3f & %0.3f/%0.3f \\\\   
\\hline
50-70 GeV & %0.3f/%0.3f & %0.3f/%0.3f  \\\\   
\\hline
70-100 GeV & %0.3f/%0.3f & %0.3f/%0.3f  \\\\   
\\hline
100-135 GeV & %0.3f/%0.3f & %0.3f/%0.3f  \\\\   
\\hline
\\end{tabular}
\\end{center}
\\caption{Fitted/true fake photon event weights.}
\\label{tab:fake_photon_event_weights_closure_test}
\end{table}
"""%(fake_photon_event_weights_wjets_wgjets_as_data["both_endcap"][0],
fake_photon_event_weights_wjets_wgjets["both_endcap"][0],
fake_photon_event_weights_wjets_wgjets_as_data["both_barrel"][0],
fake_photon_event_weights_wjets_wgjets["both_barrel"][0],
fake_photon_event_weights_wjets_wgjets_as_data["both_endcap"][1],
fake_photon_event_weights_wjets_wgjets["both_endcap"][1],
fake_photon_event_weights_wjets_wgjets_as_data["both_barrel"][1],
fake_photon_event_weights_wjets_wgjets["both_barrel"][1],
fake_photon_event_weights_wjets_wgjets_as_data["both_endcap"][2],
fake_photon_event_weights_wjets_wgjets["both_endcap"][2],
fake_photon_event_weights_wjets_wgjets_as_data["both_barrel"][2],
fake_photon_event_weights_wjets_wgjets["both_barrel"][2],
fake_photon_event_weights_wjets_wgjets_as_data["both_endcap"][3],
fake_photon_event_weights_wjets_wgjets["both_endcap"][3],
fake_photon_event_weights_wjets_wgjets_as_data["both_barrel"][3],
fake_photon_event_weights_wjets_wgjets["both_barrel"][3],
fake_photon_event_weights_wjets_wgjets_as_data["both_endcap"][4],
fake_photon_event_weights_wjets_wgjets["both_endcap"][4],
fake_photon_event_weights_wjets_wgjets_as_data["both_barrel"][4],
fake_photon_event_weights_wjets_wgjets["both_barrel"][4],
fake_photon_event_weights_wjets_wgjets_as_data["both_endcap"][5],
fake_photon_event_weights_wjets_wgjets["both_endcap"][5],
fake_photon_event_weights_wjets_wgjets_as_data["both_barrel"][5],
fake_photon_event_weights_wjets_wgjets["both_barrel"][5])


print """
\\begin{table}[htbp]
\\begin{center}
\\begin{tabular}{|c|c|c|c|c|}
\\hline
photon $p_T$ bin & muon endcap & electron endcap & muon barrel & electron barrel  \\\\   
\\hline
\\hline
25-30 GeV & %0.3f & %0.3f & %0.3f & %0.3f  \\\\   
\\hline
30-40 GeV & %0.3f & %0.3f & %0.3f & %0.3f \\\\   
\\hline
40-50 GeV & %0.3f & %0.3f & %0.3f & %0.3f \\\\   
\\hline
50-70 GeV & %0.3f & %0.3f & %0.3f & %0.3f  \\\\   
\\hline
70-100 GeV & %0.3f & %0.3f & %0.3f & %0.3f  \\\\   
\\hline
100-135 GeV & %0.3f & %0.3f & %0.3f & %0.3f  \\\\   
\\hline
\\end{tabular}
\\end{center}
\\caption{Alternative fake photon event weights.}
\\label{tab:alternative_fake_photon_event_weights}
\end{table}
"""%(
fake_photon_event_weights["muon_endcap"][0] + fake_photon_event_weights_wjets_wgjets["both_endcap"][0] - fake_photon_event_weights_wjets_wgjets_as_data["both_endcap"][0],
fake_photon_event_weights["electron_endcap"][0] + fake_photon_event_weights_wjets_wgjets["both_endcap"][0] - fake_photon_event_weights_wjets_wgjets_as_data["both_endcap"][0],
fake_photon_event_weights["muon_barrel"][0] + fake_photon_event_weights_wjets_wgjets["both_barrel"][0] - fake_photon_event_weights_wjets_wgjets_as_data["both_barrel"][0],
fake_photon_event_weights["electron_barrel"][0] + fake_photon_event_weights_wjets_wgjets["both_barrel"][0] - fake_photon_event_weights_wjets_wgjets_as_data["both_barrel"][0],
fake_photon_event_weights["muon_endcap"][1] + fake_photon_event_weights_wjets_wgjets["both_endcap"][1] - fake_photon_event_weights_wjets_wgjets_as_data["both_endcap"][1],
fake_photon_event_weights["electron_endcap"][1] + fake_photon_event_weights_wjets_wgjets["both_endcap"][1] - fake_photon_event_weights_wjets_wgjets_as_data["both_endcap"][1],
fake_photon_event_weights["muon_barrel"][1] + fake_photon_event_weights_wjets_wgjets["both_barrel"][1] - fake_photon_event_weights_wjets_wgjets_as_data["both_barrel"][1],
fake_photon_event_weights["electron_barrel"][1] + fake_photon_event_weights_wjets_wgjets["both_barrel"][1] - fake_photon_event_weights_wjets_wgjets_as_data["both_barrel"][1],
fake_photon_event_weights["muon_endcap"][2] + fake_photon_event_weights_wjets_wgjets["both_endcap"][2] - fake_photon_event_weights_wjets_wgjets_as_data["both_endcap"][2],
fake_photon_event_weights["electron_endcap"][2] + fake_photon_event_weights_wjets_wgjets["both_endcap"][2] - fake_photon_event_weights_wjets_wgjets_as_data["both_endcap"][2],
fake_photon_event_weights["muon_barrel"][2] + fake_photon_event_weights_wjets_wgjets["both_barrel"][2] - fake_photon_event_weights_wjets_wgjets_as_data["both_barrel"][2],
fake_photon_event_weights["electron_barrel"][2] + fake_photon_event_weights_wjets_wgjets["both_barrel"][2] - fake_photon_event_weights_wjets_wgjets_as_data["both_barrel"][2],
fake_photon_event_weights["muon_endcap"][3] + fake_photon_event_weights_wjets_wgjets["both_endcap"][3] - fake_photon_event_weights_wjets_wgjets_as_data["both_endcap"][3],
fake_photon_event_weights["electron_endcap"][3] + fake_photon_event_weights_wjets_wgjets["both_endcap"][3] - fake_photon_event_weights_wjets_wgjets_as_data["both_endcap"][3],
fake_photon_event_weights["muon_barrel"][3] + fake_photon_event_weights_wjets_wgjets["both_barrel"][3] - fake_photon_event_weights_wjets_wgjets_as_data["both_barrel"][3],
fake_photon_event_weights["electron_barrel"][3] + fake_photon_event_weights_wjets_wgjets["both_barrel"][3] - fake_photon_event_weights_wjets_wgjets_as_data["both_barrel"][3],
fake_photon_event_weights["muon_endcap"][4] + fake_photon_event_weights_wjets_wgjets["both_endcap"][4] - fake_photon_event_weights_wjets_wgjets_as_data["both_endcap"][4],
fake_photon_event_weights["electron_endcap"][4] + fake_photon_event_weights_wjets_wgjets["both_endcap"][4] - fake_photon_event_weights_wjets_wgjets_as_data["both_endcap"][4],
fake_photon_event_weights["muon_barrel"][4] + fake_photon_event_weights_wjets_wgjets["both_barrel"][4] - fake_photon_event_weights_wjets_wgjets_as_data["both_barrel"][4],
fake_photon_event_weights["electron_barrel"][4] + fake_photon_event_weights_wjets_wgjets["both_barrel"][4] - fake_photon_event_weights_wjets_wgjets_as_data["both_barrel"][4],
fake_photon_event_weights["muon_endcap"][5] + fake_photon_event_weights_wjets_wgjets["both_endcap"][5] - fake_photon_event_weights_wjets_wgjets_as_data["both_endcap"][5],
fake_photon_event_weights["electron_endcap"][5] + fake_photon_event_weights_wjets_wgjets["both_endcap"][5] - fake_photon_event_weights_wjets_wgjets_as_data["both_endcap"][5],
fake_photon_event_weights["muon_barrel"][5] + fake_photon_event_weights_wjets_wgjets["both_barrel"][5] - fake_photon_event_weights_wjets_wgjets_as_data["both_barrel"][5],
fake_photon_event_weights["electron_barrel"][5] + fake_photon_event_weights_wjets_wgjets["both_barrel"][5] - fake_photon_event_weights_wjets_wgjets_as_data["both_barrel"][5]
)
