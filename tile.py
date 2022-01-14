
class Tile:
  def __init__(self, point, type = ".", color = None):
    self.position = [point[0], point[1]]
    self.index = None
    self.x = self.position[0]
    self.y = self.position[1]
    self.type = type
    self.type_changed = True
    self.color = color
    self.neighbors = []
    self.rect = None
  
  def reset(self):
    self.type = "."

  #def CoordToIndex(self):


  def __str__(self):
    return str(self.type) #+ str(self.position) 

  #def __repr__(self):
    #return str(self.type) + str(self.gridPoint[0])


