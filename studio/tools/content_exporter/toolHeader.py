__TOOLNAME__ = 'Asset Content Exporter'
__TOOLID__   = 'a4758968-39be-11ed-a2d4-a85e45e349c7'
__TOOLDESC__ = ''
__TOOLICON__ = 'exporter.png'

def main():
    import studio.tools.content_exporter.export_window as export_window
    export_window.showUI(True,True,True)
    