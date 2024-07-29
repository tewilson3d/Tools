__TOOLNAME__ = 'Infinity: Cycle'
__TOOLID__ = '8d9cf270-8011-11e4-b90a-f8b156ce75fa'
__TOOLDESC__ = 'Sets the curve infinity type to cycle.'
__TOOLICON__ = 'cyclePreAndPost.png'

def main():
    from maya import cmds
    cmds.setInfinity(pri='cycle', poi='cycle')
