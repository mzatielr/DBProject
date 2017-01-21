CREATE TABLE Event_Time 
(
	event_id BIGINT(20) NOT NULL,
	timezone_id INT(11)  DEFAULT NULL,
	start_time DATETIME  DEFAULT NULL,
	end_time DATETIME  DEFAULT NULL,
	update_time DATETIME  DEFAULT NULL,
	PRIMARY KEY (event_id),
	FOREIGN KEY (event_id)
		REFERENCES Event(id),
	FOREIGN KEY (timezone_id)
		REFERENCES Timezone(id)

)
COLLATE='utf8_general_ci'
ENGINE=MyISAM
;