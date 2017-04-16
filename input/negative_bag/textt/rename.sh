#!/usr/bin

dt=17
for i in {1..10}
do
	name=$(( 10 + $i ));
	mv $i.txt $name.txt
	
done	
