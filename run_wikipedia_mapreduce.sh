#!/bin/bash

input='/data/wikipedia-full/'		#Input folder when running Hadoop in distributed mode.
numReducers=5				#Number of reducers.

#hdfs dfs -rm -r /user/moneysdr/wikiOut

#***** Run word frequency MapReduce *****
output='/user/moneysdr/wikiOut/wordFreq'	#Output folder when running Hadoop in distributed mode.
mapper='map_wordFreq.py'			#Mapper file.
combiner='wikipedia_combine.py'			#Combiner file
reducer='reduce_wordFreq.py'			#Reducer file.
other='parse_wikitext.py'			#Other files.
hadoop jar $HADOOP_INSTALL/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar -D mapreduce.job.reduces=$numReducers -input $input -output $output -file $mapper $reducer $combiner $other -mapper $mapper -combiner $combiner -reducer $reducer

#***** Run reading level MapReduce *****
output='/user/moneysdr/wikiOut/readingLevel'	#Output folder when running Hadoop in distributed mode.
mapper='map_readingLevel.py'			#Mapper file.
combiner='wikipedia_combine.py'			#Combiner file
reducer='reduce_readingLevel.py'		#Reducer file.
other='parse_wikitext.py syl_dict.p'		#Other files.
hadoop jar $HADOOP_INSTALL/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar -D mapreduce.job.reduces=$numReducers -input $input -output $output -file $mapper $reducer $combiner $other -mapper $mapper -combiner $combiner -reducer $reducer

#***** Run link count MapReduce *****
output='/user/moneysdr/wikiOut/linkCount'	#Output folder when running Hadoop in distributed mode.
mapper='map_linkCount.py'			#Mapper file.
combiner='wikipedia_combine.py'			#Combiner file
reducer='reduce_linkCount.py'			#Reducer file.
other='parse_wikitext.py'			#Other files.
hadoop jar $HADOOP_INSTALL/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar -D mapreduce.job.reduces=$numReducers -input $input -output $output -file $mapper $reducer $combiner $other -mapper $mapper -combiner $combiner -reducer $reducer

#***** Run internal link MapReduce *****
output='/user/moneysdr/wikiOut/intLink'		#Output folder when running Hadoop in distributed mode.
mapper='map_intLink.py'				#Mapper file.
combiner='wikipedia_combine.py'			#Combiner file
reducer='reduce_intLink.py'			#Reducer file.
other='parse_wikitext.py'			#Other files.
hadoop jar $HADOOP_INSTALL/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar -D mapreduce.job.reduces=$numReducers -input $input -output $output -file $mapper $reducer $combiner $other -mapper $mapper -combiner $combiner -reducer $reducer

#***** Get the results *****
hdfs dfs -get /user/moneysdr/wikiOut/

#***** Combine the results *****
for i in {0..4}
do
	cat wikiOut/wordFreq/part-0000$i >> wikiOut/wordFreq/combined
	cat wikiOut/readingLevel/part-0000$i >> wikiOut/readingLevel/combined
	cat wikiOut/linkCount/part-0000$i >> wikiOut/linkCount/combined
	cat wikiOut/intLink/part-0000$i >> wikiOut/intLink/combined
done

#***** Sort the results *****
	sort -t '|' -n -r wikiOut/wordFreq/combined >> wikiOut/wordFreq/wordFreq_results
	sort -t '|' -n -r wikiOut/readingLevel/combined >> wikiOut/readingLevel/readingLevel_results
	sort -t '|' -n -r wikiOut/linkCount/combined >> wikiOut/linkCount/linkCount_results
	sort -t '|' -n -r wikiOut/intLink/combined >> wikiOut/intLink/intLink_results
