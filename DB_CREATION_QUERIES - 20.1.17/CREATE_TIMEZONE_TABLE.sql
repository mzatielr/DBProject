CREATE TABLE Timezone 
(
	id BIGINT(17) NOT NULL AUTO_INCREMENT,
	timezone VARCHAR(40) NOT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (id)
)
COLLATE='utf8_general_ci'
ENGINE=MyISAM
;
