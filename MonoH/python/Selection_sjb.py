from PandaCore.Tools.Misc import *
from re import sub


metTrigger='(trigger&1)!=0'
eleTrigger='(trigger&2)!=0'
phoTrigger='(trigger&4)!=0'


cuts = {}
weights = {}
triggers = {}

#baseline = 'metFilter==1 && nFatjet==1 && fj1Pt>200 && nTau==0 && higgs_ecfbdt>-0.1'
#baseline = 'metFilter==1 && nFatjet==1 && fj1Pt>200 && nTau==0 && fj1ECFN_2_3_20/pow(fj1ECFN_1_2_20,2.00)<0.113'
baseline = 'metFilter==1 && nFatjet==1 && fj1Pt>200 && nTau==0 && N2DDT<0.0 && Sum$(jetPt>30 && jetIso)<2'

#cuts for specific regions
cuts['signal'] = tAND(baseline,'nLooseLep==0 && nLooseElectron==0 && nLoosePhoton==0 && puppimet>200 && isojetNBtags==0 && fj1MSD_corr>100 && fj1MSD_corr<150 && dphipuppimet>0.4 && fj1MinCSV>0.58')
cuts['tm'] = tAND(baseline,'(nLooseElectron+nLoosePhoton+nTau)==0 && nLooseMuon==1 && looseLep1IsTight==1 && puppiUWmag>200 && isojetNBtags==1 && fj1MSD_corr>100 && fj1MSD_corr<150 && dphipuppiUW>0.4 && fj1MinCSV>0.58')
cuts['te'] = tAND(baseline,'(nLooseMuon+nLoosePhoton+nTau)==0 && nLooseElectron==1 && looseLep1IsTight==1 && puppiUWmag>200 && isojetNBtags==1 && fj1MSD_corr>100 && fj1MSD_corr<150 && dphipuppiUW>0.4 && puppimet>50 && fj1MinCSV>0.58')
cuts['wmn'] = tAND(baseline,'(nLooseElectron+nLoosePhoton+nTau)==0 && nLooseMuon==1 && looseLep1IsTight==1 && puppiUWmag>200 && isojetNBtags==0 && fj1MSD_corr>50 && fj1MSD_corr<150 && dphipuppiUW>0.4 && fj1MinCSV>0.58')
cuts['wen'] = tAND(baseline,'(nLooseMuon+nLoosePhoton+nTau)==0 && nLooseElectron==1 && looseLep1IsTight==1 && puppiUWmag>200 && isojetNBtags==0 && fj1MSD_corr>50 && fj1MSD_corr<150 && dphipuppiUW>0.4 && puppimet>50 && fj1MinCSV>0.58')
cuts['zmm'] = tAND(baseline,'(nLooseElectron+nLoosePhoton+nTau)==0 && nLooseMuon==2 && looseLep1IsTight==1 && puppiUZmag>200 && isojetNBtags==0 && fj1MSD_corr>50 && fj1MSD_corr<250 && dphipuppiUZ>0.4 && diLepMass>60 && diLepMass<120 && fj1MinCSV>0.58')
cuts['zee'] = tAND(baseline,'(nLooseMuon+nLoosePhoton+nTau)==0 && nLooseElectron==2 && looseLep1IsTight==1 && puppiUZmag>200 && isojetNBtags==0 && fj1MSD_corr>50 && fj1MSD_corr<250 && dphipuppiUZ>0.4 && diLepMass>60 && diLepMass<120 && fj1MinCSV>0.58')
cuts['zmm_fail'] = tAND(baseline,'(nLooseElectron+nLoosePhoton+nTau)==0 && nLooseMuon==2 && looseLep1IsTight==1 && puppiUZmag>200 && isojetNBtags==0 && fj1MSD_corr>50 && fj1MSD_corr<250 && dphipuppiUZ>0.4 && diLepMass>60 && diLepMass<120 && fj1MinCSV<0.58')
cuts['zee_fail'] = tAND(baseline,'(nLooseMuon+nLoosePhoton+nTau)==0 && nLooseElectron==2 && looseLep1IsTight==1 && puppiUZmag>200 && isojetNBtags==0 && fj1MSD_corr>50 && fj1MSD_corr<250 && dphipuppiUZ>0.4 && diLepMass>60 && diLepMass<120 && fj1MinCSV<0.58')
cuts['pho'] = tAND(baseline,'(nLooseMuon+nLooseElectron+nTau)==0 && nLoosePhoton==1 && loosePho1IsTight==1 && puppiUAmag>200 && isojetNBtags==0 && fj1MSD_corr>50 && fj1MSD_corr<250 && dphipuppiUA>0.4 && fj1MinCSV>0.58')

#weights for specific regions
weights['base'] = 'normalizedWeight*sf_pu*sf_ewkV*sf_qcdV'
weights['signal'] = tTIMES(weights['base'],'%f*sf_metTrig*sf_tt*sf_btag0*sf_sjbtag2')
weights['tm'] = tTIMES(weights['base'],'%f*sf_metTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag1*sf_sjbtag2')
weights['te'] = tTIMES(weights['base'],'%f*sf_eleTrig*sf_lepID*sf_lepTrack*sf_tt*sf_btag1*sf_sjbtag2')
weights['wmn'] = tTIMES(weights['base'],'%f*sf_metTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*sf_sjbtag2')
weights['wen'] = tTIMES(weights['base'],'%f*sf_eleTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*sf_sjbtag2')
weights['zmm'] = tTIMES(weights['base'],'%f*sf_metTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*sf_sjbtag2')
weights['zee'] = tTIMES(weights['base'],'%f*sf_eleTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*sf_sjbtag2')
weights['zmm_fail'] = tTIMES(weights['base'],'%f*sf_metTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*sf_sjbtag0')
weights['zee_fail'] = tTIMES(weights['base'],'%f*sf_eleTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*sf_sjbtag0')
weights['pho'] = tTIMES(weights['base'],'%f*sf_phoTrig*sf_btag0*1.0*sf_sjbtag2')


for r in ['signal','wmn','wen','tm','te','zmm','zee','zmm_fail','zee_fail','pho']:
    print r
    for shift in ['BUp','BDown','MUp','MDown']:
        for cent in ['sf_btag','sf_sjbtag']:
            if '2' in weights[r]:
                weights[r+'_'+cent+shift] = sub(cent+'0',cent+'0'+shift,sub(cent+'2',cent+'2'+shift,weights[r]))
#                print weights[r+'_'+cent+shift]

            
weights['zmm_fail_PDFUp'] = tTIMES(weights['base'],'%f*sf_metTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*pdfUp')
weights['zmm_fail_PDFDown'] = tTIMES(weights['base'],'%f*sf_metTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*pdfDown')
weights['zmm_fail_ScaleUp'] = tTIMES(weights['base'],'%f*sf_metTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*(scale[3]+1)')
weights['zmm_fail_ScaleDown'] = tTIMES(weights['base'],'%f*sf_metTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*(scale[5]+1)')
weights['zee_fail_PDFUp'] = tTIMES(weights['base'],'%f*sf_eleTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*pdfUp')
weights['zee_fail_PDFDown'] = tTIMES(weights['base'],'%f*sf_eleTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*pdfDown')
weights['zee_fail_ScaleUp'] = tTIMES(weights['base'],'%f*sf_eleTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*(scale[3]+1)')
weights['zee_fail_ScaleDown'] = tTIMES(weights['base'],'%f*sf_eleTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*(scale[5]+1)')


'''
for r in ['signal','tm','te','wmn','wen']:
  for shift in ['Up','Down']:
    #for cent in ['sf_btag','sf_sjbtag']:                                                                                                                                                           
    for cent in ['sf_sjcsvWeightB','sf_sjcsvWeightM','sf_csvWeightB','sf_csvWeightM']:
    #for cent in ['sf_csvWeightB','sf_csvWeightM']: 
      weights[r+'_'+cent+shift] = sub(cent,cent+shift,weights[r])
'''
