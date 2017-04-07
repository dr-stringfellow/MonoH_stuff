#!/bin/bash


samples_2hdm=(BarZp-10-1 BarZp-10-10 BarZp-10-50 BarZp-10-150 BarZp-10-500 BarZp-15-10 BarZp-20-1 BarZp-50-1 BarZp-50-10 BarZp-50-50 BarZp-95-50 BarZp-100-1 BarZp-100-10 BarZp-200-1 BarZp-200-50 BarZp-200-150 BarZp-295-150 BarZp-300-1 BarZp-300-50 BarZp-500-1 BarZp-500-150 BarZp-995-500 BarZp-1000-1 BarZp-1000-150 BarZp-1000-1000 BarZp-1995-1000 BarZp-2000-1 BarZp-2000-500 BarZp-10000-1 BarZp-10000-10 BarZp-10000-50 BarZp-10000-150 BarZp-10000-500)
#samples_2hdm=(BarZp-1000-1000)

echo "med dm twosigdown onesigdown exp onesigup twosigup" > limits_barzp.txt


for k in "${samples_2hdm[@]}"; do
    mediatordm=${k#'BarZp-'}
    branchingratio='1.0'
    mediator=${mediatordm%-*}
    dm=`echo ${mediatordm#${mediator}-}`

    cp combined_tmpl.txt combined.txt
    sed -i 's/XX-SIGNAL-XX/'${k}'/g' combined.txt
    
    #Computing limits
    combine -M Asymptotic -t -1 combined.txt --rAbsAcc 0 --rMax 30  | tee limits_tmp.txt
    #Parsing results into textfile
    twosigdown=`cat limits_tmp.txt | grep 'Expected  2.5%: r <' | awk '{print $5}'`
    onesigdown=`cat limits_tmp.txt | grep 'Expected 16.0%: r <' | awk '{print $5}'`
    exp=`cat limits_tmp.txt | grep 'Expected 50.0%: r <' | awk '{print $5}'`
    onesigup=`cat limits_tmp.txt | grep 'Expected 84.0%: r <' | awk '{print $5}'`
    twosigup=`cat limits_tmp.txt | grep 'Expected 97.5%: r <' | awk '{print $5}'`

    rm limits_tmp.txt

    #Applying branching ratio
    onesigdown=`echo "scale=7 ; $onesigdown / $branchingratio" | bc`
    twosigdown=`echo "scale=7 ; $twosigdown / $branchingratio" | bc`
    exp=`echo "scale=7 ; $exp / $branchingratio" | bc`
    onesigup=`echo "scale=7 ; $onesigup / $branchingratio" | bc`
    twosigup=`echo "scale=7 ; $twosigup / $branchingratio" | bc`

    echo "${mediator} ${dm} ${twosigdown} ${onesigdown} ${exp} ${onesigup} ${twosigup}" >> limits_barzp.txt

done
