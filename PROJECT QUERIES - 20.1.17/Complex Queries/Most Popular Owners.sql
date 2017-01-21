SELECT Owner.id,Owner.name,OwnerAttTable.OwnerAttendings,COUNT(Comment.id) AS Num_Of_Comments
FROM Owner,Event,Event_Owner,Comment,(SELECT Owner1.id AS OwnerID1, SUM(EventGuests1.attending_count) AS OwnerAttendings
									FROM Event AS Event1, Owner AS Owner1,Event_Owner AS EventOwner1, Event_Guests AS EventGuests1
									WHERE Event.id=EventOwner1.event_id and EventOwner1.owner_id=Owner1.id and Event.id=EventGuests1.event_id
									GROUP BY Owner1.id
									ORDER BY OwnerAttendings DESC
									LIMIT 10) AS OwnerAttTable
WHERE Event.id=Event_Owner.event_id and Event_Owner.owner_id=Owner.id and Owner.id=OwnerAttTable.OwnerID1 and Event.id=Comment.event_id
GROUP BY Owner.id,Owner.name,OwnerAttTable.OwnerAttendings
ORDER BY Num_Of_Comments DESC
LIMIT 10;