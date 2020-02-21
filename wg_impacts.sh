indatacard=$1
text2workspace.py $indatacard -m 125
label=`echo $indatacard | awk -F. '{print $1} '`
combineTool.py -M Impacts -d $label.root -m 125 --doInitialFit --robustFit 1
combineTool.py -M Impacts -d $label.root -m 125 --robustFit 1 --doFits
combineTool.py -M Impacts -d $label.root -m 125 -o impacts.json
plotImpacts.py -i impacts.json -o impacts
cp impacts.pdf /eos/user/a/amlevin/www/tmp/
