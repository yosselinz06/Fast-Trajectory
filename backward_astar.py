import heapq

# Backward A* Algorithm
def backward_a_star(grid,start,end):
    reset_grid(grid) #reset grid added
    open_set = []
    heapq.heappush(open_set,(0,end)) # start from end node
    end.g = 0
    end.f = h(end,start)
    closed_set = set()

    while open_set:
        current = heapq.heappop(open_set)[1]
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
                neighbor.f = temp_g + h(neighbor,end)

                heapq.heappush(open_set,(neighbor.f,neighbor))
                # Might have a problem here. tie breaker? -- still working on fixing 

                if neighbor != end:
                    neighbor.color = RED

    return False
