import pygame
import heapq

# Grid settings
ROWS = 5
COLS = 5
WIDTH = 100
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE  = (0,0,255)
GREEN = (0,255,0)
RED   = (255,0,0)
GOLD  = (255,215,0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Simple A* Demo")
font = pygame.font.SysFont(None,20)

# Node
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
        self.parent = None
        self.is_obstacle = False

    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,CELL_SIZE,CELL_SIZE))
        pygame.draw.rect(win,BLACK,(self.x,self.y,CELL_SIZE,CELL_SIZE),1)

    def update_neighbors(self,grid):
        self.neighbors = []
        directions = [(1,0),(-1,0),(0,1),(0,-1)]

        for dr,dc in directions:
            r = self.row + dr
            c = self.col + dc

            if 0 <= r < ROWS and 0 <= c < COLS:
                if not grid[r][c].is_obstacle:
                    self.neighbors.append(grid[r][c])

    def __lt__(self,other):
        return self.f < other.f


# Heuristic
def h(a,b):
    return abs(a.row - b.row) + abs(a.col - b.col)


# Path reconstruction
def reconstruct_path(start,end):
    current = end
    while current.parent and current != start:
        current = current.parent
        current.color = GOLD


# A* Algorithm
def a_star(grid,start,end):

    open_set = []
    heapq.heappush(open_set,(0,start))

    start.g = 0
    start.f = h(start,end)

    closed_set = set()

    while open_set:

        current = heapq.heappop(open_set)[1]

        if current == end:
            reconstruct_path(start,end)
            return True

        closed_set.add(current)

        for neighbor in current.neighbors:

            if neighbor in closed_set:
                continue

            temp_g = current.g + 1

            if temp_g < neighbor.g:

                neighbor.parent = current
                neighbor.g = temp_g
                neighbor.f = temp_g + h(neighbor,end)

                heapq.heappush(open_set,(neighbor.f,neighbor))

                if neighbor != end:
                    neighbor.color = RED

    return False


# Draw grid
def draw(grid,start,end):

    screen.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(screen)

    screen.blit(font.render("START",True,BLACK),(start.x+5,start.y+5))
    screen.blit(font.render("END",True,BLACK),(end.x+5,end.y+5))

    pygame.display.update()


# Main
def main():

    grid = [[Node(r,c) for c in range(COLS)] for r in range(ROWS)]

    start = grid[0][0]
    end   = grid[ROWS-1][COLS-1] #goal

    start.color = BLUE
    end.color = GREEN

    # Example obstacle wall kept in the middle
    wall_col = COLS//2
    for r in range(1,ROWS - 1):
        grid[r][wall_col].is_obstacle = True
        grid[r][wall_col].color = BLACK

    # Precompute neighbors
    for row in grid:
        for node in row:
            node.update_neighbors(grid)

    a_star(grid,start,end)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw(grid,start,end)

    pygame.quit()


if __name__ == "__main__":
    main()
