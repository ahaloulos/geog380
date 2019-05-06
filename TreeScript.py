##This script was produced by Anthony Haloulos and James Sensenbrenner
##In order for script to work ensure all directories are correct for the machine
import arcpy
from arcpy import env 
env.workspace = "C://arcgis//FinalProject"
env.OverwriteOutput= True

mxd = "C://arcgis//FinalProject//NYCMap.mxd"
fc = "geo_export_0891c82f-5864-4525-9206-763f9621c38b.shp"

#Ask for inputs regarding pathogen spread
##bufferspread = arcpy.GetParameterAsText(0)
##treetype = arcpy.GetParameterAsText(1)

#Hardcoded parameters for testing purposes
bufferspread = "25 METERS"
treetype = 'Norway maple'
count = 2

#Deletes existing files to enable an overwrite
if arcpy.Exists("Tree_sel.shp"):
    arcpy.Delete_management("Tree_sel.shp")
if arcpy.Exists("TreeZero_sel.shp"):
    arcpy.Delete_management("TreeZero_sel.shp")

#Process of identifying sick trees and trees we are targeting workaround for select by location
arcpy.Select_analysis (fc, "Tree_sel.shp", '"spc_common"= \'Norway maple\'')
arcpy.Select_analysis ("Tree_sel.shp", "TreeZero_sel.shp", '"health"= \'Poor\'')

#Deletes existing files to enable an overwrite
if arcpy.Exists("TreeZero_buff.shp"):
    arcpy.Delete_management("TreeZero_buff.shp")

#Creates bufferspread sized buffer around sick trees
arcpy.Buffer_analysis ("TreeZero_sel.shp", "TreeZero_buff.shp", bufferspread)

#Deletes existing files to enable an overwrite
if arcpy.Exists("SickTrees.shp"):
    arcpy.Delete_management("SickTrees.shp")

#Identifies trees within the spread
arcpy.Clip_analysis("Tree_sel.shp", "TreeZero_buff.shp", "SickTrees.shp")

#Deletes existing files to enable an overwrite
if arcpy.Exists("NewSickTrees.shp"):
    arcpy.Delete_management("NewSickTrees.shp")

#Identifies new trees that would be infected
arcpy.Erase_analysis("SickTrees.shp", "TreeZero_sel.shp", "NewSickTrees.shp")

#Loops to ensure number of iterations of pathogen spread are modeled
while count < 1:

    #Deletes existing files to enable an overwrite
    if arcpy.Exists("SickTree_buff.shp"):
        arcpy.Delete_management("SickTree_buff.shp")

    #buffers currently sick trees
    arcpy.Buffer_analysis ("SickTrees.shp", "SickTree_buff.shp", bufferspread)

    #Deletes existing files to enable an overwrite
    if arcpy.Exists("SickTrees2.shp"):
        arcpy.Delete_management("SickTrees2.shp")
    arcpy.Clip_analysis("Tree_sel.shp", "SickTree_buff.shp", "SickTrees2.shp")

    #Deletes existing files to enable an overwrite
    if arcpy.Exists("NewSickTrees2.shp"):
        arcpy.Delete_management("NewSickTrees2.shp")

    #Determines the most recently infected trees     
    arcpy.Erase_analysis("SickTrees2.shp", "SickTrees.shp", "NewSickTrees2.shp")

    #Decrement for the loop
    count = count - 1

#Mapping Procedure
mapdoc = arcpy.mapping.MapDocument(mxd)
lyrlist = arcpy.mapping.ListLayers(mapdoc)
#Creates map showing the base of NYC, the streets, the primary host trees and
# the would be most recently infected trees based on number of iterations
#Hides all other layers
for lyr in lyrlist:
    if lyr.name == "Roads":
        lyr.visible = True
    elif lyr.name == "Boroughs":
        lyr.visible = True
    elif lyr.name == "NewSickTrees2":
        lyr.visible = True
    elif lyr.name == "TreeZero_sel.shp":
        lyr.visible = True
    else:
        lyr.visible = False
mapdoc.save()
pdfPath = "C://arcgis//FinalProject//TreeMap.pdf"
#Deletes existing file and then creates PDF of finished map
if arcpy.Exists(pdfPath):
    arcpy.Delete_management(pdfPath)
arcpy.mapping.ExportToPDF(mapdoc, pdfPath)
del mapdoc
del lyrlist

#Completion Statement(Optional can be removed)
print "Great Success!"

