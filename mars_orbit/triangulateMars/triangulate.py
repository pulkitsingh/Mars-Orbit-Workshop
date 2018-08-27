# This modules triangulates the projections of Mars on the ecliptic plane.

# Developed by Pulkit Singh, Niheshkumar Rathod & Rajesh Sundaresan
# Copyright lies with the Robert Bosch Center for Cyber-Physical Systems,
# Indian Institute of Science, Bangalore, India.

#----------------------------------------------------------------------------#

# importing required modules
import csv
import math
import matplotlib.pyplot as plt

#----------------------------------------------------------------------------#

def loadData():
	""" Loads data contained in triangulation.csv, returns lists of Earth
	    locations and Mars angles.

	Parameters:
		none

	Returns:
		earthLocations (float list): list of x-y coordinates of Earth
		marsAngles (float list): list of angles to Mars from Earth locations

	"""
	tri = "triangulation.csv"
	fields = []                # text headings in csv file
	earthLocations = []        # Positions of Earth - [x, y] format (AU)
	marsAngles = []            # Angles to Mars from Earth (radians)

	# reading in triangulation csv file
	with open(tri, 'r') as trifile:
		triangulation = csv.reader(trifile)
		fields = triangulation.next()    # discarding text headings

		# creating list of Earth locations and Mars angles
		for row in triangulation:

			earthAngle = math.radians(float(row[4]) + (float(row[5])/60))
			xEarth = math.cos(earthAngle)
			yEarth = math.sin(earthAngle)
			earthLocations.append([xEarth, yEarth])

			marsAngle = math.radians(float(row[6]) + (float(row[7])/60))
			marsAngles.append(marsAngle)

	return earthLocations, marsAngles

#----------------------------------------------------------------------------#

def plotEarthLocations(earthLocations):
	""" Plots loaded Earth locations.

	Parameters:
		earthLocations (float list): list of x-y coordinates of Earth

	"""

	# creating a plot
	fig, ax = plt.subplots()

	# plotting the sun at the origin
	ax.plot(0, 0, 'yo', markersize=10, label="Sun")

	# plotting different locations of Earth
	xEarth, yEarth = [], []
	for location in earthLocations:
		xEarth.append(location[0])
		yEarth.append(location[1])

	ax.plot(xEarth, yEarth, 'bo', markersize=5, label="Earth Locations")

	ax.legend(fontsize='x-small')
	plt.show()


#----------------------------------------------------------------------------#


def findMars(earthLocation1, marsAngle1, earthLocation2, marsAngle2):
	""" Triangulates location of Mars from two earthLocations and marsAngles

	Parameters:
		earthLocation1 (float): first paired location
		marsAngle1 (float)    : first paried angle
		earthLocation2 (float): second paired location
		marsAngle2 (float)    : second paried angle

	Returns:
		marsLocation (float) : x-y coordinates of triangulated Mars location

	"""

	x1, y1 = earthLocation1       # coordinates of first earth location
	ma1 = marsAngle1			  # corresponding first angle to mars

	x2, y2 = earthLocation2       # coordinates of second earth location
	ma2 = marsAngle2			  # corresponding second angle to mars

	# trignometrically finding mars coordinates from paired observation
	xMars = ((y2 - y1 + (x1 * math.tan(ma1)) - (x2 * math.tan(ma2)))
			/ (math.tan(ma1) - math.tan(ma2)))

	yMars = ((x2 - x1 + (y1 * (1 / math.tan(ma1))) 
			- (y2 * (1 / math.tan(ma2)))) 
			/ ((1 / math.tan(ma1)) - (1 / math.tan(ma2))))

	marsLocation = [xMars, yMars]
	return marsLocation

#----------------------------------------------------------------------------#

def computeRadius(marsLocations):
	""" Computes the radius of the best-fit circle to triangulated Mars
		locations.

	Parameters:
		marsLocations (float list): list of x-y coordinates of Mars

	Returns:
		triangulatedRadius (float): radius of best-fit circle (in AU)

	"""

	# for each mars location, finding distances from origin 
	rMars = []	
	for i in range(len(marsLocations)):
		xMars, yMars = marsLocations[i]
		sqDist = math.pow(xMars, 2) + math.pow(yMars, 2)
		rMars.append(math.sqrt(sqDist))

	# finding average radius
	r = sum(rMars) / len(rMars)
	
	return r

#----------------------------------------------------------------------------#

def plotTriangulations(marsLocations, radius):
	""" Plots triangulated Mars locations and best-fit circle.

	Parameters:
		marsLocations (float list): list of x-y coordinates of Mars
		triangulatedRadius (float): radius of best-fit circle (in AU)

	"""

	# creating a plot
	fig, ax = plt.subplots()

	# plotting the sun at the origin
	ax.plot(0, 0, 'yo', markersize=12)

	# plotting the projections of Mars on the ecliptic plane
	xMars, yMars = [], []
	for location in marsLocations:
		mx, my = location
		xMars.append(mx)
		yMars.append(my)
	ax.plot(xMars, yMars, 'ro', markersize=5, label="Mars's Projection")

	if radius is not None:	
		# plotting best fit circle
		fit = plt.Circle((0,0), radius, color='g', fill=False,
			label="Best-fit circle")
		ax.add_artist(fit)
		s = "Best-fit radius = " + str(round(radius, 4))
		ax.text(0.75, -2, s, fontsize=7)

	# setting dimensions of the plot
	lim = 2.2
	ax.set_xlim(-lim, lim)
	ax.set_ylim(-lim, lim)
	ax.set_aspect('equal')
	ax.legend(fontsize='x-small')
	

	# function to show the plot
	plt.show()

#----------------------------------------------------------------------------#