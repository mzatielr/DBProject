SELECT City.name
FROM City, (SELECT City1.id AS CityId ,Count(Event1.id) As Num_Of_Events
				FROM Event AS Event1,Place AS Place1,Event_Place AS EventPlace1,Street AS Street1 ,City AS City1
				WHERE Event1.id=EventPlace1.event_id and EventPlace1.place_id=Place1.id and Place1.street_id=Street1.id and Street1.city_id=City1.id
				GROUP BY City1.id) AS CityEventsTable
WHERE City.id=CityEventsTable.CityId and CityEventsTable.Num_Of_Events >= ALL (SELECT Count(Event2.id)
																				 FROM Event AS Event2,Place AS Place2,Event_Place AS EventPlace2,Street AS Street2 ,City AS City2
																				 WHERE Event2.id=EventPlace2.event_id and EventPlace2.place_id=Place2.id 
																				 and Place2.street_id=Street2.id and Street2.city_id=City2.id
																				 GROUP BY City2.id);