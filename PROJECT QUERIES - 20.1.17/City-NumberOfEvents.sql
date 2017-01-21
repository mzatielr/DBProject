SELECT City.name AS CityName ,Count(Event.id) As Num_Of_Events
FROM Event,Place,Event_Place,City,Street
WHERE Event.id=Event_Place.event_id and Event_Place.place_id=Place.id and Place.street_id=Street.id and Street.city_id=City.id
GROUP BY City.id;