#!/usr/bin/env python

'''

Add statistical shape errors (aka Barlow Beeston) to a shape .root file

Author: Evan K. Friis, UW Madison

'''

from RecoLuminosity.LumiDB import argparse
import fnmatch
import logging
import os
import ROOT
import shutil
import sys

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch()  

log = logging.getLogger('stat_shapes')

def walk_and_copy(inputdir, outputdir, datacard, pattern, mergers, threshold, prefix, normalize, writeDC):
    ''' Recursive function which copies from inputdir to outputdir '''
    for line in datacard:
        if fnmatch.fnmatch(line, "process*"):
            columns = line.strip().split()
            break

    keys = []
    for key in inputdir.GetListOfKeys():
        # Prevent double counting of histograms
        if key.GetName() in keys :
            continue
        elif isinstance(inputdir.Get(key.GetName()), ROOT.TH1) :
            keys.append(key.GetName())
        # Keep track of stuff we find in this directory
        print "Name: " + key.GetName()
        directories = []
        histos = []
        name = key.GetName()
        classname = key.GetClassName()
        print "Classname: " + classname
        if classname.startswith('TDirectory'):
            if not name in directories :
                directories.append(name)
        elif isinstance(inputdir.Get(name), ROOT.TH1):
            if not name in histos :
                histos.append(name)
        '''
        else:
            outputdir.cd()
            obj = key.ReadObj()
            obj.Write()
        ''' 
        # Copy all histograms from input -> output directory
        for histo in histos:
            th1 = inputdir.Get(histo)
            th1.SetName(histo)
            #outputdir.cd()
            th1.Write()
            # Check if this histogram has shape uncertainties
            do_shapes = False
            path = inputdir.GetPath().split(':')[1]
            full_path = os.path.join(path, histo)
            # A version without a leading slash
            rel_path = full_path if full_path[0] != '/' else full_path[1:]
            #print "rel path: ", rel_path
            log.debug("Testing path %s against pattern %s", full_path, pattern)
            if fnmatch.fnmatch(histo, pattern) or \
               fnmatch.fnmatch(full_path, pattern) or \
               fnmatch.fnmatch(rel_path, pattern) :
                log.debug("Matches!")
                do_shapes = True
                if fnmatch.fnmatch(histo, "*Up*") or \
                   fnmatch.fnmatch(histo, "*Down*") :
                    do_shapes = False
            if fnmatch.fnmatch(full_path, "*data*") :
                log.debug("... but it is data!")
                do_shapes = False
            if do_shapes:
                # check all bins to see if they need to be shape-errored
                log.info("Building stat shapes for %s", histo)
                # Check if we want to add any extra mergers
                error_clone = th1.Clone()
                # Check if we want to add the error from more histograms
                if mergers:
                    for merger in mergers:
                        log.info("Merging errors from %s into %s", merger, histo)
                        to_merge = inputdir.Get(merger)
                        error_clone.Add(to_merge)

                for ibin in range(1, th1.GetNbinsX()+1):
                    error = error_clone.GetBinError(ibin)
                    val = th1.GetBinContent(ibin)
                    # Check if we are above threshold
                    above_threshold = False
                    if val:
                        if error/val > threshold:
                            above_threshold = True
                    else:
                        # If there is nothing in the bin, but there is
                        # an error, we respect this.
                        if error:
                            log.info("%s_%s_bin_%i is zero, but will have a non-zero error.",
                                     prefix, histo, ibin)
                            above_threshold = True

                    if above_threshold:
                        myString = th1.GetName().replace("_nominal",'')
                        process = myString[myString.rfind("_")+1:]
                        process = process.replace("_",'')
                        channel = myString[:myString.find("_")]
                        # shorten channel name
                        channel = channel.replace("tH_",'').replace("tt_",'')
                        writtensys=("%s_%s_bin%i" % (channel[0:3], process, ibin))
                        err_up = th1.Clone(
                            th1.GetName().replace("_nominal",'') + "_%sUp" % (writtensys))
                        err_down = th1.Clone(
                            th1.GetName().replace("_nominal",'') + "_%sDown" % (writtensys))
                        # Print to stdout, so we can capture the uncertainties
                        print "%s" % (writtensys)
                        err_up.SetBinContent(ibin, val + error)
                        ## if not val > error bin the down entry to a small value >0 to prevent problems in combine 
                        err_down.SetBinContent(ibin, val - error if val > error else 0.01)
                        if normalize:
                            err_up.Scale(th1.Integral()/err_up.Integral())
                            err_down.Scale(th1.Integral()/err_down.Integral())
                        if val < error:
                            log.warning("%sDown, is negative, pegged to zero", writtensys)
                        #outputdir.cd()
                        print "Outputdir: " + str(outputdir)
                        err_up.Write()
                        err_down.Write()
                        # Write new entry for systematic in datacard
                        if writeDC:
                            forwhichprocess=""
                            for iprocess in columns[1:]:
                                iprocess=iprocess.replace("_",'')
                                if fnmatch.fnmatch(iprocess,process):
                                    forwhichprocess+=('%-12s' % ('1.00'))
                                else:
                                    forwhichprocess+=('%-12s' % ('-'))
                            datacard.write('%-23s%-10s%s\n' % (writtensys, 'shape', forwhichprocess))
                            
                        log.info("==> built shape for %s bin %i", histo, ibin)


#        if classname.startswith('Roo'):
 #           if not name in directories :
  #              directories.append(name)

        # Now copy and recurse into subdirectories
        for subdir in directories:
            output_subdir = outputdir.mkdir(subdir)
            # Recurse
            walk_and_copy(
                inputdir.Get(subdir), output_subdir, datacard,
                pattern, mergers, threshold, prefix, normalize, writeDC)




def main(inputfilename, outputfilename, matcher, mergers, threshold, prefix, normalize, writeDC):
    input = ROOT.TFile(inputfilename, 'READ')
    if not input:
        raise IOError("Can't open input file: %s" % inputfilename)
    output = ROOT.TFile(outputfilename, 'RECREATE')
    if not output:
        raise IOError("Can't open output file: %s" % outputfilename)
    datacard = open(inputfilename.replace('.root','.txt'), 'a+')
    if not datacard:
        raise IOError("Can't open output file: %s" % inputfilename.replace(".root",".txt"))
    copy_all = True
    walk_and_copy(input, output, datacard, matcher, mergers, threshold, prefix, normalize, writeDC)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input .root file')

    parser.add_argument('output', help='Output .root file')
    parser.add_argument('--prefix', default='',
                        help='Prefix for the systematic name,'
                        'fixme should be something like mutau, etau, etc')
    parser.add_argument('--filter', metavar='pattern',
                        help='Pattern of TH1F names to shape-ize')
    parser.add_argument('--merge-errors', nargs='+', dest='merge',
                        help='Merge in errors from different shapes. '
                        'Should be only the histogram name, which are '
                        'taken from the same directory as the filtered histo.')
    parser.add_argument('--threshold', type=float, default=0.01,
                        help='Minimum error for systematic creation,'
                        'default %(default)0.2f')
    parser.add_argument('--normalize', action='store_true', default=False,
                        help='Normalize shifted templates to the original yield')
    parser.add_argument('--writeDC', action='store_true', default=False,
                        help='Append existing datacard')
    parser.add_argument('--verbose', action='store_true',
                        help='Print debug output.')


    args = parser.parse_args()

    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO if not args.verbose else logging.DEBUG)

    in_place = True
    if args.input == args.output:
        log.info("Modifying in place!  Backing up input file...")
        shutil.copy(args.input, args.input.replace('.root', '.root.bak'))
        args.output = args.output.replace('.root', '.tmp.root')

    log.info("Building shape systematics. input: %s output: %s",
             args.input, args.output)
    main(args.input, args.output, args.filter, args.merge,
         args.threshold, args.prefix, args.normalize, args.writeDC)
    log.info("Moving temprorary output to final destination")
    shutil.move(args.output, args.output.replace('.tmp.root', '.root'))
