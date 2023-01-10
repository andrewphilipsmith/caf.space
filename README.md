![Transport for the North Logo](https://github.com/Transport-for-the-North/caf.toolkit/blob/main/docs/TFN_Landscape_Colour_CMYK.png)

<h1 align="center">CAF.Space</h1>

<p align="center">
<a href="https://www.gnu.org/licenses/gpl-3.0.en.html"><img alt="License: GNU GPL v3.0" src="https://img.shields.io/badge/license-GPLv3-blueviolet.svg"></a>
<a href="https://github.com/PyCQA/pylint"><img alt="linting: pylint" src="https://img.shields.io/badge/linting-pylint-yellowgreen"></a>
<a href="https://google.github.io/styleguide/pyguide.html"><img alt="code format: Google Style Guide" src="https://img.shields.io/badge/code%20style-Google%20Style%20Guide-blue"></a>
<a href="https://github.com/psf/black"><img alt="code style: black" src="https://img.shields.io/badge/code%20format-black-000000.svg"></a>
</p>

Common Analytical Framework (CAF) Space contain geo-processing functionality useful
for transport planners. Primarily it is a tool for generating standard weighting
translations in `.csv` format describing how to convert between different zoning systems.
The aim is to free tools up from directly having to do their own geo-processing, and
instead have a single source of truth to get them from!

<u><h4> Tool info </h4></u>
The tool has two main options for running a translation, either a purely spatial translation (where overlapping zones are split by area), or a weighted translation where overlapping zones are split by some other type of weighting data like population or employment data. for most purposes a weighted translation will be more accurate, and it is up to the user to decide the most appropriate weighting data to use. For both types of translation the tool runs from a config file (a file called config.yml in the base folder). Parameters for this config are described below.

<u><h4> Spatial Correspondence </h4></u>
For a sptial correspondence, the only user inputs needed are shapefiles for the two zone systems you want a translation between. The parameters required for a spatial translation are as follows:

<b> zone_1:
  name:</b> The name of the first zone system you are providing. This should be as simple as possible, so for and MSOA shapefile, name should simply be MSOA
  <b>shapefile:</b> A file path to the shapefile you want a translation for
  <b>id_col:</b> The name of the unique ID column in your chosen shapefile. This can be anything as long as it is unique for each zone in the shapefile
<b> zone_2: Parameters the same as for zone_1, it doesn't matter which order these are in, a two way translation will be created.</b>
<b>output_path:</b> File path to where you want your translation saved. If the path provided doesn't exist it will be created, but it's best to check first to avoid surprises.
<b>cache_path:<b/> File path to a cache of existing translations. This defaults to a location on a network drive, and it is best to keep it there, but it's more important for weighted translations.
<b>tolerance:</b> This is a float less than 1, and defaults to 0.98. If filter_slivers (explained below) is chosen, tolerance controls how big or small the slithers need to be to be rounded away. For most users this can be kept as is.
<b>rounding:</b> True or False. Select whether or not zone totals will be rounded to 1 after the translation is performed. Recommended to keep as True.
<b>filter_slithers:</b> True or False. Select whether very small overlaps between zones will be filtered out. This accounts for zone boundaries not aligning perfectly when they should between shapefiles, and the tolerance for this is controlled by the tolerance parameter. With this parameter set to false translations can be a bit messy.

The translation will be output as a csv to your output path location, in a folder named by the names selected for each zone system. Along with the csv will be a yml file containing the parameters th translation was run with, along with the date of the run.

<u><h4> Weighted Correspondence </h4></u>
For a weighted translation more parameters must be provided. The weighted translation is carried out by first producing spatial translations between each primary zone system and a lower zone system. The tool will search the cache for an existing lower translation first, which is why it is preferable to keep cache_path pointing to the network drive where existing translations exist. Once these lower translations are created / loaded the lower weighting data is used to produce a weighted translation between the two primary zone systems. Below are the additional parameters.

<b>zone_1/zone_2:
  lower_translation:</b> This is an optional parameter providing a path to an existing translation between the respective zone and the lower zone. Almost the entire run time of the tool is creating these lower translations so it is worth providing this if you have it. Alternatively if this translation has previusly been created and saved in the cache, the tool should find it and use it.
<b>lower_zoning:</b> The first three parameters for this are the same as for zones 1 and 2
  weight_data: File path to the weighting data for the lower zone system. This should be saved as a csv, and only needs two columns (an ID column and a column of weighting data)
  <b>data_col:</b> The name of the column in the weighting data csv containing the weight data.
  <b>weight_id_col:</b> The name of the columns in the weighting data containing the zone ids. This will be used to join the weighting data to the lower zoning, so the IDs must match, but the names of the ID columns may be different.
<b>method:</b> The name of the methud used for weighting (e.g. pop or emp). This can be anything, but must be included as the tool checks if this parameter exists to decide whether to perform a spatial or weighted translation.

