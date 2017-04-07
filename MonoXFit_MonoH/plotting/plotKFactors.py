#!/usr/bin/env python

import ROOT as root
from tdrStyle import *
from array import array 

setTDRStyle()

fIn = root.TFile.Open('../files/newKfactors/kfactors.root')

def smoothHist(hist,nBins=2):
  smoothedVals = [hist.GetBinContent(1)]
  for iB in xrange(1,hist.GetNbinsX()+1):
    if iB<=nBins or iB>hist.GetNbinsX()-nBins:
      smoothedVals.append(hist.GetBinContent(iB))
      continue
    newVal = 0
    for jB in xrange(-nBins,nBins+1):
      newVal += hist.GetBinContent(iB+jB)
    newVal /= (2.*nBins+1) 
    smoothedVals.append(newVal)
  smoothedVals.append(hist.GetBinContent(hist.GetNbinsX()))
  for iB in xrange(1,hist.GetNbinsX()+1):
    hist.SetBinContent(iB,smoothedVals[iB-1])

def plotCorrections(nloName,ewkName,loName,label):
  c = root.TCanvas()
  leg = root.TLegend(.55,.7,.9,.9)
  leg.SetFillStyle(0)
  leg.SetBorderSize(0)
  c.Clear()
  c.SetLogy()
  if 'G' in nloName:
    hQCD = fIn.Get(nloName+'/nominal_G')
  else:
    hQCD = fIn.Get(nloName+'/nominal')
  hEWK = fIn.Get('EWKcorr/'+ewkName)
  if 'G' in loName:
    hLO  = fIn.Get(loName+'/inv_pt_G')
  else:
    hLO  = fIn.Get(loName+'/inv_pt')

#  for h in [hQCD,hEWK,hLO]:
#    h.Scale(1,'width')

  hLO.GetXaxis().SetTitle('p_{T}^{V} [GeV]')
  hLO.GetYaxis().SetTitle('d#sigma/dp_{T} [pb/GeV]')
  hLO.GetYaxis().SetTitleOffset(1.3)
  hLO.SetMaximum(10*hLO.GetMaximum())
  hLO.SetLineColor(root.kBlack)

  hEWK.SetLineColor(root.kRed)
  hQCD.SetLineColor(root.kBlue)

  hLO.Draw('hist')
  hQCD.Draw('histsame')
  hEWK.Draw('histsame')

  leg.AddEntry(hLO,"LO","l")
  leg.AddEntry(hQCD,"NLO QCD","l")
  leg.AddEntry(hEWK,"NLO QCD+EWK","l")

  latex2 = root.TLatex()
  latex2.SetNDC()
  latex2.SetTextSize(0.5*c.GetTopMargin())
  latex2.SetTextFont(42)
  latex2.SetTextAlign(31) # align right
#  latex2.DrawLatex(0.9, 0.94,"2.32 fb^{-1} (13 TeV)")
  latex2.SetTextSize(0.6*c.GetTopMargin())
  latex2.SetTextFont(62)
  latex2.SetTextAlign(11) # align right
  latex2.DrawLatex(0.19, 0.85, "CMS")
  latex2.SetTextSize(0.5*c.GetTopMargin())
  latex2.SetTextFont(52)
  latex2.SetTextAlign(11)
  latex2.DrawLatex(0.28, 0.85, "Preliminary")          
  latex2.SetTextFont(42)
  latex2.DrawLatex(0.19,0.8,label)

  leg.Draw()
  baseName = '~/public_html/figs/monotop/kfactors/%s'%(ewkName)
  c.SaveAs(baseName+'.png')
  c.SaveAs(baseName+'.pdf')
  c.SaveAs(baseName+'.C')

def plotUpDown(nloName,label,shortName):
  c = root.TCanvas()
  leg = root.TLegend(.55,.7,.9,.9)
  leg.SetFillStyle(0)
  leg.SetBorderSize(0)
  c.Clear()
  suffix = ''
  if 'G' in nloName:
    suffix = '_G'
  hNominal = fIn.Get(nloName+'/nominal'+suffix)
  hFactUp = fIn.Get(nloName+'/fact_up'+suffix)
  hFactDown = fIn.Get(nloName+'/fact_down'+suffix)
  hRenUp = fIn.Get(nloName+'/ren_up'+suffix)
  hRenDown = fIn.Get(nloName+'/ren_down'+suffix)
  hPDF = fIn.Get(nloName+'/PDF')

  for h in [hFactUp,hFactDown,hRenUp,hRenDown]:
    h.Divide(hNominal)
    smoothHist(h)

  hFactUp.SetLineColor(6); hFactDown.SetLineColor(6)
  hRenUp.SetLineColor(7); hRenDown.SetLineColor(7)
  hPDFUp = hPDF.Clone('pdfUp'); hPDFDown = hPDF.Clone('pdfDown')
  for iB in xrange(1,hPDF.GetNbinsX()+1):
    shift = hPDF.GetBinContent(iB)
    hPDFUp.SetBinContent(iB,1+shift)
    hPDFDown.SetBinContent(iB,1-shift)

  smoothHist(hPDFUp); smoothHist(hPDFDown)

  hOne = hNominal.Clone('hone'); hOne.Divide(hNominal);
  hOne.GetXaxis().SetTitle('p_T^{V} [GeV]')
  hOne.GetYaxis().SetTitle('1+#delta#sigma/#sigma')
  hOne.GetYaxis().SetTitleOffset(1.3)
  hOne.SetLineStyle(2)
  hOne.SetLineColor(1)
  hOne.SetMaximum(1.4); hOne.SetMinimum(0.85)

  hOne.Draw('hist')
  for h in [hFactUp,hFactDown,hRenUp,hRenDown,hPDFUp,hPDFDown]:
    h.Draw('histsame')

  leg.AddEntry(hRenUp,"ren. scale","l")
  leg.AddEntry(hFactUp,"fact. scale","l")
  leg.AddEntry(hPDFUp,"PDF","l")

  latex2 = root.TLatex()
  latex2.SetNDC()
  latex2.SetTextSize(0.5*c.GetTopMargin())
  latex2.SetTextFont(42)
  latex2.SetTextAlign(31) # align right
#  latex2.DrawLatex(0.9, 0.94,"2.32 fb^{-1} (13 TeV)")
  latex2.SetTextSize(0.6*c.GetTopMargin())
  latex2.SetTextFont(62)
  latex2.SetTextAlign(11) # align right
  latex2.DrawLatex(0.19, 0.85, "CMS")
  latex2.SetTextSize(0.5*c.GetTopMargin())
  latex2.SetTextFont(52)
  latex2.SetTextAlign(11)
  latex2.DrawLatex(0.28, 0.85, "Preliminary")          
  latex2.SetTextFont(42)
  latex2.DrawLatex(0.19,0.8,label)

  leg.Draw()
  baseName = '~/public_html/figs/monotop/kfactors/uncert%s'%(shortName)
  c.SaveAs(baseName+'.png')
  c.SaveAs(baseName+'.pdf')
  c.SaveAs(baseName+'.C')

plotCorrections('ZJets_012j_NLO','Z','ZJets_LO','Z+jets')
plotCorrections('WJets_012j_NLO','W','WJets_LO','W+jets')
plotCorrections('GJets_1j_NLO','photon','GJets_LO','#gamma+jets')

plotUpDown('ZJets_012j_NLO','Z+jets','Z')
plotUpDown('WJets_012j_NLO','W+jets','W')
plotUpDown('GJets_1j_NLO','#gamma+jets','photon')
