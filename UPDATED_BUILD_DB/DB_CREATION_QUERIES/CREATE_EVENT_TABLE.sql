CREATE TABLE Event
(
	id	INT PRIMARY KEY,
	name VARCHAR(30),
	attending_count INT,
	declined_count INT,
	maybe_count INT,
	interested_count INT,
	noreply_count INT,
	is_canceled INT, 
	description VARCHAR(250),
	category_id INT REFERENCES Category(id),
	owner_id INT REFERENCES Owner(id),
	place_id INT REFERENCES Place(id),
	can_guest_invite INT,
	guest_list_enabled INT,
	cover_id INT,
	cover_offset_x INT,
	cover_offset_y INT,
	cover_source VARCHAR(100),
	start_time DATETIME,
	end_time DATETIME,
	update_time DATETIME,
	timezone_id INT REFERENCES Timezone(id),
	event_type VARCHAR(12)
	
);