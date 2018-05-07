from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk import WordNetLemmatizer
from nltk import PorterStemmer
from nltk import NaiveBayesClassifier
import nltk
import string
from nltk.probability import FreqDist

import pickle
import json

lyricsData = []
listKata = []
listGenre=[]

trainDataGenre = []

dictionary = {}

for line in open("lyrics.json"):
	lyricsData.append((json.loads(line)["genre"],json.loads(line)["lyrics"]))

for genre,lyrics in lyricsData:
	tempDictionaryPositive = {}
	tempDictionaryNegative = {}

	if genre not in listGenre:
		listGenre.append(genre)

	for word in word_tokenize(lyrics):
		word = word.lower()
		if(word not in stopwords.words("english")):
			tempDictionaryPositive[word]=True
			tempDictionaryNegative[word]=False

	for gen in listGenre:
		if(gen==genre):
			trainDataGenre.append((tempDictionaryPositive,gen))
		else:
			trainDataGenre.append((tempDictionaryNegative,gen))


genreClassifier = NaiveBayesClassifier.train(trainDataGenre)


index = 0

while(index != 5):
	index = 0
	for i in range (0,25):
		print("")

	print 'GENRE DETERMINER',nltk.classify.accuracy(genreClassifier,trainDataGenre)
	print("================")
	print("1. Classify a phrase")
	print("2. Frequency")
	print("3. Save data")
	print("4. Load data")
	print("5. Exit")

	while(index<1 or index > 5):
		try:
			index = int(input("Choice >> "))
		except:
			index = 6

	if(index==1):

		text=""
		text = input("insert phrase >> ")
		textDict = {}
		
		for word in word_tokenize(text):
			word = word.lower()
			if(word not in stopwords.words("english")):
				textDict[word]=True

		for i in range (0,25):
			print("")
		print("Phrase = ",text)
		print("Genre  = ",genreClassifier.classify(textDict))

		input("press enter to go back")

	elif(index==2):
		for i in range (0,25):
			print("")

		i=0

		for genre in listGenre:
			i+=1
			print(i,". ",genre)

		choice = len(listGenre)+1

		while(choice<1 or choice>len(listGenre)):
			try:
				choice = int(input("choice >> "))
			except:
				choice = len(listGenre)



		listKata = []

		for genre,kata in lyricsData:
			if(genre == listGenre[choice-1]):
				for word in word_tokenize(kata):
					valid = True
					for w in word:
						if(w in string.punctuation):
							valid = False

					word = word.lower()

					if(word not in stopwords.words("english") and valid):
						WordNetLemmatizer().lemmatize(PorterStemmer().stem(word),pos='a')
						listKata.append(word)

		hasilFreqDist = FreqDist(listKata)

		print("20 most common words")
		print("===================")

		for kata,freq in hasilFreqDist.most_common(20):
			print(kata," -> ",freq)

		input("press enter to go back")

	elif(index == 3):
		saveFile = open('genre.pickle',"wb")
		pickle.dump(genreClassifier,saveFile)
		saveFile.close()
		print("dump succeed")

		input("press enter to go back")

	elif(index == 4):
		loadClassify = open('genre.pickle','rb')
		genreClassifier = pickle.load(loadClassify)
		loadClassify.close()
		print("load succeed")

		input("press en000ter to go back")

	elif(index == 5):
		for i in range (0,25):
			print("")

		print("NTAB")
		



raw_input()
