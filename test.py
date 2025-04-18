import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

@pytest.fixture
def driver():
    driver = webdriver.Safari()
    yield driver
    driver.quit()

def tomar_captura(driver, nombre):
    if not os.path.exists("capturas"):
        os.makedirs("capturas")
    driver.save_screenshot(f"capturas/{nombre}.png")

def test_inventory_system(driver):
    html_file = os.path.abspath("index.html")
    driver.get(f"file://{html_file}")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "product-form")))
    tomar_captura(driver, "01_pagina_cargada")

    # Agregar producto
    driver.find_element(By.ID, 'nombre').send_keys('Laptop Dell')
    driver.find_element(By.ID, 'cantidad').send_keys('3')
    driver.find_element(By.ID, 'categoria').send_keys('Electrónica')
    tomar_captura(driver, "02_formulario_completado")
    driver.find_element(By.ID, 'submit-btn').click()
    time.sleep(1)
    tomar_captura(driver, "03_producto_agregado")

    rows = driver.find_elements(By.CSS_SELECTOR, '#tabla tbody tr')
    assert len(rows) == 1
    print("✅ Producto agregado correctamente")

    # Buscar
    driver.find_element(By.ID, 'search-input').send_keys('Dell')
    driver.find_element(By.ID, 'search-btn').click()
    time.sleep(1)
    tomar_captura(driver, "04_busqueda_realizada")
    assert 'Dell' in driver.find_element(By.CSS_SELECTOR, '#tabla tbody tr td:first-child').text

    driver.find_element(By.ID, 'search-input').clear()
    time.sleep(1)

    # Editar
    driver.find_element(By.CLASS_NAME, 'edit-btn').click()
    time.sleep(1)
    tomar_captura(driver, "05_modo_edicion")

    cantidad = driver.find_element(By.ID, 'cantidad')
    cantidad.clear()
    cantidad.send_keys('5')
    tomar_captura(driver, "06_valor_actualizado")
    driver.find_element(By.ID, 'submit-btn').click()
    time.sleep(1)
    tomar_captura(driver, "07_producto_editado")
    assert driver.find_element(By.CSS_SELECTOR, '#tabla tbody tr td:nth-child(2)').text == '5'

    # Eliminar
    driver.find_element(By.CLASS_NAME, 'delete-btn').click()
    time.sleep(1)
    Alert(driver).accept()
    time.sleep(1)
    tomar_captura(driver, "08_producto_eliminado")
    assert 'No hay productos' in driver.find_element(By.CSS_SELECTOR, '#tabla tbody tr td').text

    print("✅ Todas las pruebas pasaron exitosamente")
