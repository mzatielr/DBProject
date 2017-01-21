SELECT City.id,City.name COUNT(*)
FROM Event,Street,City,Place,Event_Place
WHERE Event.id=Event_Place.event_id and Event_Place.place_id=Place.id and Place.street_id = Street.id and Street.city_id=City.id and City.name=X