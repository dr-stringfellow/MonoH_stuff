#!/usr/bin/env python

from os import system,environ
from re import sub
from sys import argv
from argparse import ArgumentParser
from array import array

parser = ArgumentParser(description='perform 2d scan')
parser.add_argument('template',metavar='template',type=str,default='tmpl.txt')
parser.add_argument('--mMed',type=int,default=None)
parser.add_argument('--mChi',type=int,default=None)
parser.add_argument('--isRes',dest='isRes',action='store_true')
parser.add_argument('--isFCNC',dest='isRes',action='store_false')
parser.add_argument('--infile',type=str,metavar='infile')
parser.set_defaults(isRes=False)
args = parser.parse_args()
argv = []

import ROOT as root
root.gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ");
root.gSystem.AddIncludePath("-I$ROOFITSYS/include");
root.gSystem.Load("libRooFit.so")
root.gSystem.Load("libRooFitCore.so")
from HiggsAnalysis.CombinedLimit.ModelTools import *

class Model():
    def __init__(self,mMed,mChi,isRes):
        self.mMed=mMed
        self.mChi=mChi
        self.isRes=isRes
        if isRes:
            self.name = 'scalar_%i_%i'%(mMed,mChi)
        else:
            #self.name = 'monotop-nr-v3-%i-%i_med-%i_dm-%i'%(mMed,mChi,mMed,mChi)
            #self.name = 'MonoTop_%i_%i_0.25_1.0_801'%(mMed,mChi)
            self.name = '%i_%i'%(mMed,mChi)

def makeHists(model):
    name_ = sub('-','_',sub('\.','p',model.name))
    fout = root.TFile(name_+'_model.root','RECREATE')
    bins = array('f',[250,280,310,350,400,450,600,1000])
    N = len(bins)-1
    fin = root.TFile(args.infile)
    #fin = root.TFile(environ['PANDA_FLATDIR']+'/limits/limitForest.root')
    #fin = root.TFile('/afs/cern.ch/user/s/snarayan/work/skims/monotop_limits_v1/'+model.name+'.root')

    wspace = root.RooWorkspace("signalws")
#  wspace._import = SafeWorkspaceImporter(wspace)

    fout.cd()
    counter=0
    tags = {
            'loose_' : 'top_ecf_bdt>0.1 && top_ecf_bdt<0.45',
            '' : 'top_ecf_bdt>0.45',
            }

    fhists = root.TFile('signalmodel.root','RECREATE')

    vmets = {}

    for tag_label,tag in tags.iteritems():
        vmet = root.RooRealVar('min(999.9999,met)','min(999.9999,met)',250,1000)
        if 'loose' in tag_label:
            vmet.SetName('min(999.9999,met)_monotop_loose')
        else:
            vmet.SetName('min(999.9999,met)_monotop')
        vmet.setMin(250); vmet.setMax(1000)
        getattr(wspace,'import')(vmet,root.RooFit.RecycleConflictNodes())
        vmets[tag_label] = vmet

        for syst in ['','_btagUp','_btagDown','_mistagUp','_mistagDown',
                        '_sjbtagUp','_sjbtagDown','_sjmistagUp','_sjmistagDown']:
            tin = fin.Get(model.name+'_signal'+syst)
            hist = root.TH1F('h%i'%counter,'h',N,bins)
            tin.Draw('min(met,999.9999)>>h%i'%counter,'weight*(met>250 && %s)'%tag)

            print model.name,name_,syst,hist.Integral(),tin.GetEntries(),hist.GetEntries()

            dhist = root.RooDataHist('monotop_%ssignal_%s%s'%(tag_label,name_,syst),
                                     '%ssignal %s %s'%(tag_label,name_,syst),
                                     root.RooArgList(vmet),
                                     hist)
            getattr(wspace,'import')(dhist,root.RooFit.RecycleConflictNodes())

            # histsToWrite['hmonotop_%ssignal_%s%s'%(tag_label,name_,syst)] = hist
            fhists.WriteTObject(hist,'hmonotop_%ssignal_%s%s'%(tag_label,name_,syst))
            counter += 1

    fhists.Close()

    fout.Close()
    wspace.writeToFile(name_+'_dmodel.root')
    fout = root.TFile(name_+'_dmodel.root')
    fout.ls()
    fout.Close()


def run(model,runObserved=True):
    label = 'res_' if model.isRes else 'fcnc_'
    label += '%i_%i'%(model.mMed,model.mChi)
    name_ = sub('-','_',sub('\.','p',model.name))
    cmd = "sed 's?XXXX?%s?g' %s > scan_%s.txt"%(name_,args.template,label)
    #cmd = "sed 's?XXXX?%s?g' %s > combined_%s.txt"%(sub('1.0','1',model.name),args.template,label)
    system(cmd)
    cmd = "sed -i 's?signal_model\.root?%s_dmodel\.root?g' scan_%s.txt"%(name_,label)
    system(cmd)
    makeHists(model)
    cmd = "combine -M Asymptotic scan_%s.txt -n %s"%(label,label)
    print cmd
    system(cmd)
    # flimit = root.TFile('higgsCombinefcnc_%i_%i.Asymptotic.mH120.root'%(model.mMed,model.mChi))
    # tlimit = flimit.Get('limit')
    # tlimit.GetEntry(2)

    # system("combine -M Asymptotic combined_%s.txt -n %s -m %i"%(label,model.mMed*1000+mChi))

model = Model(args.mMed,args.mChi,args.isRes)
run(model,False)

