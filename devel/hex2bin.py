#!/usr/bin/python
# file converter: commented hex dump to binary
# created as reverse of hexdumpvp3.py
# eliminates comments, any non-hexanumeric-containig word starts comment until eol
# run this from command line

import sys
def is_hex(s): # is string hexanumeric?
	try:
		int(s,16)
		return True
	except ValueError:
		return False
def hexstr2bin(s):  # convert one line
	global lines,bytes
	res=""
	lines+=1
	for t in s.split():
		if is_hex(t): # or else starts comment
			if len(t) < 3: # consider longer hexwords be line numbers and ignore them
				res+=chr(int(t,16)) # hex byte to bin byte
				bytes+=1
		else: return res
	return res
bytes=0
lines=0
fname=sys.argv[1]
if fname=="": sys.exit("give a hexadecimal coded file name")
oname=fname+"bin"
o_str=""
for line in open(fname,"rt"): o_str+=hexstr2bin(line)
open(oname,"wb").write(o_str) # not guaranteed
print "input file name is '"+fname+"'  ",lines," lines"
print "output file: '"+oname+"'  ",bytes," bytes"
