#from combineControlRegions import *
from pullPlot import pullPlot
from counting_experiment import *

import ROOT as r 
r.gROOT.SetBatch(1)
r.gROOT.ProcessLine(".L diagonalizer.cc+")
from ROOT import diagonalizer

fPurity = r.TFile.Open("photonPurity.root")
ptphopurity = fPurity.Get("data")
for b in range(ptphopurity.GetNbinsX()): ptphopurity.SetBinContent(b+1,1-ptphopurity.GetBinContent(b+1))

#fkFactor = r.TFile.Open("/afs/cern.ch/work/n/nckw/public/monojet/Photon_Z_NLO_kfactors_Old.root")
#fkFactor = r.TFile.Open("Photon_Z_NLO_kfactors.root")
fkFactor = r.TFile.Open("Photon_Z_NLO_kfactors_w80pcorr.root")
nlo_pho = fkFactor.Get("pho_NLO_LO")
nlo_zjt = fkFactor.Get("Z_NLO_LO")
nlo_pho_mrUp = fkFactor.Get("pho_NLO_LO_mrUp")
nlo_zjt_mrUp = fkFactor.Get("Z_NLO_LO_mrUp")
nlo_pho_mrDown = fkFactor.Get("pho_NLO_LO_mrDown")
nlo_zjt_mrDown = fkFactor.Get("Z_NLO_LO_mrDown")
nlo_pho_mfUp = fkFactor.Get("pho_NLO_LO_mfUp")
nlo_zjt_mfUp = fkFactor.Get("Z_NLO_LO_mfUp")
nlo_pho_mfDown = fkFactor.Get("pho_NLO_LO_mfDown")
nlo_zjt_mfDown = fkFactor.Get("Z_NLO_LO_mfDown")

nlo_pho_mr2Up = fkFactor.Get("pho_NLO_LO_mr2Up")
nlo_zjt_mr2Up = fkFactor.Get("Z_NLO_LO_mr2Up")
nlo_pho_mr2Down = fkFactor.Get("pho_NLO_LO_mr2Down")
nlo_zjt_mr2Down = fkFactor.Get("Z_NLO_LO_mr2Down")
nlo_pho_mf2Up = fkFactor.Get("pho_NLO_LO_mf2Up")
nlo_zjt_mf2Up = fkFactor.Get("Z_NLO_LO_mf2Up")
nlo_pho_mf2Down = fkFactor.Get("pho_NLO_LO_mf2Down")
nlo_zjt_mf2Down = fkFactor.Get("Z_NLO_LO_mf2Down")

nlo_zjt_pdfUp  = fkFactor.Get("Z_NLO_LO_pdfUp")
nlo_zjt_pdfDown = fkFactor.Get("Z_NLO_LO_pdfDown")

nlo_ewkUp    = fkFactor.Get("EWK_Up")
nlo_ewkDown  = fkFactor.Get("EWK_Dwon")

fFFactor = r.TFile.Open("FP.root")
nlo_FPUp    = fFFactor.Get("FP_Up")
nlo_FPDown  = fFFactor.Get("FP_Down")
print "!!!!!",nlo_ewkUp.GetName()," -- ",nlo_ewkDown.GetName()

def cmodelW(cid,nam,_f,_fOut, out_ws, diag):

  _fin = _f.Get("category_%s"%nam)
  _wspace = _fin.Get("wspace_%s"%nam)
  metname = "mvamet"
  gvptname= "genVpt"

  try:
    mt = _wspace.var(metname)
    mt.GetName()

  except:
    metname = "mvamet_"

  # First we need to re-build the nominal templates from the datasets modifying the weights
  targetmc     = _fin.Get("signal_wjets")
  controlmc    = _fin.Get("singlemuon_wjets")  # defines in / out acceptance

  WScales = targetmc.Clone(); WScales.SetName("wmn_weights_%s"%nam)
  WScales.Divide(controlmc)
  _fOut.WriteTObject(WScales)
  _bins = []  # take bins from some histogram
  for b in range(targetmc.GetNbinsX()+1):
    _bins.append(targetmc.GetBinLowEdge(b+1))

  CRs = [
   Channel("W#rightarrow(#mu#nu)+jet",_wspace,out_ws,cid,0,_wspace.data("singlemuon_data"),WScales,"singlemuon_all_background")  # stupid linear fit of Purities, should move to flat 
  ]
  #Add Systematic ? This time we add them as nuisance parameters.

  CRs[0].add_nuisance("pdf_CT10",0.006)
  CRs[0].add_nuisance("CMS_eff_m",0.01)
  CRs[0].add_nuisance("xs_backgrounds",0.1,True)   # is a background systematic

  for b in range(targetmc.GetNbinsX()):
    err = WScales.GetBinError(b+1)
    if not WScales.GetBinContent(b+1)>0: continue 
    relerr = err/WScales.GetBinContent(b+1)
    if relerr<0.01: continue
    byb_u = WScales.Clone(); byb_u.SetName("wmn_weights_%s_%s_stat_error_%s_bin%d_Up"%(nam,nam,"singlemuonCR",b))
    byb_u.SetBinContent(b+1,WScales.GetBinContent(b+1)+err)
    byb_d = WScales.Clone(); byb_d.SetName("wmn_weights_%s_%s_stat_error_%s_bin%d_Down"%(nam,nam,"singlemuonCR",b))
    byb_d.SetBinContent(b+1,WScales.GetBinContent(b+1)-err)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    print "Adding an error -- ", byb_u.GetName(),err
    CRs[0].add_nuisance_shape("%s_stat_error_%s_bin%d"%(nam,"singlemuonCR",b),_fOut)

  # Make bin-to-bin errors ?!
  # We want to make a combined model which performs a simultaneous fit in all three categories so first step is to build a combined model in all three 
  cat = Category("WJets",cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,"signal_wjets",CRs,diag)
  cat.addVar("jet1pt",25,150,1000)
  cat.addVar("mt",30,50,200)
  cat.addVar("njets",10,0,10)
  cat.addVar("lep1pt",25,0,500)
  cat.addTarget("singlemuon_wjets",0)
  return cat

def cmodel(cid,nam,_f,_fOut, out_ws, diag):

  _fin = _f.Get("category_%s"%nam)

  _wspace = _fin.Get("wspace_%s"%nam)
  _photon_datasetname = "photon_data"
  _gjet_mcname 	      = "photon_gjet"
  _dimuon_datasetname = "dimuon_data"
  _dimuon_backgroundsname = "dimuon_all_background"

  metname = "mvamet"
  gvptname= "genVpt"
  wvarname= "weight"
  try:
    mt = _wspace.var(metname)
    mt.GetName()
  except:
    metname = "mvamet_"
    gvptname = "genVpt_"
    wvarname = "weight_"

  # First we need to re-build the nominal templates from the datasets modifying the weights
  target = _fin.Get("signal_zjets")
  Zmm = _fin.Get("dimuon_zll")
  GJet = _fin.Get("photon_gjet")
  ZmmScales = target.Clone(); ZmmScales.SetName("zmm_weights_%s"%nam)
  # run through 3 datasets, photon, etc and generate a template from histograms 
  # We only nned to make NLO versions of Z(vv) and Photon :) 
  # This class lets us run through corrections 
  #diag = diagonalizer(_wspace)
 
  #Loop Over Systematics also?
  Pho = target.Clone(); Pho.SetName("photon_weights_denom_%s"%nam)
  for b in range(Pho.GetNbinsX()): Pho.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho,nlo_pho,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv = target.Clone(); Zvv.SetName("photon_weights_nom_%s"%nam)
  for b in range(Zvv.GetNbinsX()): Zvv.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv,nlo_zjt,gvptname,metname,_wspace.data("signal_zjets"))

  PhotonOverZ = Pho.Clone(); PhotonOverZ.SetName("PhotonOverZNLO")
  PhotonOverZ.Divide(Zvv)
  PhotonOverZ.Multiply(target)
  PhotonOverZ.Divide(GJet)
  diag.generateWeightedDataset("photon_gjet_nlo",PhotonOverZ,wvarname,metname,_wspace,"photon_gjet")

  PhotonSpectrum = Pho.Clone(); PhotonSpectrum.SetName("photon_spectrum_%s_"%nam)
  ZvvSpectrum 	 = Zvv.Clone(); ZvvSpectrum.SetName("zvv_spectrum_%s_"%nam)
  ZmmSpectrum 	 = ZmmScales.Clone(); ZmmSpectrum.SetName("zmm_spectrum_%s_"%nam)
  _fOut.WriteTObject( PhotonSpectrum )
  _fOut.WriteTObject( ZvvSpectrum )
  _fOut.WriteTObject( ZmmSpectrum )

  #################################################################################################################
  # now do systematic parts
  Pho_mrUp = target.Clone(); Pho.SetName("photon_weights_denom_mrUp_%s"%nam)
  for b in range(Pho_mrUp.GetNbinsX()): Pho_mrUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_mrUp,nlo_pho_mrUp,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv_mrUp = target.Clone(); Zvv_mrUp.SetName("photon_weights_nom_mrUp_%s"%nam)
  for b in range(Zvv_mrUp.GetNbinsX()):Zvv_mrUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_mrUp,nlo_zjt_mrUp,gvptname,metname,_wspace.data("signal_zjets"))

  Pho_mrDown = target.Clone(); Pho.SetName("photon_weights_denom_mrDown_%s"%nam)
  for b in range(Pho_mrDown.GetNbinsX()): Pho_mrDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_mrDown,nlo_pho_mrDown,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv_mrDown = target.Clone(); Zvv_mrDown.SetName("photon_weights_nom_mrDown_%s"%nam)
  for b in range(Zvv_mrDown.GetNbinsX()): Zvv_mrDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_mrDown,nlo_zjt_mrDown,gvptname,metname,_wspace.data("signal_zjets"))

  Pho_mfUp = target.Clone(); Pho.SetName("photon_weights_denom_mfUp_%s"%nam)
  for b in range(Pho_mfUp.GetNbinsX()): Pho_mfUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_mfUp,nlo_pho_mfUp,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv_mfUp = target.Clone(); Zvv_mfUp.SetName("photon_weights_nom_mfUp_%s"%nam)
  for b in range(Zvv_mfUp.GetNbinsX()): Zvv_mfUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_mfUp,nlo_zjt_mfUp,gvptname,metname,_wspace.data("signal_zjets"))

  Pho_mfDown = target.Clone(); Pho.SetName("photon_weights_denom_mfDown_%s"%nam)
  for b in range(Pho_mfDown.GetNbinsX()): Pho_mfDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_mfDown,nlo_pho_mfDown,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv_mfDown = target.Clone(); Zvv_mfDown.SetName("photon_weights_nom_mfDown_%s"%nam)
  for b in range(Zvv_mfDown.GetNbinsX()): Zvv_mfDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_mfDown,nlo_zjt_mfDown,gvptname,metname,_wspace.data("signal_zjets"))

  Pho_mr2Up = target.Clone(); Pho.SetName("photon_weights_denom_mr2Up_%s"%nam)
  for b in range(Pho_mr2Up.GetNbinsX()): Pho_mr2Up.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_mr2Up,nlo_pho_mr2Up,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv_mr2Up = target.Clone(); Zvv_mr2Up.SetName("photon_weights_nom_mr2Up_%s"%nam)
  for b in range(Zvv_mr2Up.GetNbinsX()):Zvv_mr2Up.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_mr2Up,nlo_zjt_mr2Up,gvptname,metname,_wspace.data("signal_zjets"))

  Pho_mr2Down = target.Clone(); Pho.SetName("photon_weights_denom_mr2Down_%s"%nam)
  for b in range(Pho_mr2Down.GetNbinsX()): Pho_mr2Down.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_mr2Down,nlo_pho_mr2Down,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv_mr2Down = target.Clone(); Zvv_mr2Down.SetName("photon_weights_nom_mr2Down_%s"%nam)
  for b in range(Zvv_mr2Down.GetNbinsX()): Zvv_mr2Down.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_mr2Down,nlo_zjt_mr2Down,gvptname,metname,_wspace.data("signal_zjets"))

  Pho_mf2Up = target.Clone(); Pho.SetName("photon_weights_denom_mf2Up_%s"%nam)
  for b in range(Pho_mf2Up.GetNbinsX()): Pho_mf2Up.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_mf2Up,nlo_pho_mf2Up,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv_mf2Up = target.Clone(); Zvv_mf2Up.SetName("photon_weights_nom_mf2Up_%s"%nam)
  for b in range(Zvv_mf2Up.GetNbinsX()): Zvv_mf2Up.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_mf2Up,nlo_zjt_mf2Up,gvptname,metname,_wspace.data("signal_zjets"))

  Pho_mf2Down = target.Clone(); Pho.SetName("photon_weights_denom_mf2Down_%s"%nam)
  for b in range(Pho_mf2Down.GetNbinsX()): Pho_mf2Down.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_mf2Down,nlo_pho_mf2Down,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv_mf2Down = target.Clone(); Zvv_mf2Down.SetName("photon_weights_nom_mf2Down_%s"%nam)
  for b in range(Zvv_mf2Down.GetNbinsX()): Zvv_mf2Down.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_mf2Down,nlo_zjt_mf2Down,gvptname,metname,_wspace.data("signal_zjets"))

  Zvv_pdfDown = target.Clone(); Zvv_pdfDown.SetName("photon_weights_nom_pdfDown_%s"%nam)
  for b in range(Zvv_pdfDown.GetNbinsX()): Zvv_pdfDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_pdfDown,nlo_zjt_pdfDown,gvptname,metname,_wspace.data("signal_zjets"))
  Zvv_pdfUp = target.Clone(); Zvv_pdfUp.SetName("photon_weights_nom_pdfUp_%s"%nam)
  for b in range(Zvv_pdfUp.GetNbinsX()): Zvv_pdfUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_pdfUp,nlo_zjt_pdfUp,gvptname,metname,_wspace.data("signal_zjets"))

  # Notice that the EWKUp was calculated on the g/Z ratio and Down is its inverse, so since we are 
  # here going to correct the Z, we using the Down as the Up :)
  Zvv_ewkDown = target.Clone(); Zvv_ewkDown.SetName("photon_weights_%s_ewk_Down"%nam)
  for b in range(Zvv_ewkDown.GetNbinsX()): Zvv_ewkDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_ewkDown,nlo_ewkUp,gvptname,metname,_wspace.data("signal_zjets"))

  Zvv_ewkUp   = target.Clone(); Zvv_ewkUp   .SetName("photon_weights_%s_ewk_Up"%nam)
  for b in range(Zvv_ewkUp.GetNbinsX()): Zvv_ewkUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_ewkUp,nlo_ewkDown,gvptname,metname,_wspace.data("signal_zjets"))

  nlo_ewkFlat = nlo_ewkDown.Clone("ewk_Base")
  nlo_ewkFlat.Divide(nlo_ewkFlat)
  Zvv_ewkBase = target.Clone(); Zvv_ewkBase  .SetName("photon_weights_%s_ewk_Base"%nam)
  for b in range(Zvv_ewkBase.GetNbinsX()): Zvv_ewkBase.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_ewkBase,nlo_ewkFlat,gvptname,metname,_wspace.data("signal_zjets"))


  Zvv_FPDown = target.Clone(); Zvv_FPDown.SetName("photon_weights_%s_fp_Down"%nam)
  for b in range(Zvv_FPDown.GetNbinsX()): Zvv_FPDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_FPDown,nlo_FPDown,gvptname,metname,_wspace.data("signal_zjets"))

  Zvv_FPUp   = target.Clone(); Zvv_FPUp   .SetName("photon_weights_%s_fp_Up"%nam)
  for b in range(Zvv_FPUp.GetNbinsX()): Zvv_FPUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_FPUp,nlo_FPUp,gvptname,metname,_wspace.data("signal_zjets"))
  ##################################################################################################################


  # Have to also add one per systematic variation :(, 
  Zvv.Divide(Pho); 		 Zvv.SetName("photon_weights_%s"%nam)
  Zvv_mrUp.Divide(Pho_mrUp); 	 Zvv_mrUp.SetName("photon_weights_%s_mr_Up"%nam);_fOut.WriteTObject(Zvv_mrUp)
  Zvv_mrDown.Divide(Pho_mrDown); Zvv_mrDown.SetName("photon_weights_%s_mr_Down"%nam);_fOut.WriteTObject(Zvv_mrDown)
  Zvv_mfUp.Divide(Pho_mfUp); 	 Zvv_mfUp.SetName("photon_weights_%s_mf_Up"%nam);_fOut.WriteTObject(Zvv_mfUp)
  Zvv_mfDown.Divide(Pho_mfDown); Zvv_mfDown.SetName("photon_weights_%s_mf_Down"%nam);_fOut.WriteTObject(Zvv_mfDown)
  Zvv_mr2Up.Divide(Pho_mr2Up); 	 Zvv_mr2Up.SetName("photon_weights_%s_mr2_Up"%nam);_fOut.WriteTObject(Zvv_mr2Up)
  Zvv_mr2Down.Divide(Pho_mr2Down); Zvv_mr2Down.SetName("photon_weights_%s_mr2_Down"%nam);_fOut.WriteTObject(Zvv_mr2Down)
  Zvv_mf2Up.Divide(Pho_mf2Up); 	 Zvv_mf2Up.SetName("photon_weights_%s_mf2_Up"%nam);_fOut.WriteTObject(Zvv_mf2Up)
  Zvv_mf2Down.Divide(Pho_mf2Down); Zvv_mf2Down.SetName("photon_weights_%s_mf2_Down"%nam);_fOut.WriteTObject(Zvv_mf2Down)

  Zvv_pdfUp.Divide(Pho); 	 Zvv_pdfUp.SetName("photon_weights_%s_pdf_Up"%nam);_fOut.WriteTObject(Zvv_pdfUp)
  Zvv_pdfDown.Divide(Pho); 	Zvv_pdfDown.SetName("photon_weights_%s_pdf_Down"%nam);_fOut.WriteTObject(Zvv_pdfDown)
  
  # Divide out the nominal photon for the EWK corrections as this is already the relative difference
  Zvv_ewkUp  .Divide(Zvv_ewkBase)
  Zvv_ewkDown.Divide(Zvv_ewkBase)
  Zvv_ewkUp  .Multiply(Zvv)
  Zvv_ewkDown.Multiply(Zvv)

  Zvv_FPUp  .Divide(Zvv_ewkBase)
  Zvv_FPDown.Divide(Zvv_ewkBase)
  Zvv_FPUp  .Multiply(Zvv)
  Zvv_FPDown.Multiply(Zvv)

  #_fOut.WriteTObject(Zvv_ewkDown)
  #_fOut.WriteTObject(Zvv_ewkUp)
  _fOut.WriteTObject(Zvv_FPDown)
  _fOut.WriteTObject(Zvv_FPUp)

  ZmmScales.Divide(Zmm)
  PhotonScales = Zvv.Clone()

  #_fOut.WriteTObject(Zvv) # these are photon scales
  _fOut.WriteTObject(PhotonScales)
  _fOut.WriteTObject(ZmmScales)

  # finally make a photon background dataset 
  diag.generateWeightedDataset("photon_gjet_backgrounds",ptphopurity,wvarname,"ptpho",_wspace,"photon_data")

  _bins = []  # take bins from some histogram
  for b in range(target.GetNbinsX()+1):
    _bins.append(target.GetBinLowEdge(b+1))

  CRs = [
  Channel("Photon+jet",_wspace,out_ws,cid,0,_wspace.data(_photon_datasetname),PhotonScales,"photon_gjet_backgrounds")  # stupid linear fit of Purities, should move to flat 
  ,Channel("Dimuon",_wspace,out_ws,cid,1,_wspace.data(_dimuon_datasetname),ZmmScales,_dimuon_backgroundsname)
  ]


  CRs[0].add_nuisance_shape("mr",_fOut) 
  CRs[0].add_nuisance_shape("mf",_fOut) 
  CRs[0].add_nuisance_shape("mr2",_fOut) 
  CRs[0].add_nuisance_shape("mf2",_fOut) 
  CRs[0].add_nuisance_shape("pdf",_fOut) 
  CRs[0].add_nuisance_shape("fp",_fOut) 
  CRs[0].add_nuisance("PhotonEfficiency",0.01) 
  CRs[1].add_nuisance("CMS_eff_m",0.01)
  CRs[0].add_nuisance("purity",0.5,True)   # is a background systematic -> 50% is ~1% on 3%
  CRs[1].add_nuisance("xs_backgrounds",0.1,True)   # is a background systematic

  # Now for each bin in the distribution, we make one EWK uncertainty which is the size of  the Up/Down variation --> Completely uncorrelated between bins
  for b in range(target.GetNbinsX()):
    ewk_u = PhotonScales.Clone(); ewk_u.SetName("photon_weights_%s_ewk_%s_bin%d_Up"%(nam,nam,b))
    ewk_d = PhotonScales.Clone(); ewk_d.SetName("photon_weights_%s_ewk_%s_bin%d_Down"%(nam,nam,b))
    for j in range(target.GetNbinsX()):
      if j==b: 
	ewk_u.SetBinContent(j+1,Zvv_ewkUp.GetBinContent(j+1))
	ewk_d.SetBinContent(j+1,Zvv_ewkDown.GetBinContent(j+1))
	break
    _fOut.WriteTObject(ewk_u)
    _fOut.WriteTObject(ewk_d)
    CRs[0].add_nuisance_shape("ewk_%s_bin%d"%(nam,b),_fOut,"SetTo=1")

  # Bin by bin nuisances to cover statistical uncertainties ...
  for b in range(target.GetNbinsX()):
    err = PhotonScales.GetBinError(b+1)
    if not PhotonScales.GetBinContent(b+1)>0: continue 
    relerr = err/PhotonScales.GetBinContent(b+1)
    if relerr<0.01: continue
    byb_u = PhotonScales.Clone(); byb_u.SetName("photon_weights_%s_%s_stat_error_%s_bin%d_Up"%(nam,nam,"photonCR",b))
    byb_u.SetBinContent(b+1,PhotonScales.GetBinContent(b+1)+err)
    byb_d = PhotonScales.Clone(); byb_d.SetName("photon_weights_%s_%s_stat_error_%s_bin%d_Down"%(nam,nam,"photonCR",b))
    byb_d.SetBinContent(b+1,PhotonScales.GetBinContent(b+1)-err)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    print "Adding an error -- ", byb_u.GetName(),err
    CRs[0].add_nuisance_shape("%s_stat_error_%s_bin%d"%(nam,"photonCR",b),_fOut)

  for b in range(target.GetNbinsX()):
    err = ZmmScales.GetBinError(b+1)
    if not ZmmScales.GetBinContent(b+1)>0: continue 
    relerr = err/ZmmScales.GetBinContent(b+1)
    if relerr<0.01: continue
    byb_u = ZmmScales.Clone(); byb_u.SetName("zmm_weights_%s_%s_stat_error_%s_bin%d_Up"%(nam,nam,"dimuonCR",b))
    byb_u.SetBinContent(b+1,ZmmScales.GetBinContent(b+1)+err)
    byb_d = ZmmScales.Clone(); byb_d.SetName("zmm_weights_%s_%s_stat_error_%s_bin%d_Down"%(nam,nam,"dimuonCR",b))
    byb_d.SetBinContent(b+1,ZmmScales.GetBinContent(b+1)-err)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    print "Adding an error -- ", byb_u.GetName(),err
    CRs[1].add_nuisance_shape("%s_stat_error_%s_bin%d"%(nam,"dimuonCR",b),_fOut)

  cat = Category("ZJets",cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,"signal_zjets",CRs,diag)
  cat.addVar("jet1pt",25,150,1000)
  cat.addVar("mll",25,75,125)
  cat.addVar("mt",30,50,200)
  cat.addVar("njets",10,0,10)
  cat.addVar("lep1pt",25,0,500)
  cat.addVar("ptll",40,100,1000)
  cat.addVar("ptpho",40,100,1000)
  cat.addVar("mvamet",40,100,1000)
  cat.addTarget("dimuon_zll",1)
  cat.addTarget("singlemuon_zll",1)
  cat.addTarget("photon_gjet_nlo",0)
  cat.addTarget("photon_gjet",0)
  cat.addTarget("photon_gjet_backgrounds",-2)# -2 means dont apply any correction
  return cat 
  
#----------------------------------------------------------------------------------------------------------------------------------------------------------//
_fOut = r.TFile("photon_dimuon_combined_model.root","RECREATE")
# run once per category
categories = ["monojet","resolved","boosted"]
#categories = ["boosted","resolved"]
#categories = ["monojet"]
_f = r.TFile.Open("mono-x-vtagged.root")
out_ws = r.RooWorkspace("combinedws")
#out_ws._import = getattr(out_ws,"import")
out_ws._import = SafeWorkspaceImporter(out_ws)

# Need to setup the things here for combined dataset, need to add all possible sample types first because otherwise RooFit throws a fit! 
sampleType  = r.RooCategory("bin_number","Bin Number");
obs         = r.RooRealVar("observed","Observed Events bin",1)

out_ws._import(sampleType)  # Global variables for dataset
out_ws._import(obs)
obsargset   = r.RooArgSet(out_ws.var("observed"),out_ws.cat("bin_number"))

cmb_categories=[]
diag_combined = diagonalizer(out_ws)
for cid,cn in enumerate(categories): 
        _fDir = _fOut.mkdir("category_%s"%cn)
	cmb_categories.append(cmodel(cid,cn,_f,_fDir,out_ws,diag_combined))
	_fDirW = _fOut.mkdir("Wcategory_%s"%cn)
	cmb_categories.append(cmodelW(10+cid,cn,_f,_fDirW,out_ws,diag_combined))
# Had to define the types before adding to the combined dataset
for cid,cn in enumerate(cmb_categories):
	cn.init_channels()
        channels = cn.ret_channels()
        for ch in channels: ch.Print()
out_ws.Print('v')

out_ws.data("combinedData").Print("v")
#for i in range(out_ws.data("combinedData").numEntries()):
#  args = out_ws.data("combinedData").get(i)
#  args.Print("v")
for cid,cn in enumerate(cmb_categories):
   channels = cn.ret_channels()
   for ch in channels: ch.Print()
#sys.exit()
# Next we want to build a list of all of the nuisance parameters which will be in the fit :), this is performed with add_nuisance
ext_constraints = r.RooArgSet() 
hasSys = False

for cn in cmb_categories:
 for cr in cn.ret_control_regions():
  nuisances = cr.ret_nuisances()+cr.ret_bkg_nuisances()
  for nuis in nuisances:
   hasSys=True
   ext_constraints.add(out_ws.pdf("const_%s"%nuis))

ext_constraints.Print("v")
# Now we have the observation and expectation of all of the bins, make a combined pdf and fit!
# ------------------------------------------------------------
# WRITE THE FIT PART HERE
combined_pdf = r.RooSimultaneous("combined_pdf","combined_pdf",out_ws.cat(sampleType.GetName()))
# Loop through every bin and add the Poisson Pdf
for cid,cn in enumerate(cmb_categories):
  channels = cn.ret_channels()
  for ch in channels: 
    combined_pdf.addPdf(out_ws.pdf("pdf_%s"%ch.ret_binid()),ch.ret_binid())

nll_ = combined_pdf.createNLL(out_ws.data("combinedData"),r.RooFit.ExternalConstraints(ext_constraints))
minim = r.RooMinimizer(nll_)
# Save a Pre-fit snapshot
out_ws.saveSnapshot("PRE_EXT_FIT_Clean",out_ws.allVars()) 

if hasSys: 
	minim.migrad()
	#minim.minos()
	minim.hesse()
	combined_fit_result = minim.save()
	#combined_fit_result = combined_pdf.fitTo(out_ws.data("combinedData"),r.RooFit.Save(),r.RooFit.ExternalConstraints(ext_constraints),r.RooFit.Strategy(1))
	#combined_fit_result = combined_pdf.fitTo(out_ws.data("combinedData"),r.RooFit.Save(),r.RooFit.ExternalConstraints(ext_constraints),r.RooFit.Strategy(0))
else: 
	combined_fit_result = combined_pdf.fitTo(out_ws.data("combinedData"),r.RooFit.Save(),r.RooFit.Strategy(1))
	#combined_fit_result = combined_pdf.fitTo(out_ws.data("combinedData"),r.RooFit.Save(),r.RooFit.Strategy(0))

_fOut.WriteTObject(out_ws)
for cid,cn in enumerate(cmb_categories):
   channels = cn.ret_channels()
   for ch in channels: ch.Print()

# ------------------------------------------------------------
# Now Generate the systematics coming from the fitting 
npars = diag_combined.generateVariations(combined_fit_result)
h2covar = diag_combined.retCovariance()
h2covar.SetName("covariance_fit_fitresult_combined_pdf_combinedData")
_fOut.WriteTObject(h2covar)
h2corr = diag_combined.retCorrelation()
h2corr.SetName("correlation_fit_fitresult_combined_pdf_combinedData")
_fOut.WriteTObject(h2corr)
# ------------------------------------------------------------
for cat in cmb_categories:
   cat.save_model(diag_combined)          # Saves the nominal model and makes templates for variations from each uncorrelated parameter :) 
   cat.generate_systematic_templates(diag_combined,npars)
   cat.make_post_fit_plots() # Makes Post-fit to CR plots including approximated error bands from fit variations
   # plot additional vars and nonsence like that 
   cat.save_all_models_internal(diag_combined)
   cat.save() # make plots, save histograms and canvases

for cid,cn in enumerate(cmb_categories):
   channels = cn.ret_channels()
   for ch in channels: ch.Print()

# make a plot of the pulls from this fit, 
pull_plot = pullPlot(combined_fit_result,_fOut)
#_fOut.WriteTObject(pull_plot)

print "Init pars"
combined_fit_result.floatParsInit().Print("v")
print "Final pars"
combined_fit_result.floatParsFinal().Print("v")
_fOut.WriteTObject(combined_fit_result)
# END
print "Produced combined Z(mm) + photon fits -> ", _fOut.GetName()
_fOut.Close()
# END
