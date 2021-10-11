from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QFileInfo, QUrl

class ThumbnailsModel(QtCore.QAbstractListModel):
    def __init__(self):
        super().__init__()
        self._data = []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            theThumb, thePath, theRes = self._data[index.row()]
            return thePath.fileName()

        if role == Qt.DecorationRole:
            theThumb, thePath, theRes = self._data[index.row()]
            if theThumb:
                return theThumb

        if role == Qt.ToolTipRole:
            theThumb, thePath, theRes = self._data[index.row()]
            return thePath.path()

    def getVideoData(self, ix):
        return self._data[ix.row()]

    def rowCount(self, index):
        return len(self._data)
