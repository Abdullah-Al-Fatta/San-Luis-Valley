# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 12:27:47 2023

@author: abdullah al fatta

"""
#Import the necessary libraries:
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import geopandas as gpd
#from fiona.crs import from_epsg
import pyproj
#from shapely.geometry import Polygon


##################################################################################################
### load the study region shapefile into a geopandas dataframe and reproject it to WGS84 CRS
##################################################################################################

# load study region shapefile
study_regions = gpd.read_file(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\required_data\response_areas\Response_Areas_2014_1_21.shp')
# for campus pc
#study_regions = gpd.read_file(r'E:\OneDrive\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\required_data\response_areas\Response_Areas_2014_1_21.shp')
#study_regions.plot()

# reproject study region to WGS84 CRS
study_regions_reprojected = study_regions.to_crs(epsg=4326)
study_regions_reprojected.plot()



# subsetting each regions
Alamosa = study_regions_reprojected[study_regions_reprojected['Zone'].isin(['Alamosa / La Jara'])]
Blanca_Wildlife_Area = study_regions_reprojected[study_regions_reprojected['Zone'].isin(['Blanca Wildlife Area'])]
Closed_Basin_Project = study_regions_reprojected[study_regions_reprojected['Zone'].isin(['Closed Basin Project'])]
Conejos = study_regions_reprojected[study_regions_reprojected['Zone'].isin(['Conejos'])]
Costilla = study_regions_reprojected[study_regions_reprojected['Zone'].isin(['Costilla'])]
Rio_Grande_Alluvium = study_regions_reprojected[study_regions_reprojected['Zone'].isin(['Rio Grande Alluvium'])]
Saguache = study_regions_reprojected[study_regions_reprojected['Zone'].isin(['Saguache'])]
San_Luis = study_regions_reprojected[study_regions_reprojected['Zone'].isin(['San Luis'])]
Subdistrict = study_regions_reprojected[study_regions_reprojected['Zone'].isin(['Subdistrict 1 RA'])]
Trinchera = study_regions_reprojected[study_regions_reprojected['Zone'].isin(['Trinchera'])]

# Merge Closed_Basin_Project and  shapefiles
Closed_Basin_Project_merged = gpd.GeoDataFrame(pd.concat([Closed_Basin_Project, Blanca_Wildlife_Area], ignore_index=True))
Closed_Basin_Project_merged.plot()

# Merge Trinchera and Costilla shapefiles
#Trinchera_Costilla_merged = gpd.GeoDataFrame(pd.concat([Trinchera, Costilla], ignore_index=True))
#Trinchera_Costilla_merged.plot()


# add a new column for merging two shapefiles using dissolve function
Closed_Basin_Project_merged['dissolve'] = 1
#Trinchera_Costilla_merged['dissolve'] = 1

#merging two shapefiles using dissolve function
Closed_Basin_Project_merged = Closed_Basin_Project_merged.dissolve(by='dissolve')
#Trinchera_Costilla_merged = Trinchera_Costilla_merged.dissolve(by='dissolve')


# Load all shapefiles and combine them into a single GeoDataFrame
merged_gdf = gpd.GeoDataFrame(pd.concat([Alamosa, Closed_Basin_Project_merged, Conejos, Rio_Grande_Alluvium, Saguache, San_Luis, Subdistrict, Trinchera], ignore_index=True))
merged_gdf.plot(color = 'none', edgecolor = 'black')

# writing this shapefile to desired folder
#merged_gdf.to_file(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\required_data\response_areas\output_shapefile_without_costilla.shp', driver='ESRI Shapefile')


##################################################################################################
##                                       ''' Pumping Data'''
##################################################################################################

'''## importing pumping data ####'''

# load the CSV file into a pandas dataframe
pumping = pd.read_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Data\Pumping_data\pumping_data.csv')

# removing zero values from LatDecDeg and LongDecDeg columns
pumping = pumping[(pumping[['LatDecDeg', 'LongDecDeg']] != 0).all(axis = 1)]

   
# convert the pandas dataframe to a geopandas dataframe and create a Point object for each row
pumping_data = gpd.GeoDataFrame(
    pumping, geometry=gpd.points_from_xy(pumping['LongDecDeg'], pumping['LatDecDeg']), crs=pyproj.CRS('EPSG:4326')
    )


# '''## importing pumping data ####'''

# # load pumping shapefile
# df_pumping = gpd.read_file(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\required_data\pumping_shapefile\pumping_database.shp')

# # removing zero values from LatDecDeg and LongDecDeg columns
# pumping_data = df_pumping[(df_pumping[['LatDecDeg', 'LongDecDeg']] != 0).all(axis = 1)]

# change projection if needed
#pumping_data = pumping_data.to_crs('EPSG:4326')

# plot data to observe
#pumping_data.plot()

pumping_data.crs
# clipping the pumping data points to each study regions
pumping_data_Alamosa_La_Jara = gpd.clip(pumping_data, Alamosa)
#pumping_data_Blanca_Wildlife_Area = gpd.clip(pumping_data, Blanca_Wildlife_Area)
#pumping_data_Closed_Basin_Project = gpd.clip(pumping_data, Closed_Basin_Project)
pumping_data_Closed_Basin_Project = gpd.clip(pumping_data, Closed_Basin_Project_merged)
pumping_data_Conejos = gpd.clip(pumping_data, Conejos)
pumping_data_Costilla = gpd.clip(pumping_data, Costilla)
pumping_data_Rio_Grande_Alluvium = gpd.clip(pumping_data, Rio_Grande_Alluvium)
pumping_data_Saguache = gpd.clip(pumping_data, Saguache)
pumping_data_San_Luis = gpd.clip(pumping_data, San_Luis)
pumping_data_Subdistrict_1_RA = gpd.clip(pumping_data, Subdistrict)
pumping_data_Trinchera = gpd.clip(pumping_data, Trinchera)
#pumping_data_Trinchera = gpd.clip(pumping_data, Trinchera_Costilla_merged)


'''pumping_data_Alamosa_La_Jara'''

#create new DataFrame and only keep 'YEAR' and 'ann_amt' columns
pumping_data_Alamosa_La_Jara = pumping_data_Alamosa_La_Jara[['irr_year', 'ann_amt']]
###taking sum for each year
pumping_data_Alamosa_La_Jara = pumping_data_Alamosa_La_Jara.groupby('irr_year', as_index=False).sum()
# converting irr_year from acre-feet(AF) to m3
pumping_data_Alamosa_La_Jara['ann_amt_m3'] = pumping_data_Alamosa_La_Jara['ann_amt'] * 1233.48

#writing data to folder
#pumping_data_Alamosa_La_Jara.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\pumping_data\data\Final\pumping_data_Alamosa_La_Jara.csv')

'''pumping_data_Blanca_Wildlife_Area'''

# #create new DataFrame and only keep 'irr_year' and 'ann_amt' columns
# pumping_data_Blanca_Wildlife_Area = pumping_data_Blanca_Wildlife_Area[['irr_year', 'ann_amt']]
# ###taking sum for each year
# pumping_data_Blanca_Wildlife_Area = pumping_data_Blanca_Wildlife_Area.groupby('irr_year', as_index=False).sum()
# # converting irr_year from acre-feet(AF) to m3
# pumping_data_Blanca_Wildlife_Area['ann_amt_m3'] = pumping_data_Blanca_Wildlife_Area['ann_amt'] * 1233.48

# #writing data to folder
# #pumping_data_Blanca_Wildlife_Area.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\pumping_data\data\Final\pumping_data_Blanca_Wildlife_Area.csv')

'''pumping_data_Closed_Basin_Project'''

# #create new DataFrame and only keep 'irr_year' and 'ann_amt' columns
# pumping_data_Closed_Basin_Project = pumping_data_Closed_Basin_Project[['irr_year', 'ann_amt']]
# ###taking sum for each year
# pumping_data_Closed_Basin_Project = pumping_data_Closed_Basin_Project.groupby('irr_year', as_index=False).sum()
# # converting irr_year from acre-feet(AF) to m3
# pumping_data_Closed_Basin_Project['ann_amt_m3'] = pumping_data_Closed_Basin_Project['ann_amt'] * 1233.48

# #writing data to folder
# #pumping_data_Closed_Basin_Project.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\pumping_data\data\Final\pumping_data_Closed_Basin_Project.csv')

'''pumping_data_Conejos'''

#create new DataFrame and only keep 'irr_year' and 'ann_amt' columns
pumping_data_Conejos = pumping_data_Conejos[['irr_year', 'ann_amt']]
###taking sum for each year
pumping_data_Conejos = pumping_data_Conejos.groupby('irr_year', as_index=False).sum()
# converting irr_year from acre-feet(AF) to m3
pumping_data_Conejos['ann_amt_m3'] = pumping_data_Conejos['ann_amt'] * 1233.48

#writing data to folder
#pumping_data_Conejos.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\pumping_data\data\Final\pumping_data_Conejos.csv')

'''pumping_data_Costilla'''

#create new DataFrame and only keep 'irr_year' and 'ann_amt' columns
pumping_data_Costilla = pumping_data_Costilla[['irr_year', 'ann_amt']]
###taking sum for each year
pumping_data_Costilla = pumping_data_Costilla.groupby('irr_year', as_index=False).sum()
# converting irr_year from acre-feet(AF) to m3
pumping_data_Costilla['ann_amt_m3'] = pumping_data_Costilla['ann_amt'] * 1233.48

# #writing data to folder
# #pumping_data_Costilla.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\pumping_data\data\Final\pumping_data_Costilla.csv')

'''pumping_data_Rio_Grande_Alluvium'''

#create new DataFrame and only keep 'irr_year' and 'ann_amt' columns
pumping_data_Rio_Grande_Alluvium = pumping_data_Rio_Grande_Alluvium[['irr_year', 'ann_amt']]
###taking sum for each year
pumping_data_Rio_Grande_Alluvium = pumping_data_Rio_Grande_Alluvium.groupby('irr_year', as_index=False).sum()
# converting irr_year from acre-feet(AF) to m3
pumping_data_Rio_Grande_Alluvium['ann_amt_m3'] = pumping_data_Rio_Grande_Alluvium['ann_amt'] * 1233.48

#writing data to folder
#pumping_data_Rio_Grande_Alluvium.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\pumping_data\data\Final\pumping_data_Rio_Grande_Alluvium.csv')

'''pumping_data_Saguache'''

#create new DataFrame and only keep 'irr_year' and 'ann_amt' columns
pumping_data_Saguache = pumping_data_Saguache[['irr_year', 'ann_amt']]
###taking sum for each year
pumping_data_Saguache = pumping_data_Saguache.groupby('irr_year', as_index=False).sum()
# converting irr_year from acre-feet(AF) to m3
pumping_data_Saguache['ann_amt_m3'] = pumping_data_Saguache['ann_amt'] * 1233.48

#writing data to folder
#pumping_data_Saguache.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\pumping_data\data\Final\pumping_data_Saguache.csv')

'''pumping_data_San_Luis'''

#create new DataFrame and only keep 'irr_year' and 'ann_amt' columns
pumping_data_San_Luis = pumping_data_San_Luis[['irr_year', 'ann_amt']]
###taking sum for each year
pumping_data_San_Luis = pumping_data_San_Luis.groupby('irr_year', as_index=False).sum()
# converting irr_year from acre-feet(AF) to m3
pumping_data_San_Luis['ann_amt_m3'] = pumping_data_San_Luis['ann_amt'] * 1233.48

#writing data to folder
#pumping_data_San_Luis.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\pumping_data\data\Final\pumping_data_San_Luis.csv')

'''pumping_data_Subdistrict_1_RA'''

#create new DataFrame and only keep 'irr_year' and 'ann_amt' columns
pumping_data_Subdistrict_1_RA = pumping_data_Subdistrict_1_RA[['irr_year', 'ann_amt']]
###taking sum for each year
pumping_data_Subdistrict_1_RA = pumping_data_Subdistrict_1_RA.groupby('irr_year', as_index=False).sum()
# converting irr_year from acre-feet(AF) to m3
pumping_data_Subdistrict_1_RA['ann_amt_m3'] = pumping_data_Subdistrict_1_RA['ann_amt'] * 1233.48

#writing data to folder
#pumping_data_Subdistrict_1_RA.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\pumping_data\data\Final\pumping_data_Subdistrict_1_RA.csv')

'''pumping_data_Trinchera'''

#create new DataFrame and only keep 'irr_year' and 'ann_amt' columns
pumping_data_Trinchera = pumping_data_Trinchera[['irr_year', 'ann_amt']]
###taking sum for each year
pumping_data_Trinchera = pumping_data_Trinchera.groupby('irr_year', as_index=False).sum()
# converting irr_year from acre-feet(AF) to m3
pumping_data_Trinchera['ann_amt_m3'] = pumping_data_Trinchera['ann_amt'] * 1233.48

# #writing data to folder
# #pumping_data_Trinchera.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\pumping_data\data\Final\pumping_data_Trinchera.csv')


'''pumping_data_Closed_Basin_Project_Blanca_merged'''

#create new DataFrame and only keep 'irr_year' and 'ann_amt' columns
pumping_data_Closed_Basin_Project = pumping_data_Closed_Basin_Project[['irr_year', 'ann_amt']]
###taking sum for each year
pumping_data_Closed_Basin_Project = pumping_data_Closed_Basin_Project.groupby('irr_year', as_index=False).sum()
# converting irr_year from acre-feet(AF) to m3
pumping_data_Closed_Basin_Project['ann_amt_m3'] = pumping_data_Closed_Basin_Project['ann_amt'] * 1233.48

#writing data to folder
#pumping_data_Closed_Basin_Project.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\pumping_data\data\Final\pumping_data_Closed_Basin_Project.csv')


#'''pumping_data_Trinchera_Costilla_merged'''

# #create new DataFrame and only keep 'irr_year' and 'ann_amt' columns
# pumping_data_Trinchera = pumping_data_Trinchera[['irr_year', 'ann_amt']]
# ###taking sum for each year
# pumping_data_Trinchera = pumping_data_Trinchera.groupby('irr_year', as_index=False).sum()
# # converting irr_year from acre-feet(AF) to m3
# pumping_data_Trinchera['ann_amt_m3'] = pumping_data_Trinchera['ann_amt'] * 1233.48

# #writing data to folder
# #pumping_data_Trinchera.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\pumping_data\data\Final\pumping_data_Trinchera.csv')


##################################################################################################
##                                       ### Water Level Data ###
##################################################################################################


'''### importing water level data ###'''

# load the CSV file into a pandas dataframe
df = pd.read_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\required_data\water_level_data_marchOnly.csv')

# filtering the dataframe based on a boolean condition that checks if the year is greater than or equal 
# to 2009 and the UID has at least one non-null value for that year. Here's the code to do that
#df_filtered = df[df['YEAR'] >= 2009].groupby('UID').filter(lambda x: x['DTW'].notnull().any())
       
# convert the pandas dataframe to a geopandas dataframe and create a Point object for each row
water_level = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df['LON'], df['LAT']), crs=pyproj.CRS('EPSG:4326')
    )
# see plot
#water_level.plot()


# drop "DATE" column if it is needed to save the shapefileas ESRI Shapefile does not support datetime fields
#df = df.drop(['DATE'], axis=1)

# save the geopandas dataframe as a shapefile
#water_level.to_file(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\required_data\water_level_shape\water_level.shp')

water_level_data_all_year = water_level.groupby(['UID'], as_index=False).mean()


# clipping the water level data points to each study regions
water_level_data_Alamosa_La_Jara = gpd.clip(water_level, Alamosa)
#water_level_data_Blanca_Wildlife_Area = gpd.clip(water_level, Blanca_Wildlife_Area)
#water_level_data_Closed_Basin_Project = gpd.clip(water_level, Closed_Basin_Project)
water_level_data_Conejos = gpd.clip(water_level, Conejos)
water_level_data_Costilla = gpd.clip(water_level, Costilla)
water_level_data_Rio_Grande_Alluvium = gpd.clip(water_level, Rio_Grande_Alluvium)
water_level_data_Saguache = gpd.clip(water_level, Saguache)
water_level_data_San_Luis = gpd.clip(water_level, San_Luis)
water_level_data_Subdistrict_1_RA = gpd.clip(water_level, Subdistrict)
water_level_data_Trinchera = gpd.clip(water_level, Trinchera)

water_level_data_Closed_Basin_Project = gpd.clip(water_level, Closed_Basin_Project_merged)
#water_level_data_Trinchera = gpd.clip(water_level, Trinchera_Costilla_merged)



#subtracting “DTW: Depth to water in feet below ground surface” from surface elevation to obtain hydraulic head.
water_level_data_Alamosa_La_Jara['Hydraulic Head'] = water_level_data_Alamosa_La_Jara['GS'] - water_level_data_Alamosa_La_Jara['DTW']
#water_level_data_Blanca_Wildlife_Area['Hydraulic Head'] = water_level_data_Blanca_Wildlife_Area['GS'] - water_level_data_Blanca_Wildlife_Area['DTW']
water_level_data_Closed_Basin_Project['Hydraulic Head'] = water_level_data_Closed_Basin_Project['GS'] - water_level_data_Closed_Basin_Project['DTW']
water_level_data_Conejos['Hydraulic Head'] = water_level_data_Conejos['GS'] - water_level_data_Conejos['DTW']
water_level_data_Costilla['Hydraulic Head'] = water_level_data_Costilla['GS'] - water_level_data_Costilla['DTW']
water_level_data_Rio_Grande_Alluvium['Hydraulic Head'] = water_level_data_Rio_Grande_Alluvium['GS'] - water_level_data_Rio_Grande_Alluvium['DTW']
water_level_data_Saguache['Hydraulic Head'] = water_level_data_Saguache['GS'] - water_level_data_Saguache['DTW']
water_level_data_San_Luis['Hydraulic Head'] = water_level_data_San_Luis['GS'] - water_level_data_San_Luis['DTW']
water_level_data_Subdistrict_1_RA['Hydraulic Head'] = water_level_data_Subdistrict_1_RA['GS'] - water_level_data_Subdistrict_1_RA['DTW']
water_level_data_Trinchera['Hydraulic Head'] = water_level_data_Trinchera['GS'] - water_level_data_Trinchera['DTW']



'''Alamosa_La_Jara'''
#taking the mean of water level data collected in each month
water_level_data_Alamosa_La_Jara = water_level_data_Alamosa_La_Jara.groupby(['UID', 'YEAR'], as_index=False).mean()
# change in water level
water_level_data_Alamosa_La_Jara['hydraulic_head_change_ft'] = water_level_data_Alamosa_La_Jara['Hydraulic Head'].diff() 
#taking the mean of hydraulic head data collected in each year
water_level_data_Alamosa_La_Jara = water_level_data_Alamosa_La_Jara.groupby('YEAR', as_index=False)['hydraulic_head_change_ft'].mean()  
# converting hydraulic_head_change_ft from ft to m
water_level_data_Alamosa_La_Jara['hydraulic_head_change_m'] = water_level_data_Alamosa_La_Jara['hydraulic_head_change_ft'] * 0.3048

#writing data to folder
#water_level_data_Alamosa_La_Jara.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\water_level_data\water_level_data\Final\water_level_data_Alamosa_La_Jara.csv')


'''Blanca_Wildlife_Area'''
# #taking the mean of water level data collected in each month
# water_level_data_Blanca_Wildlife_Area = water_level_data_Blanca_Wildlife_Area.groupby(['UID', 'YEAR'], as_index=False).mean()
# # change in water level
# water_level_data_Blanca_Wildlife_Area['hydraulic_head_change_ft'] = water_level_data_Blanca_Wildlife_Area['Hydraulic Head'].diff() 
# #taking the mean of hydraulic head data collected in each year
# water_level_data_Blanca_Wildlife_Area = water_level_data_Blanca_Wildlife_Area.groupby('YEAR', as_index=False)['hydraulic_head_change_ft'].mean()    
# # converting hydraulic_head_change_ft from ft to m
# water_level_data_Blanca_Wildlife_Area['hydraulic_head_change_m'] = water_level_data_Blanca_Wildlife_Area['hydraulic_head_change_ft'] * 0.3048

#writing data to folder
#water_level_data_Blanca_Wildlife_Area.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\water_level_data\water_level_data\Final\water_level_data_Blanca_Wildlife_Area.csv')

'''Closed_Basin_Project'''
#taking the mean of water level data collected in each month
water_level_data_Closed_Basin_Project = water_level_data_Closed_Basin_Project.groupby(['UID', 'YEAR'], as_index=False).mean()
# change in water level
water_level_data_Closed_Basin_Project['hydraulic_head_change_ft'] = water_level_data_Closed_Basin_Project['Hydraulic Head'].diff() 
#taking the mean of hydraulic head data collected in each year
water_level_data_Closed_Basin_Project = water_level_data_Closed_Basin_Project.groupby('YEAR', as_index=False)['hydraulic_head_change_ft'].mean()    
# converting hydraulic_head_change_ft from ft to m
water_level_data_Closed_Basin_Project['hydraulic_head_change_m'] = water_level_data_Closed_Basin_Project['hydraulic_head_change_ft'] * 0.3048

#writing data to folder
#water_level_data_Closed_Basin_Project.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\water_level_data\water_level_data\Final\water_level_data_Closed_Basin_Project.csv')

'''Conejos'''
#taking the mean of water level data collected in each month
water_level_data_Conejos = water_level_data_Conejos.groupby(['UID', 'YEAR'], as_index=False).mean()  
# change in water level
water_level_data_Conejos['hydraulic_head_change_ft'] = water_level_data_Conejos['Hydraulic Head'].diff() 
#taking the mean of hydraulic head data collected in each year
water_level_data_Conejos = water_level_data_Conejos.groupby('YEAR', as_index=False)['hydraulic_head_change_ft'].mean()  
# converting hydraulic_head_change_ft from ft to m
water_level_data_Conejos['hydraulic_head_change_m'] = water_level_data_Conejos['hydraulic_head_change_ft'] * 0.3048

#writing data to folder
#water_level_data_Conejos.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\water_level_data\water_level_data\Final\water_level_data_Conejos.csv')

'''Costilla'''
#taking the mean of water level data collected in each month
water_level_data_Costilla = water_level_data_Costilla.groupby(['UID', 'YEAR'], as_index=False).mean()
# change in water level
water_level_data_Costilla['hydraulic_head_change_ft'] = water_level_data_Costilla['Hydraulic Head'].diff()  
#taking the mean of hydraulic head data collected in each year
water_level_data_Costilla = water_level_data_Costilla.groupby('YEAR', as_index=False)['hydraulic_head_change_ft'].mean()   
# converting hydraulic_head_change_ft from ft to m
water_level_data_Costilla['hydraulic_head_change_m'] = water_level_data_Costilla['hydraulic_head_change_ft'] * 0.3048

#writing data to folder
#water_level_data_Costilla.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\water_level_data\water_level_data\Final\water_level_data_Costilla.csv')

'''Rio_Grande_Alluvium'''
#taking the mean of water level data collected in each month
water_level_data_Rio_Grande_Alluvium = water_level_data_Rio_Grande_Alluvium.groupby(['UID', 'YEAR'], as_index=False).mean()
# change in water level
water_level_data_Rio_Grande_Alluvium['hydraulic_head_change_ft'] = water_level_data_Rio_Grande_Alluvium['Hydraulic Head'].diff()  
#taking the mean of hydraulic head data collected in each year
water_level_data_Rio_Grande_Alluvium = water_level_data_Rio_Grande_Alluvium.groupby('YEAR', as_index=False)['hydraulic_head_change_ft'].mean()   
# converting hydraulic_head_change_ft from ft to m
water_level_data_Rio_Grande_Alluvium['hydraulic_head_change_m'] = water_level_data_Rio_Grande_Alluvium['hydraulic_head_change_ft'] * 0.3048

#writing data to folder
#water_level_data_Rio_Grande_Alluvium.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\water_level_data\water_level_data\Final\water_level_data_Rio_Grande_Alluvium.csv')


'''Saguache'''
#taking the mean of water level data collected in each month
water_level_data_Saguache = water_level_data_Saguache.groupby(['UID', 'YEAR'], as_index=False).mean()
# change in water level
water_level_data_Saguache['hydraulic_head_change_ft'] = water_level_data_Saguache['Hydraulic Head'].diff()
#taking the mean of hydraulic head data collected in each year
water_level_data_Saguache = water_level_data_Saguache.groupby('YEAR', as_index=False)['hydraulic_head_change_ft'].mean()     
# converting hydraulic_head_change_ft from ft to m
water_level_data_Saguache['hydraulic_head_change_m'] = water_level_data_Saguache['hydraulic_head_change_ft'] * 0.3048

#writing data to folder
#water_level_data_Saguache.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\water_level_data\water_level_data\Final\water_level_data_Saguache.csv')

'''San_Luis '''
#taking the mean of water level data collected in each month
water_level_data_San_Luis = water_level_data_San_Luis.groupby(['UID', 'YEAR'], as_index=False).mean()
# change in water level
water_level_data_San_Luis['hydraulic_head_change_ft'] = water_level_data_San_Luis['Hydraulic Head'].diff()  
#taking the mean of hydraulic head data collected in each year
water_level_data_San_Luis = water_level_data_San_Luis.groupby('YEAR', as_index=False)['hydraulic_head_change_ft'].mean()   
# converting hydraulic_head_change_ft from ft to m
water_level_data_San_Luis['hydraulic_head_change_m'] = water_level_data_San_Luis['hydraulic_head_change_ft'] * 0.3048

#writing data to folder
#water_level_data_San_Luis.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\water_level_data\water_level_data\Final\water_level_data_San_Luis.csv')


'''Subdistrict_1_RA'''
#taking the mean of water level data collected in each month
water_level_data_Subdistrict_1_RA = water_level_data_Subdistrict_1_RA.groupby(['UID', 'YEAR'], as_index=False).mean()  
# change in water level
water_level_data_Subdistrict_1_RA['hydraulic_head_change_ft'] = water_level_data_Subdistrict_1_RA['Hydraulic Head'].diff() 
#taking the mean of hydraulic head data collected in each year
water_level_data_Subdistrict_1_RA = water_level_data_Subdistrict_1_RA.groupby('YEAR', as_index=False)['hydraulic_head_change_ft'].mean()  
# converting hydraulic_head_change_ft from ft to m
water_level_data_Subdistrict_1_RA['hydraulic_head_change_m'] = water_level_data_Subdistrict_1_RA['hydraulic_head_change_ft'] * 0.3048

#writing data to folder
#water_level_data_Subdistrict_1_RA.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\water_level_data\water_level_data\Final\water_level_data_Subdistrict_1_RA.csv')


'''Trinchera'''
#taking the mean of water level data collected in each month
water_level_data_Trinchera = water_level_data_Trinchera.groupby(['UID', 'YEAR'], as_index=False).mean()  
# change in water level
water_level_data_Trinchera['hydraulic_head_change_ft'] = water_level_data_Trinchera['Hydraulic Head'].diff() 
#taking the mean of hydraulic head data collected in each year
water_level_data_Trinchera = water_level_data_Trinchera.groupby('YEAR', as_index=False)['hydraulic_head_change_ft'].mean()  
# converting hydraulic_head_change_ft from ft to m
water_level_data_Trinchera['hydraulic_head_change_m'] = water_level_data_Trinchera['hydraulic_head_change_ft'] * 0.3048

#writing data to folder
#water_level_data_Trinchera.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\water_level_data\water_level_data\Final\water_level_data_Trinchera.csv')




##################################################################################################
##                                      Subsetting data after 2008
##################################################################################################


# Select last 13 years of pumping data
pumping_data_Alamosa_La_Jara_2009 = pumping_data_Alamosa_La_Jara[pumping_data_Alamosa_La_Jara['irr_year'] >= 2009]
#pumping_data_Blanca_Wildlife_Area_2009 = pumping_data_Blanca_Wildlife_Area[pumping_data_Blanca_Wildlife_Area['irr_year'] >= 2009]
pumping_data_Closed_Basin_Project_2009 = pumping_data_Closed_Basin_Project[pumping_data_Closed_Basin_Project['irr_year'] >= 2009]
pumping_data_Conejos_2009 = pumping_data_Conejos[pumping_data_Conejos['irr_year'] >= 2009]
pumping_data_Costilla_2009 = pumping_data_Costilla[pumping_data_Costilla['irr_year'] >= 2009]
pumping_data_Rio_Grande_Alluvium_2009 = pumping_data_Rio_Grande_Alluvium[pumping_data_Rio_Grande_Alluvium['irr_year'] >= 2009]
pumping_data_Saguache_2009 = pumping_data_Saguache[pumping_data_Saguache['irr_year'] >= 2009]
pumping_data_San_Luis_2009 = pumping_data_San_Luis[pumping_data_San_Luis['irr_year'] >= 2009]
pumping_data_Subdistrict_1_RA_2009 = pumping_data_Subdistrict_1_RA[pumping_data_Subdistrict_1_RA['irr_year'] >= 2009]
pumping_data_Trinchera_2009 = pumping_data_Trinchera[pumping_data_Trinchera['irr_year'] >= 2009]


# rename 'irr_year' to 'YEAR'
pumping_data_Alamosa_La_Jara_2009 = pumping_data_Alamosa_La_Jara_2009.rename(columns={'irr_year':'YEAR'})
#pumping_data_Blanca_Wildlife_Area_2009 = pumping_data_Blanca_Wildlife_Area_2009.rename(columns={'irr_year':'YEAR'})
pumping_data_Closed_Basin_Project_2009 = pumping_data_Closed_Basin_Project_2009.rename(columns={'irr_year':'YEAR'})
pumping_data_Conejos_2009 = pumping_data_Conejos_2009.rename(columns={'irr_year':'YEAR'})
pumping_data_Costilla_2009 = pumping_data_Costilla_2009.rename(columns={'irr_year':'YEAR'})
pumping_data_Rio_Grande_Alluvium_2009 = pumping_data_Rio_Grande_Alluvium_2009.rename(columns={'irr_year':'YEAR'})
pumping_data_Saguache_2009 = pumping_data_Saguache_2009.rename(columns={'irr_year':'YEAR'})
pumping_data_San_Luis_2009 = pumping_data_San_Luis_2009.rename(columns={'irr_year':'YEAR'})
pumping_data_Subdistrict_1_RA_2009 = pumping_data_Subdistrict_1_RA_2009.rename(columns={'irr_year':'YEAR'})
pumping_data_Trinchera_2009 = pumping_data_Trinchera_2009.rename(columns={'irr_year':'YEAR'})


######################
### with diversions
######################
# loading diversion data
diversion = pd.read_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\required_data\Diversion_Data.csv')
# filter after 2009
diversion = diversion[(diversion['year'] >= 2009) & (diversion['year'] < 2021)]
# AF to m2
diversion['total_m3'] = diversion['total_sum'] * 1233
# rename 'irr_year' to 'YEAR'
diversion = diversion.rename(columns={'year':'YEAR'})


#add diversion data to pumping_data_Subdistrict_1_RA_2009
pumping_data_Subdistrict_1_RA_2009 = pd.merge(pumping_data_Subdistrict_1_RA_2009, diversion, on='YEAR', how='left')
# substracting diversion data for Subdistrct 1 RA
pumping_data_Subdistrict_1_RA_2009['Final_pumping'] = pumping_data_Subdistrict_1_RA_2009['ann_amt_m3'] - pumping_data_Subdistrict_1_RA_2009['total_m3']


# Select last 13 years of water level data
water_level_data_Alamosa_La_Jara_2009 = water_level_data_Alamosa_La_Jara[water_level_data_Alamosa_La_Jara['YEAR'] >= 2009]
#water_level_data_Blanca_Wildlife_Area_2009 = water_level_data_Blanca_Wildlife_Area[water_level_data_Blanca_Wildlife_Area['YEAR'] >= 2009]
water_level_data_Closed_Basin_Project_2009 = water_level_data_Closed_Basin_Project[water_level_data_Closed_Basin_Project['YEAR'] >= 2009]
water_level_data_Conejos_2009 = water_level_data_Conejos[water_level_data_Conejos['YEAR'] >= 2009]
water_level_data_Costilla_2009 = water_level_data_Costilla[water_level_data_Costilla['YEAR'] >= 2009]
water_level_data_Rio_Grande_Alluvium_2009 = water_level_data_Rio_Grande_Alluvium[water_level_data_Rio_Grande_Alluvium['YEAR'] >= 2009]
water_level_data_Saguache_2009 = water_level_data_Saguache[water_level_data_Saguache['YEAR'] >= 2009]
water_level_data_San_Luis_2009 = water_level_data_San_Luis[water_level_data_San_Luis['YEAR'] >= 2009]
water_level_data_Subdistrict_1_RA_2009 = water_level_data_Subdistrict_1_RA[water_level_data_Subdistrict_1_RA['YEAR'] >= 2009]
water_level_data_Trinchera_2009 = water_level_data_Trinchera[water_level_data_Trinchera['YEAR'] >= 2009]


# merging pumping and water level data together
Alamosa_La_Jara = pd.merge(water_level_data_Alamosa_La_Jara_2009,pumping_data_Alamosa_La_Jara_2009, on ='YEAR', how = 'left')
#Blanca_Wildlife_Area = pd.merge(water_level_data_Blanca_Wildlife_Area_2009,pumping_data_Blanca_Wildlife_Area_2009, on ='YEAR', how = 'left' )
Closed_Basin_Project = pd.merge(water_level_data_Closed_Basin_Project_2009,pumping_data_Closed_Basin_Project_2009, on ='YEAR', how = 'left' )
Conejos = pd.merge(water_level_data_Conejos_2009,pumping_data_Conejos_2009, on ='YEAR', how = 'left' )
Costilla = pd.merge(water_level_data_Costilla_2009,pumping_data_Costilla_2009, on ='YEAR', how = 'left' )
Rio_Grande_Alluvium = pd.merge(water_level_data_Rio_Grande_Alluvium_2009,pumping_data_Rio_Grande_Alluvium_2009, on ='YEAR', how = 'left' )
Saguache = pd.merge(water_level_data_Saguache_2009,pumping_data_Saguache_2009, on ='YEAR', how = 'left' )
San_Luis = pd.merge(water_level_data_San_Luis_2009,pumping_data_San_Luis_2009, on ='YEAR', how = 'left' )
Subdistrict_1_RA = pd.merge(water_level_data_Subdistrict_1_RA_2009,pumping_data_Subdistrict_1_RA_2009, on ='YEAR', how = 'left' )
Trinchera = pd.merge(water_level_data_Trinchera_2009,pumping_data_Trinchera_2009, on ='YEAR', how = 'left' )





#####################################################################33
## Shifted ann_amt_m3
#####################################################################33


## plot with regression line using seaborn library for Subsiding-region

'''Alamosa_La_Jara'''

# create a new column with a one-year lag for ann_amt_m3
Alamosa_La_Jara['ann_amt_m3_lagged'] = Alamosa_La_Jara['ann_amt_m3'].shift(1)

# #drop rows that has NAs in "ann_amt_m3_lagged" column 
Alamosa_La_Jara = Alamosa_La_Jara.dropna(subset=['ann_amt_m3_lagged'])

# declaring variable as years
years = Alamosa_La_Jara['YEAR']

# get coeffs of linear fit
#slope, intercept, r_value, p_value, std_err  = stats.linregress(Alamosa_La_Jara['ann_amt_m3_lagged'],Alamosa_La_Jara['hydraulic_head_change_m'])

# use line_kws to set line label for legend
ax = sns.regplot(x="ann_amt_m3_lagged", y="hydraulic_head_change_m", data = Alamosa_La_Jara)

# plot legend
ax.legend(title='', loc='upper right', labels=['Points', 'Regression Line'])
plt.title("Alamosa/La Jara") #title
plt.xlabel("Total Groundwater Pumping, $m^3$") #x label
plt.ylabel("Head Change, m")
plt.xticks(rotation=45, ha='right')
# Showing the year next to each point on the scatter plot
for i, year in enumerate(years):
    ax.annotate(year, (Alamosa_La_Jara['ann_amt_m3_lagged'].iloc[i], Alamosa_La_Jara['hydraulic_head_change_m'].iloc[i]))
#plt.savefig(r"D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\outputs\figures\Alamosa_La_Jara3.png", dpi=400, bbox_inches='tight')
plt.show()





'''Blanca_Wildlife_Area'''

# # create a new column with a one-year lag for ann_amt_m3
# Blanca_Wildlife_Area['ann_amt_m3_lagged'] = Blanca_Wildlife_Area['hydraulic_head_change_m'].shift(1)

# #drop rows that has NAs in "ann_amt_m3_lagged" column 
# Blanca_Wildlife_Area = Blanca_Wildlife_Area.dropna(subset=['ann_amt_m3_lagged'])

# # declaring variable as years
# years = Blanca_Wildlife_Area['YEAR']

# # get coeffs of linear fit
# slope, intercept, r_value, p_value, std_err  = stats.linregress(Blanca_Wildlife_Area['ann_amt_m3_lagged'],Blanca_Wildlife_Area['hydraulic_head_change_m'])

# # use line_kws to set line label for legend
# ax = sns.regplot(x="ann_amt_m3_lagged", y="hydraulic_head_change_m", data = Blanca_Wildlife_Area)

# # plot legend
# ax.legend(title='', loc='upper right', labels=['Points', 'Regression Line'])
# plt.title("Blanca Wildlife Area") #title
# plt.xlabel("Total Groundwater Pumping, $m^3$") #x label
# plt.ylabel("Head Change, m")
# plt.xticks(rotation=45, ha='right')
# # Showing the year next to each point on the scatter plot
# for i, year in enumerate(years):
#     ax.annotate(year, (Blanca_Wildlife_Area['ann_amt_m3_lagged'].iloc[i], Blanca_Wildlife_Area['hydraulic_head_change_m'].iloc[i]))
# plt.savefig(r"D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\outputs\figures\Blanca_Wildlife_Area3.png", dpi=400, bbox_inches='tight')
# plt.show()

'''Closed_Basin_Project'''

# create a new column with a one-year lag for ann_amt_m3
Closed_Basin_Project['ann_amt_m3_lagged'] = Closed_Basin_Project['ann_amt_m3'].shift(1)

#drop rows that has NAs in "ann_amt_m3_lagged" column 
Closed_Basin_Project = Closed_Basin_Project.dropna(subset=['ann_amt_m3_lagged'])

# declaring variable as years
years = Closed_Basin_Project['YEAR']

# get coeffs of linear fit
slope, intercept, r_value, p_value, std_err  = stats.linregress(Closed_Basin_Project['ann_amt_m3_lagged'],Closed_Basin_Project['hydraulic_head_change_m'])

# use line_kws to set line label for legend
ax = sns.regplot(x="ann_amt_m3_lagged", y="hydraulic_head_change_m", data = Closed_Basin_Project)

# plot legend
ax.legend(title='', loc='upper right', labels=['Points', 'Regression Line'])
plt.title("Closed Basin and Blanca Wildlife") #title
plt.xlabel("Total Groundwater Pumping, $m^3$") #x label
plt.ylabel("Head Change, m")
plt.xticks(rotation=45, ha='right')
# Showing the year next to each point on the scatter plot
for i, year in enumerate(years):
    ax.annotate(year, (Closed_Basin_Project['ann_amt_m3_lagged'].iloc[i], Closed_Basin_Project['hydraulic_head_change_m'].iloc[i]))
#plt.savefig(r"D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\outputs\figures\Closed_Basin_Project3.png", dpi=400, bbox_inches='tight')
plt.show()


'''Conejos'''

# create a new column with a one-year lag for ann_amt_m3
Conejos['ann_amt_m3_lagged'] = Conejos['ann_amt_m3'].shift(1)

#drop rows that has NAs in "ann_amt_m3_lagged" column 
Conejos = Conejos.dropna(subset=['ann_amt_m3_lagged'])

# declaring variable as years
years = Conejos['YEAR']

# get coeffs of linear fit
slope, intercept, r_value, p_value, std_err  = stats.linregress(Conejos['ann_amt_m3_lagged'],Conejos['hydraulic_head_change_m'])

# use line_kws to set line label for legend
ax = sns.regplot(x="ann_amt_m3_lagged", y="hydraulic_head_change_m", data = Conejos)

# plot legend
ax.legend(title='', loc='lower right', labels=['Points', 'Regression Line'])
plt.title("Conejos") #title
plt.xlabel("Total Groundwater Pumping, $m^3$") #x label
plt.ylabel("Head Change, m")
plt.xticks(rotation=45, ha='right')
# Showing the year next to each point on the scatter plot
for i, year in enumerate(years):
    ax.annotate(year, (Conejos['ann_amt_m3_lagged'].iloc[i], Conejos['hydraulic_head_change_m'].iloc[i]))
#plt.savefig(r"D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\outputs\figures\Conejos3.png", dpi=400, bbox_inches='tight')
plt.show()


'''Costilla'''

# create a new column with a one-year lag for ann_amt_m3
Costilla['ann_amt_m3_lagged'] = Costilla['ann_amt_m3'].shift(1)

#drop rows that has NAs in "ann_amt_m3_lagged" column 
Costilla = Costilla.dropna(subset=['ann_amt_m3_lagged'])

# declaring variable as years
years = Costilla['YEAR']

# get coeffs of linear fit
slope, intercept, r_value, p_value, std_err  = stats.linregress(Costilla['ann_amt_m3_lagged'],Costilla['hydraulic_head_change_m'])

# use line_kws to set line label for legend
ax = sns.regplot(x="ann_amt_m3_lagged", y="hydraulic_head_change_m", data = Costilla)

# plot legend
ax.legend(title='', loc='lower right', labels=['Points', 'Regression Line'])
plt.title("Costilla") #title
plt.xlabel("Total Groundwater Pumping, $m^3$") #x label
plt.ylabel("Head Change, m")
plt.xticks(rotation=45, ha='right')
# Showing the year next to each point on the scatter plot
for i, year in enumerate(years):
    ax.annotate(year, (Costilla['ann_amt_m3_lagged'].iloc[i], Costilla['hydraulic_head_change_m'].iloc[i]))
#plt.savefig(r"D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\outputs\figures\Costilla3.png", dpi=400, bbox_inches='tight')
plt.show()


'''Rio_Grande_Alluvium'''

# create a new column with a one-year lag for ann_amt_m3
Rio_Grande_Alluvium['ann_amt_m3_lagged'] = Rio_Grande_Alluvium['ann_amt_m3'].shift(1)

#drop rows that has NAs in "ann_amt_m3_lagged" column 
Rio_Grande_Alluvium = Rio_Grande_Alluvium.dropna(subset=['ann_amt_m3_lagged'])

# declaring variable as years
years = Rio_Grande_Alluvium['YEAR']

# get coeffs of linear fit
slope, intercept, r_value, p_value, std_err  = stats.linregress(Rio_Grande_Alluvium['ann_amt_m3_lagged'],Rio_Grande_Alluvium['hydraulic_head_change_m'])

# use line_kws to set line label for legend
ax = sns.regplot(x="ann_amt_m3_lagged", y="hydraulic_head_change_m", data = Rio_Grande_Alluvium)

# plot legend
ax.legend(title='', loc='upper right', labels=['Points', 'Regression Line'])
plt.title("Rio Grande Alluvium") #title
plt.xlabel("Total Groundwater Pumping, $m^3$") #x label
plt.ylabel("Head Change, m")
plt.xticks(rotation=45, ha='right')
# Showing the year next to each point on the scatter plot
for i, year in enumerate(years):
    ax.annotate(year, (Rio_Grande_Alluvium['ann_amt_m3_lagged'].iloc[i], Rio_Grande_Alluvium['hydraulic_head_change_m'].iloc[i]))
#plt.savefig(r"D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\outputs\figures\Rio_Grande_Alluvium3.png", dpi=400, bbox_inches='tight')
plt.show()


'''Saguache'''

# create a new column with a one-year lag for ann_amt_m3
Saguache['ann_amt_m3_lagged'] = Saguache['ann_amt_m3'].shift(1)

#drop rows that has NAs in "ann_amt_m3_lagged" column 
Saguache = Saguache.dropna(subset=['ann_amt_m3_lagged'])

# declaring variable as years
years = Saguache['YEAR']

# get coeffs of linear fit
slope, intercept, r_value, p_value, std_err  = stats.linregress(Saguache['ann_amt_m3_lagged'],Saguache['hydraulic_head_change_m'])

# use line_kws to set line label for legend
ax = sns.regplot(x="ann_amt_m3_lagged", y="hydraulic_head_change_m", data = Saguache)

# plot legend
ax.legend(title='', loc='upper right', labels=['Points', 'Regression Line'])
plt.title("Saguache") #title
plt.xlabel("Total Groundwater Pumping, $m^3$") #x label
plt.ylabel("Head Change, m")
plt.xticks(rotation=45, ha='right')
# Showing the year next to each point on the scatter plot
for i, year in enumerate(years):
    ax.annotate(year, (Saguache['ann_amt_m3_lagged'].iloc[i], Saguache['hydraulic_head_change_m'].iloc[i]))
#plt.savefig(r"D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\outputs\figures\Saguache3.png", dpi=400, bbox_inches='tight')
plt.show()


'''San_Luis'''

# create a new column with a one-year lag for ann_amt_m3
San_Luis['ann_amt_m3_lagged'] = San_Luis['ann_amt_m3'].shift(1)

#drop rows that has NAs in "ann_amt_m3_lagged" column 
San_Luis = San_Luis.dropna(subset=['ann_amt_m3_lagged'])

# declaring variable as years
years = San_Luis['YEAR']

# get coeffs of linear fit
slope, intercept, r_value, p_value, std_err  = stats.linregress(San_Luis['ann_amt_m3_lagged'],San_Luis['hydraulic_head_change_m'])

# use line_kws to set line label for legend
ax = sns.regplot(x="ann_amt_m3_lagged", y="hydraulic_head_change_m", data = San_Luis)

# plot legend
ax.legend(title='', loc='upper right', labels=['Points', 'Regression Line'])
plt.title("San Luis") #title
plt.xlabel("Total Groundwater Pumping, $m^3$") #x label
plt.ylabel("Head Change, m")
plt.xticks(rotation=45, ha='right')
# Showing the year next to each point on the scatter plot
for i, year in enumerate(years):
    ax.annotate(year, (San_Luis['ann_amt_m3_lagged'].iloc[i], San_Luis['hydraulic_head_change_m'].iloc[i]))
#plt.savefig(r"D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\outputs\figures\San_Luis3.png", dpi=400, bbox_inches='tight')
plt.show()


'''Subdistrict_1_RA'''

# create a new column with a one-year lag for ann_amt_m3
Subdistrict_1_RA['ann_amt_m3_lagged'] = Subdistrict_1_RA['Final_pumping'].shift(1)

#drop rows that has NAs in "ann_amt_m3_lagged" column 
Subdistrict_1_RA = Subdistrict_1_RA.dropna(subset=['ann_amt_m3_lagged'])

# declaring variable as years
years = Subdistrict_1_RA['YEAR']

# get coeffs of linear fit
slope, intercept, r_value, p_value, std_err  = stats.linregress(Subdistrict_1_RA['ann_amt_m3_lagged'],Subdistrict_1_RA['hydraulic_head_change_m'])

# use line_kws to set line label for legend
ax = sns.regplot(x="ann_amt_m3_lagged", y="hydraulic_head_change_m", data = Subdistrict_1_RA)

# plot legend
ax.legend(title='', loc='upper right', labels=['Points', 'Regression Line'])
plt.title("Subdistrict-1 RA with Diversions") #title
plt.xlabel("Total Groundwater Pumping, $m^3$") #x label
plt.ylabel("Head Change, m")
plt.xticks(rotation=45, ha='right')
# Showing the year next to each point on the scatter plot
for i, year in enumerate(years):
    ax.annotate(year, (Subdistrict_1_RA['ann_amt_m3_lagged'].iloc[i], Subdistrict_1_RA['hydraulic_head_change_m'].iloc[i]))
#plt.savefig(r"D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\outputs\figures\Subdistrict_1_RA2_with_diversions3.png", dpi=400, bbox_inches='tight')
plt.show()


'''Trinchera'''

# create a new column with a one-year lag for ann_amt_m3
Trinchera['ann_amt_m3_lagged'] = Trinchera['ann_amt_m3'].shift(1)

#drop rows that has NAs in "ann_amt_m3_lagged" column 
Trinchera = Trinchera.dropna(subset=['ann_amt_m3_lagged'])

# declaring variable as years
years = Trinchera['YEAR']

# get coeffs of linear fit
slope, intercept, r_value, p_value, std_err  = stats.linregress(Trinchera['ann_amt_m3_lagged'],Trinchera['hydraulic_head_change_m'])

# use line_kws to set line label for legend
ax = sns.regplot(x="ann_amt_m3_lagged", y="hydraulic_head_change_m", data = Trinchera)

# plot legend
ax.legend(title='', loc='upper right', labels=['Points', 'Regression Line'])
plt.title("Trinchera") #title
plt.xlabel("Total Groundwater Pumping, $m^3$") #x label
plt.ylabel("Head Change, m")
plt.xticks(rotation=45, ha='right')
# Showing the year next to each point on the scatter plot
for i, year in enumerate(years):
    ax.annotate(year, (Trinchera['ann_amt_m3_lagged'].iloc[i], Trinchera['hydraulic_head_change_m'].iloc[i]))
#plt.savefig(r"D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\outputs\figures\Trinchera3.png", dpi=400, bbox_inches='tight')
plt.show()





# ################################################################################################
# ### Calculate slope, intercept, and r2 value and add it to a dataframe called 'df_results'
# ################################################################################################


## import required packages
import pandas as pd
from scipy.stats import linregress

# Define a function calc_linreg to calculate the slope, intercept, and R-squared values for a given dataframe using the linregress function from scipy.stats
def calc_linreg(df):
    slope, intercept, r_value, p_value, std_err = linregress(df['ann_amt_m3_lagged'], df['hydraulic_head_change_m'])
    r_squared = r_value ** 2
    return slope, intercept, r_squared

# Calculate slope, intercept, and R-squared for all four dataframes
slopes = []
intercepts = []
r_squareds = []

# Loop over each of the dataframes, call "calc_linreg" function on each of them, and append the resulting values to separate lists
for df in [Alamosa_La_Jara,Closed_Basin_Project,Conejos, Rio_Grande_Alluvium, Saguache, San_Luis, Subdistrict_1_RA, Trinchera]:
    s, i, r = calc_linreg(df)
    slopes.append(s)
    intercepts.append(i)
    r_squareds.append(r)

# Create a new dataframe with the calculated values
df_results = pd.DataFrame({'Slope': slopes, 'Intercept': intercepts, 'R-squared': r_squareds})

# adding a new column stating all the region names
df_results['response_area'] = ['Alamosa_La_Jara','Closed_Basin_Project','Conejos', 'Rio_Grande_Alluvium', 'Saguache', 'San_Luis', 'Subdistrict_1_RA', 'Trinchera']
# Print the results
#print(df_results)

#df_results.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\outputs\slope_intercept_r2_extended_boundary.csv', index=False)



# ###################################################
# ### Calculation of Storativity and storage
# ###################################################

# obtain area of each region

# change projection to "EPSG:32613" which is "WGS 84 / UTM zone 13N" to get area in m2
area = merged_gdf.to_crs('EPSG:32613')
area['Area_m2'] = area.area

# reassignig "df_results" as "storativity_calc"
storativity_calc = df_results

# adding area to storativity_calc
#storativity_calc['Area_m2'] = area['Area_m2']

# reading area of the regions data and storativity data from folder if needed
#area = pd.read_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\required_data\ResponseArea.csv')
#storativity_calc = pd.read_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\required_data\slope_intercept_r2.csv')

# total area
total_area = area['Area_m2'].sum()

# merge "area" and "storativity_calc"
storativity_calc = storativity_calc.join(area, how = 'left')
# sotrativity calculation
storativity_calc['storativity'] = - 1/(storativity_calc['Area_m2'] * storativity_calc['Slope'])

#storativity_calc.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\outputs\storativity_calculation_subdivisions.csv', index = False)


# ###################################################
# ### Calculation of Storage change
# ###################################################


# add a new column for site name
water_level_data_Alamosa_La_Jara_2009['response_area'] = 'Alamosa_La_Jara'
water_level_data_Closed_Basin_Project_2009['response_area'] = 'Closed_Basin_Project'
water_level_data_Conejos_2009['response_area'] = 'Conejos'
#water_level_data_Costilla_2009['response_area'] = 'Costilla'
water_level_data_Rio_Grande_Alluvium_2009['response_area'] = 'Rio_Grande_Alluvium'
water_level_data_Saguache_2009['response_area'] = 'Saguache'
water_level_data_San_Luis_2009['response_area'] = 'San_Luis'
water_level_data_Subdistrict_1_RA_2009['response_area'] = 'Subdistrict_1_RA'
water_level_data_Trinchera_2009['response_area'] = 'Trinchera'

# merge all dataframe 
head_change_data = pd.concat([water_level_data_Alamosa_La_Jara_2009, water_level_data_Closed_Basin_Project_2009, water_level_data_Conejos_2009, water_level_data_Rio_Grande_Alluvium_2009,water_level_data_Saguache_2009, water_level_data_San_Luis_2009, water_level_data_Subdistrict_1_RA_2009, water_level_data_Trinchera_2009])

#resetting the index
head_change_data = head_change_data.reset_index(drop=True)

# adding the storativity value and area in "head change
head_change_data = head_change_data.merge(storativity_calc, on = 'response_area', how = 'left')

# keeping only needed columns
head_change_data = head_change_data[['YEAR', 'response_area', 'hydraulic_head_change_m','Slope', 'Intercept', 'R-squared', 'Area_m2', 'storativity']]

# absolute value of storativity cloumn
head_change_data['storativity_absolute'] = head_change_data['storativity'].abs()

# calculate the annual change in storage
head_change_data['change_in_storage'] = head_change_data['storativity_absolute'] * head_change_data['hydraulic_head_change_m'] * head_change_data['Area_m2']

# removing 2009 and 2022 data as they may be problematic
head_change_data = head_change_data[(head_change_data['YEAR'] != 2009) & (head_change_data['YEAR'] != 2022)]

# pivot the dataframe
final_storage_change_data = head_change_data.pivot(index='YEAR', columns='response_area', values='change_in_storage')

# sum up all region storage to get the year total
final_storage_change_data['total_storage'] = final_storage_change_data.sum(axis=1)

#feching total area from area
final_storage_change_data['area'] = total_area

# change in m3 to area-normalized mm
final_storage_change_data['total_storage_mm'] = (final_storage_change_data['total_storage']/final_storage_change_data['area'])*1000

# adding a new column having cumulative of storage
final_storage_change_data['cumulative_storage_m3'] = final_storage_change_data['total_storage'].cumsum()

# resetting the index
final_storage_change_data = final_storage_change_data.reset_index()


# change in m3 to area-normalized mm
# final_storage_change_data['Alamosa_La_Jara_storage_mm'] = (final_storage_change_data['Alamosa_La_Jara']/final_storage_change_data['area'])*1000
# final_storage_change_data['Closed_Basin_Project_storage_mm'] = (final_storage_change_data['Closed_Basin_Project']/final_storage_change_data['area'])*1000
# final_storage_change_data['Conejos_storage_mm'] = (final_storage_change_data['Conejos']/final_storage_change_data['area'])*1000
# final_storage_change_data['Rio_Grande_Alluvium_storage_mm'] = (final_storage_change_data['Rio_Grande_Alluvium']/final_storage_change_data['area'])*1000
# final_storage_change_data['Saguache_storage_mm'] = (final_storage_change_data['Saguache']/final_storage_change_data['area'])*1000
# final_storage_change_data['San_Luis_storage_mm'] = (final_storage_change_data['San_Luis']/final_storage_change_data['area'])*1000
# final_storage_change_data['Subdistrict_1_RA_storage_mm'] = (final_storage_change_data['Subdistrict_1_RA']/final_storage_change_data['area'])*1000
# final_storage_change_data['Trinchera_storage_mm'] = (final_storage_change_data['Trinchera']/final_storage_change_data['area'])*1000

# adding a new column having cumulative of storage
final_storage_change_data['Alamosa_La_Jara_cumulative_storage_m3'] = final_storage_change_data['Alamosa_La_Jara'].cumsum()
final_storage_change_data['Closed_Basin_Project_cumulative_storage_m3'] = final_storage_change_data['Closed_Basin_Project'].cumsum()
final_storage_change_data['Conejos_cumulative_storage_m3'] = final_storage_change_data['Conejos'].cumsum()
#final_storage_change_data['Costilla_cumulative_storage_m3'] = final_storage_change_data['Costilla'].cumsum()
final_storage_change_data['Rio_Grande_Alluvium_cumulative_storage_m3'] = final_storage_change_data['Rio_Grande_Alluvium'].cumsum()
final_storage_change_data['Saguache_cumulative_storage_m3'] = final_storage_change_data['Saguache'].cumsum()
final_storage_change_data['San_Luis_cumulative_storage_m3'] = final_storage_change_data['San_Luis'].cumsum()
final_storage_change_data['Subdistrict_1_RA_cumulative_storage_m3'] = final_storage_change_data['Subdistrict_1_RA'].cumsum()
final_storage_change_data['Trinchera_cumulative_storage_m3'] = final_storage_change_data['Trinchera'].cumsum()


######################################
### plot cumulative storage data
######################################

# plotting without 
# line plot
plt.plot(final_storage_change_data['YEAR'], final_storage_change_data['cumulative_storage_m3'], color = 'b')

# add points to the line
plt.scatter(final_storage_change_data['YEAR'], final_storage_change_data['cumulative_storage_m3'], color = 'b')

# set the x-axis label
plt.xlabel('Year')
# set the y-axis label
plt.ylabel('Cumulative Change in Storage, $m^3$')
# set the title
plt.title('Change in Storage over Time')

# save figure
#plt.savefig(r"D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\outputs\figures\1.cumulative_storage_km3.png", dpi=400, bbox_inches='tight')

# show the plot
plt.show()

# save data as csv
#final_storage_change_data.to_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\outputs\final_storage_change_data_ssubdivisions.csv', index = False)


########################################################
### plot cumulative storage data for all subdistricts
########################################################

# Create plot
fig, ax = plt.subplots()
ax.plot(final_storage_change_data['YEAR'], final_storage_change_data['Alamosa_La_Jara_cumulative_storage_m3'], label='Alamosa La Jara')
ax.plot(final_storage_change_data['YEAR'], final_storage_change_data['Closed_Basin_Project_cumulative_storage_m3'], label= 'Closed Basin and Blanca Wlildife')
ax.plot(final_storage_change_data['YEAR'], final_storage_change_data['Conejos_cumulative_storage_m3'], label= 'Conejos')
#ax.plot(final_storage_change_data['YEAR'], final_storage_change_data['Costilla_cumulative_storage_m3'], label= 'Costilla')
ax.plot(final_storage_change_data['YEAR'], final_storage_change_data['Rio_Grande_Alluvium_cumulative_storage_m3'], label= 'Rio Grande Alluvium')
ax.plot(final_storage_change_data['YEAR'], final_storage_change_data['Saguache_cumulative_storage_m3'], label= 'Saguache')
ax.plot(final_storage_change_data['YEAR'], final_storage_change_data['San_Luis_cumulative_storage_m3'], label= 'San Luis')
ax.plot(final_storage_change_data['YEAR'], final_storage_change_data['Subdistrict_1_RA_cumulative_storage_m3'], label= 'Subdistrict 1 RA')
ax.plot(final_storage_change_data['YEAR'], final_storage_change_data['Trinchera_cumulative_storage_m3'], label= 'Trinchera and Costilla')

#ax.plot(data['year'], data['Streamflow_mm_contributing_area_5500'], label= 'Avg Streamflow')

# Set axis labels and title
ax.set_xlabel('Year')
ax.set_ylabel('Cumulative Change in Storage, $m^3$')
ax.set_title('')

# Add legend
ax.legend()
#ax.legend(loc= 'upper left', fontsize = 7)  # Legend at lower left corner
# ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
#           fancybox=True, shadow=True, ncol=5)
#ax.legend(loc='upper left', bbox_to_anchor=(1, 0.5))
ax.legend(bbox_to_anchor=(1, 0.8))

#plt.savefig(r"D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\outputs\figures\1.storage_change_all_subdistricts_without_costilla.png", dpi=300, bbox_inches='tight') #saving plot to folder

# Display the plot
plt.show()






# ###################################################
# ### Storage change from climate data
# ###################################################

import matplotlib.pyplot as plt

# ## plot with regression line using seaborn library
data = pd.read_csv(r'D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\water_balance_4 2 2023.csv')

# adding storage change data from Butler approach
#data['final_storage_change_Butler'] = final_storage_change_data['cumulative_storage_m3']

# Create plot
fig, ax = plt.subplots()
#ax.plot(data['Year'], data['avg_annual_precip_mm'], label='Avg Annual Precipitation')
ax.plot(data['Year'], data['ET_OpenET_mm'], label= 'Avg Annnual ET-OpenET')
ax.plot(data['Year'], data['ET_Modis_mm'], label= 'Avg Annnual ET-MODIS')
ax.plot(data['Year'], data['ET_SSEBop_mm'], label= 'Avg Annnual ET-SSEBop')

# ax.plot(data['Year'], data['soil_storage_change_mm'], label= 'Avg Storage')
# ax.plot(data['Year'], data['streamflow_mm'], label= 'Avg Streamflow')
# ax.plot(data['Year'], data['Cumulative_storage_change_mm'], label= 'Avg Change in Storage, mm')
# #ax.plot(data['year'], data['final_storage_change_Butler'], 'go--', linewidth=2, markersize= 6, color = 'b', label= 'Avg Change in Storage, mm')

#ax.plot(data['year'], data['Streamflow_mm_contributing_area_5500'], label= 'Avg Streamflow')

# Set axis labels and title
ax.set_xlabel('Year')
ax.set_ylabel('ET (mm)')
ax.set_title('')

# Add legend
ax.legend()
ax.legend(loc= 'lower left', fontsize = 7)  # Legend at lower left corner
# ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
#           fancybox=True, shadow=True, ncol=5)
#ax.legend(loc='upper left', bbox_to_anchor=(1, 0.5))
#ax.legend(bbox_to_anchor=(.75, 0.8))

#plt.savefig(r"D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\outputs\figures\ET_coparision_all.png", dpi=300, bbox_inches='tight') #saving plot to folder

# Display the plot
plt.show()

# ########################################
# #### Create plot for storage change
# ##########################################

# fig, ax = plt.subplots()
# ax.plot(data['year'], data['Storage_change_mm_jim'], label= 'Storage change using J. Butler approach, mm')
# ax.plot(data['year'], data['Storage_change_mm_total_watershed'], label= 'Storage change for total watershed, mm')


# #ax.plot(data['year'], data['Streamflow_mm_contributing_area_5500'], label= 'Avg Streamflow')

# # Set axis labels and title
# ax.set_xlabel('Year')
# ax.set_ylabel('Storage change, mm')
# ax.set_title('')

# # Add legend
# ax.legend()
# #ax.legend(loc='lower left', fontsize = 7)  # Legend at lower left corner
# # ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
# #           fancybox=True, shadow=True, ncol=5)
# ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# #ax.legend(bbox_to_anchor=(.75, 0.8))

# #plt.savefig(r"D:\OneDrive - Colostate\Al Fatta Smith\Pumping and water-level data\outputs\figures\storage_change_values.png", dpi=300, bbox_inches='tight') #saving plot to folder

# # Display the plot
# plt.show()







