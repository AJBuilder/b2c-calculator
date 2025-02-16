from pydantic import BaseModel
from cv2 import Mat
from typing import Tuple, TypeAlias, Literal
from abc import ABC, abstractmethod


class Tile(BaseModel):
    raw_image: Mat
    
    @abstractmethod
    def solve_points(self, city: "City"):
        '''Return the number of points for this tile.'''
        pass
    
TileRow: TypeAlias = Tuple[Tile, Tile, Tile, Tile, Tile]
CityTiles: TypeAlias = Tuple[TileRow, TileRow, TileRow, TileRow, TileRow]

class City(BaseModel):
    raw_image: Mat
    tiles: CityTiles
    
    
class TavernTile(Tile):
    type: Literal['food', 'beverage', 'lodging', 'music']
    
    def solve_points(self, city: "City"):
        '''Return the number of points for this tile.'''
        pass