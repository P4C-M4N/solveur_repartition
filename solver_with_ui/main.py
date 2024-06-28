# Importation des modules
import sys
from PyQt5.QtWidgets import QApplication
from windows.main_window import MainWindow
from styles import global_stylesheet
from utils import getScreenDimensions

# Module principal permettant de lancer l'application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen_width, screen_height = getScreenDimensions()
    print("Log : Largeur de l'écran --> ", screen_width)
    print("Log : Hauteur de l'écran --> ", screen_height)
    app.setStyleSheet(global_stylesheet.stylesheet)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())