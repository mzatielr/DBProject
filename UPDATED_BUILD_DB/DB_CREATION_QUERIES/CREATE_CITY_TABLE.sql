CREATE TABLE City
(
	id	INT PRIMARY KEY,
	name VARCHAR(20) NOT NULL,
	country_id INT REFERENCES Country(id)
);