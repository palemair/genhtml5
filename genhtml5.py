#!/usr/bin/python3
""" Static web site generator with lxml """

from lxml.html import fromstring, tostring, fragment_fromstring
from lxml import etree
from markdown import markdown
from pathlib import Path
from HTML.conteneur import Conteneur,Section,Article,Aside,Graphic,Img

class WebSite:
    """ Website object: it contains the logo, name of the project,
        directory where to put the files, the used language, the name of
        the css file, and the authors informations. """

    #globals
    firstpage='index'

    def __init__(self,name='LOREM IPSUM',h1='gros titre',logofile=None,
                 cssfile='styles.css', language='fr'):
        self.name=name
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
         
    def _builder_page(self,page):

        #head of the page
        head = etree.Element('head')
        etree.SubElement(head,'meta',charset='utf-8')
        headtitle=etree.SubElement(head,'title')
        headtitle.text = page.title
        etree.SubElement(head,'link',
                        {'rel':'stylesheet',
                         'href':self.cssfile,
                         'type':'text/css'})
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
        html=infile.read_text(encoding='UTF8')
        md=fragment_fromstring(markdown(html,extensions=['extra']),create_parent='div')
        elt.append(md)
    
    @staticmethod 
    def draw_logo(hauteur:int,name:str):
            
        logo=etree.Element("svg",width='300',height=str(hauteur),xmlns="http://www.w3.org/2000/svg")
        etree.SubElement(logo,"circle",cx="16",cy="14",r="13",fill="navy")
        x,y=5,14
        string=f'{x} {y},{x+5} {y-5},{x+10} {y},{x+5} {y+5}' 
        etree.SubElement(logo,"polyline",points=string,fill="ghostwhite")
        x,y=17,14
        string=f'{x} {y},{x+5} {y-5},{x+10} {y},{x+5} {y+5}' 
        etree.SubElement(logo,"polyline",points=string,fill="ghostwhite")
        x,y=11,8
        string=f'{x} {y},{x+5} {y-5},{x+10} {y},{x+5} {y+5}' 
        etree.SubElement(logo,"polyline",points=string,fill="ghostwhite")
        x,y=11,20
        string=f'{x} {y},{x+5} {y-5},{x+10} {y},{x+5} {y+5}' 
        etree.SubElement(logo,"polyline",points=string,fill="ghostwhite")

        return logo

    def write_to_file(self):

        for name,page in self.pages.items():
            self._builder_page(page)
            texte=tostring(page.doc,
                           pretty_print=True,
                           doctype='<!DOCTYPE html>',
                           encoding='unicode')
            outfile=Path.cwd() / f'{name}.html'
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
