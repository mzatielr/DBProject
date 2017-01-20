SELECT City.name AS CityName ,Count(Event.id) As Num_Of_Events
FROM Event,Place,City,Street
WHERE Place.id=Event.place_id and Place.street_id=Street.id and Street.city_id=City.id
GROUP BY City.id;