SELECT Event.id,Event.name,Category.name,Event.description
FROM Event,Category,(SELECT min(Event2.id) AS Newest_Event_ID
							FROM Event AS Event2,(SELECT Cat1.id AS CategoryID, max(Event1.start_time) AS maxDate
															FROM Category AS Cat1 ,Event AS Event1
															WHERE Cat1.id=Event1.category_id
															GROUP BY CategoryID
															ORDER BY maxDate DESC
															LIMIT 8) AS CatMaxDateTable
							WHERE Event2.category_id=CatMaxDateTable.CategoryID and Event2.start_time=CatMaxDateTable.maxDate
							GROUP BY Event2.category_id) AS EventIDS
WHERE Event.id=EventIDS.Newest_Event_ID and Event.category_id=Category.id;