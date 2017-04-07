#!/usr/bin/env python
from re import sub
from sys import argv,exit
from os import path,getenv
import argparse
parser = argparse.ArgumentParser(description='make forest')
parser.add_argument('--region',metavar='region',type=str,default=None)
toProcess = parser.parse_args().region

argv=[]
import ROOT as root
from PandaCore.Tools.Misc import *
from PandaCore.Tools.Load import *
import PandaCore.Tools.Functions 
import PandaAnalysis.MonoH.Selection_doubleb as sel
#import PandaAnalysis.MonoH.Selection_mw as sel
#import PandaAnalysis.MonoH.Selection_t21 as sel

Load('PandaAnalysisFlat','LimitTreeBuilder')


subfolder = ''
if toProcess=='signal':
  subfolder = 'sr/'
elif toProcess=='wmn':
  subfolder = 'cr_w_mu/'
elif toProcess=='wmn_fail':
  subfolder = 'cr_w_mu/'
elif toProcess=='wen':
  subfolder = 'cr_w_el/'
elif toProcess=='wen_fail':
  subfolder = 'cr_w_el/'
elif toProcess=='tm':
  subfolder = 'cr_ttbar_mu/'
elif toProcess=='te':
  subfolder = 'cr_ttbar_el/'
elif toProcess=='zmm':
  subfolder = 'cr_dimuon/'
elif toProcess=='zmm_fail':
  subfolder = 'cr_dimuon/'
elif toProcess=='zee':
  subfolder = 'cr_dielectron/'
elif toProcess=='zee_fail':
  subfolder = 'cr_dielectron/'
elif toProcess=='pho':
  subfolder = 'cr_gamma/'
   

#forestDir = '/scratch3/bmaier/flat/'
#baseDir = '/scratch3/bmaier/flat/' + subfolder
#forestDir = '/local/bmaier/flat/'
#baseDir = '/local/bmaier/flat/' + subfolder
forestDir = '/data/t3home000/bmaier/flat_v11/'
baseDir = '/data/t3home000/bmaier/flat_v11/' + subfolder   
lumi = 35900.


ttbar_mistag_SF = "*1.03"


factory = root.LimitTreeBuilder()
if toProcess:
  factory.SetOutFile(forestDir+'/limits/limitForest_%s.root'%toProcess)
else:
  factory.SetOutFile(forestDir+'/limits/limitForest_all.root')

def dataCut(basecut,trigger):
  # return tAND('metFilter==1',tAND(trigger,basecut))
  return tAND(trigger,basecut)

def getTree(fpath):
  fIn = root.TFile(baseDir+fpath+'.root')
  tIn = fIn.Get('events')
  return tIn,fIn

def enable(regionName):
  if toProcess:
    return (toProcess==regionName)
  else:
    return True

def shiftBtags(label,tree,varmap,cut,basecut,signal):
  # basecut is really the baseweight 
  ps = []
  for shift in ['BUp','BDown','MUp','MDown']:
    for cent in ['sf_btag']:
      shiftedlabel = '_'
      if 'sj' in cent:
        shiftedlabel += 'sj'
      if 'B' in shift:
        shiftedlabel += 'btag'
      else:
        shiftedlabel += 'mistag'
      if 'Up' in shift:
        shiftedlabel += 'Up'
      else:
        shiftedlabel += 'Down'
      weight = sel.weights[basecut+'_'+cent+shift]%lumi
      if signal==1:
        weight = weight + "*1"
      if signal==2:
        weight = weight + ttbar_mistag_SF
      print weight

      PInfo('makeLimitForest.py',weight)
      shiftedProcess = root.Process(label,tree,varmap,cut,weight)
      shiftedProcess.syst = shiftedlabel
      ps.append(shiftedProcess)
  return ps


def shiftScalesPDF(label,tree,varmap,cut,basecut,signal):
  

  ps = []
  for shift in ['ScaleUp','ScaleDown','PDFUp','PDFDown']:
    weight = sel.weights[basecut+'_'+shift]%lumi
    if signal==1:
      weight = weight + "*1"
    if signal==2:
      weight = weight + ttbar_mistag_SF
        
    shiftedlabel = '_'
    if 'Scale' in shift:
      shiftedlabel += 'Scale'
    else:
      shiftedlabel += 'PDF'
    if 'Up' in shift:
      shiftedlabel += 'Up'
    else:
      shiftedlabel += 'Down'
      
    PInfo('makeLimitForest.py',weight)
    shiftedProcess = root.Process(label,tree,varmap,cut,weight)
    shiftedProcess.syst = shiftedlabel
    ps.append(shiftedProcess)
  
  return ps

# input
tZll,fZll = getTree('ZJets')
tZvv,fZvv = getTree('ZtoNuNu')
tWlv,fWlv = getTree('WJets')
tPho,fPho = getTree('GJets')
tTTbar,fTT = getTree('TTbar')
tVV,fVV = getTree('Diboson')
tQCD,fQCD = getTree('QCD')
tST,fST = getTree('SingleTop')
tMET,fMET = getTree('MET')
tVH,fVH = getTree('VH')
tSingleEle,fSEle = getTree('SingleElectron')
tSinglePho,fSPho = getTree('SinglePhoton')
tZpA0_800,fZpA0_800 = getTree('ZpA0-800-300')
tZpA0_1000,fZpA0_1000 = getTree('ZpA0-1000-300')
#tZpA0_1200,fZpA0_1200 = getTree('ZpA0-1200-300')
tZpA0_1400,fZpA0_1400 = getTree('ZpA0-1400-300')
tZpA0_1700,fZpA0_1700 = getTree('ZpA0-1700-300')
tZpA0_2000,fZpA0_2000 = getTree('ZpA0-2000-300')
tZpA0_2500,fZpA0_2500 = getTree('ZpA0-2500-300')
tBarZp_10_1,fBarZp_10_1 = getTree('ZpBaryonic-10-1')
tBarZp_10_10,fBarZp_10_10 = getTree('ZpBaryonic-10-10')
tBarZp_10_50,fBarZp_10_50 = getTree('ZpBaryonic-10-50')
tBarZp_10_150,fBarZp_10_150 = getTree('ZpBaryonic-10-150')
tBarZp_10_500,fBarZp_10_500 = getTree('ZpBaryonic-10-500')
tBarZp_15_10,fBarZp_15_10 = getTree('ZpBaryonic-15-10')
tBarZp_20_1,fBarZp_20_1 = getTree('ZpBaryonic-20-1')
tBarZp_50_1,fBarZp_50_1 = getTree('ZpBaryonic-50-1')
tBarZp_50_10,fBarZp_50_10 = getTree('ZpBaryonic-50-10')
tBarZp_50_50,fBarZp_50_50 = getTree('ZpBaryonic-50-50')
tBarZp_95_50,fBarZp_95_50 = getTree('ZpBaryonic-95-50')
tBarZp_100_1,fBarZp_100_1 = getTree('ZpBaryonic-100-1')
tBarZp_100_10,fBarZp_100_10 = getTree('ZpBaryonic-100-10')
tBarZp_200_1,fBarZp_200_1 = getTree('ZpBaryonic-200-1')
tBarZp_200_50,fBarZp_200_50 = getTree('ZpBaryonic-200-50')
tBarZp_200_150,fBarZp_200_150 = getTree('ZpBaryonic-200-150')
tBarZp_295_150,fBarZp_290_150 = getTree('ZpBaryonic-295-150')
tBarZp_300_1,fBarZp_300_1 = getTree('ZpBaryonic-300-1')
tBarZp_300_50,fBarZp_300_50 = getTree('ZpBaryonic-300-50')
tBarZp_500_1,fBarZp_500_1 = getTree('ZpBaryonic-500-1')
tBarZp_500_150,fBarZp_500_150 = getTree('ZpBaryonic-500-150')
tBarZp_995_500,fBarZp_995_500 = getTree('ZpBaryonic-995-500')
tBarZp_1000_1,fBarZp_1000_1 = getTree('ZpBaryonic-1000-1')
tBarZp_1000_150,fBarZp_1000_150 = getTree('ZpBaryonic-1000-150')
tBarZp_1000_1000,fBarZp_1000_1000 = getTree('ZpBaryonic-1000-1000')
tBarZp_1995_1000,fBarZp_1995_1000 = getTree('ZpBaryonic-1995-1000')
tBarZp_2000_1,fBarZp_2000_1 = getTree('ZpBaryonic-2000-1')
tBarZp_2000_500,fBarZp_2000_500 = getTree('ZpBaryonic-2000-500')
tBarZp_10000_1,fBarZp_10000_1 = getTree('ZpBaryonic-10000-1')
tBarZp_10000_10,fBarZp_10000_10 = getTree('ZpBaryonic-10000-10')
tBarZp_10000_50,fBarZp_10000_50 = getTree('ZpBaryonic-10000-50')
tBarZp_10000_150,fBarZp_10000_150 = getTree('ZpBaryonic-10000-150')
tBarZp_10000_500,fBarZp_10000_500 = getTree('ZpBaryonic-10000-500')




factory.cd()
regions = {}
processes = {}

vm = root.VariableMap()
vm.AddFormula('met','min(999.999,puppimet)')
vm.AddVar('genBosonPt','genBosonPt')
vm.AddVar('N2DDT','N2DDT')
vmW = root.VariableMap()
vmW.AddFormula('met','min(999.999,puppiUWmag)')
vmW.AddVar('genBosonPt','genBosonPt')
vmW.AddVar('N2DDT','N2DDT')
vmZ = root.VariableMap()
vmZ.AddFormula('met','min(999.999,puppiUZmag)')
vmZ.AddVar('genBosonPt','genBosonPt')
vmZ.AddVar('N2DDT','N2DDT')
vmA = root.VariableMap()
vmA.AddFormula('met','min(999.999,puppiUAmag)')
vmA.AddVar('genBosonPt','genBosonPt')
vmA.AddVar('N2DDT','N2DDT')


# test region
if enable('test'):
  regions['test'] = root.Region('test')
  cut = sel.cuts['signal']
  weight = '%f*%s'%(lumi,sel.weights['signal'])
  processes['test'] = [
    root.Process('Data',tMET,vm,dataCut(cut,sel.triggers['met']),'1'),
    root.Process('Diboson',tVV,vm,cut,weight),
  ]

  for p in processes['test']:
    regions['test'].AddProcess(p)
  factory.AddRegion(regions['test'])

# signal region
if enable('signal'):
  regions['signal'] = root.Region('signal')
  cut = sel.cuts['signal']
  weight = '%s'%(sel.weights['signal']%lumi)
  weight_signal = weight + "*1"
  weight_ttbar = weight + ttbar_mistag_SF
  PInfo('makeLimitForest.py',cut)
  PInfo('makeLimitForest.py',weight)
  processes['signal'] = [
    root.Process('Data',tMET,vm,dataCut(cut,sel.metTrigger),'1'),
    root.Process('Zvv',tZvv,vm,cut,weight),
    root.Process('Wlv',tWlv,vm,cut,weight),
    root.Process('Zll',tZll,vm,cut,weight),
    root.Process('ttbar',tTTbar,vm,cut,weight_ttbar),
    root.Process('ST',tST,vm,cut,weight),
    root.Process('Diboson',tVV,vm,cut,weight),
    root.Process('QCD',tQCD,vm,cut,weight),
    root.Process('VH',tVH,vm,cut,weight),
    root.Process('ZpA0_800',tZpA0_800,vm,cut,weight_signal),
    root.Process('ZpA0_1000',tZpA0_1000,vm,cut,weight_signal),
    #root.Process('ZpA0_1200',tZpA0_1200,vm,cut,weight_signal),
    root.Process('ZpA0_1400',tZpA0_1400,vm,cut,weight_signal),
    root.Process('ZpA0_1700',tZpA0_1700,vm,cut,weight_signal),
    root.Process('ZpA0_2000',tZpA0_2000,vm,cut,weight_signal),
    root.Process('ZpA0_2500',tZpA0_2500,vm,cut,weight_signal),
    root.Process('BarZp_10_1',tBarZp_10_1,vm,cut,weight_signal),
    root.Process('BarZp_10_10',tBarZp_10_10,vm,cut,weight_signal),
    root.Process('BarZp_10_50',tBarZp_10_50,vm,cut,weight_signal),
    root.Process('BarZp_10_150',tBarZp_10_150,vm,cut,weight_signal),
    root.Process('BarZp_10_500',tBarZp_10_500,vm,cut,weight_signal),
    root.Process('BarZp_15_10',tBarZp_15_10,vm,cut,weight_signal),
    root.Process('BarZp_20_1',tBarZp_20_1,vm,cut,weight_signal),
    root.Process('BarZp_50_1',tBarZp_50_1,vm,cut,weight_signal),
    root.Process('BarZp_50_10',tBarZp_50_10,vm,cut,weight_signal),
    root.Process('BarZp_50_50',tBarZp_50_50,vm,cut,weight_signal),
    root.Process('BarZp_95_50',tBarZp_95_50,vm,cut,weight_signal),
    root.Process('BarZp_100_1',tBarZp_100_1,vm,cut,weight_signal),
    root.Process('BarZp_100_10',tBarZp_100_10,vm,cut,weight_signal),
    root.Process('BarZp_200_1',tBarZp_200_1,vm,cut,weight_signal),
    root.Process('BarZp_200_50',tBarZp_200_50,vm,cut,weight_signal),
    root.Process('BarZp_200_150',tBarZp_200_150,vm,cut,weight_signal),
    root.Process('BarZp_295_150',tBarZp_295_150,vm,cut,weight_signal),
    root.Process('BarZp_300_1',tBarZp_300_1,vm,cut,weight_signal),
    root.Process('BarZp_300_50',tBarZp_300_50,vm,cut,weight_signal),
    root.Process('BarZp_500_1',tBarZp_500_1,vm,cut,weight_signal),
    root.Process('BarZp_500_150',tBarZp_500_150,vm,cut,weight_signal),
    root.Process('BarZp_995_500',tBarZp_995_500,vm,cut,weight_signal),
    root.Process('BarZp_1000_1',tBarZp_1000_1,vm,cut,weight_signal),
    root.Process('BarZp_1000_150',tBarZp_1000_150,vm,cut,weight_signal),
    root.Process('BarZp_1000_1000',tBarZp_1000_1000,vm,cut,weight_signal),
    root.Process('BarZp_1995_1000',tBarZp_1995_1000,vm,cut,weight_signal),
    root.Process('BarZp_2000_1',tBarZp_2000_1,vm,cut,weight_signal),
    root.Process('BarZp_2000_500',tBarZp_2000_500,vm,cut,weight_signal),
    root.Process('BarZp_10000_1',tBarZp_10000_1,vm,cut,weight_signal),
    root.Process('BarZp_10000_10',tBarZp_10000_10,vm,cut,weight_signal),
    root.Process('BarZp_10000_50',tBarZp_10000_50,vm,cut,weight_signal),
    root.Process('BarZp_10000_150',tBarZp_10000_150,vm,cut,weight_signal),
    root.Process('BarZp_10000_500',tBarZp_10000_500,vm,cut,weight_signal),


  ]
  processes['signal'] += shiftBtags('ttbar',tTTbar,vm,cut,'signal',2)
  processes['signal'] += shiftBtags('Zvv',tZvv,vm,cut,'signal',False)
  processes['signal'] += shiftBtags('Wlv',tWlv,vm,cut,'signal',False)
  processes['signal'] += shiftBtags('ST',tST,vm,cut,'signal',False)
  processes['signal'] += shiftBtags('Zll',tZll,vm,cut,'signal',False)
  processes['signal'] += shiftBtags('Diboson',tVV,vm,cut,'signal',False)
  processes['signal'] += shiftBtags('QCD',tQCD,vm,cut,'signal',False)
  processes['signal'] += shiftBtags('VH',tVH,vm,cut,'signal',False)
  processes['signal'] += shiftBtags('ZpA0_800',tZpA0_800,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('ZpA0_1000',tZpA0_1000,vm,cut,'signal',True)
  #processes['signal'] += shiftBtags('ZpA0_1200',tZpA0_1200,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('ZpA0_1400',tZpA0_1400,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('ZpA0_1700',tZpA0_1700,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('ZpA0_2000',tZpA0_2000,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('ZpA0_2500',tZpA0_2500,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_10_1',tBarZp_10_1,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_10_10',tBarZp_10_10,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_10_50',tBarZp_10_50,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_10_150',tBarZp_10_150,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_10_500',tBarZp_10_500,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_15_10',tBarZp_15_10,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_20_1',tBarZp_20_1,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_50_1',tBarZp_50_1,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_50_10',tBarZp_50_10,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_50_50',tBarZp_50_50,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_95_50',tBarZp_95_50,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_100_1',tBarZp_100_1,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_100_10',tBarZp_100_10,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_200_1',tBarZp_200_1,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_200_50',tBarZp_200_50,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_200_150',tBarZp_200_150,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_295_150',tBarZp_295_150,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_300_1',tBarZp_300_1,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_300_50',tBarZp_300_50,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_500_1',tBarZp_500_1,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_500_150',tBarZp_500_150,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_995_500',tBarZp_995_500,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_1000_1',tBarZp_1000_1,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_1000_150',tBarZp_1000_150,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_1000_1000',tBarZp_1000_1000,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_1995_1000',tBarZp_1995_1000,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_2000_1',tBarZp_2000_1,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_2000_500',tBarZp_2000_500,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_10000_1',tBarZp_10000_1,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_10000_10',tBarZp_10000_10,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_10000_50',tBarZp_10000_50,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_10000_150',tBarZp_10000_150,vm,cut,'signal',True)
  processes['signal'] += shiftBtags('BarZp_10000_500',tBarZp_10000_500,vm,cut,'signal',True)
  processes['signal'] += shiftScalesPDF('ttbar',tTTbar,vm,cut,'signal',2)
  processes['signal'] += shiftScalesPDF('Zvv',tZvv,vm,cut,'signal',False)
  processes['signal'] += shiftScalesPDF('Wlv',tWlv,vm,cut,'signal',False)
  processes['signal'] += shiftScalesPDF('Zll',tZll,vm,cut,'signal',False)
  processes['signal'] += shiftScalesPDF('VH',tVH,vm,cut,'signal',False)

  
  for p in processes['signal']:
    regions['signal'].AddProcess(p)
  factory.AddRegion(regions['signal'])

# wmn
if enable('wmn'):
  regions['wmn'] = root.Region('wmn')
  cut = sel.cuts['wmn']
  weight = '%s'%(sel.weights['wmn']%lumi)
  weight_ttbar = weight + ttbar_mistag_SF
  PInfo('makeLimitForest.py',cut)
  PInfo('makeLimitForest.py',weight)
  processes['wmn'] = [
    root.Process('Data',tMET,vmW,dataCut(cut,sel.metTrigger),'1'),
    root.Process('Wlv',tWlv,vmW,cut,weight),
    root.Process('Zll',tZll,vmW,cut,weight),
    root.Process('ttbar',tTTbar,vmW,cut,weight_ttbar),
    root.Process('ST',tST,vmW,cut,weight),
    root.Process('Diboson',tVV,vmW,cut,weight),
    root.Process('QCD',tQCD,vmW,cut,weight),
  ]
  processes['wmn'] += shiftBtags('ttbar',tTTbar,vmW,cut,'wmn',2)
  processes['wmn'] += shiftBtags('Wlv',tWlv,vmW,cut,'wmn',False)
  processes['wmn'] += shiftBtags('ST',tST,vmW,cut,'wmn',False)
  processes['wmn'] += shiftBtags('Zll',tZll,vmW,cut,'wmn',False)
  processes['wmn'] += shiftBtags('Diboson',tVV,vmW,cut,'wmn',False)
  processes['wmn'] += shiftBtags('QCD',tQCD,vmW,cut,'wmn',False)
  processes['wmn'] += shiftScalesPDF('ttbar',tTTbar,vmW,cut,'wmn',2)
  processes['wmn'] += shiftScalesPDF('Wlv',tWlv,vmW,cut,'wmn',False)
  processes['wmn'] += shiftScalesPDF('Zll',tZll,vmW,cut,'wmn',False)
  for p in processes['wmn']:
    regions['wmn'].AddProcess(p)
  factory.AddRegion(regions['wmn'])


# wmn_fail
if enable('wmn_fail'):
  regions['wmn_fail'] = root.Region('wmn_fail')
  cut = sel.cuts['wmn_fail']
  weight = '%s'%(sel.weights['wmn_fail']%lumi)
  PInfo('makeLimitForest.py',cut)
  PInfo('makeLimitForest.py',weight)
  processes['wmn_fail'] = [
    root.Process('Data',tMET,vmW,dataCut(cut,sel.metTrigger),'1'),
    root.Process('Wlv',tWlv,vmW,cut,weight),
    root.Process('Zll',tZll,vmW,cut,weight),
    root.Process('ttbar',tTTbar,vmW,cut,weight),
    root.Process('ST',tST,vmW,cut,weight),
    root.Process('Diboson',tVV,vmW,cut,weight),
    root.Process('QCD',tQCD,vmW,cut,weight),
  ]
  processes['wmn_fail'] += shiftBtags('ttbar',tTTbar,vmW,cut,'wmn_fail',False)
  processes['wmn_fail'] += shiftBtags('Wlv',tWlv,vmW,cut,'wmn_fail',False)
  processes['wmn_fail'] += shiftBtags('ST',tST,vmW,cut,'wmn_fail',False)
  processes['wmn_fail'] += shiftBtags('Zll',tZll,vmW,cut,'wmn_fail',False)
  processes['wmn_fail'] += shiftBtags('Diboson',tVV,vmW,cut,'wmn_fail',False)
  processes['wmn_fail'] += shiftBtags('QCD',tQCD,vmW,cut,'wmn_fail',False)
  processes['wmn_fail'] += shiftScalesPDF('ttbar',tTTbar,vmW,cut,'wmn_fail',False)
  processes['wmn_fail'] += shiftScalesPDF('Wlv',tWlv,vmW,cut,'wmn_fail',False)
  processes['wmn_fail'] += shiftScalesPDF('Zll',tZll,vmW,cut,'wmn_fail',False)
  for p in processes['wmn_fail']:
    regions['wmn_fail'].AddProcess(p)
  factory.AddRegion(regions['wmn_fail'])

# wen
if enable('wen'):
  regions['wen'] = root.Region('wen')
  cut = sel.cuts['wen']
  weight = '%s'%(sel.weights['wen']%lumi)
  weight_ttbar = weight + ttbar_mistag_SF
  PInfo('makeLimitForest.py',cut)
  PInfo('makeLimitForest.py',weight)
  processes['wen'] = [
    root.Process('Data',tSingleEle,vmW,dataCut(cut,sel.eleTrigger),'1'),
    root.Process('Wlv',tWlv,vmW,cut,weight),
    root.Process('Zll',tZll,vmW,cut,weight),
    root.Process('ttbar',tTTbar,vmW,cut,weight_ttbar),
    root.Process('ST',tST,vmW,cut,weight),
    root.Process('Diboson',tVV,vmW,cut,weight),
    root.Process('QCD',tQCD,vmW,cut,weight),
  ]
  processes['wen'] += shiftBtags('ttbar',tTTbar,vmW,cut,'wen',2)
  processes['wen'] += shiftBtags('Wlv',tWlv,vmW,cut,'wen',False)
  processes['wen'] += shiftBtags('ST',tST,vmW,cut,'wen',False)
  processes['wen'] += shiftBtags('Zll',tZll,vmW,cut,'wen',False)
  processes['wen'] += shiftBtags('Diboson',tVV,vmW,cut,'wen',False)
  processes['wen'] += shiftBtags('QCD',tQCD,vmW,cut,'wen',False)
  processes['wen'] += shiftScalesPDF('ttbar',tTTbar,vmW,cut,'wen',2)
  processes['wen'] += shiftScalesPDF('Wlv',tWlv,vmW,cut,'wen',False)
  processes['wen'] += shiftScalesPDF('Zll',tZll,vmW,cut,'wen',False)
  for p in processes['wen']:
    regions['wen'].AddProcess(p)
  factory.AddRegion(regions['wen'])


# wen_fail
if enable('wen_fail'):
  regions['wen_fail'] = root.Region('wen_fail')
  cut = sel.cuts['wen_fail']
  weight = '%s'%(sel.weights['wen_fail']%lumi)
  PInfo('makeLimitForest.py',cut)
  PInfo('makeLimitForest.py',weight)
  processes['wen_fail'] = [
    root.Process('Data',tSingleEle,vmW,dataCut(cut,sel.eleTrigger),'1'),
    root.Process('Wlv',tWlv,vmW,cut,weight),
    root.Process('Zll',tZll,vmW,cut,weight),
    root.Process('ttbar',tTTbar,vmW,cut,weight),
    root.Process('ST',tST,vmW,cut,weight),
    root.Process('Diboson',tVV,vmW,cut,weight),
    root.Process('QCD',tQCD,vmW,cut,weight),
  ]
  processes['wen_fail'] += shiftBtags('ttbar',tTTbar,vmW,cut,'wen_fail',False)
  processes['wen_fail'] += shiftBtags('Wlv',tWlv,vmW,cut,'wen_fail',False)
  processes['wen_fail'] += shiftBtags('ST',tST,vmW,cut,'wen_fail',False)
  processes['wen_fail'] += shiftBtags('Zll',tZll,vmW,cut,'wen_fail',False)
  processes['wen_fail'] += shiftBtags('Diboson',tVV,vmW,cut,'wen_fail',False)
  processes['wen_fail'] += shiftBtags('QCD',tQCD,vmW,cut,'wen_fail',False)
  processes['wen_fail'] += shiftScalesPDF('ttbar',tTTbar,vmW,cut,'wen_fail',False)
  processes['wen_fail'] += shiftScalesPDF('Wlv',tWlv,vmW,cut,'wen_fail',False)
  processes['wen_fail'] += shiftScalesPDF('Zll',tZll,vmW,cut,'wen_fail',False)
  for p in processes['wen_fail']:
    regions['wen_fail'].AddProcess(p)
  factory.AddRegion(regions['wen_fail'])


# tm
if enable('tm'):
  regions['tm'] = root.Region('tm')
  cut = sel.cuts['tm']
  weight = '%s'%(sel.weights['tm']%lumi)
  weight_ttbar = weight + ttbar_mistag_SF
  PInfo('makeLimitForest.py',cut)
  PInfo('makeLimitForest.py',weight)
  processes['tm'] = [
    root.Process('Data',tMET,vmW,dataCut(cut,sel.metTrigger),'1'),
    root.Process('Wlv',tWlv,vmW,cut,weight),
    root.Process('Zll',tZll,vmW,cut,weight),
    root.Process('ttbar',tTTbar,vmW,cut,weight_ttbar),
    root.Process('ST',tST,vmW,cut,weight),
    root.Process('Diboson',tVV,vmW,cut,weight),
    root.Process('QCD',tQCD,vmW,cut,weight),
  ]
  processes['tm'] += shiftBtags('ttbar',tTTbar,vmW,cut,'tm',2)
  processes['tm'] += shiftBtags('Wlv',tWlv,vmW,cut,'tm',False)
  processes['tm'] += shiftBtags('ST',tST,vmW,cut,'tm',False)
  processes['tm'] += shiftBtags('Zll',tZll,vmW,cut,'tm',False)
  processes['tm'] += shiftBtags('Diboson',tVV,vmW,cut,'tm',False)
  processes['tm'] += shiftBtags('QCD',tQCD,vmW,cut,'tm',False)
  processes['tm'] += shiftScalesPDF('ttbar',tTTbar,vmW,cut,'tm',2)
  processes['tm'] += shiftScalesPDF('Wlv',tWlv,vmW,cut,'tm',False)
  processes['tm'] += shiftScalesPDF('Zll',tZll,vmW,cut,'tm',False)
  for p in processes['tm']:
    regions['tm'].AddProcess(p)
  factory.AddRegion(regions['tm'])

# te
if enable('te'):
  regions['te'] = root.Region('te')
  cut = sel.cuts['te']
  weight = '%s'%(sel.weights['te']%lumi)
  weight_ttbar = weight + ttbar_mistag_SF
  PInfo('makeLimitForest.py',cut)
  PInfo('makeLimitForest.py',weight)
  processes['te'] = [
    root.Process('Data',tSingleEle,vmW,dataCut(cut,sel.eleTrigger),'1'),
    root.Process('Wlv',tWlv,vmW,cut,weight),
    root.Process('Zll',tZll,vmW,cut,weight),
    root.Process('ttbar',tTTbar,vmW,cut,weight_ttbar),
    root.Process('ST',tST,vmW,cut,weight),
    root.Process('Diboson',tVV,vmW,cut,weight),
    root.Process('QCD',tQCD,vmW,cut,weight),
  ]
  processes['te'] += shiftBtags('ttbar',tTTbar,vmW,cut,'te',2)
  processes['te'] += shiftBtags('Wlv',tWlv,vmW,cut,'te',False)
  processes['te'] += shiftBtags('ST',tST,vmW,cut,'te',False)
  processes['te'] += shiftBtags('Zll',tZll,vmW,cut,'te',False)
  processes['te'] += shiftBtags('Diboson',tVV,vmW,cut,'te',False)
  processes['te'] += shiftBtags('QCD',tQCD,vmW,cut,'te',False)
  processes['te'] += shiftScalesPDF('ttbar',tTTbar,vmW,cut,'te',2)
  processes['te'] += shiftScalesPDF('Wlv',tWlv,vmW,cut,'te',False)
  processes['te'] += shiftScalesPDF('Zll',tZll,vmW,cut,'te',False)
  for p in processes['te']:
    regions['te'].AddProcess(p)
  factory.AddRegion(regions['te'])


# zmm
if enable('zmm'):
  regions['zmm'] = root.Region('zmm')
  cut = sel.cuts['zmm']
  weight = '%s'%(sel.weights['zmm']%lumi)
  weight_ttbar = weight + ttbar_mistag_SF
  PInfo('makeLimitForest.py',cut)
  PInfo('makeLimitForest.py',weight)
  processes['zmm'] = [
    root.Process('Data',tMET,vmZ,dataCut(cut,sel.metTrigger),'1'),
    root.Process('Zvv',tZvv,vmZ,cut,weight),
    root.Process('Wlv',tWlv,vmZ,cut,weight),
    root.Process('Zll',tZll,vmZ,cut,weight),
    root.Process('ttbar',tTTbar,vmZ,cut,weight_ttbar),
    root.Process('ST',tST,vmZ,cut,weight),
    root.Process('Diboson',tVV,vmZ,cut,weight),
    root.Process('QCD',tQCD,vmZ,cut,weight),
  ]
  processes['zmm'] += shiftBtags('ttbar',tTTbar,vmZ,cut,'zmm',2)
  processes['zmm'] += shiftBtags('Wlv',tWlv,vmZ,cut,'zmm',False)
  processes['zmm'] += shiftBtags('ST',tST,vmZ,cut,'zmm',False)
  processes['zmm'] += shiftBtags('Zll',tZll,vmZ,cut,'zmm',False)
  processes['zmm'] += shiftBtags('Zvv',tZvv,vmZ,cut,'zmm',False)
  processes['zmm'] += shiftBtags('Diboson',tVV,vmZ,cut,'zmm',False)
  processes['zmm'] += shiftBtags('QCD',tQCD,vmZ,cut,'zmm',False)
  processes['zmm'] += shiftScalesPDF('ttbar',tTTbar,vmZ,cut,'zmm',2)
  processes['zmm'] += shiftScalesPDF('Wlv',tWlv,vmZ,cut,'zmm',False)
  processes['zmm'] += shiftScalesPDF('Zll',tZll,vmZ,cut,'zmm',False)
  processes['zmm'] += shiftScalesPDF('Zvv',tZvv,vmZ,cut,'zmm',False)
  for p in processes['zmm']:
    regions['zmm'].AddProcess(p)
  factory.AddRegion(regions['zmm'])

# zmm_fail
if enable('zmm_fail'):
  regions['zmm_fail'] = root.Region('zmm_fail')
  cut = sel.cuts['zmm_fail']
  weight = '%s'%(sel.weights['zmm_fail']%lumi)
  PInfo('makeLimitForest.py',cut)
  PInfo('makeLimitForest.py',weight)
  processes['zmm_fail'] = [
    root.Process('Data',tMET,vmZ,dataCut(cut,sel.metTrigger),'1'),
    root.Process('Zvv',tZvv,vmZ,cut,weight),
    root.Process('Wlv',tWlv,vmZ,cut,weight),
    root.Process('Zll',tZll,vmZ,cut,weight),
    root.Process('ttbar',tTTbar,vmZ,cut,weight),
    root.Process('ST',tST,vmZ,cut,weight),
    root.Process('Diboson',tVV,vmZ,cut,weight),
    root.Process('QCD',tQCD,vmZ,cut,weight),
  ]
  processes['zmm_fail'] += shiftBtags('ttbar',tTTbar,vmZ,cut,'zmm_fail',False)
  processes['zmm_fail'] += shiftBtags('Wlv',tWlv,vmZ,cut,'zmm_fail',False)
  processes['zmm_fail'] += shiftBtags('ST',tST,vmZ,cut,'zmm_fail',False)
  processes['zmm_fail'] += shiftBtags('Zll',tZll,vmZ,cut,'zmm_fail',False)
  processes['zmm_fail'] += shiftBtags('Zvv',tZvv,vmZ,cut,'zmm_fail',False)
  processes['zmm_fail'] += shiftBtags('Diboson',tVV,vmZ,cut,'zmm_fail',False)
  processes['zmm_fail'] += shiftBtags('QCD',tQCD,vmZ,cut,'zmm_fail',False)
  processes['zmm_fail'] += shiftScalesPDF('ttbar',tTTbar,vmZ,cut,'zmm_fail',False)
  processes['zmm_fail'] += shiftScalesPDF('Wlv',tWlv,vmZ,cut,'zmm_fail',False)
  processes['zmm_fail'] += shiftScalesPDF('Zll',tZll,vmZ,cut,'zmm_fail',False)
  processes['zmm_fail'] += shiftScalesPDF('Zvv',tZvv,vmZ,cut,'zmm_fail',False)
  for p in processes['zmm_fail']:
    regions['zmm_fail'].AddProcess(p)
  factory.AddRegion(regions['zmm_fail'])


# zee
if enable('zee'):
  regions['zee'] = root.Region('zee')
  cut = sel.cuts['zee']
  weight = '%s'%(sel.weights['zee']%lumi)
  weight_ttbar = weight + ttbar_mistag_SF
  PInfo('makeLimitForest.py',cut)
  PInfo('makeLimitForest.py',weight)
  processes['zee'] = [
    root.Process('Data',tSingleEle,vmZ,dataCut(cut,sel.eleTrigger),'1'),
    root.Process('Zvv',tZvv,vmZ,cut,weight),
    root.Process('Wlv',tWlv,vmZ,cut,weight),
    root.Process('Zll',tZll,vmZ,cut,weight),
    root.Process('ttbar',tTTbar,vmZ,cut,weight_ttbar),
    root.Process('ST',tST,vmZ,cut,weight),
    root.Process('Diboson',tVV,vmZ,cut,weight),
    root.Process('QCD',tQCD,vmZ,cut,weight),
  ]
  processes['zee'] += shiftBtags('ttbar',tTTbar,vmZ,cut,'zee',2)
  processes['zee'] += shiftBtags('Wlv',tWlv,vmZ,cut,'zee',False)
  processes['zee'] += shiftBtags('ST',tST,vmZ,cut,'zee',False)
  processes['zee'] += shiftBtags('Zll',tZll,vmZ,cut,'zee',False)
  processes['zee'] += shiftBtags('Zvv',tZvv,vmZ,cut,'zee',False)
  processes['zee'] += shiftBtags('Diboson',tVV,vmZ,cut,'zee',False)
  processes['zee'] += shiftBtags('QCD',tQCD,vmZ,cut,'zee',False)
  processes['zee'] += shiftScalesPDF('ttbar',tTTbar,vmZ,cut,'zee',2)
  processes['zee'] += shiftScalesPDF('Wlv',tWlv,vmZ,cut,'zee',False)
  processes['zee'] += shiftScalesPDF('Zll',tZll,vmZ,cut,'zee',False)
  processes['zee'] += shiftScalesPDF('Zvv',tZvv,vmZ,cut,'zee',False)

  for p in processes['zee']:
    regions['zee'].AddProcess(p)
  factory.AddRegion(regions['zee'])

# zee_fail
if enable('zee_fail'):
  regions['zee_fail'] = root.Region('zee_fail')
  cut = sel.cuts['zee_fail']
  weight = '%s'%(sel.weights['zee_fail']%lumi)
  PInfo('makeLimitForest.py',cut)
  PInfo('makeLimitForest.py',weight)
  processes['zee_fail'] = [
    root.Process('Data',tSingleEle,vmZ,dataCut(cut,sel.eleTrigger),'1'),
    root.Process('Zvv',tZvv,vmZ,cut,weight),
    root.Process('Wlv',tWlv,vmZ,cut,weight),
    root.Process('Zll',tZll,vmZ,cut,weight),
    root.Process('ttbar',tTTbar,vmZ,cut,weight),
    root.Process('ST',tST,vmZ,cut,weight),
    root.Process('Diboson',tVV,vmZ,cut,weight),
    root.Process('QCD',tQCD,vmZ,cut,weight),
  ]
  processes['zee_fail'] += shiftBtags('ttbar',tTTbar,vmZ,cut,'zee_fail',False)
  processes['zee_fail'] += shiftBtags('Wlv',tWlv,vmZ,cut,'zee_fail',False)
  processes['zee_fail'] += shiftBtags('ST',tST,vmZ,cut,'zee_fail',False)
  processes['zee_fail'] += shiftBtags('Zll',tZll,vmZ,cut,'zee_fail',False)
  processes['zee_fail'] += shiftBtags('Zvv',tZvv,vmZ,cut,'zee_fail',False)
  processes['zee_fail'] += shiftBtags('Diboson',tVV,vmZ,cut,'zee_fail',False)
  processes['zee_fail'] += shiftBtags('QCD',tQCD,vmZ,cut,'zee_fail',False)
  processes['zee_fail'] += shiftScalesPDF('ttbar',tTTbar,vmZ,cut,'zee_fail',False)
  processes['zee_fail'] += shiftScalesPDF('Wlv',tWlv,vmZ,cut,'zee_fail',False)
  processes['zee_fail'] += shiftScalesPDF('ST',tST,vmZ,cut,'zee_fail',False)
  processes['zee_fail'] += shiftScalesPDF('Zll',tZll,vmZ,cut,'zee_fail',False)
  processes['zee_fail'] += shiftScalesPDF('Zvv',tZvv,vmZ,cut,'zee_fail',False)
  processes['zee_fail'] += shiftScalesPDF('Diboson',tVV,vmZ,cut,'zee_fail',False)
  processes['zee_fail'] += shiftScalesPDF('QCD',tQCD,vmZ,cut,'zee_fail',False)
  
  


  for p in processes['zee_fail']:
    regions['zee_fail'].AddProcess(p)
  factory.AddRegion(regions['zee_fail'])

# photon
if enable('pho'):
  regions['pho'] = root.Region('pho')
  cut = sel.cuts['pho']
  weight = '%s'%(sel.weights['pho']%lumi)
  PInfo('makeLimitForest.py',cut)
  PInfo('makeLimitForest.py',weight)
  processes['pho'] = [
    root.Process('Data',tSinglePho,vmA,dataCut(cut,sel.phoTrigger),'1'),
    root.Process('Pho',tPho,vmA,cut,weight),
    # root.Process('QCD',tSinglePho,vmA,dataCut(cut,phoTrigger),'photonPurityWeight'),
    root.Process('QCD',tQCD,vmA,cut,weight),
  ]
  processes['pho'] += shiftBtags('Pho',tPho,vmA,cut,'pho',False)
  processes['pho'] += shiftBtags('QCD',tQCD,vmA,cut,'pho',False)
  processes['pho'] += shiftScalesPDF('Pho',tPho,vmA,cut,'pho',False)

  for p in processes['pho']:
    regions['pho'].AddProcess(p)
  factory.AddRegion(regions['pho'])


PInfo('makeLimitForest','Starting '+str(toProcess))
factory.Run()
PInfo('makeLimitForest','Finishing '+str(toProcess))

factory.Output()

