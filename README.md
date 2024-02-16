# GENHTML5

Genhtml5 is a simple webpage generator. it depends a lot on LXML, Markdown (library), and Pygal for graphical uses.
The goal is to easily create an entire statique website.

## introduction

I know, there is many web app on python (django, flask) and even some html generator on github.
The main idea of this repo is to use lxml in an easier way and to be pedagogic.
it needs work to be achieved.

## How use it

only 2 files : genhtml5 and conteneur.

```python
from HTML.genhtml5 import WebSite, Page, Section, Article, Img, Graphic

site=WebSite('Example Project')
site.add_page('Page1','Page2')

home=site.get_page('index')

section1=Section()
section1.add_mdcontent('Markdown/article.md',tag='article')

graph = Graphic(('histogram','histo exemple'))
datas = ('values',[10,20,35,12,45,22])
graph.bar(datas)

section1.add_conteneur(graph)
home.add_conteneur(section1)

section2=Section()
section2.add_mdcontent('Markdown/article2.md',tag='article')

page1=site.get_page('Page1')
page1.add_conteneur(section2)

site.write_to_file()
```
![example] (genthtml5/screenshot.jpg "homepage")


with a bit of css, this is the result :


