SELECT Place.id, COUNT(Event.id) AS NumberOfEvents
FROM Place,Event,(SELECT Category1.id AS CategoryID, SUM(Event1.attending_count) AS Num_Of_Attendings
						FROM Event AS Event1 ,Category AS Category1
						WHERE Event1.category_id=Category1.id
						GROUP BY Category1.id
						ORDER BY Num_Of_Attendings DESC
						LIMIT 1) AS Category_With_Highest_Att
WHERE Place.id=Event.place_id and Event.category_id=Category_With_Highest_Att.CategoryID
GROUP BY Place.id
ORDER BY(NumberOfEvents)
LIMIT 1;