SELECT DISTINCT Category.id,Category.name
FROM Category,(SELECT Event.id AS EventID,Event.category_id AS EventCategoryID, COUNT(Comment.id) AS Num_Of_Comments
					FROM Event,Comment
					WHERE Event.id=Comment.event_id
					GROUP BY Event.id,Event.category_id
					ORDER BY Num_Of_Comments DESC
					LIMIT 10) AS TopTenEventsByComments
WHERE Category.id=TopTenEventsByComments.EventCategoryID