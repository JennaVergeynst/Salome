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

##---------------##
## Geometry ##
##---------------##0.

print("GEOMETRY TIME !")

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

# generation of front view NS and MS
# the origin is on the right bank of the channel

part1 = geompy.MakeSketcher("Sketcher:F 0 0:TT "+ str(L_box1) + " 0:TT " + str(L_box1) + " " + str(height_box1) + ":TT 0 0")
part2 = geompy.MakeSketcher("Sketcher:F "+ str(L_box1) + " 0:TT "+str(L_box1) + " " + str(height_box1) + ":TT " + str(L_box2) + " " + str(height_box2) + ":TT " + str(L_box2) + " 0")
part3 = geompy.MakeSketcher("Sketcher:F "+ str(L_box2) + " 0:TT "+str(L_box2) + " " + str(height_box3) + ":TT " + str(L_box3) + " " + str(height_box3) + ":TT " + str(L_box3) + " 0")

all2D = geompy.MakePartition([part1,part2,part3])
all2D = geompy.RemoveExtraEdges(all2D, True)
geompy.addToStudy(all2D ,"all2D")




