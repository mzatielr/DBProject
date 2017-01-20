CREATE TABLE Street 
(
	id BIGINT(20) NOT NULL,
	name VARCHAR(75) NOT NULL,
	city_id BIGINT(20) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (city_id)
		REFERENCES City(id)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;