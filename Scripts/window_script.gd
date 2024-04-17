extends Control
var show_window = true
var collapse_window = false
var window_border_size
# Called when the node enters the scene tree for the first time.
func _ready():
	window_border_size = $window_border.get_size()
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
	pass

func update_window_title(text:String):
	$title_bar/map_title.text = text

func _on_menu_button_pressed():
	show_window = false


func _on_minimize_button_pressed():
	# play a lil animation here to show the window rolling up
	# for now, just do it instantly
	var target_size = Vector2i(window_border_size.x, 4)
	$window_container.hide()
	$window_border.set_size(target_size)
	$minimize.hide()
	$maximize.show()
	pass # Replace with function body.


func _on_maximize_button_pressed():
	
	$window_container.show()
	$window_border.set_size(window_border_size)
	$maximize.hide()
	$minimize.show()
	pass # Replace with function body.
