SELECT Street.id,Street.name,Count(Event.id) AS NumOfEvents
FROM Event,Place,Street,Country
WHERE Event.place_id=Place.id and Place.street_id=Street.id 
		and Place.country_id=Country.id and (Country.name='United States' OR Country.name='United Kingdom')
GROUP BY Street.id,Street.name
ORDER BY NumOfEvents
LIMIT 5;