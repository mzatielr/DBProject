SELECT City.name AS CityName ,Count(Event.id) As Num_Of_Events
FROM Event,Place,Street ,City
WHERE Place.id=Event.place_id and Place.street_id = Street.id and Street.city_id = City.id
GROUP BY City.name
ORDER BY Num_Of_Events DESC
LIMIT 1;