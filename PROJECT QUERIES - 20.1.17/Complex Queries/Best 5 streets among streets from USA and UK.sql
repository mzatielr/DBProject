SELECT Street.id,Street.name,Count(Event.id) AS NumOfEvents
FROM Event,Place,Event_Place,Street,City,Country
WHERE Event.id=Event_Place.event_id and Event_Place.place_id=Place.id and Place.street_id=Street.id 
		and Street.city_id=City.id and City.country_id=country.id and (Country.name='United States' OR Country.name='United Kingdom')
GROUP BY Street.id,Street.name
ORDER BY NumOfEvents
LIMIT 5;