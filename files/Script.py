import heapq
import math

# Define the heuristic function
def heuristic(pos):
    #For any arbitrary node “n” the heuristic to reach the Heart h(n) is given by the below:
    #Manhattan distance + Color Penalty
    #where, Color Penalty = +5 if the node “n” and goal node is in different colored room
    #and Color Penalty = -5 if the node “n” and goal node is in same colored room
    # Calculate the Manhattan distance
    manhattan_distance = abs(pos[0] - end_position[0]) + abs(pos[1] - end_position[1])
    # Calculate the color penalty
    color_penalty = 5 if matrix[pos[0]][pos[1]] != matrix[end_position[0]][end_position[1]] else -5
    # Return the total heuristic value
    return manhattan_distance + color_penalty


# Define the A* search function
def a_star_search(start, end, agent):
    # Create a heap to store the unexplored nodes
    heap = []
    next_cost=0
    # Push the start node onto the heap with a cost of 0
    #https://realpython.com/python-heapq-module/
    heap.append((0, start))
    # Create a dictionary to store the cost of each node, initially cost is 0 for the start node
    costs = {start: 0}
    # Create a dictionary to store the parent of each node, Initial set it to None
    parents = {start: None}
    # Create a set to store the explored nodes
    visited_nodes = set()
    # Loop until the heap is empty
    while heap:
        # Pop the node with the lowest cost from the heap
        #https://docs.python.org/3/library/heapq.html
        current = heapq.heappop(heap)[1]
        # If the current node is the emd, return the path
        if current == end:
            path = []
            while current in parents:
                path.append(current)
                current = parents[current]
            return path[::-1]
        # If the current node has been explored, continue
        if current in visited_nodes:
            continue
        # Mark the current node as visited
        visited_nodes.add(current)
        # Expand the current node and look in each possible direction, currently only 4 directions defined
        # Left Right Up and down
        for i, (dx, dy) in enumerate(directions):
            # Calculate the next position
            next_pos = (current[0] + dx, current[1] + dy)
            # Skip the next position if it is outside the grid or is an obstacle
            if (
                next_pos[0] < 0
                or next_pos[0] >= len(matrix)
                or next_pos[1] < 0
                or next_pos[1] >= len(matrix[0])
            ):
                print("Outside the matrix")
                continue                
            # Calculate the cost of the next position, every trainsition cost 1 hence add the cost by 1
            next_cost = costs[current] + 1
            # If the next position is the goal and the agent is R1, add the penalty for the green room
            if next_pos == end and agent == "R1":
                next_cost += 10
            # If the next position is the goal and the agent is G1, add the penalty for the red room
            if next_pos == end and agent == "G1":
                next_cost -= 10
            # If the next position has not been explored or the cost of the next position is lower than the current cost, update the cost and parent of the next position
            if next_pos not in costs or next_cost < costs[next_pos]:
                costs[next_pos] = next_cost
                priority = next_cost + heuristic(next_pos)
                heapq.heappush(heap, (priority, next_pos))
                parents[next_pos] = current
    # Return None if the end position was not reached
    return None


#main function
def main():
    # Run the A* search for R1
    path__For_R1 = a_star_search(start_position, end_position, "R1")
    print(f"Path for R1: {path__For_R1}")
    # Run the A* search for G1
    #path__For_G1 = a_star(start_position, end_position, "G1")
    #print(f"Path for G1: {path__For_G1}")

#### Globals Start #####
# Define the matrix
matrix = [
    [" ", " ", " ", " ", " ", " "],
    [" ", "G", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " "],
    [" ", " ", " ", "H", " ", " "],
    [" ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " "],
]

# Define the start and goal positions
start_position = (1, 2)
end_position = (3, 3)

# Define the movement directions and costs
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
costs = [1, 1, 1, 1]
#### Globals End #####
if __name__ == '__main__':
    main()
