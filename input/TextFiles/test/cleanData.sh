#!/usr/bin

dt=17
for i in {1..20}
do
	
	grep -E -v 'Lead story now on|Top stories now on|#JustIn|#ndtv9|#Alert|UPDATE|#JUSTIN|#BREAKING|JUST IN' $i.txt > text/$i.txt
	
done	
