__TOOLNAME__ = 'Infinity: Constant'
__TOOLID__ = '8d93f1c0-8011-11e4-a54d-f8b156ce75fa'
__TOOLDESC__ = 'Sets the curve infinity type to constant.'
__TOOLICON__ = 'constantPreAndPost.png'

def main():
    from maya import cmds
    cmds.setInfinity(pri='constant', poi='constant')
