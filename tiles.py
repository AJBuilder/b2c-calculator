from _types import Tile, City
from typing import Literal

# Just an example of what a tile would look like?
class TavernTile(Tile):
    type: Literal['food', 'beverage', 'lodging', 'music']
    
    def calculate(self, city: City):
        '''Return the number of points for this tile.'''
        pass