__TOOLNAME__ = 'Animation Copy'
__TOOLID__ = '8d5d0340-8011-11e4-8123-f8b156ce75fa'
__TOOLDESC__ = 'Copy animation from the selected objects to the clipboard. ' +\
               'Copied animation will be lost when Maya is closed.\n\n' +\
               'Used with "Animation Paste".'
__TOOLICON__ = 'animationCopy.png'

def main():
    from maya import mel
    mel.eval('superCopyAnim()')
