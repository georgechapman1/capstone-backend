sqlite> .mode csv

sqlite>.import c:/sqlite/city.csv rivers

sqlite> .schema rivers
CREATE TABLE rivers(
  "name" TEXT,
);

SELECT 
   name
FROM 
   rivers;

DROP TABLE IF EXISTS rivers;


CREATE TABLE rivers(
  name TEXT NOT NULL,
#   population INTEGER NOT NULL 
);

sqlite> .mode csv
sqlite> .import c:/sqlite/city_no_header.csv rivers
