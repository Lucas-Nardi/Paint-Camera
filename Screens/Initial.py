from PyQt5 import QtGui
from PyQt5 import QtCore, QtWidgets
from Qt_Forms.initialScreenForms import Ui_Form


class InitialScreen(QtWidgets.QWidget):

    toDraw = QtCore.pyqtSignal()

    exitScreen = QtCore.pyqtSignal()

    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.ui.draw_button.clicked.connect(self.switch)
        self.ui.exit_button.clicked.connect(self.exit)

    def switch(self):
        self.toDraw.emit()

    def exit(self):
        self.exitScreen.emit()