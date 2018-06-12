import sys
import re
import math

#change name of file here to different word embeddings
with open('vectors_ap8889_skipgram_s200_w10_neg20_hs0_sam1e-4_iter5.txt.tar', 'r') as myfile:
    data=myfile.read()

#Split data into list by newlines
data = re.split('\n', data)

#</s> seems to have been considered a word, we will consider this an error
#remove first 10 lines
for i in range(0,10):
    del data[0]
#remove the last line
del data[-1]

#Split data into 2-D array by spaces
#make it a dictionary for ease of use
datadict = {}
for i in range(0,len(data)):
   data[i] = re.split('\s', data[i])
   del data[i][-1]
   datadict[data[i][0]] = data[i]
   del datadict[data[i][0]][0]
   
#convert the rest to numbers
for word in datadict:
    for k in range(0,len(datadict[word])):
        datadict[word][k] = float(datadict[word][k])


            
with open('queries.txt', 'r') as myfile:
    querydata=myfile.read()
#removing extra spaces
querydata = re.sub('\s+(?=\n)', '', querydata)
#split by the tags
querydata = re.split('<num>[0-9]+</num><title>', querydata)

for i in range(0, len(querydata)):
    #remove garbage tags
    querydata[i] = re.sub('<.*?>', '', querydata[i], re.DOTALL)

#Split data into 2-D array by spaces
for i in range(0,len(querydata)):
    querydata[i] = re.split('\s', querydata[i])
    #remove all the empties
    querydata[i] = list(filter(lambda a: a != '', querydata[i]))
del querydata[0]


for i in range(0,len(querydata)):
    querybest = ''
    #we'll only accept query extensions with a similarity above 0
    querysimil = 0
    dataminus = dict(datadict)
    for j in range(0,len(querydata[i])):
        #can set to lowercase here
        querydata[i][j] = querydata[i][j].lower()
        #remove because we don't want to evaluate any terms against terms already
        #in the query
        dataminus.pop(querydata[i][j], None)
    for j in range(0,len(querydata[i])):
        if querydata[i][j] in datadict:
            for word in dataminus:
                topside = 0
                bottomleft = 0
                bottomright = 0
                for k in range(0,len(dataminus[word])):
                    topside += datadict[querydata[i][j]][k] * dataminus[word][k]
                    bottomleft += datadict[querydata[i][j]][k] ** 2
                    bottomright += dataminus[word][k] ** 2
                cosine = topside / math.sqrt(bottomleft*bottomright)
                if (cosine > querysimil):
                    #if cosine similarity is higher, make it the new record
                    querybest = word
                    querysimil = cosine
    print(querybest)
    querydata[i].append(querybest)

print("Creating text file")

#change name of file here to avoid overwriting old files
text_file = open("extendedQueriesSkipgram200.txt", "w")
#Write the new queries to the file
for i in range(0,len(querydata)):
    text_file.write('<top>\n<num>' + str(i + 51) + '</num><title>\n')
    for j in range(0, len(querydata[i])):
        text_file.write(querydata[i][j].upper() + ' ')
    text_file.write('\n</title>\n</top>\n')
text_file.close()

#Indicate that the process is complete
print("Done! :D")
