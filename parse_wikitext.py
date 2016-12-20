#! /usr/bin/python

import re			#Used for regular expressions.
import unicodedata		#Used for converting Unicode to ASCII.
from bs4 import BeautifulSoup	#Used for parsing HTML style tags.

class article_parser():
	#***** Init Method *****
	def __init__(self):
		#Category Patterns:
		self.catSect_ptrn = re.compile("\[\[Category.*$")				#Regex: Matches an article's category section.
		self.cat_ptrn = re.compile("(?<=\[\[Category:).*?(?=\]\])")			#Regex: Matches a category inside an article's category section.

		#Title Pattern:
		self.title_ptrn = re.compile("^.*?(?=:{6})")

		#Section Pattern:
		self.section_ptrn = re.compile("={2,6}.*?={2,6}")				#Regex: Matches section tags.

		#Reference Pattern:
		self.ref_ptrn = re.compile("<ref(?:(?!<ref).)*?(?:(?:</ref>)|(?:/>))")		#Regex: Matches references.

		#External link pattern:
		#NOTE: Figure out how to modify this to explicitly not match double brackets [[...]]
		self.extLink_ptrn = re.compile("(?<=\[)(?:http|https)://.*?(?=\])")

		#Internal Link Pattern:
		#NOTE: This will not match links beginning with "File:", "media:", "Special:", or "Image:"
		#NOTE: The [[Image: ...]] format is not listed in the documentation but appears to be used.
		self.intLink_ptrn = re.compile("(?<=\[\[)(?:(?!File:)(?!media:)(?!Special:)(?!Image:).)*?(?=\]\])")	#Regex: matches internal links.

		#Misc Link Pattern:
		#NOTE: The following will remove both an image AND its caption.
		self.miscLink_ptrn = re.compile("\[\[(?:File|media|Special|Image):.*?\]\]")	#Regex: Matches images, media, and "special" links.

		#Template Pattern:
		self.template_ptrn = re.compile("(?<=\{\{).*?(?=\}\})")				#Regex: Matches templates (format {{text}}).

	#***** Parsing Methods *****
	def parse_article(self, article):
		self.text = article
		self.parse_categories()
		self.parse_title()
		self.parse_tags()
		self.parse_sections()
#		self.parse_unicode()
#		self.parse_references()
		self.parse_templates()
		self.parse_external_links()
		self.parse_internal_links()
		self.parse_misc_links()

	#********************************************
	# parse_categories()
	#********************************************
	# Removes the categories section from the
	# end of the text.
	#********************************************
	def parse_categories(self):
		try:
			#NOTE:	Is it safe to assume that categories are always present and are always at the end of the file?
			catSect = self.catSect_ptrn.search(self.text)			#Find the category section of the article.
			self.text = self.text[0:catSect.start()]			#Remove the category section from the text.
		except:
			pass

	#********************************************
	# parse_title()
	#********************************************
	# Removes the title from the text.
	#********************************************
	def parse_title(self):
		self.title = ""
		try:
			self.title = self.title_ptrn.match(self.text).group(0).strip()	#Find the title.  Strip off the leading space.
			self.text = self.text.replace(" " + self.title + " ::::::", "")	#Remove the title from the text.
		except:
			pass

	#********************************************
	# parse_tags()
	#********************************************
	# Removes tags from the text using Beatiful-
	# Soup, a library designed to parse HTML.
	#********************************************
	def parse_tags(self):
		try:
			soup = BeautifulSoup(self.text)
			new_text = soup.get_text()
			new_text = unicodedata.normalize('NFKD', new_text).encode('ascii','ignore')
			self.text = new_text
		except:
			pass

	#********************************************
	# parse_sections()
	#********************************************
	# Removes section tags from the text.
	#********************************************
	def parse_sections(self):
		try:
			for tag in self.section_ptrn.findall(self.text):		#Loop through each section tag in the article.
				self.text = self.text.replace(tag, "")			#Remove the section tag from the text.
		except:
			pass

	#********************************************
	# parse_unicode()
	#********************************************
	# Normalizes the text from Unicode to ASCII.
	#********************************************
	def parse_unicode(self):
		#NOTE: Verify that this is the correct/best way to do this.
		#This first normalizes the unicode text.
		#	KD replaces compatability characters with their equivalents.
		#	KC appears to also apply a "cannonical decomposition".
		#The text is then encoded as ASCII.  Characters that cannot be converted are ommited.
		#NOTE:	It would also be possible to replace a character with '\ufffd', to raise an exception, or to use XML's character
		#	references.
		try:
			self.text = unicodedata.normalize('NFKD', self.text).encode('ascii','ignore')
		except:
			pass

	#********************************************
	# parse_references()
	#********************************************
	# Removes references from the text.
	#********************************************
	def parse_references(self):
		self.refList = list()
		try:
			for ref in self.ref_ptrn.findall(self.text):
				self.text = self.text.replace(ref, "")			#Remove the references from the text.
		except:
			pass

	#********************************************
	# parse_templates()
	#********************************************
	# Removes templates from the text.
	#********************************************
	def parse_templates(self):
		try:
			for template in self.template_ptrn.findall(self.text):		#Find and iterate through all templates in the text.
				self.text = self.text.replace(template, "")		#Remove the templates from the text.
		except:
			pass

	#********************************************
	# parse_external_links()
	#********************************************
	# Removes external links from the text.
	#********************************************
	def parse_external_links(self):
		self.extLinkSet = set()
		try:
			for link in set(self.extLink_ptrn.findall(self.text)):
				self.text = self.text.replace("[" + link + "]", "")	#Remove the external links from the text.
		except:
			pass

	#********************************************
	# parse_internal_links()
	#********************************************
	# Removes the double brackets surrounding
	# internal links in the text.
	#********************************************
	#NOTE:	We use two variables: "actualName" which is the actual name of the article being linked to.  "textName" which is the
	#	link text/name that appears in the article's text.
	#NOTE:	Renamed links have a format "name of the article|name appearing in the text".  Therefore we split the links on '|'.
	#	This could theoretically interfere with article names, if any, which actually contain '|'.
	#NOTE:	Links to subsections within an article have a format "name of the article#name of the subsection".  Therefore, we split
	#	the links on '#'.  This could theoretically interfere with article names, if any, which actually contain '|'.
	#NOTE:	Links to a subsection within the same article have the format "#name of subsection".  We do not store these links in the linkList.
	#	We do not need to check for or remove this leading # from the textName since non-alphanumeric characters will eventually be ignored.
	def parse_internal_links(self):
		self.intLinkSet = set()						#Holds the actual name of all articles linked to by this article.
		#NOTE:	I am using a temporary list rather than a temporary set because I am assuming the number of repeats will be small and therefore
		#	it will be more efficient to process any repeats than to convert the list to a set.
		try:
			tempLinkList = self.intLink_ptrn.findall(self.text)		#Find all internal links in the text and store them in a temporary list.
			for link in tempLinkList:
				#Parse renamed links:
				splitLink = link.split("|")
				if len(splitLink) == 2:
					actualName = splitLink[0]
					textName = splitLink[1]
				elif len(splitLink) == 1:	#Link is not a renamed link.
					actualName = link
					textName = link
				else:				#Other
					#NOTE: How should we handle situtations where a link name contains a |?
					#Error
					pass

				#Parse links to subsections within the same article:
				#NOTE:	We do not handle explicit links to subsections within the same article.
				#	i.e. [[<same article name>]] or [[<same article name>#<subsection>]].
				if actualName[0] == "#":	#If the first character in the actual name is "#".
					continue		#Links to a subsection in the current article are not actually internal links.  Skip them.

				#Parse links to subsections in other articles:
				#NOTE: This also parses links to subsections in the same article (i.e. links with format [[#subsection]]).
				#NOTE: The parsing for this section is rather complicated, is there a way to ensure that it is correct?
				#NOTE: In both of these we take the 0th element (with [0]) in order to end up with a string rather than a list.
				actualName = actualName.split("#", 1)[0]
				textName = textName.split("#", 1)[0]

				#Store the actualName in the linkedList and replace the link with the textName in the text.
				self.intLinkSet.add(actualName)					#Store the link in the intLinkSet.
	        		self.text = self.text.replace("[[" + link + "]]", textName)	#Remove the link brackets from the text.
		except:
			pass

	#********************************************
	# parse_misc_links()
	#********************************************
	# Removes images, media, and "special" links
	# from the text.
	#********************************************
	def parse_misc_links(self):
		self.miscLinkList = list()
		try:
			for link in self.miscLink_ptrn.findall(self.text):
				self.text = self.text.replace(link, "")			#Remove the misc. links. from the text.
		except:
			pass

	#***** Accessor Methods *****
	def get_text(self):
		return self.text
	def get_title(self):
		return self.title
	def get_internal_links(self):
		for link in self.intLinkSet:
			yield link
	def get_internal_link_count(self):
		return len(self.intLinkSet)

if __name__ == "__main__":
	#Open the article:
	f = open("testInput.txt", "r")		#Open the text file containing the articles.

	#Parse the article:
	parser = article_parser()
	for article in f:
		parser.parse_article(article)	#Parse the next article

	#Print the results:
	print parser.get_text()

