from ROOT import *
from math import sqrt
from array import array
from tdrStyle import *
from os import getenv
import plotConfig

setTDRStyle()

def plot_ratio(process,suffix = ''):

		highest = {}
		lowest = {}

		baseDir = getenv('CMSSW_BASE')+'/src/MonoXFit_CSV/'
		f = TFile(baseDir + 'combined_model.root','READ')

		if 'electron' in process:
			extralabel = 'Electrons'
		elif 'muon' in process:
			extralabel = 'Muons'
		elif 'photon' in process:
			extralabel = 'Photons'
		else:
			extralabel = ''

		if (process=='wz'):
				dirname = 'Z_constraints_category_monotop'+suffix
				base		= 'w_weights_monotop'+suffix
				label	 = 'Z#rightarrow#nu#nu/W#rightarrow(l)#nu'
				addsys = 0

		if (process=='dimuon'):
				dirname = "Z_constraints_category_monotop"+suffix
				base		= "zmm_weights_monotop"+suffix
				label	 = 'Z#rightarrow#nu#nu/Z#rightarrow#mu#mu'
				addsys	= sqrt(0.02*0.02)

		if (process=='dielectron'):
				dirname = "Z_constraints_category_monotop"+suffix
				base		= "zee_weights_monotop"+suffix
				label	 = 'Z#rightarrow#nu#nu/Z#rightarrowee'
				addsys	= sqrt(0.04*0.04)

		if (process=='photon'):
				dirname = "Z_constraints_category_monotop"+suffix
				base		= "photon_weights_monotop"+suffix
				label	 = 'Z#rightarrow#nu#nu/#gamma'
				addsys	= 0

		if (process=='singleelectronw'):
				dirname = "W_constraints_category_monotop"+suffix
				base		= "wen_weights_monotop"+suffix
				label	 = 'W#rightarrow(l)#nu/W#rightarrowe#nu'
				addsys	= sqrt(0.02*0.02)

		if (process=='singlemuonw'):
				dirname = "W_constraints_category_monotop"+suffix
				base		= "wmn_weights_monotop"+suffix
				label	 = 'W#rightarrow(l)#nu/W#rightarrow#mu#nu'
				addsys	= sqrt(0.01*0.01)

		if (process=='singleelectrontop'):
				dirname = "Top_constraints_category_monotop"+suffix
				base		= "topen_weights_monotop"+suffix
				label	 = 't#rightarrowb(l)#nu/t#rightarrowbe#nu'
				addsys	= sqrt(0.02*0.02)

		if (process=='singlemuontop'):
				dirname = "Top_constraints_category_monotop"+suffix
				base		= "topmn_weights_monotop"+suffix
				label	 = 't#rightarrowb(l)#nu/t#rightarrowb#mu#nu'
				addsys	= sqrt(0.01*0.01)

		if (process=='singleelectronwtop'):
				dirname = "Top_constraints_category_monotop"+suffix
				base		= "topwen_weights_monotop"+suffix
				label	 = 't#rightarrowb(l)#nu/t#rightarrow(b)e#nu'
				addsys	= sqrt(0.02*0.02)

		if (process=='singlemuonwtop'):
				dirname = "Top_constraints_category_monotop"+suffix
				base		= "topwmn_weights_monotop"+suffix
				label	 = 't#rightarrowb(l)#nu/t#rightarrow(b)#mu#nu'
				addsys	= sqrt(0.01*0.01)

		ratio = f.Get(dirname+"/"+base)
		up_final = ratio.Clone("ratio")
		down_final = ratio.Clone("ratio")

		for b in range(ratio.GetNbinsX()+1):
				up_final.SetBinContent(b,0.0)
				down_final.SetBinContent(b,0.0)
				highest[b] = 0
				lowest [b] = 100.0

		f.cd(dirname)
		for key in gDirectory.GetListOfKeys():
				if ('TH1' in key.GetClassName()):
						if (process in key.GetName()) or (base in key.GetName()):
								if ('Up' in key.GetName()):
										up = f.Get(dirname+"/"+key.GetName())
										for b in range(ratio.GetNbinsX()+1):
												diff = up.GetBinContent(b) - ratio.GetBinContent(b)
												highest[b] =	sqrt(highest[b]**2 + diff**2)
												#if up.GetBinContent(b) > highest[b]:
												#		highest[b] = up.GetBinContent(b)
												#else:
												#		highest[b] = highest[b]
												up_final.SetBinContent(b,highest[b])

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
		c.SetLeftMargin(0.15)


		uncertband = ratio.Clone("ratio")
		for b in range(ratio.GetNbinsX()+1):
				#err1 = abs(down_final.GetBinContent(b) -	ratio.GetBinContent(b))
				err1 = abs(up_final.GetBinContent(b) -	ratio.GetBinContent(b))
				#uncertband.SetBinError(b,max(err1,err2))
				#uncertband.SetBinError(b,err1)
				uncertband.SetBinError(b,up_final.GetBinContent(b) + ratio.GetBinContent(b)*addsys)
#				print b,up_final.GetBinContent(b),ratio.GetBinContent(b),addsys
				#print "Uncert",b,ratio.GetBinContent(b),down_final.GetBinContent(b),up_final.GetBinContent(b), max(err1,err2)

		#uncertband.SetFillStyle(3144);
		#uncertband.SetFillColor(33);

		#uncertband.SetFillStyle(0);
		uncertband.SetFillColor(ROOT.kGray+1);

		uncertband.GetYaxis().SetTitle(label)
		uncertband.GetYaxis().CenterTitle()
		uncertband.GetYaxis().SetTitleSize(0.4*c.GetLeftMargin())
		uncertband.GetXaxis().SetTitle("U [GeV]")
		uncertband.GetXaxis().SetTitleSize(0.4*c.GetBottomMargin())
		uncertband.SetMaximum(1.5*(ratio.GetMaximum()+uncertband.GetBinError(uncertband.GetNbinsX())))
		uncertband.SetMinimum(0)
		#uncertband.SetMinimum(0.5*ratio.GetMinimum())
#		uncertband.SetMinimum(0)
		uncertband.GetYaxis().SetTitleOffset(1.15)

		ratio.SetMarkerStyle(20)
		ratio.SetLineColor(1)
		ratio.SetLineWidth(2)

		uncertband.Draw("e2")		
		ratio.Draw("same")

		legend = TLegend(.60,.75,.92,.92)
		legend.AddEntry(ratio,"Transfer Factor (Stat Uncert)" , "p")
		legend.AddEntry(uncertband,"Stat + Sys Uncert" , "f")

		legend.SetShadowColor(0);
		legend.SetFillColor(0);
		legend.SetLineColor(0);

		legend.Draw("same")

		latex2 = TLatex()
		latex2.SetNDC()
		latex2.SetTextSize(0.035)
		latex2.SetTextAlign(11) # align left
		latex2.DrawLatex(0.15, 0.95, extralabel);
		latex2.SetTextAlign(31) # align right
		latex2.DrawLatex(0.87, 0.95, "%.1f fb^{-1} (13 TeV)"%(plotConfig.lumi));
#		latex2.DrawLatex(0.87, 0.95, "2.1 pb^{-1} (13 TeV)");

		#latex3 = TLatex()
		#latex3.SetNDC()
		#latex3.SetTextSize(0.75*c.GetTopMargin())
		latex2.SetTextSize(0.7*c.GetTopMargin())
		latex2.SetTextFont(62)
		latex2.SetTextAlign(11) # align right
		latex2.DrawLatex(0.19, 0.85, "CMS")
		latex2.SetTextFont(52)
		latex2.SetTextAlign(11)
		latex2.DrawLatex(0.28, 0.85, "Preliminary")					
		'''
		latex3.SetTextFont(62)
		latex3.SetTextAlign(11) # align right
		latex3.DrawLatex(0.22, 0.85, "CMS");
		latex3.SetTextSize(0.5*c.GetTopMargin())
		latex3.SetTextFont(52)
		latex3.SetTextAlign(11)
		latex3.DrawLatex(0.20, 0.8, "Preliminary");
		'''
		
		gPad.RedrawAxis()


		plotDir = plotConfig.plotDir

		c.SaveAs(plotDir+"rfactor_"+process+suffix+".pdf")
		c.SaveAs(plotDir+"rfactor_"+process+suffix+".png")
		c.SaveAs(plotDir+"rfactor_"+process+suffix+".C")

		#c.SaveAs("rfactor_"+process+".root")

		'''
		f_out = TFile(process+".root","recreate")
		f_out.cd()
		ratio.Write()
		f_out.Close()
		'''

		del c

for suffix in ['','_loose']:
	plot_ratio('dimuon',suffix)
	plot_ratio('dielectron',suffix)
	plot_ratio('photon',suffix)
	plot_ratio('singlemuonw',suffix)
	plot_ratio('singleelectronw',suffix)
	plot_ratio('singlemuontop',suffix)
	plot_ratio('singleelectrontop',suffix)
	plot_ratio('singlemuonwtop',suffix)
	plot_ratio('singleelectronwtop',suffix)
	plot_ratio('wz',suffix)
