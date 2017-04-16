#!/usr/bin

dt=17
for i in {1..10}
do
	cut -d";" -f5 $i.csv|tr -d "\"" > allData.txt
	sed 's/http:.*//g' allData.txt > alldata2.txt
	sed 's/https:.*//g' alldata2.txt >> onlyTweets.txt 
	sed '/^$/d' alldata2.txt > textt/$i.txt 
	grep -v "Lead story now on" textt/$i.txt > text/$i.txt
	grep -v "Top stories now on" text/$i.txt > textt/$i.txt
	
done	
