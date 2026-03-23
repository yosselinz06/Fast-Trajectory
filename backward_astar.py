import heapq
import time

# Colors
RED   = (255,0,0)
GOLD  = (255,215,0)

# Heuristic
def h(a,b):
    return abs(a.row - b.row) + abs(a.col - b.col)

# reset grid
def reset_grid(grid):
    for row in grid:
        for node in row:
            node.g = float("inf")
            node.f = float("inf")
            node.h=0
            node.parent=None

# Path reconstruction
def reconstruct_path(start,end):
    current = end.parent
    while current.parent and current != start:
        current.color = GOLD
        current = current.parent

# Backward A* Algorithm
def backward_a_star(grid,start,end):
    reset_grid(grid) #reset grid added

    start_time = time.perf_counter()

    open_set = []
    closed_set = set()
    count = 0
    expanded = 0

    #search starts from end
    end.g = 0
    end.f = h(end,start)
    heapq.heappush(open_set, (end.f, -end.g, count, end))  # start from end node
    count += 1


    while open_set:
        current = heapq.heappop(open_set)[3]

        if current in closed_set: #skip nodes that are in closed set
            continue

        if current == start:
            reconstruct_path(end, start) # reconstruct path backwards
            end_time = time.perf_counter()
            return True, expanded, end_time - start_time

        closed_set.add(current)
        expanded += 1

        for neighbor in current.neighbors:
            if neighbor in closed_set:
                continue

            temp_g = current.g + 1

            if temp_g < neighbor.g:
                neighbor.parent = current
                neighbor.g = temp_g
                neighbor.f = neighbor.g + h(neighbor,start)

                heapq.heappush(open_set,(neighbor.f, -neighbor.g, count, neighbor))
                count += 1

                if neighbor != end and neighbor != start:
                    neighbor.color = RED
    end_time = time.perf_counter()
    return False, expanded, end_time - start_time
