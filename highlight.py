# -*- coding: utf-8 -*-
import re
from pygments import highlight
from pygments import lexers, styles
from pygments.formatters.html import HtmlFormatter


class Highlight:
    def __init__(self):
        self.all_langs = [lexer[0] for lexer in lexers.get_all_lexers()]
        self.all_styles = [style for style in styles.get_all_styles()]

    def return_all_languages(self):
        ls = open('lexers.txt', 'r', encoding='utf-8').read()
        return ls.split('\n')

    def return_all_styles(self):
        return self.all_styles

    def highlightEvent(self, code, style, lang):
        # Build the style and lexer object
        style = styles.get_style_by_name(style)
        lexer = lexers.get_lexer_by_name(lang)

        # Set the highlight color of keywords
        class_style = HtmlFormatter(style=style).get_style_defs('.highlight')
        background = re.findall('\{ background: (#......;)', class_style)[0]
        class_styles = re.findall('.highlight (\.\w+) \{ (.+) \}', class_style)
        kw_color = dict()

        for cs in class_styles:
            key = 'class="{}"'.format(cs[0][1:])
            style = 'style="{};"'.format(cs[1])
            kw_color[key] = style

        # Highlight the code
        lines = code.split('\n')
        results = '<!-- More information can refer: https://clay-atlas.com/blog/2020/03/05/python-english-tutorial-package-pygments-highlight-code/ -->'
        kw = set()

        for n in range(len(lines)):
            space_n = 0
            for w in lines[n]:
                if w != ' ': break
                space_n += 1

            if space_n > 0: space_n -= 1

            highlight_line = highlight(lines[n], lexer, HtmlFormatter())
            new_line = re.findall('<span>.+', highlight_line)[0]
            new_line = re.sub('<span></span>', '<span>{}</span>'.format('&nbsp;' * space_n), new_line)

            for kc in kw_color:
                new_line = re.sub(kc, kw_color[kc], new_line)
            results += new_line

            if n != len(lines) - 1:
                results += '<br>\n'

            for w in re.findall('class="\w+">', new_line):
                kw.add(w)

        # Finished
        results = '<div style="overflow: auto;' \
                  'background: {};' \
                  'border:solid gray;' \
                  'border-width:.1em .1em .1em .8em;' \
                  'padding:.2em .6em;">\n' \
                  '<pre style="margin: 0; line-height: 125%;' \
                  'white-space:nowrap">\n'.format(background) + results + '</pre></div>'

        # results += '\n{}'.format('<textarea style="display:none">{}</textarea>\n<a style="position: absolute; bottom: 10px; right: 10px;" href="#head">testetstsetst<img src="upbutton.png" id="fixedbutton"></a>'.format(code))
        # print(results)

        return results
