########
# Designed for doing dev on a system that can't do displays
# (specifically github codespaces)
# outputs to a text file
#import mapgen
import mapdata
def write_map_to_txt(mapD):
    outstring = ""
    actor_locations = []
    actor_chars = []
    for actor in mapD.actors:
        actor_locations.append([actor.posx, actor.posy])
        print(actor.name)
        if actor.name == "Player":
            actor_chars.append("@")
        elif actor.name == "Door":
            if actor.open:
                actor_chars.append("O")
            else:
                actor_chars.append("D")
        else:
            actor_chars.append("?")
    #we're not doing items yet
    with open("mapdebug.txt", "w") as outfile:
        countx = 0
        while countx < mapD.map.shape[0]:
            county = 0
            while county < mapD.map.shape[1]:
                if [countx, county] in actor_locations:
                    outstring += actor_chars[actor_locations.index([countx, county])]
                else:
                    check_tile = mapD.map[countx][county]
                    if check_tile.tile_type == "floor":
                        outstring += "."
                    elif check_tile.tile_type == "stairup":
                        outstring += "^"
                    elif check_tile.tile_type == "stairdown":
                        outstring += "v"
                    else:
                        outstring += "#"
                county += 1
            countx += 1
            outstring += "\n"
        outfile.write(outstring)
        
        

map_to_write = mapdata.DungeonLevel("mapdebug2.json")
write_map_to_txt(map_to_write)

