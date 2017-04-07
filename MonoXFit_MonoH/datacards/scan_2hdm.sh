#!/bin/bash


#samples_2hdm=(ZpA0-800 ZpA0-1000 ZpA0-1400 ZpA0-1700 ZpA0-2000 ZpA0-2500)
samples_2hdm=(ZpA0-1700)

echo "med dm twosigdown onesigdown exp onesigup twosigup" > limits_2hdm.txt


for k in "${samples_2hdm[@]}"; do
    mediator=${k#'ZpA0-'}
    branchingratio='1.0'
    cp combined_tmpl.txt combined.txt
    sed -i 's/XX-SIGNAL-XX/'${k}'/g' combined.txt
    
    #Computing limits
    combine -M Asymptotic -t -1 combined.txt  --rAbsAcc 0 --rMax 0.6 --verbose 3 | tee limits_tmp.txt
    #Parsing results into textfile
    twosigdown=`cat limits_tmp.txt | grep 'Expected  2.5%: r <' | awk '{print $5}'`
    onesigdown=`cat limits_tmp.txt | grep 'Expected 16.0%: r <' | awk '{print $5}'`
    exp=`cat limits_tmp.txt | grep 'Expected 50.0%: r <' | awk '{print $5}'`
    onesigup=`cat limits_tmp.txt | grep 'Expected 84.0%: r <' | awk '{print $5}'`
    twosigup=`cat limits_tmp.txt | grep 'Expected 97.5%: r <' | awk '{print $5}'`

    #Applying branching ratio
    twosigdown=`echo "scale=7 ; $twosigdown / $branchingratio" | bc`
    onesigdown=`echo "scale=7 ; $onesigdown / $branchingratio" | bc`
    exp=`echo "scale=7 ; $exp / $branchingratio" | bc`
    onesigup=`echo "scale=7 ; $onesigup / $branchingratio" | bc`
    twosigup=`echo "scale=7 ; $twosigup / $branchingratio" | bc`

    echo "${mediator} 300 ${twosigdown} ${onesigdown} ${exp} ${onesigup} ${twosigup}" >> limits_2hdm.txt
done
