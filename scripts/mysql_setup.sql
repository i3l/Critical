DROP DATABASE icu;
CREATE DATABASE icu;
USE icu;

CREATE TABLE pinfo (
        id INT,
        age INT,
        gender INT,
        height DOUBLE,
        icutype INT,
        weight INT
);
CREATE TABLE outcome (
        id INT,
        saps1 INT,
        sofa INT,
        los INT,
        survival INT,
        death INT
);
CREATE TABLE vstats (
        id INT,
        time TIME,
        var TEXT,
        value DOUBLE,
        dvalue INT
);
LOAD DATA LOCAL INFILE 'data/Outcomes-a.txt' INTO TABLE outcome
        FIELDS TERMINATED BY ','
        LINES TERMINATED BY '\n';
SELECT "Database setup complete!" AS "";
SELECT "Run the following to insert data in Unix console:" AS "";
SELECT "" AS "";
SELECT "for f in data/set-a/*.txt; do" AS "";
SELECT "python2 txtDataToMySQL.py $f;" AS "";
SELECT "done" AS "";
