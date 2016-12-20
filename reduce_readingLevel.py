#! /usr/bin/python

import sys
sys.path.append(".")
import heapq
from operator import itemgetter	#Used when we sort the data from heaps of tuples before returning them to the user.

class reduce_readingLevel():
	wordDict = dict()	#Dictionary: Keys are words, values are the number of times the word has occured.
	topRLHeap = list()	#Heap that holds the five articles with the highest reading levels.
	bottomRLHeap = list()	#Heap that holds the five articles with the lowest reading levels.
	def process_packet(self, packet):
		#NOTE: Is it possible to do self.packet instead of passing things around?
		if len(packet) != 2:	#Error Checking: Verify that the packet is the correct length.
			print "********************"
			print "Error: Incorrect packet length. Packet length was " + str(len(packet)) + ", length should be 2."
			print "********************"
			print packet[0]
			return False

		if packet[0][0:3] == "RL_":
			try:
				packet[1] = float(packet[1])
			except:
				print "********************"
				print "Error: Failed to convert second element of the packet to a float."
				print "********************"
				return False
			self.reduce_reading_level(packet)
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

	def reduce_reading_level(self, packet):
		#Calculate top reading level:
		if len(self.topRLHeap) < 5:
			heapq.heappush(self.topRLHeap, (packet[1], packet[0]))
		else:
			heapq.heappushpop(self.topRLHeap, (packet[1], packet[0]))

		#Calculate bottom reading level:
		readingLevel = -1 * packet[1]	#Invert the reading level in order to make the min heap act like a max heap.
		if len(self.bottomRLHeap) < 5:
			heapq.heappush(self.bottomRLHeap, (readingLevel, packet[0]))
		else:
			heapq.heappushpop(self.bottomRLHeap, (readingLevel, packet[0]))

	def get_top_reading_level(self):
		return sorted(self.topRLHeap)

	def get_bottom_reading_level(self):
		return sorted(self.bottomRLHeap)

if __name__ == "__main__":
	reducer = reduce_readingLevel()
	for line in sys.stdin:
		#Get the current packet:
		packet = line.strip().split('\t')	#Split on tabs.
		reducer.process_packet(packet)

	#Print Top Reading Level:
	for article in reducer.get_top_reading_level():
		print str(article[0]) + "|" + article[1][3:]

	#Print Bottom Reading Level:
	for article in reducer.get_bottom_reading_level():
		#NOTE:	When reducing we multiplied article[0] by -1 to make heapq act like a max heap instead of a min heap.
		#	Therefore, we now mutliply by -1 again before printing the value.
		print str(article[0] * -1) + "|" + article[1][3:]

