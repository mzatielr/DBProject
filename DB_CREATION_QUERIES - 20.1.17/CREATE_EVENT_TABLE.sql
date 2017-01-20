CREATE TABLE Event (
	id BIGINT(20) NOT NULL,
	name VARCHAR(100)  DEFAULT NULL,
	attending_count INT(11) DEFAULT NULL,
	declined_count INT(11) DEFAULT NULL,
	maybe_count INT(11)  DEFAULT NULL,
	interested_count INT(11)  DEFAULT NULL,
	noreply_count INT(11)  DEFAULT NULL,
	is_canceled Tinyint(1)  DEFAULT NULL,
	description VARCHAR(400)  DEFAULT NULL,
	category_id BIGINT(20)  DEFAULT NULL,
	owner_id BIGINT(20)  DEFAULT NULL,
	place_id BIGINT(20)  DEFAULT NULL,
	can_guest_invite Tinyint(1)  DEFAULT NULL,
	cover_source VARCHAR(500)  DEFAULT NULL,
	event_ticket_uri VARCHAR(30) DEFAULT NULL,
	guest_list_enabled INT(11)  DEFAULT NULL,
	start_time DATETIME  DEFAULT NULL,
	end_time DATETIME  DEFAULT NULL,
	update_time DATETIME  DEFAULT NULL,
	timezone_id INT(11)  DEFAULT NULL,
	event_type VARCHAR(12)  DEFAULT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (category_id)
		REFERENCES Category(id)
	FOREIGN KEY (owner_id)
		REFERENCES Owner(id)
	FOREIGN KEY (place_id)
		REFERENCES Place(id)
	FOREIGN KEY (timezone_id)
		REFERENCES Timezone(id)

)
COLLATE='utf8_general_ci'
ENGINE=MyISAM
;