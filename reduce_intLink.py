#! /usr/bin/python

import sys
sys.path.append(".")
import heapq
from operator import itemgetter	#Used when we sort the data from heaps of tuples before returning them to the user.

class reduce_intLink():
	intLinkDict = dict()	#Dictionary: Keys are article titles, values are the number of distinct articles that link to that article.
	def process_packet(self, packet):
		#NOTE: Is it possible to do self.packet instead of passing things around?
		if len(packet) != 2:	#Error Checking: Verify that the packet is the correct length.
			print "********************"
			print "Error: Incorrect packet length. Packet length was " + str(len(packet)) + ", length should be 2."
			print "********************"
			print packet[0]
			return False

		if packet[0][0:3] == "IL_":
			try:
				packet[1] = int(packet[1])
			except:
				print "********************"
				print "Error: Failed to convert second element of the packet to an integer."
				print "********************"
				return False
			self.reduce_internal_links(packet)
			return True
		elif packet[0][0:3] == "ER_":
			print "********************"
			print packet[0][3:]
			print packet[1]
			print "********************"
		else:
			print "********************"
			print "Error: Unrecognized packet type: " + packet[0]
			print "********************"
			return False

	def reduce_internal_links(self, packet):
		try:
			self.intLinkDict[packet[0]] += packet[1]	#Increment the link's frequency.
		except KeyError:
			self.intLinkDict[packet[0]] = packet[1]		#If the link is not in the dicitonary yet, add it.

	#***** Accessor Functions *****
	def get_top_internal_links(self):
		#Use a heap to find the most common internal links:
		topIntLinkHeap = list()
		for article in self.intLinkDict:
			if len(topIntLinkHeap) < 5:
				heapq.heappush(topIntLinkHeap, (self.intLinkDict[article], article))
			else:
				heapq.heappushpop(topIntLinkHeap, (self.intLinkDict[article], article))

		#Sort and return the list of most common internal links:
		return topIntLinkHeap

if __name__ == "__main__":
	reducer = reduce_intLink()
	for line in sys.stdin:
		#Get the current packet:
		packet = line.strip().split('\t')	#Split on tabs.
		reducer.process_packet(packet)

	#Print Internal Links:
	for link in reducer.get_top_internal_links():
		print str(link[0]) + "|" + link[1][3:]

