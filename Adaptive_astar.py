import heapq

# Adaptive astar
# No manhattan distance - Jason S

RED = (255,0,0)
GOLD = (255,215,0)
# Heuristic
#def h(a,b):
    #return abs(a.row - b.row) + abs(a.col - b.col)

# Check if node has a heuristic- Use if available, manhatten if not
def heuristic_adaptive(node, goal):
    if node.h> 0:
        return node.h
    return abs(node.row - goal.row) + abs(node.col - goal.col)

# Added Code here ------------------- Chang this - do not rase heruistic - Jason S
def reset_grid(grid):
    for row in grid:
        for node in row:
            node.g = float("inf")
            node.f = float("inf")
            # node.h=0 #Do not Use this for adaptive - Jason S
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
def a_star_adaptive(grid,start,end):

    # Section to measure expanded nodes - Jason S
    expanded = 0


    reset_grid(grid) #reset grid added
    open_set = []
    heapq.heappush(open_set,(0,start))
    start.g = 0
    start.f = heuristic_adaptive(start,end) # Change for adaptive
    closed_set = set()

    while open_set:
        current = heapq.heappop(open_set)[1]
        expanded+=1 # Count expanded - Jason S
        if current == end:
            reconstruct_path(start,end)
            goal_cost = end.g # - Research more - Jason S
            for node in closed_set:#--
                node.h = goal_cost - node.g#--
            return True, expanded

        closed_set.add(current)

        for neighbor in current.neighbors:
            if neighbor in closed_set:
                continue
            temp_g = current.g + 1
            if temp_g < neighbor.g:
                neighbor.parent = current
                neighbor.g = temp_g
                neighbor.f = temp_g + heuristic_adaptive(neighbor,end) #change this? adaptive - Jason S

                heapq.heappush(open_set,(neighbor.f,neighbor))
                # Might have a problem here. tie breaker?

                if neighbor != end:
                    neighbor.color = RED

    return False, expanded

def main():
    if __name__ == "__main__":
        main()