SELECT Event.id AS EventID, Event.name AS EventName,Category.name AS CategoryName, Event_Time.start_time As StartTime
FROM Event,Category,Event_Time
WHERE Event.id=Event_Time.event_id and Event.category_id=Category.id and MATCH(Event.description)
														AGAINST('+word' IN BOOLEAN MODE)
