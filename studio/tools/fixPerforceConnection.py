__TOOLNAME__ = 'Perforce: Fix Connection'
__TOOLID__ = '91cf788f-8011-11e4-8c24-f8b156ce75fa'
__TOOLDESC__ = 'Start a new perforce connection if the current one is not working'
__TOOLICON__ = 'perforce.png'

def main():
    import sourceControl.perforce as perforce;reload(perforce)
    import sourceControl.perforceQt as perforceQt;reload(perforceQt)