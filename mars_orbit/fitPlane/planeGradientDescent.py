# E0 259: Data Analytics. Module 1: Mars Orbit.
# Gradient Descent Module to be used for Question 2.
# Pulkit Singh, July 19 2018

import numpy as np
import math

#-------------------------------------------------------------------------------#

# Takes x-y-z coordinate matrix and guesses for slope parameters a, b.
# Computes squared euclidian distance from points (x, y, z) to plane
# defined by ax + by + z = 0.
# Squared Distance = sum(((ax + by + z)/(a^2 + b^2 + 1))^2)
def evaluateDistance(coordinates, a, b):

	# creating normal vector for plane
	normal = np.array([a, b, 1.0])[:,None]

	# calculating scale (a^2 + b^2 + 1)
	scale = math.pow(a, 2) + math.pow(b, 2) + 1.0

	# calculating distance = coordinate matrix * normal vector
	distance = np.dot(coordinates, normal) / scale

	# calculating and returning sum of square distances
	squareDist = float(sum(distance ** 2))
	return squareDist

#-------------------------------------------------------------------------------#

# Takes x-y-z coordinate matrix and guesses for slope parameters a, b.
# Computes gradient vector of squaredDistance function(as defined above)
# Returns ([ df/da, df/db ])
def computeGradient(coordinates, a, b):

	# creating normal vector for plane
	normal = np.array([a, b, 1.0])[:,None]

	# calculating scale (a^2 + b^2 + 1)
	scale = math.pow(a, 2) + math.pow(b, 2) + 1.0

	# linearSum = ax + by + z
	linearSum = np.dot(coordinates, normal)

	# calculating the partial derivatives with respect to a and b

	scaledX = np.array([coordinates[:, 0] * scale]).T  # scaled x-coordinates
	scaledY = np.array([coordinates[:, 1] * scale]).T  # scaled y-coordinates
	partialScale = (2 / (math.pow(scale, 3)))          # partial deriv scale

	# computing values of derivatives
	partialA = partialScale * ((-2 * a * linearSum) + scaledX) * linearSum
	partialB = partialScale * ((-2 * b * linearSum) + scaledY) * linearSum 

	# returning a gradient vector
	gradient = [float(sum(partialA)), float(sum(partialB))]
	return gradient

#-------------------------------------------------------------------------------#
