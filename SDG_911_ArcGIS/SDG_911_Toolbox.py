# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# SDG_911_Toolbox_publication.py
# Created on: 2019-04-30 10:07:59.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: SDG_911_Toolbox_publication <Input_Country_Boundaries> <Input_Global_Rural_Population_Raster> <Input_Roads> <Output_Table> 
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

# Load required toolboxes
arcpy.ImportToolbox("Model Functions")

# Script arguments
Input_Country_Boundaries = arcpy.GetParameterAsText(0)
if Input_Country_Boundaries == '#' or not Input_Country_Boundaries:
    Input_Country_Boundaries = "D:\\SDG_911\\SDG_911.gdb\\Country_Reproject\\gadm_Region1_reproject" # provide a default value if unspecified

Input_Global_Rural_Population_Raster = arcpy.GetParameterAsText(1)
if Input_Global_Rural_Population_Raster == '#' or not Input_Global_Rural_Population_Raster:
    Input_Global_Rural_Population_Raster = "D:\\SDG_911\\GHS_population\\GHS_POP_RURAL_Clip.tif" # provide a default value if unspecified

Input_Roads = arcpy.GetParameterAsText(2)
if Input_Roads == '#' or not Input_Roads:
    Input_Roads = "D:\\SDG_911\\GRIP_raw\\GRIP4_region1_Rural.shp" # provide a default value if unspecified

Output_Table = arcpy.GetParameterAsText(3)
if Output_Table == '#' or not Output_Table:
    Output_Table = "D:\\SDG_911\\SDG_911.gdb\\SDG_911_output" # provide a default value if unspecified

# Local variables:
Value__2_ = "1"
Iterator_Country_Output = "I_gadm_Region1_reproject_ISO"
Clipped_Rural_Population_Count = "D:\\SDG_911\\SDG_911.gdb\\Clipped_Rural_Population_Count"
rural_pop = "D:\\SDG_911\\SDG_911.gdb\\rural_pop"
Joined_table = rural_pop
Roads_Clip = "D:\\SDG_911\\SDG_911.gdb\\Intermediate_data\\Road_CLIP"
Road_Buffer_1 = "D:\\SDG_911\\SDG_911.gdb\\Intermediate_data\\Road_CLIP_buffer1"
Road_Buffer_2 = "D:\\SDG_911\\SDG_911.gdb\\Intermediate_data\\Road_CLIP_buffer2"
Road_Buffer_3 = "D:\\SDG_911\\SDG_911.gdb\\Intermediate_data\\Road_CLIP_buffer3"
Road_Buffer_4 = "D:\\SDG_911\\SDG_911.gdb\\Intermediate_data\\Road_CLIP_buffer4"
Road_Buffer_Reprojected = "D:\\SDG_911\\SDG_911.gdb\\Road_CLIP_buffer_Mollweide"
ruralpop_in_2km = "D:\\SDG_911\\SDG_911.gdb\\ruralpop_in_2km"
Result_Table = Joined_table
Result_Table__2_ = Result_Table
Output_Table_Output = Result_Table__2_

# Process: Iterate through country codes
arcpy.IterateFeatureSelection_mb(Input_Country_Boundaries, "ISO #", "false")

# Process: Clip (2)
arcpy.Clip_management(Input_Global_Rural_Population_Raster, "-15641162.1443 2321790.7856 13401188.7741 8720711.1295", Clipped_Rural_Population_Count, Iterator_Country_Output, "-3.400000e+38", "NONE", "NO_MAINTAIN_EXTENT")

# Process: Zonal Statistics as Table
arcpy.gp.ZonalStatisticsAsTable_sa(Iterator_Country_Output, "ISO", Clipped_Rural_Population_Count, rural_pop, "DATA", "SUM")

# Process: Clip
arcpy.Clip_analysis(Input_Roads, Iterator_Country_Output, Roads_Clip, "")

# Process: Buffer
arcpy.Buffer_analysis(Roads_Clip, Road_Buffer_1, "30 Meters", "FULL", "ROUND", "ALL", "", "PLANAR")

# Process: Buffer (2)
arcpy.Buffer_analysis(Road_Buffer_1, Road_Buffer_2, "100 Meters", "FULL", "ROUND", "ALL", "", "PLANAR")

# Process: Buffer (3)
arcpy.Buffer_analysis(Road_Buffer_2, Road_Buffer_3, "500 Meters", "FULL", "ROUND", "ALL", "", "PLANAR")

# Process: Buffer (4)
arcpy.Buffer_analysis(Road_Buffer_3, Road_Buffer_4, "1370 Meters", "FULL", "ROUND", "ALL", "", "PLANAR")

# Process: Project
arcpy.Project_management(Road_Buffer_4, Road_Buffer_Reprojected, "PROJCS['World_Mollweide',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mollweide'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],UNIT['Meter',1.0]]", "", "", "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")

# Process: Zonal Statistics as Table (2)
arcpy.gp.ZonalStatisticsAsTable_sa(Road_Buffer_Reprojected, "OBJECTID", Clipped_Rural_Population_Count, ruralpop_in_2km, "DATA", "SUM")

# Process: Join Field
arcpy.JoinField_management(rural_pop, "OBJECTID", ruralpop_in_2km, "OBJECTID", "SUM")

# Process: Add 9.1.1 Result Field
arcpy.AddField_management(Joined_table, "SDG_911", "DOUBLE", "2", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Calculate Field
arcpy.CalculateField_management(Result_Table, "SDG_911", "( [SUM_1] / [SUM]) * 100", "VB", "")

# Process: Append
arcpy.Append_management("D:\\SDG_911\\SDG_911.gdb\\rural_pop", Output_Table, "NO_TEST", "", "")

