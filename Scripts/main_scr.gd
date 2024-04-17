extends Control


# Called when the node enters the scene tree for the first time.
func _ready():
	randomize()
	$main_window/map_window.update_window_title("map name here")
	pass


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):

	if not $main_window.show_window:
		get_tree().quit()
	pass
