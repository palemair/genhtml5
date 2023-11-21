#!/usr/bin/python3
""" Mixin used in Page and conteneur """

from lxml.html import fromstring, tostring, fragment_fromstring
from lxml import etree
from markdown import markdown
from pathlib import Path

class Mixconteneur:
    
    def add_mdcontent(self,*inputfile: any, tag: str = 'article', tag_attr: str=None):
        
	    if tag is not None :
	        balise=tag
	    else:
	        balise=False

	    for file in inputfile :
	        infile=Path(file)
	        contenu=infile.read_text(encoding='UTF8')
	        md=fragment_fromstring(markdown(contenu,extensions=['extra']),create_parent=balise)
	
	        if tag_attr is not None : 
	            html.set('id',tag_attr)
	        self.doc['main'].append(md)

    def add_conteneur(self,*conteneurs):

        for conteneur in conteneurs:

            el=conteneur.root
            self.root.append(conteneur.root)


    def _link_list(self, elt : str = 'article', target :str = 'h2'):
        """create linked element list from an element """

        div = etree.Element('div')
        liste_elt = [ elt for elt in self.doc['main'].iterfind(f'.//{elt}') ]
        
        for elt in liste_elt:
            titre= elt.find(f'.//{target}')
            if titre is not None :
                elt.set('id',titre.text)
                a=etree.SubElement(div,'a',href=f'{self.title}.html#{titre.text}',title=f'Aller à {titre.text}')
                a.text=titre.text

        return div

