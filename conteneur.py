#!/usr/bin/python3

import pygal
from lxml.html import tostring, fragment_fromstring
from lxml import etree
from markdown import markdown
from pathlib import Path

class Conteneur(object):
    "HTML conteneur : section, article, aside...."
    
    def __init__(self,tag: str, attrib: dict = None):

        elt = etree.Element(tag)
        if attrib :
            for arg,value in attrib.items():
                elt.set(arg,value)
        self.root = elt

    def add_conteneur(self,*conteneurs):
        
        for conteneur in conteneurs:
            self.root.append(conteneur.root)

    def add_md_content(self,*inputfile: any, tag: str = None, tag_attr: str=None):
        
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
    
    def __init__(self,attrib: dict = None, caption:tuple= None, imgdatas: dict = None):

        super().__init__('figure',attrib)
        self.imgdatas = imgdatas
        self.caption = caption
        self.__initialize()

    def __initialize(self):
        
        if self.imgdatas is not None:
            elt=etree.Element('img')
            for k,v in self.imgdatas.items():
               elt .set(k,v)
            self.root.append(elt)
        
        if self.caption is not None:
            fc=etree.Element('figcaption')
            fc.set('class', self.caption[0])
            fc.text=self.caption[1]
            self.root.append(fc)
    

class Graphic(Figure):
    
    def __init__(self,att: dict = None, capt:tuple= None):

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
        
    def pie(self,data :dict):
        
        graph = pygal.Pie(self,self.conf,style=self.styl,disable_xml_declaration=True,no_prefix=True)
        for k,v in data.items():
            graph.add(k,v)
        self.root.append(graph.render_tree())
    
    def bar(self,*datas :dict, xlabels:list =None):
        
        legendcol =len(datas)
        graph = pygal.Bar(self.conf,style=self.styl,legend_at_bottom_columns=legendcol, xlabels=xlabels,disable_xml_declaration=True,no_prefix=True)

        for data in datas:
            for k,v in data.items():
                graph.add(k,v)
    
        self.root.append(graph.render_tree())
        
    
    def frmap(self,title:str='titre',*datas :dict):
        
        carte=pygal.maps.fr.Departments(self.conf,style=self.styl)
        for data in datas:
            carte.add(title,data)

        self.root.append(carte.render_tree())

#---------------------------------------------------------------------
#program

if __name__ == '__main__' :

    
    Y=Figure({'id':'test'},('photo','La plus belle'),{'class':'test-pic','src':'images/img_3.jpg','alt':'image de montagne'})
    
    graph1=Graphic({'id':'graph-1'},('graphic','test'))
    graph1.bar({'test':[23,24,45]})

    print(Y)

    print(graph1)
