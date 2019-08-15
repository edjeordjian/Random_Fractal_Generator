import time
import random
    
    
def createFractalMap(length, height, sand):
    map = []
    
    for i in range(height):
        map.append([])
        for j in range(length):
            map[i].append(sand)   

    return map

    
def addMounds(map, length, height, mounds, sand, cell_len, cell_hei):
    for i in range(mounds):
        x = random.randint(length//2 - cell_len, length//2 + cell_len)	
        y = random.randint(height//2 - cell_hei, height//2 + cell_hei)
        map[x][y] = sand


def addSandpiles(map, max_sand):
    next_map = map #copy
    is_unstable = True
    
    while is_unstable:
        is_unstable = False
        
        for i in range( len(map) ):
            for j in range( len( map[0] ) ):
                if (map[i][j] > max_sand):
                    is_unstable = True
                    
                    try:
						# 4: adyacents cells
                        monts_out = map[i][j]//4
                        next_map[i][j] = map[i][j] - (monts_out * 4)
                        
                        map[i + 1][j] += monts_out
                        map[i - 1][j] += monts_out
                        map[i][j + 1] += monts_out
                        map[i][j - 1] += monts_out
                    
                    except IndexError:
                        continue
        
        map = next_map


def mirrorFractal(map, hor, ver):
    hor_mirrored = map

    for n in range(hor - 1):
        actual_hor = hor_mirrored
        for j in range( len(actual_hor) ):
            for k in range( len( actual_hor[j] ) - 1, -1, -1 ):
                hor_mirrored[j].append( actual_hor[j][k] )
     
    updated_map = hor_mirrored

    for n in range(ver - 1):
        actual_ver = updated_map
        for l in range( len(actual_ver) - 1, -1, -1 ):
            updated_map.append( actual_ver[l] )

    return updated_map
        

def sizeFractal(map, length, height):
    new_map = []

    for i in range( len(map) ):
        new_map.append( [] )
        for j in range( len( map[i] ) ):
            for l in range(length):
                new_map[i].append( map[i][j] )

    updated_map = []

    for line in new_map:
        for k in range(height):
            updated_map.append(line)

    return updated_map


def createPPMFile(file, fractal_map, colors):
    '''
	Saves the fractal in a .ppm file: each number in the fractal map 
	is matched and stored with its RGB color code, according to "colors".
    '''
    nw_ln = "\n"

    with open(file,'w') as fractal_file:
        #.ppm header
        fractal_file.write('P3' + nw_ln)
        fractal_file.write( "{} {}{}".format( len( fractal_map[0] ), len(fractal_map), nw_ln ) )
        fractal_file.write('255' + nw_ln)

        for line in fractal_map:
            for nro in line:
                fractal_file.write(colors[nro] + nw_ln) 


def createFractal():
    '''
    Creates a fractal by sandpiles method in a .ppm local file.
    '''
    
    ### DEFAULT PARAMETERS ###
    DEFAULT_SAND = 0
    MAX_SAND = 3
    DEF_CELL_LEN = 10
    DEF_CELL_HEIG = 10
    FILE = "fractal_" + str( time.time() ) + ".ppm"
    SIZE = random.choice( range(100,200,10) )
    MOUNDS_NUMBER = random.randint(1,4)
    HORIZONTAL_MIRROR = random.randint(1,4)
    VERTICAL_MIRROR = random.randint(1,4)
    LENG = SIZE
    HEIG = SIZE
    SAND = 120 * SIZE
    ######
    
    #In RGB: black, red, blue, green, yellow, orange, violet, brown, white, cyan
    COLORS_CODES = [
                   "0 0 0", 
                   "255 0 0", 
                   "0 0 255",
                   "0 255 0", 
                   "225 255 0",
                   "255 185 15",
                   "255 0 255",
                   "139 90	43",
                   "255 255 255", 
                   "0 255 255"]

    #Always use black as background color
    SNDP_COLORS = [ COLORS_CODES[0] ]

    for i in random.sample( range( len(COLORS_CODES) - 1 ), MAX_SAND):
        # + 1: avoid usign black again
        SNDP_COLORS.append( COLORS_CODES[i + 1] ); 
    
    print("Size: " + str(SIZE))
    print("Mounds: " + str(MOUNDS_NUMBER))
    print("Hor. Mirroring: " + str(HORIZONTAL_MIRROR))
    print("Ver. Mirroring: " + str(VERTICAL_MIRROR))
    
    print("\nCreating fractal...")
    map = createFractalMap(LENG, HEIG, DEFAULT_SAND)
    addMounds(map, LENG, HEIG, MOUNDS_NUMBER, SAND, DEF_CELL_LEN, DEF_CELL_HEIG)
    addSandpiles(map, MAX_SAND)
    mirrored_map = mirrorFractal(map, HORIZONTAL_MIRROR, VERTICAL_MIRROR)
    sized_map = sizeFractal(mirrored_map, DEF_CELL_LEN, DEF_CELL_HEIG)
    
    print("Saving in file...")
    createPPMFile(FILE, sized_map, SNDP_COLORS)

    
createFractal()
