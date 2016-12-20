#! /usr/bin/python

import sys
sys.path.append(".")
import heapq
from operator import itemgetter	#Used when we sort the data from heaps of tuples before returning them to the user.

class reduce_wordFreq():
	wordDict = dict()	#Dictionary: Keys are words, values are the number of times the word has occured.
	def process_packet(self, packet):
		#NOTE: Is it possible to do self.packet instead of passing things around?
		if len(packet) != 2:	#Error Checking: Verify that the packet is the correct length.
			print "********************"
			print "Error: Incorrect packet length. Packet length was " + str(len(packet)) + ", length should be 2."
			print "********************"
			print packet[0]
			return False

		if packet[0][0:3] == "WF_":
			try:
				packet[1] = int(packet[1])
				#NOTE: Is it better practice to use a general except or an except for a specific type of error (in this case ValueError)?
			except:
				print "********************"
				print "Error: Failed to convert second element of the packet to an integer."
				print "********************"
				return False
			self.reduce_word_frequency(packet)
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

	def reduce_word_frequency(self, packet):
		try:
			self.wordDict[packet[0]] += packet[1]	#Increase the frequency currently in the dictionary by the frequency in the packet.
		except KeyError:
			self.wordDict[packet[0]] = packet[1]	#If the words is not in the dicitonary yet, add it.

	#***** Accessor Functions *****
	def get_top_word_count(self):
		#Use a heap to find the most common words:
		topWordHeap = list()
		for word in self.wordDict:
			if len(topWordHeap) < 50:
				heapq.heappush(topWordHeap, (self.wordDict[word], word))
			else:
				heapq.heappushpop(topWordHeap, (self.wordDict[word], word))

		#Sort and return the list of most common words:
		return topWordHeap

if __name__ == "__main__":
	reducer = reduce_wordFreq()
	for line in sys.stdin:
		#Get the current packet:
		packet = line.strip().split('\t')	#Split on tabs.
		reducer.process_packet(packet)

	#Print Word Count:
	for word in reducer.get_top_word_count():
		print str(word[0]) + "|" + word[1][3:]

