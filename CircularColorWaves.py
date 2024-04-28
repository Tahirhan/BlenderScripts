import bpy

# TORUS NUMBER
layers = 9

# RANGE METHOD FOR FLOATS
def frange(x, y, jump=1.0):
    '''Range for floats.'''
    i = 0.0
    x = float(x)  # Prevent yielding integers.
    x0 = x
    epsilon = jump / 2.0
    yield x  # yield always first value
    while x + epsilon < y:
        i += 1.0
        x = x0 + i * jump
        if x < y:
          yield x

# LIST FOR COLOR CHANGE STEP VALUES, IT WILL GO FORWARD AND BACK
forward = list(frange(0, 1, 1/layers))
rev = forward.copy()
rev.reverse()
steps = forward + rev
colors = []
for r in steps:
   for g in steps:
      for b in steps:
         colors.append((1*r, 1*g, 1*b, 1)) # WE ARE COMBINING R-G-B TO GET PALETTE

# FOR EACH LAYER; 
# TORUS WITH LAYER NUMBER RADIUS GETS ADDED
# COLOR MATERIAL GETS CREATED FOR THE TORUS AND
# ANIMATION POINTS ADDED FOR EVERY COLOR
# COLOR INDEX STARTS FROM LAYER NUMBER TO EXPRESS WAVE ANIMATION
for layer in range(1,layers):
    bpy.ops.mesh.primitive_torus_add(major_radius=layer, minor_radius=0.25)
    torus = bpy.context.object
    colorMat = bpy.data.materials.new(name='colorFor'+str(layer))
    torus.active_material = colorMat
    colorIndex = layer
    for animationIndex in range(1, len(colors)):
        index = animationIndex*3
        if colorIndex < len(colors):
            colorMat.diffuse_color = colors[colorIndex]
        else:
            colorMat.diffuse_color = colors[colorIndex-len(colors)]
        colorMat.keyframe_insert(data_path='diffuse_color', frame=index)
        colorIndex += 1
        