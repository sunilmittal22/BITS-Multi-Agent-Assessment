#!/usr/bin/env python
# coding: utf-8

# In[1]:


from heapq import heappush, heappop

class GBFSAgent:
    def __init__(self, scenario, start, goal, color_penalty, obstacle_penalty):
        self.scenario = scenario
        self.start = start
        self.goal = goal
        self.color_penalty = color_penalty
        self.obstacle_penalty = obstacle_penalty
    
    def gbfs(self):
        # Initialize variables
        rows = len(self.scenario)
        cols = len(self.scenario[0])
        visited = set()
        cost = {self.start: 0}
        parent = {self.start: None}
        queue = []
        
        # Add start node to queue
        heappush(queue, (0, self.start))
        
        # Loop until queue is empty
        while queue:
            # Get node with lowest heuristic cost
            _, current = heappop(queue)
            
            # Check if we have reached the goal
            if current == self.goal:
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                return path[::-1], cost[self.goal]
            
            # Mark current node as visited
            visited.add(current)
            
            # Iterate through neighbors
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                x, y = current
                neighbor = (x + dx, y + dy)
                
                # Check if neighbor is out of bounds or has been visited
                if not (0 <= x + dx < rows and 0 <= y + dy < cols) or neighbor in visited:
                    continue
                
                # Check if neighbor is an obstacle
                if self.scenario[x + dx][y + dy] == self.obstacle_penalty[0]:
                    c = cost[current] + self.obstacle_penalty[1]
                else:
                    c = cost[current] + 1
                
                # Check if neighbor is in a different colored room than the goal
                if self.scenario[x + dx][y + dy] != self.scenario[self.goal[0]][self.goal[1]]:
                    h = self.manhattan_distance(neighbor, self.goal) + self.color_penalty
                else:
                    h = self.manhattan_distance(neighbor, self.goal) - self.color_penalty
                
                # Update cost and parent if needed
                if neighbor not in cost or c < cost[neighbor]:
                    cost[neighbor] = c
                    parent[neighbor] = current
                    # Add neighbor to queue
                    heappush(queue, (h, neighbor))
        
        # Return empty path if goal was not reached
        return [], float('inf')
    
    def manhattan_distance(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x1 - x2) + abs(y1 - y2)
    
    def visualize_scenario(self, scenario, path, cost):
        scenario = [[cell if cell != 'H' else 'G' for cell in row] for row in scenario]
        light_red = '#FF0000'
        light_green = '#009900'
        cmap = ListedColormap([light_red, light_green])
        plt.imshow(scenario, cmap=cmap)
        plt.plot([cell[1] for cell in path], [cell[0] for cell in path], c='w')
        plt.title(f'Cost: {cost}')
        # Add grid lines
        plt.grid(False)
    
        plt.show()
    
def map_values(scenario):
    mapping = {'R': 1, 'G': 2, 'O': 3}
    return [[mapping[cell] for cell in row] for row in scenario]


def main():
    # Define scenarios
    scenario1 = [    
        ['R', 'G', 'G', 'G', 'R', 'G'],
        ['G', 'G', 'G', 'R', 'G', 'G'],
        ['G', 'G', 'R', 'G', 'G', 'G'],
        ['G', 'R', 'G', 'G', 'G', 'R'],
        ['R', 'G', 'G', 'G', 'R', 'G'],
        ['G', 'G', 'G', 'R', 'G', 'G'],
    ]

    scenario2 = [    
        ['R', 'G', 'R', 'G', 'R', 'G'],
        ['G', 'R', 'G', 'R', 'G', 'R'],
        ['R', 'G', 'R', 'G', 'R', 'G'],
        ['G', 'R', 'G', 'R', 'G', 'R'],
        ['R', 'G', 'R', 'G', 'R', 'G'],
        ['G', 'R', 'G', 'R', 'G', 'R'],
    ]
    
    # Map character values to integers
    scenario1 = map_values(scenario1)
    scenario2 = map_values(scenario2)
    
    # Create agents
    R1_S1 = GBFSAgent(scenario1, (0, 0), (2, 3), 5, (2, 10)) # (2,10) means Green obstacle penanlty
    G1_S1 = GBFSAgent(scenario1, (0, 0), (2, 3), 5, (1, 10)) # # (1,10) means Red obstacle penanlty

                                                                     
    # Find paths and costs
    path1, cost1 = R1_S1.gbfs()
    path2, cost2 = G1_S1.gbfs()
    
    # Visualize scenarios
    print(f"R1 scenario1")
    print(f"Path: {path1}")
    print(f"Cost: {cost1}")
    
    print(f"G1 scenario1")
    print(f"Path: {path2}")
    print(f"Cost: {cost2}")
    
    
if __name__ == '__main__':
    main()


# With this code, we have defined an intelligent agent that can find the shortest path between a start and a goal in a given scenario, using the GBFS algorithm. The agent takes into account the presence of obstacles and the cost of traversing different colored rooms, as well as the distance to the goal. The agent also has a method for visualizing the scenario and the path it has found.
