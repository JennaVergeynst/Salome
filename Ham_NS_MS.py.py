# Copyright (C) BIOMATH - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Sophie Balemans <Sophie.Balemans@ugent.be>, februari 2016
'''
Notes on running this python script for salome automatically:
in the bash run the command:
	salome720 -t <pathToScript>
Where -t = TUI only
afterwards execute following command to kill all sleeping salome sessions
	salome720 --killall
'''
####----------####
#### Preamble ####
####----------####

#importing necessary libraries and defining functions
#SINGLE IMPELLER WITH INLET AND OUTLET
import salome
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)
gg = salome.ImportComponentGUI("GEOM")

import SMESH, SALOMEDS
from salome.smesh import smeshBuilder
smesh =  smeshBuilder.New(salome.myStudy)

import math
import GEOM



####--------------------####
#### Printing the intro ####
####--------------------####

print ("\nHere we go...\n")

##-----------##
## Functions ##
##-----------##

def PrintMeshInfo(theMesh):
        aMesh = theMesh.GetMesh()
        print("Mesh description", aMesh.Dump())
        pass

##-----------##
## Constants ##
##-----------##
print ("Reading in constants ...")

# left x coordinate of each part:
L_box1 = 5.2
L_box2 = 14.30
L_box3 = 81.075

# height of each part
height_box1 = 4.65 #triangle
height_box2 = 7
height_box3 = 7

# considered lenght of the upstream channel part
L_channel = 100

# y (depth) coordinates of the intersecting horizontal planes
upper_DV = 0.75
middle_NS_MS = 1.39
lower_all = 4.35
# another horizontal plane needed to intersect at the point where the angle of the RB changes
triangle_cut = 4.65

# x-coordinates of vertical planes intersecting for the inlet openings and sluice door
# NS (inlet raster - sluice - inlet raster)
x1 = 8.475
x2 = x1 + 3.60
x3 = 15.075
x4 = x3 + 16
x5 = x4 + 3
x6 = x5 + 3.60
# MS (inlet raster - sluice - inlest raster)
x7 = x6 + 2.80
x8 = x7 + 3.60
x9 = 16 + 16 + 15.075
x10 = x9 + 16
x11 = x10 + 3 
x12 = x11 + 3.60
# DV (RB inlet raster)
x13 = x12 + 3.10 
x14 = x13 + 4.40


##---------------##
## Geometry ##
##---------------##
print ("Geometry construction ...")

# generation of front view NS and MS
# MakeSketcher creates the edges, MakeFace fills them to a face
# the origin is on the right bank of the channel

part1 = geompy.MakeSketcher("Sketcher:F 0 0:TT "+ str(L_box1) + " 0:TT " + str(L_box1) + " " + str(height_box1) + ":TT 0 0")
part1_2D = geompy.MakeFace(part1, 1)
part2= geompy.MakeSketcher("Sketcher:F "+ str(L_box1) + " 0:TT "+str(L_box1) + " " + str(height_box1) + ":TT " + str(L_box2) + " " + str(height_box2) + ":TT " + str(L_box2) + " 0:TT " + str(L_box1) + " 0")
part2_2D = geompy.MakeFace(part2, 1)
part3 = geompy.MakeSketcher("Sketcher:F "+ str(L_box2) + " 0:TT "+str(L_box2) + " " + str(height_box3) + ":TT " + str(L_box3) + " " + str(height_box3) + ":TT " + str(L_box3) + " 0:TT " + str(L_box2) + " 0")
part3_2D = geompy.MakeFace(part3, 1)

# add all faces together (via partition, but nothing is cut out here)
all2D = geompy.MakePartition([part1_2D,part2_2D,part3_2D])
all2D = geompy.RemoveExtraEdges(all2D, True)

geompy.addToStudy(all2D ,"all2D")


# create 2 points defining a vector in upstream direction (100 m lenght considered)
p1 = geompy.MakeVertex( 0., 0., 0.)
p2 = geompy.MakeVertex( 0., 0., L_channel)

# extrude the front view over the lenght of the study site
all3D = geompy.MakePrism(all2D, p1, p2)
geompy.addToStudy(all3D ,"all3D")

# intersect all horizontally by a plane to create inlet openings
normal_vec = geompy.MakeVector(p1, geompy.MakeVertex(0, 1, 0))
upper_DV_intersect = geompy.MakePlane(geompy.MakeVertex(0, upper_DV, 0), normal_vec, 200)
middle_intersect = geompy.MakePlane(geompy.MakeVertex(0, middle_NS_MS, 0), normal_vec, 200)
lower_intersect = geompy.MakePlane(geompy.MakeVertex(0, lower_all, 0), normal_vec, 200)
all3D = geompy.MakePartition([all3D], [upper_DV_intersect, middle_intersect, lower_intersect])


	

# intersect all vertically by a plane to create inlet openings
normal_vec2 = geompy.MakeVector(p1, geompy.MakeVertex(1, 0, 0))

def vert_planes(xco):
	plane = geompy.MakePlane(geompy.MakeVertex(xco, 0, 0), normal_vec2, 200)
	return plane
intersect_list = []
x_list = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14]
for x in x_list:
	intersect_list.append(vert_planes(x))

all3D = geompy.MakePartition([all3D], intersect_list)

print
geompy.addToStudy(all3D ,"all3D")

