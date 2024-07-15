from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import json
import logging
from datetime import datetime
import argparse


# Configurar Selenium y el controlador de Firefox
options = FirefoxOptions()
options.add_argument("--headless")  # Ejecutar en modo headless si lo deseas
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def convertir_numero(texto):
    try:
        texto = texto.replace(',', '')
        if 'k' in texto:
            return int(float(texto[:-1]) * 1000)
        elif 'M' in texto:
            return int(float(texto[:-1]) * 1000000)
        else:
            return int(texto)
    except ValueError:
        logging.error(f"Error al convertir el número: {texto}")
        return 0

def obtener_datos_pixabay(url):
    driver.get(url)
    
    try:
        # Espera explícita hasta que la sección de estadísticas esté visible
        WebDriverWait(driver, 40).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.statistics--hQV9u'))
        )
        
        # Espera explícita hasta que las métricas específicas estén presentes
        me_gustan_texto = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#app > div:nth-child(1) > div.page--qGgEw.container--uRw1m > div.userInfo--7BuwE > div > div.statistics--hQV9u > div > div:nth-child(1) > span.count--Zj6dz'))
        ).text.strip()
        
        vistas_texto = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#app > div:nth-child(1) > div.page--qGgEw.container--uRw1m > div.userInfo--7BuwE > div > div.statistics--hQV9u > div > div:nth-child(2) > span.count--Zj6dz'))
        ).text.strip()
        
        descargas_texto = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#app > div:nth-child(1) > div.page--qGgEw.container--uRw1m > div.userInfo--7BuwE > div > div.statistics--hQV9u > div > div:nth-child(3) > span.count--Zj6dz'))
        ).text.strip()
        
        nuestra_seleccion_texto = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#app > div:nth-child(1) > div.page--qGgEw.container--uRw1m > div.userInfo--7BuwE > div > div.statistics--hQV9u > div > div:nth-child(4) > span.count--Zj6dz'))
        ).text.strip()
        
        seguidores_texto = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#app > div:nth-child(1) > div.page--qGgEw.container--uRw1m > div.userInfo--7BuwE > div > div.followStats--gPL7e > button:nth-child(1) > span.userCount--ladWE'))
        ).text.strip()
        
        siguiendo_texto = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#app > div:nth-child(1) > div.page--qGgEw.container--uRw1m > div.userInfo--7BuwE > div > div.followStats--gPL7e > button:nth-child(2) > span.userCount--ladWE'))
        ).text.strip()
 
# FOTOS
#        fotos =  WebDriverWait(driver, 40).until(
#	    EC.presence_of_element_located((By.CSS_SELECTOR, '#app > div:nth-child(1) > div.page--qGgEw.container--uRw1m > div.userMedia--KX5LV > div > div.controls--xnb3V > div.typeSwitcher--nT4xx > div > div:nth-child(2) > button > span > span'))
#        ).text.strip()
	# FOTOS

        fotos = WebDriverWait(driver, 40).until(
	    EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[3]/div/div[1]/div[1]/div/div[1]/button/span/span'))
	).text.strip()
       
        # Convertir los textos a valores numéricos
        me_gustan = convertir_numero(me_gustan_texto)
        vistas = convertir_numero(vistas_texto)
        descargas = convertir_numero(descargas_texto)
        nuestra_seleccion = convertir_numero(nuestra_seleccion_texto)
        seguidores = convertir_numero(seguidores_texto)
        siguiendo = convertir_numero(siguiendo_texto)
        fotos = convertir_numero(siguiendo_texto)
        
        # Obtener la fecha y hora actual en formato ISO 8601
        fecha_y_hora = datetime.now().isoformat()
        
        # Estructurar los datos en un diccionario incluyendo la fecha y hora
        datos = {
            "fecha_y_hora": fecha_y_hora,
            "me_gustan": me_gustan,
            "vistas": vistas,
            "descargas": descargas,
            "nuestra_seleccion": nuestra_seleccion,
            "seguidores": seguidores,
            "siguiendo": siguiendo,
            "fotos": fotos
        }
        
        # Intentar cargar datos existentes desde el archivo JSON
        try:
            with open('pixabay.json', 'r') as f:
                datos_exist = json.load(f)
                if isinstance(datos_exist, dict):
                    # Si es un diccionario, convertirlo a una lista con un elemento
                    datos_exist = [datos_exist]
                elif not isinstance(datos_exist, list):
                    # Si no es ni un diccionario ni una lista, iniciar una nueva lista
                    datos_exist = []
        except FileNotFoundError:
            datos_exist = []
        
        # Agregar los nuevos datos a la lista
        datos_exist.append(datos)
        
        # Guardar los datos como JSON en un archivo
        with open('pixabay.json', 'w') as f:
            json.dump(datos_exist, f, indent=4)
            logging.info("Datos guardados en pixabay.json")
    
    except Exception as e:
        logging.error(f"Error al obtener datos: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Extraer datos de perfil de Pixabay')
    parser.add_argument('url', help='URL del perfil de Pixabay')
    args = parser.parse_args()

    try:
        obtener_datos_pixabay(args.url)
        logging.info("Extracción de datos completada con éxito")
    except Exception as e:
        logging.error(f"Error durante la extracción de datos: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
