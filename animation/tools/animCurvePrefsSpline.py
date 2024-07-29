__TOOLNAME__ = 'Set Globals To Spline'
__TOOLID__ = '8d787a80-8011-11e4-8348-f8b156ce75fa'
__TOOLDESC__ = 'Sets the animation curve tangent preferences to spline.'
__TOOLICON__ = 'animCurvePrefsSpline.png'

def main():
    from maya import cmds
    cmds.keyTangent(g=True, itt='spline')
    cmds.keyTangent(g=True, ott='spline')
    