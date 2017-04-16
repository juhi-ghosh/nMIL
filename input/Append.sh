#!/usr/bin

dt=17
for i in {1..10}
do
	cat ./DemonitizationData/text/$i.txt >> ./TextFiles/Demonitization/$i.txt
done	
