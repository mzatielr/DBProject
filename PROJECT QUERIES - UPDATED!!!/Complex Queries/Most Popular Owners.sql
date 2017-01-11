SELECT Owner.id,Owner.name,OwnerAttTable.OwnerAttendings,COUNT(Comment.id) AS Num_Of_Comments
FROM Owner,Event,Comment,(SELECT Owner1.id AS OwnerID1, SUM(Event1.attending_count) AS OwnerAttendings
									FROM Event AS Event1, Owner AS Owner1
									WHERE Owner1.id=Event1.owner_id
									GROUP BY Owner1.id
									ORDER BY OwnerAttendings DESC
									LIMIT 10) AS OwnerAttTable
WHERE Owner.id=OwnerAttTable.OwnerID1 and Owner.id=Event.owner_id and Event.id=Comment.event_id
GROUP BY Owner.id,Owner.name,OwnerAttTable.OwnerAttendings
ORDER BY Num_Of_Comments DESC
LIMIT 10;