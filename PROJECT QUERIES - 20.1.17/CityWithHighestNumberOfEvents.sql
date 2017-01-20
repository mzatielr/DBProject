SELECT City.name
FROM City, (SELECT City1.id AS CityId ,Count(Event1.id) As Num_Of_Events
				FROM Event AS Event1,Place AS Place1,Street AS Street1 ,City AS City1
				WHERE Place1.id=Event1.place_id and Place1.street_id=Street1.id and Street1.city_id=City1.id
				GROUP BY City1.id) AS CityEventsTable
WHERE City.id=CityEventsTable.CityId and CityEventsTable.Num_Of_Events >= ALL (SELECT Count(Event2.id)
																										 FROM Event AS Event2,Place AS Place2,Street AS Street2 ,City AS City2
																										 WHERE Place2.id=Event2.place_id and Place2.street_id=Street2.id and Street2.city_id=City2.id
																										 GROUP BY City2.id);