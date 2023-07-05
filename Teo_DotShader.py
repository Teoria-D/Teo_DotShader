import maya.cmds as cmds

#ArnoldのRender Settingsで事前にfilterをcontourに、サンプリングを全て0にしてください
#rampノードに繋がったplace2dTextureのRepeatUVのXYそれぞれ解像度/2に設定してください

def createMaterial(*args):
    textures = openDialog()
    makeTemplate(textures)

def makeTemplate(textures):
    aitoon = cmds.shadingNode('aiToon', asShader=True)
    sgname = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
    blendcolor = cmds.shadingNode('aiComposite', asUtility=True)
    colorcorrect = cmds.shadingNode('aiColorCorrect', asUtility=True)
    projection = cmds.shadingNode('aiCameraProjection', asUtility=True)
    bayer = cmds.shadingNode('checker', asTexture=True)
    bayerp2d = p2dNode()
    ramp = cmds.shadingNode('ramp',asTexture = True)
    rampp2d = p2dNode()
    base = fileNode()
    basep2d = p2dNode()
    
    cmds.setAttr(base + '.fileTextureName', textures[0],type="string")
    cmds.setAttr(aitoon + '.base', 0)
    cmds.setAttr(aitoon + '.emission', 1)
    cmds.setAttr(blendcolor + '.operation', 22)
    cmds.setAttr(colorcorrect + '.saturation',1)
    cmds.setAttr(colorcorrect + '.contrast', 1)
    cmds.setAttr(ramp + '.colorEntryList[1].color', 0, 0, 0, type="double3")
    cmds.setAttr(ramp + '.colorEntryList[2].color', 1, 1, 1, type="double3")
    cmds.setAttr(ramp + '.colorEntryList[1].position', 0.5)
    cmds.setAttr(ramp + '.colorEntryList[2].position', 0)
    cmds.setAttr(ramp + '.interpolation', 0)
    cmds.setAttr(bayerp2d + '.repeatU', 100)
    cmds.setAttr(bayerp2d + '.repeatV', 75)

    
    connectNode(aitoon, '.outColor', sgname, '.surfaceShader')
    connectNode(ramp, '.outColor', aitoon, '.edgeTonemap')
    connectNode(rampp2d, '.outUV', ramp, '.uvCoord')
    connectNode(blendcolor, '.outColor', aitoon, '.emissionColor')
    connectNode(colorcorrect, '.outColor', blendcolor, '.B')
    connectNode(projection, '.outColor', blendcolor, '.A')
    connectNode(base, '.outColor', colorcorrect, '.input')
    connectNode(basep2d, '.outUV', ramp, '.uvCoord')
    connectNode(bayer, '.outColor', projection, '.projectionColor')
    connectNode(bayerp2d, '.outUV', bayer, '.uvCoord')

def fileNode():
    return cmds.shadingNode('file', asTexture=True, isColorManaged=True)

def p2dNode():
    return cmds.shadingNode('place2dTexture', asUtility=True)

def connectNode(input1, attribute1, input2, attribute2):
    return cmds.connectAttr(input1 + attribute1, input2 + attribute2, f=True)

def openDialog():
    textures = cmds.fileDialog2(fileMode=4, caption="Connect Image")
    if not textures:
        print("No texture file selected.")
    else:
        return textures

window = cmds.window(title = 'Dotshader_maker')
cmds.columnLayout(adjustableColumn=True)
cmds.frameLayout(label='Make Dotshader', labelAlign='top')
cmds.button(label='Create Material(Please select basecolor texture)', command=createMaterial)
cmds.showWindow(window)
