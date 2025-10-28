#!./env/bin/python3

import xml.etree.ElementTree as et
from pathlib import Path
from markdown import markdown

class Container():
    
    "Abstract XML container"
    
    def __init__(self,tag : str, title : str, **kwargs):

        self._root = et.Element(tag,**kwargs)
        self._title = title

    def __repr__(self)-> str:
        
        et.indent(self._root)
        return str(et.tostring(self._root, encoding = 'unicode'))

    def append(self,*containers):
        
        for container in containers:
            if (isinstance(container._root,et.Element)):
                self._root.append(container._root)
        return self

class HtmlContainer(Container):
    
    "HTML conteneur : section, article, aside...."
    
    def add_text(self,input_text : str):

        self._root.text = input_text
        
    def add_markdown(self,input_content : any, tag : str = 'div', **kwargs):
        
	    for file in inputfile :
	        infile=Path(file)
	        content=infile.read_text(encoding='UTF8')
	        md=fragment_fromstring(markdown(contenu,extensions=['extra']),create_parent=tag)
	
	        if tag_attr is not None : 
	            html.set('id',tag_attr)
	        self._root.append(md)

    def _link_list(self, elt : str = 'div', target : str = 'h2'):
        """create linked element list from an element """

        ul = et.Element('ul')
        liste_elt = ( elt for elt in self.root.iterfind(f'.//{elt}') )
        
        for elt in liste_elt:
            titre= elt.find(f'.//{target}')
            if titre is not None :
                elt.set('id',titre.text)
                li=et.SubElement(ul,'li')
                a=et.SubElement(li,'a',href=f'{self.title}.html#{titre.text}',title=f'Aller à {titre.text}')
                a.text=titre.text

        return ul

class SvgContainer(Container):

    "Svg generic container : Use, defs, animate...."
    
    def basicshape(self,forme : str, *args,**kwargs):
        
        coord = {}

        match forme:
            case "line":
                if(len(args) == 4):
                    param = ('x1','y1','x2','y2')
                    coord.update(dict(zip(param,[str(x) for x in args])))
                else:
                    raise SyntaxError('bad number of arguments')

            case "circle":
                if(len(args) == 3):
                    param = ('cx','cy','r')
                    coord.update(dict(zip(param,[str(x) for x in args])))
                else:
                    raise SyntaxError('bad number of arguments')

            case "ellipse":
                if(len(args) == 4):
                    param = ('cx','cy','rx','ry')
                    coord.update(dict(zip(param,[str(x) for x in args])))
                else:
                    raise SyntaxError('bad number of arguments')

            case "rect":
                if(len(args) >= 4):
                    param = ('x','y','width','height','rx','ry')
                    coord.update(dict(zip(param,[str(x) for x in args])))
                else:
                    raise SyntaxError('bad number of arguments')

            case "polyline":
                if(len(args) >= 1):
                    param = ('points')
                    coord[param] = ' '.join((f'{p[0]},{p[1]}' for p in args))
                else:
                    raise SyntaxError('bad number of arguments')

            case "polygon":
                if(len(args) >= 1):
                    param = ('points')
                    coord[param] = ' '.join((f'{p[0]},{p[1]}' for p in args))
                else:
                    raise SyntaxError('bad number of arguments')

            case _:
                raise SyntaxError ('Not a basic shape')

        coord.update(kwargs)
        self._root.append(et.Element(forme,coord))
        
        return self

class ContainerFactory:

    def html_tag(tag : str, title = '',**kwargs) -> HtmlContainer :
        return HtmlContainer(tag, title, **kwargs)

    def svg_tag(tag : str, title = '',**kwargs) -> SvgContainer :
        return SvgContainer(tag, title, **kwargs)

#Concrete html container 
class Page(HtmlContainer):

    """Simple html page object"""
    def __init__(self,title : str = 'Lorem Ipsum',**kwargs):
        super().__init__('main',title,**kwargs)

class Section(HtmlContainer):
    
    def __init__(self,title :str = '',**kwargs):
        super().__init__('section',title, **kwargs)

class Article(HtmlContainer):
    
    def __init__(self,title :str = '',**kwargs):
        super().__init__('article',title, **kwargs)

class Paragraph(HtmlContainer):
    
    def __init__(self,input_str : str = '',title : str = '',**kwargs):
        super().__init__('p',title,**kwargs)
        self.add_text(input_str)

class Img(HtmlContainer):

    def __init__(self,imgdatas:dict = None,attrib: dict = {'class':'image'}) :

        super().__init__(attrib,caption)
        self.imgdatas = imgdatas
        self.__initialize()
    
    def __initialize(self):
        
        if self.imgdatas is not None:
            elt=etree.Element('img')
            for k,v in self.imgdatas.items():
                elt.set(k,v )
            self._root.insert(0,elt)

class Figure(HtmlContainer):
    
    def __init__(self,caption_class : str = None, caption_text : str = None, **kwargs):

        super().__init__('figure', **kwargs)
        
        if self.caption is not None:
            fc=et.Element('figcaption')
            fc.set('class', caption_class)
            fc.text= caption_text

        self.root.append(fc)

#Concrete Svg container 
class Svg(SvgContainer):

    "Svg : Element root of the drawing"

    def __init__(self, width : int = 1000, height : int = 1000,title : str = '',cssfile = ''):
        
        attrib_svg ={'version' : "1.1",
                     'baseProfile' : "full",
                     'xmlns' : "http://www.w3.org/2000/svg"                                                                                         
                     }

        super().__init__('svg', title, **attrib_svg)
        self.width = width
        self.height = height
        self.css = Path(cssfile)

    def to_svg_file(self,dest_file : str):
        
        self._root.set('width' , f"{self.width}")
        self._root.set('height' , f"{self.height}")

        if (self.css.is_file()):
            style = et.Element('style',{"type":"text/css"})
            style.text = self.css.read_text('utf-8')
            self._root.insert(0,style)

        et.indent(self._root)

        file = Path.home() / 'Bureau' / dest_file
        file = file.with_suffix('.svg')

        with file.open('w') as f:
            f.write('<?xml version = "1.0" encoding="UTF-8">\n')
            f.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"\n "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n')
            f.write(f"{et.tostring(self._root,encoding = 'unicode')}")
        if (self._root.find('style') is not None):
            self._root.remove(style)

    def _close(self):
        
        self.root.set('width' , '100%')
        self.root.set('height' , '100%')
        self.root.set('viewBox', f"0 0 {self.width} {self.height}")

class Groupe(SvgContainer):

    def __init__(self,title : str = '', **kwargs):
        super().__init__('g',title, **kwargs)

class Defs(SvgContainer):

    def __init__(self,title : str = '', **kwargs):
        super().__init__('defs', title, **kwargs)

class Use(SvgContainer):

    def __init__(self, href : str,title : str = '',**kwargs):
        
        attrib = {"xlink:href" : f'#{href}'}
        attrib.update(kwargs)
        super().__init__('use', title, **attrib)

class Texte(SvgContainer):

    def __init__(self, xpos : int, ypos : int , texte : str,title : str = '', **kwargs):
        
        attrib = dict(x = str(xpos), y = str(ypos))
        attrib.update(kwargs)
        super().__init__('text', title, **attrib)
        self._root.text = texte

if __name__ == '__main__':

    fabrik = ContainerFactory()

    r = fabrik.svg_tag('rect')
    p=Paragraph()
    p.add_text("Le premier paragraphe !!")
    home = Page()
    home.append(p)
    home.append(Paragraph("Un deuxieme"))

    print(home)

    dessin = Svg()
    linestyle = {'stroke' : 'blue', 'stroke-width' : '2px', 'fill' : 'gray'}
    groupe1 = Groupe(**linestyle)

    groupe1.basicshape('line',300,200,456,234)
    groupe1.basicshape('circle',300,200,45)

    dessin.append(groupe1)

    dessin.append(Texte(200,300,"test"))

    dessin.basicshape('ellipse',600,500,45,70, stroke = 'red',fill = 'green')
    dessin.basicshape('rect',300,700,300,150,**linestyle)

    dessin.append(Use("stric", transform="translate(200,150) scale(3) rotate(17)"))

    print(dessin)
    dessin.to_svg_file('test.svg')
    
    home.append(dessin)
    print(home)

