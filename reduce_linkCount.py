#! /usr/bin/python

import sys
sys.path.append(".")
import heapq
from operator import itemgetter	#Used when we sort the data from heaps of tuples before returning them to the user.

class reduce_linkCount():
	linkCountHeap = list()	#Heap that holds the five articles which link to the most other articles.
	def process_packet(self, packet):
		#NOTE: Is it possible to do self.packet instead of passing things around?
		if len(packet) != 2:	#Error Checking: Verify that the packet is the correct length.
			print "********************"
			print "Error: Incorrect packet length. Packet length was " + str(len(packet)) + ", length should be 2."
			print "********************"
			print packet[0]
			return False

		if packet[0][0:3] == "LC_":
			try:
				packet[1] = int(packet[1])
			except:
				print "********************"
				print "Error: Failed to convert second element of the packet to an integer."
				print "********************"
				return False
			self.reduce_link_count(packet)
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

	def reduce_link_count(self, packet):
		#Calculate top out links:
		if len(self.linkCountHeap) < 5:
			heapq.heappush(self.linkCountHeap, (packet[1], packet[0]))
		else:
			#NOTE: Is the following faster than checking whether the current article has more links than the minimum in the heap?
			heapq.heappushpop(self.linkCountHeap, (packet[1], packet[0]))

	#***** Accessor Functions *****
	def get_link_count(self):
		return sorted(self.linkCountHeap)

if __name__ == "__main__":
	reducer = reduce_linkCount()
	for line in sys.stdin:
		#Get the current packet:
		packet = line.strip().split('\t')	#Split on tabs.
		reducer.process_packet(packet)

	#Print Link Count:
	for article in reducer.get_link_count():
		print str(article[0]) + "|" + article[1][3:]

