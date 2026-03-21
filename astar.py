#import pygame
import heapq


RED = (255,0,0)
GOLD = (255,215,0)
# Heuristic
def h(a,b):
    return abs(a.row - b.row) + abs(a.col - b.col)

# Added Code here -------------------
def reset_grid(grid):
    for row in grid:
        for node in row:
            node.g = float("inf")
            node.f = float("inf")
            node.h=0
            node.parent=None
# -----------------------------------


# Path reconstruction
def reconstruct_path(start,end):
    current = end.parent # Added .parent
    while current.parent and current != start:
        current.color = GOLD
        current = current.parent

# Issue with duplicates added to heap - Jason S
# A* Algorithm
def a_star(grid,start,end):
    reset_grid(grid) #reset grid added
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
                # Might have a problem here. tie breaker?

                if neighbor != end:
                    neighbor.color = RED

    return False




# Main
def main():
    if __name__ == "__main__":
        main()