__TOOLNAME__ = 'Set Globals To Stepped'
__TOOLID__ = '8d817b30-8011-11e4-b57f-f8b156ce75fa'
__TOOLDESC__ = 'Sets the animation curve tangent preferences to stepped.'
__TOOLICON__ = 'animCurvePrefsStepped.png'

def main():
    from maya import cmds
    cmds.keyTangent(g=True, itt='linear')
    cmds.keyTangent(g=True, ott='step')
    