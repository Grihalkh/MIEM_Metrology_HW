# This Python file uses the following encoding: utf-8
import sys
from PyQt5.QtWidgets import QApplication
import libs.interface as ui


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ui.Ui()
    sys.exit(app.exec_())
