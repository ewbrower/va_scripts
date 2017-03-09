CREATE database


CREATE TABLE procedures (
	CPT int NOT NULL,
	orcc int NOT NULL,
	surgery char(30)
	PRIMARY KEY (CPT),
	PRIMARY KEY (orcc)
	);
CREATE TABLE trays (
	orcc int NOT NULL,
	tray int NOT NULL,
	name char(30),
	instrumentID int,
	PRIMARY KEY (orcc),
	PRIMARY KEY (tray)
	);
CREATE TABLE instruments (
	id int NOT NULL,
	instrument char(30),
	PRIMARY KEY (id)
	);

-- inserts

-- INSERT INTO procedures VALUES(1, "brain surgery - left", 1);
-- INSERT INTO procedures VALUES(2, "brain surgery - right", 1);
-- INSERT INTO picklists VALUES(1, "brain box");
-- INSERT INTO trays VALUES(1, "brain tools", 1);
-- INSERT INTO trays VALUES(2, "cutting tools", 1);
-- INSERT INTO trays VALUES(3, "cleanup tools", 1);
-- INSERT INTO instruments VALUES(1, "brain bucket", 1);
-- INSERT INTO instruments VALUES(2, "brain scope", 1);
-- INSERT INTO instruments VALUES(3, "knife", 2);
-- INSERT INTO instruments VALUES(4, "bigger knife", 2);
-- INSERT INTO instruments VALUES(5, "saw", 2);
-- INSERT INTO instruments VALUES(6, "mop", 3);

-- queries

SELECT * FROM instruments;
SELECT * FROM trays;
SELECT * FROM picklists;
SELECT * FROM procedures;
