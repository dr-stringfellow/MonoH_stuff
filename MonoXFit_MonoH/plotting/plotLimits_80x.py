from ROOT import TCanvas, TGraph, TGraphAsymmErrors, TLegend, TLatex, TMarker
from array import array
from sys import argv,stdout
from tdrStyle import *
import plotConfig

setTDRStyle()

VERBOSE=False
''' # old xsecs
resonantXsecs = {
  1100 : 3.91,
  900 : 9.37,
  1300 : 1.81,
  1500 : 0.9,
  1700 : 0.47,
  1900 : 0.25,
  2100 : 0.14,
    }

fcncXsecs = {
  300 : 27.6,
  500 : 6.52,
  700 : 2.06,
  900 : 0.78,
  1100 : 0.33,
  1300 : 0.15,
  1500 : 0.076
    }
'''

resonantXsecs = {
  900 : 3.09067,
  1100 : 1.307,
  1300 : 0.6149,
  1500 : 0.314,
  1700 : 0.1699,
  1900 : 0.0962,
  2100 : 0.05673,
  2300 : 0.03456,
  2500 : 0.02148,
  2700 : 0.01375,
  2900 : 0.008956,
    }

fcncXsecs = {
  50 : 2223,
  100 :  750.4,
  150 :  370.85,
  200 :  187.1545,
  300 :  48.4024,
  500 :  9.23265,
  700 :  2.836662,
  900 :  1.098356,
  1100 : 0.4855015,
  1300 : 0.2350739,
  1500 : 0.12218969,
  1700 : 0.06657825,
  1900 : 0.03860199,
  2100 : 0.02303869,
    }

BLIND=False

def parseLine(l):
  if 'Observed' in l:
    return 'Observed',float(l.split('<')[1])
  return float(l.split()[1].strip(':%')),float(l.split('<')[1])

def findIntersect(g1,g2,x1,x2):
  orientation = (g1.Eval(x1)<g2.Eval(x1))
  for iX in xrange(1000):
    x = (x2-x1)*iX/1000.+x1
    if orientation != (g1.Eval(x)<g2.Eval(x)):
      # return TGraph(1,array('f',[x]),array('f',[g1.Eval(x)]))
      return TMarker(x,g1.Eval(x),1)
      # return x
  print 'Could not find intersection!'
  return None


def makePlot(finname,foutname,plottitle='',masstitle='',scale=False):
  xsecs = resonantXsecs if 'resonant' in finname else fcncXsecs
  points = {}
  if BLIND:
    cls = [2.5, 16, 50, 84, 97.5]
  else:
    cls = [2.5, 16, 50, 84, 97.5,'Observed']
  xaxis = []
  for cl in cls:
    points[cl] = []
  xsec=1
  for l in open(finname):
    try:
      if l.strip()[0]=='#':
        continue
      if 'MASS' in l:
        if scale:
          xsec = xsecs[int(l.split()[1])] 
        if VERBOSE:
          print ''
          stdout.write('$%6s$ & $%7.3g$'%(l.split()[1],xsec/(0.667)))
        xaxis.append(float(l.split()[1]))
      else:
        cl,val = parseLine(l)
        points[cl].append(val/xsec)
        if VERBOSE and (cl==50 or cl=='Observed'):
          stdout.write(' & $%10.4g$'%(val/xsec))
    except:
      pass
  if VERBOSE:
    print ''
  
  N = len(xaxis)
  up1Sigma=[]; up2Sigma=[]
  down1Sigma=[]; down2Sigma=[]
  for iM in xrange(N):
    up1Sigma.append(points[84][iM]-points[50][iM])
    up2Sigma.append(points[97.5][iM]-points[50][iM])
    down1Sigma.append(-points[16][iM]+points[50][iM])
    down2Sigma.append(-points[2.5][iM]+points[50][iM])
  
  up1Sigma = array('f',up1Sigma)
  up2Sigma = array('f',up2Sigma)
  down1Sigma = array('f',down1Sigma)
  down2Sigma = array('f',down2Sigma)
  cent = array('f',points[50])
  if not BLIND:
    obs = array('f',points['Observed'])
  xarray = array('f',xaxis)

  xsecarray = array('f',[xsecs[xx] for xx in xaxis])
  xsecarrayLow = array('f',[0.0625*xsecs[xx] for xx in xaxis])
  onearray = array('f',[1 for xx in xaxis])
  graphXsec = TGraph(N,xarray,xsecarray)
  graphXsecLow = TGraph(N,xarray,xsecarrayLow)
  graphOne = TGraph(N,xarray,onearray)

  zeros = array('f',[0 for i in xrange(N)])
  graphCent = TGraph(N,xarray,cent)
  if not BLIND:
    graphObs = TGraph(N,xarray,obs)
  graph1Sigma = TGraphAsymmErrors(N,xarray,cent,zeros,zeros,down1Sigma,up1Sigma)
  graph2Sigma = TGraphAsymmErrors(N,xarray,cent,zeros,zeros,down2Sigma,up2Sigma)
  c = TCanvas('c','c',700,600)
  c.SetLogy()
  c.SetLeftMargin(.15)
  graph2Sigma.GetXaxis().SetTitle(masstitle+' [GeV]')
  if scale:
    graph2Sigma.GetYaxis().SetTitle('Upper limit [#sigma/#sigma_{theory}]')  
  else:
    graph2Sigma.GetYaxis().SetTitle("Upper limit [#sigma] [pb]")  
  graph2Sigma.SetLineColor(5)
  graph1Sigma.SetLineColor(3)
  graph2Sigma.SetFillColor(5)
  graph1Sigma.SetFillColor(3)
  graph2Sigma.SetMinimum(0.5*min(points[2.5]))
  if scale:
    graph2Sigma.SetMaximum(10*max(max(points[97.5]),max(xsecarray),4))
  else:
    graph2Sigma.SetMaximum(10*max(max(points[97.5]),max(xsecarray)))
  graphCent.SetLineWidth(2)
  graphCent.SetLineStyle(2)
  if not BLIND:
    graphObs.SetLineColor(1)
    graphObs.SetLineWidth(3)
  graph1Sigma.SetLineStyle(0)
  graph2Sigma.SetLineStyle(0)
 
  leg = TLegend(0.55,0.7,0.9,0.9)
  leg.AddEntry(graphCent,'Expected','L')
  if not BLIND:
    leg.AddEntry(graphObs,'Observed','L')
  leg.AddEntry(graph1Sigma,'1 #sigma','F')
  leg.AddEntry(graph2Sigma,'2 #sigma','F')
  leg.SetFillStyle(0)
  leg.SetBorderSize(0)

  graph2Sigma.Draw('A3')
  graph1Sigma.Draw('3 same')
  graphCent.Draw('same L')
  subscript = 'SR' if 'Resonant' in plottitle else 'FC'
  coupling = '0.1' if 'Resonant' in plottitle else '0.25'
  if not BLIND:
    graphObs.Draw('same L')
  if scale:
    graphOne.SetLineColor(2)
    graphOne.SetLineWidth(2)
    graphOne.SetLineStyle(2)
    graphOne.Draw('same L')
  else:
    graphXsec.SetLineColor(2)
    graphXsecLow.SetLineColor(4)
    if 'Resonant' in plottitle:
      leg.AddEntry(graphXsec,'Theory #splitline{a_{%s}=b_{%s}=%s}{m_{#chi}=100 GeV}'%(subscript,subscript,coupling),'l')
    else:
      leg.AddEntry(graphXsec,'Theory #splitline{a_{%s}=b_{%s}=%s}{m_{#chi}=10 GeV}'%(subscript,subscript,coupling),'l')
#    leg.AddEntry(graphXsecLow,'Theory a_{%s}=b_{%s}=0.025'%(subscript,subscript),'l')
    for g in [graphXsec]:
      g.SetLineWidth(2)
      g.SetLineStyle(2)
      g.Draw('same L')
  if not BLIND:
    gx = graphOne if scale else graphXsec
    obslimit = findIntersect(graphObs,gx,xaxis[0],xaxis[-1])
    if obslimit:
      obslimit.SetMarkerStyle(29); obslimit.SetMarkerSize(3)
      obslimit.Draw('p same')
    explimit = findIntersect(graphCent,gx,xaxis[0],xaxis[-1])
    if explimit:
      explimit.SetMarkerStyle(30); explimit.SetMarkerSize(3)
      explimit.Draw('p same')
  leg.Draw()
  label = TLatex()
  label.SetNDC()
  label.SetTextFont(62)
  label.SetTextAlign(11)
  label.DrawLatex(0.19,0.85,"CMS")
  label.SetTextFont(52)
  label.DrawLatex(0.28,0.85,"Preliminary")
  label.SetTextFont(42)
  label.SetTextSize(0.6*c.GetTopMargin())
  label.DrawLatex(0.19,0.77,plottitle)
  if scale:
    if 'Resonant' in plottitle:
      label.DrawLatex(0.19,0.7,"a_{SR} = b_{SR} = %s"%coupling)
      label.DrawLatex(0.19,0.64,"m_{#chi}=100 GeV")
    else:
      label.DrawLatex(0.19,0.7,"a_{FC} = b_{FC} = %s"%coupling)
      label.DrawLatex(0.19,0.64,"m_{#chi}=10 GeV")
  label.SetTextSize(0.5*c.GetTopMargin())
  label.SetTextFont(42)
  label.SetTextAlign(31) # align right
  label.DrawLatex(0.9, 0.94,"%.1f fb^{-1} (13 TeV)"%(plotConfig.lumi))
  c.SaveAs(foutname+'.pdf')
  c.SaveAs(foutname+'.png')

plotsdir = plotConfig.plotDir

makePlot('../datacards/fcncv3_obs_limits.txt',plotsdir+'fcncv3_obs_limits_xsec','#splitline{Flavor-changing}{neutral current}','M_{V}')
makePlot('../datacards/fcncv3_obs_limits.txt',plotsdir+'fcncv3_obs_limits','#splitline{Flavor-changing}{neutral current}','M_{V}',True)
makePlot('../datacards/resonantv3_obs_limits.txt',plotsdir+'resonantv3_obs_limits_xsec','#splitline{Resonant}{production}','M_{#phi}')
makePlot('../datacards/resonantv3_obs_limits.txt',plotsdir+'resonantv3_obs_limits','#splitline{Resonant}{production}','M_{#phi}',True)
