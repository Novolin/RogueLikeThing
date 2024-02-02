extends Node
class_name MapGen


class Level:
	var size
	var entry_point = false
	var file_loc = false
	var exit_point
	var level_name
	var room_list
	var hall_list
	func _init(size:Vector2i, level_name:String, entry_point = false, load_from_file = false):
		self.size = size
		self.level_name = level_name
		if not entry_point:
			self.entry_point = Vector2i(size.x, (size.y / 2) - 1)
		if load_from_file:
			self.file_loc = load_from_file

	func generate_layout(first_floor = false):
		var density = 0
		var density_goal = (self.size.x * self.size.y)/4
		room_list[0] = Room.new(self.entry_point, Vector2i(randi_range(3,8), randi_range(3,8)), "start")
		if first_floor: # Make the first room of the first floor always the same:
			room_list[0].origin = Vector2i(self.size.x - 4, (size.y/2 ) - 3)
		#check the validity of the first room:
		while not room_list[0].is_in_bounds(self.size):
			room_list[0] = Room.new(self.entry_point, Vector2i(randi_range(3,8), randi_range(3,8)), "start")
		
		# Begin the room generation loop:
		density = room_list[0].size.x * room_list[0].size.y
		while density < density_goal:
			var next_room_size = Vector2i(randi_range(3,8), randi_range(3,8))
			var next_room_origin = Vector2i(randi_range(0,self.size.x - next_room_size.x), randi_range(0, self.size.y - next_room_size.y))
			var next_room = Room.new(next_room_origin, next_room_size)
			var next_room_valid = true
			for room in room_list:
				if next_room.does_room_collide(room):
					next_room_valid = false
			if next_room_valid: # If it passes the check, add it to the list and update the density counter.
				density += next_room.size.x * next_room.size.y
				room_list.append(next_room)
				
		# The level is now populated with rooms, add the hallways.
		
		#or i will after i test this stuff
		
		
		
	func render_camera_view(target:TileMap, cam_origin:Vector2i, cam_size:Vector2i = Vector2i(21,21)):
		pass # push the given rectangle to the tilemap, but make sure that it's within bounds.
		# this is basically the Camera class from before

			
		

class Room:
	var connected_to_entrance = false
	var origin
	var size
	var special_tiles = {}
	func _init(origin:Vector2i, size:Vector2i, special_type = false):
		self.origin = origin
		self.size = size
		if special_type == "start":
			var connected_to_entrance = true
			special_tiles["stairup"] = origin
			self.origin = Vector2i(randi_range(0,size.x), randi_range(0, size.y)) # shuffle the origin
		else:
			var connected_to_entrance = false
	func is_in_bounds(level_size:Vector2i):
		if level_size.x < self.origin.x + self.size.y:
			return false
		elif level_size.y < self.origin.y + self.size.y:
			return false
		else:
			return true
			
	func does_room_collide(check_room:Room):
		# Check if this room would collide with the other one listed
		# Returns TRUE if room collides. Returns FALSE if they do not.
		var check_x = 0
		var self_right_val = self.origin.x + self.size.x
		var check_right_val = check_room.origin.x + check_room.size.x
		var self_bottom_val = self.origin.y + self.size.y
		var check_bottom_val = check_room.origin.y + check_room.size.y

		# make an array of greater/less thans:
		if self.origin.x < check_room.origin.x:
			check_x += 1
		if self.origin.x < check_right_val:
			check_x += 1
		if self_right_val < check_room.origin.x:
			check_x += 1
		if self_right_val < check_right_val:
			check_x += 1
		if check_x %2 == 1: # If it's odd, we know that it's a potential overlap, so check the Y axis:
			var check_y = 0
			if self.origin.y < check_room.origin.y:
				check_y += 1
			if self.origin.y < check_bottom_val:
				check_y += 1
			if self_bottom_val < check_room.origin.y:
				check_y += 1
			if self_bottom_val < check_bottom_val:
				check_y += 1
			if check_y % 2 == 1: # If it also collides here, we're in trouble!
				return true
		return false
				
		
class Hall:
	func _init(origin:Array, x_length:int, y_length:int, inverted = false, door_location = false):
		self.origin = origin
		self.x_length = x_length
		self.y_length = y_length
		self.inverted = inverted
		self.door_location = door_location
		self.connected_rooms = []
		
