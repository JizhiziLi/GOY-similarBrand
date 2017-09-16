###########
# Created by Jizhizi Li @ 17/09/2017
# A simple NLP algorithm to find similar brand based on 
# keywords crawling from brand website.
# word2vec of nltk is been used as similarity calculation
# algorithm between words.
#
# Input: A string crawling from raw HTML of brand website
# Output: The domain category for one specific brand.
###########

import numpy as np
import gensim
import nltk
import operator
from nltk.data import find
# download word2vec_sample as lexicon used in this case
nltk.download('word2vec_sample')
word2vec_sample = str(find('models/word2vec_sample/pruned.word2vec.txt'))
model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_sample, binary=False)
# do stemming on words for normalisation
stemmer = nltk.stem.PorterStemmer()

# previous and after-mapping categorySet, mapping is based on lexicon
# categorySet = set(['sport shoes','handbag','denim','shoes','jackets','shirts','swimwear','underwear','activewear','tshirts','lingerie','shorts','wallets','pants','jewellery','tops','skirts','eyewear','sleepwear','bags','hats','workwear','watches','socks','booties','sandals','suits','backpack','sneakers','plus','sportswear','surfwear','heels','outerwear','thongs','dress shoes','jumpers','eveningwear','tights','knitwear','casualwear','flats','belts','uggs','luggage','hosiery','polos','hoodies','ties','sweatshirts','scarves','casual shoes','wedges','sports coats','slippers'])
categorySet = set(['runners','handbag','jeans','shoes','jackets','shirts','swimsuit','underwear','gym','tshirts','lingerie','shorts','wallets','pants','accessories','tops','skirts','glasses','sleep','bags','hats','suits','watches','socks','boot','sandals','suits','backpack','sneakers','plus','sportswear','surfwear','heels','jacket','thongs','heels','jumpers','dresses','tights','sweater','casualwear','flats','belts','uggs','luggage','hosiery','polos','ties','sweatshirts','scarf','casual shoes','wedges','coats','slippers'])
# define a final dictionary
finalDic={}


### generateSoringDic
### Input: a single word and a set of words to compare
### Output: a list sorted by similarity value 
def generateSortingDic(word,wordset):
    count=0
    returnDic = {}
    onelist = []
    for item in wordset:
        try:
            returnDic[item]=model.similarity(word,item)
        except:
            try:
                returnDic[item]=model.similarity(word,stemmer.stem(item))
            except:
                count=count+1
    sorted_x = sorted(returnDic.items(), key=lambda x: x[1],reverse=True)
    if(sorted_x==[]):
        finalDic[word+'-null'] = 0
        return 0
    finalDic[word+'-'+sorted_x[0][0]] = sorted_x[0][1]
    return sorted_x


### stemWordIfNotExist
### Input: a single word
### Output: a stemming word if its not existed in lexicon
def stemWordIfNotExist(word):
    try:
        model[word]
        return word
    except:
        return stemmer.stem(word)



### processString
### Input: a raw string
### Output: process input string as a set of words
def processString(string):
    string = string.lower()
    newstring = string.replace(",","")
    newlist = newstring.split(" ")
    newset = set()
    for word in newlist:
        word = stemWordIfNotExist(word)
        newset.add(word)
    return newset


### generateResults
### Input: a raw string, a catogery set to compare
### Output: the domain category, one word we want
def generateResults(string,wordset):
    mostrelevant = 0
    keywordset = processString(string)
    for item in keywordset:
#         print(generateSortingDic(item,wordset))
        generateSortingDic(item,wordset)
    sorted_sorted = sorted(finalDic.items(), key=lambda x: x[1],reverse=True)
    print(sorted_sorted)
    index = sorted_sorted[0][0].find('-')
    return sorted_sorted[0][0][index+1:len(sorted_sorted[0][0])]
    



### Test for brand AG Jeans

string = 'ag jeans, brand, adriano goldschmied, online store AG Jeans, official, premium denim, denim jeans, designer clothing AGJeans'
print(generateResults(string,categorySet))
