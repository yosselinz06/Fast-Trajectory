#cells start unvisited
#traverse and label 70% open 30% blocked
import pygame
import random
from Astar import a_star #import function a_star from Astar.py
from Menu import menu
import sys
sys.setrecursionlimit(100000) #extend recursion depth


# Class for grid squares
# object should have [x coord, y coord, g(n), h(n), f(n), parent pointer]
# Need heap (priority queue) binary
# Need 2d vector
# hash table to map keys - Store Visited nodes
# tuple??

#improve. make stack for proper recursion (iterative version). python standard recursion limit is 1000
# stack based dfs

#improve. Make impossible mazes impossible

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
        self.row = row
        self.col = col
        self.x = col * CELL_SIZE
        self.y = row * CELL_SIZE
        self.color = WHITE
        self.neighbors = []
        self.g = float("inf")
        self.f = float("inf")
        self.h = 0
        self.parent = None
        self.is_obstacle = False
        self.is_visited = False #Set all cells to unvisited

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, CELL_SIZE, CELL_SIZE), 1)

    def update_neighbors(self, grid):
        self.neighbors = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dr, dc in directions:
            r = self.row + dr
            c = self.col + dc

            if 0 <= r < ROWS and 0 <= c < COLS:
                if not grid[r][c].is_obstacle:
                    self.neighbors.append(grid[r][c])

    def __lt__(self, other): #what does this do?
        return self.f < other.f

def create_grid():
    grid = []
    for row in range(ROWS):
        grid_row = []
        for col in range(COLS):
            grid_row.append(Node(row,col))
        grid.append(grid_row)
    return grid

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
def dfs_label(grid, node, force_open=False):
    if node.is_visited:
        return

    node.is_visited = True #// fix typo

    if force_open:
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

    for neighbor in get_neighbors(grid, node): #problem here? - Jason S
        if not neighbor.is_visited:
            neighbor.parent = node
            dfs_label(grid, neighbor)


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


if __name__ == "__main__":

    # This creates the screen. pygame.draw uses this as a canvas - Jason S
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DFS")

    clock = pygame.time.Clock()
    running = True

    grid = create_grid()
    create_grid_dfs(grid)

    option = menu()
    # Run astar - put this before running - Jason S
    if option == 1:
        start = grid[0][0]
        start.color = BLUE
        start.is_obstacle = False

        end = grid[ROWS - 1][COLS - 1]
        end.color = GREEN
        end.is_obstacle = False

        for row in grid:
            for node in row:
                node.update_neighbors(grid)

        found = a_star(grid, start, end)

        if not found:
            print("No Path. Impossible maze")

        while running:
            #screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            draw_grid(screen,grid)
            clock.tick(60)
        pygame.quit()



