import os
import pygame
import random
from grid import Grid
from astar import astar
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

#UTILITIES ============================

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

# VISUALS =======================================

def DisplayGrid(grid, display, dis_width, dis_height, scale = 15):
  #print("Grid Display Radius ", grid.hRadius, grid.vRadius)
  boxSize = scale

  #for each index in double array
  for y in range(grid.vertDiameter):
    for x in range(grid.horzDiameter):
      tile = grid.array[x][y]
      tilePos = [dis_width/2 + (tile.position[0] * boxSize) - boxSize/2, dis_height/2 - (tile.position[1] * boxSize) - boxSize/2]
      rect = pygame.Rect(tilePos[0], tilePos[1], boxSize, boxSize)

      if (tile.type != "." and tile.color != None):
        pygame.draw.rect(display, tile.color, rect)
      else:
        pygame.draw.rect(display, white, rect, 1)

      totalText = SetText(str(tile.position), tilePos[0] + (boxSize/2), tilePos[1] + (boxSize/2), 7)
      display.blit(totalText[0], totalText[1])

def SetText(string, coordx, coordy, fontSize): #Function to set text

    font = pygame.font.Font('freesansbold.ttf', fontSize) 
    #(0, 0, 0) is black, to make black text
    text = font.render(string, True, white) 
    textRect = text.get_rect()
    textRect.center = (coordx, coordy) 
    return (text, textRect)


#MAIN ======================================
if __name__ == "__main__":

    pygame.init()
    clearConsole()

    dis_width = 600
    dis_height = 600

    dis = pygame.display.set_mode((dis_width, dis_height))
    pygame.display.set_caption('Grid GAme')

    grid = Grid(10,10)
    path = None
    print(grid)

    loop = True
    while loop:  # making a loop
      #INPUTS
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              print("quit")
              loop = False
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                  print("left")
              elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                  grid.Mutate()
              elif event.key == pygame.K_UP or event.key == pygame.K_w:
                  path = astar(grid, grid.startTile.index, grid.endTile.index)
                  print(path)
              elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                  print("down")
              elif event.key == pygame.K_SPACE:
                  grid.Randomize(3)

      dis.fill(black)
      DisplayGrid(grid, dis, dis_width, dis_height, 25)
      pygame.display.update()

    pygame.quit()
    quit()
