

import argparse

parser = argparse.ArgumentParser(description='Deleting bonds from a pdb file')
parser.add_argument('-f','--file')
parser.add_argument('-n','--outname', default='chromatin_mod', help='Name of output file')
parser.add_argument('-l', '--list', help='comma delimited list input of break points', type=str)

try:
    arguments = parser.parse_args()
except IOError as msg:
    parser.error(str(msg))

print("starting read of",arguments.file)

breaks = [int(item) for item in arguments.list.split(',')]

f = open(arguments.file, "r")
of= open(arguments.outname, "w")

chain=1
monomer=1
currbreak=breaks[0]
linecount=0;

for line in f:
	linecount+=1
	if(line[0:5]=='MODEL'):
		chain=1
		monomer=0
		currbreak=breaks[chain-1]
		linecount=0
	if(line[0:4]=='ATOM'):
		monomer+=1;
		id=str(monomer)
		while len(id)<4:
			id=' '+id
		lid=str(linecount)
		while len(lid)<4:
			lid=' '+lid		
		cid=chr(ord('@')+chain)

		newline=line[0:7]+lid+line[12:]
		line=newline
		newline=line[0:21]+cid+line[22:]
		line=newline
		newline=line[0:22]+id+line[26:]
		line=newline

	if line[0:3]!='TER':
		of.write(line)
	else:
		lid=str(linecount)
		while len(lid)<4:
			lid=' '+lid		
		id=str(monomer+1)
		while len(id)<4:
			id=' '+id
		of.write('TER    '+lid+'     '+line[16:20]+' '+cid+id+'\n')
		
	if (monomer==currbreak):
		lid=str(linecount+1)
		while len(lid)<4:
			lid=' '+lid		
		id=str(monomer+1)
		while len(id)<4:
			id=' '+id
		of.write('TER    '+lid+'     '+line[16:20]+' '+cid+id+'\n')
		monomer=0
		chain+=1;
		linecount+=1
		if chain<=len(breaks):
			currbreak=breaks[chain-1]
		else:
			currbreak=100000
