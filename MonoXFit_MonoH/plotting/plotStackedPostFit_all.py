from ROOT import *
from collections import defaultdict
from os import getenv
from array import array
from tdrStyle import *
import plotConfig
#from __future__ import print_function
setTDRStyle()


new_dic = defaultdict(dict)

def getInt(h):
  nbins = h.GetNbinsX()
  total=0.
  for iB in xrange(1,nbins+1):
    total += h.GetBinContent(iB)*h.GetBinWidth(iB)
  return total

ttbar_color = ROOT.TColor.GetColor(0.329411764705882,0.534640522875817,0.728104575163399)
singletop_color = ROOT.TColor.GetColor(0.560, 0.662, 0.596)
diboson_color = ROOT.TColor.GetColor(0.709, 0.686, 0.721)
zll_color = ROOT.TColor.GetColor(1, 0.709, 0.862)
wjets_color = ROOT.TColor.GetColor(0.717, 0.815, 0.749)
qcd_color = ROOT.TColor.GetColor(0.270, 0.2, 0.301)
syst_color = ROOT.TColor.GetColor(0.960, 0.925, 0.6)
def plotPreFitPostFit(region):
  global blind
  channel = {"singlemuonw":"wmn", 
              "singlemuontop":"tmn",
              "dielectron":"zee",
              "dielectron_fail":"zee_fail",
              "dimuon":"zmm",
              "dimuon_fail":"zmm_fail",
              "singlemuonw_fail":"wmn_fail", 
              "photon":"pho", 
              "signal":"sig", 
              "singleelectrontop":"ten", 
              "singleelectronw":"wen"}
  extralabels = {"singlemuonw":"W CR (#mu)", 
              "singlemuontop":"t#bar{t} CR (#mu)",
              "dielectron":"Dielectron CR",
              "dielectron_fail":"Dielectron CR (fail)",
              "dimuon":"Dimuon CR",
              "dimuon_fail":"Dimuon CR (fail)",
              "singlemuonw_fail":"W CR (#mu) (fail)", 
              "photon":"Photon CR", 
              "signal":"SR", 
              "singleelectrontop":"t#bar{t} CR (e)", 
              "singleelectronw":"W CR (e)"}

  extralabel = extralabels[region]
  mainbkg = {"singlemuonw":"wjets", "singlemuonw_fail":"wjets", "dimuon":"zll", "dimuon_fail":"zll", "photon":"gjets", "signal":None, "singleelectronw":"wjets", "dielectron":"zll", "dielectron_fail":"zll", "singlemuontop":"ttbar","singleelectrontop":"ttbar"}

  basedir = getenv('CMSSW_BASE') + '/src/MonoXFit_MonoH/'

  f_mlfit = TFile(basedir+'/datacards/mlfit.root','READ')

  f_data = TFile(basedir+"/mono-x.root","READ")
  f_data.cd("category_monohiggs")
  h_data = None
  blind = False 
  h_data = gDirectory.Get(region+"_data")
#  if region=='signal':
#    h_res = gDirectory.Get('signal_Mres1100_Mchi100'); h_res.SetLineColor(kGreen+3)
#    h_fcnc = gDirectory.Get('signal_monotop_fcnc_mMed900'); h_fcnc.SetLineColor(kViolet+9)
#    h_res.Scale(3.91)
#    h_fcnc.Scale(0.78)
#    for h in [h_res,h_fcnc]:
#    for h in [h_fcnc]:
#      h.Scale(1,"width")
#      h.SetLineWidth(2)
#      h.SetLineStyle(2)

  '''
  if not region=="signal":
    h_data = gDirectory.Get(region+"_data")
  else:
    blind = True
  '''
  
  h_postfit_sig = f_mlfit.Get("shapes_fit_b/"+channel['signal']+"/total_background")
  h_prefit_sig = f_mlfit.Get("shapes_prefit/"+channel['signal']+"/total_background")
  
  b_width = [50,50,50,100,500]

  processesNormal = [
      'qcd',
      'dibosons',
      'stop',
      'wjets',
      'ttbar',
      'zvv',
      'zll',
      'gjets',
      'vh',
  ]

  processesZ = [
      'dibosons',
      'stop',
      'ttbar',
      'zll',
  ]

  processesT = [
      'qcd',
      'dibosons',
      'zll',
      'stop',
      'wjets',
      'ttbar',
  ]

  processesW = [
      'qcd',
      'dibosons',
      'zll',
      'stop',
      'wjets',
      'ttbar',
  ]

  if region=='singlemuonw' or region=='singleelectronw' or region=='singlemuonw_fail':
    processes = processesW
  elif region=='dimuon' or region=='dielectron' or region == 'dielectron_fail' or region == 'dimuon_fail':
    processes = processesZ
  elif 'top' in region:
    processes = processesT
  else:
    processes = processesNormal
  
  processNames = {'gjets':'#gamma+jets',
                  'vh':'VH',
                  'qcd':'QCD',
                  'ttbar':'t#bar{t}',
                  'stop':'Single top',
                  'dibosons':'Diboson',
                  'zvv':'Z+jets',
                  'zll':'Z+jets',
                  'wjets':'W+jets'
                  }
  
  order = [
           'VH',
           'Z#rightarrow#nu#nu',
           'Z#rightarrowll',
           'W#rightarrowl#nu',
           't#bar{t}',
           'Single top',
           'VV',
           'QCD',
           '#gamma+jets',
           'Data',
      ]
  zcolor = kCyan-4
  colors = {
      'qcd':qcd_color,
      'vh':632,
      'dibosons':diboson_color,    
      'ttbar':ttbar_color,
      'gjets':zcolor,
      'zjets':zcolor,
      'zvv':zcolor,
      'zll':zcolor,
      'wjets':wjets_color,
      'stop':singletop_color
  }

  binLowE = []

  # Pre-Fit
  h_prefit = {}
  h_prefit['total'] = f_mlfit.Get("shapes_prefit/"+channel[region]+"/total")
  for i in range(1,h_prefit['total'].GetNbinsX()+2):
    binLowE.append(h_prefit['total'].GetBinLowEdge(i))

  h_all_prefit = TH1F("h_all_prefit","h_all_prefit",len(binLowE)-1,array('d',binLowE))    
  h_other_prefit = TH1F("h_other_prefit","h_other_prefit",len(binLowE)-1,array('d',binLowE))    
  h_stack_prefit = THStack("h_stack_prefit","h_stack_prefit")    

  f_prefit = open('prefit_%s.txt' % region, 'w')
  print >> f_prefit, 'proc xmin xmax y yerr'

  for process in processes:
    h_prefit[process] = f_mlfit.Get("shapes_prefit/"+channel[region]+"/"+process)
    print process 
    if (not h_prefit[process]): continue
    if (str(h_prefit[process].Integral())=="nan"): continue
    print str(h_prefit[process].Integral())
#    h_prefit[process].SetLineColor(colors[process])
    h_prefit[process].SetLineColor(kBlack)
    h_prefit[process].SetFillColor(colors[process])
    h_all_prefit.Add(h_prefit[process])
    if (not process==mainbkg[region]): h_other_prefit.Add(h_prefit[process])
    h_stack_prefit.Add(h_prefit[process])
    print h_prefit[process].Integral()
    for i in range(1, h_prefit[process].GetNbinsX()+1):
     # print >>process.txt, process + ' ' + str(h_prefit[process].GetBinContent(i))
      print >> f_prefit, process + ' ' + str(h_prefit[process].GetXaxis().GetBinLowEdge(i)) + ' ' + str(h_prefit[process].GetXaxis().GetBinUpEdge(i)) + ' ' + str(h_prefit[process].GetBinContent(i)) + ' ' + str(h_prefit[process].GetBinError(i))
    
    

  # Post-Fit
  h_postfit = {}
  h_postfit['total'] = f_mlfit.Get("shapes_fit_b/"+channel[region]+"/total")
  h_all_postfit = TH1F("h_all_postfit","h_all_postfit",len(binLowE)-1,array('d',binLowE))    
  h_other_postfit = TH1F("h_other_postfit","h_other_postfit",len(binLowE)-1,array('d',binLowE))    
  h_stack_postfit = THStack("h_stack_postfit","h_stack_postfit")    
  

  h_postfit['totalv2'] = f_mlfit.Get("shapes_fit_b/"+channel[region]+"/total_background")
  h_postfit['total_prefit'] = f_mlfit.Get("shapes_prefit/"+channel[region]+"/total_background")

  for i in range(1, h_postfit['totalv2'].GetNbinsX()+1):
    error = h_postfit['totalv2'].GetBinError(i)
    content = h_postfit['totalv2'].GetBinContent(i)

  f_postfit = open('postfit_%s.txt' % region, 'w')
  print >> f_postfit, 'proc xmin xmax y yerr'


  for process in processes:
    h_postfit[process] = f_mlfit.Get("shapes_fit_b/"+channel[region]+"/"+process)
    if (not h_postfit[process]): continue
    if (str(h_postfit[process].Integral())=="nan"): continue
#    h_postfit[process].SetLineColor(colors[process])
    h_postfit[process].SetLineColor(kBlack)
    h_postfit[process].SetFillColor(colors[process])
    h_all_postfit.Add(h_postfit[process])
    if (not process==mainbkg[region]): h_other_postfit.Add(h_postfit[process])
    h_stack_postfit.Add(h_postfit[process])
    for i in range(1, h_prefit[process].GetNbinsX()+1):
     # print >>process.txt, process + ' ' + str(h_prefit[process].GetBinContent(i))
      print >> f_postfit, process + ' ' + str(h_postfit[process].GetXaxis().GetBinLowEdge(i)) + ' ' + str(h_postfit[process].GetXaxis().GetBinUpEdge(i)) + ' ' + str(h_postfit[process].GetBinContent(i)) + ' ' + str(h_postfit[process].GetBinError(i))
    
  f_postfit.close()
    
            
  gStyle.SetOptStat(0)
  gStyle.SetNdivisions(405, "XYZ")

  c = TCanvas("c","c",720,800)  
  SetOwnership(c,False)
  c.cd()
  c.SetLogy()

#  c.Range(0,0,1,1);
  c.SetFillColor(0);
  c.SetBorderMode(0);
  c.SetBorderSize(10);
  c.SetLogy();
  c.SetTickx(1);
  c.SetTicky(1);
  c.SetLeftMargin(0.12);
  c.SetRightMargin(0.07);
  c.SetTopMargin(0.04838082);
  c.SetBottomMargin(0.3)  



  dummy = h_all_prefit.Clone("dummy")
  dummy.SetFillColor(0)
  dummy.SetLineColor(0)
  dummy.SetLineWidth(0)
  dummy.SetMarkerSize(0)
  dummy.SetMarkerColor(0) 
  dummy.GetYaxis().SetTitle("Events / GeV")
  dummy.GetXaxis().SetTitle("")
  dummy.GetXaxis().SetTitleSize(0)
  dummy.GetXaxis().SetLabelSize(0)
  dummy.SetMaximum(50*dummy.GetMaximum())
  dummy.SetMinimum(0.0013)
  dummy.GetYaxis().SetTitleOffset(1.21)
  dummy.Draw()

  h_stack_postfit.Draw("hist same")

  h_all_prefit.SetLineColor(2)
  h_all_prefit.SetLineWidth(3)
#  h_all_prefit.Scale(1,"width")
  h_all_prefit.Draw("histsame")

  h_all_postfit.SetLineColor(4)
  h_all_postfit.SetLineWidth(3)
  #h_all_postfit.Draw("histsame")

  h_all_prefit.SetLineWidth(2)
  h_all_postfit.SetLineWidth(2)
  '''
  h_all_postfit.Scale(1,"width")


  h_other_prefit.SetLineColor(1)
  h_other_prefit.SetFillColor(kGray+1)
  h_other_prefit.Scale(1,"width")
  h_other_prefit.Draw("histsame")
  '''

  if not blind:
    h_data.SetLineColor(1)
    h_data.SetLineWidth(0)
    h_data.SetMarkerStyle(20)
    h_data.SetMarkerSize(1.2)
    h_data.Scale(1,"width")
    h_data.Draw("epsame")
    for i in range(1, h_data.GetNbinsX()+1):
      print process
      print >> f_prefit,'data' + ' ' + str(h_data.GetXaxis().GetBinLowEdge(i)) + ' ' + str(h_data.GetXaxis().GetBinUpEdge(i)) + ' ' + str(h_data.GetBinContent(i)) + ' ' + str(h_data.GetBinError(i))
      


    
  f_prefit.close()

  length = len(processes)
  #legend = TLegend(.55,.55,.95,.90)
  ymax = 0.9
  ymin = 0.9 - 0.35/6 * (len(processes))
  print "_________________"
  print len(processes)
  print ymin
  print "_________________"
  legend = TLegend(.55,ymin,.88,ymax)
  legend.SetTextSize(0.035)
  yields = {}
  if not blind:
    legend.AddEntry(h_data,"Data","elp")
    yields['Data'] = getInt(h_data)
  legend.AddEntry(h_all_prefit, "SM (pre-fit)", "l")
  #legend.AddEntry(h_all_postfit, "SM backgrounds (post-fit)", "l") 

  processes_reverted = processes[::-1]
  for process in processes_reverted:
    try:
      hist = h_postfit[process]
      if (not h_postfit[process]): continue
      if (str(h_postfit[process].Integral())=="nan"): continue
      legend.AddEntry(hist,processNames[process],"f")
      yields[processNames[process]] = getInt(hist)
    except KeyError:
      pass
#  if region=='signal':
#    legend.AddEntry(h_res,'Resonant M_{#phi}=1.1 TeV','l')
#    legend.AddEntry(h_fcnc,'FCNC M_{V}=0.9 TeV','l')
  legend.SetShadowColor(0);
  legend.SetFillColor(0);
  legend.SetFillStyle(0)
  legend.SetBorderSize(0)
  legend.SetLineColor(0);
  legend.Draw("same")

  l1=region+' & '
  for o in order:
    if o in yields:
      y = yields[o]
      if o=='Data':
        l1 += ' $%i$ & '%(int(y))
      else:
        l1 += ' $%.3g$ & '%y
    else:
      l1 += ' $-$ & '
  print l1

  latex2 = TLatex()
  latex2.SetNDC()
  latex2.SetTextSize(0.85*c.GetTopMargin())
  latex2.SetTextFont(42)
  latex2.DrawLatex(0.16, 0.825,extralabel)
  latex2.SetTextAlign(31) # align right
  latex2.SetTextSize(0.92*c.GetTopMargin())
  latex2.DrawLatex(0.92, 0.963,"%.1f fb^{-1} (13 TeV)"%(plotConfig.lumi))
  

  latex_CMS = TLatex()
  latex_CMS.SetNDC()
  latex_CMS.SetTextFont(42)
  latex_CMS.SetTextSize(0.06);
  latex_CMS.DrawLatex(0.16,0.87715,"#bf{CMS}#scale[0.8]{#it{ Preliminary}}")
  
  
  gPad.RedrawAxis()

  pad = TPad("pad", "pad", 0.0, 0.0, 1.0, 0.9)
  SetOwnership(pad,False)

  pad.SetTopMargin(0.7)
  pad.SetRightMargin(0.07)
  pad.SetLeftMargin(0.12)
  pad.SetFillColor(0)
  pad.SetGridy(0)
  pad.SetFillStyle(0)
  pad.Draw()
  pad.cd(0)

  met = []; dmet = [];
  ratio_pre = []; ratio_pre_hi = []; ratio_pre_lo = [];
  ratio_post = []; ratio_post_hi = []; ratio_post_lo = [];

  for i in range(1,h_all_prefit.GetNbinsX()+1):

    #ndata = array("d", [0.0])
    #metave = array("d",[0.0])
    #h_data.GetPoint(i-1, metave[0], ndata[0])

    #ndata = h_data.GetY()[i-1]
    if not blind:
      ndata = h_data.GetBinContent(i)
    else:
      ndata = 0
    #print ndata

    if (ndata>0.0 and not blind):
      e_data_hi = h_data.GetBinError(i)/ndata
      e_data_lo = h_data.GetBinError(i)/ndata
    else:
      e_data_hi = 0.0
      e_data_lo = 0.0
      
    n_all_pre = h_all_prefit.GetBinContent(i)
    n_all_post = h_all_postfit.GetBinContent(i)

    met.append(h_all_prefit.GetBinCenter(i))
    dmet.append((h_all_prefit.GetBinLowEdge(i+1)-h_all_prefit.GetBinLowEdge(i))/2)

    if (n_all_pre>0.0):
      ratio_pre.append(ndata/n_all_pre)
      ratio_pre_hi.append(ndata*e_data_hi/n_all_pre)
      ratio_pre_lo.append(ndata*e_data_lo/n_all_pre)
    else:
      ratio_pre.append(0.0)
      ratio_pre_hi.append(0.0)
      ratio_pre_lo.append(0.0)

    if (n_all_post>0.0):
      ratio_post.append(ndata/n_all_post)
      ratio_post_hi.append(ndata*e_data_hi/n_all_post)
      ratio_post_lo.append(ndata*e_data_lo/n_all_post)      
    else:
      ratio_post.append(0.0)
      ratio_post_hi.append(0.0)
      ratio_post_lo.append(0.0)

  a_met = array("d", met)
  v_met = TVectorD(len(a_met),a_met)
          
  a_dmet = array("d", dmet)
  v_dmet = TVectorD(len(a_dmet),a_dmet)
    
  a_ratio_pre = array("d", ratio_pre)
  a_ratio_pre_hi = array("d", ratio_pre_hi)
  a_ratio_pre_lo = array("d", ratio_pre_lo)
  
  v_ratio_pre = TVectorD(len(a_ratio_pre),a_ratio_pre)
  v_ratio_pre_hi = TVectorD(len(a_ratio_pre_hi),a_ratio_pre_hi)
  v_ratio_pre_lo = TVectorD(len(a_ratio_pre_lo),a_ratio_pre_lo)

  a_ratio_post = array("d", ratio_post)
  a_ratio_post_hi = array("d", ratio_post_hi)
  a_ratio_post_lo = array("d", ratio_post_lo)

  v_ratio_post = TVectorD(len(a_ratio_post),a_ratio_post)
  v_ratio_post_hi = TVectorD(len(a_ratio_post_hi),a_ratio_post_hi)
  v_ratio_post_lo = TVectorD(len(a_ratio_post_lo),a_ratio_post_lo)

  g_ratio_pre = TGraphAsymmErrors(v_met,v_ratio_pre,v_dmet,v_dmet,v_ratio_pre_lo,v_ratio_pre_hi)
  g_ratio_pre.SetLineColor(2)
  g_ratio_pre.SetMarkerColor(2)
  g_ratio_pre.SetMarkerStyle(20)

  g_ratio_post = TGraphAsymmErrors(v_met,v_ratio_post,v_dmet,v_dmet,v_ratio_post_lo,v_ratio_post_hi)
  g_ratio_post.SetLineColor(1)
  g_ratio_post.SetMarkerColor(1)
  g_ratio_post.SetMarkerStyle(20)
  
  ratiosys = h_postfit['totalv2'].Clone();
  ratiosys_prefit = h_postfit['total_prefit'].Clone();
  for hbin in range(0,ratiosys.GetNbinsX()+1): 
        
    ratiosys.SetBinContent(hbin+1,1.0)
    ratiosys_prefit.SetBinContent(hbin+1,1.0)
    if (h_postfit['totalv2'].GetBinContent(hbin+1)>0):
      print h_postfit['totalv2'].GetBinError(hbin+1)/h_postfit['totalv2'].GetBinContent(hbin+1)
      ratiosys.SetBinError(hbin+1,h_postfit['totalv2'].GetBinError(hbin+1)/h_postfit['totalv2'].GetBinContent(hbin+1))

    else:
      ratiosys.SetBinError(hbin+1,0)
    if (h_postfit['total_prefit'].GetBinContent(hbin+1)>0):
      print h_postfit['total_prefit'].GetBinError(hbin+1)/h_postfit['total_prefit'].GetBinContent(hbin+1)
      ratiosys_prefit.SetBinError(hbin+1,h_postfit['total_prefit'].GetBinError(hbin+1)/h_postfit['total_prefit'].GetBinContent(hbin+1))

    else:
      ratiosys_prefit.SetBinError(hbin+1,0)


  dummy2 = TH1F("dummy2","dummy2",len(binLowE)-1,array('d',binLowE))
  for i in range(1,dummy2.GetNbinsX()):
    dummy2.SetBinContent(i,1.0)
  dummy2.GetYaxis().SetTitle("Data / Pred.")
  dummy2.GetXaxis().SetTitle("Recoil (GeV)")
  dummy2.SetLineColor(0)
  dummy2.SetMarkerColor(0)
  dummy2.SetLineWidth(0)
  dummy2.SetMarkerSize(0)
  dummy2.GetYaxis().SetLabelSize(0.03)
  dummy2.GetYaxis().SetNdivisions(5);
  dummy2.GetXaxis().SetNdivisions(510)
  dummy2.GetYaxis().CenterTitle()
  dummy2.GetYaxis().SetTitleSize(0.04)
  dummy2.GetYaxis().SetTitleOffset(1.5)

  dummy2.SetMaximum(2.1)
  dummy2.SetMinimum(0.1)
  dummy2.Draw("hist")

  ratiosys.SetFillColor(syst_color) #SetFillColor(ROOT.kYellow)
  ratiosys.SetLineColor(syst_color) #SetLineColor(1)
  ratiosys.SetLineWidth(1)
  ratiosys.SetMarkerSize(0)
  ratiosys.Draw("e2same")

  ratiosys_prefit.SetFillColor(kGreen) #SetFillColor(ROOT.kYellow)
  ratiosys_prefit.SetLineColor(kGreen) #SetLineColor(1)
  ratiosys_prefit.SetFillStyle(3415) #SetLineColor(1)
  ratiosys_prefit.SetLineWidth(1)
  ratiosys_prefit.SetMarkerSize(1)
  ratiosys_prefit.Draw("e2same")

  

  f1 = TF1("f1","1",-5000,5000);
  f1.SetLineColor(1);
  f1.SetLineStyle(2);
  f1.SetLineWidth(2);
  f1.Draw("same")

  if not blind:
    g_ratio_pre.Draw("epsame")
    g_ratio_post.Draw("epsame")
    
    f_ratios = open('ratios_%s.txt' % region, 'w')

    print >> f_ratios, 'type x y yerrup yerrdown'
    for i in range(1,dummy2.GetNbinsX()+1):
      xval = ROOT.Double(0.)
      yval = ROOT.Double(0.)
      g_ratio_pre.GetPoint(i-1,xval,yval)
      print >> f_ratios,'pre' + ' ' + str(xval) + ' ' + str(yval) + ' ' + str(g_ratio_pre.GetErrorYhigh(i-1)) + ' ' + str(g_ratio_pre.GetErrorYlow(i-1)) 
      xval = ROOT.Double(0.)
      yval = ROOT.Double(0.)
      g_ratio_post.GetPoint(i-1,xval,yval)
      print >> f_ratios,'post' + ' ' + str(xval) + ' ' + str(yval) + ' ' + str(g_ratio_post.GetErrorYhigh(i-1)) + ' ' + str(g_ratio_post.GetErrorYlow(i-1)) 
      

    for i in range(1,ratiosys.GetNbinsX()+1):
      print >> f_ratios,'unc' + ' ' + str(ratiosys.GetXaxis().GetBinLowEdge(i)) + ' ' + str(ratiosys.GetXaxis().GetBinUpEdge(i)) + ' ' + str(ratiosys.GetBinError(i)) + ' ' + str(ratiosys.GetBinError(i))

    f_ratios.close()

    legend2 = TLegend(.60,.25,.75,.29)
    legend3 = TLegend(.75,.25,.90,.29)
    legend4 = TLegend(.30,.25,.45,.29)
    legend5 = TLegend(.15,.25,.30,.29)
    legend2.AddEntry(g_ratio_pre,"pre-fit","elp")
    legend3.AddEntry(g_ratio_post,"post-fit","elp")
    legend4.AddEntry(ratiosys,"post-fit","f")
    legend5.AddEntry(ratiosys_prefit,"pre-fit","f")
    for l in [legend2,legend3,legend4,legend5]:
      l.SetShadowColor(0);
      l.SetFillColor(0);
      l.SetFillStyle(0)
      l.SetBorderSize(0)
      l.SetLineColor(0);
      l.Draw()
    
  plotsDir = plotConfig.plotDir


  c.SaveAs(plotsDir+"MSDcorr_stackedPostfit_"+region+".pdf")
  c.SaveAs(plotsDir+"MSDcorr_stackedPostfit_"+region+".png")
  c.SaveAs(plotsDir+"MSDcorr_stackedPostfit_"+region+".C")

  #c.SaveAs("test.pdf")

  #del c
  #del process
  #del colors
  #del h_prefit


plotPreFitPostFit("singlemuonw")
plotPreFitPostFit("singlemuonw_fail")
plotPreFitPostFit("singlemuontop")
plotPreFitPostFit("dimuon")
plotPreFitPostFit("dimuon_fail")
plotPreFitPostFit("singleelectronw")
plotPreFitPostFit("singleelectrontop")
plotPreFitPostFit("dielectron")
plotPreFitPostFit("dielectron_fail")
#plotPreFitPostFit("photon")

#plotPreFitPostFit("signal") ### fitting to real data now!
