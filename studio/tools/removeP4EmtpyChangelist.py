__TOOLNAME__ = 'Perforce: Removes empty unused changelists'
__TOOLID__   = '81b3e0b0-7c09-11e9-a51b-f07959dbdf47'
__TOOLDESC__ = 'Removes all empty unsed perforce changelist'
__TOOLICON__ = 'perforce.png'

def main():
    import helix.perforce as p4
    p4w = p4.PerforceWrapper()
    p4w.deleteEmptyChangelist()