__TOOLNAME__ = 'SA Rigging Exporter'
__TOOLID__   = '9c163086-820f-11ed-a859-a85e45e349c7'
__TOOLDESC__ = ''
__TOOLICON__ = 'exporter.png'

def main():
    import studio.tools.content_exporter.export_window as export_window
    export_window.showUI(True,None,None)