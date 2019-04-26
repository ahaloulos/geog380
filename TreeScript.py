import arcpy
from arcpy import env 
env.workspace = "C://argis//treeproject"

#Ask for inputs regarding pathogen spread 
#Make list of sick target trees through data
#Make buffer around each ill tree in the list, will require another loop
#Update sick tree list with target trees in buffer 
#somehow have looping mechanism that will iterate through lines 7 and 8 until desired number of iterations is reached. 
#In final iteration make list of target trees that would in harms way on last iteration called trees of interest
# Create points of interest by copying the points from trees of interest
#Use mapping features to plot trees of interest and buffers.
#output map and save as pdf
