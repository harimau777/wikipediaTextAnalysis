#! /usr/bin/python

import sys
sys.path.append(".")
import string
from string import translate
import pickle
import re
from parse_wikitext import article_parser

class map_readingLevel():
	def __init__(self):
		#Instantiate the article_parser:
		self.parser = article_parser()

		#Load the syllable dictionary:
		f = open('syl_dict.p', 'rb')
		self.syl_dict = pickle.load(f)
		f.close()

		self.digit_ptrn = re.compile("\d")								#Matches numerical digits.
		#NOTE:	Sentence is defined as one non-whitespace or punctuation character
		#	followed by any number of non-closing punctuation characters or decimal points.
		#		a decimal point is defined as a "." with a digit before and after it.
		#	followed by a punctuation character.
		#	This messes up if the sentence contains abbreviations or other uses of punctuation.
		#NOTE:	See: http://www.rexegg.com/regex-tricks.html#staralt
#		self.sentence_ptrn = re.compile("\w(?:[^.!?])*(?:(?:(?<=\d)\.(?=\d))+(?:[\w\s])*)*[.!?]")	#Matches sentences.
#		self.sentence_ptrn = re.compile("\w(?:[\w\s]|(?<=\d)\.(?=\d))*[.!?]")				#Matches sentences.

	def map_article(self, article):
		#Parse the article:
		self.parser.parse_article(article)

		#Get the parsed data:
		self.text = self.parser.get_text()
		self.articleTitle = self.parser.get_title()

		self.wordList = self.get_words()

		#Calculate the reading level:
		self.reading_level()

	def get_words(self):
		#Get and return the word list:
		#NOTE: Should we remove non-alphanumeric characters?
		try:
			#NOTE: In the future, we might be able to get a speed up by using yield instead of returing the whole dictionary.
			return self.text.strip().lower().translate(None, string.punctuation).split()
		except:
			return []
			self.log_error("get_words failed", {})

	def reading_level(self):
		wordCount = 0
		sylCount = 0
		sentenceCount = 0
		try:
			#Count the words:
			wordCount = len(self.wordList)

			#Count the syllables:
			for word in self.wordList:
				try:
					syl = self.syl_dict[word]
				except KeyError:
					#NOTE:	Currently we are assuming that unfound words are one syllable.
					#	In the future we could try a more sophisticated approach.
					syl = 1
				sylCount += syl

			#Count the sentences:
			#Note: The regex is more accurate than detecting sentences with a for loop; however it is too slow for our cluster.
			for i in range(1, len(self.text)):
				if (self.text[i] == ".") or (self.text[i] == "?") or (self.text[i] == "!"):
					if self.text[i - 1].isalnum():
						sentenceCount += 1
#			sentenceCount = len(self.sentence_ptrn.findall(self.text))
			#NOTE:	Currently we are assuming that if no sentences are found, then the entire article is one sentence.
			#	In the future we could try a more sophisticated approach.
			if sentenceCount == 0:		#If no sentences were found,
				sentenceCount = 1	#Then assume that the entire article is one sentence

			#Calculate the reading level:
			readingLevel = .39 * (wordCount / sentenceCount) + 11.8 * (sylCount / wordCount) - 15.59	#Calculate reading level using Flesch-Kincaid Grade Level.

			#Generate the key-value pair:
			print "%s%s\t%s" % ("RL_", self.articleTitle, readingLevel)
		except:
			errorVarDict = {"wordCount" : wordCount, "sylCount" : sylCount, "sentenceCount" : sentenceCount}
			self.log_error("reading_level failed", errorVarDict)

	def log_error(self, errorType, errorVarDict):
		errorMsg = errorType + ", Article: " + self.articleTitle
		print "%s%s\t%s" % ("ER_", errorMsg, errorVarDict)

#Testing
if __name__ == "__main__":
	mapper = map_readingLevel()
	for line in sys.stdin:	#Get articles from standard input.
		mapper.map_article(line)

