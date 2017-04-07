import ROOT
from counting_experiment import *
# Define how a control region(s) transfer is made by defining cmodel provide, the calling pattern must be unchanged!
# First define simple string which will be used for the datacard 
model = "ttbar"
convertHistograms = []

### helper functions ###

def makeTop(cid,_fOut,newName,targetmc,controlmc,systs=None,doSJ=False):
  TopScales = targetmc.Clone(); TopScales.SetName(newName+"_weights_%s"%cid)
  TopScales.Divide(controlmc)
  _fOut.WriteTObject(TopScales)

  if not(systs==None):
    for uncert in ['btag']:
      TopScalesUp = systs['targetmc%sUp'%(uncert)].Clone(); TopScalesUp.SetName(newName+"_weights_%s_%s_Up"%(cid,uncert))
      TopScalesUp.Divide(systs['controlmc%sUp'%(uncert)])

      TopScalesDown = systs['targetmc%sDown'%(uncert)].Clone(); TopScalesDown.SetName(newName+"_weights_%s_%s_Down"%(cid,uncert))
      TopScalesDown.Divide(systs['controlmc%sDown'%(uncert)])

      _fOut.WriteTObject(TopScalesUp)
      _fOut.WriteTObject(TopScalesDown)

  return TopScales


def addTopErrors(TopScales,targetmc,newName,crName,_fOut,CRs,nCR,cid,doBtag=True):

  if doBtag:
    uncerts = ['btag']
    for uncert in uncerts:
      CRs[nCR].add_nuisance_shape(uncert,_fOut)

  bins = range(targetmc.GetNbinsX())

  for b in bins:
    err = TopScales.GetBinError(b+1)
    '''
    if err > TopScales.GetBinContent(b+1):
      err = TopScales.GetBinContent(b+1)-0.00001
      print "BIN CONTENT: " + str(TopScales.GetBinContent(b+1))
      print "BIN ERROR: " + str(TopScales.GetBinError(b+1))
      print "NEW ERROR: " + str(err)
    '''
    if not TopScales.GetBinContent(b+1)>0: continue 
    else: relerr = err/TopScales.GetBinContent(b+1)
    if relerr<0.001: continue
    byb_u = TopScales.Clone(); byb_u.SetName("%s_weights_%s_%s_stat_error_%sCR_bin%d_Up"%(newName,cid,cid,crName,b))
    byb_u.SetBinContent(b+1,TopScales.GetBinContent(b+1)+err)
    byb_d = TopScales.Clone(); byb_d.SetName("%s_weights_%s_%s_stat_error_%sCR_bin%d_Down"%(newName,cid,cid,crName,b))
    byb_d.SetBinContent(b+1,TopScales.GetBinContent(b+1)-err)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    CRs[nCR].add_nuisance_shape("%s_stat_error_%sCR_bin%d"%(cid,crName,b),_fOut)


def cmodel(cid,nam,_f,_fOut, out_ws, diag):
  # Some setup
  _fin = _f.Get("category_%s"%cid)
  _wspace = _fin.Get("wspace_%s"%cid)

  # ############################ USER DEFINED ###########################################################
  # First define the nominal transfer factors (histograms of signal/control, usually MC 
  # note there are many tools available inside include/diagonalize.h for you to make 
  # special datasets/histograms representing these and systematic effects 
  # but for now this is just kept simple 
  processName = "TTbar" # Give a name of the process being modelled
  metname = "met"    # Observable variable name 

  targetmc     = _fin.Get("signal_ttbar")      # define monimal (MC) of which process this config will model
  controlmc    = _fin.Get("singlemuontop_ttbar")
  controlmc_e  = _fin.Get("singleelectrontop_ttbar")
  controlmc_w    = _fin.Get("singlemuonw_ttbar")
  controlmc_w_e  = _fin.Get("singleelectronw_ttbar")
 

  systs = {}; systs_e = {}
  systs_w = {}; systs_w_e = {}

  # btag systs
  systs['targetmcbtagUp']      = _fin.Get("signal_ttbar_btagUp");           systs_e['targetmcbtagUp']      = systs['targetmcbtagUp']
  systs['targetmcbtagDown']    = _fin.Get("signal_ttbar_btagDown");         systs_e['targetmcbtagDown']    = systs['targetmcbtagDown']
  systs['controlmcbtagUp']     = _fin.Get("singlemuontop_ttbar_btagUp");    systs_e['controlmcbtagUp']     = _fin.Get("singleelectrontop_ttbar_btagUp")
  systs['controlmcbtagDown']   = _fin.Get("singlemuontop_ttbar_btagDown");  systs_e['controlmcbtagDown']   = _fin.Get("singleelectrontop_ttbar_btagDown")
  
  systs_w['targetmcbtagUp']      = _fin.Get("signal_ttbar_btagUp");           systs_w_e['targetmcbtagUp']      = systs_w['targetmcbtagUp']
  systs_w['targetmcbtagDown']    = _fin.Get("signal_ttbar_btagDown");         systs_w_e['targetmcbtagDown']    = systs_w['targetmcbtagDown']
  systs_w['controlmcbtagUp']     = _fin.Get("singlemuonw_ttbar_btagUp");      systs_w_e['controlmcbtagUp']     = _fin.Get("singleelectronw_ttbar_btagUp")
  systs_w['controlmcbtagDown']   = _fin.Get("singlemuonw_ttbar_btagDown");    systs_w_e['controlmcbtagDown']   = _fin.Get("singleelectronw_ttbar_btagDown")

  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down

  TopScales      = makeTop(cid,_fOut,"topmn",targetmc,controlmc,systs,False)
  TopScales_e    = makeTop(cid,_fOut,"topen",targetmc,controlmc_e,systs_e,False)
  TopScales_w    = makeTop(cid,_fOut,"topwmn",targetmc,controlmc_w,None,False)
  TopScales_w_e  = makeTop(cid,_fOut,"topwen",targetmc,controlmc_w_e,None,False)


  #######################################################################################################

  _bins = []  # take bins from some histogram, can choose anything but this is easy 
  for b in range(targetmc.GetNbinsX()+1):
    _bins.append(targetmc.GetBinLowEdge(b+1))

  # Here is the important bit which "Builds" the control region, make a list of control regions which 
  # are constraining this process, each "Channel" is created with ...
  # 	(name,_wspace,out_ws,cid+'_'+model,TRANSFERFACTORS) 
  # the second and third arguments can be left unchanged, the others instead must be set
  # TRANSFERFACTORS are what is created above, eg TopScales

  CRs = [
   Channel("singlemuontopModel",      _wspace,out_ws,cid+'_'+model,TopScales),
   Channel("singleelectrontopModel",  _wspace,out_ws,cid+'_'+model,TopScales_e),
   Channel("singlemuonwtopModel",     _wspace,out_ws,cid+'_'+model,TopScales_w),
   Channel("singleelectronwtopModel", _wspace,out_ws,cid+'_'+model,TopScales_w_e),
  ]


  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=TopScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)
  
  addTopErrors(TopScales,    targetmc,"topmn", "singlemuontopModel",     _fOut,CRs,0,cid)
  addTopErrors(TopScales_e,  targetmc,"topen", "singleelectrontopModel", _fOut,CRs,1,cid)
  addTopErrors(TopScales_w,  targetmc,"topwmn","singlemuonwtopModel",    _fOut,CRs,2,cid,False)
  addTopErrors(TopScales_w_e,targetmc,"topwen","singleelectronwtopModel",_fOut,CRs,3,cid,False)

  #######################################################################################################

  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,targetmc.GetName(),CRs,diag)
  #cat.setDependant("zjets","wjetsdependant")  # Can use this to state that the "BASE" of this is already dependant on another process
  # EG if the W->lv in signal is dependant on the Z->vv and then the W->mv is depenant on W->lv, then 
  # give the arguments model,channel name from the config which defines the Z->vv => W->lv map! 
  # Return of course
  return cat

