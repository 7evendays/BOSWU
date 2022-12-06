from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
img_path = "src/imgsource/"


class MovieSplashScreen(QSplashScreen): #mainwindow 시작 전 스플래시 화면 
       def __init__(self, movie, parent = None):
          movie.jumpToFrame(0)
          pixmap = QPixmap(movie.frameRect().size())
           
          QSplashScreen.__init__(self, pixmap)
          self.movie = movie
          self.movie.frameChanged.connect(self.repaint)
           
       def showEvent(self, event):
           self.movie.start()
       
       def hideEvent(self, event):
           self.movie.stop()
       
       def paintEvent(self, event):
           painter = QPainter(self)
           pixmap = self.movie.currentPixmap()
           self.setMask(pixmap.mask())
           painter.drawPixmap(0, 0, pixmap)
       
       def sizeHint(self):
           return self.movie.scaledSize()