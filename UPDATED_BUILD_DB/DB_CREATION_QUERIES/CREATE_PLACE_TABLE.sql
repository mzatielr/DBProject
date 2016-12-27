CREATE TABLE Place
(
	id	INT PRIMARY KEY,
	name VARCHAR(25) NOT NULL,
	city_id INT REFERENCES City(id),
	country_id INT REFERENCES Country(id),
	latitude REAL,
	longitude REAL
);