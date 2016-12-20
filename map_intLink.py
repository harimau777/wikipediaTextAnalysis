#! /usr/bin/python

import sys
sys.path.append(".")
from parse_wikitext import article_parser

class map_intLink():
	def __init__(self):
		#Instantiate the article_parser:
		self.parser = article_parser()

	def map_article(self, article):
		#Parse the article:
		self.parser.parse_article(article)

		#Get the parsed data:
		self.text = self.parser.get_text()
		self.articleTitle = self.parser.get_title()

		#Output key-value pairs for internal links:
		self.internal_links()

	def internal_links(self):
		try:
			for link in self.parser.get_internal_links():
				print "%s%s\t%s" % ("IL_", link, 1)
		except:
			self.log_error("internal_links failed", {"intLinkSet" : self.articleTitle})

	def log_error(self, errorType, errorVarDict):
		errorMsg = errorType + ", Article: " + self.articleTitle
		print "%s%s\t%s" % ("ER_", errorMsg, errorVarDict)

#Testing
if __name__ == "__main__":
	mapper = map_intLink()
	for line in sys.stdin:	#Get articles from standard input.
		mapper.map_article(line)

