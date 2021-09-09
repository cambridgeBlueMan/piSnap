
# This function takes the info which has been passed in and outputs it 
# to the terminal widget
# The second (boolean) argument indicates whether the terminal widget should
# by cleared prior to adding the new information   
# note that in order to be usable by the app that psFunctions will have to be imported
# into any files where it is to be used  
"""when calling this function from psPiSnap ref should be 'self' but when calling this fucntion from anywhere else ref should be self.window()"""
def printT(ref, val, clear=False):

    """
    setPlainText() : deletes existing text and replaces
    insertPlainText : inserts text at the current cursor pos
    appendPlainText() : appends a new paragraph at the end 
    """
    if clear==True:
        ref.terminalWidget.clear()
    ref.terminalWidget.appendPlainText(val)