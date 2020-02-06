text2workspace.py datacard_el_chan.txt -m 125
combineTool.py -M Impacts -d datacard_el_chan.root -m 125 --doInitialFit --robustFit 1
combineTool.py -M Impacts -d datacard_el_chan.root -m 125 --robustFit 1 --doFits
combineTool.py -M Impacts -d datacard_el_chan.root -m 125 -o impacts.json
plotImpacts.py -i impacts.json -o impacts
cp impacts.pdf /eos/user/a/amlevin/www/tmp/
