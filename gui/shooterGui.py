# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shooterGui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1163, 889)
        self.captureTab = QtWidgets.QTabWidget(Form)
        self.captureTab.setGeometry(QtCore.QRect(240, 650, 801, 221))
        self.captureTab.setInputMethodHints(QtCore.Qt.ImhUrlCharactersOnly)
        self.captureTab.setObjectName("captureTab")
        self.still = QtWidgets.QWidget()
        self.still.setObjectName("still")
        self.snapHold = QtWidgets.QPushButton(self.still)
        self.snapHold.setGeometry(QtCore.QRect(20, 20, 99, 30))
        self.snapHold.setObjectName("snapHold")
        self.snapSave = QtWidgets.QPushButton(self.still)
        self.snapSave.setGeometry(QtCore.QRect(140, 20, 99, 30))
        self.snapSave.setObjectName("snapSave")
        self.isCounter = QtWidgets.QRadioButton(self.still)
        self.isCounter.setGeometry(QtCore.QRect(630, 20, 119, 27))
        self.isCounter.setChecked(True)
        self.isCounter.setObjectName("isCounter")
        self.isDatestamp = QtWidgets.QRadioButton(self.still)
        self.isDatestamp.setGeometry(QtCore.QRect(510, 20, 119, 27))
        self.isDatestamp.setObjectName("isDatestamp")
        self.formLayoutWidget_3 = QtWidgets.QWidget(self.still)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(270, 20, 160, 34))
        self.formLayoutWidget_3.setObjectName("formLayoutWidget_3")
        self.formLayout_4 = QtWidgets.QFormLayout(self.formLayoutWidget_3)
        self.formLayout_4.setContentsMargins(0, 0, 0, 0)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_15 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_15.setObjectName("label_15")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_15)
        self.stillFileRoot = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        self.stillFileRoot.setInputMethodHints(QtCore.Qt.ImhNone)
        self.stillFileRoot.setObjectName("stillFileRoot")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.stillFileRoot)
        self.acceptStillRootUpdate = QtWidgets.QPushButton(self.still)
        self.acceptStillRootUpdate.setGeometry(QtCore.QRect(440, 20, 61, 30))
        self.acceptStillRootUpdate.setObjectName("acceptStillRootUpdate")
        self.captureTab.addTab(self.still, "")
        self.video = QtWidgets.QWidget()
        self.video.setObjectName("video")
        self.vidPosSlider = QtWidgets.QSlider(self.video)
        self.vidPosSlider.setGeometry(QtCore.QRect(220, 30, 571, 26))
        self.vidPosSlider.setMaximum(1000)
        self.vidPosSlider.setOrientation(QtCore.Qt.Horizontal)
        self.vidPosSlider.setObjectName("vidPosSlider")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.video)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 196, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.startRecordVid = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.startRecordVid.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/media-record.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.startRecordVid.setIcon(icon)
        self.startRecordVid.setObjectName("startRecordVid")
        self.horizontalLayout_2.addWidget(self.startRecordVid)
        self.playVid = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.playVid.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/media-playback-start.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playVid.setIcon(icon1)
        self.playVid.setObjectName("playVid")
        self.horizontalLayout_2.addWidget(self.playVid)
        self.stopVid = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.stopVid.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/media-playback-stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stopVid.setIcon(icon2)
        self.stopVid.setObjectName("stopVid")
        self.horizontalLayout_2.addWidget(self.stopVid)
        self.pauseVid = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pauseVid.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/media-playback-pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pauseVid.setIcon(icon3)
        self.pauseVid.setObjectName("pauseVid")
        self.horizontalLayout_2.addWidget(self.pauseVid)
        self.useZoomOnRecord = QtWidgets.QCheckBox(self.video)
        self.useZoomOnRecord.setGeometry(QtCore.QRect(10, 90, 181, 27))
        self.useZoomOnRecord.setObjectName("useZoomOnRecord")
        self.videoStabilization = QtWidgets.QCheckBox(self.video)
        self.videoStabilization.setGeometry(QtCore.QRect(10, 130, 171, 27))
        self.videoStabilization.setObjectName("videoStabilization")
        self.frameRate = QtWidgets.QComboBox(self.video)
        self.frameRate.setGeometry(QtCore.QRect(340, 90, 83, 32))
        self.frameRate.setObjectName("frameRate")
        self.frameRate.addItem("")
        self.frameRate.addItem("")
        self.frameRate.addItem("")
        self.frameRate.addItem("")
        self.frameRateLabel = QtWidgets.QLabel(self.video)
        self.frameRateLabel.setGeometry(QtCore.QRect(240, 90, 91, 22))
        self.frameRateLabel.setObjectName("frameRateLabel")
        self.formLayoutWidget = QtWidgets.QWidget(self.video)
        self.formLayoutWidget.setGeometry(QtCore.QRect(440, 90, 160, 41))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.videoFileRoot = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.videoFileRoot.setInputMethodHints(QtCore.Qt.ImhNone)
        self.videoFileRoot.setObjectName("videoFileRoot")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.videoFileRoot)
        self.acceptVideoRootUpdate = QtWidgets.QPushButton(self.video)
        self.acceptVideoRootUpdate.setGeometry(QtCore.QRect(610, 90, 61, 30))
        self.acceptVideoRootUpdate.setObjectName("acceptVideoRootUpdate")
        self.captureTab.addTab(self.video, "")
        self.thumbnails = QtWidgets.QListWidget(Form)
        self.thumbnails.setGeometry(QtCore.QRect(20, 10, 140, 601))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.thumbnails.setFont(font)
        self.thumbnails.setIconSize(QtCore.QSize(128, 96))
        self.thumbnails.setViewMode(QtWidgets.QListView.IconMode)
        self.thumbnails.setWordWrap(True)
        self.thumbnails.setObjectName("thumbnails")
        self.resizePreview = QtWidgets.QSlider(Form)
        self.resizePreview.setGeometry(QtCore.QRect(360, 620, 591, 26))
        self.resizePreview.setOrientation(QtCore.Qt.Horizontal)
        self.resizePreview.setObjectName("resizePreview")
        self.previewVisible = QtWidgets.QCheckBox(Form)
        self.previewVisible.setGeometry(QtCore.QRect(240, 620, 101, 27))
        self.previewVisible.setObjectName("previewVisible")
        self.imgContainer = QtWidgets.QLabel(Form)
        self.imgContainer.setGeometry(QtCore.QRect(190, 10, 800, 600))
        self.imgContainer.setFrameShape(QtWidgets.QFrame.Box)
        self.imgContainer.setText("")
        self.imgContainer.setObjectName("imgContainer")
        self.previewFrame = QtWidgets.QFrame(Form)
        self.previewFrame.setEnabled(False)
        self.previewFrame.setGeometry(QtCore.QRect(20, 650, 214, 130))
        self.previewFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.previewFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.previewFrame.setObjectName("previewFrame")
        self.previewButton = DragButton(self.previewFrame)
        self.previewButton.setEnabled(False)
        self.previewButton.setGeometry(QtCore.QRect(0, 0, 31, 30))
        self.previewButton.setObjectName("previewButton")
        self.unlockPreview = QtWidgets.QCheckBox(Form)
        self.unlockPreview.setGeometry(QtCore.QRect(20, 790, 141, 27))
        self.unlockPreview.setObjectName("unlockPreview")

        self.retranslateUi(Form)
        self.captureTab.setCurrentIndex(1)
        self.thumbnails.itemDoubleClicked['QListWidgetItem*'].connect(Form.doThumbnailClicked)
        self.stopVid.clicked.connect(Form.doStopVid)
        self.startRecordVid.clicked.connect(Form.doRecordVid)
        self.resizePreview.valueChanged['int'].connect(Form.setPreviewSize)
        self.vidPosSlider.sliderMoved['int'].connect(Form.setPosition)
        self.snapSave.clicked.connect(Form.snapAndHold)
        self.snapHold.clicked.connect(Form.snapAndSave)
        self.previewVisible.clicked.connect(Form.showPreview)
        self.playVid.clicked.connect(Form.doPlayVid)
        self.pauseVid.clicked.connect(Form.doPauseVid)
        self.isDatestamp.clicked.connect(Form.isDateStamp)
        self.isCounter.clicked.connect(Form.isCounter)
        self.stillFileRoot.textChanged['QString'].connect(Form.setFileRoot)
        self.captureTab.currentChanged['int'].connect(Form.setCaptureMode)
        self.previewButton.released.connect(Form.movePreview)
        self.previewButton.posChanged['int','int'].connect(Form.movePreviewOrigin)
        self.useZoomOnRecord.clicked['bool'].connect(Form.setRecordZoomFlag)
        self.videoStabilization.clicked['bool'].connect(Form.doVideoStabilization)
        self.frameRate.currentIndexChanged['QString'].connect(Form.setFrameRate)
        self.acceptStillRootUpdate.clicked.connect(Form.updateStillRoot)
        self.acceptVideoRootUpdate.clicked.connect(Form.updateVideoRoot)
        self.unlockPreview.clicked['bool'].connect(Form.setPreviewLockState)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.snapHold.setText(_translate("Form", "Snap/Save"))
        self.snapSave.setText(_translate("Form", "Snap/Hold"))
        self.isCounter.setText(_translate("Form", "Counter "))
        self.isDatestamp.setText(_translate("Form", "Datestamp"))
        self.label_15.setText(_translate("Form", "File root"))
        self.stillFileRoot.setText(_translate("Form", "img_"))
        self.acceptStillRootUpdate.setText(_translate("Form", "Update"))
        self.captureTab.setTabText(self.captureTab.indexOf(self.still), _translate("Form", "Still"))
        self.useZoomOnRecord.setText(_translate("Form", "Use Zoom on Record"))
        self.videoStabilization.setText(_translate("Form", "Video Stabilization"))
        self.frameRate.setItemText(0, _translate("Form", "25"))
        self.frameRate.setItemText(1, _translate("Form", "30"))
        self.frameRate.setItemText(2, _translate("Form", "35"))
        self.frameRate.setItemText(3, _translate("Form", "40"))
        self.frameRateLabel.setText(_translate("Form", "Frame Rate"))
        self.label.setText(_translate("Form", "File Root"))
        self.videoFileRoot.setText(_translate("Form", "img_"))
        self.acceptVideoRootUpdate.setText(_translate("Form", "Update"))
        self.captureTab.setTabText(self.captureTab.indexOf(self.video), _translate("Form", "Video"))
        self.previewVisible.setText(_translate("Form", "Preview"))
        self.previewButton.setText(_translate("Form", "b"))
        self.unlockPreview.setText(_translate("Form", "Unlock Preview"))

from dragbutton import DragButton
import resource_rc
