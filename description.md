# UTMC data explanation

This document provides initial guidance on using the data available at [http://butc.opendata.onl/AL_opendata] (http://butc.opendata.onl/AL_opendata)

## Basic Information

Most datasets have the following common columns:
-	SCN – System Code Number – a unique value for each asset (detector, carpark, incident, sign etc)
-	Description – an English language description (not always complete)
-	Northing and Easting – Ordance Survey Grid reference based on OSGB36 datum. Locations aren’t always available. Some are plotted in OSM with direction and lane information added. Python script available for finding this out.
-	LastUpdated – Timestamp
As the data is in a raw there are a number of unused columns, so this list just sets out the key fields from each one
Some data is sourced from Highways England and is available elsewhere.

## Live Data URLs 

*Updated every 5 minutes for most sources*

##### http://butc.opendata.onl/UTMC%20ANPR.xml (xml,json,xlsx,xls,csv,txt,htm)

-	TravelTime – traveltimein seconds over the Automatic Number Plate Recognition link.
-	SCN’s labelled ‘Wifi?’ are not ANPR but are created using mac address detection over wifi, and processed in the same way as number plates.
-	Very few of these are currently working due to SIM card issues. The Wifi is working, ‘JTMSTL19’ – is a good one to use for the ANPR.

##### http://butc.opendata.onl/UTMC%20AverageSpeed.xml (xml,json,xlsx,xls,csv,txt,htm

-	Value_Level shows average speed over last 5 mins. Note that ‘80’ is a default provided by internal system when data is not available. Cross check against ‘UTMC Flow’ to see if it’s a real one.

##### http://butc.opendata.onl/UTMC%20Congestion.xml (xml,json,xlsx,xls,csv,txt,htm)

-	Very few records in here. Value level shows congestion percentage.

##### http://butc.opendata.onl/UTMC%20Detector.xml (xml,json,xlsx,xls,csv,txt,htm)

-	Flow_Value and Speed_Value could be useful

##### http://butc.opendata.onl/UTMC%20Flow.xml (xml,json,xlsx,xls,csv,txt,htm)

-	Value_Level is traffic flow in last 5 minutes.

##### http://butc.opendata.onl/UTMC%20Incident.xml (xml,json,xlsx,xls,csv,txt,htm)

-	Automatically identified incidents.

##### http://butc.opendata.onl/UTMC%20Occupancy.xml (xml,json,xlsx,xls,csv,txt,htm)

-	Value_Level shows occupancy percentage

##### http://butc.opendata.onl/UTMC%20Parking.xml (xml,json,xlsx,xls,csv,txt,htm)

-	Information from car parking guidance signs. If Northing and Easting not available, then the information refers to a sign, not a car park.
-	Capacity is car park capacity in terms of number of spaces. Occupancy is the number of spaces currently in use.

##### http://butc.opendata.onl/UTMC%20Roadworks.xml (xml,json,xlsx,xls,csv,txt,htm)

-	Roadworks info from Highways England

##### http://butc.opendata.onl/UTMC%20Scoot.xml (xml,json,xlsx,xls,csv,txt,htm)

-	Amalgamation of other datasets.

##### http://butc.opendata.onl/UTMC%20TravelTime.xml (xml,json,xlsx,xls,csv,txt,htm)

-	Travel Time in seconds for Scoot and ANPR links. Scoot is derived.

##### http://butc.opendata.onl/UTMC%20VMS.xml (xml,json,xlsx,xls,csv,txt,htm)

-	MsgTxt is message shown on VMS sign.

##### http://butc.opendata.onl/UTMC%20VMSC.xml (xml,json,xlsx,xls,csv,txt,htm)

-	Messages shown on car park signs. Similar to UTMC Parking.

##### http://butc.opendata.onl/UTMC%20roadevent.xml (xml only)

-	Provides a standardised feed of road events. [Click for detailed info] (http://butc.opendata.onl/roadevent.xml?help=True) 

## Historic Data URLS

> *Only works as .xml.* e.g. http://butc.opendata.onl/UTMC%20Flow.xml?SCN=N13192A&TS=True&Earliest=25/10/2016&Latest=27/10/2016

The following parameters are required:-
-	?SCN=XXXXX (SCN identifies the individual asset (detector, carpark, sign etc)
-	&Earliest=dd/mm/yyyy (start date – fairly flexible as to the date format)
-	&Latest= dd/mm/yyyy (end date – fairly flexible as to the date format)
-	&TS=True (Time Series – needed to access historic data)
Note – historic data access can be quite slow. Historic data is only up to the end of the previous day.
