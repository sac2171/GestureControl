import string
from operator import itemgetter


#filepath = raw_input("Enter a filepath:")
filepath = 'trainingTweets.txt' 
fileHandle = open(filepath, 'r')

dictionary = {}
for line in fileHandle:
    elements = string.split(line, '\t')    
    words = string.split(elements[1])
    for w in words:
        if w not in dictionary:
            dictionary[w] = 1
        else:
            dictionary[w] = dictionary[w] + 1  
fileHandle.close()   

output = str(sorted(dictionary.items(), key=itemgetter(1), reverse=True))
newoutput = string.replace(output, '), ', '\n')
newoutput = string.replace(newoutput, '\'','')
newoutput = string.replace(newoutput, '(', '')
newoutput = string.replace(newoutput, ')', '')
newoutput = string.replace(newoutput, '[', '')
newoutput = string.replace(newoutput, ']', '')


#for line in newoutput:
#    line = line.lstrip()

fp2 = 'vocab.txt'
fh2 = open(fp2,'w')
fh2.write(newoutput)

#print sorted(dictionary.items(), key=itemgetter(1), reverse=True)
