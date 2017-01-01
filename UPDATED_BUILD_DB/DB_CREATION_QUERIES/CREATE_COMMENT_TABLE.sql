CREATE TABLE Comment
(
	id	INT PRIMARY KEY,
	message VARCHAR(150) NOT NULL,
	updated_time DATETIME,
	event_it INT REFERENCES Event(id)
);