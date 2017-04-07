text2workspace.py combined_nopho_wtop_fail_now.txt -m 125
combineTool.py -M Impacts -d combined_nopho_wtop_fail_now.root -m 125 --doInitialFit --robustFit 1
combineTool.py -M Impacts -d combined_nopho_wtop_fail_now.root -m 125 --robustFit 1 --doFits
combineTool.py -M Impacts -d combined_nopho_wtop_fail_now.root -m 125 -o impacts.json
plotImpacts.py -i impacts.json -o impacts