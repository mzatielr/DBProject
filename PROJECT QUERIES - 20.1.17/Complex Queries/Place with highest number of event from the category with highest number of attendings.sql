SELECT Place.id, Place.name, Country.name, City.name, Street.name
FROM Place,Country,City,Street,(SELECT Place2.id AS PlaceID, COUNT(Event.id) AS NumberOfEvents
											FROM Place AS Place2,Event,Event_Place,(SELECT Category1.id AS CategoryID, SUM(EventTime1.attending_count) AS Num_Of_Attendings
																					FROM Event AS Event1 ,Category AS Category1, Event_Time AS EventTime1
																					WHERE Event1.category_id=Category1.id and Event.id=EventTime1.event_id
																					GROUP BY Category1.id
																					ORDER BY Num_Of_Attendings DESC
																					LIMIT 1) AS Category_With_Highest_Att
											WHERE Event.id=Event_Place.event_id and Event_Place.place_id=Place2.id and Event.category_id=Category_With_Highest_Att.CategoryID
											GROUP BY Place2.id
											ORDER BY(NumberOfEvents) DESC
											LIMIT 1) AS table1
WHERE Place.id=table1.PlaceID and Place.street_id=Street.id and Street.city_id=City.id and City.country_id=Country.id;