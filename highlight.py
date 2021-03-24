# coding: utf-8
import random
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

        highlight_code = re.sub('<pre><span></span>', '<pre class="ccode" style="margin: 0; line-height: 125%; font-size:15px;"><span></span>', highlight_code)

        print(highlight_code)

        results = \
            '<!-- More information can refer: https://clay-atlas.com/blog/2020/03/05/python-english-tutorial-package-pygments-highlight-code/ -->' \
            '\n<div style="background: {}; ' \
            'overflow:auto; width:auto; border:solid gray; ' \
            'border-width:.1em .1em .1em .8em; ' \
            'padding:.2em .5em;">\n    '.format(background_color) + highlight_code

        # Add button
        if show_copy_button:
            # Random ID
            random_id = "".join([str(random.randint(0, 9)) for _ in range(8)])

            results += """
<textarea readonly id="{}" style="position:absolute;left:-9999px">""".format(random_id) +\
        code +\
        """</textarea>
    <button type="button" onclick="copyEvent('""" + random_id + """')" style="float: right">COPY</button>

<script>
function copyEvent(id) {
  let textarea;
  let result;

  try {
    textarea = document.createElement('textarea');
    textarea.setAttribute('readonly', true);
    textarea.setAttribute('contenteditable', true);
    textarea.style.position = 'fixed'; // prevent scroll from jumping to the bottom when focus is set.
    textarea.value = document.getElementById(id).textContent;

    document.body.appendChild(textarea);

    textarea.focus();
    textarea.select();

    const range = document.createRange();
    range.selectNodeContents(textarea);

    const sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);

    textarea.setSelectionRange(0, textarea.value.length);
    result = document.execCommand('copy');
  } catch (err) {
    console.error(err);
    result = null;
  } finally {
    document.body.removeChild(textarea);
  }

  // manual copy fallback using prompt
  if (!result) {
    const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
    const copyHotkey = isMac ? '⌘C' : 'CTRL+C';
    result = prompt(`Press ${copyHotkey}`, string); // eslint-disable-line no-alert
    if (!result) {
      return false;
    }
  }
  return true;
}
</script>"""

        return results


if __name__ == '__main__':
    code = 'while (i <= 100) { i++; }'
    lang = 'C++'
    style = 'default'
    hl = Highlight()

    results = hl.highlightEvent(code, style, lang, True)
    open('test.html', 'w').write(results)
