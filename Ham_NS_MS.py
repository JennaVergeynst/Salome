# Copyright (C) BIOMATH - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Sophie Balemans <Sophie.Balemans@ugent.be>, februari 2016
'''
Notes on running this python script for salome automatically:
in the bash run the command:
	salome720 -t <pathToScript>
Where -t = TUI only
afterwards eyecute following command to kill all sleeping salome sessions
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

# y-coordinates of vertical planes intersecting for the inlet openings and sluice door
# NS (inlet raster - sluice - inlet raster)
y1 = -3
y2 = y1 - 3.60
y3 = -9.6
y4 = y3 - 16
y5 = y4 - 3
y6 = y5 - 3.60
# MS (inlet raster - sluice - inlest raster)
y7 = y6 - 2.80
y8 = y7 - 3.60
y9 = y3 -16 - 16
y10 = y9 - 16
y11 = y10 - 3 
y12 = y11 - 3.60
# DV
y16 = y10 - 29
y14 = y16 + 4 #protruding corner
y15 = y14 - 0.60
y17 = y15 - 2*4.90
y18 = y17 - 3.60
y19 = y18 - 24
y20 = y19 - 3.60
y21 = y20 - 2*4.90
y22 = y21 - 0.60
# tap
y13 = y16 + 11

# divide the front view in 4 parts: 2 triangles + 1 rectangle of MS and NS, 1 rectangle for protruding DV

"""
this part may be deleted
# left y coordinate of each part:
L_boy2 = -10.9 #skipped L_boy1: on the ground
L_boy3 = y16
L_boy4 = y22

# depth (z-co) of each part
height_boy1 = -4.6 #trapezium instead of triangle
height_boy2 = -7
height_boy3 = -7

# considered lenght of the upstream channel part
L_channel = 100

"""

# z (depth) coordinates of the intersecting horizontal planes
z_DV_up = -2.13
z_DV_down = -7.13 # = bottom of DV sluice

z_MS_NS_up = -1.39
z_MS_NS_down = -4.35

z_small_sluices = -5

# some other y-coordinates
y_NS_RB = -9.6
y_NS_LB = y_NS_RB - 16
y_MS_RB = y_NS_LB - 16
y_MS_LB = y_MS_RB - 16
y_DV_RR = y_MS_LB - 29
y_DV_RB = y_DV_RR - 10
y_DV_LB = y_DV_RB - 24
y_LB = y_DV_LB - 14

# some x-coordinates
x_MS_NS_cove = -13.7 # cove = inham
x_DV_extr = 71.65
x_DV_cove1 = x_DV_extr - 4.7
x_DV_cove2 = x_DV_cove1 - 9.4
x1_sidechannel = x_DV_extr + 43.60
x2_sidechannel = x1_sidechannel + 13.7


##---------------##
## Geometry ##
##---------------##
print ("Geometry construction ...")

# 1. start the geometry from aerial view: first define all points

p0 = geompy.MakeVertex(0, 0, 0)
p1 = geompy.MakeVertex(0, y_NS_RB, 0)
p2 = geompy.MakeVertex(-3, y_NS_RB, 0)
p3 = geompy.MakeVertex(-4.08, y_NS_RB+1.28, 0)
p4 = geompy.MakeVertex(x_MS_NS_cove, y_NS_RB+1.28, 0)
p5 = geompy.MakeVertex(x_MS_NS_cove, y_NS_RB, 0)
p6 = geompy.MakeVertex(-11.7, y_NS_RB - 8, 0)
p7 = geompy.MakeVertex(x_MS_NS_cove, y_NS_LB, 0)
p8 = geompy.MakeVertex(x_MS_NS_cove , y_NS_LB-1.28, 0)
p9 = geompy.MakeVertex(-4.08, y_NS_LB-1.28, 0)
p10 = geompy.MakeVertex(-3, y_NS_LB, 0)
p11 = geompy.MakeVertex(0, y_NS_LB, 0)

p12 = geompy.MakeVertex(0, y_MS_RB, 0)
p13 = geompy.MakeVertex(-3, y_MS_RB, 0)
p14 = geompy.MakeVertex(-4.08, y_MS_RB+1.28, 0)
p15 = geompy.MakeVertex(x_MS_NS_cove, y_MS_RB+1.28, 0)
p16 = geompy.MakeVertex(x_MS_NS_cove, y_MS_RB, 0)
p17 = geompy.MakeVertex(-11.7, y_MS_RB - 8, 0)
p18 = geompy.MakeVertex(x_MS_NS_cove, y_MS_LB, 0)
p19 = geompy.MakeVertex(x_MS_NS_cove , y_MS_LB-1.28, 0)
p20 = geompy.MakeVertex(-4.08, y_MS_LB-1.28, 0)
p21 = geompy.MakeVertex(-3, y_MS_LB, 0)
p22 = geompy.MakeVertex(0, y_MS_LB, 0)

p23 = geompy.MakeVertex(0, y_DV_RR, 0)
p24 = geompy.MakeVertex(46.55, y_DV_RR, 0)
p25 = geompy.MakeVertex(51.55, y_DV_RR+5, 0)
p26 = geompy.MakeVertex(x_DV_extr-6, y_DV_RR+5, 0) #6: estimated from map
p27 = geompy.MakeVertex(x_DV_extr-4.7, y_DV_RB+14, 0)
p28 = geompy.MakeVertex(x_DV_extr, y_DV_RB+14, 0)

p29 = geompy.MakeVertex(x_DV_extr, y_DV_RB, 0)
p30 = geompy.MakeVertex(x_DV_cove1, y_DV_RB, 0)
p31 = geompy.MakeVertex(x_DV_cove1, y_DV_RB + 2.85, 0)
p32 = geompy.MakeVertex(x_DV_cove2, y_DV_RB + 2.85, 0)
p33 = geompy.MakeVertex(x_DV_cove2, y_DV_RB, 0)
p34 = geompy.MakeVertex(x_DV_cove2, y_DV_LB, 0)
p35 = geompy.MakeVertex(x_DV_cove2, y_DV_LB - 2.85, 0)
p36 = geompy.MakeVertex(x_DV_cove1, y_DV_LB - 2.85, 0)
p37 = geompy.MakeVertex(x_DV_cove1, y_DV_LB, 0)
p38 = geompy.MakeVertex(x_DV_extr, y_DV_LB, 0)

p39 = geompy.MakeVertex(x_DV_extr, y_LB, 0)
p39_low = geompy.MakeVertex(x_DV_extr, y_LB, -5)
p44 = geompy.MakeVertex(x_DV_extr+218.875, y_DV_LB - 45, 0)
p44_low = geompy.MakeVertex(x_DV_extr+218.875, y_DV_LB - 45, -4)
p45 = geompy.MakeVertex(x_DV_extr+218.875, y_DV_LB + 135, 0)
p46 = geompy.MakeVertex(120, y_DV_LB + 135, 0) #120 AANPASSEN NR WERKELIJKE X!!!

# 2. make a closed polyline

poly = geompy.MakePolyline([p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, p21, p22, 
p23, p24, p25, p26, p27, p28, p29, p30, p31, p32, p33, p34, p35, p36, p37, p38, p39, p44, p45, p46, p0])

# 3. closed polyline becomes a face

groundface = geompy.MakeFace(poly, isPlanarWanted = True)
geompy.addToStudy(groundface, "groundface")

# 4. extend the face in z-direction (depth)

# create vectors along the ayes
Vx = geompy.MakeVectorDXDYDZ(1, 0, 0)
Vy = geompy.MakeVectorDXDYDZ(0, 1, 0)
Vz = geompy.MakeVectorDXDYDZ(0, 0, 1)

shape3D = geompy.MakePrismVecH(groundface, Vz, -7.13) # for now: take bottom of DV sluice as lowest point
geompy.addToStudy(shape3D, "shape3D")

# 5. cut the 3D-shape by use of horizontal and vertical planes

# intersect all horizontally by a plane to create inlet openings
def hor_planes(zco):
	return geompy.MakePlane(geompy.MakeVertex(0, 0, zco), Vz, 1000)
	
DV_up_intersect = hor_planes(z_DV_up)
DV_down_intersect = hor_planes(z_DV_down) #this also intersects bottom of DV sluice
MS_NS_up_intersect = hor_planes(z_MS_NS_up)
MS_NS_down_intersect = hor_planes(z_MS_NS_down)
small_sluices_intersect = hor_planes(z_small_sluices)
all3D = geompy.MakePartition([shape3D], [DV_up_intersect, DV_down_intersect, MS_NS_up_intersect, MS_NS_down_intersect, small_sluices_intersect])
geompy.addToStudy(all3D ,"all3D")

# intersect all vertically by a plane to create inlet openings

def vert_planes(yco):
	plane = geompy.MakePlane(geompy.MakeVertex(0, yco, 0), Vy, 1000)
	return plane
intersect_list = []
y_list = [y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15, y16, y17, y18, y19, y20, y21, y22]
for y in y_list:
	intersect_list.append(vert_planes(y))

all3D = geompy.MakePartition([all3D], intersect_list)
all3D = geompy.RemoveExtraEdges(all3D, True)
geompy.addToStudy(all3D ,"all3D")

#check if the generated shape is valid
print("Checking whether the created shape is valid")
IsValid = geompy.CheckShape(all3D)
if IsValid == 0:
    raise(RuntimeError, "Invalid geometry created")
else:
    print("Hurray! Created geometry is valid!")

# 6. locate faces to determine inlets and outlets

# outlet faces (intakes of the sluice filling): all intakes are split by horizontal intersects, so have to be grouped again

intake_NS_RB_1 = geompy.GetFaceNearPoint(all3D, geompy.MakeVertex(0, y1-0.5, z_MS_NS_up-0.5))
intake_NS_RB_2 = geompy.GetFaceNearPoint(all3D, geompy.MakeVertex(0, y1-0.5, z_MS_NS_down+0.5))
intake_NS_LB_1 = geompy.GetFaceNearPoint(all3D, geompy.MakeVertex(0, y5-0.5, z_MS_NS_up-0.5))
intake_NS_LB_2 = geompy.GetFaceNearPoint(all3D, geompy.MakeVertex(0, y5-0.5, z_MS_NS_down+0.5))
intakes_NS = geompy.CreateGroup(all3D, geompy.ShapeType["FACE"])
geompy.UnionList(intakes_NS, [intake_NS_RB_1, intake_NS_RB_2, intake_NS_LB_1, intake_NS_LB_2])
geompy.addToStudy(intakes_NS, "intakes_NS")

intake_MS_RB_1 = geompy.GetFaceNearPoint(all3D, geompy.MakeVertex(0, y7-0.5, z_MS_NS_up-0.5))
intake_MS_RB_2 = geompy.GetFaceNearPoint(all3D, geompy.MakeVertex(0, y7-0.5, z_MS_NS_down+0.5))
intake_MS_LB_1 = geompy.GetFaceNearPoint(all3D, geompy.MakeVertex(0, y11-0.5, z_MS_NS_up-0.5))
intake_MS_LB_2 = geompy.GetFaceNearPoint(all3D, geompy.MakeVertex(0, y11-0.5, z_MS_NS_down+0.5))
intakes_MS = geompy.CreateGroup(all3D, geompy.ShapeType["FACE"])
geompy.UnionList(intakes_MS, [intake_MS_RB_1, intake_MS_RB_2, intake_MS_LB_1, intake_MS_LB_2])
geompy.addToStudy(intakes_MS, "intakes_MS")

intake_DV_RB_1 = geompy.GetFaceNearPoint(all3D, geompy.MakeVertex(x_DV_extr, y15-0.5, z_DV_up-0.5))
intake_DV_RB_2 = geompy.GetFaceNearPoint(all3D, geompy.MakeVertex(x_DV_extr, y15-0.5, z_small_sluices+0.05))
intake_DV_RB_3 = geompy.GetFaceNearPoint(all3D, geompy.MakeVertex(x_DV_extr, y15-0.5, z_DV_down+0.5))

intake_DV_RB_4 = geompy.GetFaceNearPoint(all3D, geompy.MakeVertex(x_DV_extr, y16-0.5, z_DV_up-0.5))
intake_DV_RB_5 = geompy.GetFaceNearPoint(all3D, geompy.MakeVertex(x_DV_extr, y16-0.5, z_small_sluices+0.05))
intake_DV_RB_6 = geompy.GetFaceNearPoint(all3D, geompy.MakeVertex(x_DV_extr, y16-0.5, z_DV_down+0.5))

intake_DV_LB_1 = geompy.GetFaceNearPoint(all3D, geompy.MakeVertex(x_DV_extr, y20-0.5, z_DV_up-0.5))
intake_DV_LB_2 = geompy.GetFaceNearPoint(all3D, geompy.MakeVertex(x_DV_extr, y20-0.5, z_small_sluices+0.05))
intake_DV_LB_3 = geompy.GetFaceNearPoint(all3D, geompy.MakeVertex(x_DV_extr, y20-0.5, z_DV_down+0.5))

intake_DV = geompy.CreateGroup(all3D, geompy.ShapeType["FACE"]) # create a group on all3D which will contain faces
geompy.UnionList(intake_DV, [intake_DV_RB_1, intake_DV_RB_2, intake_DV_RB_3, intake_DV_RB_4, intake_DV_RB_5, intake_DV_RB_6, intake_DV_LB_1, intake_DV_LB_2, intake_DV_LB_3]) # put in the group: 2 parts of the intake
geompy.addToStudy(intake_DV, "intake_DV")

# intake of the turbine side channel

# inlet face: upstream part
inlet_upstream = geompy.CreateGroup(all3D, geompy.ShapeType["FACE"]) 
geompy.UnionList(inlet_upstream, geompy.GetShapesOnPlaneWithLocation(all3D, geompy.ShapeType["FACE"], Vx, geompy.MakeVertex(x_DV_extr+218.875, -0.05, -0.05), GEOM.ST_ON))
geompy.addToStudy(inlet_upstream, "inlet_upstream")

#wall_left = geompy.CreateGroup(all3D, geompy.ShapeType["FACE"]) 
#geompy.UnionList(wall_left, geompy.GetShapesOnQuadrangle(all3D, geompy.ShapeType["FACE"], p39, p44, geompy.MakeVertex(x_DV_extr+100, y_LB, -5), geompy.MakeVertex(x_DV_extr+218.875, y_DV_LB - 45, -5), GEOM.ST_ON))
wall_left = geompy.MakePlaneThreePnt(p39, p44, p39_low, 400)
geompy.addToStudy(wall_left, "wall_left")

# x/z coordinates on wall_left plane:
xx40 = 44 #p40
xx43 = xx40+13.85 #p44
zzhigh = 0.3
zzlow = 4.46

intake_sidechannel = geompy.MakeSketcherOnPlane("Sketcher:F "+str(xx40)+" "+str(zzhigh)+" :TT "+str(xx43)+" "+str(zzhigh)+" :TT "+str(xx43)+" "+str(zzlow)+" :TT "+str(xx40)+" "+str(zzlow)+" :TT "+str(xx40)+" "+str(zzhigh)+" :WF", wall_left)
geompy.addToStudy(intake_sidechannel, "intake_sidechannel")
#quaIn = geompy.MakeSketcher("Sketcher:F -" + str_rad_2 + " -" + str_rad_2 + ":TT -" + str_rad_2 + " " + str_rad_2 + ":TT " + str_rad_2 + " " + str_rad_2 + ":TT " + str_rad_2 + " -" + str_rad_2 + ":WF")


