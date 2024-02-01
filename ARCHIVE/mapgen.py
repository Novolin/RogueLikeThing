#########################
# Map Generation Script #
#########################
from math import floor, ceil
import random
import json

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
            self.origin = [origin[0] - floor(width/2), origin[1] - height]
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

    def get_dict(self):
        room_dict = {}
        room_dict["origin"] = {"x":self.origin[0], "y":self.origin[1]}
        room_dict["width"] = self.width
        room_dict["height"] = self.height
        return room_dict
class Hall:
    def __init__(self, start, length, direction, doors = 1):
        self.start_point = start
        self.doors = doors
        self.length = length
        self.direction = direction

    def get_dict(self):
        hall_dict = {"start":{"x":self.start_point[0], "y":self.start_point[1]}, 
                     "direction":self.direction, 
                     "length":self.length}
        return hall_dict

    def get_hall_doors(self):
        door_coords = []
        door_count = self.doors
        if door_count % 2 == 1:
            door_coords = [self.start_point]
            door_count -= 1
        if door_count > 0:
            if self.direction == "+x":
                door_coords.append([self.start_point[0] + self.length, self.start_point[1]])
            elif self.direction == "-x":
                door_coords.append([self.start_point[0] - self.length, self.start_point[1]])
            elif self.direction == "+y":    
                door_coords.append([self.start_point[0], self.start_point[1] + self.length])
            elif self.direction == "-y":
                door_coords.append([self.start_point[0], self.start_point[1] - self.length])
        return door_coords


def route_hall(room_list, origin_room, target_room, all_hall_points = []):
    # The list we will return
    halls_made = []
    
    # Check relative positions:
    left_room = False
    upper_room = False
    right_room = False
    lower_room = False

    # Left/Right
    if room_list[origin_room].origin[0] > room_list[target_room].origin[0] + room_list[target_room].width:
        left_room = room_list[target_room]
        right_room = room_list[origin_room]
    elif room_list[origin_room].origin[0] + room_list[origin_room].width < room_list[target_room].origin[0]:
        left_room = room_list[origin_room]
        right_room = room_list[target_room]
    elif room_list[origin_room].origin[0] < room_list[target_room].origin[0]:
        left_room = room_list[origin_room]
        right_room = room_list[target_room]
    elif room_list[origin_room].origin[0] > room_list[target_room].origin[0]:
        left_room = room_list[target_room]
        right_room = room_list[origin_room]
    elif room_list[origin_room].origin[0] == room_list[target_room].origin[0]: #they share an X origin
        left_room = room_list[origin_room] # doesn't matter what we choose
        right_room = room_list[target_room]

    # Up/Down
    if room_list[origin_room].origin[1] > room_list[target_room].origin[1] + room_list[target_room].height:
        upper_room = room_list[target_room]
        lower_room = room_list[origin_room]
    elif room_list[origin_room].origin[1] + room_list[origin_room].height < room_list[target_room].origin[1]:
        upper_room = room_list[origin_room]
        lower_room = room_list[target_room]
    elif room_list[origin_room].origin[1] < room_list[target_room].origin[1]:
        upper_room = room_list[origin_room]
        lower_room = room_list[target_room]
    elif room_list[origin_room].origin[1] > room_list[target_room].origin[1]:
        upper_room = room_list[target_room]
        lower_room = room_list[origin_room]
    elif room_list[origin_room].origin[1] == room_list[target_room].origin[1]:
        upper_room = room_list[target_room]
        lower_room = room_list[origin_room]
    
    # Start writing to our list of points
    cointoss = random.randint(0,1) # choose if we start horizontal or vertical
    hall_points = all_hall_points
    this_hall_points = []
    hall_origin = [-1, -1]
    hall_target = [-1, -1]
    hall_doors = 1 # where the doors at
    
    if cointoss: # start vertical    
        hall_origin[1] = upper_room.origin[1] + upper_room.height + 1
        hall_origin[0] = random.randint(upper_room.origin[0], upper_room.origin[0] + upper_room.height)
        # Choose a random point in the other room, we can detect when we enter it.
        hall_target = random.choice(lower_room.floor_points)
    else:
        hall_origin[1] = random.randint(left_room.origin[1], left_room.origin[1] + left_room.height)
        hall_origin[0] = left_room.origin[0] + left_room.width + 1
        # Choose a random point in the room, we will detect when we enter the room
        hall_target = random.choice(right_room.floor_points)
        

    hall_points.append(hall_origin)
    this_hall_points.append(hall_origin)
    touched_rooms = []
    last_point = hall_origin
    next_point = last_point
    make_turn = False # do we need to make a turn in this hall. Will be set in the next block.
    while True:
        next_point[cointoss] += 1
        if next_point in hall_points: # if we touch another hall, we can kill it without doing anything else.
            if random.randint(0,10) > 9: # 10% chance to add a door at the end of the hall.
                hall_doors += 2 
            break
        touches_room = False
        # Time for the worst part: check if the point is in another room:
        for room in room_list:
            if next_point in room.floor_points:
                touches_room = True
                touched_rooms.append(room_list.index(room))
                break
        if touches_room: # we touch a room
            hall_doors += 2
            break
        
        hall_points.append(next_point)
        this_hall_points.append(next_point)
        last_point = next_point
        if hall_target[cointoss] == next_point[cointoss]:
            make_turn = True
            break
        
    # make a hall object based on what we have so far:
    if cointoss:
        hall_dir = "+y"
    else:
        hall_dir = "+x"
    halls_made.append(Hall(hall_origin, len(this_hall_points), hall_dir, hall_doors))


    # Check if we had to make a turn while doing this:
    if make_turn:
        make_turn = False
        hall_doors = 0
        this_hall_points = []
        hall_origin = last_point
        if cointoss:
            hall_dir = "+x"
            cointoss = 0
        else:
            hall_dir = "+y"
            cointoss = 1
        
        while True:
            next_point[cointoss] += 1
            if next_point in hall_points: # if we touch another hall, we can kill it without doing anything else.
                if random.randint(0,10) > 9: # 10% chance to add a door at the end of the hall.
                    hall_doors += 2 
                break
            touches_room = False
            # Time for the worst part: check if the point is in another room:
            for room in room_list:
                if next_point in room.floor_points:
                    touches_room = True
                    touched_rooms.append(room_list.index(room))
                    break
            if touches_room: # we touch a room
                hall_doors += 2
                break
            
            hall_points.append(next_point)
            hall_points.append(next_point)
            last_point = next_point
            if hall_target[cointoss] == next_point[cointoss]:
                make_turn = True
                break
        halls_made.append(Hall(hall_origin, len(this_hall_points), hall_dir, hall_doors))
    halls_made.append(touched_rooms)
    halls_made.append(this_hall_points)
    return halls_made

def is_room_valid(room, map_size, existing_rooms = []):
    # Returns true if the room will fit, returns false if it will not.
    # Start with checking OOB:
    if room.origin[0] + room.width >= map_size[0] - 1:
        return False
    if room.origin[1] + room.height >= map_size[1] -1:
        return False
    for r in existing_rooms:
        for p in r.floor_points:
            if p in room.floor_points:
                return False
    # If it passes those checks:
    return True

def generate_map(width, height, origin = False, tileset = False):
    print("Generating Map:", end = "")
    map_dict = {"sizex": width, "sizey":height}
    density_goal = ceil(width * height / 4)
    room_list = []
    hall_list = []
    actor_list = [] #doors, etc.
    hall_points = []
    new_room = False
    
    if not origin:
        new_room = Room(3,3,[floor(width / 2), floor(height/2)], "dungeon_start")
    else:
        new_room = Room(random.randint(1, 8), random.randint(1, 8), origin, "floor_start")
        while not is_room_valid(new_room, (width, height), room_list):
            new_room = Room(random.randint(1, 8), random.randint(1, 8), origin, "floor_start")
    room_list.append(new_room)
    density = new_room.tile_count
    # Find where to put the exit.
    while True:
        next_width = random.randint(3,8)
        next_height = random.randint(3,8)
        next_origin = [random.randint(1, width - next_width), random.randint(1, height - next_height)]
        next_room = Room(next_width, next_height, next_origin, "exit")
        if is_room_valid(next_room, (width, height), room_list):
            room_list.append(next_room)
            density += next_width * next_height
            print(".", end = "")
            break
    # Place the rest of the rooms:
    while density < density_goal:
        while True: 
            next_width = random.randint(3,8)
            next_height = random.randint(3,8)
            next_origin = [random.randint(1, width - next_width), random.randint(1, height - next_height)]
            next_room = Room(next_width, next_height, next_origin)
            if is_room_valid(next_room, (width, height), room_list): #make sure it's valid
                density += next_width * next_height
                room_list.append(next_room)
                print(".", end = "")
                break
    # Calculate the hallways:
    print("\nFinding Hallways:", end = "")

    # Place the first hallway:
    target_room = random.choice(room_list[1:])
    hall = route_hall(room_list, 0, room_list.index(target_room), hall_points)
    hall_points.append(hall.pop())
    connected = hall.pop()
    if connected == []:
        connected = False
    if connected != False and not room_list[connected].connected_to_entrance:
        room_list[connected].connected_to_entrance = True
    for h in hall:
        hall_list.append(h)
        print(".", end = "")
    
    # now add more, because life is hell:
    connected_rooms = []
    for room in room_list:
        if room.connected_to_entrance:
            connected_rooms.append(room_list.index(room))
    while len(connected_rooms) < len(room_list):
        
        hall_start = random.choice(connected_rooms)
        hall_end = random.randint(0, len(room_list) - 1)
        hall = route_hall(room_list, hall_start, hall_end, hall_points)
        hall_points.append(hall.pop())
        connected = hall.pop()
        if connected == []:
            connected = False
        if connected != False and not room_list[connected].connected_to_entrance:
            room_list[connected].connected_to_entrance = True
        for h in hall:
            hall_list.append(h)
            print(".", end = "")
        for room in room_list:
            if room.connected_to_entrance:
                connected_rooms.append(room_list.index(room))

    # Put the doors into the actor list
    for h in hall_list:
        doors = h.get_hall_doors()
        for d in doors:
            actor_list.append(d)

    # This is where we would place enemies?
    map_dict["actors"] = {}
    map_dict["doors"] = {}
    '''
    for actor in actor_list:
        if actor.name == "door":
            map_dict["doors"]["D" + str(actor_list.index(actor))] = {"x":actor.}
        else: 
            map_dict["actors"]["A" + str(actor_list.index(actor))] = {"actor data here":69420}'''
    # place items in the dictionary:
    count = 0
    map_dict["rooms"] = {}
    map_dict["halls"] = {}
    while count < len(room_list) and count < len(hall_list):
        if count <= len(room_list):
            map_dict["rooms"]["R" + str(count)] = room_list[count].get_dict()
        if count <= len(hall_list):
            map_dict["halls"]["H" + str(count)] = hall_list[count].get_dict()
        count += 1

    map_dict["stairs"] = {}
    map_dict["stairs"]["up"] = {"x":room_list[0].reserved_points["in"][0], "y":room_list[0].reserved_points["in"][1]}
    map_dict["stairs"]["down"] = {"x":room_list[1].reserved_points["out"][0], 
                                  "y":room_list[1].reserved_points["out"][1]}
    map_dict["tileset"] = tileset
    map_dict["name"] = "none"
    print("\nDone!")
    return map_dict
    
with open("mapdebug2.json", "w") as outfile:
    json.dump(generate_map(48,48), outfile)
