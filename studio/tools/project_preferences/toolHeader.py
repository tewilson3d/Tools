__TOOLNAME__ = 'Project Preferences UI'
#__TOOLID__ = '0aff6a80-1062-11e7-aa18-64006a959e92'
__TOOLDESC__ = 'Sets and stores maya preferences'
#__TOOLICON__ = 'monolith.png'

def main():
    import studio.tools.project_preferences.project_pref_window as mpui
    mpui.showUI()