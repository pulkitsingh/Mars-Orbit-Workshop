![Header Image](./images/into.jpg)

## Introduction

This project contains the material to conduct a workshop recreating Kepler's breakthrough discovery of the elliptical orbit of Mars, intended for a high school audience. The workshop is designed to give the students a deeper undersanding of the physical concepts, along with a flavor of data analytics. 

## Workshop Design
The approach for this workshop comes from a graduate data-analytics class taught by Professor Rajesh Sundaresan and Professor Ramesh Hariharan at the Indian Institute of Science, Bangalore, India. The Mars Orbit module from this class was adapted for the session, by simplifying and black-boxing the computational approach. This enabled high-school students to understand the conceptual elements, and use the modules they were provided to perform relatively complex computations. This was done during the course of my internship from June - August 2018, under the guidance of Professor Sundaresan and Niheshkumar Rathod, at the Robert Bosch Center for Cyber-Physical Systems, Indian Institute of Science, Bangalore, India.

There are two main parts of the project:
- The Jupyter notebook designed to guide the students through hands-on programming activities.
- The Python package that modularises all the need computational and plotting requirement for the workshop.

## Using the Material

A quick fork of the repository will give you access to the Jupyter notebook and python package. Launch the Jupyter notebook with the program of your choice, and you should be guided into the programming activities. 

Please contact Pulkit Singh (pulkit@princeton.edu) or Professor Rajesh Sundaresan (rajeshs@iisc.ac.in) if you intend to use this material to conduct a workshop or in any non-personal use.

## Jupyter Notebook

The noteboook contains three programming activities that are designed to be interspersed with explanation. Here is a brief summary of the design:

1. **Part 1**: Triangulating the projections of Mars on the Ecliptic Plane
2. **Part 2**: Finding the locations of Mars on the Celestial Sphere and fitting a plane the locations using gradient descent.
3. **Part 3**: Lifting the projections found in Part 1 onto the plane found in Part 2. Then, fitting a circle and an ellipse for the orbit in order to determine which one provides a better fit to the data.

## Python Package

The python package corresponds to the parts of the programming exercise contained in the Jupyter notebook. It contains the following three subpackage directories:
- triangualateMars
- fitPlane
- fitOrbit

The code is documented appropriately and the specifics of the package functionality can be accessed using pydoc or any other tool of your choice.

## Feedback

If you see something that can be improved, please direct your feedback to Pulkit Singh (pulkit@princeton.edu)

 


