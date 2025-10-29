#!./env/bin/python3

from abc import ABC, abstractmethod
from pathlib import Path
import pathlib

import xml.etree.ElementTree as et
from markdown import Markdown

class Container(ABC):
    
    "Abstract element container"
    
    def __init__(self,tag : str, **kwargs):

        self._root = et.Element(tag,**kwargs)

    def __repr__(self)-> str:
        
        et.indent(self._root)
        return str(et.tostring(self._root, encoding = 'unicode'))

    def append(self,*containers):
        
        for container in containers:
            if (not isinstance(container,Container)):
                raise TypeError("Need an xml.etree.element !!")
            match container._root.tag:
                case  'main' :
                    raise ValueError(f"You can only assign '{container._root.tag}' in a page")
            self._root.append(container._root)
        return self

#abstract class htmlcontainer
class HtmlSection(Container):
    
    "HTML conteneur : section, article, aside...."
    
    def add_from_markdown(self,input_content : any, parent : str = 'div', **kwargs):

        """Add element from a Markdown File or string """
        md = Markdown()
        elem = et.Element(parent)

        if(isinstance(input_content,pathlib.PosixPath)):
            if(input_content.exists()):
                s = input_content.read_text(encoding = 'utf-8')
            else:
                raise TypeError("file not exist")

        elif (isinstance(input_content,str)):
            s = input_content

        else:
            raise ValueError("You must provide str, Path !!")

        s = s.split(sep="\n")
        s = [md.convert(x) for x in s if x != '']
        elist = [et.fromstring(x) for x in s]

        for element in elist:
            elem.append(element)

        self._root.append(elem)

    def _link_list(self, elt : str = 'div', target : str = 'h2'):
        """create linked element list from an element """

        ul = et.Element('ul')
        liste_elt = ( elt for elt in self._root.iterfind(f'.//{elt}') )
        
        for elt in liste_elt:
            titre= elt.find(f'.//{target}')
            if titre is not None :
                elt.set('id',titre.text)
                li=et.SubElement(ul,'li')
                a=et.SubElement(li,'a',href=f'{self.title}.html#{titre.text}',title=f'Aller à {titre.text}')
                a.text=titre.text

        return ul

class HtmlText(Container):

    "HTML text container : p,h1,..."
    def __init__(self,tag : str,content : str = '', **kwargs):

        super().__init__(tag,**kwargs)
        self._root.text = content

    def set_text(self,input_text : str):

        self._root.text = input_text

#abstract class svgcontainer
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

    @staticmethod
    def html_section(tag : str, **kwargs) -> HtmlSection :

        match tag:
            case 'main':
                raise ValueError("You can only assign 'main' with a Page object !!")
            case _:
                return HtmlSection(tag, **kwargs)

    @staticmethod
    def html_text(tag : str, **kwargs) -> HtmlText :

        return HtmlText(tag, **kwargs)

    @staticmethod
    def svg_tag(tag : str, **kwargs) -> SvgContainer :

        match tag:
            case 'svg':
                raise ValueError("You can only assign 'svg' with a Svg object !!")
            case _:
                return SvgContainer(tag, **kwargs)


#Concrete html section 
class Page(HtmlSection):

    """Simple html page object"""
    def __init__(self,**kwargs):
        super().__init__('main',**kwargs)

class Section(HtmlSection):
    
    def __init__(self, **kwargs):
        super().__init__('section', **kwargs)

class Article(HtmlSection):
    
    def __init__(self, **kwargs):
        super().__init__('article', **kwargs)

#Concrete html text 
class Paragraph(HtmlText):
    
    def __init__(self,input_str : str = '', **kwargs):
        super().__init__('p',input_str,**kwargs)

class h1(HtmlText):
    
    def __init__(self,input_str : str = '', **kwargs):
        super().__init__('h1',input_str,**kwargs)

# class Img(HtmlContainer):

#     def __init__(self,imgdatas:dict = None,attrib: dict = {'class':'image'}) :

#         super().__init__(attrib,caption)
#         self.imgdatas = imgdatas
#         self.__initialize()
    
#     def __initialize(self):
        
#         if self.imgdatas is not None:
#             elt=etree.Element('img')
#             for k,v in self.imgdatas.items():
#                 elt.set(k,v )
#             self._root.insert(0,elt)

# class Figure(HtmlContainer):
    
#     def __init__(self,caption_class : str = None, caption_text : str = None, **kwargs):

#         super().__init__('figure', **kwargs)
        
#         if self.caption is not None:
#             fc=et.Element('figcaption')
#             fc.set('class', caption_class)
#             fc.text= caption_text

#         self.root.append(fc)

#Concrete Svg container 
class Svg(SvgContainer):

    "Svg : Element root of the drawing"

    def __init__(self, width : int = 1000, height : int = 1000, cssfile = ''):
        
        attrib_svg ={'version' : "1.1",
                     'baseProfile' : "full",
                     'xmlns' : "http://www.w3.org/2000/svg"                                                                                         
                     }

        super().__init__('svg', **attrib_svg)
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

        with file.open('w',encoding = 'utf-8') as f:
            f.write('<?xml version = "1.0" encoding="UTF-8">\n')
            f.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"\n "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n')
            f.write(f"{et.tostring(self._root,encoding = 'unicode')}")
        if (self._root.find('style') is not None):
            self._root.remove(style)

    def _close(self):
        
        self._root.set('width' , '100%')
        self._root.set('height' , '100%')
        self._root.set('viewBox', f"0 0 {self.width} {self.height}")

class Groupe(SvgContainer):

    def __init__(self, **kwargs):
        super().__init__('g', **kwargs)

class Defs(SvgContainer):

    def __init__(self, **kwargs):
        super().__init__('defs', **kwargs)

class Use(SvgContainer):

    def __init__(self, href : str, **kwargs):
        
        attrib = {"xlink:href" : f'#{href}'}
        attrib.update(kwargs)
        super().__init__('use', **attrib)

class Texte(HtmlText):

    """ Must be use in svg only"""
    def __init__(self, xpos : int, ypos : int , text : str, **kwargs):
        
        attrib = dict(x = str(xpos), y = str(ypos))
        attrib.update(kwargs)
        super().__init__('text', **attrib)
        self.set_text(text)

if __name__ == '__main__':

    home = Page()
    home.append(h1("title"))
    home.add_from_markdown("#Mardownprojet",'article')
    home.add_from_markdown(Path('Markdown/projet.md'))
    home.add_from_markdown(Path('Markdown/footer.md'))

    home.append(Paragraph("Un deuxieme"))

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

    dessin.to_svg_file('test.svg')
    
    home.append(dessin)
    print(home)

