#!/usr/bin/env python

import ROOT as root
from tdrStyle import *

setTDRStyle()

fIn = root.TFile.Open('../files/monotop-boosted-combo-mar9.root')
signals = [
#           ('Mchi900' ,'M_{V}=900 GeV',2),
#           ('Mchi500' ,'M_{V}=500 GeV',1),
#           ('Mchi-1500' ,'M_{V}=1.5 TeV',2),
#           ('Mchi-900','M_{V}=900 GeV',1),
#           ('Mchi-300' ,'M_{V}=300 GeV',0),
           ('Mres-1900_Mchi-100' ,'M_{S}=1.9 TeV',2),
           ('Mres-1300_Mchi-100' ,'M_{S}=1.3 TeV',1),
           ('Mres-900_Mchi-100' ,'M_{S}=0.9 TeV',0),
#           ('Mres1100_Mchi100' ,'M_{S}=1.1 TeV',1),
#           ('Mres900_Mchi100' ,'M_{S}=0.9 TeV',0),
#           ('Mres1900_Mchi100' ,'M_{S}=1.8 TeV',1),
           ]

signals.reverse()

c = root.TCanvas()
leg = root.TLegend(.55,.7,.9,.9)
leg.SetFillStyle(0)
leg.SetBorderSize(0)
colors = [root.kRed, root.kBlue, root.kBlack, root.kGreen]
hists = []
drawn=False
for sig in signals:
  k = sig[0]
  label = sig[1]
  num = sig[2]
  tsig = fIn.Get(k+'_signal')
  hsig = root.TH1F('hsig'+k,'hsig'+k,25,250,2250)
  tsig.Draw("mt>>hsig"+k,"weight")
  print k,hsig.Integral()
  hsig.SetLineColor(colors[num])
  hsig.SetLineWidth(2)
  hists.append(hsig)
  if not drawn:
    drawn=True
    hsig.SetStats(0)
    hsig.SetTitle('')
    hsig.GetXaxis().SetTitle('M_{T} [GeV]')
    hsig.GetYaxis().SetTitle('Events/40 GeV')
    hsig.SetMaximum(1.5*hsig.GetMaximum())
#    hsig.Draw('hist')
#  else:
#    hsig.Draw('hist same')
  leg.AddEntry(hsig,label,'l')

for iH in xrange(len(hists)):
  if iH==0:
    hists[iH].Draw('hist')
  else:
    hists[iH].Draw('hist same')

latex2 = root.TLatex()
latex2.SetNDC()
latex2.SetTextSize(0.5*c.GetTopMargin())
latex2.SetTextFont(42)
latex2.SetTextAlign(31) # align right
latex2.DrawLatex(0.9, 0.94,"2.32 fb^{-1} (13 TeV)")
latex2.SetTextSize(0.6*c.GetTopMargin())
latex2.SetTextFont(62)
latex2.SetTextAlign(11) # align right
latex2.DrawLatex(0.19, 0.85, "CMS")
latex2.SetTextSize(0.5*c.GetTopMargin())
latex2.SetTextFont(52)
latex2.SetTextAlign(11)
latex2.DrawLatex(0.28, 0.85, "Preliminary")          

leg.Draw()
baseName = '~/public_html/figs/monotop/fits_thq/signals_resonant_mt'
print c
c.SaveAs(baseName+'.png')
c.SaveAs(baseName+'.pdf')
c.SaveAs(baseName+'.C')



