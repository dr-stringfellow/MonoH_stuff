import ROOT as r

_fin = r.TFile.Open("mono-x.root")

zll   = _fin.Get("category_monojet/Zmm_zll")
zll_d = _fin.Get("category_monojet/Zmm_data")
zvv   = _fin.Get("category_monojet/signal_zjets")

for b in range(zll.GetNbinsX()):
    print "mc  ", b+1, "zll", zll.GetBinContent(b+1),"zvv", zvv.GetBinContent(b+1), "ratio ", zvv.GetBinContent(b+1) / zll.GetBinContent(b+1)
    print "data", b+1, "zll", zll_d.GetBinContent(b+1)
