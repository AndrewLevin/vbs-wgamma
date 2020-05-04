date 2>&1 | tee wg_ewdim6.txt; python -u wg.py --lep both --ewdim6 --draw_ewdim6 -o /eos/user/a/amlevin/www/wg/ewdim6/ --make_all_plots  --phoeta both --year run2 2>&1 | tee -a wg_ewdim6.txt; date 2>&1 | tee -a wg_ewdim6.txt

date 2>&1 | tee wg_electron.txt; python -u wg.py --lep electron -o /eos/user/a/amlevin/www/wg/electron/ --phoeta both --year run2 --make_datacard --make_all_plots --zveto 2>&1 | tee -a wg_electron.txt; date 2>&1 | tee -a wg_electron.txt

date 2>&1 | tee wg_electron_zveto.txt; python -u wg.py --lep electron -o /eos/user/a/amlevin/www/wg/electron_zveto/ --phoeta both --year run2 --make_all_plots --zveto 2>&1 | tee -a wg_electron_zveto.txt; date 2>&1 | tee -a wg_electron_zveto.txt

date 2>&1 | tee wg_muon.txt; python -u wg.py  --lep muon -o /eos/user/a/amlevin/www/wg/muon/ --phoeta both --year run2 --make_datacard --make_all_plots 2>&1 | tee -a wg_muon.txt; date 2>&1 | tee -a wg_muon.txt

date 2>&1 | tee wg_electron_mcfakephoton_zveto.txt; python -u wg.py  --lep electron -o /eos/user/a/amlevin/www/wg/electron_mcfakephoton_zveto/ --phoeta both --year run2 --make_all_plots --zveto --use_wjets_for_fake_photon 2>&1 | tee -a wg_electron_mcfakephoton_zveto.txt; date 2>&1 | tee -a wg_electron_mcfakephoton_zveto.txt

date 2>&1 | tee wg_muon_mcfakephoton.txt; python -u wg.py --lep muon -o /eos/user/a/amlevin/www/wg/muon_mcfakephoton/ --phoeta both --year run2 --make_all_plots --use_wjets_for_fake_photon 2>&1 | tee -a wg_muon_mcfakephoton.txt; date 2>&1 | tee -a wg_muon_mcfakephoton.txt


date 2>&1 | tee wg_2016_electron.txt; python -u wg_rdf.py --lep electron -o /eos/user/a/amlevin/www/wg/2016/electron/ --make_plots --overflow --phoeta both --year 2016 2>&1 | tee -a wg_2016_electron.txt; date 2>&1 | tee -a wg_2016_electron.txt
date 2>&1 | tee wg_2017_electron.txt; python -u wg_rdf.py --lep electron -o /eos/user/a/amlevin/www/wg/2017/electron/ --make_plots --overflow --phoeta both --year 2017 2>&1 | tee -a wg_2017_electron.txt; date 2>&1 | tee -a wg_2017_electron.txt
date 2>&1 | tee wg_2018_electron.txt; python -u wg_rdf.py --lep electron -o /eos/user/a/amlevin/www/wg/2018/electron/ --make_plots --overflow --phoeta both --year 2018 2>&1 | tee -a wg_2018_electron.txt; date 2>&1 | tee -a wg_2018_electron.txt
