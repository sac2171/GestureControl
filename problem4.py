import string

def extractFeatures(text, dictionary):
    words = string.split(text, ' ')
    f_list = ''
    for word in words:
        newword = word+','
        if newword in dictionary:
            f_list= f_list+'' + str(dictionary[newword]) +":1" + ''
    return f_list

#tfilePath=raw_input('Path to training tweets')
tfilePath = 'trainingTweets.txt'
#vfilePath=raw_input('Path of vocab txt')
vfilePath = 'vocab.txt'
#vfilePath=raw_input('Path of vocab txt')
outfilePath = 'out.txt'
#fileHandle = open(filepath, 'r')

V = open(vfilePath, 'r')

counter = 1
d = {}
for line in V:
    elements = string.split(line)
    d[elements[0]]= counter
    counter = counter+1
V.close()


T = open(tfilePath, 'r')

F = open(outfilePath, 'w')

for line in T:
    elements = string.split(line, '\t')
    label = elements[0]
    #print elements[1]
    f_list = extractFeatures(elements[1], d)
    F.write(label+ ' ' + f_list +'\n')
    
T.close()
F.close()

