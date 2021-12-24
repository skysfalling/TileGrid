from tile import Tile
import random

white = (255, 255, 255)
black = (0, 0, 0)
light_grey = (80, 86, 94)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)


class Grid:
    def __init__(self, hRadius, vRadius):
        #start tile
        self.array = [[Tile([0, 0], ".")]]
        self.tiles = []
        self.hRadius = hRadius
        self.vRadius = vRadius
        self.horzDiameter = (self.hRadius * 2) + 1
        self.vertDiameter = (self.vRadius * 2) + 1
        self.startTile = Tile([-hRadius + 2, -vRadius + 2])
        self.endTile = Tile([hRadius - 2, vRadius - 2])

        self.tiles.append(self.startTile)
        self.tiles.append(self.endTile)

        self.ResetGridSize()

    def clear(self):
      for y in range(self.vertDiameter):
        for x in range (self.horzDiameter):
          self.array[x][y].reset()

# =========== CREATE TILES ===========================

    def AddTile(self, x, y, type, color = None):
        #print("<<NEW TILE (", x, y, ") >>")

        radiusReset = False

        #<<<if tile point is outside current grid height>>>
        if abs(y) > self.vRadius:
            #set to new width & radius
            self.vRadius = abs(y)
            #print("set vRadius to ", self.vRadius)
            radiusReset = True

        # <<<if tile point is outside current grid width>>>
        if abs(x) > self.hRadius:
            #set to new width & radius
            self.hRadius = abs(x)
            #print("set hRadius to ", self.hRadius)
            radiusReset = True

        if radiusReset:
            self.ResetGridSize()  #Reset Grid so it matches the necessary size
            self.horzDiameter = (self.hRadius * 2) +1 #reset diameters
            self.vertDiameter = (self.vRadius * 2) +1

        newTile = Tile([x, y], type, color)  #create variable
        self.tiles.append(newTile)  #add to tile list
        gridArrayIndex = self.CoordToArrayIndex(
            newTile.position)  #get array index of coordinates
        self.array[gridArrayIndex[0]][
            gridArrayIndex[1]] = newTile  #set index to new tile

    def ResetGridSize(self):
        print("hD:",self.horzDiameter)
        print("vD:",self.vertDiameter)
        # CREATE EMPTY ROWS =============================================
        self.array = [[Tile([0, 0], ".")]]  #reset grid

        for r in range(self.vRadius):
            self.array.insert(0, [Tile([0, r + 1])])  #positive numbers
            self.array.append([Tile([0, -(r + 1)])])  #negative numbers

        # for all positive rows
        for i in range(self.vRadius):
            r = -(i - self.vRadius)
            for j in range(self.hRadius):
                self.array[i].append(Tile([j + 1, r]))
                self.array[i].insert(0, Tile([-(j + 1), r]))
        # for all negative rows
        for i in range(self.vRadius + 1):
            r = i + self.vRadius
            for j in range(self.hRadius):
                self.array[r].append(Tile([j + 1, -i]))
                self.array[r].insert(0, Tile([-(j + 1), -i]))

        #place tiles in their spots
        for tile in self.tiles:
            tileIndex = self.CoordToArrayIndex(tile.position)
            #print("tile coord:", tile.position, "index:", tileIndex)
            self.array[tileIndex[0]][tileIndex[1]] = tile
            tile.index = tileIndex #set tile index

        #set start and end tiles
        self.AddTile(self.startTile.x, self.startTile.y, "s", green) #set start point
        self.AddTile(self.endTile.x, self.endTile.y, "e", red) #set end point

        #set the neighbors for each tile in grid
        self.SetAllNeighbors()



# ============= SET TILE VALUES ==========================================

    def GetTileNeighbors(self, x, y):
        possibleNeighbors = [self.GetTile(x - 1, y), self.GetTile(x + 1, y), self.GetTile(x, y - 1), self.GetTile(x, y + 1)]
        #print(x, ",", y, ":")
        trueNeighbors = []
        for n in possibleNeighbors:
            if n != None and n.type == "x":
                trueNeighbors.append(n)
                #print("    ", n.position)
        return trueNeighbors

    def SetAllNeighbors(self):
      for y in range(self.vertDiameter):
        for x in range(self.horzDiameter):
          tile = self.array[x][y]
          tile.neighbors = self.GetTileNeighbors(tile.x, tile.y)

    def GetTile(self, x, y):
        tileIndex = self.CoordToArrayIndex([x,y])

        if tileIndex[0] >= 0 and tileIndex[0] < self.horzDiameter and tileIndex[1] >= 0 and tileIndex[1] < self.vertDiameter:
            #print("Get Tile:", tileIndex)
            return self.array[tileIndex[0]][tileIndex[1]]
        else: return None

    def CoordToArrayIndex(self, coord):
        x = coord[0]
        y = coord[1]

        #translate y coordinates to double array
        row = self.vRadius  #if y == 0
        if (y < 0): row = self.vRadius + abs(y)
        elif (y > 0): row = self.vRadius - y

        #translate x coordinates to double array
        col = x + self.hRadius

        return [row, col]

    def Randomize(self, scale):
      self.clear()
      for y in range(self.vertDiameter):
          for x in range(self.horzDiameter):
              tile = self.array[x][y]
              randInt = random.randint(0, 10)

              if randInt < scale: 
                self.AddTile(tile.x, tile.y, "x", white)

      self.AddTile(self.startTile.x, self.startTile.y, "s", green) #set start point
      self.AddTile(self.endTile.x, self.endTile.y, "e", red) #set end point
      self.SetAllNeighbors()


# ======== MUTATION ====================================================
    def Mutate(self):

      #first pass over ... fill in empty holes
      for y in range(self.vertDiameter):
          for x in range(self.horzDiameter):
              tile = self.array[x][y]
              n_count = len(tile.neighbors)

              if tile.type == "x" and tile.color != white:
                tile.color = white

              if tile.type == "." and n_count >= 2:
                tile.type = "x"
                tile.color = blue

      '''#second pass over ... eliminate eye sores
      for y in range(self.vertDiameter):
          for x in range(self.horzDiameter):
              tile = self.array[x][y]
              n_count = len(tile.neighbors)

              if tile.type == "x" and n_count == 0:
                tile.type = "."
                tile.color = None'''

      self.SetAllNeighbors()



# ========================================================

    def __str__(self):
        #print("Grid Horizontal Radius: ", self.hRadius)
        print("Start:", self.startTile.position)
        print("End:", self.endTile.position)

        for row in range((self.vRadius * 2) + 1):
            for col in range((self.hRadius * 2) + 1):
                print(self.array[row][col], " ", end="")
            print()
        return ""