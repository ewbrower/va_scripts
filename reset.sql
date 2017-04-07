DROP DATABASE va_inventory;
CREATE DATABASE va_inventory;
USE va_inventory;
CREATE TABLE procedures (CPT int NOT NULL,name char(60),ORCC int, PRIMARY KEY (CPT, ORCC));
CREATE TABLE trays (Tray_id int NOT NULL,tray char(60),ORCC int NOT NULL,T_QTY int NOT NULL,PRIMARY KEY (Tray_id, ORCC));
CREATE TABLE instruments (id char(60) NOT NULL,instrument char(100),I_QTY int NOT NULL,Tray_id int,PRIMARY KEY (id, Tray_id));