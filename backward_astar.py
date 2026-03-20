import heapq

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE  = (0,0,255)
GREEN = (0,255,0)
RED   = (255,0,0)
GOLD  = (255,215,0)

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

# Backward A* Algorithm
def backward_a_star(grid,start,end):
    reset_grid(grid) #reset grid added

    open_set = []
    count = 0

    #search starts from end
    end.g = 0
    end.f = h(end,start)
    heapq.heappush(open_set, (end.f, count, end))  # start from end node
    closed_set = set()

    while open_set:
        current = heapq.heappop(open_set)[2]

        if current in closed_set: #skip nodes that are in closed set
            continue

        if current == start:
            reconstruct_path(end, start) # reconstruct path backwards
            return True

        closed_set.add(current)

        for neighbor in current.neighbors:
            if neighbor in closed_set:
                continue

            temp_g = current.g + 1

            if temp_g < neighbor.g:
                neighbor.parent = current
                neighbor.g = temp_g
                neighbor.f = temp_g + h(neighbor,start)

                count += 1
                heapq.heappush(open_set,(neighbor.f, count, neighbor))
                # for tie breaking issue

                if neighbor != end and neighbor != start:
                    neighbor.color = RED

    return False
