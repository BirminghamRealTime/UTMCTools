# coding: utf-8

import requests
try:
	from lxml import etree as ET
except ImportError:
	import xml.etree.cElementTree as ET
import math
import time
import pickle
import os.path
import json
from datetime import datetime, timedelta
from math import sqrt, pi, sin, cos, tan, atan2 as arctan2


def calculate_initial_compass_bearing(pointA, pointB):
	"""
	Calculates the bearing between two points.
	The formulae used is the following:
	θ = atan2(sin(Δlong).cos(lat2),
	cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
	:Parameters:
	- `pointA: The tuple representing the latitude/longitude for the
	first point. Latitude and longitude must be in decimal degrees
	- `pointB: The tuple representing the latitude/longitude for the
	second point. Latitude and longitude must be in decimal degrees
	:Returns:
	The bearing in degrees
	:Returns Type:
	float
	"""
	if (type(pointA) != tuple) or (type(pointB) != tuple):
		raise TypeError("Only tuples are supported as arguments")

	lat1 = math.radians(pointA[0])
	lat2 = math.radians(pointB[0])

	diffLong = math.radians(pointB[1] - pointA[1])

	x = math.sin(diffLong) * math.cos(lat2)
	y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
										   * math.cos(lat2) * math.cos(diffLong))

	initial_bearing = math.atan2(x, y)

	# Now we have the initial bearing but math.atan2 return values
	# from -180° to + 180° which is not what we want for a compass bearing
	# The solution is to normalize the initial bearing as shown below
	initial_bearing = math.degrees(initial_bearing)
	compass_bearing = (initial_bearing + 360) % 360

	return compass_bearing


def OSGB36toWGS84(E, N):
	# E, N are the British national grid coordinates - eastings and northings
	a = 6377563.396
	b = 6356256.909
	# The Airy 180 semi-major and semi-minor axes used for OSGB36 (m)
	F0 = 0.9996012717
	lat0 = 49 * pi / 180
	lon0 = -2 * pi / 180
	N0, E0 = -100000, 400000
	e2 = 1 - (b * b) / (a * a)
	n = (a - b) / (a + b)

	# Initialise the iterative variables
	lat, M = lat0, 0

	while N - N0 - M >= 0.00001:
		lat = (N - N0 - M) / (a * F0) + lat;
		M1 = (1 + n + (5. / 4) * n ** 2 + (5. / 4) * n ** 3) * (lat - lat0)
		M2 = (3 * n + 3 * n ** 2 + (21. / 8) * n ** 3) * sin(lat - lat0) * cos(lat + lat0)
		M3 = ((15. / 8) * n ** 2 + (15. / 8) * n ** 3) * sin(2 * (lat - lat0)) * cos(2 * (lat + lat0))
		M4 = (35. / 24) * n ** 3 * sin(3 * (lat - lat0)) * cos(3 * (lat + lat0))
		# meridional arc
		M = b * F0 * (M1 - M2 + M3 - M4)

	# transverse radius of curvature
	nu = a * F0 / sqrt(1 - e2 * sin(lat) ** 2)

	# meridional radius of curvature
	rho = a * F0 * (1 - e2) * (1 - e2 * sin(lat) ** 2) ** (-1.5)
	eta2 = nu / rho - 1

	secLat = 1. / cos(lat)
	VII = tan(lat) / (2 * rho * nu)
	VIII = tan(lat) / (24 * rho * nu ** 3) * (5 + 3 * tan(lat) ** 2 + eta2 - 9 * tan(lat) ** 2 * eta2)
	IX = tan(lat) / (720 * rho * nu ** 5) * (61 + 90 * tan(lat) ** 2 + 45 * tan(lat) ** 4)
	X = secLat / nu
	XI = secLat / (6 * nu ** 3) * (nu / rho + 2 * tan(lat) ** 2)
	XII = secLat / (120 * nu ** 5) * (5 + 28 * tan(lat) ** 2 + 24 * tan(lat) ** 4)
	XIIA = secLat / (5040 * nu ** 7) * (61 + 662 * tan(lat) ** 2 + 1320 * tan(lat) ** 4 + 720 * tan(lat) ** 6)
	dE = E - E0

	# These are on the wrong ellipsoid currently: Airy1830. (Denoted by _1)
	lat_1 = lat - VII * dE ** 2 + VIII * dE ** 4 - IX * dE ** 6
	lon_1 = lon0 + X * dE - XI * dE ** 3 + XII * dE ** 5 - XIIA * dE ** 7

	# Want to convert to the GRS80 ellipsoid.
	# First convert to cartesian from spherical polar coordinates
	H = 0
	x_1 = (nu / F0 + H) * cos(lat_1) * cos(lon_1)
	y_1 = (nu / F0 + H) * cos(lat_1) * sin(lon_1)
	z_1 = ((1 - e2) * nu / F0 + H) * sin(lat_1)

	# Perform Helmut transform (to go between Airy 1830 (_1) and GRS80 (_2))
	s = -20.4894 * 10 ** -6
	tx, ty, tz = 446.448, -125.157, + 542.060
	rxs, rys, rzs = 0.1502, 0.2470, 0.8421
	rx, ry, rz = rxs * pi / (180 * 3600.), rys * pi / (180 * 3600.), rzs * pi / (180 * 3600.)
	x_2 = tx + (1 + s) * x_1 + (-rz) * y_1 + (ry) * z_1
	y_2 = ty + (rz) * x_1 + (1 + s) * y_1 + (-rx) * z_1
	z_2 = tz + (-ry) * x_1 + (rx) * y_1 + (1 + s) * z_1

	# Back to spherical polar coordinates from cartesian
	# Need some of the characteristics of the new ellipsoid
	a_2, b_2 = 6378137.000, 6356752.3141
	e2_2 = 1 - (b_2 * b_2) / (a_2 * a_2)
	p = sqrt(x_2 ** 2 + y_2 ** 2)

	# Lat is obtained by an iterative proceedure:
	lat = arctan2(z_2, (p * (1 - e2_2)))
	latold = 2 * pi
	while abs(lat - latold) > 10 ** -16:
		lat, latold = latold, lat
		nu_2 = a_2 / sqrt(1 - e2_2 * sin(latold) ** 2)
		lat = arctan2(z_2 + e2_2 * nu_2 * sin(latold), p)

	# Lon and height are then pretty easy
	lon = arctan2(y_2, x_2)
	H = p / cos(lat) - nu_2

	# Convert to degrees
	lat = lat * 180 / pi
	lon = lon * 180 / pi

	# Job's a good'n.
	return lat, lon


def findsensordirection(bbox=(-2.1691, 52.3088, -1.5930, 52.6801), update=3600):
	"""
	Return the direction of traffic sensors as an angle
	:param tuple bbox: (startlat,startlon,endlat,endlon): bounding box for the sensors in question
	:param int update: time in seconds to update data from source rather than cached local file (default 3600)
	:return: dict bearinglookup: a dictionary whose keys are SCN numbers and values are: "OSM Way ID"(int),"Sensor bearing"(int, -1 if not available),"Lanes covered" (int, -1 if not available),"Lane numbers":(list first item is -1 if not available),"Total lanes":(int, -1 if not available)
	"""
	# download all the ways with sensors from overpass API
	# if the cache exists and it's datestamp is within the last week and the bbox is the same, then load the cache and retun. remember to add no-cache tag
	bearinglookup = {}
	usecache='no'
	if os.path.isfile('bearingcache.json'):
		if int(time.time()-os.path.getmtime('bearingcache.json'))<update:
			usecache='yes'
	if usecache=='no':
		url = "http://www.overpass-api.de/api/xapi?way[bbox=" + str(bbox[0]) + "," + str(bbox[1]) + "," + str(bbox[2]) + "," + str(bbox[3]) + "][sensor_ref:lanes=*]"
		getdata = requests.get(url)
		root = ET.fromstring(getdata.content)
		# find the start and end nodes of a way
		allways = root.findall('way')
		for way in allways:
			startway = "none"
			currentway = "none"
			endway = "none"
			sensorreflanes = "none"
			startlat = 0
			startlon = 0
			endlat = 0
			endlon = 0
			# find the node reference for the start node of the way (startway) and the end node (endway)
			for tag in way.findall('nd'):
				if startway == "none":
					startway = tag.get('ref')
					currentway = startway
				else:
					currentway = tag.get('ref')
			endway = currentway
			# get the attributes for the sensor from the way tag
			# We also need lanes:backward lanes:forward and direction=oneway (and maybe sensor:ref:lanes:forward)
			# and also just lanes so we know the total and divide by 2 for our first guess.
			# If there are no lanes, then we put in 2 or 1 for oneway
			lanesno=-1
			lanesbackward=-1
			lanesforward=-1
			oneway="No"
			rdnm=""
			for tag in way.findall('tag'):
				if tag.get('k') == 'sensor_ref:lanes':
					sensorreflanes = tag.attrib['v']
				if tag.get('k') == 'lanes':
					lanesno = int(tag.attrib['v'])
				if tag.get('k') == 'lanes:backward':
					lanesbackward = int(tag.attrib['v'])
				if tag.get('k') == 'lanes:forward':
					lanesforward = int(tag.attrib['v'])
				#add the sensor lanes backward and forward, which is an odd use case
				if tag.get('k') == 'oneway':
					oneway= tag.attrib['v']
				if tag.get('k') == 'name':
					rdnm=tag.attrib['v']
			#so we can actually do most of the logic here
			#if lanesno=-1 then it's oneway therefore lanes forward= lanes no and lanes backward=0
			#if there's no lanesforward or backward then it's lanesforward=lanes/2 and lanesbackward=lanes/2
			#if lanesforward exists but not lanesbackward then its lanesbackward=lanes - lanesforward
			#if lanesbackward exists but not lanesforward then its lanesforward=lanes-lanesbackward
			if lanesno==-1 and oneway=="yes":
				lanesno=1
				lanesforward=1
				lanesbackward=0
			elif lanesno==-1:
				lanesno=2
			elif oneway=="yes":
				lanesforward=lanesno
				lanesbackward=0   
			if lanesbackward==-1 and lanesforward==-1:
				lanesforward=int(lanesno/2)
				lanesbackward=lanesno-lanesforward
			elif lanesbackward==-1:
				lanesbackward=lanesno-lanesforward
			elif lanesforward==-1:
				lanesforware=lanesno-lanesbackward
			allnodes = root.findall('node')
			# get the locations of the start and end nodes
			for node in allnodes:
				if startway == node.get('id'):
					startlat = node.attrib['lat']
					startlon = node.attrib['lon']
				if endway == node.get('id'):
					endlat = node.attrib['lat']
					endlon = node.attrib['lon']
			pointA = (float(startlat), float(startlon))
			pointB = (float(endlat), float(endlon))
			# calculate the bearings
			bearing = calculate_initial_compass_bearing(pointA, pointB)
			# split the sensor information into lanes
			newlist = sensorreflanes.split('|')
			if lanesno != len(newlist):
				print way.attrib, len(newlist), lanesno, sensorreflanes, rdnm
				currval = "none"
				for n in newlist:    #remember this loop somehow manages to take 2 different loops if they are there and maybe even more
					if n == "no":
						bearing = bearing + 180
						if bearing > 360:
							bearing = bearing - 360
					if currval == "none":
						if n <> "no":
							# print n, bearing
							bearinglookup[n] = {"OSM Way ID":int(way.attrib['id']),"Sensor bearing":bearing,"Lanes covered":-1,"Lane numbers":[-1],"Total lanes":-1}
							currval = n
					if n <> currval:
						if n <> "no":
							bearing = bearing + 180
							if bearing > 360:
								bearing = bearing - 360
								# print n, bearing
								bearinglookup[n] = {"OSM Way ID":int(way.attrib['id']),"Sensor bearing":bearing,"Lanes covered":-1,"Lane numbers":[-1],"Total lanes":-1} #so extend this to cover all the columns that we need
								currval = n
			# Need to count here to see if lanes (or the lack of lanes) is the same at the split
			# if not print something to the console (or even a spreadsheet called osmerrors?
			# then do a 'bestguess routine' which is basically lanes are foward while they are the same but lanes are different when they swap.
			# wont work for all use cases but that's not my fault.
			#{"OSM Way ID":int(way.attrib['id']),"Sensor bearing":bearing,"Lanes covered":-1,"Lane numbers":[-1],"Total lanes":-1]
			else:
				for n in range(lanesforward):
					if newlist[n]<>"no":
						if newlist[n]in bearinglookup:
							if bearinglookup[newlist[n]]["Lane numbers"][-1]<=n:
								bearinglookup[newlist[n]]["Lanes covered"]+=1
								bearinglookup[newlist[n]]["Lane numbers"].append(n+1)
						else:
							bearinglookup[newlist[n]]={"OSM Way ID":int(way.attrib['id']),"Sensor bearing":bearing,"Lanes covered":1,"Lane numbers":[n+1],"Total lanes":lanesforward}
				bearing = bearing + 180
				if bearing > 360:
					bearing = bearing - 360
				for n in range(lanesbackward):  #0-3
					rn=(lanesno-(lanesbackward-n)) #8-(0-n)
					if newlist[rn]<>"no":
						if newlist[rn]in bearinglookup:
							if bearinglookup[newlist[rn]]["Lane numbers"][-1]<=n:
								bearinglookup[newlist[rn]]["Lanes covered"]+=1
								bearinglookup[newlist[rn]]["Lane numbers"].append(n+1)
						else:
							bearinglookup[newlist[rn]]={"OSM Way ID":int(way.attrib['id']),"Sensor bearing":bearing,"Lanes covered":1,"Lane numbers":[n+1],"Total lanes":lanesbackward}
			# so actually return node = osm way id[0], bearing[1], lanes covered [2], whichlanes (1,2,3,4), total lanes
			# serialise bearinglookup here to save having to do this processing in future....
		with open('bearingcache.json','wb')as handle:
			json.dump(bearinglookup,handle)
	else:
		with open('bearingcache.json','rb')as handle:
			bearinglookup=json.load(handle)
	print bearinglookup
	return bearinglookup

def allcurrentsensordata(url="http://butc.opendata.onl/UTMC flow.xml",bbox=(-2.1691, 52.3088, -1.5930, 52.6801),update=300):
	"""
	Return the information currently working traffic sensors
	:param str url: url of the sesnsor data
	:param tuple bbox: (startlat,startlon,endlat,endlon): bounding box for the sensors in question
	:param int update: time in seconds to update data from source rather than cached local file (default 300)
	:return: dict sensorreturn: a dictionary whose keys are SCN numbers and values are dictionaries of "Location", "Traffic flow", "Latitude", "Longitude","Sensor bearing","Compass Direction","OSM Way ID":,"Lanes covered", "Lane numbers","Total lanes"
	"""
	bearinglookup = findsensordirection()
	sensorreturn={}
	usecache='no'
	if os.path.isfile('sensorcache.json'):
		if int(time.time()-os.path.getmtime('sensorcache.json'))<update:
			usecache='yes'
	if usecache=='no':
		# Download current flow data from the adaptor logic site
		z = 0 #working sensor counter
		y = 0 #unfound co-ordinate counter
		x = datetime.now()
		print x
		x = x - timedelta(days=1)  # age of data to get rid of
		r = requests.get(url)
		print len(r.content)
		# Download the node information from Overpass (we could probably reuse the way stuff from earlier)
		root = ET.fromstring(r.content)
		urlosm = "http://www.overpass-api.de/api/xapi?node[bbox=" + str(bbox[0]) + "," + str(bbox[1]) + "," + str(bbox[2]) + "," + str(bbox[3]) + "][monitoring=traffic]"
		rosm = requests.get(urlosm)
		rootosm = ET.fromstring(rosm.content)
		allnodesosm = rootosm.findall('node')

		# Get rid of all the data that is older than a day
		for flow in root.iter('Flow'):

			timestamp = datetime.strptime(flow[4].text, '%Y-%m-%d %H:%M:%S')
			if timestamp > x:
				scnno = flow[0].text
				z += 1
				easting = float(flow[3].text)
				northing = float(flow[3].text)
				lat, lon = 0, 0
				# convert easting and northing to WGS84 if data available, otherwise get it from openstreetmap
				if easting <> 0:
					lat, lon = OSGB36toWGS84(float(flow[3].text), float(flow[2].text))
				else:
					for node in allnodesosm:
						for tag in node.findall('tag'):
							if tag.get('k') == 'traffic:sensor:ref':
								foundtag = tag.attrib['v']
								if foundtag == scnno:
									lat = node.get('lat')
									lon = node.get('lon')
				# write it all down nicely, with bearing if we have one. This will go into a nice datastructure for upload (later). I also add some cheeky generalisation of the bearing.
				if lat <> 0:
					if scnno in bearinglookup:
						if (bearinglookup[scnno]["Sensor bearing"] > 22.5 and bearinglookup[scnno]["Sensor bearing"] < 67.5):
							genbearing = "NE"
						elif (bearinglookup[scnno]["Sensor bearing"] > 67.5 and bearinglookup[scnno]["Sensor bearing"] < 112.5):
							genbearing = "E"
						elif (bearinglookup[scnno]["Sensor bearing"] > 112.5 and bearinglookup[scnno]["Sensor bearing"] < 157.5):
							genbearing = "SE"
						elif (bearinglookup[scnno]["Sensor bearing"] > 157.5 and bearinglookup[scnno]["Sensor bearing"] < 202.5):
							genbearing = "S"
						elif (bearinglookup[scnno]["Sensor bearing"] > 202.5 and bearinglookup[scnno]["Sensor bearing"] < 247.5):
							genbearing = "SW"
						elif (bearinglookup[scnno]["Sensor bearing"] > 247.5 and bearinglookup[scnno]["Sensor bearing"] < 292.5):
							genbearing = "W"
						elif (bearinglookup[scnno]["Sensor bearing"] > 292.5 and bearinglookup[scnno]["Sensor bearing"] < 337.5):
							genbearing = "NW"
						else:
							genbearing = "N"
						#{"OSM Way ID":int(way.attrib['id']),"Sensor bearing":bearing,"Lanes covered":1,"Lane numbers":[n+1],"Total lanes":lanesforward}
						sensorreturn[scnno]={"Location":flow[4].text, "Traffic flow":int(flow[5][0].text),"Latitude": lat, "Longitude":lon, "Sensor bearing":int(bearinglookup[scnno]["Sensor bearing"]), "Compass direction":genbearing, "OSM Way ID":bearinglookup[scnno]["OSM Way ID"], "Lanes covered":bearinglookup[scnno]["Lanes covered"],"Lane numbers":bearinglookup[scnno]["Lane numbers"],"Total lanes":bearinglookup[scnno]["Total lanes"]}
					else:
						sensorreturn[scnno]= {"Location":flow[4].text, "Traffic flow":int(flow[5][0].text), "Latitude":lat, "Longitude":lon,"Sensor bearing": -1,"Compass Direction":"Unknown","OSM Way ID": -1,"Lanes covered": -1,"Lane numbers":[-1],"Total lanes":-1}
				else:
					y = y + 1
		print "working detectors", z
		print "unfound co-ordinates", y
		with open('sensorcache.json','wb')as handle:
			json.dump(sensorreturn,handle)
	else:
		with open('sensorcache.json','rb')as handle:
			sensorreturn=json.load(handle)
	return sensorreturn

if __name__=="__main__":
	print allcurrentsensordata()

#possible helper files
#1. any duplicate scn's (i.e. same number on different ways)
#2. ways with lanes that don't match number of sensors
