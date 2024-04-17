extends Node2D


# OH BOY LETS REWRITE THAT MAP DATA STUFF
# At least we have some of what we had to define baked in.
var displayed_level = false
var map_size = Vector2i(64,64)



# Called when the node enters the scene tree for the first time.
func _ready():
	displayed_level = MapGen.Level.new(map_size, "TEST")
	displayed_level.generate_poi_layout()
	displayed_level.render_camera_view($map_tiles, Vector2i(0,0))
	


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
	pass
