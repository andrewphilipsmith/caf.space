# -*- coding: utf-8 -*-
"""
    Module containing functionality for storing
    input parameters and reading config file.
"""

##### IMPORTS #####
from __future__ import annotations

# Standard imports
import logging
import configparser
import dataclasses
from pathlib import Path
from typing import Any, Dict, Union
from caf.space import config_base

# Third party imports

# Local imports

##### CONSTANTS #####
LOG = logging.getLogger(__name__)

@dataclasses.dataclass
class ShapefileInfo:
    """Base class for storing information about a shapefile input."""

    name: str
    shapefile: Path
    id_col: str

    def __post_init__(self) -> None:
        self.name = str(self.name)
        self.shapefile = Path(self.shapefile)
        # if not self.shapefile.is_file():
        #     raise FileNotFoundError(
        #         f"cannot find {self.name} shapefile: {self.shapefile}"
        #     )

@dataclasses.dataclass
class ZoneSystemInfo(ShapefileInfo):
    """Zone system input data for `ZoneTranslationInputs`.

    Parameters
    ----------
    name : str
        Name of the zone system.
    shapefile : Path
        Path to the shapefile.
    id_col : str
        The name of the column in the shapefile you want to use as ID
    lower_translation : Path, optional
        Path to a lower level translation.

    Raises
    ------
    FileNotFoundError
        If either of the paths given don't
        exist.
    """

    lower_translation: Path = None

    # def __post_init__(self) -> None:
    #     super().__post_init__()
    #     if self.lower_translation is None:
    #         return
    #     self.lower_translation = Path(self.lower_translation)
        # if not self.lower_translation.is_file():
        #     raise FileNotFoundError(
        #         f"cannot find {self.name} lower "
        #         f"translation file: {self.lower_translation}"
        #     )

@dataclasses.dataclass
class LowerZoneSystemInfo(ShapefileInfo):
    """Lower level zone system input data for `ZoneTranslationInputs`.

    Parameters
    ----------
    name : str
        Name of the zone system.
    shapefile : Path
        Path to the shapefile.
    id_col : str
        The name of the column in the shapefile you want to use as ID
    weight_data : Path
        Path to weighting data.
    data_col: str
        Name of the column containing weighting data.
    weight_id_col: str
        The name of the column in the weighting data you want to use as ID

    Raises
    ------
    FileNotFoundError
        If either of the paths given don't
        exist.
    """

    weight_data: Path
    data_col: str
    weight_id_col: str

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.weight_data is None:
            return
        self.weight_data = Path(self.weight_data)
        # if not self.weight_data.is_file():
        #     raise FileNotFoundError(
        #         f"cannot find {self.name} weight data: {self.weight_data}"
        #     )
    
    def _lower_to_higher(self) -> ZoneSystemInfo:
        return ZoneSystemInfo(name = self.name,
        shapefile = self.shapefile,
        id_col = self.id_col)


class ZoningTranslationInputs(config_base.BaseConfig):
    """Class for storing and reading input parameters for `ZoneTranslation`.

    Attributes
    ----------
    zone_1 : ZoneSystemInfo
        Zone system 1 information
    zone_2 : ZoneSystemInfo
        Zone system 2 information
    output_path : Path
        Folder to save outputs to.
    existing_translation : Path, optional
        Path to an existing zone tranlation.
    method : str, optional
        Method for zone correpondence calculation.
    tolerance : float, default 0.98
        Tolerance for rounding and filtering.
    point_handling : bool, default True
        Should point handling be ran.
    point_tolerance : float, default 0.95
        Tolerance for determining point zones.
    point_zones_path : Path, optional
        Path to list of point zones.
    rounding : bool, default True
        Should rounding be done on outputs.
    filter_slithers : bool, True
        Should slithers be filtered out.
    lower_zoning : LowerZoneSystemInfo, optional
        Information about the lower zone system.
    """

    zone_1: ZoneSystemInfo
    zone_2: ZoneSystemInfo
    lower_zoning: LowerZoneSystemInfo
    output_path: Path
    cache_path: Path
    existing_translation: Path = None
    method: str = None
    tolerance: float = 0.98
    point_handling: bool = True
    point_tolerance: float = 0.95
    point_zones_path: Path = None
    rounding: bool = True
    filter_slithers: bool = True
    

    _CONFIG_SECTION: str = dataclasses.field(
        default="ZONING TRANSLATION PARAMETERS", init=False, repr=False
    )

    def __post_init__(self) -> None:
        self.output_path = Path(self.output_path)
        self.output_path.mkdir(exist_ok=True, parents=True)
        # TODO Add more validation checks for parameters

    @staticmethod
    def _path_none(value: str) -> Union[Path, None]:
        """Convert string to Path, or None if empty."""
        if value is None or value.strip() == "":
            return None
        return Path(value)

    @classmethod
    def _check_config_parameters(cls, config: configparser.ConfigParser) -> None:
        """Check `config` contains all mandatory options.

        Looks in section `cls._CONFIG_SECTION`.

        Parameters
        ----------
        config : configparser.ConfigParser
            Config parser after reading data from file.

        Raises
        ------
        configparser.NoOptionError
            If any mandatory options are missing.
        """
        mandatory_options = [
            f"zone_{i}_{j}" for i in (1, 2) for j in ("name", "shapefile")
        ]
        mandatory_options.append("output_path")
        for opt in mandatory_options:
            if not config.has_option(cls._CONFIG_SECTION, opt):
                raise configparser.NoOptionError(opt, cls._CONFIG_SECTION)

def write_example(out_path: Path):
    zones = {}
    for i in range(1,3):
        zones[i] = ZoneSystemInfo(name = f"zone_{i}_name", shapefile = Path(f"path/to/shapefile_{i}"), id_col = f"id_col_for_zone_{i}", lower_translation= Path(f"path/to/lower_trans_{i}"))
    lower = LowerZoneSystemInfo(name = "lower_zone_name", shapefile = Path("path/to/lower/shapefile"), id_col = "id_col_for_lower_zone", weight_data=Path("path/to/lower/weight/data"), data_col="data_col_name", weight_id_col = "id_col_in_weighting_data")
    ex = ZoningTranslationInputs(zone_1=zones[1],
    zone_2 = zones[2],
    lower_zoning = lower,
    output_path = r"path\to\output\folder",
    existing_translation = r"OPTIONAL\path\to\existing\translation",
    method = "OPTIONAL name of method",
    point_zones_path = r"OPTIONAL\path\to\list\of\point\zones"
    )
    ex.save_yaml(out_path)