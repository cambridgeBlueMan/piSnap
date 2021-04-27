from PyQt5 import QtWidgets as qtw
class KeyboardSlider(qtw.QSlider):
    def __init__(self,parent):
        super().__init__(parent)
        
    def keyPressEvent(self, event):
        if event.key()==16777235:
            #print('in key up')
            self.setValue(self.value() +1) # uparrow
            #print(self.value())
        if event.key() == 16777237:
            #print('in key down')
            self.setValue(self.value() -1) # down arrow
            #print(self.value())
