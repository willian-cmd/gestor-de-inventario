from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import time
import os

# Crear carpeta de capturas
if not os.path.exists('capturas'):
    os.makedirs('capturas')

def tomar_captura(driver, nombre):
    driver.save_screenshot(f'capturas/{nombre}.png')

def test_inventory_system():
    # Configurar el driver de Safari
    driver = webdriver.Safari()

    try:
        # Obtener la ruta absoluta al archivo HTML
        html_file = os.path.abspath('index.html')
        
        print("\n=== Iniciando pruebas del Gestor de Inventario ===")

        # 1. Cargar la página
        print("\n1. Cargando página...")
        driver.get(f'file://{html_file}')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'product-form')))
        print("Página cargada correctamente")
        tomar_captura(driver, "01_pagina_cargada")

        # 2. Agregar producto
        print("\n2. Probando agregar producto...")
        nombre = driver.find_element(By.ID, 'nombre')
        cantidad = driver.find_element(By.ID, 'cantidad')
        categoria = driver.find_element(By.ID, 'categoria')
        submit_btn = driver.find_element(By.ID, 'submit-btn')

        nombre.send_keys('Laptop Dell')
        cantidad.send_keys('3')
        categoria.send_keys('Electrónica')
        tomar_captura(driver, "02_formulario_completado")
        submit_btn.click()
        time.sleep(1)
        tomar_captura(driver, "03_producto_agregado")

        rows = driver.find_elements(By.CSS_SELECTOR, '#tabla tbody tr')
        assert len(rows) == 1, "Error: Producto no apareció en la tabla"
        print("Producto agregado correctamente")

        # 3. Buscar producto
        print("\n3. Probando búsqueda...")
        search_input = driver.find_element(By.ID, 'search-input')
        search_btn = driver.find_element(By.ID, 'search-btn')

        search_input.send_keys('Dell')
        search_btn.click()
        time.sleep(1)
        tomar_captura(driver, "04_busqueda_realizada")

        found_product = driver.find_element(By.CSS_SELECTOR, '#tabla tbody tr td:first-child').text
        assert 'Dell' in found_product, "Error: Búsqueda no encontró el producto"
        print("Búsqueda funcionó correctamente")

        driver.find_element(By.ID, 'search-input').clear()
        time.sleep(1)

        # 4. Editar producto
        print("\n4. Probando edición...")
        edit_btn = driver.find_element(By.CLASS_NAME, 'edit-btn')
        edit_btn.click()
        time.sleep(1)
        tomar_captura(driver, "05_modo_edicion")

        assert driver.find_element(By.ID, 'submit-btn').text == 'Actualizar', "Error: No entró en modo edición"

        cantidad = driver.find_element(By.ID, 'cantidad')
        cantidad.clear()
        cantidad.send_keys('5')
        tomar_captura(driver, "06_valor_actualizado")
        driver.find_element(By.ID, 'submit-btn').click()
        time.sleep(1)
        tomar_captura(driver, "07_producto_editado")

        updated_qty = driver.find_element(By.CSS_SELECTOR, '#tabla tbody tr td:nth-child(2)').text
        assert updated_qty == '5', "Error: Cantidad no se actualizó"
        print("Edición funcionó correctamente")

        # 5. Eliminar producto
        print("\n5. Probando eliminación...")
        delete_btn = driver.find_element(By.CLASS_NAME, 'delete-btn')
        delete_btn.click()
        time.sleep(1)
        Alert(driver).accept()
        time.sleep(1)
        tomar_captura(driver, "08_producto_eliminado")

        empty_message = driver.find_element(By.CSS_SELECTOR, '#tabla tbody tr td').text
        assert 'No hay productos' in empty_message, "Error: Producto no se eliminó"
        print("Eliminación funcionó correctamente")

        print("\n ¡Todas las pruebas pasaron exitosamente!")

    except Exception as e:
        print(f"\n Error en las pruebas: {str(e)}")
        tomar_captura(driver, "ERROR")
        raise

    finally:
        driver.quit()

if __name__ == "__main__":
    test_inventory_system()
