import ROOT
from counting_experiment import *
# Define how a control region(s) transfer is made by defining *cmodel*, the calling pattern must be unchanged!
# First define simple string which will be used for the datacard 
model = "zjets"

def cmodel(cid,nam,_f,_fOut, out_ws, diag):
  
  # Some setup
  _fin = _f.Get("category_%s"%cid)
  _wspace = _fin.Get("wspace_%s"%cid)

  # ############################ USER DEFINED ###########################################################
  # First define the nominal transfer factors (histograms of signal/control, usually MC 
  # note there are many tools available inside include/diagonalize.h for you to make 
  # special datasets/histograms representing these and systematic effects 
  # example below for creating shape systematic for photon which is just every bin up/down 30% 

  metname    = "met"          # Observable variable name 
  gvptname   = "genBosonPt"    # Weights are in generator pT

  target                = _fin.Get("signal_zjets")            # define monimal (MC) of which process this config will model
  controlmc             = _fin.Get("dimuon_zll")              # defines Zmm MC of which process will be controlled by
  controlmc_photon      = _fin.Get("photon_gjets")            # defines Gjets MC of which process will be controlled by
  controlmc_e           = _fin.Get("dielectron_zll")          # defines Zmm MC of which process will be controlled by

  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down
  ZmmScales = target.Clone(); ZmmScales.SetName("zmm_weights_%s"%cid)
  ZmmScales.Divide(controlmc)
  _fOut.WriteTObject(ZmmScales)  # always write out to the directory 

  ZeeScales = target.Clone(); ZeeScales.SetName("zee_weights_%s"%cid)
  ZeeScales.Divide(controlmc_e)
  _fOut.WriteTObject(ZeeScales)  # always write out to the directory 

  ### PHOTONS ###
  #my_function(_wspace,_fin,_fOut,cid,diag)
  #PhotonScales = _fOut.Get("photon_weights_%s"%cid)

  #######################################################################################################

  _bins = []  # take bins from some histogram, can choose anything but this is easy 
  for b in range(target.GetNbinsX()+1):
    _bins.append(target.GetBinLowEdge(b+1))

  # Here is the important bit which "Builds" the control region, make a list of control regions which 
  # are constraining this process, each "Channel" is created with ...
  # 	(name,_wspace,out_ws,cid+'_'+model,TRANSFERFACTORS) 
  # the second and third arguments can be left unchanged, the others instead must be set
  # TRANSFERFACTORS are what is created above, eg WScales

  CRs = [
  Channel("dimuonModel",_wspace,out_ws,cid+'_'+model,ZmmScales),
  Channel("dielectronModel",_wspace,out_ws,cid+'_'+model,ZeeScales),
  #Channel("photonModel",_wspace,out_ws,cid+'_'+model,PhotonScales), 
  ]

  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=WScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)

  # Bin by bin nuisances to cover statistical uncertainties ...

  # define function locally for convenient access to stuff
  def addStatErrs(hx,cr,crname1,crname2):
    for b in range(1,target.GetNbinsX()+1):
      err = hx.GetBinError(b)
      if not hx.GetBinContent(b)>0:
        continue
      relerr = err/hx.GetBinContent(b)
      if relerr<0.01:
        continue
      byb_u = hx.Clone(); byb_u.SetName('%s_weights_%s_%s_stat_error_%s_bin%d_Up'%(crname1,cid,cid,crname2,b-1))
      byb_u.SetBinContent(b,hx.GetBinContent(b)+err)
      byb_d = hx.Clone(); byb_d.SetName('%s_weights_%s_%s_stat_error_%s_bin%d_Down'%(crname1,cid,cid,crname2,b-1))
      if err<hx.GetBinContent(b):
        byb_d.SetBinContent(b,hx.GetBinContent(b)-err)
      else:
        byb_d.SetBinContent(b,0)
      _fOut.WriteTObject(byb_u)
      _fOut.WriteTObject(byb_d)
      cr.add_nuisance_shape('%s_stat_error_%s_bin%d'%(cid,crname2,b-1),_fOut)

  addStatErrs(ZmmScales,CRs[0],'zmm','dimuonModelCR')
  addStatErrs(ZeeScales,CRs[1],'zee','dielectronModelCR')
  #addStatErrs(ZmmScales,CRs[2],'zmm','photonModelCR')


  #######################################################################################################
  
  '''
  CRs[2].add_nuisance_shape("renscale",_fOut) 
  CRs[2].add_nuisance_shape("facscale",_fOut) 
  CRs[2].add_nuisance_shape("pdf",_fOut) 
  CRs[2].add_nuisance("PhotonEff",0.02) 
  '''
  #######################################################################################################

  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,target.GetName(),CRs,diag)
  # Return of course
  return cat

# My Function. Just to put all of the complicated part into one function
def my_function(_wspace,_fin,_fOut,nam,diag):

  metname    = "met"          # Observable variable name 
  gvptname   = "genBosonPt"    # Weights are in generator pT

  target             = _fin.Get("signal_zjets")      # define monimal (MC) of which process this config will model
  
  controlmc          = _fin.Get("dimuon_zll")           # defines Zmm MC of which process will be controlled by
  controlmc_photon   = _fin.Get("photon_gjets")       # defines Gjets MC of which process will be controlled by
  
  _gjet_mcname 	     = "photon_gjets"
  GJet               = _fin.Get("photon_gjets")

  fztoa = r.TFile.Open("files/atoz_unc.root")
  
  ztoa_renscale_up   = fztoa.Get("znlo1_over_anlo1_renScaleUp")
  ztoa_renscale_down = fztoa.Get("znlo1_over_anlo1_renScaleDown")

  ztoa_facscale_up   = fztoa.Get("znlo1_over_anlo1_facScaleUp")
  ztoa_facscale_down = fztoa.Get("znlo1_over_anlo1_facScaleDown")

  ztoa_pdf_up   = fztoa.Get("znlo1_over_anlo1_pdfUp")
  ztoa_pdf_down = fztoa.Get("znlo1_over_anlo1_pdfDown")

  PhotonSpectrum = controlmc_photon.Clone(); PhotonSpectrum.SetName("photon_spectrum_%s_"%nam)
  ZvvSpectrum 	 = target.Clone(); ZvvSpectrum.SetName("zvv_spectrum_%s_"%nam)

  _fOut.WriteTObject( PhotonSpectrum )
  _fOut.WriteTObject( ZvvSpectrum )
  
  #################################################################################################################

  Pho = controlmc_photon.Clone(); Pho.SetName("photon_weights_denom_%s"%nam)
  Zvv = target.Clone(); Zvv.SetName("photon_weights_nom_%s"%nam)


  ratio_ren_scale_up = Zvv.Clone();  ratio_ren_scale_up.SetName("photon_weights_%s_renscale_Up"%nam);
  for b in range(ratio_ren_scale_up.GetNbinsX()): ratio_ren_scale_up.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(ratio_ren_scale_up,ztoa_renscale_up,gvptname,metname,_wspace.data("signal_zjets"))
  ratio_ren_scale_up.Divide(Pho)
  _fOut.WriteTObject(ratio_ren_scale_up)
  
  ratio_ren_scale_down = Zvv.Clone();  ratio_ren_scale_down.SetName("photon_weights_%s_renscale_Down"%nam);
  for b in range(ratio_ren_scale_down.GetNbinsX()): ratio_ren_scale_down.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(ratio_ren_scale_down,ztoa_renscale_down,gvptname,metname,_wspace.data("signal_zjets"))
  ratio_ren_scale_down.Divide(Pho)
  _fOut.WriteTObject(ratio_ren_scale_down)

  ratio_fac_scale_up = Zvv.Clone();  ratio_fac_scale_up.SetName("photon_weights_%s_facscale_Up"%nam);
  for b in range(ratio_fac_scale_up.GetNbinsX()): ratio_fac_scale_up.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(ratio_fac_scale_up,ztoa_facscale_up,gvptname,metname,_wspace.data("signal_zjets"))
  ratio_fac_scale_up.Divide(Pho)
  _fOut.WriteTObject(ratio_fac_scale_up)
  
  ratio_fac_scale_down = Zvv.Clone();  ratio_fac_scale_down.SetName("photon_weights_%s_facscale_Down"%nam);
  for b in range(ratio_fac_scale_down.GetNbinsX()): ratio_fac_scale_down.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(ratio_fac_scale_down,ztoa_facscale_down,gvptname,metname,_wspace.data("signal_zjets"))
  ratio_fac_scale_down.Divide(Pho)
  _fOut.WriteTObject(ratio_fac_scale_down)

  ratio_pdf_up = Zvv.Clone();  ratio_pdf_up.SetName("photon_weights_%s_pdf_Up"%nam);
  for b in range(ratio_pdf_up.GetNbinsX()): ratio_pdf_up.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(ratio_pdf_up,ztoa_pdf_up,gvptname,metname,_wspace.data("signal_zjets"))
  ratio_pdf_up.Divide(Pho)
  _fOut.WriteTObject(ratio_pdf_up)
  
  ratio_pdf_down = Zvv.Clone();  ratio_pdf_down.SetName("photon_weights_%s_pdf_Down"%nam);
  for b in range(ratio_pdf_down.GetNbinsX()): ratio_pdf_down.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(ratio_pdf_down,ztoa_pdf_down,gvptname,metname,_wspace.data("signal_zjets"))
  ratio_pdf_down.Divide(Pho)
  _fOut.WriteTObject(ratio_pdf_down)


  Zvv.Divide(Pho); Zvv.SetName("photon_weights_%s"%nam)

  PhotonScales = Zvv.Clone()
  _fOut.WriteTObject(PhotonScales)
  

  # fztoaewk = fztoa
  fztoaewk = r.TFile.Open('files/atoz_unc.root')
  ztoa_ewk_up   = fztoaewk.Get("a_ewkcorr_overz_Upcommon")
  ztoa_ewk_down = fztoaewk.Get("a_ewkcorr_overz_Downcommon")

  ratio_ewk_up = Zvv.Clone();  ratio_ewk_up.SetName("photon_weights_%s_ewk_Up"%nam);
  for b in range(ratio_ewk_up.GetNbinsX()): ratio_ewk_up.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(ratio_ewk_up,ztoa_ewk_up,gvptname,metname,_wspace.data("signal_zjets"))
  ratio_ewk_up.Divide(Pho)
  
  ratio_ewk_down = Zvv.Clone();  ratio_ewk_down.SetName("photon_weights_%s_ewk_Down"%nam);
  for b in range(ratio_ewk_down.GetNbinsX()): ratio_ewk_down.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(ratio_ewk_down,ztoa_ewk_down,gvptname,metname,_wspace.data("signal_zjets"))
  ratio_ewk_down.Divide(Pho)

  #Now lets uncorrelate the bins:
  for b in range(target.GetNbinsX()):
    ewk_up = Zvv.Clone(); ewk_up.SetName("photon_weights_%s_ewk_%s_bin%d_Up"%(nam,nam,b))
    ewk_down = Zvv.Clone(); ewk_down.SetName("photon_weights_%s_ewk_%s_bin%d_Down"%(nam,nam,b))
    for i in range(target.GetNbinsX()):
      if i==b:
        ewk_up.SetBinContent(i+1,ratio_ewk_up.GetBinContent(i+1))
        ewk_down.SetBinContent(i+1,ratio_ewk_down.GetBinContent(i+1))
        break


    _fOut.WriteTObject(ewk_up)
    _fOut.WriteTObject(ewk_down)


