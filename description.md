# UTMC Data Explanation

This document provides initial guidance on using the data available at [http://butc.opendata.onl/AL_opendata](http://butc.opendata.onl/AL_opendata)

## Basic Information

Most datasets have the following common columns:
-	**SCN** – System Code Number – a unique value for each asset (detector, carpark, incident, sign etc.)
-	**Description** – an English language description (not always complete)
-	**Northing and Easting** – Ordance Survey Grid reference based on OSGB36 datum. Locations aren’t always available. Some are plotted in OSM with direction and lane information added. Python script available for finding this out.
-	**LastUpdated** – Timestamp

As the data is in a raw there are a number of unused columns, so this list just sets out the key fields from each one
Some data is sourced from Highways England and is available elsewhere.

## Live Data URLs 

*Updated every 5 minutes for most sources*

#### ANPR - http://butc.opendata.onl/UTMC%20ANPR.xml 
([XML](http://butc.opendata.onl/UTMC%20ANPR.xml), [JSON](http://butc.opendata.onl/UTMC%20ANPR.json), [XLSX](http://butc.opendata.onl/UTMC%20ANPR.xlsx), [XLS](http://butc.opendata.onl/UTMC%20ANPR.xls), [CSV](http://butc.opendata.onl/UTMC%20ANPR.csv), [TXT](http://butc.opendata.onl/UTMC%20ANPR.txt), [HTM](http://butc.opendata.onl/UTMC%20ANPR.htm))

-	**TravelTime** – travel time in seconds over the Automatic Number Plate Recognition link.
-	SCN’s labelled ‘Wifi?’ are not ANPR but are created using mac address detection over wifi, and processed in the same way as number plates.
-	Very few of these are currently working due to SIM card issues. The Wifi is working, ‘JTMSTL19’ – is a good one to use for the ANPR.

#### Average Speed - http://butc.opendata.onl/UTMC%20AverageSpeed.xml 
([XML](http://butc.opendata.onl/UTMC%20AverageSpeed.xml), [JSON](http://butc.opendata.onl/UTMC%20AverageSpeed.json), [XLSX](http://butc.opendata.onl/UTMC%20AverageSpeed.xlsx), [XLS](http://butc.opendata.onl/UTMC%20AverageSpeed.xls), [CSV](http://butc.opendata.onl/UTMC%20AverageSpeed.csv), [TXT](http://butc.opendata.onl/UTMC%20AverageSpeed.txt), [HTM](http://butc.opendata.onl/UTMC%20AverageSpeed.htm))

-	**Value_Level** shows average speed over last 5 mins. Note that ‘80’ is a default provided by internal system when data is not available. Cross check against ‘UTMC Flow’ to see if it’s a real one.

#### Congestion  - http://butc.opendata.onl/UTMC%20Congestion.xml 
([XML](http://butc.opendata.onl/UTMC%20Congestion.xml), [JSON](http://butc.opendata.onl/UTMC%20Congestion.json), [XLSX](http://butc.opendata.onl/UTMC%20Congestion.xlsx), [XLS](http://butc.opendata.onl/UTMC%20Congestion.xls), [CSV](http://butc.opendata.onl/UTMC%20Congestion.csv), [TXT](http://butc.opendata.onl/UTMC%20Congestion.txt), [HTM](http://butc.opendata.onl/UTMC%20Congestion.htm))

-	Very few records in here. Value level shows congestion percentage.

#### Detector - http://butc.opendata.onl/UTMC%20Detector.xml 
([XML](http://butc.opendata.onl/UTMC%20Detector.xml), [JSON](http://butc.opendata.onl/UTMC%20Detector.json), [XLSX](http://butc.opendata.onl/UTMC%20Detector.xlsx), [XLS](http://butc.opendata.onl/UTMC%20Detector.xls), [CSV](http://butc.opendata.onl/UTMC%20Detector.csv), [TXT](http://butc.opendata.onl/UTMC%20Detector.txt), [HTM](http://butc.opendata.onl/UTMC%20Detector.htm))

-	**Flow_Value** and **Speed_Value** could be useful

#### Flow - http://butc.opendata.onl/UTMC%20Flow.xml 
([XML](http://butc.opendata.onl/UTMC%20Flow.xml), [JSON](http://butc.opendata.onl/UTMC%20Flow.json), [XLSX](http://butc.opendata.onl/UTMC%20Flow.xlsx), [XLS](http://butc.opendata.onl/UTMC%20Flow.xls), [CSV](http://butc.opendata.onl/UTMC%20Flow.csv), [TXT](http://butc.opendata.onl/UTMC%20Flow.txt), [HTM](http://butc.opendata.onl/UTMC%20Flow.htm))

-	**Value_Level** is traffic flow in last 5 minutes.

#### Incident - http://butc.opendata.onl/UTMC%20Incident.xml 
([XML](http://butc.opendata.onl/UTMC%20Incident.xml), [JSON](http://butc.opendata.onl/UTMC%20Incident.json), [XLSX](http://butc.opendata.onl/UTMC%20Incident.xlsx), [XLS](http://butc.opendata.onl/UTMC%20Incident.xls), [CSV](http://butc.opendata.onl/UTMC%20Incident.csv), [TXT](http://butc.opendata.onl/UTMC%20Incident.txt), [HTM](http://butc.opendata.onl/UTMC%20Incident.htm))

-	Automatically identified incidents.

#### Occupancy - http://butc.opendata.onl/UTMC%20Occupancy.xml 
([XML](http://butc.opendata.onl/UTMC%20Occupancy.xml), [JSON](http://butc.opendata.onl/UTMC%20Occupancy.json), [XLSX](http://butc.opendata.onl/UTMC%20Occupancy.xlsx), [XLS](http://butc.opendata.onl/UTMC%20Occupancy.xls), [CSV](http://butc.opendata.onl/UTMC%20Occupancy.csv), [TXT](http://butc.opendata.onl/UTMC%20Occupancy.txt), [HTM](http://butc.opendata.onl/UTMC%20Occupancy.htm))

-	**Value_Level** shows occupancy percentage

#### Parking - http://butc.opendata.onl/UTMC%20Parking.xml 
([XML](http://butc.opendata.onl/UTMC%20Parking.xml), [JSON](http://butc.opendata.onl/UTMC%20Parking.json), [XLSX](http://butc.opendata.onl/UTMC%20Parking.xlsx), [XLS](http://butc.opendata.onl/UTMC%20Parking.xls), [CSV](http://butc.opendata.onl/UTMC%20Parking.csv), [TXT](http://butc.opendata.onl/UTMC%20Parking.txt), [HTM](http://butc.opendata.onl/UTMC%20Parking.htm))

-	Information from car parking guidance signs. If Northing and Easting not available, then the information refers to a sign, not a car park.
-	Capacity is car park capacity in terms of number of spaces. Occupancy is the number of spaces currently in use.

#### Roadworks - http://butc.opendata.onl/UTMC%20Roadworks.xml 
([XML](http://butc.opendata.onl/UTMC%20Roadworks.xml), [JSON](http://butc.opendata.onl/UTMC%20Roadworks.json), [XLSX](http://butc.opendata.onl/UTMC%20Roadworks.xlsx), [XLS](http://butc.opendata.onl/UTMC%20Roadworks.xls), [CSV](http://butc.opendata.onl/UTMC%20Roadworks.csv), [TXT](http://butc.opendata.onl/UTMC%20Roadworks.txt), [HTM](http://butc.opendata.onl/UTMC%20Roadworks.htm))

-	Roadworks info from Highways England

#### SCOOT - http://butc.opendata.onl/UTMC%20Scoot.xml 
([XML](http://butc.opendata.onl/UTMC%20Scoot.xml), [JSON](http://butc.opendata.onl/UTMC%20Scoot.json), [XLSX](http://butc.opendata.onl/UTMC%20Scoot.xlsx), [XLS](http://butc.opendata.onl/UTMC%20Scoot.xls), [CSV](http://butc.opendata.onl/UTMC%20Scoot.csv), [TXT](http://butc.opendata.onl/UTMC%20Scoot.txt), [HTM](http://butc.opendata.onl/UTMC%20Scoot.htm))

-	Amalgamation of other datasets.

#### Travel Time - http://butc.opendata.onl/UTMC%20TravelTime.xml 
([XML](http://butc.opendata.onl/UTMC%20TravelTime.xml), [JSON](http://butc.opendata.onl/UTMC%20TravelTime.json), [XLSX](http://butc.opendata.onl/UTMC%20TravelTime.xlsx), [XLS](http://butc.opendata.onl/UTMC%20TravelTime.xls), [CSV](http://butc.opendata.onl/UTMC%20TravelTime.csv), [TXT](http://butc.opendata.onl/UTMC%20TravelTime.txt), [HTM](http://butc.opendata.onl/UTMC%20TravelTime.htm))

-	**Travel Time** in seconds for Scoot and ANPR links. Scoot is derived.

#### VMS - http://butc.opendata.onl/UTMC%20VMS.xml 
([XML](http://butc.opendata.onl/UTMC%20VMS.xml), [JSON](http://butc.opendata.onl/UTMC%20VMS.json), [XLSX](http://butc.opendata.onl/UTMC%20VMS.xlsx), [XLS](http://butc.opendata.onl/UTMC%20VMS.xls), [CSV](http://butc.opendata.onl/UTMC%20VMS.csv), [TXT](http://butc.opendata.onl/UTMC%20VMS.txt), [HTM](http://butc.opendata.onl/UTMC%20VMS.htm))

-	**MsgTxt** is message shown on VMS sign.

#### VMSC - http://butc.opendata.onl/UTMC%20VMSC.xml 
([XML](http://butc.opendata.onl/UTMC%20VMSC.xml), [JSON](http://butc.opendata.onl/UTMC%20VMSC.json), [XLSX](http://butc.opendata.onl/UTMC%20VMSC.xlsx), [XLS](http://butc.opendata.onl/UTMC%20VMSC.xls), [CSV](http://butc.opendata.onl/UTMC%20VMSC.csv), [TXT](http://butc.opendata.onl/UTMC%20VMSC.txt), [HTM](http://butc.opendata.onl/UTMC%20VMSC.htm))

-	Messages shown on car park signs. Similar to UTMC Parking.

#### Road Events - http://butc.opendata.onl/UTMC%20roadevent.xml 
([XML](http://butc.opendata.onl/UTMC%20roadevent.xml) only)

-	Provides a standardised feed of road events. [Click for detailed info.](http://butc.opendata.onl/roadevent.xml?help=True) 

## Historic Data URLS

*Only works as .xml.* 
e.g. http://butc.opendata.onl/UTMC%20Flow.xml?SCN=N13192A&TS=True&Earliest=25/10/2016&Latest=27/10/2016

The following parameters are required:
-	**?SCN=XXXXX** - SCN identifies the individual asset (detector, carpark, sign etc)
-	**&Earliest=dd/mm/yyyy** - start date – fairly flexible as to the date format
-	**&Latest=dd/mm/yyyy** - end date – fairly flexible as to the date format-
-	**&TS=True** - Time Series – needed to access historic data
Note – historic data access can be quite slow. Historic data is only up to the end of the previous day.
