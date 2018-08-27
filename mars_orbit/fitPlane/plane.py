""" This module locates Mars on the celestial sphere and fits a plane to 
	these positions using gradient descent.
"""

# Developed by Pulkit Singh, Niheshkumar Rathod & Rajesh Sundaresan
# Copyright lies with the Robert Bosch Center for Cyber-Physical Systems,
# Indian Institute of Science, Bangalore, India.

#----------------------------------------------------------------------------#

import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# importing custom module to run gradient descent on mars orbital plane
import planeGradientDescent

#----------------------------------------------------------------------------#

def loadData():
	""" Loads data contained in opposition.csv, returns lists of heliocentric
		Mars longitudes and geocentric Mars latitudes.

	Parameters:
		none

	Returns:
		helioLong (float list): list of heliocentric Mars longitudes
		geoLat (float list): list of geocentric Mars latitudes

	"""
	opp = "opposition.csv"
	fields = []        # text headings in csv file
	helioLong = []     # heliocentric longitude of Mars (in radians)
	geoLat = []        # geocentric latitude of Mars (in radians)

	# reading in opposition csv file
	with open(opp, 'r') as oppfile:
		opposition = csv.reader(oppfile)
		fields = opposition.next()

		# creating list of heliocentric longitudes and geocentric latitudes
		for row in opposition:

			# Computing heliocentric longitudes (in radians)
			helioLong.append(math.radians((30 * float(row[3])) + float(row[4]) 
				+ (float(row[5])/60) + (float(row[6])/3600)))

			# Computing geocentric latitudes (in radians)
			geoLat.append(math.radians(float(row[7]) + (float(row[8])/60)))

	return helioLong, geoLat

#----------------------------------------------------------------------------#

def findHelioLat(radius, geoLat):
	""" Finds heliocentric Mars latitudes from geocentric Mars latitudes.

	Parameters:
		radius (float): radius of best-fit circle to Mars triangulations
		geoLat (float list): list of geocentric Mars latitudes

	Returns:
		helioLat (float list): list of heliocentric Mars latitudes

	"""

	helioLat = []
	scale = (radius - 1)/radius
	for angle in geoLat:
		helioLat.append(math.atan(scale * math.tan(angle)))

	return helioLat

#----------------------------------------------------------------------------#

def findCoordinates(helioLong, helioLat):
	""" Finds coordinates of Mars on the Celestial Sphere from heliocentric
		latitudes and longitudes.

	Parameters:
		helioLong (float list): list of heliocentric Mars longitudes
		helioLat  (float list): list of heliocentric Mars latitudes
		
	Returns:
		coordinates (float list): list of x-y-z coordinates of Mars on the
								  celestial sphere

	"""
	xMars = []
	yMars = []
	zMars = []

	# Given the radius of celestial sphere, latitude and longitude of mars, 
	# we have spherical coordinates of Mars.
	# Spherical coordinates can be converted to cartesian using the formula:
	# 	x = radius * cos(pi/2 - latitude) * cos(longitude)
	# 	y = radius * sin(pi/2 - latitude) * sin(longitude)
	#   z = radius * cos(pi/2 - latitude)
	for i in range(len(helioLat)):
		xMars.append(math.sin((math.pi / 2.0)-helioLat[i]) 
					* math.cos(helioLong[i]))
		yMars.append(math.sin((math.pi / 2.0)-helioLat[i]) 
					* math.sin(helioLong[i]))
		zMars.append(math.cos((math.pi / 2.0)-helioLat[i]))

	coordinates = [xMars, yMars, zMars]
	return coordinates

#----------------------------------------------------------------------------#

def fitPlane(coordinates):
	""" Fits a plane to the coordinates of Mars on the celestial sphere.

	Parameters:
		coordinates (float list): list of x-y-z coordinates of Mars on the
					celestial sphere.
		
	Returns:
		planeParameters (float list): coefficients (a,b) of x and y for a 
					plane with equation ax + by + z = 0

	"""
	planeParameters = planeGradientDescent.findPlane(coordinates)
	return planeParameters

#----------------------------------------------------------------------------#

def plotPlane(coordinates, planeParams):
	""" Plots coordinates of Mars on the celestial sphere and the best-fit
		plane to these coordinates.

	Parameters:
		coordinates (float list): list of x-y-z coordinates of Mars on the
					celestial sphere.
		planeParameters (float list): coefficients (a,b) of x and y for a 
					plane with equation ax + by + z = 0

	"""


	# unpacking necessary parameters
	a, b = planeParams
	xMars, yMars, zMars = coordinates

	# creating a figure
	fig = plt.figure()
	ax = Axes3D(fig)

	# plotting Mars's locations on the celestial sphere
	ax.scatter(xMars, yMars, zMars, 'r')
	ax.scatter(0.0, 0.0, 0.0, 'y')

	# plotting mars's best-fit orbital plane
	point = np.array([0.0, 0.0, 0.0])
	normal = np.array([a, b, 1.0])
	d = -point.dot(normal)
	xx, yy = np.meshgrid(range(-2, 3), range(-2, 3))
	zm = (-normal[0] * xx - normal[1] * yy - d) * 1. /normal[2]
	ax.plot_surface(xx, yy, zm, alpha=0.2, color='b',
		label="Mars Orbital Plane")

	# plotting the ecliptic plane
	ze = yy * 0.0
	ax.plot_surface(xx, yy, ze, alpha=0.2, color='y', label="Ecliptic Plane")

	plt.show()

#----------------------------------------------------------------------------#

def findInclination(planeParams):
	""" Calculate angle between Ecliptic plane and best-fit Mars orbital 
		plane.

	Parameters:
		planeParameters (float list): coefficients (a,b) of x and y for a 
					plane with equation ax + by + z = 0

	Returns:
		Angle of Inclination of Mars Orbital plane

	"""

	a, b = planeParams
	angle = math.acos(1/(math.sqrt(math.pow(a, 2) + math.pow(b, 2) + 1.0)))
	return math.degrees(angle)

#----------------------------------------------------------------------------#
