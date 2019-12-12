date 2>&1 | tee wg_muon.txt; python -u wg_rdf.py --no_pdf_var_for_2017_and_2018 --lep muon -o /eos/user/a/amlevin/www/wg/muon/ --make_plots --overflow --phoeta both --year run2 2>&1 | tee -a wg_muon.txt; date 2>&1 | tee -a wg_muon.txt
date 2>&1 | tee wg_electron.txt; python -u wg_rdf.py --no_pdf_var_for_2017_and_2018 --lep electron --fit -o /eos/user/a/amlevin/www/wg/electron/ --make_plots --overflow --phoeta both --year run2 2>&1 | tee -a wg_electron.txt; date 2>&1 | tee -a wg_electron.txt
date 2>&1 | tee wg_2016_electron.txt; python -u wg_rdf.py --no_pdf_var_for_2017_and_2018 --lep electron -o /eos/user/a/amlevin/www/wg/2016/electron/ --make_plots --overflow --phoeta both --year 2016 2>&1 | tee -a wg_2016_electron.txt; date 2>&1 | tee -a wg_2016_electron.txt
date 2>&1 | tee wg_2017_electron.txt; python -u wg_rdf.py --no_pdf_var_for_2017_and_2018 --lep electron -o /eos/user/a/amlevin/www/wg/2017/electron/ --make_plots --overflow --phoeta both --year 2017 2>&1 | tee -a wg_2017_electron.txt; date 2>&1 | tee -a wg_2017_electron.txt
date 2>&1 | tee wg_2018_electron.txt; python -u wg_rdf.py --no_pdf_var_for_2017_and_2018 --lep electron -o /eos/user/a/amlevin/www/wg/2018/electron/ --make_plots --overflow --phoeta both --year 2018 2>&1 | tee -a wg_2018_electron.txt; date 2>&1 | tee -a wg_2018_electron.txt