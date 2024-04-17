extends Sprite2D

var player_name = "Player"
var health = 100
var mana = 100
var fortitude = 1
var power = 1
var knowledge = 1
var precision = 1
var awareness = 1
var current_tile = Vector2i(0,0) 

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func check_wall_collide(check_pos:Vector2i):
	pass # if it collides, print a true, print a false if not.
