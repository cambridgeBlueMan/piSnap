# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zoomTabGui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(537, 617)
        self.getZoom = KeyboardSlider(Form)
        self.getZoom.setGeometry(QtCore.QRect(10, 420, 501, 21))
        self.getZoom.setMinimum(1920)
        self.getZoom.setMaximum(3470)
        self.getZoom.setSingleStep(1)
        self.getZoom.setProperty("value", 3470)
        self.getZoom.setOrientation(QtCore.Qt.Horizontal)
        self.getZoom.setObjectName("getZoom")
        self.showPreview = QtWidgets.QCheckBox(Form)
        self.showPreview.setGeometry(QtCore.QRect(10, 580, 161, 27))
        self.showPreview.setObjectName("showPreview")
        self.start = QtWidgets.QPushButton(Form)
        self.start.setGeometry(QtCore.QRect(160, 490, 71, 30))
        self.start.setObjectName("start")
        self.showStart = QtWidgets.QPushButton(Form)
        self.showStart.setGeometry(QtCore.QRect(40, 490, 81, 30))
        self.showStart.setObjectName("showStart")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(670, 30, 91, 22))
        self.label_3.setObjectName("label_3")
        self.end = QtWidgets.QPushButton(Form)
        self.end.setGeometry(QtCore.QRect(160, 530, 71, 30))
        self.end.setObjectName("end")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(0, 0, 507, 380))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.adjustZoom = DragButton(self.frame)
        self.adjustZoom.setGeometry(QtCore.QRect(0, 0, 22, 22))
        self.adjustZoom.setObjectName("adjustZoom")
        self.runZoom = QtWidgets.QPushButton(Form)
        self.runZoom.setGeometry(QtCore.QRect(150, 570, 99, 30))
        self.runZoom.setObjectName("runZoom")
        self.showEnd = QtWidgets.QPushButton(Form)
        self.showEnd.setGeometry(QtCore.QRect(30, 540, 81, 30))
        self.showEnd.setObjectName("showEnd")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 390, 68, 22))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(280, 450, 68, 22))
        self.label_2.setObjectName("label_2")
        self.getSpeed = QtWidgets.QSlider(Form)
        self.getSpeed.setGeometry(QtCore.QRect(280, 490, 221, 26))
        self.getSpeed.setProperty("value", 49)
        self.getSpeed.setOrientation(QtCore.Qt.Horizontal)
        self.getSpeed.setObjectName("getSpeed")

        self.retranslateUi(Form)
        self.start.clicked.connect(Form.doSetStart)
        self.showStart.clicked.connect(Form.doShowStart)
        self.showPreview.clicked['bool'].connect(Form.showPreview)
        self.showEnd.clicked.connect(Form.doShowEnd)
        self.runZoom.clicked.connect(Form.doRunZoom)
        self.getZoom.valueChanged['int'].connect(Form.setZoom)
        self.end.clicked.connect(Form.doSetEnd)
        self.adjustZoom.posChanged['int','int'].connect(Form.setZoomWithButton)
        self.adjustZoom.released.connect(Form.movePosition)
        self.getSpeed.sliderMoved['int'].connect(Form.setSpeed)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.showPreview.setText(_translate("Form", "show preview"))
        self.start.setText(_translate("Form", "set start"))
        self.showStart.setText(_translate("Form", "show start"))
        self.label_3.setText(_translate("Form", "zoom"))
        self.end.setText(_translate("Form", "set end"))
        self.adjustZoom.setText(_translate("Form", "b"))
        self.runZoom.setText(_translate("Form", "run zoom"))
        self.showEnd.setText(_translate("Form", "show end"))
        self.label.setText(_translate("Form", "set Zoom"))
        self.label_2.setText(_translate("Form", "set Speed"))

from dragbutton import DragButton
from keyboardslider import KeyboardSlider