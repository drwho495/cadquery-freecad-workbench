from CQGui.display import show_object
from CQGui.CodeFeature import upload_part

# Register the show_object function as a global function
globals()['show_object'] = show_object
globals()['upload_part'] = upload_part
