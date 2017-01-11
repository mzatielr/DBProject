SELECT Owner.id AS OwnerID2,COUNT(Comment.id) AS Num_Of_Comments
FROM Owner AS Owner2,Event AS Event2, Comment,(SELECT Owner1.id AS OwnerID1, SUM(Event1.attending_count) AS OwnerAttendings
																FROM Event AS Event1, Owner AS Owner1
																WHERE Owner1.id=Event1.owner_id
																GROUP BY Owner1.id
																ORDER BY OwnerAttendings DESC
																LIMIT 10) AS OwnerAttTable
WHERE Owner2.id=OwnerAttTable.id and Owner2.id=Event2.owner_id and Event2.id=Comment.event_id
GROUP BY OwnerID2
ORDER BY Num_Of_Comments DESC
