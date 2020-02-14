wjets_nlines=`cat delete_this.txt | wc -l`

i=1

while (( $(($i-1)) < $wjets_nlines )); do

wjets_lumi=`cat delete_this.txt | head -n$i | tail -n1 | awk '{print $1}'`
wjets_event=`cat delete_this.txt | head -n$i | tail -n1 | awk '{print $2}'`
wjets_eta=`cat delete_this.txt | head -n$i | tail -n1 | awk '{print $3}'`
wjets_phi=`cat delete_this.txt | head -n$i | tail -n1 | awk '{print $4}'`

inlfn=`cat wjets_lfns_lumis.txt | grep ","${wjets_lumi}"," | awk '{print $1}'`

ret=`python print_pileup_info.py --infile root://cms-xrd-global.cern.ch/${inlfn} --event ${wjets_event} --lumi ${wjets_lumi}`

firstlumi=`echo $ret | awk '{print $2}'`
firstevent=`echo $ret | awk '{print $3}'`
lastevent=`echo $ret | awk '{print $3}'`

j=1

singlelumi=1

nlines=`echo $ret | wc -w`

#echo $nlines

while (( $(($j+2)) < $nlines )); 
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

#minbiasfilename=`dasgoclient --query "file,run,lumi dataset=/MinBias_TuneCUETP8M1_13TeV-pythia8/RunIISummer15GS-MCRUN2_71_V1_ext1-v1/GEN-SIM"  | grep ","$firstlumi"," | awk '{print $1}'`
minbiasfilename=`cat minbias_lfns_lumis.txt | grep ","$firstlumi"," | awk '{print $1}'`

python print_gen_particles.py  --infile root://cms-xrd-global.cern.ch/$minbiasfilename --lumi $lumi --evmin $firstevent --evmax $lastevent --eta $wjets_eta --phi $wjets_phi

i=$(($i+1))

done;

