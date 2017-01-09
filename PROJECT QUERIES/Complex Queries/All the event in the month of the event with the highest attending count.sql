SELECT Event.*
FROM Event
WHERE Month(Event.start_time) = (SELECT Month(Event1.start_time)
											FROM Event as Event1
											WHERE Event1.attending_count = (SELECT max(Event2.attending_count)
																						FROM Event as Event2)
											Limit 1);
