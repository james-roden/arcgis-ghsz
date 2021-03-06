# arcgis-ghsz
An ArcGIS toolbox for caculating the base of the Gas Hydrate Stability Zone given a sea floor raster. Derived from the [Joides formula](http://www.odplegacy.org/PDF/Admin/JOIDES_Journal/JJ_1992_V18_No7.pdf).

*James M Roden*

*Version==1.0.0 // Apr 2020*

## Index
1. [Background](https://github.com/james-roden/ArcGIS-GHSZ-Tool/blob/master/README.md#background)
2. [How to Use](https://github.com/james-roden/ArcGIS-GHSZ-Tool/blob/master/README.md#how-to-use)

## Background

Gas hydrate stability zone, abbreviated GHSZ refers to a zone and depth of the marine environment at which methane clathrates (large amount of methane trapped within a crystal structure of water, forming a solid similar to ice) naturally exist in the Earth's crust. 

Stability primarily depends upon temperature and pressure, however other variables such as gas composition and ionic impurities in water influence stability boundaries.

The upper limit of the GHSZ occures at a depth of approximately 150 meters below mud line (BML) in polar regions; approximately 500 meters BML along continental regions; approximately 300 meters in oceanic sediments when the bottom water temperature is at or near 0 degrees celsius. The maximal depth (the base) of the GHSZ is limited by the geothermal gradient. Generally the maximum resides around 2000 meters BML. 

Joides algorithm for calculating the GHSZ given the water depth (meters), bottom water temperature (degrees celsius), and geothermal gradient (degrees c/km):

![JoidesFormula](https://github.com/james-roden/ArcGIS-GHSZ-Tool/blob/master/joides_alg.PNG)

## How to Use
- Ensure the sea floor raster has only positive values. 
