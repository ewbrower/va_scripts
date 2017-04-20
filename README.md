The database is populated with scribe.py

This script requires the following csv tables:
* FullSurgery.csv
* trays.csv
* instruments.csv

These are stored in the "data" directory

---

The schedules are created with scheduler.py

This script requires the following information:
* a database initialized correctly with scribe.py
* block.csv
* depCPT.csv

You can increase the number of schedules created by making the "number" variable larger.

----
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