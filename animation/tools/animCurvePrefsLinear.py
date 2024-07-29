__TOOLNAME__ = 'Set Globals To Linear'
__TOOLID__ = '8d6f52c0-8011-11e4-8507-f8b156ce75fa'
__TOOLDESC__ = 'Sets the animation curve tangent preferences to linear.'
__TOOLICON__ = 'animCurvePrefsLinear.png'

def main():
    from maya import cmds
    cmds.keyTangent(g=True, itt='linear')
    cmds.keyTangent(g=True, ott='linear')
    