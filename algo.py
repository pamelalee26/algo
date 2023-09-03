import math
from queue import PriorityQueue

# Define the Grid class as the parent class
class Grid:
    def __init__(self, x, y, direction="N", obstacle_id=-1):
        self.x = x
        self.y = y
        self.direction = direction
        self.obstacle_id = obstacle_id
    
    def getGrid(self):
        return {'x': self.x, 'y': self.y, 'd': self.direction, 's': self.obstacle_id}
    
# Inherit from Grid to create the Obstacle class
class Obstacle(Grid):
    next_id = 1  # Class variable to keep track of the next available ID

    def __init__(self, x, y, direction):
        if direction not in ['N', 'S', 'E', 'W']:
            raise ValueError("Invalid direction. Use 'N', 'S', 'E', or 'W'.")
        super().__init__(x, y, direction)  # Initialize using the parent class constructor
        self.obstacle_id = Obstacle.next_id  # Assign a unique ID
        Obstacle.next_id += 1

    def __str__(self):
        return f"Obstacle {self.obstacle_id} at ({self.x}, {self.y}) facing {self.direction}"
    
    def calculate_visible_coordinates(self):
        visible_coordinates = []

        if self.direction == 'N':
            for x in range(self.x - 1, self.x + 2):
                visible_coordinates.append((x, self.y-2, "N"))
        elif self.direction == 'S':
            for x in range(self.x - 1, self.x + 2):
                visible_coordinates.append((x, self.y + 2, "S"))
        elif self.direction == 'E':
            for y in range(self.y - 1, self.y + 2):
                visible_coordinates.append((self.x+2, y, "E"))
        elif self.direction == 'W':
            for y in range(self.y - 1, self.y + 2):
                visible_coordinates.append((self.x-2, y, "W"))

        return visible_coordinates
    
class Map:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = []

    def add_obstacle(self, obstacle):
        if self.is_valid_position(obstacle.x, obstacle.y) and self.has_space_for_obstacle(obstacle):
            if obstacle not in self.obstacles:
                self.obstacles.append(obstacle)
            else:
                print("EXISTS")
                print(f"Obstacle at ({obstacle.x}, {obstacle.y}) facing {obstacle.direction} already exists.")
        else:
            print(f"Obstacle at ({obstacle.x}, {obstacle.y}) cannot be added. Invalid position or insufficient space.")
            
    def is_valid_position(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def has_space_for_obstacle(self, obstacle):
        # Define the size of the robot car
        car_size = 3

        if obstacle.direction == 'N':
            return obstacle.y >= car_size  # Check for enough space in the North direction
        elif obstacle.direction == 'S':
            return self.height - obstacle.y >= car_size + 1 # Check for enough space in the South direction
        elif obstacle.direction == 'E':
            return self.width - obstacle.x >= car_size + 1 # Check for enough space in the East direction
        elif obstacle.direction == 'W':
            return obstacle.x >= car_size # Check for enough space in the West direction
    
    # Add a method to set the robot's position in the map
    def set_robot(self, robot):
        self.robot = robot
        
    def print_map(self):
        for y in range(self.height):
            for x in range(self.width):
                obstacle_at_position = False
                for obstacle in self.obstacles:
                    if obstacle.x == x and obstacle.y == y:
                        print(obstacle.direction, end=" ")
                        obstacle_at_position = True
                        break
                if not obstacle_at_position:
                    if self.robot and self.robot.x == x and self.robot.y == y:
                        print("R", end=" ")  # Print 'R' for the robot
                    else:
                        print(".", end=" ")  # Print '.' for empty spaces
            print()


    def __str__(self):
        return f"Map Size: {self.width}x{self.height}, Obstacles: {self.obstacles}"
    
class Robot:
    def __init__(self, x=0, y=0, direction="N"):
        self.x = x
        self.y = y
        self.path = []  # List to store the robot's path

    def move(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y
        self.path.append((self.x, self.y))  # Record the current position
    
    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y

    def __str__(self):
        return f"Robot at ({self.x}, {self.y}) facing self.direction"

def find_shortest_path(map):
    obstacles = map.obstacles
    robot = map.robot
    visited_obstacles = set()

    while len(visited_obstacles) < len(obstacles):
        shortest_path = None
        for obstacle in obstacles:
            if obstacle in visited_obstacles:
                continue

            best_x, best_y, best_direction = None, None, None
            best_distance = float('inf')

            visible_coordinates = obstacle.calculate_visible_coordinates()

            for x, y, facing_direction in visible_coordinates:
                # Calculate the distance from the robot's center to the obstacle's location
                distance = math.sqrt((robot.x - x) ** 2 + (robot.y - y) ** 2)

                # Check if the distance is within the required range (e.g., 20 units)
                if distance <= 20 and distance < best_distance:
                    # Ensure there is at least a one-grid spacing between the robot and the obstacle
                    is_safe = True
                    for rx in range(robot.x - 1, robot.x + 2):
                        for ry in range(robot.y - 1, robot.y + 2):
                            if (rx, ry) == (obstacle.x, obstacle.y):
                                is_safe = False
                                break

                    if is_safe:
                        best_x, best_y, best_direction = x, y, facing_direction
                        best_distance = distance

            if best_x is not None:
                # Move the robot one step at a time toward the best position
                while robot.x != best_x or robot.y != best_y:
                    # Determine the next step towards the best position
                    delta_x = 1 if best_x > robot.x else -1 if best_x < robot.x else 0
                    delta_y = 1 if best_y > robot.y else -1 if best_y < robot.y else 0
                    robot.move(delta_x, delta_y)
                    print(f"Moved to ({robot.x}, {robot.y})")

                # Mark the obstacle as visited
                visited_obstacles.add(obstacle)

        if shortest_path is None:
            break

    print("All obstacles visited.")

if __name__ == "__main__":
    # Create a Map instance
    map = Map(20, 20)

    # Add obstacles to the map
    obstacle1 = Obstacle(5, 5, 'N')
    obstacle2 = Obstacle(15, 15, 'E')
    map.add_obstacle(obstacle1)
    map.add_obstacle(obstacle2)

    # Create a Robot instance
    robot = Robot(1, 18)

    map.set_robot(robot)
    map.print_map()

    find_shortest_path(map)