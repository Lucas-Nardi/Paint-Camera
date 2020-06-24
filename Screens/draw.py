import cv2
import os
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
# import some PyQt5 modules
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.Qt import Qt

from Qt_Forms.paintScreenForms import Ui_Form
from PyQt5 import QtCore, QtWidgets


BACKGROUND = "./Image/drawing/background.jpg"

class PaintScreen(QtWidgets.QWidget):

    toEdition = QtCore.pyqtSignal()
    toInitial = QtCore.pyqtSignal()
    drawing = False
    imgResult = None
                # [hue_min, saturation_min, value_min, hue_max, saturation_max, value_max]
    paintBrush = [ [149, 157, 0, 179, 255, 255] ]      # The object data the camera can capture with this range channel de camera
    
    correntColor = [ [0,0,0] ]   # BGR color format, the color that im using to paint
                  
    myPoints =  []  ## [x , y , [B, G, R], size ] All points of my draw

    idPointColor = 0;

    # the colors is in B G R pattern
    favoritesColor =[ [15, 196, 241], [39, 174, 96], [219, 152, 52], [173, 68, 142], 
                      
                      [60, 76, 231 ], [34, 126, 230], [171, 178, 185 ], [94, 73, 52] ]      

    toErase = False 
    eraseX = 0
    eraseY = 0

    def __init__(self):
        super().__init__()
        self.image = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # create a timer
        self.timer = QTimer()
        self.canIDraw()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        # set control_bt callback clicked  function
        
        self.ui.screen.setPixmap(QtGui.QPixmap(BACKGROUND))           

        self.ui.save_draw_button.clicked.connect(self.initialScreen)

        # Taking the value of red channel, green channel and blue channel
        self.ui.red_channel.valueChanged.connect(self.channelRed) 
        self.ui.green_channel.valueChanged.connect(self.channelGreen)
        self.ui.blue_channel.valueChanged.connect(self.channelBlue)

        # Setting the color of favorite colors

        self.ui.favorite_color1.setStyleSheet("background-color: rgb(" + "{}".format(self.favoritesColor[0][2]) + "," + "{}".format(self.favoritesColor[0][1]) + "," + "{}".format(self.favoritesColor[0][0]) +")")
        self.ui.favorite_color2.setStyleSheet("background-color: rgb(" + "{}".format(self.favoritesColor[1][2]) + "," + "{}".format(self.favoritesColor[1][1]) + "," + "{}".format(self.favoritesColor[1][0]) +")")
        self.ui.favorite_color3.setStyleSheet("background-color: rgb(" + "{}".format(self.favoritesColor[2][2]) + "," + "{}".format(self.favoritesColor[2][1]) + "," + "{}".format(self.favoritesColor[2][0]) +")")
        self.ui.favorite_color4.setStyleSheet("background-color: rgb(" + "{}".format(self.favoritesColor[3][2]) + "," + "{}".format(self.favoritesColor[3][1]) + "," + "{}".format(self.favoritesColor[3][0]) +")")
        self.ui.favorite_color5.setStyleSheet("background-color: rgb(" + "{}".format(self.favoritesColor[4][2]) + "," + "{}".format(self.favoritesColor[4][1]) + "," + "{}".format(self.favoritesColor[4][0]) +")")
        self.ui.favorite_color6.setStyleSheet("background-color: rgb(" + "{}".format(self.favoritesColor[5][2]) + "," + "{}".format(self.favoritesColor[5][1]) + "," + "{}".format(self.favoritesColor[5][0]) +")")
        self.ui.favorite_color7.setStyleSheet("background-color: rgb(" + "{}".format(self.favoritesColor[6][2]) + "," + "{}".format(self.favoritesColor[6][1]) + "," + "{}".format(self.favoritesColor[6][0]) +")")
        self.ui.favorite_color8.setStyleSheet("background-color: rgb(" + "{}".format(self.favoritesColor[7][2]) + "," + "{}".format(self.favoritesColor[7][1]) + "," + "{}".format(self.favoritesColor[7][0]) +")")


        # Brush Paint 
        self.ui.brush_paint_size.valueChanged.connect(self.brushSize)

        #Erase button
        self.ui.erase_button.clicked.connect(self.erase)


        # Rotation 
        self.ui.rotation_slider.valueChanged.connect(self.rotation)

        #Setting the on click favorite color buttons

        self.ui.favorite_color1.clicked.connect(self.takeMyFavoriteColo1)
        self.ui.favorite_color2.clicked.connect(self.takeMyFavoriteColo2)
        self.ui.favorite_color3.clicked.connect(self.takeMyFavoriteColo3)
        self.ui.favorite_color4.clicked.connect(self.takeMyFavoriteColo4)
        self.ui.favorite_color5.clicked.connect(self.takeMyFavoriteColo5)
        self.ui.favorite_color6.clicked.connect(self.takeMyFavoriteColo6)
        self.ui.favorite_color7.clicked.connect(self.takeMyFavoriteColo7)
        self.ui.favorite_color8.clicked.connect(self.takeMyFavoriteColo8)
    
    def takeMyFavoriteColo1(self):    

        self.toErase = False
        self.correntColor[0][0] = self.favoritesColor[0][0]  # B
        self.correntColor[0][1] = self.favoritesColor[0][1]  # G
        self.correntColor[0][2] = self.favoritesColor[0][2]  # R
        self.ui.color.setStyleSheet("background-color: rgb(" + "{}".format(self.correntColor[0][2]) + "," + "{}".format(self.correntColor[0][1]) + "," + "{}".format(self.correntColor[0][0]) +")")
        
        self.ui.red_channel.setValue(self.favoritesColor[0][2])
        self.ui.green_channel.setValue(self.favoritesColor[0][1])
        self.ui.blue_channel.setValue(self.favoritesColor[0][0])

    def takeMyFavoriteColo2(self):    

        self.toErase = False
        self.correntColor[0][0] = self.favoritesColor[1][0]
        self.correntColor[0][1] = self.favoritesColor[1][1]
        self.correntColor[0][2] = self.favoritesColor[1][2]
        self.ui.color.setStyleSheet("background-color: rgb(" + "{}".format(self.correntColor[0][2]) + "," + "{}".format(self.correntColor[0][1]) + "," + "{}".format(self.correntColor[0][0]) +")")
        
        self.ui.red_channel.setValue(self.favoritesColor[1][2])
        self.ui.green_channel.setValue(self.favoritesColor[1][1])
        self.ui.blue_channel.setValue(self.favoritesColor[1][0])

    def takeMyFavoriteColo3(self):    

        self.toErase = False
        self.correntColor[0][0] = self.favoritesColor[2][0] # B
        self.correntColor[0][1] = self.favoritesColor[2][1] # G
        self.correntColor[0][2] = self.favoritesColor[2][2] # R
        self.ui.color.setStyleSheet("background-color: rgb(" + "{}".format(self.correntColor[0][2]) + "," + "{}".format(self.correntColor[0][1]) + "," + "{}".format(self.correntColor[0][0]) +")")
        
        self.ui.red_channel.setValue(self.favoritesColor[2][2])
        self.ui.green_channel.setValue(self.favoritesColor[2][1])
        self.ui.blue_channel.setValue(self.favoritesColor[2][0])

    def takeMyFavoriteColo4(self):    

        self.toErase = False
        self.correntColor[0][0] = self.favoritesColor[3][0]
        self.correntColor[0][1] = self.favoritesColor[3][1]
        self.correntColor[0][2] = self.favoritesColor[3][2]
        self.ui.color.setStyleSheet("background-color: rgb(" + "{}".format(self.correntColor[0][2]) + "," + "{}".format(self.correntColor[0][1]) + "," + "{}".format(self.correntColor[0][0]) +")")

        
        self.ui.red_channel.setValue(self.favoritesColor[3][2])
        self.ui.green_channel.setValue(self.favoritesColor[3][1])
        self.ui.blue_channel.setValue(self.favoritesColor[3][0])

    def takeMyFavoriteColo5(self):    

        self.toErase = False
        self.correntColor[0][0] = self.favoritesColor[4][0]
        self.correntColor[0][1] = self.favoritesColor[4][1]
        self.correntColor[0][2] = self.favoritesColor[4][2]
        self.ui.color.setStyleSheet("background-color: rgb(" + "{}".format(self.correntColor[0][2]) + "," + "{}".format(self.correntColor[0][1]) + "," + "{}".format(self.correntColor[0][0]) +")")

        self.ui.red_channel.setValue(self.favoritesColor[4][2])
        self.ui.green_channel.setValue(self.favoritesColor[4][1])
        self.ui.blue_channel.setValue(self.favoritesColor[4][0])

    def takeMyFavoriteColo6(self):    

        self.toErase = False
        self.correntColor[0][0] = self.favoritesColor[5][0]
        self.correntColor[0][1] = self.favoritesColor[5][1]
        self.correntColor[0][2] = self.favoritesColor[5][2]
        self.ui.color.setStyleSheet("background-color: rgb(" + "{}".format(self.correntColor[0][2]) + "," + "{}".format(self.correntColor[0][1]) + "," + "{}".format(self.correntColor[0][0]) +")")       
        
        self.ui.red_channel.setValue(self.favoritesColor[5][2])
        self.ui.green_channel.setValue(self.favoritesColor[5][1])
        self.ui.blue_channel.setValue(self.favoritesColor[5][0])

    def takeMyFavoriteColo7(self):    

        self.toErase = False
        self.correntColor[0][0] = self.favoritesColor[6][0]
        self.correntColor[0][1] = self.favoritesColor[6][1]
        self.correntColor[0][2] = self.favoritesColor[6][2]
        self.ui.color.setStyleSheet("background-color: rgb(" + "{}".format(self.correntColor[0][2]) + "," + "{}".format(self.correntColor[0][1]) + "," + "{}".format(self.correntColor[0][0]) +")")
        
        self.ui.red_channel.setValue(self.favoritesColor[6][2])
        self.ui.green_channel.setValue(self.favoritesColor[6][1])
        self.ui.blue_channel.setValue(self.favoritesColor[6][0])

    def takeMyFavoriteColo8(self):    

        self.toErase = False
        self.correntColor[0][0] = self.favoritesColor[7][2]
        self.correntColor[0][1] = self.favoritesColor[7][1]
        self.correntColor[0][2] = self.favoritesColor[7][0]
        self.ui.color.setStyleSheet("background-color: rgb(" + "{}".format(self.correntColor[0][2]) + "," + "{}".format(self.correntColor[0][1]) + "," + "{}".format(self.correntColor[0][0]) +")")
        
        self.ui.red_channel.setValue(self.favoritesColor[7][2])
        self.ui.green_channel.setValue(self.favoritesColor[7][1])
        self.ui.blue_channel.setValue(self.favoritesColor[7][0])

    def erase(self):
        self.toErase = True

    def channelRed(self):
        
        self.toErase = False
        _translate = QtCore.QCoreApplication.translate
        value = self.ui.red_channel.value()
        self.correntColor[0][2] = value
        self.ui.red_channel_value.setText(_translate("Form", "{}".format(value)))        
        self.ui.color.setStyleSheet("background-color: rgb(" + "{}".format(self.correntColor[0][2]) + "," + "{}".format(self.correntColor[0][1]) + "," + "{}".format(self.correntColor[0][0]) +")")
                                
    def channelGreen(self):
        
        self.toErase = False
        _translate = QtCore.QCoreApplication.translate
        value = self.ui.green_channel.value()
        self.correntColor[0][1] = value
        self.ui.green_channel_value.setText(_translate("Form", "{}".format(value)))        
        self.ui.color.setStyleSheet("background-color: rgb(" + "{}".format(self.correntColor[0][2]) + "," + "{}".format(self.correntColor[0][1]) + "," + "{}".format(self.correntColor[0][0]) +")")
    
    def channelBlue(self):
        
        self.toErase = False
        _translate = QtCore.QCoreApplication.translate
        value = self.ui.blue_channel.value()
        self.correntColor[0][0] = value
        self.ui.blue_channel_value.setText(_translate("Form", "{}".format(value)))        
        self.ui.color.setStyleSheet("background-color: rgb(" + "{}".format(self.correntColor[0][2]) + "," + "{}".format(self.correntColor[0][1]) + "," + "{}".format(self.correntColor[0][0]) +")")

    def brushSize(self):
        _translate = QtCore.QCoreApplication.translate
        value = self.ui.brush_paint_size.value()
        self.ui.size_value.setText(_translate("Form", "{}".format(value)))        

    def rotation(self):
        _translate = QtCore.QCoreApplication.translate
        value = self.ui.rotation_slider.value()
        self.ui.rotation_value.setText(_translate("Form", "{}".format(value)))

    def initialScreen(self):
        self.timer.stop()
        self.cap.release()
        self.toInitial.emit()

    def editar(self):
        self.switch_window.emit()

        # view camera
    
    def keyPressEvent(self, event):

        if(event.key() == 81):
            self.canIDraw()

        

    def viewCam(self):

    
        ret, self.image = self.cap.read()
                
        self.image = cv2.flip(self.image, 1)

        #if(self.stopDrawing == True):

        s = self.findColor(self.image, self.paintBrush, self.correntColor)

        if ( s != None and len(s) !=0) :
            for newP in s:                
                self.myPoints.append(newP)
    
        if (len(self.myPoints)!=0 ):
            self.drawOnCanvas(self.myPoints)


        # read image in BGR format
        # convert image to RGB format
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        # get image infos
        height, width, channel = self.image.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(self.image.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.screen.setPixmap(QPixmap.fromImage(qImg))

    def drawOnCanvas(self,myPoints):
        
    
        if(self.drawing):
            
            self.image = cv2.imread(BACKGROUND)
        
            for point in myPoints:       # X        Y            Size                              Color

                if(self.toErase == False):

                    cv2.circle(self.image, (point[0], point[1]), point[3], point[2] , cv2.FILLED)
                
                else:
                    
                    if( point[0] >= (self.eraseX - self.ui.brush_paint_size.value()) and point[0] <= (self.eraseX + self.ui.brush_paint_size.value())  and point[1] >= (self.eraseY - self.ui.brush_paint_size.value()) and point[1] <= (self.eraseY + self.ui.brush_paint_size.value())):
                        myPoints.remove(point)

                    else:

                        cv2.circle(self.image, (point[0], point[1]), point[3], point[2] , cv2.FILLED)
                      
    def findColor(self,img,paintBrush,correntColor):
    

        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        newPoint=[]
        size = self.ui.brush_paint_size.value()
      
        cor = [self.ui.blue_channel.value(), self.ui.green_channel.value(),self.ui.red_channel.value()]

        for color in paintBrush:
            lower = np.array(color[0:3])
            upper = np.array(color[3:6])
            mask = cv2.inRange(imgHSV,lower,upper)
            x,y= self.getContours(mask)
            
            if(self.toErase == False):

                if (x!=0 and y!=0):  # Mem count colocar quanl é a cor atual
                    newPoint.append([x,y,cor,size])
                    self.idPointColor = self.idPointColor + 1

            else:
                
                cv2.circle(self.image,(x,y),size, [255,255,255],cv2.FILLED) # Cursor do Pincel 
                self.eraseX = x
                self.eraseY = y
                return None 

        return newPoint

    def take_photo(self):
            
        self.image =  cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        cv2.imwrite("./image/drawing/draw.jpg", self.image)
        self.ui.screen.setPixmap(QtGui.QPixmap("./image/drawing/draw.jpg"))
        #self.ui.editar.setEnabled(True)

    def controlTimer(self):
        # if timer is stopped
        
        if (not self.timer.isActive() and self.drawing):

            # create video capture
            self.cap = cv2.VideoCapture(0)
            # start timer
            self.timer.start(20)
            
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.take_photo()

    def canIDraw(self):
    
        if(self.drawing == False):
            
            self.drawing = True
            self.controlTimer()
        
        else:

            self.drawing = False           
            self.controlTimer()

    def getContours(self,img):
        contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        x,y,w,h = 0,0,0,0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area>500:
                peri = cv2.arcLength(cnt,True)
                approx = cv2.approxPolyDP(cnt,0.02*peri,True)
                x, y, w, h = cv2.boundingRect(approx)
        
        return x+w//2,y
 