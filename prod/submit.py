#!/usr/bin/env python

from os import system,environ,getuid
from sys import exit,stdout,argv
from time import sleep


user = environ['USER']
uid = getuid()
cfgName=argv[1]
nPerJob = 4
xrd='root://xrootd.cmsaf.mit.edu/'

histdir = '/mnt/hadoop/scratch/%s/private_pandatree/files/%s/'%(user,cfgName)
cfgdir = '/mnt/hadoop/scratch/%s/private_pandatree/condor/%s/'%(user,cfgName)
logdir = '/mnt/hadoop/scratch/%s/private_pandatree/logs/%s/'%(user,cfgName)
#histdir = '/home/%s/cms/private_pandatree/files/%s/'%(user,cfgName)
#cfgdir  = '/home/%s/cms/private_pandatree/condor/%s/'%(user,cfgName)
#logdir  = '/home/%s/cms/private_pandatree/logs/%s/'%(user,cfgName)
for dire in [histdir,cfgdir,logdir]:
  system('rm -rf '+dire)
  system('mkdir -p '+dire)

def submit(l):
  print "submitting",l,cfgName
  condorJDLString = '''
Executable                 = run.sh
Universe                   = vanilla
requirements = UidDomain == \\\"mit.edu\\\" && Arch == \\\"X86_64\\\" && OpSysAndVer == \\\"SL6\\\" && Machine != \\\"t3home000.mit.edu\\\"
Error                      = %s/\$(Process).err
Output                     = %s/\$(Process).out
Log                        = %s/\$(Process).log
Arguments                  = \$(Process) %s/\$(Process).cfg %s
should_transfer_files      = YES
when_to_transfer_output    = ON_EXIT
GetEnv                     = True
accounting_group           = group_cmsuser.%s
use_x509userproxy          = True
x509userproxy              = /tmp/x509up_u%s
Queue %i'''%(logdir,logdir,logdir,cfgdir,histdir,user,uid,l)
  system('echo "%s" | condor_submit'%condorJDLString)


with open("cfg/%s.txt"%(cfgName)) as cfgFile:
  filesToProcess = list(cfgFile)


nJobs = len(filesToProcess)/nPerJob+1
for iJ in xrange(nJobs):
  filesThisJob = filesToProcess[nPerJob*iJ:nPerJob*(iJ+1)]
  with open(cfgdir+'%i.cfg'%(iJ),'w') as thisCfg:
    for f in filesThisJob:
      thisCfg.write(xrd+f)


submit(nJobs)
#submit(10)
