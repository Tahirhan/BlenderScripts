import bpy
import random
from random import randint
import time

# COLOR MATERIAL FOR LETTER OBJECTS
color_mat = bpy.data.materials.new("Text")
color_mat.diffuse_color = (0.85, 25.8, 1.1, 1)

# METHOD FOR CREATING A LETTER OBJECT AT GIVEN LOCATION
def CreateLetterObject(x, y, z):
    bpy.ops.object.text_add(location=(x,y,z))
    letter = bpy.context.active_object
    
    letter.data.body = random.choice(matrix_letters)
    letter.data.size = random.choice(font_sizes)
    
    if len(letter.data.materials) == 0:
        letter.data.materials.append(color_mat)
    else:
        letter.data.materials[0] = color_mat
    return letter

# CLEAN OBJECTS
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# GET JAPANESE LETTERS LIST
matrix_letters = [chr(i) for i in range(0x30a0, 0x3100)]

# ANIMATION PARAMETERS
animation_iteration = 100
initial_letter_number = 1
x_range = 180
y_range = 40
z_range = 20

#RANDOM FONT SIZE LIST
font_sizes = [1.5, 1.5, 2.5, 3.5, 3.5, 3.5]

# LIST FOR LETTER OBJECTS
letters = []

# CREATING A LETTER OBJECT LIST WITH GIVEN INITIAL NUMBER
for c in range(0, initial_letter_number):
    x = randint(0, x_range)
    y = randint(0, y_range)
    z = 0
    letters.append(CreateLetterObject(x,y,z))
    
# FOR EACH ANIMATION ITERATION WE MOVE LETTERS DOWN AND ADD NEW LETTER TO LIST
# AT TOP
for a in range(0, animation_iteration):
    for letter in letters:
        if letter.location.y-5 > 0:
            letter.location=(letter.location.x,letter.location.y-5,letter.location.z)
        else: # IF LETTER LOCATION SURPASS Y AXIS LIMIT, MOVE IT TO TOP
            letter.location=(letter.location.x, y_range, letter.location.z)
            
    # ADD NEW ONE TO LETTER OBJECTS
    x = randint(0, x_range)
    y = y_range
    z = 0
    letters.append(CreateLetterObject(x,y,z))
    
    # DESELECT ALL OBJECTS, REDRAW VIEW, AND WAIT FOR SOME TIME FOR ANIMATION
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
    time.sleep(0.04)