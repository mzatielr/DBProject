CREATE TABLE City 
(
	id BIGINT(20) NOT NULL AUTO_INCREMENT,
	name VARCHAR(40) NOT NULL,
	country_id BIGINT(20) NOT NULL,
	PRIMARY KEY (id)
	FOREIGN KEY (country_id) 
        	   REFERENCES  City(id) 
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;
