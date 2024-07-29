__TOOLNAME__ = 'SA Animation Exporter'
__TOOLID__   = '5e321a98-820f-11ed-bbe8-a85e45e349c7'
__TOOLDESC__ = ''
__TOOLICON__ = 'exporter.png'

def main():
    import studio.tools.content_exporter.export_window as export_window
    export_window.showUI(None,True,None)