from typing import Union

from classes import City

PathDictionaryType = Union[dict[str, list[City]], dict[str, int]] 
IndividualType = Union[dict[str, list[PathDictionaryType]], dict[str, int]]

PathType = Union[dict[str, City], dict[str, int]]

