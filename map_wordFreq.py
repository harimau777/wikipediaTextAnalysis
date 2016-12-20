#! /usr/bin/python

import sys
sys.path.append(".")
import string
from string import translate
import re
from parse_wikitext import article_parser

class map_wordFreq():
	def __init__(self):
		#Instantiate the article_parser:
		self.parser = article_parser()

		self.digit_ptrn = re.compile("\d")	#Matches numerical digits.

	def map_article(self, article):
		#Parse the article:
		self.parser.parse_article(article)

		#Get the parsed data:
		self.text = self.parser.get_text()
		self.articleTitle = self.parser.get_title()

		self.wordList = self.get_words()

		#Calculate the word frequency:
		self.word_frequency()

	def get_words(self):
		#Get and return the word list:
		#NOTE: Should we remove non-alphanumeric characters?
		try:
			#NOTE: In the future, we might be able to get a speed up by using yield instead of returing the whole dictionary.
			return self.text.strip().lower().translate(None, string.punctuation).split()
		except:
			return []
			self.log_error("get_words failed", {})

	def word_frequency(self):
		try:
			#Calculate the word frequency:
			wordDict = dict()			#Dictionary: Keys are words in the article, values are the number of times the word occured.
			for word in self.wordList:
				#NOTE:	If the word is longer than 30 characters or contains a numeric digit, then we assume it is the result of a parser
				#	error and skip it.
				#	This is partially done in order to improve performance on our cluster.
				if (len(word) > 30) or self.digit_ptrn.search(word):
					continue
				try:
					wordDict[word] += 1
				except KeyError:
					wordDict[word] = 1	#If the word is not in the dictionary, then add it.

			#Generate key-value pairs:
			for word in wordDict:
				print "%s%s\t%s" % ("WF_", word, wordDict[word])
		except:
			self.log_error("word_frequency failed", {"wordDict" : wordDict})

	def log_error(self, errorType, errorVarDict):
		errorMsg = errorType + ", Article: " + self.articleTitle
		print "%s%s\t%s" % ("ER_", errorMsg, errorVarDict)

#Testing
if __name__ == "__main__":
	mapper = map_wordFreq()
	for line in sys.stdin:	#Get articles from standard input.
		mapper.map_article(line)

