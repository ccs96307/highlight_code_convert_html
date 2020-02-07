import re
from pygments import highlight
from pygments.lexers.python import PythonLexer
from pygments.formatters.html import HtmlFormatter


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

for line in lines:
    space_n = 0
    for w in line:
        if w != ' ': break
        space_n += 1

    highlight_line = highlight(line, PythonLexer(), HtmlFormatter())
    print(line)
    print(highlight_line)
    print('='*80)
    new_line = re.findall('<span>.+', highlight_line)[0]
    new_line = re.sub('<span></span>', '<span>{}</span>'.format('&nbsp;'*space_n), new_line)
    results += new_line
    results += '<br>\n'

results = '<div style="overflow: auto">\n<pre style="margin: 0; line-height: 125%; white-space:nowrap">\n' + results + '</pre></div>'
print(results)
