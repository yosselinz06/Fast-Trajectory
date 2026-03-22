#cells start unvisited
#traverse and label 70% open 30% blocked
import pygame
import random
import time
from astar import a_star #import function a_star from Astar.py
from backward_astar import backward_a_star
from Adaptive_astar import a_star_adaptive
from Menu import menu
import sys
sys.setrecursionlimit(100000) #extend recursion depth- Not needed, exceeding max ecursion depth was syntax error - Jason S

#Notes ------------------------------------------
# Class for grid squares
# object should have [x coord, y coord, g(n), h(n), f(n), parent pointer]
# Need heap (priority queue) binary
# Need 2d vector
# hash table to map keys - Store Visited nodes
# tuple??

#improve. make stack for proper recursion (iterative version). python standard recursion limit is 1000
# stack based dfs

#improve: random start/end
#improve: Tiebreaking

#improve. Make impossible mazes impossible
---------------------------------------------------

pygame.init()

ROWS = 51
COLS = 51
CELL_SIZE = 18

HEIGHT = ROWS * CELL_SIZE
WIDTH = COLS * CELL_SIZE

# Color codes - Jason S
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Node:
    def __init__(self,row,col):
        self.row = row # cell position
        self.col = col
        self.x = col * CELL_SIZE #coordinates
        self.y = row * CELL_SIZE
        self.color = WHITE
        self.neighbors = []
        self.g = float("inf") #distance from start
        self.f = float("inf")
        self.h = 0 #heruistic
        self.parent = None
        self.is_obstacle = False
        self.is_visited = False #Set all cells to unvisited

    # draw node with color and border
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, CELL_SIZE, CELL_SIZE), 1)

    #clears/updates neighbor list
    def update_neighbors(self, grid):
        self.neighbors = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dr, dc in directions: #check each neighbor
            r = self.row + dr
            c = self.col + dc

            if 0 <= r < ROWS and 0 <= c < COLS: # add if not blocked
                if not grid[r][c].is_obstacle:
                    self.neighbors.append(grid[r][c])

def create_grid(): #create 2d list of node objects  (grid)
    grid = []
    for row in range(ROWS):
        grid_row = []
        for col in range(COLS):
            grid_row.append(Node(row,col))
        grid.append(grid_row)
    return grid

#adds neighbors in grid to list.
def get_neighbors(grid, node):
    neighbors = []
    row = node.row
    col = node.col

    if row > 0:
        neighbors.append(grid[row-1][col])
    if row < ROWS-1:
        neighbors.append(grid[row+1][col])
    if col > 0:
        neighbors.append(grid[row][col-1])
    if col < COLS-1:
        neighbors.append(grid[row][col+1])

    return neighbors
    #random.shuffle(neighbors) #randomizes search order. check if needed

# DFS algorithm recursive - Jason S
def dfs_label(grid, node, force_open=False): # implicit stack - resarch more - Jason S
    if node.is_visited: #stop when every node visited
        return

    node.is_visited = True #

    if force_open: # Force open start
        node.is_obstacle = False
        node.color = WHITE
    else:
        #Set blocked if random < 0.3
        if random.random() < 0.3: # Gen ran floating point 0-1 - Jason S
            node.is_obstacle = True
            node.color = BLACK
            return
        else:
            node.is_obstacle = False
            node.color = WHITE
    #recursive part: set curr to parent and run recursively (parent pointer)
    for neighbor in get_neighbors(grid, node): #problem here? - Jason S
        if not neighbor.is_visited:
            neighbor.parent = node
            dfs_label(grid, neighbor)

# Create the actual maze with blocks
def create_grid_dfs(grid):
    #force cells open
    dfs_label(grid, grid[0][0], force_open=True) #start first cell no block - Jason S

    for row in grid: #
        for node in row:
            if not node.is_visited:
                dfs_label(grid, node)

def draw_grid(screen, grid):
    screen.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(screen)
    pygame.display.flip()

# Make sure start/end have at least 1 open neighbor - Jason S
def has_move(grid, node):
    for neighbor in get_neighbors(grid, node):
        if not neighbor.is_obstacle:
            return True
    return False


    # randomize end - Jason S
def randomize_grid(grid):
    loop = True
    while loop == True:
        start = grid[random.randint(0, 50)][random.randint(0, 50)]
        end = grid[random.randint(0, 50)][random.randint(0, 50)]

        while start == end:  # change if to while. randomize again if start and end are same cell - Jason S
            end = grid[random.randint(0, 50)][random.randint(0, 50)]

        start.is_obstacle = False
        end.is_obstacle = False

        #man distance - Jason S
        if abs(start.row - end.row) + abs(start.col - end.col)< 80:
            continue

        if has_move(grid, start) == True and has_move(grid, end) == True:
            loop = False
            start.color = BLUE
            end.color = GREEN

    return start, end

def run_astar(grid):
    running = True
    #start = grid[0][0]
    # randomize start - Jason S
    start, end = randomize_grid(grid)

    for row in grid:
        for node in row:
            node.update_neighbors(grid)

    found = a_star(grid, start, end)

    if not found:
        print("No Path. Impossible maze")

    while running:
        # screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw_grid(screen, grid)
        clock.tick(60)

def run_astar_30(grid):
    start, end = randomize_grid(grid)

    for row in grid:
        for node in row:
            node.update_neighbors(grid)

    found = a_star(grid, start, end)

    if not found:
        print("No Path. Impossible maze")
    #added
    screen.fill(WHITE)
    draw_grid(screen, grid)
    pygame.display.flip()
    return screen.copy()

def run_astar_back(grid):
    running = True
    #start = grid[0][0]
    # randomize start - Jason S
    start, end = randomize_grid(grid)

    for row in grid:
        for node in row:
            node.update_neighbors(grid)

    found = backward_a_star(grid, start, end)

    if not found:
        print("No Path. Impossible maze")

    while running:
        # screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw_grid(screen, grid)
        clock.tick(60)

def run_astar_adaptive(grid, runs):
    running = True
    #start = grid[0][0]
    # randomize start - Jason S
    start, end = randomize_grid(grid)

    for i in range(runs): #Pick nw start
        start = grid[random.randint(0, 50)][random.randint(0, 50)]
        while start == end or start.is_obstacle or abs(start.row - end.row) + abs(start.col - end.col)< 80:
            start = grid[random.randint(0, 50)][random.randint(0, 50)]

        for row in grid:
            for node in row:
                if node !=end:
                    if node.is_obstacle:
                        node.color =BLACK
                    else:
                        node.color = WHITE
        start.color = BLUE
        end.color = GREEN

        for row in grid:
            for node in row:
                node.update_neighbors(grid)

        # Get time of each run - Jason S
        start_time = time.perf_counter()
        #visited = a_star_adaptive(grid, start, end)
        expanded = a_star_adaptive(grid, start, end)
        end_time = time.perf_counter()
        total_time = (end_time-start_time) * 1000

        found = a_star_adaptive(grid, start, end)
        if not found:
            print("No path")
        else:
            print(f"Success! Time: {total_time} ms")
            #print(f"Nodes visited: {visited} ")
            print(f"Nodes expanded: {expanded} ")


        #draw_grid(screen, grid)
        #pygame.time.delay(100) Don't use this, need code to refresh screen every run - Jason S

        # Section to refresh screen after each 'run; - Jason S
        start_time = pygame.time.get_ticks() # get ticks prevents freezing - Jason S

        while pygame.time.get_ticks() - start_time < 5000: # change 1delay to 5 seconds - Jason S
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            draw_grid(screen, grid)
            pygame.display.flip()
            clock.tick(60)

    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running = False

        draw_grid(screen, grid)
        clock.tick(60)

#AI Section --------------------------------------------------------------------------
def make_thumbnail(grid, thumb_width, thumb_height):
    thumb = pygame.Surface((thumb_width, thumb_height))
    thumb.fill(WHITE)

    cell_w = thumb_width / COLS
    cell_h = thumb_height / ROWS

    for r in range(ROWS):
        for c in range(COLS):
            node = grid[r][c]

            x1 = round(c * cell_w)
            y1 = round(r * cell_h)
            x2 = round((c + 1) * cell_w)
            y2 = round((r + 1) * cell_h)

            pygame.draw.rect(
                thumb,
                node.color,
                (x1, y1, max(1, x2 - x1), max(1, y2 - y1))
            )
    return thumb
 # End AI Section----------------------------------------------------------------------


if __name__ == "__main__":

    # This creates the screen. pygame.draw uses this as a canvas - Jason S
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DFS")
    clock = pygame.time.Clock()

    option = menu()
    # Run astar - put this before running - Jason S
    if option == 1:
        grid = create_grid()
        create_grid_dfs(grid)
        run_astar(grid)

    # run astar x 30
    if option == 2:
        col = 6
        row = 5
        width = 255
        height = 255
        pad = 5 # add padding for cleaner output - Jason S
        all_output = pygame.Surface((col * width +(col-1) * pad, row * height + (row-1)*pad))
        all_output.fill(WHITE)

        for i in range(30):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            grid = create_grid()
            create_grid_dfs(grid)
            #snapshot = run_Astar_30(grid)
            run_astar_30(grid)

            #Scale snapshot
            #small_snapshot = pygame.transform.scale(snapshot, (width, height))
            small_snapshot = make_thumbnail(grid, width, height)

            x = (i % col) * (width+pad)
            y = (i // col) * (height+pad)
            all_output.blit(small_snapshot, (x, y))  # blit? - Jason S
            pygame.draw.rect(all_output, BLACK, (x,y,width,height),2)

        pygame.image.save(all_output, "a_star Output.png")
        print("Save success")

        preview = pygame.transform.scale(all_output, (WIDTH, HEIGHT))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill(WHITE)
            screen.blit(preview, (0, 0))
            pygame.display.flip()
            clock.tick(60)

    if option == 3:
        grid = create_grid()
        create_grid_dfs(grid)
        run_astar_back(grid)

    if option == 4:
        grid = create_grid()
        create_grid_dfs(grid)
        runs = int(input("Enter numbr of runs: "))
        run_astar_adaptive(grid, runs)

pygame.quit()



