SELECT Event.id AS EventID, Event.name AS EventName,Category.name AS CategoryName, Event.start_time As StartTime
FROM Event,Category
WHERE Event.category_id=Category.id and MATCH(Event.description)
														AGAINST('+word' IN BOOLEAN MODE)
