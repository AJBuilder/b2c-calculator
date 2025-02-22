from pydantic import BaseModel
from cv2 import Mat
from typing import Tuple, TypeAlias, Literal
from abc import ABC, abstractmethod

class Tile(BaseModel, ABC):
    
    @classmethod
    @abstractmethod
    def calculate(cls, city: "City"):
        '''Return the number of points for this type of tile in this city.'''
        pass
    
TileRow: TypeAlias = Tuple[Tile, Tile, Tile, Tile, Tile]
CityTiles: TypeAlias = Tuple[TileRow, TileRow, TileRow, TileRow, TileRow]
class City(BaseModel):
    tiles: CityTiles
    
    @classmethod
    def from_image(cls, raw_image: Mat) -> "City":
        pass
    
    # Alex: Probably a "from_json" function to aid in developing the scoring?
    # BaseModel has model_dumps_json to get a template, then you can modify the JSON to your needs.
    
    def calculate(self):
        '''Return the score for the city.'''
        pass
    
# Just an example of what a tile would look like?
class TavernTile(Tile):
    type: Literal['food', 'beverage', 'lodging', 'music']
    
    
    def calculate(cls, city: City):
        '''Return the number of points for this type of tile in this city.'''
        pass
    
    
    
if __name__ == "__main__":
    pass