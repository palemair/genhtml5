# GENHTML5

Genhtml5 is a simple webpage generator. it depends a lot on LXML, Markdown (library), and Pygal for graphical uses.
The goal is to easily create an entire statique website.

## introduction

I know, there is many web app on python (django, flask) and even some html generator on github.
The main idea of this repo is to use lxml in an easier way and to be pedagogic.
it needs work to be achieved.

## How use it

only 2 files : genhtml5 and conteneur.

```
#!/usr/bin/python3

from HTML.genhtml5 import WebSite, Page, Section, Article, Img, Graphic

site=WebSite('Example Project') #the entire website
site.add_page('Page1','Page2')  #  add 2 pages

home=site.get_page('index') #the first page

section1=Section()

section1.add_mdcontent('Markdown/projet.md',tag='article') #add markdown content

home.add_conteneur(section1)

section2=Section()
section2.add_mdcontent('Markdown/article2.md',tag='article')

page1=site.get_page('Page1')

page1.add_conteneur(section2)

site.write_to_file() #create all pages
```
