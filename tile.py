
class Tile:
  def __init__(self, point, type = "."):
    self.gridPoint = [point[0], point[1]]
    self.x = self.gridPoint[0]
    self.y = self.gridPoint[1]
    self.type = type
    self.neighbors = []
  
  def reset(self):
    self.type = "."

  def __str__(self):
    return str(self.type) #+ str(self.gridPoint) 

  #def __repr__(self):
    #return str(self.type) + str(self.gridPoint[0])


