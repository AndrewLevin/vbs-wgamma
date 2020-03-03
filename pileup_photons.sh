#root [1] Events->Scan("lumi:event:photon_eta:photon_phi","(photon_genjet_matching == 0 && pass_selection && puppimet > 40 && !(photon_gen_matching == 1|| photon_gen_matching == 4 || photon_gen_matching == 5 || photon_gen_matching == 6) && is_lepton_real == 1 && abs(lepton_pdg_id) == 13 && photon_pt > 25 && lepton_pt > 26 && photon_selection == 0 && is_lepton_tight == 1)")
date
wjets_nlines=`cat wjets_events.txt | wc -l`

i=1

while (( $(($i-1)) < $wjets_nlines )); do

wjets_lumi=`cat wjets_events.txt | head -n$i | tail -n1 | awk '{print $1}'`
wjets_event=`cat wjets_events.txt | head -n$i | tail -n1 | awk '{print $2}'`
wjets_eta=`cat wjets_events.txt | head -n$i | tail -n1 | awk '{print $3}'`
wjets_phi=`cat wjets_events.txt | head -n$i | tail -n1 | awk '{print $4}'`

inlfn=`cat wjets_lfns_lumis.txt | grep ","${wjets_lumi}"," | awk '{print $1}'`

echo "python wg_print_pileup_info.py --infile root://cms-xrd-global.cern.ch/${inlfn} --event ${wjets_event} --lumi ${wjets_lumi}"

ret=`python wg_print_pileup_info.py --infile root://cms-xrd-global.cern.ch/${inlfn} --event ${wjets_event} --lumi ${wjets_lumi}`

firstlumi=`echo $ret | awk '{print $2}'`
firstevent=`echo $ret | awk '{print $3}'`
lastevent=`echo $ret | awk '{print $3}'`

j=1

singlelumi=1

nwords=`echo $ret | wc -w`

#echo $nlines

while (( $(($j+1)) < $nwords )); 
do 

lumi=`echo $ret | awk '{print $'$(($j+1))'}'`
event=`echo $ret | awk '{print $'$(($j+2))'}'`
lastevent=$event
#echo $run" "$lumi" "$event
j=$(($j+3))

if ! [ $lumi == $firstlumi ];
    then
    singlelumi=0;
fi

done;

i=$(($i+1))

if  ! (( $singlelumi )); 
then
    echo "not a single lumi, continuing"
    continue;
fi

#minbiasfilename=`dasgoclient --query "file,run,lumi dataset=/MinBias_TuneCUETP8M1_13TeV-pythia8/RunIISummer15GS-MCRUN2_71_V1_ext1-v1/GEN-SIM"  | grep ","$firstlumi"," | awk '{print $1}'`
minbiasfilename=`cat minbias_lfns_lumis.txt | grep ","$firstlumi"," | awk '{print $1}'`

echo \$wjets_lumi
echo $wjets_lumi
echo \$wjets_event
echo $wjets_event

echo "python wg_print_gen_particles.py  --infile root://cms-xrd-global.cern.ch/$minbiasfilename --lumi $lumi --evmin $firstevent --evmax $lastevent --eta $wjets_eta --phi $wjets_phi"

python wg_print_gen_particles.py  --infile root://cms-xrd-global.cern.ch/$minbiasfilename --lumi $lumi --evmin $firstevent --evmax $lastevent --eta $wjets_eta --phi $wjets_phi

done;
date
