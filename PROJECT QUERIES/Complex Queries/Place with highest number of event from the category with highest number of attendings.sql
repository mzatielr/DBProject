SELECT Place.*
FROM Place,(SELECT Place2.id AS PlaceID, COUNT(Event.id) AS NumberOfEvents
				FROM Place AS Place2,Event,(SELECT Category1.id AS CategoryID, SUM(Event1.attending_count) AS Num_Of_Attendings
										FROM Event AS Event1 ,Category AS Category1
										WHERE Event1.category_id=Category1.id
										GROUP BY Category1.id
										ORDER BY Num_Of_Attendings DESC
										LIMIT 1) AS Category_With_Highest_Att
				WHERE Place2.id=Event.place_id and Event.category_id=Category_With_Highest_Att.CategoryID
				GROUP BY Place2.id
				ORDER BY(NumberOfEvents) DESC
				LIMIT 1) AS table1
WHERE Place.id=table1.PlaceID;