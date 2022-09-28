import sys
from collections import defaultdict

def Hamming_distance(s1,s2):
	if len(s1)!=len(s2):
		return [-1]
	else:
		p = []
		for i in range(len(s1)):
			if s1[i] != s2[i]:
				p.append(1)
			else:
				p.append(0)
	return p		
	
input_file = sys.argv[1]	
pattern = sys.argv[3]
k = int(sys.argv[2])        
p = len(pattern)

text = ""
with open(input_file) as file_in:		 
	for line in file_in:
		if line[0] != ">":
			text += line.strip() 
			
j = 0
temp =[]
for i in range(0, len(text) - p + 1):
	if len(text[i: i + p]) == p:
		if sum(Hamming_distance(text[i: i + p], pattern)) == k:
			j += 1
			temp.append((text[i: i + p], i))

for key in sorted(temp):
	print (key[0], key[1])

print (j)


	
		
		