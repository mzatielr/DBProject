SELECT maxDateTable.CategoryID,maxDateTable.CategoryName,min(Event2.id) AS Newest_Event_ID
FROM Event AS Event2,(SELECT Cat1.id AS CategoryID,Cat1.name AS CategoryName, max(Event1.start_time) AS maxDate
								FROM Category AS Cat1 ,Event AS Event1
								WHERE Cat1.id=Event1.category_id
								GROUP BY CategoryID,CategoryName
								ORDER BY maxDate DESC) AS maxDateTable
WHERE Event2.category_id=maxDateTable.CategoryID and Event2.start_time=maxDateTable.maxDate
GROUP BY maxDateTable.CategoryID,maxDateTable.CategoryName
LIMIT 8;