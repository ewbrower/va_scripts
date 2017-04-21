
# VAMC Surgical Goods Flow

## Populating the Database
The database is populated with scribe.py

This script requires the following csv tables:
* FullSurgery.csv
* trays.csv
* instruments.csv

These are stored in the "data" directory

## Creating Schedules
The schedules are created with scheduler.py

This script requires the following information:
* a database initialized correctly with scribe.py
* block.csv
* depCPT.csv

You can increase the number of schedules created by making the "number" variable larger.

## Data Directory

FullSurgery.csv
This csv describes the links between the surgery and the case carts needed to fulfill the surgery.

trays.csv
This csv describes the trays required to support a particular surgical procedure.

instruments.csv
This csv links trays and their component instruments.

block.csv
This is a block schedule.

depCPT.csv
This csv lists the frequency of a surgery given it's department.

## Integer Program

Block Schedule CSV Writer.py
This code renders a GUI through which a user can create new blocked schedules in the appropriate format.

Fast IP.mos
This integer program produces inventory minimums while running at the highest rate of tray processing time.

Practical IP.mos
This integer program produces inventory minimums while running at the most practical rate of tray processing time.

Slow IP.mos
This integer program produces inventory minimums while running at the observed worst case rate of tray processing time

Fast IP with costs.mos
Practical IP with costs.mos
Slow IP with costs.mos

These are versions of the runnable integer programs that have placeholders for tray cost.






