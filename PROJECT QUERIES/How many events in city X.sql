SELECT COUNT(*)
FROM Event,City,Place
WHERE Event.place_id=Place.id and Place.city_id=City.id and City.name=X