import bpy, random

fnt = bpy.data.fonts.load('C:\\Users\\taho_\\OneDrive\\Belgeler\\BlenderScripts\\CarbonBold W00 Regular.ttf')
scene = bpy.context.scene
brief = "Akinci UCAV Reconnisance Mission.\n\nBatman/Türkiye 23:30.\n\nTabriz/Iran 02:36.\n\nHelicopter detected on remote mountainous region of Iran’s northwest.\n\nTürkiye 06:45."
briefTextObj = None
UpperLetterASCIIStart = 65
LowerLetterASCIIStart = 97
digitASCIIStart = 48

global_frame_counter = 1
transitionStarted = False
fadeIndexOrder = random.sample([i for i in range(len(brief))], len(brief))
fadeIndex = 0
def TextUpdate(scene):
    global global_frame_counter
    global briefTextObj
    global transitionStarted, fadeIndexOrder, fadeIndex
    global_frame_counter += 1
    # BELOW CODE BLOCK REMOVES LETTERS RANDOMLY FROM THE BRIEF TEXT
    # if transitionStarted:
    #     currentState = list(briefTextObj.data.body)
    #     currentState[fadeIndexOrder[fadeIndex]] = ' '
    #     briefTextObj.data.body = "".join(currentState)
    #     fadeIndex+=1
    #     return
    # if brief in briefTextObj.data.body:
    #     transitionStarted = True
    #     return
    length = len(briefTextObj.data.body)
    if length == 0:
        briefTextObj.data.body = f"{brief[0]}"
    elif briefTextObj.data.body[-1] == brief[length-1]:
        isLetter = brief[length].isalpha()
        isDigit = brief[length].isdigit()
        if not isLetter and not isDigit:
            briefTextObj.data.body += brief[length] # punctuations will be inserted directly
            return
        if isLetter:
            isUpper = brief[length].isupper()
            if isUpper:
                briefTextObj.data.body += chr(UpperLetterASCIIStart)
            else:
                briefTextObj.data.body += chr(LowerLetterASCIIStart)
        else:
            briefTextObj.data.body += chr(digitASCIIStart)
    else:
        step = int((ord(brief[length-1])-ord(briefTextObj.data.body[-1]))/2)
        step = 1 if step == 0 else step 
        briefTextObj.data.body = briefTextObj.data.body[:-1] + chr(ord(briefTextObj.data.body[-1])+step)
    
def rgba(r,g,b): # COLOR CODE CONVERSION
    return (r/255, g/255, b/255, 1)

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

def MissionBrief():
    bpy.ops.object.text_add(location=(0,0,0))
    # INITIAL DEFINE FOR DIGIT OBJECT
    global briefTextObj
    briefTextObj = bpy.context.active_object
    briefTextObj.data.body = ""
    briefTextObj.data.font = fnt
    # COLOR MATERIAL FOR LETTER OBJECTS
    color_mat = bpy.data.materials.new("Text")
    color_mat.diffuse_color = rgba(104,136,35)
    
    if len(briefTextObj.data.materials) == 0:
        briefTextObj.data.materials.append(color_mat)
    else:
        briefTextObj.data.materials[0] = color_mat

run_ops_without_view_layer_update(MissionBrief)
bpy.app.handlers.frame_change_pre.append(TextUpdate)
bpy.context.view_layer.update()