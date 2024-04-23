import bpy

layer_number = 5
layer_space = 5
scale_coef = 5

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

def AddCubeWithAnimation(x, y, z):
    bpy.ops.mesh.primitive_cube_add()

    cube = bpy.context.active_object
    cube.location = (x,y,z)
    cube.scale = 1,1,1

    start_frame = 1
    cube.keyframe_insert("location", frame=start_frame)
    cube.keyframe_insert("scale", frame=start_frame)

    cube.location = (x*scale_coef,y*scale_coef,z*scale_coef)
    cube.scale = 5,5,5

    mid_frame = 90
    cube.keyframe_insert("location", frame=mid_frame)
    cube.keyframe_insert("scale", frame=mid_frame)

    cube.location = (x,y,z)
    cube.scale = 1,1,1
    last_frame = 180
    cube.keyframe_insert("location", frame=last_frame)
    cube.keyframe_insert("scale", frame=last_frame)
        
AddCubeWithAnimation(0,0,0)
for layer in range(1, layer_number):
    steps = list(frange(-1, 1, 1/layer))
    for x in steps:
        for y in steps:
            for z in steps:
                recent_x = x * layer * layer_space
                recent_y = y * layer * layer_space
                recent_z = z * layer * layer_space
                AddCubeWithAnimation(recent_x, recent_y, recent_z)