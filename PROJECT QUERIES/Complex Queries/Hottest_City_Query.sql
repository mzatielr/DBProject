SELECT Event.*
FROM Event,Place,(SELECT City1.id AS CityId1 ,Count(Event1.id) As Num_Of_Events
								FROM Event AS Event1,Place AS Place1 ,City AS City1
								WHERE City1.id=Place1.city_id and Place1.id=Event1.place_id
								GROUP BY City1.id) AS CityEventsTable
WHERE Event.place_id=Place.id and Place.city_id=CityEventsTable.CityId1 and CityEventsTable.Num_Of_Events >= ALL (SELECT Count(Event2.id)
																																					  	 FROM Event AS Event2,Place AS Place2 ,City AS City2
																																					 	 WHERE City2.id=Place2.city_id and Place2.id=Event2.place_id
																																					    GROUP BY City2.id)
ORDER BY (Event.start_time)
LIMIT 10;