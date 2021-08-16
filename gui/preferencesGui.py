# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preferencesGui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(536, 322)
        Dialog.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(20, 30, 351, 141))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.doSetPhotoPath = QtWidgets.QPushButton(self.frame)
        self.doSetPhotoPath.setGeometry(QtCore.QRect(10, 10, 99, 30))
        self.doSetPhotoPath.setStyleSheet("font: 11pt \"PibotoLt\";")
        self.doSetPhotoPath.setObjectName("doSetPhotoPath")
        self.doSetVideoPath = QtWidgets.QPushButton(self.frame)
        self.doSetVideoPath.setGeometry(QtCore.QRect(10, 50, 99, 30))
        self.doSetVideoPath.setStyleSheet("font: 11pt \"PibotoLt\";")
        self.doSetVideoPath.setObjectName("doSetVideoPath")
        self.doSetFilePath = QtWidgets.QPushButton(self.frame)
        self.doSetFilePath.setGeometry(QtCore.QRect(10, 90, 99, 30))
        self.doSetFilePath.setStyleSheet("font: 11pt \"PibotoLt\";")
        self.doSetFilePath.setObjectName("doSetFilePath")
        self.defaultPhotoPath = QtWidgets.QLabel(self.frame)
        self.defaultPhotoPath.setGeometry(QtCore.QRect(140, 10, 161, 21))
        self.defaultPhotoPath.setStyleSheet("color : blue")
        self.defaultPhotoPath.setObjectName("defaultPhotoPath")
        self.defaultVideoPath = QtWidgets.QLabel(self.frame)
        self.defaultVideoPath.setGeometry(QtCore.QRect(140, 50, 181, 22))
        self.defaultVideoPath.setStyleSheet("color : blue")
        self.defaultVideoPath.setObjectName("defaultVideoPath")
        self.defaultFilePath = QtWidgets.QLabel(self.frame)
        self.defaultFilePath.setGeometry(QtCore.QRect(140, 100, 181, 22))
        self.defaultFilePath.setStyleSheet("color : blue")
        self.defaultFilePath.setObjectName("defaultFilePath")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.doSetPhotoPath.clicked.connect(Dialog.setDefaultPhotoPath)
        self.doSetVideoPath.clicked.connect(Dialog.setDefaultVideoPath)
        self.doSetFilePath.clicked.connect(Dialog.setDefaultFilePath)
        self.buttonBox.accepted.connect(Dialog.doAccepted)
        self.buttonBox.rejected.connect(Dialog.doRejected)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.doSetPhotoPath.setText(_translate("Dialog", "Photos"))
        self.doSetVideoPath.setText(_translate("Dialog", "Videos"))
        self.doSetFilePath.setText(_translate("Dialog", "Files"))
        self.defaultPhotoPath.setText(_translate("Dialog", "/home/pi/Pictures"))
        self.defaultVideoPath.setText(_translate("Dialog", "/home/pi/Videos"))
        self.defaultFilePath.setText(_translate("Dialog", "/home/pi/Documents"))

