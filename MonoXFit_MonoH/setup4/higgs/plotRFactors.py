from ROOT import *
from array import array
from tdrStyle import *
setTDRStyle()

def plotRFactors(process):

  f = TFile('mono-x.root','READ')

  if (process=='zjets'):
    num = f.Get("category_monojet/signal_zjets")
    den = f.Get("category_monojet/Zmm_zll")
    den_e = f.Get("category_monojet/Zee_zll")
    label = "R_{Z}"
  elif (process=='gjets'):
    num = f.Get("category_monojet/signal_zjets")
    den = f.Get("category_monojet/gjets_gjets")
    label = "R_{#gamma}"
  elif (process=='wjets'):
    num = f.Get("category_monojet/signal_wjets")
    den = f.Get("category_monojet/Wmn_wjets")
    den_e = f.Get("category_monojet/Wen_wjets")
    label = "R_{W}"
  elif (process=='zwjets'):
    num = f.Get("category_monojet/signal_zjets")
    den = f.Get("category_monojet/signal_wjets")
    label = "R_{Z/W}"


  ratio = num.Clone("ratio")
  ratio.Divide(den)

  for b in range(num.GetNbinsX()+1):
    print num.GetBinContent(b), den.GetBinContent(b), ratio.GetBinContent(b)


  
  if process is 'wjets' or process is 'zjets':
    ratio2 = num.Clone("ratio2")
    ratio2.Divide(den_e)

  gStyle.SetOptStat(0)

  c = TCanvas("c","c",1000,800)  
  c.SetTopMargin(0.06)
  c.cd()
  c.SetRightMargin(0.04)
  c.SetTopMargin(0.07)
  c.SetLeftMargin(0.12)


  dummy = den.Clone("dummy")
  for i in range(1,dummy.GetNbinsX()):
    dummy.SetBinContent(i,0.01)
  dummy.SetFillColor(0)
  dummy.SetLineColor(0)
  dummy.SetLineWidth(0)
  dummy.SetMarkerSize(0)
  dummy.SetMarkerColor(0) 
  dummy.GetYaxis().SetTitle(label)
  dummy.GetYaxis().SetTitleSize(0.4*c.GetLeftMargin())
  dummy.GetXaxis().SetTitle("U [GeV]")
  dummy.GetXaxis().SetTitleSize(0.4*c.GetBottomMargin())
  #dummy.SetMaximum(1.5*ratio.GetMaximum())
  #dummy.SetMinimum(0.5*ratio.GetMinimum())
  dummy.SetMaximum(2.0*ratio.GetMaximum())
  dummy.SetMinimum(0.5*ratio.GetMinimum())
  dummy.GetYaxis().SetTitleOffset(1.15)
  dummy.Draw()

  ratio.SetLineColor(1)
  ratio.SetLineWidth(2)
  ratio.Draw("ehistsame")
  if process is 'wjets' or process is 'zjets':
    ratio2.Draw("ehistsame")

  
  latex2 = TLatex()
  latex2.SetNDC()
  latex2.SetTextSize(0.8*c.GetTopMargin())
  latex2.SetTextFont(42)
  latex2.SetTextAlign(31) # align right
  latex2.DrawLatex(0.9, 0.94,"13 TeV")
  latex2.SetTextSize(0.8*c.GetTopMargin())
  latex2.SetTextFont(62)
  latex2.SetTextAlign(11) # align right
  latex2.DrawLatex(0.19, 0.85, "CMS")
  latex2.SetTextSize(0.7*c.GetTopMargin())
  latex2.SetTextFont(52)
  latex2.SetTextAlign(11)
  latex2.DrawLatex(0.19, 0.80, "Preliminary")          

  gPad.RedrawAxis()

  c.SaveAs("/afs/cern.ch/user/z/zdemirag/www/Monojet/unblinding/rfactor_"+process+".pdf")
  c.SaveAs("/afs/cern.ch/user/z/zdemirag/www/Monojet/unblinding/rfactor_"+process+".png")
  c.SaveAs("/afs/cern.ch/user/z/zdemirag/www/Monojet/unblinding/rfactor_"+process+".C")
  c.SaveAs("rfactor_"+process+".root")

  f_out = TFile(process+".root","recreate")
  f_out.cd()
  ratio.Write()
  if process is 'wjets' or process is 'zjets':
    ratio2.Write()
  f_out.Close()

  del c
  
plotRFactors("zjets")
plotRFactors("gjets")
plotRFactors("wjets")
plotRFactors("zwjets")
