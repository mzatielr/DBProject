CREATE TABLE Event (
	id BIGINT(20) NOT NULL,
	name VARCHAR(100)  DEFAULT NULL,
	is_canceled Tinyint(1)  DEFAULT NULL,
	description VARCHAR(400)  DEFAULT NULL,
	category_id INT(5)  DEFAULT 'Other',
	owner_id BIGINT(20)  NOT NULL,
	place_id BIGINT(20)  DEFAULT NULL,
	can_guest_invite Tinyint(1)  DEFAULT NULL,
	cover_source VARCHAR(255)  DEFAULT NULL,
	event_ticket_uri VARCHAR(255) DEFAULT NULL,
	guest_list_enabled Tinyint(1)  DEFAULT NULL,
	event_type VARCHAR(12)  DEFAULT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (category_id)
		REFERENCES Category(id),
	FOREIGN KEY (owner_id)
		REFERENCES Owner(id),
	FOREIGN KEY (place_id)
		REFERENCES Place(id)
)
COLLATE='utf8_general_ci'
ENGINE=MyISAM
;