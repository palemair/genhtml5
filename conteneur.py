#!/usr/bin/python3
""" Mixin used in Page and conteneur """

import pygal
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
	        self.root.append(md)

    def add_conteneur(self,*conteneurs):

        for conteneur in conteneurs:

            el=conteneur.root
            self.root.append(conteneur.root)


    def _link_list(self, elt : str = 'article', target :str = 'h2'):
        """create linked element list from an element """

        div = etree.Element('div')
        liste_elt = [ elt for elt in self.root.iterfind(f'.//{elt}') ]
        
        for elt in liste_elt:
            titre= elt.find(f'.//{target}')
            if titre is not None :
                elt.set('id',titre.text)
                a=etree.SubElement(div,'a',href=f'{self.title}.html#{titre.text}',title=f'Aller à {titre.text}')
                a.text=titre.text

        return div


class Conteneur(Mixconteneur):
    "HTML conteneur : section, article, aside...."
    __slots__=('root')
    
    def __init__(self,tag: str, attrib: dict = None):

        elt = etree.Element(tag)
        if attrib :
            for arg,value in attrib.items():
                elt.set(arg,value)
        self.root = elt

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
    
    def __init__(self,attrib: dict = None, caption:tuple= None):

        super().__init__('figure',attrib)
        self.caption = caption
        self.__initialize()

    def __initialize(self):
        
        if self.caption is not None:
            fc=etree.Element('figcaption')
            fc.set('class', self.caption[0])
            fc.text=self.caption[1]
            self.root.append(fc)
    
class Img(Figure):

    def __init__(self,caption:tuple= None,imgdatas:dict = None,attrib: dict = {'class':'image'}) :

        super().__init__(attrib,caption)
        self.imgdatas = imgdatas
        self.__initialize()
    
    def __initialize(self):
        
        if self.imgdatas is not None:
            elt=etree.Element('img')
            for k,v in self.imgdatas.items():
                elt.set(k,v )
            self.root.insert(0,elt)
        
class Graphic(Figure):
    
    def __init__(self,capt:tuple= None,att: dict = {'class':'graph'}):

        super().__init__(att,capt)
        self.conf = pygal.Config(
                      tooltip_border_radius=8,
                      tooltip_fancy_mode=False,
                      legend_at_bottom=True,
                      legend_box_size=20
                      )
        self.styl = pygal.style.DefaultStyle(
                      background ='transparent',
                      font_family ='arial,sans',
                      label_font_size = 16,
                      opacity_hover = 1, 
                      legend_font_size = 20,
                      major_label_font_size = 18,
                      guide_stroke_color = 'gray',
                      guide_stroke_dasharray = 3.1,
                      major_guide_stroke_color = 'gray',
                      major_guide_stroke_dasharray = 5.1
                      )
        
    def pie(self,*datas :tuple):
        
        graph = pygal.Pie(self,self.conf,style=self.styl,disable_xml_declaration=True,no_prefix=True)
        for data in datas:
            graph.add(*data)
        self.root.insert(0,graph.render_tree())
    
    def line(self,*datas :tuple, xlabels:list =None):
        
        graph = pygal.Line(self,self.conf,style=self.styl,disable_xml_declaration=True,no_prefix=True)
        for data in datas:
            graph.add(*data)
        self.root.insert(0,graph.render_tree())
    
    def bar(self,*datas :tuple, xlabels:list =None):
        
        legendcol =len(datas)
        graph = pygal.Bar(self.conf,style=self.styl,legend_at_bottom_columns=legendcol, xlabels=xlabels,disable_xml_declaration=True,no_prefix=True)

        for data in datas:
            graph.add(*data)
    
        self.root.insert(0,graph.render_tree())
        
    
    def frmap(self,title:str='titre',*datas :dict):
        
        carte=pygal.maps.fr.Departments(self.conf,style=self.styl)
        for data in datas:
            carte.add(title,data)

        self.root.insert(0,carte.render_tree())
