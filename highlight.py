# coding: utf-8
import re
from pygments import highlight, lexers, styles
from pygments.formatters.html import HtmlFormatter


class Highlight:
    def __init__(self):
        self.all_langs = {lexer[0]: lexer[1][0] for lexer in lexers.get_all_lexers()}
        self.all_styles = [style for style in styles.get_all_styles()]

    def return_all_languages(self):
        return [lang for lang in self.all_langs]

    def return_all_styles(self):
        return self.all_styles

    def highlightEvent(self, code, style, lang, show_copy_button):
        # Build the style and lexer object
        lang = self.all_langs[lang]
        style = styles.get_style_by_name(style)
        lexer = lexers.get_lexer_by_name(lang)
        formatter = HtmlFormatter(full=True, style=style)

        # Highlight the code
        results = highlight(code, lexer, formatter)

        print(results)

        # Finished
        class_style = re.findall('body \.(.*) { (.+) }', results)
        highlight_code = re.findall('<div class="highlight">(<pre>.*</pre></div>)', results, re.DOTALL)[0]
        background_color = re.findall('body \{ background: (.+); \}', results)

        if background_color:
            background_color = background_color[0]
        else:
            background_color = "#f8f8f8"

        for item in class_style:
            class_pattern = '<span class="{}"'.format(item[0])
            color_pattern = '<span style="{}"'.format(item[1])
            highlight_code = highlight_code.replace(class_pattern, color_pattern)

        highlight_code = re.sub('<pre><span></span>', '<pre style="margin: 0; line-height: 125%; font-size:15px;"><span></span>', highlight_code)

        results = \
            '<!-- More information can refer: https://clay-atlas.com/blog/2020/03/05/python-english-tutorial-package-pygments-highlight-code/ -->' \
            '\n<div style="background: {}; ' \
            'overflow:auto; width:auto; border:solid gray; ' \
            'border-width:.1em .1em .1em .8em; ' \
            'padding:.2em .5em;">\n    '.format(background_color) + highlight_code

        # Add button
        if show_copy_button:
            results += """
<textarea readonly id="copyText" style="position:absolute;left:-9999px">""" +\
        code +\
        """</textarea>
    <button type="button" onclick="copyEvent('copyText')" style="float: right">COPY</button>

<script>
    function copyEvent(id)
    {
        var str = document.getElementById(id);
        window.getSelection().selectAllChildren(str);
        document.execCommand("Copy")
    }
</script>"""

        return results


if __name__ == '__main__':
    code = 'while (i <= 100) { i++; }'
    lang = 'C++'
    style = 'default'
    hl = Highlight()

    results = hl.highlightEvent(code, style, lang, False)
    open('test.html', 'w').write(results)
