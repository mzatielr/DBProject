SELECT 
    Event.id AS event_id,
    Event.name AS event_name,
    Category.name AS event_category,	
    Event.description AS event_description,
    DATE_FORMAT(Event.start_time,"%e/%c/%Y %H:%i") AS event_start_time,
    DATE_FORMAT(Event.end_time,"%e/%c/%Y %H:%i") AS event_end_time
FROM
    Event,
    Category
WHERE
    Event.category_id = Category.id
        AND MONTH(Event.start_time) = (SELECT 
            MONTH(Event1.start_time)
        FROM
            Event AS Event1
        WHERE
            Event1.attending_count = (SELECT 
                    MAX(Event2.attending_count)
                FROM
                    Event AS Event2)
        LIMIT 1);
