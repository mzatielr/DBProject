SELECT Event.id, Event.name, Category.name, Event.description, Event.start_time, Event.end_time,City.name
FROM Event,Category,Place,Street,City,(SELECT Month(Event1.start_time) AS month1,City.id AS cityID Event1.attending_count as maxAtt
																		FROM Event as Event1,Place AS Place1, Street AS Street1, City As City1
																		WHERE Event.place_id=Place.id and Place.street_id = Street.id and Street.city_id = City.it
																		ORDER BY (maxAtt) DESC
																		LIMIT 1) AS maxAttTable
WHERE Event.category_id=Category.id and Event.place_id = Place.id and Place.street_id = Street.id and Street.city_id = City.id and City.id = maxAttTable.cityID
and Month(Event.start_time) = maxAttTable.month1;
