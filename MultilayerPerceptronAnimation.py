import bpy, math

# NODE NUMBERS IN LAYERS, FIRST INDEX IS INPUT LAYER
# LAST INDEX IS OUTPUT LAYER, OTHERS ARE HIDDENS
layerNodeNumbers = [13,8,8,5,2] 
layerNodeLocations = [] # LIST TO HOLD NODE LOCATIONS, USED FOR CONNECTIONS
layerSpace = 100 # SPACE BETWEEN LAYERS
nodeSpace = 20 # VERTICAL NODE SPACE
sphereRadius = 7 # NODES ARE BUILT AS SPHERES
lineThickness = 1 # CONNECTION LINE THICKNESS

def rgba(r,g,b): # COLOR CODE CONVERSION
    return (r/255, g/255, b/255, 1)

# GET COLOR CODE W.R.T OBJECT TYPE AND STATE
def GetColor(layerIndex, layerMaxIndex, state, isSphere):
    if isSphere: 
        if layerIndex == 0:
            return rgba(0,0,250) if state else rgba(30,144,255)
        elif layerIndex == layerMaxIndex:
            return rgba(250,0,0) if state else rgba(255,127,127)
        else:
            return rgba(0,250,0) if state else rgba(152,251,152)
    else: # connection
        return rgba(240,240,20) if state else rgba(65,65,65)

# DRAW CONNECTION(CYLINDER) BETWEEN NODES
def cylinder_between(pt1, pt2, r):
    dx = pt2[0] - pt1[0]
    dy = pt2[1] - pt1[1]
    dz = pt2[2] - pt1[2]    
    dist = math.sqrt(dx**2 + dy**2 + dz**2)

    bpy.ops.mesh.primitive_cylinder_add(
        radius = r, 
        depth = dist,
        location = (dx/2 + pt1[0], dy/2 + pt1[1], dz/2 + pt1[2])   
    ) 

    phi = math.atan2(dy, dx) 
    theta = math.acos(dz/dist) 

    bpy.context.object.rotation_euler[1] = theta 
    bpy.context.object.rotation_euler[2] = phi 

# CREATE NODES W.R.T LAYER NODE NUMBERS
def CreateNodes():
    nodeLocations = []
    sphereObjs = []
    for index, layerNodeNumber in enumerate(layerNodeNumbers):
        currentLayerNodeLocations = []
        currentLayerSphereObjs = []
        x = index * layerSpace
        z = 0
        y = (layerNodeNumber/2) * nodeSpace
        for i in range(layerNodeNumber):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=sphereRadius, location=(x, y, z))
            sphere = bpy.context.active_object
            currentLayerSphereObjs.append(sphere)
            currentLayerNodeLocations.append((x, y, z))
            y -= nodeSpace
        nodeLocations.append(currentLayerNodeLocations)
        sphereObjs.append(currentLayerSphereObjs)
    return nodeLocations, sphereObjs

# CONNECT EACH LAYER AND NODES
def CreateConnections(nodeLocations):
    allBatches = []
    for index, currentLayerNodeLocations in enumerate(nodeLocations):
        if index == 0:
            continue
        layerBatch = []
        for currentNodeIx, currentNodeLocation in enumerate(currentLayerNodeLocations):
            nodeBatch = []
            for preNodeIx, preNodeLocation in enumerate(nodeLocations[index-1]):
                cylinder_between(preNodeLocation, currentNodeLocation, lineThickness)
                nodeBatch.append((bpy.context.active_object, preNodeIx, currentNodeIx))
            layerBatch.append(nodeBatch)
        allBatches.append(layerBatch)
    return allBatches

# COLOR ANIMATION POINTS FOR MATERIALS
def SetMaterialColorsKeyFrames(colorMatPreNode, colorMatCurrentNode, colorMatConnection, batchIx, sphereObjs, state, frame):
    colorMatPreNode.diffuse_color = GetColor(batchIx, len(sphereObjs)-1, state, True)
    colorMatCurrentNode.diffuse_color = GetColor(batchIx+1, len(sphereObjs)-1, state, True)
    colorMatConnection.diffuse_color = GetColor(batchIx, len(sphereObjs[batchIx])-1, state, False)
    colorMatPreNode.keyframe_insert(data_path='diffuse_color', frame=frame)
    colorMatCurrentNode.keyframe_insert(data_path='diffuse_color', frame=frame)
    colorMatConnection.keyframe_insert(data_path='diffuse_color', frame=frame)

# THIS IS WHERE MAGIC HAPPENS
# EACH BATCH GETS ANIMATED TOGETHER
def CreateAnimationPoints(batches, sphereObjs):
    frame = 0
    frameStep = 15
    sphereObjMaterialSetIndexes = []
    for batchIx, batch in enumerate(batches):
        for nodeBatchIx, nodeBatchEl in enumerate(batch):
            for batchElIx, batchEl in enumerate(nodeBatchEl):
                if (batchIx, batchEl[1]) not in sphereObjMaterialSetIndexes:
                    colorMatPreNode = bpy.data.materials.new(name=f"colorForPreNode_Batch{batchIx}_{nodeBatchIx}_BatchEl{batchElIx}")
                    sphereObjs[batchIx][batchEl[1]].active_material = colorMatPreNode
                    sphereObjMaterialSetIndexes.append((batchIx, batchEl[1]))
                else:
                    colorMatPreNode = sphereObjs[batchIx][batchEl[1]].active_material

                if (batchIx+1, batchEl[2]) not in sphereObjMaterialSetIndexes:
                    colorMatCurrentNode = bpy.data.materials.new(name=f"colorForCurrentNode_Batch{batchIx}_{nodeBatchIx}_BatchEl{batchElIx}")
                    sphereObjs[batchIx+1][batchEl[2]].active_material = colorMatCurrentNode
                    sphereObjMaterialSetIndexes.append((batchIx+1, batchEl[2]))
                else:
                    colorMatCurrentNode = sphereObjs[batchIx+1][batchEl[2]].active_material

                colorMatConnection = bpy.data.materials.new(name=f"colorForConnection_Batch{batchIx}_{nodeBatchIx}_BatchEl{batchElIx}")
                batchEl[0].active_material = colorMatConnection

                SetMaterialColorsKeyFrames(colorMatPreNode, colorMatCurrentNode, colorMatConnection, batchIx, sphereObjs, False, frame)
                SetMaterialColorsKeyFrames(colorMatPreNode, colorMatCurrentNode, colorMatConnection, batchIx, sphereObjs, True, frame+frameStep)
                SetMaterialColorsKeyFrames(colorMatPreNode, colorMatCurrentNode, colorMatConnection, batchIx, sphereObjs, False, frame+(frameStep*2))
            frame += (frameStep*2)

# YES, RUN METHODS OTHERWISE IT WONT WORK :|
nodeLocations, sphereObjs = CreateNodes()
batches = CreateConnections(nodeLocations)
CreateAnimationPoints(batches, sphereObjs)