import os
import pygame
from grid import Grid
import time

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0,255,0)
light_grey = (80, 86, 94)
dark_green = (0, 150, 0)
purple = (255, 0, 255)


dis_width = 600
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))


# ===============================================================

#                        UTILITIES

# ===============================================================

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


# ===============================================================

#                        VISUALS

# ===============================================================

def DisplayGrid(grid, display, dis_width, dis_height, box_size = 15):
  #print("Grid Display Radius ", grid.hRadius, grid.vRadius)
  tiles_changed = False

  #for each index in double array
  for y in range(grid.vertDiameter):
    for x in range(grid.horzDiameter):

      #create rectangles
      tile = grid.array[x][y]

      if tile.type_changed:
        tiles_changed = True
        continue

  if tiles_changed:
    display.fill(black)

    #for each index in double array
    for y in range(grid.vertDiameter):
      for x in range(grid.horzDiameter):

        #create rectangles
        tile = grid.array[x][y]


        tilePos = [dis_width/2 + (tile.position[0] * box_size) - box_size/2, dis_height/2 - (tile.position[1] * box_size) - box_size/2]
        tile.rect = pygame.Rect(tilePos[0], tilePos[1], box_size, box_size)

        # add rect to display rects array for mouse click check
        grid.display_rects.append(tile.rect)


        if tile.type == ".":
          pygame.draw.rect(display, white, tile.rect, 1)
        elif tile.color != None:
          pygame.draw.rect(display, tile.color, tile.rect)

        if box_size > 25:
          totalText = SetText(str(tile.position), tilePos[0] + (box_size/2), tilePos[1] + (box_size/2), 7)
          display.blit(totalText[0], totalText[1])

        #reset type changed
        tile.type_changed = False

    pygame.display.flip()



def UpdateGrid(scale = 45):
  DisplayGrid(grid, dis, dis_width, dis_height, scale)
  clock.tick(60)


def SetText(string, coordx, coordy, fontSize): #Function to set text
  font = pygame.font.Font('freesansbold.ttf', fontSize) 
  #(0, 0, 0) is black, to make black text
  text = font.render(string, True, white) 
  textRect = text.get_rect()
  textRect.center = (coordx, coordy) 
  return (text, textRect)

# ===============================================================

#                        ASTAR

# ===============================================================
class Node():
  def __init__(self, coord, parent = None):
    self.f = 0
    self.g = 0
    self.h = 0
    self.coord = coord
    self.parent = parent

def return_coord_path(current_node):
  path = []
  current = current_node
  while current is not None:
      path.append(current.coord)
      current = current.parent
  # Return reversed path
  return path[::-1]

def return_node_path(current_node):
  path = []
  current = current_node
  while current is not None:
      path.append(current)
      current = current.parent
  # Return reversed path
  return path[::-1]

def Get_Node_Path_F(node_path):
  f = 0
  for node in node_path:
    f += node.f
  return f

def Display_Path_From_Node(grid, current_node, closed_list = None):
  path = return_coord_path(current_node)
  #print("display path: ", path)

  if closed_list != None:
    for node in closed_list:
      tile_type = grid.GetTile(node.coord[0], node.coord[1]).type
      if tile_type != "b":
        grid.AddTile(node.coord[0], node.coord[1], ":", light_grey)

  for coord in path:
    #if not displayed as best path, don't change
    tile_type = grid.GetTile(coord[0], coord[1]).type
    if tile_type != "b":
      grid.AddTile(coord[0], coord[1], "p", dark_green)



  UpdateGrid()

def Display_Node_Path(grid, node_path, closed_list = None):
  path = []

  for node in node_path:
    path.append(node.coord)

  if closed_list != None:
    for node in closed_list:      
      tile_type = grid.GetTile(node.coord[0], node.coord[1]).type
      if tile_type != "b" and tile_type != "p":
        grid.AddTile(node.coord[0], node.coord[1], ":", light_grey)


  for coord in path:
    tile_type = grid.GetTile(coord[0], coord[1]).type
    grid.AddTile(coord[0], coord[1], "p", dark_green)

  UpdateGrid()

def Set_Best_Paths(current_node, best_paths):

  current_node_path = return_node_path(current_node)

  # if best paths empty, set to path from current Node
  if len(best_paths) == 0:
    best_paths = [current_node_path]
  else:

    # get current path f
    current_path_f = Get_Node_Path_F(current_node_path)

    # get lowest f in best paths
    best_paths_f = -1
    for path in best_paths:
      if Get_Node_Path_F(path) < best_paths_f or best_paths_f == -1:
        best_paths_f = Get_Node_Path_F(path)

    #print(">> best path f: ", best_paths_f)

    #if current node path f < best paths f OR best_paths_f == 0
    #   or length of current node path is greater than best path
    if current_path_f < best_paths_f or best_paths_f == 0 or len(current_node_path) > len(best_paths[0]):
      best_paths = [current_node_path]
    
    elif current_path_f == best_paths_f:
      # best paths append current node path
      best_paths.append(current_node_path)
  
  #print best paths
  #print("\n>>best path length: ", len(best_paths))
  #print(">>best path: [", end="")
  #for node in best_paths[0]:
    #print("["+ str(node.coord[0]) + "," + str(node.coord[1]) + "]", end="")
  #print("]")

  return best_paths

def Find_Node_Closest_To_End(node_list, end):
  closest = None

  for node in node_list:
    if closest == None or closest.h == 0:
      closest = node
    elif node.h <= closest.h:
      closest = node

  grid.AddTile(closest.coord[0], closest.coord[1], "c", purple)

  #if closest_to_end != None:
    #print("Closest Node To End: ", closest_to_end.coord, "h: ", closest_to_end.h)
  
  return closest

def Find_ASTAR_Path(grid, start_coord, end_coord, diagonal_movement = False):

  print("\nASTAR => start_coord: ", start_coord, "end_coord: ", end_coord)
  if diagonal_movement: print(">>>> diag move allowed")
  #create start/end nodes
  start_node = Node(start_coord)
  end_node = Node(end_coord)

  #init open list with start node, init closed list
  open_list = [start_node]
  closed_list = []

  #init current node
  current_node = open_list[0]

  #init best paths
  best_paths = []

  # Adding a stop condition
  outer_iterations = 0
  max_iterations = (len(grid.array[0]) ** 4) // 2
  #print("MAX ITERATIONS: ", max_iterations)

  # << START OF LOOP >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  #while the open list is not empty
  while len(open_list) != 0:
    outer_iterations += 1
    #print("\n==============\nIteration: ", outer_iterations)

    # if reaches max iterations or closed list is way greater than best path
    if outer_iterations > max_iterations :
      # if we hit this point return the path such as it is
      # it will not contain the destination
      print(">>>>giving up on pathfinding too many iterations")
      Display_Path_From_Node(grid, current_node, closed_list)
      Display_Node_Path(grid, best_paths[0])
      closest_node = Find_Node_Closest_To_End(closed_list, end_node)
      Display_Path_From_Node(grid, closest_node, closed_list)
      print("Iterations: ", outer_iterations)

      return return_coord_path(current_node)  

    #find the node with the least f on the open list, call it "current_node"
    current_node = open_list[0]
    for node in open_list:

      #print nodes 
      #print(".   ", node.coord, ".f: ", node.f)

      #set current node to node with lowest f
      if node.f < current_node.f:
        current_node = node

    #pop current_node from open list
    open_list.remove(current_node)

    #add current_node to closed list
    if current_node not in closed_list:
      closed_list.append(current_node)

    #print("**new current node: ", current_node.coord)

    # ========================= UPDATE DISPLAY ==============================

    # display current_node path
    #Display_Path_From_Node(grid, current_node, closed_list)

    #get & display best path
    best_paths = Set_Best_Paths(current_node, best_paths)
    #Display_Node_Path(grid, best_paths[0], closed_list)

    #print("\n>> best paths length:", len(best_paths[0]))

    #print(">> open list length:", len(open_list))
    #print("\nOpen List: ")
    #for node in open_list: print(node.coord, end="")

    #print(">> closed list length:", len(closed_list))
    #print("Closed List: ")
    #for node in closed_list: print(node.coord, end="")
    #print()


    # ======================= CHECK IF MEETS END CONDITION ===================
    #print("\nEnd? ", current_node.coord , "=?", end_node.coord)
    #you've found end goal
    if current_node.coord == end_node.coord:
      print("End Found!")
      #Display_Path_From_Node(grid, current_node)
      Display_Node_Path(grid, best_paths[0])
      print("Iterations: ", outer_iterations)
      return return_coord_path(current_node)
      break

    # ====================== GENERATE CHILDREN OF CURRENT NODE ================
    #move options change based on allowed diagonal movement
    moveOptions = [[-1, 0], [1, 0], [0,-1], [0,1]]
    if (diagonal_movement):
      moveOptions.extend([[-1, -1], [-1, 1], [1, 1], [1, -1]])


    #set currentChildren equal to adjacent nodes from current_node
    currentChildren = []
    for opt in moveOptions:
      #get position
      new_child_coord = [current_node.coord[0] + opt[0], current_node.coord[1] + opt[1]]

      # Make sure within range
      if grid.GetTile(new_child_coord[0], new_child_coord[1]) == None:
          continue

      # Make sure walkable terrain
      tile_type = grid.GetTile(new_child_coord[0], new_child_coord[1]).type
      if tile_type == "x" or tile_type == "s":
          continue


      new_child = Node(new_child_coord, current_node)
      currentChildren.append(new_child)

    #print("\nChildren of ", current_node.coord)
    #for child in currentChildren: print("    ", child.coord)
    
    #for child in children set g, h, f
    for child in currentChildren:
      #if child already in closed list, continue
      if child in closed_list:
        continue
      
      child.g = current_node.g + 1 #distance from start node
      child.h = abs(child.coord[0] - end_node.coord[0]) + abs(child.coord[1] - end_node.coord[1]) #estimated distance from child to end node
      child.f = child.g + child.h #total cost

      #child is already in the open list
      for open_node in open_list:
        if child.coord == open_node.coord and child.g > open_node.g:
          continue

      #add child to open list
      open_list.append(child)



# ===============================================================

#                        MAIN

# ===============================================================
if __name__ == "__main__":

    pygame.init()
    clock = pygame.time.Clock()
    clearConsole()

    pygame.display.set_caption('Grid GAme')


    grid = Grid(4,4)
    print(grid)

    loop = True





    # <<<<<<<<<< MAIN UPDATE LOOP >>>>>>>>>>>>>>>>>>>>>>>

    mouse_is_dragging = False
    mouse_button_pressed = -1
    while loop:


      # ********** GET INPUTS ******************
      for event in pygame.event.get():

          if event.type == pygame.QUIT:
            print("quit")
            loop = False

          elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_is_dragging = True
            mouse_button_pressed = event.button
            
            #get mouse position
            pos = pygame.mouse.get_pos()

            # get tile from grid
            clicked_tile = None
            for tile in grid.all_tiles:
              if tile.rect != None:
                if tile.rect.collidepoint(pos):
                  #print("Mouse selected: ", tile.position)
                  clicked_tile = tile


            if clicked_tile != None:
              #if mouse button 1, create wall
              if mouse_button_pressed == 1:
                clicked_tile.color = white
                clicked_tile.type = "x"
                clicked_tile.type_changed = True
              #if mouse button 3, remove wall
              elif mouse_button_pressed == 3:
                clicked_tile.color = black
                clicked_tile.type = "."
                clicked_tile.type_changed = True


          elif event.type == pygame.MOUSEBUTTONUP:
            mouse_is_dragging = False
            mouse_button_pressed = -1

          elif event.type == pygame.MOUSEMOTION:
            if mouse_is_dragging:
              #get mouse position
              pos = pygame.mouse.get_pos()

              # get tile from grid
              clicked_tile = None
              for tile in grid.all_tiles:
                if tile.rect != None:
                  if tile.rect.collidepoint(pos):
                    #print("Mouse selected: ", tile.position)
                    clicked_tile = tile

              if clicked_tile != None:
                #if mouse button 1, create wall
                if mouse_button_pressed == 1:
                  clicked_tile.color = white
                  clicked_tile.type = "x"
                  clicked_tile.type_changed = True

                #if mouse button 3, remove wall
                elif mouse_button_pressed == 3:
                  clicked_tile.color = black
                  clicked_tile.type = "."
                  clicked_tile.type_changed = True


          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                  print("left")
              elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                  grid.Mutate()
              elif event.key == pygame.K_UP or event.key == pygame.K_w:
                  Find_ASTAR_Path(grid, grid.startTile.position, grid.endTile.position)
                  print(grid)
                  break
              elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                  print("down")
              elif event.key == pygame.K_SPACE:
                  grid.Randomize(3)

      UpdateGrid(45)



    pygame.quit()
    quit()
