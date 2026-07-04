import argparse
import os

parser = argparse.ArgumentParser(description='Deleting bonds from a pdb file')
parser.add_argument('-f','--file')
parser.add_argument('-n','--outname', default='chromatin_mod', help='Name of output file')
# parser.add_argument('-splitNum', '--splitNumber', help='the number of times the chromosome will have been split after this', default='1')

try:
    arguments = parser.parse_args()
except IOError as msg:
    parser.error(str(msg))



f = open(arguments.file, "r")
clist=[]


# print(arguments.splitNumber)



for line in f:
	if line[0:6]=='SEQCHR':
		#Travis changed this to move/ instead of current directory #I needed to be consistent with this
		fn=line[11:13]+".ndb"
		# fn="move/"+line[11:13]+".ndb"
		if fn not in clist:
			clist.append(fn)
			if os.path.isfile(fn):
				os.remove(fn)
		of=open(fn,'a')
		of.write(line)
		of.close()
	if line[0:5]=='MODEL':
		for fn in clist:
			of=open(fn,'a')
			of.write(line)
			of.close()
	if line[0:5]=='CHROM':
		fn=line[26:28]+".ndb"
		of=open(fn,'a')
		of.write(line)
		of.close()
	if line[0:3]=='TER':
		fn=line[26:28]+".ndb"
		of=open(fn,'a')
		of.write(line)
		of.close()
	if line[0:6]=='ENDMDL':
		for fn in clist:
			of=open(fn,'a')
			of.write(line)
			of.close()
	if line[0:6]=='MASTER':
		for fn in clist:
			of=open(fn,'a')
			of.write(line)
			of.close()
for fn in clist:
	of=open(fn,'a')
	of.write('END')
	of.close()
