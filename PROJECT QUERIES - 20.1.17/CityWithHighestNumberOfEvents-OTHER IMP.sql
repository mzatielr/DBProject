SELECT City.name AS CityName ,Count(Event.id) As Num_Of_Events
FROM Event,Place,Event_Place,Street ,City
WHERE Event.id=EventPlace.event_id and EventPlace.place_id=Place.id and Place.street_id = Street.id and Street.city_id = City.id
GROUP BY City.name
ORDER BY Num_Of_Events DESC
LIMIT 1;