"""
Test data for the enabled mistune plugins. Adapted from:
https://github.com/lepture/mistune/blob/master/docs/plugins.rst
"""

abbr = (
    """The HTML specification
is maintained by the W3C.

*[HTML]: Hyper Text Markup Language
*[W3C]: World Wide Web Consortium""",
    """<p>The <abbr title="Hyper Text Markup Language">HTML</abbr> specification
is maintained by the <abbr title="World Wide Web Consortium">W3C</abbr>.</p>
"""
)

def_list = (
    """First term
: First definition
: Second definition

Second term
: Third definition""",
    """<dl>
<dt>First term</dt>
<dd>First definition</dd>
<dd>Second definition</dd>
<dt>Second term</dt>
<dd>Third definition</dd>
</dl>
"""
)

footnote = (
    "content in paragraph with footnote[^1] markup.\n\n[^1]: footnote explain",
    """<p>content in paragraph with footnote<sup class="footnote-ref" id="fnref-1"><a href="#fn-1">1</a></sup> markup.</p>
<section class="footnotes">
<ol>
<li id="fn-1"><p>footnote explain<a href="#fnref-1" class="footnote">&#8617;</a></p></li>
</ol>
</section>
"""
)

insert = (
    "^^insert me^^ ^^insert\^\^me^^", "<ins>insert me</ins> <ins>insert^^me</ins>"
)

mark = (
    "==mark me== ==mark with\=\=equal==",
    "<mark>mark me</mark> <mark>mark with==equal</mark>"
)

math = (
    "$$\n\operatorname{ker} f=\{g\in G:f(g)=e_{H}\}{\mbox{.}}\n$$",
    "<div class=\"math\">$$\n\operatorname{ker} f=\{g\in G:f(g)=e_{H}\}{\mbox{.}}\n$$</div>"
)

spoiler = (
    # ">! here is the spoiler content\n>!\n>! it will be hidden",
    """>! here is the spoiler content
>!
>! it will be hidden""",
"<div class=\"spoiler\"n<p>here is the spoiler content</p>\n<p>it will be hidden</p>\n</div>"
)

subscript = (
    "Hello~subscript~\n\nCH~3~CH~2~OH",
    "<p>Hello<sub>subscript</sub></p>\n<p>CH<sub>3</sub>CH<sub>2</sub>OH</p>"
)

superscript = "Hello^superscript^", "<p>Hello<sup>superscript</sup></p>"

table = (
    """First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell""",
    """<table>
<thead>
<tr>
  <th>First Header</th>
  <th>Second Header</th>
</tr>
</thead>
<tbody>
<tr>
  <td>Content Cell</td>
  <td>Content Cell</td>
</tr>
<tr>
  <td>Content Cell</td>
  <td>Content Cell</td>
</tr>
</tbody>
</table>
"""
)

task_list = (
    """- [x] item 1
- [ ] item 2""",
    """<ul>
<li class="task-list-item"><input class="task-list-item-checkbox" type="checkbox" disabled checked/>item 1</li>
<li class="task-list-item"><input class="task-list-item-checkbox" type="checkbox" disabled/>item 2</li>
</ul>
"""
)
