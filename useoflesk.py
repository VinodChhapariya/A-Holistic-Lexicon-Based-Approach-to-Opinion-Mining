import glob
import sys
reload(sys)
import nltk
from nltk.wsd import lesk
from nltk.corpus import stopwords
from nltk.wsd import lesk
#from textblob import TextBlob
#from nltk.wsd import lesk
from nltk.corpus import wordnet as wn
#nltk.download("stopwords")
sys.setdefaultencoding("utf-8")



list_of_files = glob.glob('./*.txt')
mylist = []
mylist1 = [] 

for file_name in list_of_files:
  FI = open(file_name, 'r')

  nf = FI.read()
  sentences = nltk.sent_tokenize(nf)
  mylist.append(sentences)
   
nouns = [] #empty to array to hold all nouns
print"=================****NOUN****================"
for sentence in mylist:
   for word,pos in nltk.pos_tag(nltk.word_tokenize(str(sentence))):
   	    if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
   	    	fi = lesk(sentence, word)
   	    	#print fi
   	    	for ss in wn.synsets(word):
   	    		#print(ss, ss.definition())
   	    		file = open("noun.txt",'a')
   	    		tg1 = str(ss)
   	    		tg2 = str(ss.definition())
   	    		file.write(''+str(word)+'-->'+str(fi)+"::"+tg1+":"+tg2+"\n")
   	     
#print"==================***VERB***===================="          
for sentence in sentences:
   for word,pos in nltk.pos_tag(nltk.word_tokenize(str(sentence))):
      if (pos == 'VB' or pos == 'VBD' or pos == 'VBG' or pos == 'VBN'):
          #print word  
          fi=lesk(sentence, word)
          #print fi
          for ss in wn.synsets(word):
          	file = open("verb.txt",'a')
   	    	tg1 = str(ss)
   	    	tg2 = str(ss.definition())
   	    	file.write(''+str(word)+'-->'+str(fi)+"::"+tg1+":"+tg2+"\n")
            #print(ss, ss.definition())

         #  print(fi=lesk(sentence, word))
        
           
       #    file = open("verb.txt",'a')
        #   tg = str(file)
         #  file.write(str(fi)
#print "===================***ADVERB**=================="
#for sentence in sentences:
 #  for word,pos in nltk.pos_tag(nltk.word_tokenize(str(sentence))):
  #    if (pos == 'VB' or pos == 'VBD' or pos == 'VBG' or pos == 'VBN'):
   #        print "=====>",word
    #       fi = lesk(sentence, word)
     #      file = open("adverb.txt",'a')
      #     tg = str(file)
       #    file.write(str(fi))

