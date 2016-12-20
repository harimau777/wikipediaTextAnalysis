#! /usr/bin/python

import sys
sys.path.append(".")
from parse_wikitext import article_parser

class map_linkCount():
	def __init__(self):
		#Instantiate the article_parser:
		self.parser = article_parser()

	def map_article(self, article):
		#Parse the article:
		self.parser.parse_article(article)

		#Get the parsed data:
		self.text = self.parser.get_text()
		self.articleTitle = self.parser.get_title()

		#Calculate the number of internal links:
		self.count_links()

	def count_links(self):
		try:
			print "%s%s\t%s" % ("LC_", self.articleTitle, self.parser.get_internal_link_count())
		except:
			self.log_error("count_links failed", {"intLinkCount" : self.parser.get_internal_link_count()})

	def log_error(self, errorType, errorVarDict):
		errorMsg = errorType + ", Article: " + self.articleTitle
		print "%s%s\t%s" % ("ER_", errorMsg, errorVarDict)

#Testing
if __name__ == "__main__":
	mapper = map_linkCount()
	for line in sys.stdin:	#Get articles from standard input.
		mapper.map_article(line)

