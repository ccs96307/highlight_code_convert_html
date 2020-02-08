# -*- coding: utf-8 -*-
"""
Highlight Class
"""
import re
from pygments import highlight
from pygments.lexers.python import PythonLexer
from pygments.formatters.html import HtmlFormatter


class HighLight:
    def __init__(self):
        self.kw_color = {'class="kn"': 'style="color: #6ab825; font-weight: bold;"',
                 'class="nn"': 'style="color: #447fcf;"',
                 'class="n"': 'style="color: #d0d0d0;"',
                 'class="o"': 'style="color: #d0d0d0;"',
                 'class="s1"': 'style="color: #ed9d13;"',
                 'class="k"': 'style="color: #6ab825; font-weight: bold;"',
                 'class="nb"': 'style="color: #24909d;"',
                 'class="p"': 'style="color: #d0d0d0;"',
                 'class="si"': 'style="color: #ed9d13;"',
                 'class="mi"': 'style="color: #3677a9;"',
                 'class="ow"': 'style="color: #6ab825; font-weight: bold;"',
                 'class="se"': 'style="color: #ed9d13;"'}

    def highlightEvent(self, code):
        lines = code.split('\n')
        results = ''
        kw = set()

        for n in range(len(lines)):
            space_n = 0
            for w in lines[n]:
                if w != ' ': break
                space_n += 1

            highlight_line = highlight(lines[n], PythonLexer(), HtmlFormatter())
            new_line = re.findall('<span>.+', highlight_line)[0]
            new_line = re.sub('<span></span>', '<span>{}</span>'.format('&nbsp;' * space_n), new_line)

            for kc in self.kw_color:
                new_line = re.sub(kc, self.kw_color[kc], new_line)
            results += new_line

            if n != len(lines) - 1:
                results += '<br>\n'

            for w in re.findall('class="\w+">', new_line):
                kw.add(w)

        results = '<div style="overflow: auto; background: #202020; border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;">\n<pre style="margin: 0; line-height: 125%; white-space:nowrap">\n' + results + '</pre></div>'
        print(results)
        print('=' * 80)

        for w in kw:
            print(w)
