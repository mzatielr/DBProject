SELECT Category1.id, SUM(EventGuests1.attending_count) AS Num_Of_Attendings
FROM Event AS Event1 ,Category AS Category1,Event_Guests AS EventGuests1
WHERE Event1.category_id=Category1.id and Event.id=EventGuests1.event_id
GROUP BY Category1.id
ORDER BY Num_Of_Attendings DESC
LIMIT 1;