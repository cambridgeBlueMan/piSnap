import json

# open the settings file and put the contents into the 
class CameraSettings():
    def __init__(self, win, camera):  #first initialize the super class QWidget
        with open("settings.json", "r") as settings:
            self.camvals = json.load(settings)
            #print(self.camvals)
            #print(win)
            #print(camera)
            self.widgetList = []

    def registerWidget(self, widg):
        self.widgetList.append(widg)
        print(self.widgetList)

