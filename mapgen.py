#########################
# Map Generation Script #
#########################
from math import floor, ceil
import random
import numpy as np

class Room:
    def __init__(self, width, height, origin, flags = []):
        self.origin = origin
        self.width = width
        self.height = height
        self.reserved_points = {}
        self.floor_points = []
        self.tile_count = width * height
        self.connected_to_entrance = False
        
        # Now let's actually prepare the room
        if "dungeon_start" in flags: # If it's flagged as the start of the dungeon
            self.reserved_points["in"] = [origin[0], origin[1]]
            print(self.origin)
            self.origin = [origin[0] - floor(width/2), origin[1] - height]
            print(self.origin)
            self.connected_to_entrance = True
        elif "floor_start" in flags: # First room of a floor, but not the dungeon
            self.reserved_points["in"] = origin
            self.connected_to_entrance = True
            self.move_origin_around()
        elif "exit" in flags:
            self.reserved_points["out"] = origin
            self.move_origin_around()
        
        # Append tiles to the room
        CX = 0
        while CX < width:
            CY = 0
            while CY < height:
                self.floor_points.append([CX + origin[0], CY + origin[1]])
                CY += 1
            CX += 1
        for p in self.reserved_points:
            insert_at = self.floor_points.index(self.reserved_points[p])
            self.floor_points[insert_at] = self.reserved_points[p] + [p]


    def get_bordering_points(self, side = False):
        out_list = []
        # Returns a list of tiles that border the room, and what side of the room it is on
        CX = 0
        while CX < self.width:
            out_list.append([self.origin[0] + CX, self.origin[1] - 1, "N"])
            out_list.append([self.origin[0] + CX, self.origin[1] + self.width + 1, "S"])
            CX += 1
        CY = 0
        while CY < self.height:
            out_list.append([self.origin[0] - 1, self.origin[1] + CY, "W"])
            out_list.append([self.origin[0] + 1 + self.width, self.origin[1] + CY, "E"])
            CY += 1
        out_list.append([self.origin[0] - 1, self.origin[1] - 1, "NW"])
        out_list.append([self.origin[0] + self.width + 1, self.origin[1] - 1, "NE"])
        out_list.append([self.origin[0] - 1, self.origin[1] + self.width + 1, "SW"])
        out_list.append([self.origin[0] + self.width + 1, self.origin[1] + self.width + 1, "SE"])
        
        if side: # filter by what side you want
            filter( lambda x: x[2] == side, out_list)

        return out_list

        
    def move_origin_around(self):
        # shifts the room around the origin
        # otherwise stairs would always be in the top left
        x_offset = random.randint(0, self.width)
        y_offset = random.randint(0, self.height)
        if x_offset - self.origin[0] < 0:
            x_offset = self.origin[0] # move it to the side
        if y_offset - self.origin[1] < 0:
            y_offset = self.origin[1] # just shift it to the side.
        self.origin = [self.origin[0] - x_offset, self.origin[1] - y_offset]

class Hall:
    def __init__(self, start, end):
        self.start_room = start
        self.end_room = end
        self.points = []
    
    def prepare_points(self):
        hall_direction = ""
        # check relative location of rooms:
        if self.start_room.origin[0] + self.start_room.width < self.end_room.origin[0]:
            # Origin room is entirely to the left of the target
            hall_direction += "E"
            
        elif self.start_room.origin[0] > self.end_room.origin[0] + self.end_room.width:
            # Origin room is entirely to the right of the target
            hall_direction += "W"

        else:
            #Calculate the overlap situation
            pass

        # Do the same thing for the other axis:
        if self.start_room.origin[1] + self.start_room.height < self.end_room.origin[1]:
            # Origin room is entirely below the target
            hall_direction += "N"
            
        elif self.start_room.origin[1] > self.end_room.origin[1] + self.end_room.height:
            # Origin room is entirely above the target
            hall_direction += "S"

        else:
            #Calculate the overlap situation
            pass

        


def is_room_valid(room, map_data, existing_rooms = []):
    # Returns true if the room will fit, returns false if it will not.
    # Start with checking OOB:
    if room.origin[0] + room.width >= map_data.shape[0] - 1:
        return False
    if room.origin[1] + room.height >= map_data.shape[0] -1:
        return False
    for r in existing_rooms:
        for p in r.floor_points:
            if p in room.floor_points:
                return False
    # If it passes those checks:
    return True

def get_hall_points(start_room, end_room):
    hall_points = []

    # find what sides have a valid starting point
    if start_room.origin[0] > end_room.origin[0] + end_room.width:
        x_dir = "W" # West
    elif start_room.origin[0] + start_room.width > end_room.origin[0]:
        x_dir = "E" # East
    else: 
        x_dir = False # overlap
    if start_room.origin[1] > end_room.origin[1] + end_room.height:
        y_dir = "N" # North
    elif start_room.origin[1] + start_room.height > end_room.origin[1]:
        y_dir = "S" # South
    else:
        y_dir = False #overlap
    
    # Choose a point bordering start_room on one of the possible sides (e.g. NE = North OR east)   
    start_points = []
    if x_dir and y_dir:
        start_points += start_room.get_bordering_points(x_dir)
        start_points += start_room.get_bordering_points(y_dir)
    elif x_dir:
        start_points += start_room.get_bordering_points(x_dir)
    elif y_dir: 
        start_points += start_room.get_bordering_points(y_dir)
    else:
        start_points += [start_room.origin] ## IDK ##
    start_door_pos = random.choice(start_points)

    # Do the same to find the end door
    end_points = []
    if x_dir and y_dir:
        if x_dir == "E":
            x_dir = "W"
        else:
            x_dir = "E"
        end_points += end_room.get_bordering_points(x_dir)
        if y_dir == "N":
            y_dir = "S"
        else:
            y_dir = "N"
        end_points += end_room.get_bordering_points(y_dir)
    elif x_dir:
        # Invert the side
        if x_dir == "E":
            x_dir = "W"
        else:
            x_dir = "E"
        end_points += end_room.get_bordering_points(x_dir)
    elif y_dir:
        if y_dir == "N":
            y_dir = "S"
        else:
            y_dir = "N"
        end_points += end_room.get_bordering_points(y_dir)
    else: 
        end_points += [end_room.origin] # FUCK

    start_door_pos = random.choice(start_points)
    end_door_pos = random.choice(end_points)
    hall_points.append([start_door_pos[0], start_door_pos[1], "D"])
    # With the start and end points, we can draw a path.
    # Figure out our X and Y directions

    x_travel = start_door_pos[0] - end_door_pos[0]
    y_travel = start_door_pos[1] - end_door_pos[1]
    hor_move = 0 # If we're moving right or left
    if x_travel > 0:
        hor_move = -1
    elif x_travel < 0:
        hor_move = 1

    ver_move = 0# or up or down
    if y_travel > 0:
        ver_move = -1
    elif y_travel < 0:
        ver_move = 1
    # hopefully this works?
    hor_move_count = 0
    next_x = start_door_pos[0] # declare outside the loop so we can use it in the next one:
    next_y = start_door_pos[1]
    while hor_move_count < x_travel * hor_move:
        hor_move_count += 1 # Increment here since we're doing some multiplication stuff
        next_x = hor_move_count * hor_move
        hall_points.append([next_x, next_y, "."])
    ver_move_count = 0
    while ver_move_count < y_travel * ver_move:
        ver_move_count += 1 
        next_y = ver_move_count * ver_move
        hall_points.append([next_x, next_y, "."])

    hall_points.append([end_door_pos[0], end_door_pos[1], "D"])
    
    return hall_points


def generate_map(width, height, origin = False):
    print("Generating Map:", end = "")
    density_goal = ceil(width * height / 4)
    #test for now, make walls later################################################
    output_map = np.full((width, height), "#")
    room_list = []
    new_room = False
    if not origin:
        new_room = Room(3,3,[floor(width / 2), floor(height/2)], "dungeon_start")
    else:
        new_room = Room(random.randint(1, 8), random.randint(1, 8), origin, "floor_start")
        while not is_room_valid(new_room, output_map, room_list):
            new_room = Room(random.randint(1, 8), random.randint(1, 8), origin, "floor_start")
    room_list.append(new_room)
    density = new_room.tile_count
    # Find where to put the exit.
    while True:
        next_width = random.randint(1,8)
        next_height = random.randint(1,8)
        next_origin = [random.randint(1, width - next_width), random.randint(1, height - next_height)]
        next_room = Room(next_width, next_height, next_origin, "E")
        if is_room_valid(next_room, output_map, room_list):
            room_list.append(next_room)
            density += next_width * next_height
            print(".", end = "")
            make_exit_room = False
            break
    # Place the rest of the rooms:
    while density < density_goal:
        while True: 
            next_width = random.randint(1,8)
            next_height = random.randint(1,8)
            next_origin = [random.randint(1, width - next_width), random.randint(1, height - next_height)]
            next_room = Room(next_width, next_height, next_origin)
            if is_room_valid(next_room, output_map, room_list): #make sure it's valid
                density += next_width * next_height
                room_list.append(next_room)
                print(".", end = "")
                break
    # Calculate the hallways:
    hall_count = 1
    print("\nFinding Hallways:", end = "")
    print(len(room_list))
    halls = []
    while hall_count < len(room_list):
        print(".", end = "")
        halls.append(get_hall_points(room_list[hall_count - 1], room_list[hall_count]))
        hall_count += 1

    # Place the rooms on the map:
    print("\n Placing Rooms:", end = "")
    for room in room_list:
        print(".", end = "")
        for point in room.floor_points:
            if len(point) > 2:
                # This point has something on it, so see what it is.
            ####DEBUG#### for now just do text, so we can dump this to file:
                output_map[point[0]][point[1]] = point[2][0]
            else:
                output_map[point[0]][point[1]] = "."
    print("\nPlacing Halls:", end = "")
    for hall in halls:
        for point in hall:
                output_map[point[0]][point[1]] == point[2]
                print(".", end = "")
    return output_map
    