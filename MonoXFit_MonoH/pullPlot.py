import ROOT as r
import sys
def pullPlot(fitres,fout):

  fi = fitres.floatParsInit()
  ff = fitres.floatParsFinal()
  
  nnuis = 0
  for i in range(fi.getSize()):
    nuis_pref = fi.at(i)
    name   = nuis_pref.GetName();
    if "nuis" not in name: continue
    nnuis+=1

  hist_pull         = r.TH1F("nuisance_pulls","Post-fit Nuisances;;#theta ",nnuis,0,nnuis)
  hist_pull_eold    = r.TH1F("nuisance_pulls_eold","Nuisances    ;;#theta ",nnuis,0,nnuis)
  hist_pull_1s      = r.TH1F("nuisance_pulls_1s","Nuisances    ;;#theta ",nnuis,0,nnuis)
  canv = r.TCanvas("canv_hist_post_fit_nuisances","",1000,300)

  inuis = 1
  for i in range(fi.getSize()):

    nuis_pref = fi.at(i)
    nuis_post = ff.at(i)
    name   = nuis_pref.GetName();
    if "nuis" not in name: continue

    x = nuis_post.getVal()
    m = nuis_pref.getVal()
    e  = nuis_post.getError()
    eo = 1

    #print name, x-m, e
    hist_pull.SetBinContent(inuis,(x-m))
    hist_pull.SetBinError(inuis,e)
    hist_pull_eold.SetBinContent(inuis,(x-m))
    hist_pull_eold.SetBinError(inuis,eo)

    if abs(x-m)/e > 1: 
      hist_pull_1s.SetBinContent(inuis,(x-m))
      hist_pull_1s.SetBinError(inuis,e)
    else: hist_pull_1s.SetBinContent(inuis,-999)
    hist_pull.GetXaxis().SetBinLabel(inuis,name)
    inuis+=1

  hist_pull.GetYaxis().SetTitle("#theta-#theta_{0}")
  hist_pull.GetYaxis().SetTitleSize(0.05)
  hist_pull.SetMarkerStyle(20)
  hist_pull.SetMarkerSize(1.)
  hist_pull.SetMarkerColor(1)
  hist_pull_eold.SetMarkerSize(0.)
  hist_pull_eold.SetMarkerColor(1)
  hist_pull_eold.SetLineColor(1)
  hist_pull_eold.SetFillColor(r.kGray)
  hist_pull_1s.SetMarkerStyle(20)
  hist_pull_1s.SetMarkerSize(1.)
  hist_pull_1s.SetMarkerColor(2)
  hist_pull_1s.SetLineColor(2)
  hist_pull.SetLineColor(1)
  hist_pull.SetLineWidth(2)
  hist_pull_1s.SetLineWidth(2)
  canv.cd()
  hist_pull.Draw("")
  hist_pull_eold.Draw("E2psame")
  hist_pull.Draw("same")
  hist_pull_1s.Draw("samepel")
  line = r.TLine(0,0,nnuis,0)
  line.SetLineStyle(2)
  line.SetLineColor(1)
  line.Draw()
  #return canv
  canv.RedrawAxis()
  fout.WriteTObject(canv)
  #return canv

"""
f = r.TFile.Open("photon_dimuon_combined_model.root")
fr = f.Get("fitresult_combined_pdf_combinedData")
a = pullPlot(fr)
#a.Draw()
raw_input()
"""
