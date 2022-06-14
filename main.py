from gui import Window
from PySide6.QtWidgets import QApplication
import sys

def main():
    jRemiteApp = QApplication(sys.argv)
    jRemiteWindow = Window()
    jRemiteWindow.show()
    jRemiteApp.exec()
if __name__ == '__main__':
    main()