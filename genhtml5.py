#!./env/bin/python3
""" Static web site generator with lxml """

from lxml.html import fromstring, tostring, fragment_fromstring
from lxml import etree
from markdown import markdown
from pathlib import Path
from conteneur import Conteneur,Svg,Section,Article,Aside,Graphic,Img

class WebSite:
    """ Website object: it contains the logo, name of the project,
        directory where to put the files, the used language, the name of
        the css file, and the authors informations. """

    #globals
    firstpage='index'

    def __init__(self,name='LOREM IPSUM',h1='gros titre',logofile=None,
                 cssfile='styles.css', language='fr'):
        self.name=name
        self.outdir = Path.cwd().parent
        self.h1=h1
        self.logofile= logofile
        self.md_dir= Path.cwd() / 'Markdown'
        self.cssfile=cssfile
        self.language=language
        self.pages={WebSite.firstpage:Page(self.name)}

    def get_page(self,name:str):
        return self.pages[name]

    def add_page(self, *titles:str):
        """Add a new web page. """
        
        for t in titles:
            if isinstance(t,Page):
                self.pages[t.title]=t
            else:
                self.pages[t] = Page(t)
        return self
         
    def _builder_page(self,page):

        #head of the page
        head = etree.Element('head')
        etree.SubElement(head,'meta',charset='utf-8')
        headtitle=etree.SubElement(head,'title')
        headtitle.text = page.title
        style = etree.SubElement(head,'style')
        infile = Path(self.cssfile)
        if infile.is_file():
            style.text = infile.read_text('utf-8')
        page.doc.insert(0,head)

        #header of the page
        el=page.header
        nav=etree.SubElement(el,'nav')
        ul=etree.SubElement(nav,'ul')
        homeli = etree.SubElement(ul,'li')
        lia=etree.SubElement(homeli,'a',href=f'{WebSite.firstpage}.html',title='Accueil')
        lia.text=self.name

        for k,v in self.pages.items():
            if k != WebSite.firstpage:
                li=etree.SubElement(ul,'li')
                a=etree.SubElement(li,'a',href=f'{k}.html',title=f'Aller à {k}')
                a.text=k
                element=v._link_list()
                li.append(element)

        #footer of the page
        elt=page.footer
        infile=self.md_dir / 'footer.md'
        foot=infile.read_text(encoding='UTF8')
        md=fragment_fromstring(markdown(foot,extensions=['extra']),create_parent='div')
        elt.append(md)
    
    def write_to_file(self):

        for name,page in self.pages.items():
            self._builder_page(page)
            texte=tostring(page.doc,
                           pretty_print=True,
                           doctype='<!DOCTYPE html>',
                           encoding='unicode')
            outfile=self.outdir / f'{name}.html'
            outfile.write_text(texte)

    def __repr__(self):

        return str(self.__dict__)

class Page(Conteneur):

    """Simple html page object"""

    def __init__(self,title):

        self.title=title
        self.doc,self.header,self.main,self.footer=self._builder()
        self.root=self.main

    def _builder(self):

        html=etree.Element('html')
        body=etree.SubElement(html,'body',)
        header=etree.SubElement(body,'header')
        main=etree.SubElement(body,'main')
        footer=etree.SubElement(body,'footer')

        return html,header,main,footer

    def __str__(self):

        return str(tostring(self.doc['body'],
                      pretty_print=True,
                      doctype='<!DOCTYPE html>',
                      encoding='unicode'))
