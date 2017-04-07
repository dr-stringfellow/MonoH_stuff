from ROOT import *
from collections import defaultdict
from os import getenv
from array import array
from tdrStyle import *
setTDRStyle()

plotDir = '~/public_html/figs/monotop/fits_smoothed/'
#plotDir = '~/public_html/figs/monotop/fits_unsmoothed/'


new_dic = defaultdict(dict)

def plotUndividedVariations(process,variation,label,varLabel):
  basedir = getenv('CMSSW_BASE') + '/src/MonoX/'     
#  f_data = TFile(basedir+"/mono-x.root","READ")
  f_data = TFile(basedir+"/mono-x-smoothed.root","READ")
#  f_data.cd("category_monotop")

  nominal = f_data.Get('category_monotop/'+process)
  up = f_data.Get('category_monotop/'+process+"_"+variation+"Up")
  down = f_data.Get('category_monotop/'+process+"_"+variation+"Down")

  nominalFlat = nominal.Clone()
  nominalFlatErr = nominalFlat.Clone()
  gStyle.SetOptStat(0)

  c = TCanvas("c","c",600,700)  
  SetOwnership(c,False)
  c.cd()
  c.SetLogy()
#  c.SetBottomMargin(0.3)
  c.SetRightMargin(0.06)
  #c.SetTopMargin(0.07)
  c.SetLeftMargin(0.15)

  nominalFlat.SetLineColor(1)
  nominalFlat.SetLineWidth(1)
  nominalFlat.SetLineStyle(2)
  nominalFlatErr.SetFillColor(kGray+1)
  nominalFlatErr.SetLineWidth(0)
  nominalFlatErr.GetYaxis().SetTitle("#sigma/GeV")
  nominalFlatErr.GetYaxis().SetTitleOffset(1.3)
  nominalFlatErr.Draw("e2")
  nominalFlat.Draw("hist same")
  
  up.SetLineColor(4)
  up.SetLineWidth(1)
  up.Draw("hist same")

  down.SetLineColor(2)
  down.SetLineWidth(1)
  down.Draw("histsame")
  
  legend = TLegend(.5,.75,.90,.90)
  #legend.SetTextSize(0.04)
  legend.AddEntry(nominalFlat,label , "l") 
  legend.AddEntry(nominalFlatErr,"stat uncert" , "f") 
  legend.AddEntry(up,varLabel+" up", "l") 
  legend.AddEntry(down,varLabel+" down", "l") 
  legend.SetShadowColor(0);
  legend.SetFillStyle(0);
  legend.SetBorderSize(0);
  legend.Draw("same")

  latex2 = TLatex()
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

  gPad.RedrawAxis()


  c.SaveAs(plotDir+"variationUndivided"+process+"_"+variation+".png")
  c.SaveAs(plotDir+"variationUndivided"+process+"_"+variation+".pdf")
  c.SaveAs(plotDir+"variationUndivided"+process+"_"+variation+".C")

def plotVariations(process,variation,label,varLabel):
  basedir = getenv('CMSSW_BASE') + '/src/MonoX/'     
  f_data = TFile(basedir+"/mono-x-smoothed.root","READ")
  #f_data = TFile(basedir+"/mono-x.root","READ")
#  f_data.cd("category_monotop")

  nominal = f_data.Get('category_monotop/'+process)
  up = f_data.Get('category_monotop/'+process+"_"+variation+"Up")
  down = f_data.Get('category_monotop/'+process+"_"+variation+"Down")

  nominalFlat = nominal.Clone()
  up.Divide(nominal)
  down.Divide(nominal)
  for iB in xrange(1,nominalFlat.GetNbinsX()+1):
    newErr = nominal.GetBinError(iB)/nominal.GetBinContent(iB)
    nominalFlat.SetBinError(iB,newErr)
    nominalFlat.SetBinContent(iB,1)
  gStyle.SetOptStat(0)

  c = TCanvas("c","c",600,700)  
  SetOwnership(c,False)
  c.cd()
  #c.SetLogy()
  c.SetRightMargin(0.06)
  #c.SetTopMargin(0.07)
  c.SetLeftMargin(0.25)

  maxVal = max(up.GetMaximum(), down.GetMaximum())

  up.SetLineColor(4)
  up.SetLineWidth(2)
  up.GetYaxis().SetTitle('1+#delta#sigma/#sigma')
  up.GetYaxis().SetTitleOffset(3)
  up.SetMinimum(1-(maxVal-1)*2); up.SetMaximum((maxVal-1)*2+1)
  up.Draw("hist")

  nominalFlat.SetLineColor(1)
  nominalFlat.SetLineWidth(1)
  nominalFlat.SetLineStyle(2)
#  nominalFlat.SetMinimum(0.9); nominalFlat.SetMaximum(1.2)
  nominalFlat.Draw("hist same")
  
  down.SetLineColor(2)
  down.SetLineWidth(2)
  down.Draw("histsame")
  
  legend = TLegend(.6,.75,.90,.90)
  #legend.SetTextSize(0.04)
  legend.AddEntry(nominalFlat,label , "l") 
  legend.AddEntry(up,varLabel+" up", "l") 
  legend.AddEntry(down,varLabel+" down", "l") 
  legend.SetShadowColor(0);
  legend.SetFillStyle(0);
  legend.SetBorderSize(0);
  legend.Draw("same")

  latex2 = TLatex()
  latex2.SetNDC()
  latex2.SetTextSize(0.5*c.GetTopMargin())
  latex2.SetTextFont(42)
  latex2.SetTextAlign(31) # align right
  latex2.DrawLatex(0.9, 0.94,"2.32 fb^{-1} (13 TeV)")
  latex2.SetTextSize(0.6*c.GetTopMargin())
  latex2.SetTextFont(62)
  latex2.SetTextAlign(11) # align right
  latex2.DrawLatex(0.25, 0.85, "CMS")
  latex2.SetTextSize(0.5*c.GetTopMargin())
  latex2.SetTextFont(52)
  latex2.SetTextAlign(11)
  latex2.DrawLatex(0.34, 0.85, "Preliminary")          

  gPad.RedrawAxis()


  c.SaveAs(plotDir+"variation"+process+"_"+variation+".png")
  c.SaveAs(plotDir+"variation"+process+"_"+variation+".pdf")
  c.SaveAs(plotDir+"variation"+process+"_"+variation+".C")


'''
plotVariations("dimuon_zll","zjethf","Z#rightarrow#mu#mu+jets","HF fraction")
plotVariations("dielectron_zll","zjethf","Z#rightarrowee+jets","HF fraction")
plotVariations("signal_zjets","zjethf","Z#rightarrow#nu#nu+jets","HF fraction")
plotVariations("singlemuonw_wjets","wjethf","W#rightarrow#mu#nu+jets","HF fraction")
plotVariations("singleelectronw_wjets","wjethf","W#rightarrowe#nu+jets","HF fraction")
plotVariations("signal_wjets","wjethf","W#rightarrow(l)#nu+jets","HF fraction")
plotVariations("photon_gjets","gjethf","#gamma+jets","HF fraction")

plotUndividedVariations("dimuon_zll","zjethf","Z#rightarrow#mu#mu+jets","HF fraction")
plotUndividedVariations("dielectron_zll","zjethf","Z#rightarrowee+jets","HF fraction")
plotUndividedVariations("signal_zjets","zjethf","Z#rightarrow#nu#nu+jets","HF fraction")
plotUndividedVariations("singlemuonw_wjets","wjethf","W#rightarrow#mu#nu+jets","HF fraction")
plotUndividedVariations("singleelectronw_wjets","wjethf","W#rightarrowe#nu+jets","HF fraction")
plotUndividedVariations("signal_wjets","wjethf","W#rightarrow(l)#nu+jets","HF fraction")
plotUndividedVariations("photon_gjets","gjethf","#gamma+jets","HF fraction")

plotVariations("signal_zjets","btag","Z#rightarrow#nu#nu+jets","btag")

plotVariations("singlemuonw_wjets","btag","W#rightarrow#mu#nu+jets","btag")
plotVariations("singlemuontop_wjets","btag","W#rightarrow#mu#nu+jets","btag")
plotVariations("signal_wjets","btag","W#rightarrow(l)#nu+jets","btag")

plotVariations("singlemuontop_ttbar","btag","t#bar{t}#rightarrowb#mu#nu+jets","btag")
plotVariations("signal_ttbar","btag","t#bar{t}#rightarrowb(l)#nu+jets","btag")
plotVariations("singlemuonw_ttbar","btag","t#bar{t}#rightarrowb(#mu)#nu+jets","btag")

plotVariations("signal_zjets","mistag","Z#rightarrow#nu#nu+jets","mistag")
plotVariations("singlemuonw_wjets","mistag","W#rightarrow#mu#nu+jets","mistag")
plotVariations("signal_wjets","mistag","W#rightarrow(l)#nu+jets","mistag")
'''
plotVariations("singlemuonw_wjets","btag","W#rightarrow#mu#nu+jets","btag")
plotVariations("singlemuontop_wjets","btag","W#rightarrow#mu#nu+jets","btag")
plotVariations("signal_wjets","btag","W#rightarrow(l)#nu+jets","btag")

plotVariations("singlemuontop_ttbar","btag","t#bar{t}#rightarrowb#mu#nu+jets","btag")
plotVariations("signal_ttbar","btag","t#bar{t}#rightarrowb(l)#nu+jets","btag")
plotVariations("singlemuonw_ttbar","btag","t#bar{t}#rightarrowb(#mu)#nu+jets","btag")

plotVariations("singlemuonw_wjets","mistag","W#rightarrow#mu#nu+jets","mistag")
plotVariations("singlemuontop_wjets","mistag","W#rightarrow#mu#nu+jets","mistag")
plotVariations("signal_wjets","mistag","W#rightarrow(l)#nu+jets","mistag")

plotVariations("singlemuontop_ttbar","mistag","t#bar{t}#rightarrowb#mu#nu+jets","mistag")
plotVariations("signal_ttbar","mistag","t#bar{t}#rightarrowb(l)#nu+jets","mistag")
plotVariations("singlemuonw_ttbar","mistag","t#bar{t}#rightarrowb(#mu)#nu+jets","mistag")

plotVariations("signal_zjets","mistag","Z#rightarrow#nu#nu+jets","mistag")
plotVariations("signal_zjets","btag","Z#rightarrow#nu#nu+jets","btag")
