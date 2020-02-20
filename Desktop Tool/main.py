# -*- coding: utf-8 -*-
import sys
import re

from PyQt5 import QtWidgets
from UI import Ui_MainWindow
from highlight import Highlight

from pygments import highlight
from pygments import lexers, styles
from pygments.formatters.html import HtmlFormatter


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Code-to-Html')

        # StyleSheet
        self.setStyleSheet('''
        QMainWindow{background-color:
        qlineargradient(spread:
        pad, x1:0, y1:0.5, x2:1, y2:0.5,
        stop:0 rgb(255, 255, 255),
        stop:1 rgb(150, 150, 150));}
        ''')

        # Highlight class
        self.highlight = Highlight()

        # ComboBox
        all_langs = self.highlight.return_all_languages()
        all_styles = self.highlight.return_all_styles()
        self.ui.comboBox.addItems(all_langs)
        self.ui.comboBox_2.addItems(all_styles)

        # Button
        self.ui.pushButton.clicked.connect(self.convertEvent)

    def convertEvent(self):
        code = self.ui.plainTextEdit.toPlainText()
        code = self.highlightEvent(code)
        self.ui.plainTextEdit_2.setPlainText(code)
        self.ui.textBrowser.setHtml(code)

    def highlightEvent(self, code):
        lexer = self.ui.comboBox.currentText()
        style = self.ui.comboBox_2.currentText()
        results = self.highlight.highlightEvent(code, style, lexer)

        return results


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())