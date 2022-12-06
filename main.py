import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from src.movieSplashScreen import *
from qt_material import apply_stylesheet
from src.settings import *
from src.mainWindow import MainWindow

if __name__ == "__main__":
    # create the application and the main window
    app = QApplication(sys.argv)
    window = MainWindow()
    
    # setup stylesheet
    # See this link for more information. -> https://pypi.org/project/qt-material/
    extra = {
        # Font
        'font_family': '나눔고딕',
        'font_size': '12px'
    }
    apply_stylesheet(app, theme='src/theme.xml', invert_secondary = True, extra = extra)
    
    window.show()

    try:
        sys.exit(app.exec_())
    except:
        settings.expireInfo()
        print("Exiting")