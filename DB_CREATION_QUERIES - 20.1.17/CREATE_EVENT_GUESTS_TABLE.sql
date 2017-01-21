CREATE TABLE Event_Guests
 (
	event_id BIGINT(20) NOT NULL,
	attending_count INT(8) DEFAULT NULL,
	declined_count INT(8) DEFAULT NULL,
	maybe_count INT(8)  DEFAULT NULL,
	interested_count INT(8)  DEFAULT NULL,
	noreply_count INT(8)  DEFAULT NULL,
	PRIMARY KEY (event_id),
	FOREIGN KEY (event_id)
		REFERENCES Event(id)
)
COLLATE='utf8_general_ci'
ENGINE=MyISAM
;