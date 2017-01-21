SELECT Event.id, Event.name, Category.name, Event.description, Event_Time.start_time, Event_Time.end_time,City.name
FROM Event,Category,Place,Event_Place,Street,City,Event_Time,(SELECT Month(EventTime1.start_time) AS month1,City.id AS cityID EventGuests1.attending_count as maxAtt
																		FROM Event as Event1,Place AS Place1,Event_Place AS EventPlace1, Street AS Street1, City As City1, Event_Time AS EventTime1, Event_Guests AS EventGuests1
																		WHERE Event.id=EventTime1.event_id and Event.id=EventGuests1.event_id 
																					and Event.id=EventPlace1.event_id and EventPlace1.place_id=Place.id and Place.street_id = Street.id and Street.city_id = City.it
																		ORDER BY (maxAtt) DESC
																		LIMIT 1) AS maxAttTable
WHERE Event.category_id=Category.id and Event.id=Event_Place.event_id and Event_Place.place_id = Place.id and Place.street_id = Street.id and Street.city_id = City.id and City.id = maxAttTable.cityID
and Event.id=Event_Time.event_id and Month(Event_Time.start_time) = maxAttTable.month1;
