__TOOLNAME__ = 'Check Out & Save'
__TOOLID__   = '905e8370-8011-11e4-b278-f8b156ce75fa'
__TOOLDESC__ = 'Attempts to check out the current scene in source control, then saves scene.'
__TOOLICON__ = 'p4checkOutSave.png'

def main():
	import io_utils as save
	save.save_file()