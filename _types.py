from pydantic import BaseModel
from cv2 import Mat
from typing import Tuple, TypeAlias
from abc import ABC, abstractmethod


class Tile(BaseModel, ABC):
    
    @classmethod
    def from_image(cls, raw_image: Mat) -> "Tile":
        pass
    
    @abstractmethod
    def calculate(self, city: "City"):
        '''Return the number of points for this tile.'''
        pass
    
TileRow: TypeAlias = Tuple[Tile, Tile, Tile, Tile, Tile]
CityTiles: TypeAlias = Tuple[TileRow, TileRow, TileRow, TileRow, TileRow]
class City(BaseModel):
    tiles: CityTiles
    
    @classmethod
    def from_image(cls, raw_image: Mat) -> "City":
        pass
    
    def calculate(self):
        '''Return the score for the city.'''
        pass
    