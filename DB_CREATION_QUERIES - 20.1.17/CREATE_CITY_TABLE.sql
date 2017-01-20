CREATE TABLE City 
(
	id BIGINT(10) NOT NULL AUTO_INCREMENT,
	name VARCHAR(30) NOT NULL,
	country_id BIGINT(10) NOT NULL,
	PRIMARY KEY (id)
	FOREIGN KEY (country_id) 
        	   REFERENCES  Country(id) 
)
COLLATE='utf8_general_ci'
ENGINE=MyISAM
;
