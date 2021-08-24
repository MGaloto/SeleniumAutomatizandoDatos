# 1. Importar librerias

from bs4 import BeautifulSoup as BS
from selenium import webdriver
from time import sleep
import requests
import csv

# 2. Ejecutar URL

options = webdriver.ChromeOptions()
options.add_argument("--incognito")
driver = webdriver.Chrome('C:/Users/54116/Downloads/chromedriver_win32/chromedriver.exe', options = options)
url = 'https://www.carrefour.com.ar/Bebidas/Cervezas'
driver.get(url)

# 3. Darle tiempo a la pagina (sleep)

sleep(20)

# 4. Crear el script para recorrer la pagina

script_scroll_js = """
    fondoDePantalla = document.body.scrollHeight
    for (let i = 0; i < fondoDePantalla; i += 50){
          setInterval(function(){window.scrollTo(0, i)}, 1000);
          }
"""

# 4. Crear el script para CLICK

script_boton = '''
            let boton = document.querySelector('[class="vtex-button bw1 ba fw5 v-mid relative pa0 lh-solid br2 min-h-small t-action--small bg-action-primary b--action-primary c-on-action-primary hover-bg-action-primary hover-b--action-primary hover-c-on-action-primary pointer "]')
    if (boton){
          boton.click()
      }
    else {
        return "False"}'''
    
# 5. Ejecutar el while

driver.execute_script(script_scroll_js)

sleep(10)

while driver.execute_script(script_boton) != "False":
    sleep(10)
    driver.execute_script(script_scroll_js)
    sleep(10)
print('fin')


html_primero = driver.execute_script('return document.documentElement.outerHTML')

dom_primero = BS(html_primero, 'html.parser')

cervezas = dom_primero.find_all(class_='vtex-product-summary-2-x-container vtex-product-summary-2-x-container--contentProduct vtex-product-summary-2-x-containerNormal vtex-product-summary-2-x-containerNormal--contentProduct overflow-hidden br3 h-100 w-100 flex flex-column justify-between center tc')


# Creamos una tabla

tabla = [['Id','Descripcion','Marca', 'Precio Publicado', 'CC', 'Promociones', 'Precio Por Litro', 'Observaciones', 'Total Pack', 'Precio por Lata']]

# Creamos una lista de str para separar los packs

separar_pack = ['6','10','12','16','18']

# 6. Ejecutar el for

conteo = 0
for cerveza in cervezas:
    link = cerveza.a['href']
    url_final = 'https://www.carrefour.com.ar' + link
    driver.get(url_final)
    sleep(2)
    html = driver.execute_script('return document.documentElement.outerHTML')
    dom = BS(html,'html.parser')
    marca = dom.find(class_="vtex-store-components-3-x-productBrandName").text
    descripcion = dom.find(class_="vtex-store-components-3-x-productNameContainer vtex-store-components-3-x-productNameContainer--quickview mv0 t-heading-4").text
    observaciones = "El precio es por Lata"
    for i in descripcion.split():
       if i in separar_pack:
          observaciones = "El precio es por Pack"
    precio = dom.find(class_="lyracons-carrefourarg-product-price-1-x-currencyInteger").text
    if precio == '':
        precio = 1
    decimales = dom.find(class_="lyracons-carrefourarg-product-price-1-x-currencyFraction").text
    precio_publicado = round(float(precio + '.' + decimales),2)
    promociones = dom.find(attrs = {'data-highlight-id':"101"}).text
    if promociones == '':
        promociones = "No tiene promociones"
    cc_total = []
    cc = descripcion.split()
    pack = 'No tiene Pack'
    for i in cc:
       if i in separar_pack:
          pack = i
    if 'cc.' in cc:
        cc_total = float(cc[cc.index('cc.') - 1])
    elif 'l.' in cc:
        cc_total = float(cc[cc.index('l.') - 1]) * 1000
    else:
        print('No hay ni cc. ni l.')
        break
    precio_x_litro = round((( 1000 / cc_total) * precio_publicado),2)
    precio_publicado = '$ ' + str(precio_publicado)
    precio_por_lata = precio_publicado
    if pack in cc:
        precio_por_lata = '$ ' + str(round((round(float(precio + '.' + decimales),2) / int(pack)),2)) 
    precio_x_litro = '$ ' + str(precio_x_litro) 
    conteo = conteo + 1
    faltan = len(cervezas) - conteo
    variables = [conteo, descripcion, marca, precio_publicado, cc_total, promociones, precio_x_litro, observaciones, pack, precio_por_lata]
    tabla.append(variables)
    print('Fila: ',conteo,'\n\n', 'Descripcion: ', descripcion, '\n','Marca: ',marca , '\n','Precio: ', precio_publicado,'\n', 'CC: ',cc_total,'\n','Promociones: ', promociones, '\n','Precio por Litro: ',precio_x_litro, '\n','Observaciones: ', observaciones,'\n' ,'Pack Unidades: ',pack,'\n', 'Precio por Lata: ',precio_por_lata, '\n\n', 'Restantes: ' + str(faltan) + ' lineas\n\n')

print('TERMINADO al fin :D')
    
  
# 6. Guardar en CSV  
    
with open('cervezasfinal.csv', 'w', newline = '') as cervezas_final:
    salida = csv.writer(cervezas_final)
    salida.writerows(tabla)
    
    


    
    
        
