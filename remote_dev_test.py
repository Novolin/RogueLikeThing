########
# Designed for doing dev on a system that can't do displays
# (specifically github codespaces)
# outputs to a text file
#import mapgen
import mapdata
def write_map_to_txt(mapD):
    with open("mapdebug.txt", "w") as outfile:
        countx = 0
        while countx < mapD.shape[0]:
            county = 0
            while county < mapD.shape[1]:
                check_tile = mapD[countx][county]
                if len(check_tile.actors) > 0:
                    if check_tile.actors[0] == "Player":
                        outfile.write("@")
                    elif check_tile.actors[0] == "closed":
                        outfile.write("D")
                    elif check_tile.actors[0] == "open":
                        outfile.write("d")
                    else:
                        outfile.write(".")
                elif check_tile.tile_type == "floor":
                    outfile.write(".")
                elif check_tile.tile_type == "stairup":
                    outfile.write("^")
                elif check_tile.tile_type == "stairdown":
                    outfile.write("v")
                else:
                    outfile.write("#")
                county += 1
            countx += 1
            outfile.write("\n")
        
        

write_map_to_txt(mapdata.load_map_from_file("maps/debugmap.json"))