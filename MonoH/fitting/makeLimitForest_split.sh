#!/bin/bash

#echo signal zmm zee wmn wen tm te pho | xargs -n 1 -P 8 python makeLimitForest_split.py --region
#echo signal | xargs -n 1 -P 8 python makeLimitForest_split.py --region
#echo pho | xargs -n 1 -P 8 python makeLimitForest_split.py --region
#echo zmm zee | xargs -n 1 -P 8 python makeLimitForest_split.py --region
#echo  zmm_fail zee_fail | xargs -n 1 -P 8 python makeLimitForest_split.py --region
echo  wmn_fail wen_fail | xargs -n 1 -P 8 python makeLimitForest_split.py --region
#echo  zmm_fail | xargs -n 1 -P 8 python makeLimitForest_split.py --region
#echo tm te | xargs -n 1 -P 8 python makeLimitForest_split.py --region
#echo wmn wen | xargs -n 1 -P 8 python makeLimitForest_split.py --region
