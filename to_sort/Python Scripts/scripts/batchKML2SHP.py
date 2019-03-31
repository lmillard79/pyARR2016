# Name: BatchKML_to_GDB.py
# Description: Converts a directory of KMLs and copies the output into a single fGDB.
#              A 2 step process: first convert the KML files, and then copy the featureclases

# Import system models
import arcpy, os, sys

### workspacefolder = sys.argv[1]
### outputfolder = sys.argv[2]

# Set workspace (where all the KMLs are)
arcpy.env.workspace=sys.argv[1]

# Set local variables and location for the consolidated file geodatabase
outLocation = sys.argv[2]
MasterGDB = 'AllKMLLayers.gdb'
MasterGDBLocation = os.path.join(outLocation, MasterGDB)

# Create the master FileGeodatabase
arcpy.CreateFileGDB_management(outLocation, MasterGDB)

# Convert all KMZ and KML files found in the current workspace
for kmz in arcpy.ListFiles('*.KM*'):
  print "CONVERTING: " + os.path.join(arcpy.env.workspace,kmz)
  arcpy.KMLToLayer_conversion(kmz, outLocation)

 # ***arcpy.KMLToLayer_conversion(r'V:\KML\rv_stn.kmz',r'V:\KML')

# Change the workspace to fGDB location
arcpy.env.workspace = outLocation

# Loop through all the FileGeodatabases within the workspace
wks = arcpy.ListWorkspaces('*', 'FileGDB')
# Skip the Master GDB
wks.remove(MasterGDBLocation)

for fgdb in wks:  
     
  # Change the workspace to the current FileGeodatabase
  arcpy.env.workspace = fgdb    

  # For every Featureclass inside, copy it to the Master and use the name from the original fGDB  
  featureClasses = arcpy.ListFeatureClasses('*', '', 'Placemarks')
  for fc in featureClasses:
    print "COPYING: " + fc + " FROM: " + fgdb    
    fcCopy = fgdb + os.sep + 'Placemarks' + os.sep + fc    
    arcpy.FeatureClassToFeatureClass_conversion(fcCopy, MasterGDBLocation, fgdb[fgdb.rfind(os.sep)+1:-4])
  

# Clean up
del kmz, wks, fc, featureClasses, fgdb