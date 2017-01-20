SELECT City.id,City.name COUNT(*)
FROM Event,Street,City,Place
WHERE Event.place_id=Place.id and Place.street_id = Street.id and Street.city_id=City.id and City.name=X