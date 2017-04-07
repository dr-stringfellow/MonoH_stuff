from ROOT import *
from array import array
from tdrStyle import *
setTDRStyle()

import math

def plot_ratio(process,category):

    highest = {}
    highest2 = {}
    lowest = {}

    f = TFile('combined_model.root','READ')
        
    if (process=='zmm'):
        dirname = "Z_constraints_category_"+category
        base    = "zmm_weights_"+category
        label = "R_{Z(#mu#mu)}"
        addsys  = math.sqrt(0.02*0.02)

    if (process=='zee'):
        dirname = "Z_constraints_category_"+category
        base    = "zee_weights_"+category
        label   = "R_{Z(ee)}"
        addsys  = math.sqrt(0.04*0.04 + 0.01*0.01)

    if (process=='photon'):
        dirname = "Z_constraints_category_"+category 
        base    = "photon_weights_"+category
        label   = "R_{#gamma}"
        addsys  = 0

    if (process=='w_weights'):
        dirname = "Z_constraints_category_"+category 
        base    = "w_weights_"+category
        label   = "R_{Z/W}"
        addsys  = 0.0

    if (process=='wen'):
        dirname = "W_constraints_category_"+category 
        base    = "wen_weights_"+category
        label   = "R_{W(e#nu)}"
        #addsys  = math.sqrt(0.05*0.05 + 0.01*0.01 + 0.03*0.03)
        addsys  = 0.01

    if (process=='wmn'):
        dirname = "W_constraints_category_"+category 
        base    = "wmn_weights_"+category
        label   = "R_{W(#mu#nu)}"
        #addsys  = math.sqrt(0.03*0.03 + 0.01*0.01)
        addsys  = 0.01
        

    ratio = f.Get(dirname+"/"+base)
    up_final = ratio.Clone("ratio")
    up_ewk = ratio.Clone("ratio")
    down_final = ratio.Clone("ratio")

    for b in range(ratio.GetNbinsX()+1):
        up_final.SetBinContent(b,0.0)
        up_ewk.SetBinContent(b,0.0)
        down_final.SetBinContent(b,0.0)
        highest[b] = 0
        highest2[b] = 0
        lowest [b] = 100.0

    f.cd(dirname)
    for key in gDirectory.GetListOfKeys():
        if (key.GetClassName(),"TH1"):
            if process in key.GetName():
                #print key.GetName()
                if ('Up' in key.GetName()):
                    #print key.GetName()
                    up = f.Get(dirname+"/"+key.GetName())
                    for b in range(ratio.GetNbinsX()+1):
                        diff = up.GetBinContent(b) - ratio.GetBinContent(b)
                        highest[b] =  math.sqrt(highest[b]**2 + diff**2)
                        #bin =  ratio.GetXaxis().FindBin(1000)
                        #if b >= bin and 'scale' in key.GetName():
                        #    print key.GetName(), bin
                        #    highest[b] = math.sqrt(highest[b]**2 + (ratio.GetBinContent(b)*0.1)**2)
                        up_final.SetBinContent(b,highest[b])

                        if ('ewk' in key.GetName() or 'stat' in key.GetName()):
                            diff2 = up.GetBinContent(b) - ratio.GetBinContent(b)
                            highest2[b] =  math.sqrt(highest2[b]**2 + diff2**2)
                            up_ewk.SetBinContent(b,highest2[b])

                if ('Down' in key.GetName()):
                    down = f.Get(dirname+"/"+key.GetName())
                    for b in range(ratio.GetNbinsX()+1):
                        if down.GetBinContent(b) < lowest[b]:
                            lowest[b] = down.GetBinContent(b)
                        else:
                            lowest[b] = lowest[b]
                        down_final.SetBinContent(b,lowest[b])
              
    gStyle.SetOptStat(0)

    c = TCanvas("c","c",600,600)  
    c.SetTopMargin(0.06)
    c.cd()
    c.SetRightMargin(0.04)
    c.SetTopMargin(0.07)
    c.SetLeftMargin(0.12)


    uncertband    = ratio.Clone("ratio")
    uncertband2   = ratio.Clone("ratio2")
    for b in range(ratio.GetNbinsX()+1):
        #err1 = abs(down_final.GetBinContent(b) -  ratio.GetBinContent(b))
        err1 = abs(up_final.GetBinContent(b) -  ratio.GetBinContent(b))
        #uncertband.SetBinError(b,max(err1,err2))
        #uncertband.SetBinError(b,err1)
        uncertband.SetBinError(b,up_final.GetBinContent(b) + addsys)
        uncertband2.SetBinError(b,up_ewk.GetBinContent(b))
        #print "Uncert",b,ratio.GetBinContent(b),down_final.GetBinContent(b),up_final.GetBinContent(b), max(err1,err2)

    #uncertband.SetFillStyle(3144);
    #uncertband.SetFillColor(33);

    #uncertband.SetFillStyle(0);
    uncertband2.SetFillColor(ROOT.kOrange+1);
    #uncertband2.SetFillColor(ROOT.kGray);
    
    if process == "photon" or process == "w_weights":
        uncertband.SetFillColor(ROOT.kGreen+1);
        #uncertband.SetFillColor(ROOT.kMagenta+3);
    else:
        uncertband.SetFillColor(ROOT.kOrange+1);
        #uncertband.SetFillColor(ROOT.kGray);

    uncertband.GetYaxis().SetTitle(label)
    uncertband.GetYaxis().CenterTitle()
    uncertband.GetYaxis().SetTitleSize(0.4*c.GetLeftMargin())
    uncertband.GetXaxis().SetTitle("U [GeV]")
    uncertband.GetXaxis().SetTitleSize(0.4*c.GetBottomMargin())
    uncertband.SetMaximum(1.5*ratio.GetMaximum())
    uncertband.SetMinimum(0.5*ratio.GetMinimum())
    uncertband.GetYaxis().SetTitleOffset(1.15)

    ratio.SetMarkerStyle(20)
    ratio.SetLineColor(1)
    ratio.SetLineWidth(2)

    uncertband.Draw("e2")    
    uncertband2.Draw("e2same")    
    ratio.Draw("same")

    legend = TLegend(.45,.75,.82,.92)
    legend.AddEntry(ratio,"Transfer Factor (Stat Uncert)" , "p")
    if process == "photon" or process == "w_weights":
        legend.AddEntry(uncertband ,"Stat + Sys Uncert" , "f")
        legend.AddEntry(uncertband2,"UnCorr Stat + Sys Uncert" , "f")
    else:
        legend.AddEntry(uncertband2,"UnCorr Stat + Sys Uncert" , "f")
        
        
    legend.SetShadowColor(0);
    legend.SetFillColor(0);
    legend.SetLineColor(0);

    legend.Draw("same")

    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.035)
    latex2.SetTextAlign(31) # align right
    latex2.DrawLatex(0.87, 0.95, "2.6 fb^{-1} (13 TeV)");

    latex3 = TLatex()
    latex3.SetNDC()
    latex3.SetTextSize(0.75*c.GetTopMargin())
    latex3.SetTextFont(62)
    latex3.SetTextAlign(11) # align right
    latex3.DrawLatex(0.22, 0.85, "CMS");
    latex3.SetTextSize(0.5*c.GetTopMargin())
    latex3.SetTextFont(52)
    latex3.SetTextAlign(11)
    latex3.DrawLatex(0.20, 0.8, "Preliminary");
    
    gPad.RedrawAxis()

    folder = "/afs/cern.ch/user/z/zdemirag/www/Monojet/ichep_80x/topupv2/fits/"
    c.SaveAs(folder+"/rfactor_"+category+"_"+process+".pdf")
    c.SaveAs(folder+"/rfactor_"+category+"_"+process+".png")
    c.SaveAs(folder+"/rfactor_"+category+"_"+process+".C")

    #c.SaveAs("rfactor_"+process+".root")

    #f_out = TFile(process+".root","recreate")
    #f_out.cd()
    #ratio.Write()
    #f_out.Close()

    del c
 
plot_ratio('zmm','monojet')
plot_ratio('zee','monojet')
plot_ratio('w_weights','monojet')
plot_ratio('photon','monojet')
plot_ratio('wen','monojet')
plot_ratio('wmn','monojet')

plot_ratio('zmm','monov')
plot_ratio('zee','monov')
plot_ratio('w_weights','monov')
plot_ratio('photon','monov')
plot_ratio('wen','monov')
plot_ratio('wmn','monov')
