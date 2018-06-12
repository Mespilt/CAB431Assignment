import sys
import re
import math

#PLEASE NOTE
#There was an error in the query topics files given
#Number 110 had a "tab" or alternate kind of spacing than whitespace
#This was changed manually in the file


with open('TopicsFull.51-200', 'r') as myfile:
    data=myfile.read()
    
data = re.sub('\n', ' ', data)
data = re.sub(' +', ' ', data)
data = re.sub('<desc>(.*?)<title> Topic: ', '<title>', data)
#Now we remove the last and first
data = re.sub('<top>(.*?)<title> Topic: ', '', data)
data = re.sub('<desc>(.*?)</top>', '', data)

data = re.split('<title>', data)

text_file = open("queries.txt", "w")
for i in range(0,len(data)):
    text_file.write('<top>\n<num>' + str(i + 51) + '</num><title>\n' + data[i].upper() + '\n</title>\n</top>\n')
text_file.close()
print("done")
