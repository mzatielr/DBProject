SELECT Owner.id AS OwnerID, Owner.name AS OwnerName,COUNT(Event.id) AS NumberOfEvents
FROM Event,Owner
WHERE Owner.id=Event.owner_id and MATCH(Event.description)
												AGAINST('+Love' IN BOOLEAN MODE)
GROUP BY Owner.id
ORDER BY NumberOfEvents DESC
LIMIT 1;
