from urllib.request import urlopen
from bs4 import BeautifulSoup

url = 'http://www.pythonscraping.com/pages/warandpeace.html'
html = urlopen(url)
bs = BeautifulSoup(html.read(), 'html.parser')

nombres = bs.find_all('span', {'class':'green'})
for nombre in nombres:
    print(nombre.get_text())


colores = bs.find_all('span', {'class':['green','red']})
for color in colores:
    print(color.get_text())

nombres = bs.find_all(string='The prince')
print(len(nombres))

# Las siguientes búsquedas coinciden:
nombres = bs.find(id='text')
print(len(nombres))

nombres = bs.find(attrs={'id':'text'})
print(len(nombres))

# Analicemos la búsqueda por navegación en árboles
url = 'http://www.pythonscraping.com/pages/page3.html'

"""
Si analizamos la página web podemos comprobar su estructura.
* HTML
    * body
        * div.wrapper
            * h1
            * div.content
            * table#giftlist
                * tr
                    * th
                    * th
                    * th
                    * th
                * tr.gift#gift1
                    * td
                    * td
                        * span.excitingNote
                    * td
                    * td
                        * img
            * .... continúa la tabla ....
        * div.footer
"""

# un hijo es una etiqueta inmediatamente abajo de la etiqueta padre --> children
# un descendiente puede estra varios niveles más abajo --> descendants

# veamos los hijos de la tabla (las filas)
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = 'http://www.pythonscraping.com/pages/page3.html'
html = urlopen(url)
bs = BeautifulSoup(html, 'html.parser')

for child in bs.find('table',{'id':'giftList'}).children:
    print(child)



# Comparemos con los descendientes de la tabla:
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = 'http://www.pythonscraping.com/pages/page3.html'
html = urlopen(url)
bs = BeautifulSoup(html, 'html.parser')

for descendant in bs.find('table',{'id':'giftList'}).descendants:
    print(descendant)

