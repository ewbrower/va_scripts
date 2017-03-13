DROP DATABASE va_inventory;
CREATE DATABASE va_inventory;
USE va_inventory;
CREATE TABLE procedures (CPT int NOT NULL,name char(30),ORCC int NOT NULL,PRIMARY KEY (CPT, ORCC));
CREATE TABLE trays (Tray_id int NOT NULL,tray char(30),ORCC int NOT NULL,T_QTY int NOT NULL,PRIMARY KEY (Tray_id, ORCC));
CREATE TABLE instruments (id int NOT NULL,instrument char(30),I_QTY int NOT NULL,Tray_id int,PRIMARY KEY (id, Tray_id));