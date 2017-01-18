SELECT 
    Event.id,
    Event.name,
    Category.name,
    Event.description,
    Event.start_time,
    Event.end_time
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
