import datetime
from pathlib import Path
from caf.space import config_base

class weight_metadata(config_base.BaseConfig):
    """
    Class for storing metadata avout weighting date

    Args:
        config_base (_type_): _description_
    """
    data_col: str
    id_col: str
    year: int
    type: str
    
class shapefile_metadata(config_base.BaseConfig):
    """
    Class for creating, storing and loading metadata relating to shapefiles used for 
    translations.
    Args:
        config_base (_type_): _description_
    """
    name: str
    path: Path
    id_col: str
    weighting_data: weight_metadata = None

class lower_trans_log(config_base.BaseConfig):
    zone_shapefile: Path
    lower_shapefile: Path
    date: datetime.datetime

class lower_metadata(config_base.BaseConfig):
    translations : list[lower_trans_log]


