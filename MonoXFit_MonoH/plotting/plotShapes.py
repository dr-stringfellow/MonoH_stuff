#!/usr/bin/env python

from sys import argv
argv = []

import ROOT as root
import plotConfig as cfg

fTemplates = root.TFile('../combined_model.root')

counter=0
#category = 'monotop_loose'
category = 'monotop'

def mycanvas():
  global counter
  counter += 1
  return root.TCanvas('c%i'%(counter),'c%i'%(counter),600,600)


def getDivided(dirname,central,uncert,linecolor):
  fTemplates.cd(dirname)
  centralHist = fTemplates.Get(dirname+central)
#  print central+'_'+uncert+'_Up'
#  fTemplates.ls()
  upHist = fTemplates.Get(dirname+central+'_'+uncert+'_Up')
  downHist = fTemplates.Get(dirname+central+'_'+uncert+'_Down')
#  print centralHist,upHist
  upDivided = upHist.Clone(); upDivided.Divide(centralHist)
  downDivided = downHist.Clone(); downDivided.Divide(centralHist)
  maxval = 1+2*(max(upDivided.GetMaximum(),downDivided.GetMaximum())-1)
  minval = 1-1.2*(1-min(upDivided.GetMinimum(),downDivided.GetMinimum()))
  #maxval = 1.4*max(upDivided.GetMaximum(),downDivided.GetMaximum())
  #minval = 0.8*min(upDivided.GetMinimum(),downDivided.GetMinimum())
  for hist in [upDivided,downDivided]:
    hist.SetLineColor(linecolor)
    hist.SetStats(0)
    hist.SetMaximum(maxval)
    hist.SetMinimum(minval)
    hist.SetLineWidth(2)
  return upDivided,downDivided

def getBinDivided(dirname,central,uncert,linecolor):
  centralHist = fTemplates.Get(dirname+central)
  upDivided = centralHist.Clone()
  downDivided = centralHist.Clone()
  for iB in xrange(centralHist.GetNbinsX()):
    upHist = fTemplates.Get(dirname+central+'_'+uncert+'_bin%i_Up'%(iB))
    downHist = fTemplates.Get(dirname+central+'_'+uncert+'_bin%i_Down'%(iB))
    upDivided.SetBinContent(iB+1,upHist.GetBinContent(iB+1))
    downDivided.SetBinContent(iB+1,downHist.GetBinContent(iB+1))
  upDivided.Divide(centralHist)
  downDivided.Divide(centralHist)
  maxval = 1+2*(max(upDivided.GetMaximum(),downDivided.GetMaximum())-1)
  minval = 1-1.2*(1-min(upDivided.GetMinimum(),downDivided.GetMinimum()))
  for hist in [upDivided,downDivided]:
    hist.SetLineColor(linecolor)
    hist.SetStats(0)
    hist.SetMaximum(maxval)
    hist.SetMinimum(minval)
    hist.SetLineWidth(2)
  return upDivided,downDivided

###

wzcanvas = mycanvas()
dirname = 'Z_constraints_category_%s/'%(category)
central = 'w_weights_%s'%category
leg = root.TLegend(0.7,0.7,0.9,0.9)
upren,downren = getDivided(dirname,central,'wrenscale',1)
upren.SetTitle('Shape variations (W#rightarrowl#nu/Z#rightarrow#nu#nu)')
upren.Draw('hist'); downren.Draw('hist same')
leg.AddEntry(upren,'wrenscale','L')

upfac,downfac = getDivided(dirname,central,'wfacscale',2)
upfac.Draw('hist same'); downfac.Draw('hist same')
leg.AddEntry(upfac,'wfacscale','L')

uppdf,downpdf = getDivided(dirname,central,'wpdf',3)
uppdf.Draw('hist same'); downpdf.Draw('hist same')
leg.AddEntry(uppdf,'PDF','L')

upewk,downewk = getBinDivided(dirname,central,'w_ewk_%s'%(category),4)
upewk.Draw('hist same'); downewk.Draw('hist same')
leg.AddEntry(upewk,'EWK','L')

ones = upewk.Clone(); ones.Divide(upewk);
ones.SetLineStyle(2)
ones.SetLineColor(1)
ones.Draw('hist same')

leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.Draw()

for e in ['pdf','png']:
  wzcanvas.SaveAs(cfg.plotDir+'/'+category+'_wzshapes.'+e)

###

phocanvas = mycanvas()
dirname = 'Z_constraints_category_%s/'%(category)
central = 'photon_weights_%s'%category
leg = root.TLegend(0.7,0.7,0.9,0.9)
upren,downren = getDivided(dirname,central,'renscale',1)
upren.SetTitle('Shape variations (Z#rightarrow#nu#nu/#gamma)')
upren.Draw('hist'); downren.Draw('hist same')
leg.AddEntry(upren,'renscale','L')

upfac,downfac = getDivided(dirname,central,'facscale',2)
upfac.Draw('hist same'); downfac.Draw('hist same')
leg.AddEntry(upfac,'facscale','L')

uppdf,downpdf = getDivided(dirname,central,'pdf',3)
uppdf.Draw('hist same'); downpdf.Draw('hist same')
leg.AddEntry(uppdf,'PDF','L')

upbtag,downbtag = getDivided(dirname,central,'btag',6)
upbtag.Draw('hist same'); downbtag.Draw('hist same')
leg.AddEntry(upbtag,'b-tag','L')

upmistag,downmistag = getDivided(dirname,central,'mistag',7)
upmistag.Draw('hist same'); downmistag.Draw('hist same')
leg.AddEntry(upmistag,'b-mistag','L')

upewk,downewk = getBinDivided(dirname,central,'ewk_%s'%(category),4)
upewk.Draw('hist same'); downewk.Draw('hist same')
leg.AddEntry(upewk,'EWK','L')

ones = upewk.Clone(); ones.Divide(upewk);
ones.SetLineStyle(2)
ones.SetLineColor(1)
ones.Draw('hist same')

leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.Draw()

for e in ['pdf','png']:
  phocanvas.SaveAs(cfg.plotDir+'/'+category+'_phoshapes.'+e)


###
zmmcanvas = mycanvas()
dirname = 'Z_constraints_category_%s/'%(category)
central = 'zmm_weights_%s'%category
leg = root.TLegend(0.7,0.7,0.9,0.9)

upsjmistag,downsjmistag = getDivided(dirname,central,'sjmistag',4)
upsjmistag.SetTitle('Shape variations (Z#rightarrow#nu#nu/Z#rightarrow#mu#mu)')
upsjmistag.Draw('hist'); downsjmistag.Draw('hist same')
leg.AddEntry(upsjmistag,'b-sj-mistag','L')

upsjbtag,downsjbtag = getDivided(dirname,central,'sjbtag',5)
upsjbtag.Draw('hist same'); downsjbtag.Draw('hist same')
leg.AddEntry(upsjbtag,'b-sj-tag','L')

upmistag,downmistag = getDivided(dirname,central,'mistag',7)
upmistag.Draw('hist same'); downmistag.Draw('hist same')
leg.AddEntry(upmistag,'b-mistag','L')

upbtag,downbtag = getDivided(dirname,central,'btag',6)
upbtag.Draw('hist same'); downbtag.Draw('hist same')
leg.AddEntry(upbtag,'b-tag','L')

ones.Draw('hist same')

leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.Draw()

for e in ['pdf','png']:
  zmmcanvas.SaveAs(cfg.plotDir+'/'+category+'_zmmshapes.'+e)

###
zeecanvas = mycanvas()
dirname = 'Z_constraints_category_%s/'%(category)
central = 'zee_weights_%s'%category
leg = root.TLegend(0.7,0.7,0.9,0.9)

upsjmistag,downsjmistag = getDivided(dirname,central,'sjmistag',4)
upsjmistag.SetTitle('Shape variations (Z#rightarrow#nu#nu/Z#rightarrow#mu#mu)')
upsjmistag.Draw('hist'); downsjmistag.Draw('hist same')
leg.AddEntry(upsjmistag,'b-sj-mistag','L')

upsjbtag,downsjbtag = getDivided(dirname,central,'sjbtag',5)
upsjbtag.Draw('hist same'); downsjbtag.Draw('hist same')
leg.AddEntry(upsjbtag,'b-sj-tag','L')

upmistag,downmistag = getDivided(dirname,central,'mistag',7)
upmistag.Draw('hist same'); downmistag.Draw('hist same')
leg.AddEntry(upmistag,'b-mistag','L')

upbtag,downbtag = getDivided(dirname,central,'btag',6)
upbtag.Draw('hist same'); downbtag.Draw('hist same')
leg.AddEntry(upbtag,'b-tag','L')

ones.Draw('hist same')

leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.Draw()

for e in ['pdf','png']:
  zeecanvas.SaveAs(cfg.plotDir+'/'+category+'_zeeshapes.'+e)

###

topencanvas = mycanvas()
dirname = 'Top_constraints_category_%s/'%(category)
central = 'topen_weights_%s'%category
leg = root.TLegend(0.7,0.85,0.9,0.9)
upbtag,downbtag = getDivided(dirname,central,'btag',6)
upbtag.SetTitle('Shape variations (t#bar{t}#rightarrowb(l)#nu/t#bar{t}#rightarrowbe#nu)')
upbtag.Draw('hist'); downbtag.Draw('hist same')
leg.AddEntry(upbtag,'btag','L')

ones.Draw('hist same')

leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.Draw()

for e in ['pdf','png']:
  topencanvas.SaveAs(cfg.plotDir+'/'+category+'_topenshapes.'+e)

###

topmncanvas = mycanvas()
dirname = 'Top_constraints_category_%s/'%(category)
central = 'topmn_weights_%s'%category
leg = root.TLegend(0.7,0.85,0.9,0.9)
upbtag,downbtag = getDivided(dirname,central,'btag',6)
upbtag.SetTitle('Shape variations (t#bar{t}#rightarrowb(l)#nu/t#bar{t}#rightarrowb#mu#nu)')
upbtag.Draw('hist'); downbtag.Draw('hist same')
leg.AddEntry(upbtag,'btag','L')

ones.Draw('hist same')

leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.Draw()

for e in ['pdf','png']:
  topmncanvas.SaveAs(cfg.plotDir+'/'+category+'_topmnshapes.'+e)





