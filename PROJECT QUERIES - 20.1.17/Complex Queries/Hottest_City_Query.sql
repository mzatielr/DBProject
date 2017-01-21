SELECT City.name,Event.id,Event.name,Category.name,Event.description,Date(Event_Time.start_time),DATE(Event_Time.end_time)
FROM Event,Street,City,Category,Place,Event_Time,(SELECT City1.id AS CityId1 ,Count(Event1.id) As Num_Of_Events
													FROM Event AS Event1,Place AS Place1 ,Street AS Street1,City AS City1
													WHERE Place1.street_id = Street1.id and Street1.city_id=City1.id and Place1.id=Event1.place_id
													GROUP BY City1.id
													ORDER BY Num_Of_Events DESC
													LIMIT 1) AS CityMaxEventsTable
WHERE Event.category_id=Category.id and Event.place_id=Place.id and Place.street_id=Street.id and Street.city_id = City.id 
									and City.id=CityMaxEventsTable.CityId1 and Event.id=Event_Time.event_id and Event_Time.start_time>=CURDATE() 
ORDER BY (Event.start_time)
LIMIT 10;