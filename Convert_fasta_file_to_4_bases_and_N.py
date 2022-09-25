import sys
import fileinput
 
fasta_file = sys.argv[1]

out = ""

for line in fileinput.input(fasta_file):
    if line[0] == ">":
        pass
    else:
        for c in line:
            if c in ["A", "C", "G", "T", "N"]:
                out += c
				
print (out)
