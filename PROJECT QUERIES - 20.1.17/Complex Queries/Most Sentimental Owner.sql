SELECT Owner.id AS OwnerID, Owner.name AS OwnerName,COUNT(Event.id) AS NumberOfEvents
FROM Event,Owner,Event_Owner
WHERE Event.id=Event_Owner.event_id and Event_Owner.owner_id=Owner.id and MATCH(Event.description)
												AGAINST('+Love' IN BOOLEAN MODE)
GROUP BY Owner.id
ORDER BY NumberOfEvents DESC
LIMIT 1;
