import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QPushButton,\
                            QLineEdit, QDesktopWidget, QComboBox,  QApplication

app = QApplication(sys.argv)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_window()

    def init_window(self):
        self.setWindowTitle("QtDeepL v1.0")
        self.resize(610, 390)
        self.setStyleSheet("background-color: rgb(47, 47, 47);")

        self.center_window()
        self.buttons_window()
        self.line_edits()
        self.combo_boxes()

        self.show()
        sys.exit(app.exec_())

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def buttons_window(self):
        self.btn_translate = QPushButton('Translate', self)
        self.btn_switch_lang = QPushButton('Switch Lang', self)
        self.btn_reverse_lang = QPushButton('<-------->', self)

        self.btn_translate.setGeometry(QtCore.QRect(260, 280, 91, 31))
        self.btn_switch_lang.setGeometry(QtCore.QRect(490, 342, 111, 21))
        self.btn_reverse_lang.setGeometry(QtCore.QRect(210, 10, 181, 21))

        self.btn_translate.setStyleSheet("color: rgb(255, 255, 255);\n" 
                                         "font: 57 8pt \"Fira Code Medium\";")
        self.btn_switch_lang.setStyleSheet("color: rgb(255, 255, 255);\n"
                                           "font: 57 8pt \"Fira Code Medium\";")
        self.btn_reverse_lang.setStyleSheet("color: rgb(255, 255, 255);\n"
                                            "font: 57 8pt \"Fira Code Medium\";")
        
    def line_edits(self):
        self.in_text = QLineEdit(self)
        self.out_text = QLineEdit(self)

        self.in_text.setGeometry(QtCore.QRect(10, 40, 281, 231))
        self.out_text.setGeometry(QtCore.QRect(310, 40, 291, 231))

        self.in_text.setStyleSheet("background-color: rgb(24, 24, 24);")
        self.out_text.setStyleSheet("background-color: rgb(25, 25, 25);")

    def combo_boxes(self):
        self.combo_box_one = QComboBox(self)
        self.combo_box_two = QComboBox(self)

        self.combo_box_one.setGeometry(QtCore.QRect(10, 10, 91, 22))
        self.combo_box_two.setGeometry(QtCore.QRect(508, 10, 91, 22))

        self.combo_box_one.setStyleSheet("color: rgb(255, 255, 255);\n" 
                                         "font: 57 8pt \"Fira Code Medium\";")
        self.combo_box_two.setStyleSheet("color: rgb(255, 255, 255);\n"
                                         "font: 57 8pt \"Fira Code Medium\";")