from PyQt5.QtWidgets import QDesktopWidget

def getScreenDimensions():
    screen = QDesktopWidget().screenGeometry()
    screen_width = screen.width()
    screen_height = screen.height()
    return screen_width, screen_height