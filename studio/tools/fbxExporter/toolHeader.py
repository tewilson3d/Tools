__TOOLNAME__ = 'Generic FBX Exporter'
__TOOLID__   = '9002a7cf-8011-11e4-972d-f8b156ce75fa'
__TOOLDESC__ = 'This is Generic FBX exporter for any Unreal or Unity asset. \n' \
               +'1) Exports: Skelmeshs, Animations, Static Meshes. \n' \
               +'2) DOES NOT havbe perforce support. \n' \
               +'\n\n Excellent for one time exports'
__TOOLICON__ = 'default.png'

def main():
    import studio.tools.fbxExporter.fbxExporter_window as fbxUI
    fbxUI.showUI()