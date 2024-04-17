extends Node
class_name MapGen


class Level:
	var size
	var entry_point = false
	var file_loc = false
	var exit_point
	var level_name
	var room_list = []
	var hall_list = []
	var floor_tiles = PackedVector2Array()
	func _init(size:Vector2i, level_name:String, entry_point = false, load_from_file = false):
		self.size = size
		self.level_name = level_name
		if not entry_point:
			self.entry_point = Vector2i(size.x, (size.y / 2) - 1)
		if load_from_file:
			self.file_loc = load_from_file
		## BELOW WILL BE DEPRECIATED, KEPT BECAUSE OTHERWISE THINGS GO KABOOM?? ##
	func generate_layout(first_floor = false):
		var density = 0
		var density_goal = (self.size.x * self.size.y)/4
		room_list.append(Room.new(self.entry_point, Vector2i(randi_range(3,8), randi_range(3,8)), "start"))
		if first_floor: # Make the first room of the first floor always the same:
			room_list[0].origin = Vector2i(self.size.x - 4, (size.y/2 ) - 3)
		#check the validity of the first room:
		while not room_list[0].is_in_bounds(self.size):
			room_list[0] = Room.new(self.entry_point, Vector2i(randi_range(3,8), randi_range(3,8)), "start")
		
		# Begin the room generation loop:
		density = room_list[0].size.x * room_list[0].size.y
		while density < density_goal:
			var next_room_size = Vector2i(randi_range(3,5), randi_range(3,5))
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
		## END DEPRECIATION ##
	
	func process_floor_tiles():
		for room in room_list:
			var count_x = room.origin.x
			while count_x <= room.origin.x + room.size.x:
				var count_y = room.origin.y
				while count_y <= room.origin.y + room.size.y:
					self.floor_tiles.append(Vector2i(count_x, count_y))
					count_y += 1
				count_x += 1
		#do the same with halls
		
	func generate_poi_layout(first_floor = false): # Updating to use a POI system instead because i like that more
		var poi_list = []
		poi_list.append(entry_point)
		
		var number_of_points = 23 # Just a few points for now
		while len(poi_list) < number_of_points:
			while true
				var try_another_point = true # this is our break condition
				var next_point = Vector2i(randi_range(0,size.x), randi_range(0,size.y))
				for p in poi_list: # see if we overlap a radius around a point
					var x_ok = false
					var y_ok = false
					if next_point.x > p.x + 8 and next_point.x < p.x - 8: # make a barrier around all of the room points
						x_ok = true
					if next_point.y > p.y + 8 and next_point.y < p.y - 8: # Doing this with two ifs because it's easier to read
						y_ok = true
					if y_ok or x_ok:
						try_another_point = false
				if not try_another_point: # make sure we're good
					break
			poi_list.append(next_point)

		# Now we have our points, so we can start placing rooms
		# First room will have our entry stairs, so we place it separately:
		
		var next_room = Room.new(poi_list[0], Vector2i(randi_range(3,5), randi_range(3,5)), "start")
		room_list.append(next_room) # Add it to the list!

		while len(room_list) < len (poi_list):
			var current_poi = len(room_list) # Use the length of the room list to give us the index of our next poi
			next_room = Room.new(poi_list[current_poi], Vector2i(randi_range(3,8), randi_range(3,8)))
			# now generate a matching hall!
			# Start with a relative direction:
			var last_room = room_list[current_poi - 1]
			var x_offset = poi_list[current_poi].x - room_list[current_poi - 1].origin.x
			var y_offset = poi_list[current_poi].y - room_list[current_poi - 1].origin.y
			


			

		
		process_floor_tiles()
		
	func render_camera_view(target:TileMap, cam_origin:Vector2i, cam_size:Vector2i = Vector2i(21,21)):
		var count_x = 0
		while count_x <= cam_size.x:
			var count_y = 0
			while count_y <= cam_size.y:
				if floor_tiles.has(Vector2i(count_x + cam_origin.x, count_y + cam_origin.y)):
					# We have this as a floor tile, draw to tilemap!
					target.set_cell(0,Vector2i(count_x, count_y), 0, Vector2i(0,0))
				else:
					target.set_cell(0,Vector2i(count_x, count_y), 0, Vector2i(0,1))
				count_y += 1
			count_x += 1

		return

			
		

class Room:
	var connected_to_entrance = false
	var origin
	var size
	var special_tiles = {}
	func _init(origin:Vector2i, size:Vector2i, special_type = "none"):
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
	func get_room_tiles():
		# returns an array containing every tile location in the given room, in Vector2i coords
		var output = PackedVector2Array()
		var count_x = self.origin.x
		while count_x <= self.origin.x + self.size.x:
			var count_y = self.origin.y
			while count_y <= self.origin.y + self.size.y:
				output.append(Vector2i(count_x, count_y))
				count_y += 1
			count_x += 1

		return output
	
	func get_border_tiles(direction): # Returns a set of Vector2i points indicating the tiles on that edge of the room
		var out_array = [] # kinda quick and dirty for now, can be cleaned up later for sure
		if direction == "E":
			var tile_out_x = origin.x + size.x + 1
			var tile_out_y = origin.y
			while tile_out_y <= origin.y + size.y:
				out_array.append(Vector2i(tile_out_x, tile_out_y))
				tile_out_y += 1
		elif direction == "W":
			tile_out_x = origin.x - 1
			tile.out_y = origin.y
			while tile_out_y <= origin.y + size.y:
				out_array.append(Vector2i(tile_out_x, tile_out_y))
				tile_out_y += 1
		elif direction == "N":
			tile_out_x = origin.x
			tile_out_y = origin.y - 1
			while tile_out_x <= origin.x + size.x:
				out_array.append(Vector2i(tile_out_x, tile_out_y))
				tile_out_x += 1
		elif direction == "S":
			tile_out_x = origin.x
			tile_out_y = origin.y + size.y + 1
			while tile_out_x <= origin.x + size.x:
				out_array.append(Vector2i(tile_out_x, tile_out_y))
				tile_out_x += 1
		return out_array

class Hall:
	func _init(origin:Array, x_length:int, y_length:int, door_locations = 0):
		self.origin = origin
		self.x_length = x_length
		self.y_length = y_length
		self.inverted = inverted
		self.door_location = door_location
		self.connected_rooms = []
	func get_hall_tiles(): # Returns a list of every tile in the hall, and its contents
		var out_arr = []


		return out_arr
		
