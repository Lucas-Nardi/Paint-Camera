# import system module
import sys

from Screens.Initial import InitialScreen
from Screens.draw import PaintScreen

from PyQt5 import QtWidgets
#from Screens.Telaedition import Telaedition

class Controller:

    def __init__(self):
        self.edition = None
        self.initial = None
        self.paint = None

    def show_initial(self):
        self.initial = InitialScreen()
       
        if (self.edition != None and self.edition.isVisible() ):
            self.edition.close()

        if(self.paint != None and self.paint.isVisible() ):
            self.paint.close()

        self.initial.toDraw.connect(self.show_paint_screen)
        self.initial.exitScreen.connect(self.exit)
        self.initial.show()

    def show_paint_screen(self):

        self.paint = PaintScreen()
        
        if(self.initial.isVisible() ):
            self.initial.close()
        
        if( self.edition != None and self.edition.isVisible() ):
            self.edition.close()

        #self.paint.toEdition.connect(self.show_edition)
        self.paint.toInitial.connect(self.show_initial)
        self.paint.show()

    #def show_edition(self):
     #   self.edition = Telaedition()
      #  self.edition.voltando.connect(self.show_paint_screen)
       # self.edition.initialScreen.connect(self.show_initial)
        #self.paint.close()
        #self.edition.show()

    def exit(self):
        if (self.initial != None and self.initial.isVisible() ):
            self.initial.close()
            sys.exit()

def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_initial()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()