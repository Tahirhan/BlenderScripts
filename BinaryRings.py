import bpy
import math, time
import random
import numpy as np
pi = math.pi
scene = bpy.context.scene

# METHOD FOR CALCULATING DIGIT LOCATIONS
def PointsInCircum(r,n=100):
    return [(math.cos(2*pi/n*x)*r,math.sin(2*pi/n*x)*r,0) for x in range(0,n+1)]

# TO GET DISTINCT VALUES OF THE LIST
def unique(list1):
    # initialize a null list
    unique_list = []
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

# METHOD TO SET DIGIT NUMBERS RANDOM AT EVERY 20 FRAMES
global_frame_counter = 1
def digitRandomizerPerFrame(scene):
    global global_frame_counter
    global_frame_counter += 1
    if global_frame_counter % 20 != 0:
        return
    for digit in digits:
        digit.data.body = random.choice(["0", "1"])

# CODE SPEED OPTIMIZATION
def run_ops_without_view_layer_update(func):
    from bpy.ops import _BPyOpsSubModOp

    view_layer_update = _BPyOpsSubModOp._view_layer_update

    def dummy_view_layer_update(context):
        pass

    try:
        _BPyOpsSubModOp._view_layer_update = dummy_view_layer_update

        func()

    finally:
        _BPyOpsSubModOp._view_layer_update = view_layer_update

# RING NUMBER
layers = 11

# INITIAL PARAMETERS
initial_radius = 10
initial_points = 8
radius_step = 5
animationPtNumber = pow(initial_points + (layers-1),2)
# IT IS BETTER WITHOUT FONT SO I REMOVED IT BUT YOU CAN USE
#fnt = bpy.data.fonts.load('C:\\Users\\taho_\\OneDrive\\Belgeler\\BlenderScripts\\SoccerLeague.ttf')

# HERE IS WHERE THE MAGIC HAPPENS
digits = []
def CreateBinaryRings():
    color = (255,215,0,0.8)
    # LAYERS WILL MOVE REVERSE IN ORDER
    goReverse = False
    for layer in range(1, layers):
        radius = initial_radius + ((layer-1) * radius_step)
        # GETTINGS DIGIT LOCATIONS FOR EACH LAYER, DIGIT NUMBER GET INCREASED AS THE LAYER MOVE UP
        digitPts = unique(PointsInCircum(radius, initial_points+(layer-1)))
        animationPts = digitPts.copy() #PointsInCircum(radius, pow(initial_points + (layer-1),2))
        # IF YOU NOT POP, ANIMATION LAGS AT O PT, TRY AND SEE WHAT I MEAN
        animationPts.pop()
        rVal = 0
        gVal = 0
        # INITIALS FOR COLOR TRANSITION
        rChangeVal = 255/len(animationPts)
        gChangeVal = 215/len(animationPts)
        print(f"layer: {layer} - digitPts: {len(digitPts)} - animationPts: {len(animationPts)}")
        if goReverse:
            animationPts.reverse()
        goReverse = not goReverse
        del digitPts[-1] # ANOTHER FORM OF POP
        digitPtIndex = 1 
        for digitPt in digitPts:
            colorMat = bpy.data.materials.new(name='colorFor'+str(layer))
            print(f"Processing {digitPtIndex}")
            digitPtIndex+=1
            bpy.ops.object.text_add(location=digitPt)
            # INITIAL DEFINE FOR DIGIT OBJECT
            digit = bpy.context.active_object
            digit.data.body = random.choice(["0", "1"])
            #digit.data.font = fnt
            digit.data.size = 2+layer/5
            if len(digit.data.materials) == 0:
                digit.data.materials.append(colorMat)
            else:
                digit.data.materials[0] = colorMat
            matched = False
            currentAnimationPtNumber = 1
            while True:
                breakWhile = False
                for animationPt in animationPts:
                    if digitPt == animationPt:
                        matched = True
                    # WHEN ANIMATION PT MATCHES WITH DIGIT PT WE CAN START TO REV
                    if matched:
                        digit.location = animationPt                    
                        digit.keyframe_insert("location", frame=currentAnimationPtNumber*30)
                        
                        # COLOR TRANSITION GOES FORWARD AND BACK BETWEEN GOLD AND BLACK
                        if rVal > 255 or rVal < 0:
                            rChangeVal = -rChangeVal
                            gChangeVal = -gChangeVal
                        
                        rVal += rChangeVal
                        gVal += gChangeVal
                        color = (rVal,gVal,0,0.8)
                        print(color)
                        colorMat.diffuse_color = color
                        colorMat.keyframe_insert(data_path='diffuse_color', frame=currentAnimationPtNumber*15)
                        
                        currentAnimationPtNumber += 1
                        if currentAnimationPtNumber > animationPtNumber:
                            breakWhile = True
                            break
                if breakWhile:
                    break
            digits.append(digit)

# RUN THE METHODS WE HAVE CREATED
start_time = time.time()
run_ops_without_view_layer_update(CreateBinaryRings)
bpy.app.handlers.frame_change_pre.append(digitRandomizerPerFrame)
bpy.context.view_layer.update()
end_time = time.time()            
print(end_time-start_time)