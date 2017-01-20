CREATE TABLE Comment 
(
	id BIGINT(20) NOT NULL AUTO_INCREMENT,
	name VARCHAR(25) NOT NULL,
	message VARCHAR(300) NOT NULL COLLATE 'utf8_general_ci',
	updated_time DATETIME DEFAULT NULL,
	event_id BIGINT(20) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (event_id)
		REFERENCES Event(id)
)
COLLATE='utf8_unicode_ci'
ENGINE=MyISAM
;