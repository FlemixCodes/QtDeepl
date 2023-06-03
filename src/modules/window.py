import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QPushButton, QMessageBox,\
                            QLineEdit, QDesktopWidget, QComboBox,  QApplication

from .languages import Language

app = QApplication(sys.argv)


class Window(QMainWindow):
    fr_languages = {
        "Auto":"auto",
        "Bulgarian":"bg",
        "Czech":"cs",
        "Danish": "da",
        "German": "de",
        "Greek": "el",
        "English": "en",
        "Spanish": "es",
        "Estonian": "et",
        "Finnish": "fi",
        "France": "fr",
        "Hungarian": "hu",
        "Indonesian": "id",
        "Italian": "it",
        "Japan": "ja",
        "Korean": "ko",
        "Lithuanian": "lt",
        "Latvian": "lv",
        "Dutch": "nl",
        "Polish": "pl",
        "Portuguese": "pt",
        "Romanian": "ro",
        "Russian": "ru",
        "Slovak": "sk",
        "Slovenian": "sl",
        "Swedish": "sv",
        "Turkish": "tr",
        "Ukrainian": "uk",
        "Chinese": "zh",
    }
    to_languages = fr_languages.copy()
    to_languages.pop("Auto")

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

        self.multi_translator = Language()
        self.multi_translator.set_language("en")

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
        
    def reverse_language(self) -> None:
        temp = self.fr_language.get()
        
        if temp in self.to_languages:
            self.fr_language.set(self.to_language.get())
            self.to_language.set(temp)
        else:
            QMessageBox.warning(
                self,
                self.multi_translator.get_string('error'),
                self.multi_translator.get_string('error_auto')
            )

    def switch_language(self) -> None:
        continue_switch = None

        for language in self.multi_translator.get_languages():
            if language != self.multi_translator.get_select_language():
                continue_switch = language
                break

        self.multi_translator.set_language(continue_switch)

        # TODO: Reconfigure PyQt objects