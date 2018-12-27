from ROOT import *
import optparse
import sys
from array import array

parser = optparse.OptionParser()

parser.add_option('-i', '--input_filename', help='input_filename', dest='infname', default='my_input_file.root')
parser.add_option('-o', '--output_filename', help='output_filename', dest='outfname', default='my_output_file.root')

(options,args) = parser.parse_args()

fin=TFile(options.infname,"read")
fout=TFile(options.outfname,"recreate")
fin.cd()

told = fin.Get("Events")

fout.cd()

tnew = told.CloneTree(0)

run_lumi_evt_nums = {}

n_new = 0

for entry in range(0,told.GetEntries()):

    if entry % 100000 == 0:
        print entry

    told.GetEntry(entry)

    if (told.run,told.lumi,told.event) not in run_lumi_evt_nums:
        n_new=n_new+1
        tnew.Fill()
        run_lumi_evt_nums[(told.run,told.lumi,told.event)] = True

    assert(tnew.GetEntries() == n_new)

tnew.Write()
