import tweetTokenizer as t, pickle as p
import codecs, re, operator, sys
from matplotlib import pyplot as ppl
from collections import OrderedDict

def formatTheSentences():
	fileIn = codecs.open('The Adventures of Sherlock Holmes.txt')
	fileOut = codecs.open('The Adventures of Sherlock Holmes.formated', "w+")
	fileInContent = ""
	for line in fileIn:
		if len(line.strip()) !=0:
			fileInContent += line
	fileInContent = "<s>" + fileInContent
		


def doTokenization():
	o = t.Tokenizer( ignoreList= [ 'email', 'url', 'ellipses', 'punct', 'unicodeEmoji' ] )
	fileIn = codecs.open('twitter.dump', encoding='utf-8')
	fileOut = open('twitter.tokens', "w+")
	tokensList = []
	lines = ""
	for line in fileIn:
		o.tokenize(line.strip())
		temp = o.getTokens();
		o.clearTokens();
		if len(temp) != 0:
			tokens = [ "<s>" ]
			tokens.extend( temp )
			tokens.extend( ["</s>"] )
			tokensList.append( tokens )
	for line in tokensList:
		fileOut.write( str(line) )
		fileOut.write( "\n" )
	fileOut.close()
	return tokensList


def generateNGrams( tokensList, n ):
	ngrams = {}
	for line in tokensList:
		if len(line) < n:
			break;
		for i in xrange( n, len(line)+1 ):
			key = tuple( line[i-n:i] )
			ngrams[ key ]  = (ngrams[key]+1) if key in ngrams else 1

	sortedByValues = OrderedDict(sorted(ngrams.items(), key=lambda x: x[1], reverse=True))

	if len(sortedByValues) != 0:
		fileOut = open('twitter.ngrams', "w+")
		for k,v in sortedByValues.items():
			fileOut.write( str(k) )
			fileOut.write( " : " )
			fileOut.write( str(v) )
			fileOut.write( "\n")

	return sortedByValues

def getProbabiliy( ngrams, word ):
	countNum, countDen = 0.0,0.0;
	for ngram in ngrams:
		countNum += ( 1 if ngram[-2]==word and ngram[-1]=="</s>" else 0 )
		countDen += ( 1 if word in ngram else 0 )
	return (countNum/countDen) if countDen!=0 else 0


def getUnigramProbabilities( uniGrams ):
	probability = []
	countDen = len(uniGrams)*1.0
	for key in uniGrams.keys():
		probability.append( (key, uniGrams[key]/countDen) )

	return probability;


if __name__ == "__main__":
	i = 1
	
	print "{0}. Tokenizing".format(i);	i+=1
	tokensList = doTokenization();

	print "{0}. Generating \'{1}-grams\'".format(i,1);	i+=1
	uniGrams = generateNGrams( tokensList, n=1 )

	print "{0}. Persisting \'{1}-grams\'".format(i,1);	i+=1
	p.dump( uniGrams, open( "1gram", "wb+") )

	probability = getUnigramProbabilities( uniGrams )

	vals = [ x[1] for x in probability ]
	ppl.plot( range(len(probability)), vals )
	ppl.show()