# -*- coding: utf-8 -*-
import sys
import re

from PyQt5 import QtWidgets
from UI import Ui_MainWindow

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

        # ComboBox
        all_langs = [lexer[0] for lexer in lexers.get_all_lexers()]
        all_styles = [style for style in styles.get_all_styles()]
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
        # Initial
        self.kw_color = {}

        style = styles.get_style_by_name(self.ui.comboBox_2.currentText())
        class_style = HtmlFormatter(style=style).get_style_defs('.highlight')
        print(class_style)

        self.background = re.findall('\{ background: (#......;)', class_style)[0]
        print(self.background)

        class_style = re.findall('.highlight (\.\w+) \{ (.+) \}', class_style)
        for cs in class_style:
            key = 'class="{}"'.format(cs[0][1:])
            style = 'style="{};"'.format(cs[1])

            self.kw_color[key] = style

        # Highlight
        lines = code.split('\n')
        results = ''
        kw = set()

        lexer = lexers.get_lexer_by_name(self.ui.comboBox.currentText())

        for n in range(len(lines)):
            space_n = 0
            for w in lines[n]:
                if w != ' ': break
                space_n += 1

            highlight_line = highlight(lines[n], lexer, HtmlFormatter())
            new_line = re.findall('<span>.+', highlight_line)[0]
            new_line = re.sub('<span></span>', '<span>{}</span>'.format('&nbsp;' * space_n), new_line)

            for kc in self.kw_color:
                new_line = re.sub(kc, self.kw_color[kc], new_line)
            results += new_line

            if n != len(lines) - 1:
                results += '<br>\n'

            for w in re.findall('class="\w+">', new_line):
                kw.add(w)

        results = '<div style="overflow: auto; background: {}; border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;">\n<pre style="margin: 0; line-height: 125%; white-space:nowrap">\n'.format(self.background) + results + '</pre></div>'

        return results


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())