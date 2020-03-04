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
        ls = '''ABAP
APL
ABNF
ActionScript
Ada
ADL
Agda
Aheui
Alloy
AmbientTalk
Ampl
ANTLR
ApacheConf
AppleScript
Arduino
AspectJ
Asymptote
Augeas
AutoIt
autohotkey
Awk
BBCode
BC
BST
Bash
Befunge
BibTeX
BlitzBasic
BlitzMax
BNF
Boa
Boo
Boogie
Brainfuck
BUGS
CAmkES
C
CMake
c-objdump
CPSA
aspx-cs
C#
cADL
CapDL
Ceylon
CFEngine3
ChaiScript
Chapel
Charmci
HTML+Cheetah
JavaScript+Cheetah
Cheetah
XML+Cheetah
Cirru
Clay
Clean
Clojure
ClojureScript
COBOLFree
COBOL
CoffeeScript
Coq
C++
cpp-objdump
Crmsh
Croc
Cryptol
Crystal
CSS+Ruby
CSS
CSS+PHP
CSS+Smarty
CUDA
Cypher
Cython
D
d-objdump
Dart
DASM16
Delphi
dg
Diff
Docker
DTD
Duel
Dylan
ECL
eC
Easytrieve
EBNF
Eiffel
Elixir
Elm
ERB
Erlang
HTML+Evoque
Evoque
XML+Evoque
Ezhil
F#
Factor
Fancy
Felix
Fennel
Fish
Flatline
FloScript
Forth
FortranFixed
Fortran
FoxPro
Freefem
GAP
GLSL
GAS
Genshi
Gherkin
Gnuplot
Go
Golo
GoodData-CL
Gosu
Groff
Groovy
HLSL
Haml
HTML+Handlebars
Handlebars
Haskell
Haxe
Hexdump
HSAIL
Hspec
HTML+Genshi
HTML
HTML+PHP
HTML+Smarty
HTTP
Hxml
Hy
Hybris
IDL
Icon
Idris
Igor
INI
Io
Ioke
Isabelle
J
JAGS
Jasmin
Java
JavaScript+Ruby
JavaScript
JavaScript+PHP
JavaScript+Smarty
JCL
JSGF
JSON-LD
JSON
Julia
Juttle
Kal
Kconfig
Koka
Kotlin
LSL
CSS+Lasso
HTML+Lasso
JavaScript+Lasso
Lasso
XML+Lasso
Lean
Limbo
liquid
LiveScript
LLVM
Logos
Logtalk
Lua
MIME
MOOCode
Makefile
CSS+Mako
HTML+Mako
JavaScript+Mako
Mako
XML+Mako
MAQL
Mask
Mason
Mathematica
Matlab
MiniD
Modelica
Monkey
Monte
MoonScript
CSS+mozpreproc
mozhashpreproc
Javascript+mozpreproc
mozpercentpreproc
XUL+mozpreproc
MQL
Mscgen
MuPAD
MXML
MySQL
CSS+Myghty
HTML+Myghty
JavaScript+Myghty
Myghty
XML+Myghty
NCL
NSIS
NASM
objdump-nasm
Nemerle
nesC
NewLisp
Newspeak
Nimrod
Nit
Nix
Notmuch
NuSMV
NumPy
objdump
Objective-C
Objective-C++
Objective-J
OCaml
Octave
ODIN
Ooc
Opa
PacmanConf
Pan
ParaSail
Pawn
Perl6
Perl
PHP
Pig
Pike
PkgConfig
Pony
PostScript
PowerShell
Praat
Prolog
Properties
Pug
Puppet
Python
QBasic
QVTO
QML
RConsole
Racket
Ragel
Rd
REBOL
Red
Redcode
ResourceBundle
Rexx
RHTML
RobotFramework
RQL
RSL
reStructuredText
TrafficScript
Ruby
Rust
SAS
S
SARL
Sass
Scala
Scaml
scdoc
Scheme
Scilab
SCSS
ShExC
Shen
Silver
Slash
Slim
Slurm
Smali
Smalltalk
Smarty
Snobol
Snowball
Solidity
SPARQL
SQL
SquidConf
Stan
Stata
SuperCollider
Swift
SWIG
systemverilog
TAP
TOML
TASM
Tcl
Tcsh
Tea
Termcap
Terminfo
Terraform
TeX
Thrift
Todotxt
Treetop
Turtle
HTML+Twig
Twig
TypeScript
TypoScriptCssData
TypoScriptHtmlData
TypoScript
ucode
Unicon
UrbiScript
VBScript
VCL
VCLSnippets
VCTreeStatus
VGL
Vala
aspx-vb
VB.net
HTML+Velocity
Velocity
XML+Velocity
verilog
vhdl
WDiff
Whiley
X10
XQuery
XML+Ruby
XML
XML+PHP
XML+Smarty
XSLT
Xtend
YAML+Jinja
YAML
Zeek
Zephir
Zig'''
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
        results = ''
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
            print(new_line)

            for kc in kw_color:
                new_line = re.sub(kc, kw_color[kc], new_line)
            results += new_line

            if n != len(lines) - 1:
                results += '<br>\n'

            for w in re.findall('class="\w+">', new_line):
                kw.add(w)

        # Finished
        results = '<div style="overflow: auto;' \
                  ' background: {};' \
                  ' border:solid gray;' \
                  'border-width:.1em .1em .1em .8em;' \
                  'padding:.2em .6em;">\n' \
                  '<pre style="margin: 0; line-height: 125%;' \
                  ' white-space:nowrap">\n'.format(background) + results + '</pre></div>'

        print(results)

        return results
