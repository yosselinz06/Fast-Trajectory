import heapq
import time

RED = (255,0,0)
GOLD = (255,215,0)
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
    current = end.parent # Added .parent
    while current.parent and current != start:
        current.color = GOLD
        current = current.parent


# A* Algorithm
def a_star(grid,start,end):
    reset_grid(grid) #reset grid added
    open_set = []

    start_time = time.perf_counter()  # start timer

    start.g = 0
    start.f = h(start,end)
    closed_set = set()
    count = 0
    expanded = 0 #count expanded nodes

    #if same f value, will take largest g
    heapq.heappush(open_set, (start.f, -start.g, count, start))
    count += 1

    while open_set:
        current = heapq.heappop(open_set)[3]

        #skips nodes that have already been explored and processed
        if current in closed_set:
            continue

        if current == end:
            reconstruct_path(start,end)
            end_time = time.perf_counter()
            return True, expanded, end_time - start_time

        closed_set.add(current)
        expanded += 1 #counting expanded nodes

        for neighbor in current.neighbors:
            if neighbor in closed_set:
                continue

            temp_g = current.g + 1

            if temp_g < neighbor.g:
                neighbor.parent = current
                neighbor.g = temp_g
                neighbor.f = neighbor.g + h(neighbor,end)

                heapq.heappush(open_set,(neighbor.f,-neighbor.g, count, neighbor))
                count += 1

                if neighbor != end:
                    neighbor.color = RED

    end_time = time.perf_counter()
    return False, expanded, end_time - start_time
