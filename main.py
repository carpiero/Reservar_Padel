import pandas as pd
import datetime
import time
import re
import configparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def min_seconds(td):
  minutes = divmod(td.seconds , 60)
  return f'Time:\n{minutes[0]} minutes, {minutes[1]} seconds'

def main():
    print(f'\n\nStar: {datetime.datetime.now().strftime("%H:%M:%S")}\n\n')
    start = datetime.datetime.now()

    cfg = configparser.RawConfigParser()
    cfg.read('/home/carpiero/ir/pass_projects/pass.ini')

    u_padel = cfg['padel']['username']
    p_padel = cfg['padel']['password']

    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install() , options=options)

    driver.get('https://www.centrodeportivosmp.es/')

# reservar desplegable arriba a la derecha
    padel_button = driver.find_element_by_xpath('//*[@id="top-menu"]/li[6]')
    padel_button.click()
    padel_button = driver.find_element_by_xpath('//*[@id="top-menu"]/li[6]/ul/li[1]')
    padel_button.click()

# login
    user_input = driver.find_element_by_id('ctl00_ContentPlaceHolderContenido_Login1_UserName')
    user_input.send_keys(u_padel)
    pass_input = driver.find_element_by_id('ctl00_ContentPlaceHolderContenido_Login1_Password')
    pass_input.send_keys(p_padel)

    enter_button = driver.find_element_by_id('ctl00_ContentPlaceHolderContenido_Login1_LoginButton')
    enter_button.click()

# Dentro de panel usuario click en reservas en lateral izquierdo
    rev_button = driver.find_element_by_id('ctl00_ctl00_ContentPlaceHolderContenido_WUCMenuLateralIzquierdaIntranet_LabelMenuReservasBuscador')
    rev_button.click()


    # time.sleep(60)

    start2 = datetime.datetime.now()
    print(f'\n\nStar2: {datetime.datetime.now().strftime("%H:%M:%S")}\n\n')

# Mover hasta el martes siguiente
    fecha = driver.find_element_by_id('fechaTabla')
    manana = driver.find_element_by_xpath('//*[@id="tablaReserva"]/div[2]/div[2]/div[1]/div[3]/input[3]')
    print(fecha.get_property("value"))
    manana.click()
    manana.click()
    manana.click()
    manana.click()
    manana.click()
    manana.click()
    manana.click()
    print(fecha.get_property("value"))

    while 'lunes' not in fecha.get_property("value").lower():
        time.sleep(2)
        manana.click()

    print(fecha.get_property("value"))
    cuerpotabla = driver.find_element_by_id('CuerpoTabla')
    print(cuerpotabla.get_attribute("time"))

# coger los horarios que queremos
    reser = driver.find_elements_by_class_name('subDivision.plantilla.buttonHora')

    h1 = '18:00'
    h2 = '18:30'
    pista_h1 = []

    for x in reser:
        if x.get_attribute("time") == h1:
            pista_h1.append(x)

    for x in reser:
        if x.get_attribute("time") == h2:
            pista_h1.append(x)


# primero h1 pistas 4, 5 y 6 y luego h2 pistas 4, 5 y 6 primero.

    # pista_h1.insert(0 , pista_h1.pop(3))
    # pista_h1.insert(1 , pista_h1.pop(4))
    # pista_h1.insert(2 , pista_h1.pop(5))
    #
    # pista_h1.insert(6 , pista_h1.pop(9))
    # pista_h1.insert(7 , pista_h1.pop(10))
    # pista_h1.insert(8 , pista_h1.pop(11))

# pistas 1, 2 y 3 primero de distinto horario

    pista_h1.insert(3 , pista_h1.pop(6))
    pista_h1.insert(4 , pista_h1.pop(7))
    pista_h1.insert(5 , pista_h1.pop(8))

    for x in pista_h1:
        print(f'{x.get_attribute("time")} {x.get_attribute("columna")}')

# ir mirando y reservar la libre

    for x in pista_h1:
        try:
            WebDriverWait(driver , 10).until(EC.element_to_be_clickable((By.ID , 'CuerpoTabla')))
            x.click()
            opt = driver.find_elements_by_class_name('btnTiempo')
            opt_text = driver.find_elements_by_class_name('buttonHoraTxt')
            WebDriverWait(driver , 10).until(EC.element_to_be_clickable((By.ID , 'reserva')))
            print(opt_text[0].text)
            if opt_text[0].text == 'Cerrar':
                opt[0].click()
                print(f'{x.get_attribute("time")} {x.get_attribute("columna")}')
            else:
                driver.find_element_by_id('terminos').click()
                opt[0].click()
                break
        except ElementClickInterceptedException:
            pass
            print('ERROR')
            print(f'pista ocupada {x.get_attribute("time")} {x.get_attribute("columna")}')


        finally:  # ejecutar siempre
            print(f'\nFINAL')

    print(driver.find_element_by_id('ctl00_ContentPlaceHolderContenido_LabelEspacio').text)
    print(driver.find_element_by_id('ctl00_ContentPlaceHolderContenido_LabelHorario').text)
    print(driver.find_element_by_id('ctl00_ContentPlaceHolderContenido_LabelFecha').text)
    print(driver.find_element_by_id('ctl00_ContentPlaceHolderContenido_LabelPrecio').text)

# reserva final
#     driver.find_element_by_id('ctl00_ContentPlaceHolderContenido_CheckBoxAceptoCondicionesLegales').click()
#     driver.find_element_by_id('ctl00_ContentPlaceHolderContenido_ButtonPagoSaldo').click()


    finish = datetime.datetime.now() - start
    finish2 = datetime.datetime.now() - start2
    print(f'\n\nFinish: {datetime.datetime.now().strftime("%H:%M:%S")}\n\n')
    print(min_seconds(finish))
    print(min_seconds(finish2))
    driver.quit()


if __name__ == "__main__":
    main()

