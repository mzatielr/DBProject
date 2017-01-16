SELECT City.name AS CityName ,Count(Event.id) As Num_Of_Events
FROM Event,Place ,City
WHERE City.id=Place.city_id and Place.id=Event.place_id
GROUP BY City.name
ORDER BY Num_Of_Events DESC
LIMIT 1;