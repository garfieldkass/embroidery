#!/usr/bin/python
# explained hex dump of vp3 file, for debugging
# run this from command line
# output file = stdout

import sys
import os.path
import vp3io

fname=sys.argv[1]
#print "input file name is '"+fname+"'"
if fname=="":
	sys.exit("ERR: file name not given")

if os.path.isfile(fname):
	vp3io.explain (fname)
else: 
	sys.exit("file '"+fname+"' does not exist")
# oname=fname+"hex"
#print "output file: '",oname,"'" # output file=fname+"hex"   ("working.vp3hex")
