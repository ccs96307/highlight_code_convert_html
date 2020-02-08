# -*- coding: utf-8 -*-
"""
A simple test for pygments
"""
import re
from pygments import highlight
from pygments.lexers.python import PythonLexer
from pygments.formatters.html import HtmlFormatter


# Settings
keyword_color = {'class="kn"': 'style="color: #6ab825; font-weight: bold;"',
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

code = \
r'''from gensim.corpora import WikiCorpus

wiki_corpus = WikiCorpus('zhwiki-20200101-pages-articles-multistream.xml.bz2', dictionary={})
text_num = 0

with open('wiki_text.txt', 'w', encoding='utf-8') as f:
     for text in wiki_corpus.get_texts():
         f.write(' '.join(text)+'\n')
         text_num += 1
         if text_num % 10000 == 0:
             print('{} articles processed.'.format(text_num))

     print('{} articles processed.'.format(text_num))
'''

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
    new_line = re.sub('<span></span>', '<span>{}</span>'.format('&nbsp;'*space_n), new_line)

    for kc in keyword_color:
        new_line = re.sub(kc, keyword_color[kc], new_line)
    results += new_line

    if n != len(lines)-1:
        results += '<br>\n'

    for w in re.findall('class="\w+">', new_line):
        kw.add(w)

results = '<div style="overflow: auto; background: #202020; border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;">\n<pre style="margin: 0; line-height: 125%; white-space:nowrap">\n' + results + '</pre></div>'
print(results)
print('='*80)

for w in kw:
    print(w)