from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

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

lexer = get_lexer_by_name("python", stripall=True)
formatter = HtmlFormatter(linenos=True, cssclass="source")
result = highlight(code, lexer, formatter)
print(result)