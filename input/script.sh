#!/usr/bin

dt=17
for i in {1..10}
do
	touch $i.csv

	from_date=2016-11-$dt
	dt=$(( dt + 1))
	to_date=2016-11-$dt

	python Exporter.py --username "ndtv" --since $from_date --until $to_date
	mv output_got.csv "ndtv"$i.csv

	python Exporter.py --username "timesofindia" --since $from_date --until $to_date
	mv output_got.csv "timesofindia"$i.csv

	python Exporter.py --username "IndianExpress" --since $from_date --until $to_date
	mv output_got.csv "IndianExpress"$i.csv

	tail -n +2 "ndtv"$i.csv >> $i.csv
	echo "" >> $i.csv
	tail -n +2 "timesofindia"$i.csv >> $i.csv
	echo "" >> $i.csv
	tail -n +2 "IndianExpress"$i.csv >> $i.csv

	rm ndtv*
	rm timesofindia*
	rm IndianExpress*	
	
	echo $from_date," and ",$to_date
done	