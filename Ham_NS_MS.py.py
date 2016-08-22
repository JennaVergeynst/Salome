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

# depth (z-co) of each part
height_box1 = -4.65 #triangle
height_box2 = -7
height_box3 = -7

# considered lenght of the upstream channel part
L_channel = 100

# z (depth) coordinates of the intersecting horizontal planes
upper_DV = -0.75 # upper level of DV intake
middle_NS_MS = -1.39 # upper level of NS and MS intake
lower_all = -4.35 # lower level of all intakes
sluice_bottom = -5
# another horizontal plane needed to intersect at the point where the angle of the RB changes
triangle_cut = -4.65

# x-coordinates of vertical planes intersecting for the inlet openings and sluice door
# NS (inlet raster - sluice - inlet raster)
x1 = -8.475
x2 = x1 - 3.60
x3 = -15.075
x4 = x3 - 16
x5 = x4 - 3
x6 = x5 - 3.60
# MS (inlet raster - sluice - inlest raster)
x7 = x6 - 2.80
x8 = x7 - 3.60
x9 = -16 - 16 - 15.075
x10 = x9 - 16
x11 = x10 - 3 
x12 = x11 - 3.60
# DV (RB inlet raster) !!!dimensions probably not correct!!!
x13 = x12 - 3.10 
x14 = x13 - 4.40


##---------------##
## Geometry ##
##---------------##
print ("Geometry construction ...")

# make the workingplane of sketcher: the OZX plane (= 3)
XZ_plane = geompy.MakeFaceHW(100, 500, 3)

# generation of front view NS and MS
# MakeSketcher creates the edges, MakeFace fills them to a face
# the origin is on the right bank of the channel

part1 = geompy.MakeSketcherOnPlane("Sketcher:F 0 0:TT 0 "+ str(L_box1) + ":TT " + str(height_box1)+ " " + str(L_box1)  + ":TT 0 0", XZ_plane)
part1_2D = geompy.MakeFace(part1, 1)
part2= geompy.MakeSketcherOnPlane("Sketcher:F 0 "+ str(L_box1) + " :TT "+ str(height_box1) + " " +str(L_box1) + ":TT "  + str(height_box2) + " " + str(L_box2)+ ":TT 0 " + str(L_box2) + ":TT 0 " + str(L_box1), XZ_plane)
part2_2D = geompy.MakeFace(part2, 1)
part3 = geompy.MakeSketcherOnPlane("Sketcher:F 0 "+ str(L_box2) + " :TT "+ str(height_box3) + " " +str(L_box2) + ":TT " + str(height_box3) + " " + str(L_box3) + ":TT 0 " + str(L_box3) + ":TT 0 " + str(L_box2), XZ_plane)
part3_2D = geompy.MakeFace(part3, 1)

# add all faces together (via partition, but nothing is cut out here)
all2D = geompy.MakeCompound([part1_2D,part2_2D,part3_2D])
all2D = geompy.RemoveExtraEdges(all2D, True)


# create vectors along the axes
Vx = geompy.MakeVectorDXDYDZ(1, 0, 0)
Vy = geompy.MakeVectorDXDYDZ(0, 1, 0)
Vz = geompy.MakeVectorDXDYDZ(0, 0, 1)

# rotate all2D 180 around z-axis
all2D = geompy.MakeRotation(all2D, Vz, math.pi)
geompy.addToStudy(all2D ,"all2D")

# extrude the front view over the lenght of the study site
all3D = geompy.MakePrismVecH(all2D, Vy, -L_channel)

# intersect all horizontally by a plane to create inlet openings
def hor_planes(zco):
	return geompy.MakePlane(geompy.MakeVertex(0, 0, zco), Vz, 200)
	
upper_DV_intersect = hor_planes(upper_DV)
middle_intersect = hor_planes(middle_NS_MS)
lower_intersect = hor_planes(lower_all)
sluice_bottom_intersect = hor_planes(sluice_bottom)
triangle_intersect = hor_planes(triangle_cut)
all3D = geompy.MakePartition([all3D], [upper_DV_intersect, middle_intersect, lower_intersect, sluice_bottom_intersect, triangle_intersect])
geompy.addToStudy(all3D ,"all3D")


# intersect all vertically by a plane to create inlet openings

def vert_planes(xco):
	plane = geompy.MakePlane(geompy.MakeVertex(xco, 0, 0), Vx, 200)
	return plane
intersect_list = []
x_list = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14]
for x in x_list:
	intersect_list.append(vert_planes(x))

all3D = geompy.MakePartition([all3D], intersect_list)
geompy.addToStudy(all3D ,"all3D")

# add simplified sluice forms
NS = geompy.MakeBoxTwoPnt(geompy.MakeVertex(x3, 0, 0), geompy.MakeVertex(x4, 11.70, sluice_bottom))
MS = geompy.MakeBoxTwoPnt(geompy.MakeVertex(x9, 0, 0), geompy.MakeVertex(x10, 11.70, sluice_bottom))
geompy.addToStudy(NS, "NS")
geompy.addToStudy(MS, "MS")


compound = geompy.MakeCompound([all3D, NS, MS])
compound = geompy.MakeGlueFaces(compound,10**-7,1)
geompy.addToStudy(compound, "compound")

#

# locate faces to determine inlets and outlets

# faces below are the outlet faces (intake of the sluice filling)
intake_NS_RB = geompy.GetFaceNearPoint(compound, geompy.MakeVertex(x1+0.5, 0, middle_NS_MS-0.5))
geompy.addToStudy(intake_NS_RB, "intake_NS_RB")
intake_NS_LB = geompy.GetFaceNearPoint(compound, geompy.MakeVertex(x5+0.5, 0, middle_NS_MS-0.5))
intake_MS_RB = geompy.GetFaceNearPoint(compound, geompy.MakeVertex(x7+0.5, 0, middle_NS_MS-0.5))
intake_MS_LB = geompy.GetFaceNearPoint(compound, geompy.MakeVertex(x11+0.5, 0, middle_NS_MS-0.5))



#check if the generated shape is valid
print("Checking whether the created shape is valid")
IsValid = geompy.CheckShape(all3D)
if IsValid == 0:
    raise(RuntimeError, "Invalid geometry created")
else:
    print("Hurray! Created geometry is valid!")



	
