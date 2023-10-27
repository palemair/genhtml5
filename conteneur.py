#!/usr/bin/python3

from lxml.html import tostring, fragment_fromstring
from lxml import etree
from markdown import markdown
from pathlib import Path

class Conteneur(object):
    "HTML conteneur : section, article, figure, aside...."
    counter = 0 #conteneur count

    def __init__(self,tag: str, attrib: dict = None):

        elt = etree.Element(tag)
        if attrib :
            for arg,value in attrib.items():
                elt.set(arg,value)
        self.root = elt
        Conteneur.counter += 1

    def add_conteneur(self,conteneur):
        
        self.root.append(conteneur.root)

    def add_md_content(self,inputfile: any, tag: str = None, tag_attr: str=None):
        
        infile=Path(inputfile)
        contenu=infile.read_text(encoding='UTF8')
        if tag is not None :
            balise=tag
        else:
            balise=False

        html=fragment_fromstring(markdown(contenu,extensions=['extra']),create_parent=balise)

        if tag_attr is not None : 
            html.set('id',tag_attr)
        self.root.append(html)
    
    def add_list_link_element(self, elt : str = 'section',target : str = 'h2',unordered : bool = False ) : 
        """create linked element list from a div(elt) """
        if unordered is False :
            typeliste = 'ol'
        else:
            typeliste = 'ul'

        table = etree.Element(typeliste)
        table.set('id','sous-menu')

        liste_elt = [ elt for elt in self.root.iterfind(f'.//{elt}') ]

        for elt in liste_elt:
                titre=[e for e in elt.iterfind(f'.//{target}')]
                lien= elt.get('id')
                li=etree.SubElement(table, 'li')
                a=etree.SubElement(li,'a',href=f'#{lien}',title=f'Aller à {titre[0].text}')
                a.text=titre[0].text
        self.root.insert(0,table)

    def __repr__(self):

        return str(tostring(self.root,encoding='unicode',pretty_print=True))

class Section(Conteneur):
    
    def __init__(self,attrib: dict = None):

        super().__init__('section',attrib)

class Article(Conteneur):
    
    def __init__(self,attrib: dict = None):

        super().__init__('article',attrib)

class Aside(Conteneur):
    
    def __init__(self,attrib: dict = None):

        super().__init__('aside',attrib)

class Figure(Conteneur):
    
    def __init__(self,attrib: dict = None):

        super().__init__('figure',attrib)

#---------------------------------------------------------------------
#program

if __name__ == '__main__' :

    y=Path.cwd()/ 'Markdown'

    A=Conteneur('div',{'id':'auto','class':'maybe'})
    A.add_md_content(y / 'article1.md','article','test')
    B=Section()
    A.add_list_link_element('article', unordered=True)
    print(A)

