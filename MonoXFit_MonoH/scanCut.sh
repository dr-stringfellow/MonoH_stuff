#!/bin/bash

cut=$1

sed "s?XXXX?top_ecf_bdt>${cut}?" configs/categories_tmpl.py > configs/categories_scan.py
python buildModel.py categories_scan
cp mono-x.root /home/snarayan/home000/store/panda/v_8020_2_3//scans/hists/mono-x_${cut}.root
