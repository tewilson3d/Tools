__TOOLNAME__ = 'Animation Paste'
__TOOLID__ = '8d6603f0-8011-11e4-afd0-f8b156ce75fa'
__TOOLDESC__ = 'Paste animation from the clipboard.\n\nUsed with "Animation Copy".'
__TOOLICON__ = 'animationPaste.png'

def main():
    from maya import mel
    mel.eval('superPasteAnim()')
