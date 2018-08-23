# E0 259: Data Analytics. Module 1: Mars Orbit.
# Ellipse Descent Module to be used for Question 3.
# Pulkit Singh, July 23 2018

import numpy as np
import math

#-------------------------------------------------------------------------------#

# Takes x-y coordinate matrix of different Mars locations, x-y coordinates of
# the second focus and the length of the major axis as input, and computes the
# cost by calculating:
# (sum of distances from focii - length of major axis)^2
def evaluateDistance(xMars, yMars, xFocus, yFocus, majorAxis):
	dist = []

	# calculating (distance to origin + distance to focus2 - major axis length)^2
	# for each (x, y) pair
	for i in range(len(xMars)):
		distOrigin = math.sqrt(math.pow(xMars[i], 2) + math.pow(yMars[i], 2))
		distFocus = math.sqrt(math.pow((xMars[i] - xFocus), 2) + math.pow((yMars[i] - yFocus), 2))
		dist.append(math.pow((distOrigin + distFocus - majorAxis), 2))

	# adding up all the square distances
	squareDist = sum(dist)
	return squareDist

#-------------------------------------------------------------------------------#

# Takes x-y coordinate matrix of different Mars locations, x-y coordinates of
# the second focus and the length of the major axis as input, and computes the
# gradient vector ([df/d(xFocus), df/d(yFocus), df/d(majorAxis)])
def computeGradient(xMars, yMars, xFocus, yFocus, majorAxis):

	dxFocus = []
	dyFocus = []
	dmajorAxis = []

	# df/d(xFocus) = (-2 * (xMars - xFocus) * evaluateDistance) / distFocus
	# df/d(yFocus) = (-2 * (yMars - yFocus) * evaluateDistance) / distFocus
	# df/d(majorAxis) = -2 * evaluateDistance

	# computing partial derivatives for each set of coordinates
	for i in range(len(xMars)):
		distOrigin = math.sqrt(math.pow(xMars[i], 2) + math.pow(yMars[i], 2))
		distFocus = math.sqrt(math.pow((xMars[i] - xFocus), 2) + math.pow((yMars[i] - yFocus), 2))
		dist = distOrigin + distFocus - majorAxis

		xDiff = xMars[i] - xFocus
		yDiff = yMars[i] - yFocus

		dxFocus.append((-2 * xDiff * dist) / distFocus)
		dyFocus.append((-2 * yDiff * dist) / distFocus)
		dmajorAxis.append(-2 * dist)

	# returning gradient vector
	gradient = [float(sum(dxFocus)), float(sum(dyFocus)), float(sum(dmajorAxis))]
	return gradient

#-------------------------------------------------------------------------------#

# Takes x-y coordinate matrix of different Mars locations, x-y coordinates of
# the second focus and the length of the major axis as input, and runs gradient
# descent to find the best fit ellipse. Returns the x-y coordinates of the found
# focus, and the length of the major axis of the ellipse.
def findEllipse(xMars, yMars, xf, yf, axis):
	
	# initialising alpha as the step value
	alpha = 0.001

	# initialising array to keep track of cost values in gradient descent
	cost = []

	# running gradient descent
	for i in range (10000):	
		# finding cost for given parameters
		squareDist = evaluateDistance(xMars, yMars, xf, yf, axis)
		#print("square dist"), squareDist

		# adding current cost to list of previous costs
		cost.append(squareDist)

		# finding gradient with parameter values a & b
		delta = computeGradient(xMars, yMars, xf, yf, axis)

		# updating parameter values
		xf   = xf - (alpha * delta[0])
		yf   = yf - (alpha * delta[1])
		axis = axis - (alpha * delta[2])

	return xf, yf, axis, cost

#-------------------------------------------------------------------------------#
