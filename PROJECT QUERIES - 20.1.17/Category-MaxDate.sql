SELECT Cat1.id AS CategoryID,Cat1.name AS CategoryName, max(EventTime1.start_time) AS maxDate
								FROM Category AS Cat1 ,Event AS Event1, Event_Time AS EventTime1
								WHERE Cat1.id=Event1.category_id and Event.id=EventTime1.event_id
								GROUP BY CategoryID,CategoryName
ORDER BY maxDate DESC;