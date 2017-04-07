from sys import argv; argv = []

from ROOT import *
from collections import namedtuple 
from os import getenv
from array import array
from tdrStyle import *
import plotConfig
setTDRStyle()

basedir = getenv('CMSSW_BASE')+'/src/MonoXFit_CSV/'

f_mlfit = TFile(basedir+'/datacards/mlfit.root','READ')
f_data = TFile(basedir+"/mono-x.root","READ")

Region = namedtuple('Region',['monox_name','label','main_proc','main_bkg'])
regions = {
        'pho' : Region('photon','#gamma','gjets','qcd'),
        'zmm' : Region('dimuon','Z#rightarrow#mu#mu','zll','ttbar'),
        'zee' : Region('dielectron','Z#rightarrowee','zll','ttbar'),
        'wmn' : Region('singlemuonw','W#rightarrow#mu#nu','wjets','ttbar'),
        'wen' : Region('singleelectronw','W#rightarrowe#nu','wjets','ttbar'),
        'tmn' : Region('singlemuontop','t#rightarrowb#mu#nu','ttbar',None),
        'ten' : Region('singleelectrontop','t#rightarrowbe#nu','ttbar',None),
}

def build_ratio(hnum,hden,both_unc=True):
    hratio = hnum.Clone()
    hratio.Divide(hden)
    return hratio

def subtract(hdata,hbkg):
    hsub = hdata.Clone()
    hsub.Add(hbkg,-1)
    return hsub

def scale(h):
    h_scale = h.Clone()
    nbins = h.GetNbinsX();
    for ib in xrange(1,nbins+1):
        width = h.GetBinWidth(ib)
        h_scale.SetBinContent(ib,h.GetBinContent(ib)/width)
        h_scale.SetBinError(ib,h.GetBinError(ib)/width)
    return h_scale

def plot_ratio(num_region,den_region,cat,folder='shapes_prefit'):
    num = regions[num_region]
    den = regions[den_region]

    # first get the data
    monox_cat = 'category_monotop' if cat=='tight' else 'category_monotop_loose'
    hnum_data = f_data.Get(monox_cat+'/%s_data'%(num.monox_name))
    hden_data = f_data.Get(monox_cat+'/%s_data'%(den.monox_name))
    hnum_data = scale(hnum_data)
    hden_data = scale(hden_data)
    
    # now get the leading bkg
    hnum_mainproc = f_mlfit.Get(folder+'/'+cat+'_'+num_region+'/'+num.main_proc)
    hden_mainproc = f_mlfit.Get(folder+'/'+cat+'_'+den_region+'/'+den.main_proc)

    # subleading background to subtract (if necessary)
    if num.main_bkg:
        hnum_mainbkg = f_mlfit.Get(folder+'/'+cat+'_'+num_region+'/'+num.main_bkg)
        hnum_data = subtract(hnum_data,hnum_mainbkg)
    if den.main_bkg:
        hden_mainbkg = f_mlfit.Get(folder+'/'+cat+'_'+den_region+'/'+den.main_bkg)
        hden_data = subtract(hden_data,hden_mainbkg)
    
    hdata = build_ratio(hnum_data,hden_data)
    hmc = build_ratio(hnum_mainproc,hden_mainproc)
                        
    gStyle.SetOptStat(0)

    c = TCanvas("c","c",600,700)  
    SetOwnership(c,False)
    c.cd()

    hdata.SetLineColor(1); hdata.SetLineWidth(2)
    hdata.SetMarkerStyle(20)
    hmc.SetMinimum(0) 
    hmc.SetMaximum(2*max(hdata.GetMaximum(),hmc.GetMaximum()))
    hmc.SetLineWidth(2)
    hmc.SetLineColor(2)
    hmc_err = hmc.Clone()
    hmc_err.SetLineWidth(0)
    hmc_err.SetLineColor(kGray)
    hmc_err.SetFillColor(kGray)
    hmc_err.GetXaxis().SetTitle('U [GeV]')
    hmc_err.GetYaxis().SetTitle('')
    hmc_err.Draw('e2')
    hmc.Draw('hist same')
    hdata.Draw('elp same')

    legend = TLegend(.55,.75,.95,.90)
    legend.AddEntry(hdata, "Data", "p")
    legend.AddEntry(hmc, "Prediction", "l") 
    legend.AddEntry(hmc_err,'Stat+sys unc','f')
    legend.SetShadowColor(0);
    legend.SetFillColor(0);
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetLineColor(0);
    legend.Draw('same')

    latex = TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.SetTextSize(0.8*c.GetTopMargin())
    latex.DrawLatex(0.2, 0.8,'#frac{%s}{%s}'%(num.label,den.label))

    plotname = 'ratio_%s_%s_%s_%s'%(cat,num_region,den_region,folder)
    for ext in ['pdf','png','C']:
        c.SaveAs(plotConfig.plotDir+plotname+'.'+ext)

    del c


plot_ratio('pho','zmm','tight',folder='shapes_prefit')
plot_ratio('pho','zmm','tight',folder='shapes_fit_b')

plot_ratio('pho','zmm','loose',folder='shapes_prefit')
plot_ratio('pho','zmm','loose',folder='shapes_fit_b')

plot_ratio('pho','zee','tight',folder='shapes_prefit')
plot_ratio('pho','zee','tight',folder='shapes_fit_b')

plot_ratio('pho','zee','loose',folder='shapes_prefit')
plot_ratio('pho','zee','loose',folder='shapes_fit_b')

plot_ratio('wmn','zmm','tight',folder='shapes_prefit')
plot_ratio('wmn','zmm','tight',folder='shapes_fit_b')

plot_ratio('wmn','zmm','loose',folder='shapes_prefit')
plot_ratio('wmn','zmm','loose',folder='shapes_fit_b')

plot_ratio('wen','zee','tight',folder='shapes_prefit')
plot_ratio('wen','zee','tight',folder='shapes_fit_b')

plot_ratio('wen','zee','loose',folder='shapes_prefit')
plot_ratio('wen','zee','loose',folder='shapes_fit_b')

plot_ratio('wen','pho','tight',folder='shapes_prefit')
plot_ratio('wen','pho','tight',folder='shapes_fit_b')

plot_ratio('wen','pho','loose',folder='shapes_prefit')
plot_ratio('wen','pho','loose',folder='shapes_fit_b')

plot_ratio('wmn','pho','tight',folder='shapes_prefit')
plot_ratio('wmn','pho','tight',folder='shapes_fit_b')

plot_ratio('wmn','pho','loose',folder='shapes_prefit')
plot_ratio('wmn','pho','loose',folder='shapes_fit_b')

plot_ratio('wmn','wen','loose',folder='shapes_prefit')
plot_ratio('wmn','wen','loose',folder='shapes_fit_b')

plot_ratio('zmm','zee','loose',folder='shapes_prefit')
plot_ratio('zmm','zee','loose',folder='shapes_fit_b')

plot_ratio('wmn','wen','tight',folder='shapes_prefit')
plot_ratio('wmn','wen','tight',folder='shapes_fit_b')

plot_ratio('zmm','zee','tight',folder='shapes_prefit')
plot_ratio('zmm','zee','tight',folder='shapes_fit_b')
