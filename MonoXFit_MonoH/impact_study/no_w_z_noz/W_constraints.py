import ROOT
from counting_experiment import *
# Define how a control region(s) transfer is made by defining cmodel provide, the calling pattern must be unchanged!
# First define simple string which will be used for the datacard 
model = "wjets"
def cmodel(cid,nam,_f,_fOut, out_ws, diag):
  
  # Some setup
  _fin    = _f.Get("category_%s"%cid)
  _wspace = _fin.Get("wspace_%s"%cid)


  # ############################ USER DEFINED ###########################################################
  # First define the nominal transfer factors (histograms of signal/control, usually MC 
  # note there are many tools available inside include/diagonalize.h for you to make 
  # special datasets/histograms representing these and systematic effects 
  # but for now this is just kept simple 
  processName  = "WJets" # Give a name of the process being modelled
  metname      = "met"    # Observable variable name 
  targetmc     = _fin.Get("signal_wjets")      # define monimal (MC) of which process this config will model
  controlmc    = _fin.Get("Wmn_wjets")  # defines in / out acceptance
  controlmc_e  = _fin.Get("Wen_wjets")  # defines in / out acceptance

  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down
  WScales = targetmc.Clone(); WScales.SetName("wmn_weights_%s"%cid)
  WScales.Divide(controlmc)
  _fOut.WriteTObject(WScales)  # always write out to the directory 

  WScales_e = targetmc.Clone(); WScales_e.SetName("wen_weights_%s"%cid)
  WScales_e.Divide(controlmc_e)
  _fOut.WriteTObject(WScales_e)  # always write out to the directory 

  #######################################################################################################

  _bins = []  # take bins from some histogram, can choose anything but this is easy 
  for b in range(targetmc.GetNbinsX()+1):
    _bins.append(targetmc.GetBinLowEdge(b+1))

  # Here is the important bit which "Builds" the control region, make a list of control regions which 
  # are constraining this process, each "Channel" is created with ...
  # 	(name,_wspace,out_ws,cid+'_'+model,TRANSFERFACTORS) 
  # the second and third arguments can be left unchanged, the others instead must be set
  # TRANSFERFACTORS are what is created above, eg WScales

  CRs = [
   Channel("singlemuon",_wspace,out_ws,cid+'_'+model,WScales),
   Channel("singleelectron",_wspace,out_ws,cid+'_'+model,WScales_e)
  ]


  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=WScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)

  #CRs[0].add_nuisance("SingleMuonEff",0.01)
  #CRs[1].add_nuisance("SingleElEff",0.02)

  # Statistical uncertainties too!, one per bin 
  for b in range(targetmc.GetNbinsX()):
    err = WScales.GetBinError(b+1)
    print "ZEYNEP MISSING:", b+1, WScales.GetBinContent(b+1), err
    if not WScales.GetBinContent(b+1)>0: continue 
    relerr = err/WScales.GetBinContent(b+1)
    print "ZEYNEP MISSING:", b+1, WScales.GetBinContent(b+1), err, relerr
    if relerr<0.001: continue
    byb_u = WScales.Clone(); byb_u.SetName("wmn_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"singlemuonCR",b))
    byb_u.SetBinContent(b+1,WScales.GetBinContent(b+1)+err)
    byb_d = WScales.Clone(); byb_d.SetName("wmn_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"singlemuonCR",b))
    byb_d.SetBinContent(b+1,WScales.GetBinContent(b+1)-err)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    print "Adding an error -- ", byb_u.GetName(),err
    CRs[0].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"singlemuonCR",b),_fOut)

  # Statistical uncertainties too!, one per bin 
  for b in range(targetmc.GetNbinsX()):
    err_e = WScales_e.GetBinError(b+1)
    if not WScales_e.GetBinContent(b+1)>0: continue 
    relerr_e = err_e/WScales_e.GetBinContent(b+1)
    if relerr_e<0.001: continue
    byb_u_e = WScales_e.Clone(); byb_u_e.SetName("wen_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"singleelectronCR",b))
    byb_u_e.SetBinContent(b+1,WScales_e.GetBinContent(b+1)+err_e)
    byb_d_e = WScales_e.Clone(); byb_d_e.SetName("wen_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"singleelectronCR",b))
    byb_d_e.SetBinContent(b+1,WScales_e.GetBinContent(b+1)-err_e)
    _fOut.WriteTObject(byb_u_e)
    _fOut.WriteTObject(byb_d_e)
    print "Adding an error -- ", byb_u_e.GetName(),err_e
    CRs[1].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"singleelectronCR",b),_fOut)

  #######################################################################################################

  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,targetmc.GetName(),CRs,diag)
  
  # Return of course
  return cat

