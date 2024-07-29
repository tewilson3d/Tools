__TOOLNAME__ = 'SA Model Exporter'
__TOOLID__   =  '75311cac-820f-11ed-a24f-a85e45e349c7'
__TOOLDESC__ = ''
__TOOLICON__ = 'exporter.png'

def main():
    import studio.tools.content_exporter.export_window as export_window
    export_window.showUI(None,None,True)