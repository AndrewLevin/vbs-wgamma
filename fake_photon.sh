python -u wg_make_fake_photon_weights.py --year 2016 -o /eos/user/a/amlevin/www/wg_fake_photon/data/ 2>&1 | tee -a fake_photon_data_2016.txt
python -u wg_make_fake_photon_weights.py --year 2017 -o /eos/user/a/amlevin/www/wg_fake_photon/data/ 2>&1 | tee -a fake_photon_data_2017.txt
python -u wg_make_fake_photon_weights.py --year 2018 -o /eos/user/a/amlevin/www/wg_fake_photon/data/ 2>&1 | tee -a fake_photon_data_2018.txt
python -u wg_make_fake_photon_weights.py --year 2016 -o /eos/user/a/amlevin/www/wg_fake_photon/mc/ --mc 2>&1 | tee -a fake_photon_mc_2016.txt
python -u wg_make_fake_photon_weights.py --year 2017 -o /eos/user/a/amlevin/www/wg_fake_photon/mc/ --mc 2>&1 | tee -a fake_photon_mc_2017.txt
python -u wg_make_fake_photon_weights.py --year 2018 -o /eos/user/a/amlevin/www/wg_fake_photon/mc/ --mc 2>&1 | tee -a fake_photon_mc_2018.txt
python -u wg_make_fake_photon_weights.py --year 2016 -o /eos/user/a/amlevin/www/wg_fake_photon/mc/ --mc --true 2>&1 | tee -a fake_photon_true_2016.txt
python -u wg_make_fake_photon_weights.py --year 2017 -o /eos/user/a/amlevin/www/wg_fake_photon/mc/ --mc --true 2>&1 | tee -a fake_photon_true_2017.txt
python -u wg_make_fake_photon_weights.py --year 2018 -o /eos/user/a/amlevin/www/wg_fake_photon/mc/ --mc --true 2>&1 | tee -a fake_photon_true_2018.txt
