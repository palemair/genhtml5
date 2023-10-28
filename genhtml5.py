#!/usr/bin/python3
""" Static web site generator with lxml """

from lxml.html import fromstring, tostring, fragment_fromstring
from lxml import etree
from markdown import markdown
from pathlib import Path
from conteneur import Conteneur,Section,Article,Aside,Figure

class WebSite:
    """ Website object: it contains the logo, name of the project,
        directory where to put the files, the used language, the name of
        the css file,
        and the authors informations. """

    #globals
    firstpage='index'

    def __init__(self,name='Example', logofile='images/logo.svg',
                 cssfile='styles.css', language='fr'):

        self.name=name
        self.logofile= logofile
        self.md_dir= Path.cwd() / 'Markdown'
        self.cssfile=cssfile
        self.language=language
        self.pages={WebSite.firstpage:Page(self.name)}

    def get_home(self):

        return self.pages[WebSite.firstpage]

    def add_page(self, title):
        """Add a simple web page. """

        p = Page(title)
        self.pages[title] = p

        return p

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
        page.doc['html'].insert(0,head)

        #header of the page
        el=page.doc['pageheader']
        nav=etree.SubElement(el,'nav')
        nav.set('id','mainnav')
        home = etree.SubElement(nav,'a',href=f'{WebSite.firstpage}.html')
        logo = etree.parse(self.logofile)
        home.append(logo.getroot())
        
        ul=etree.SubElement(nav,'ul')

        for k,v in self.pages.items():
            if k != WebSite.firstpage:
                li=etree.SubElement(ul,'li')
                li.set('class','drop-down')
                a=etree.SubElement(li,'a',href=f'{k}.html',title=f'Aller à {k}')
                a.text=k
                element=v._link_list()
                element.set('class','under')
                li.append(element)

        #footer of the page
        elt=page.doc['pagefooter']
        infile=self.md_dir / 'footer.md'
        html=infile.read_text(encoding='UTF8')
        md=fragment_fromstring(markdown(html,extensions=['extra']),create_parent='div')
        elt.append(md)
  
    def write_to_file(self):

        for name,page in self.pages.items():
            self._builder_page(page)
            texte=tostring(page.doc['html'],
                           pretty_print=True,
                           doctype='<!DOCTYPE html>',
                           encoding='unicode')
            outfile=Path.cwd() / f'{name}.html'
            outfile.write_text(texte)

    def __str__(self):

        for page in self.pages:
            return str(self.pages)

class Page():

    """Simple html page object"""

    def __init__(self,title):

        self.title=title
        self.doc=self._builder()

    def _builder(self):

        root=etree.Element('html')
        body=etree.SubElement(root,'body',)
        header=etree.SubElement(body,'header')
        header.set('id','pageheader')
        main=etree.SubElement(body,'main')
        footer=etree.SubElement(body,'footer')
        footer.set('id','pagefooter')

        return {'html':root,
                'body':body,
                'main':main,
                'pageheader':header,
                'pagefooter':footer}

    def _link_list(self, elt : str = 'article', target :str = 'h2'):
        """create linked element list from an element """

        div = etree.Element('div')
        liste_elt = [ elt for elt in self.doc['main'].iterfind(f'.//{elt}') ]

        for elt in liste_elt:
                titre=[e for e in elt.iterfind(f'.//{target}')]
                lien= elt.get('id')
                a=etree.SubElement(div,'a',href=f'{self.title}.html#{lien}',title=f'Aller à {titre[0].text}')
                a.text=titre[0].text

        return div

    def add_conteneur(self,conteneur):

        if isinstance(conteneur,Conteneur):

            el=conteneur.root
            self.doc['main'].append(conteneur.root)

        else:
            print("Not a valid container !!")

    def __repr__(self):

        return str(tostring(self.doc['body'],
                      pretty_print=True,
                      doctype='<!DOCTYPE html>',
                      encoding='unicode'))

#---------------------------------------------------------------------
#program

if __name__ == '__main__' :

    site=WebSite(cssfile='styles.css')

    home=site.get_home()

    top=Aside({'id':'top'})
    top.add_md_content('Markdown/pageheader.md','div')
    home.add_conteneur(top)

    blog=site.add_page('Blog')
    concept=site.add_page('Concept')

    section1=Section()
    
    article1=Article()
    article1.add_md_content('Markdown/article1.md','a1')

    section1.add_conteneur(article1)

    section1.add_list_link_element('article')

    home.add_conteneur(section1)
    
    site.write_to_file()
