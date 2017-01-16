SELECT Cat1.id AS CategoryID,Cat1.name AS CategoryName, max(Event1.start_time) AS maxDate
								FROM Category AS Cat1 ,Event AS Event1
								WHERE Cat1.id=Event1.category_id
								GROUP BY CategoryID,CategoryName
ORDER BY maxDate DESC;