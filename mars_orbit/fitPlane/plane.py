# This module locates Mars on the celestial sphere and fits a plane to these
# positions using gradient descent.

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

	helioLat = []
	scale = (radius - 1)/radius
	for angle in geoLat:
		helioLat.append(math.atan(scale * math.tan(angle)))

	return helioLat

#----------------------------------------------------------------------------#

def findCoordinates(helioLong, helioLat):
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

	# creating coordinate matrix: [x, y, z]
	coordinateMatrix = np.array(coordinates).T

	# initalizing guesses for plane parameters a and b to be 0.0
	a, b = 0.0, 0.0

	# initialising alpha as the step value
	alpha = 0.0001

	# initialising array to keep track of cost values in gradient descent
	cost = []

	# running gradient descent
	for i in range (10000):
		
		# finding cost for given parameter values a & b
		squareDist = planeGradientDescent.evaluateDistance(coordinateMatrix, a, b)

		# adding current cost to list of previous costs
		cost.append(squareDist)
		
		# finding gradient with parameter values a & b
		delta = planeGradientDescent.computeGradient(coordinateMatrix, a, b)
		
		# updating parameter values
		a = a - (alpha * delta[0])
		b = b - (alpha * delta[1])

	# Final parameters of the plane
	planeParams = [a, b]

	return planeParams

#----------------------------------------------------------------------------#

def plotPlane(coordinates, planeParams):

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

	plt.savefig("planePlot.png")

#----------------------------------------------------------------------------#

def findInclination(planeParams):
	a, b = planeParams
	angle = math.acos(1/(math.sqrt(math.pow(a, 2) + math.pow(b, 2) + 1.0)))
	return math.degrees(angle)

#----------------------------------------------------------------------------#
