import os
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
import subprocess

class main_frame:
    def find_path(self):
        rutas = ['C:\Program Files\Google\Chrome\Application\chrome.exe', "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
        for ruta in rutas:
            if os.path.exists(ruta):
                self.ruta_encontrada = ruta
                return self.ruta_encontrada  # Agregar return para salir del bucle si se encuentra la ruta
        return None  # Devolver None si no se encuentra ninguna ruta

    def find_chrome(self):
        self.ruta = self.find_path()
        if self.ruta:
            self.cmd = f'"{self.ruta}" --remote-debugging-port=9222'
            return self.cmd
        else:
            return None  # Devolver None si no se encontró la ruta

    def start_chrome(self):
        self.cmd = self.find_chrome()
        if self.cmd:
            subprocess.Popen(self.cmd, shell=True)
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
            # Crear un objeto Service usando ChromeDriverManager
            service = ChromeService(executable_path=ChromeDriverManager().install())
            # Pasar el objeto Service a webdriver.Chrome
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            print("No se encontró la ruta de Chrome.")

    def click(self, id):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, id))
        )
        self.driver.execute_script(f"document.getElementById('{id}').click();")

    def insert(self, id, texto):
        self.driver.execute_script(f"document.getElementById('{id}').value = '{texto}';")

    def insertar_imagen(self, valor, elemento, texto):
        if isinstance(valor, str):
            valor = getattr(By, valor)

        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((valor, elemento)))
        element.send_keys(texto)

    def click_menu(self, valor, boton):
        # Convierte la cadena a la clase By si es necesario
        if isinstance(valor, str):
            valor = getattr(By, valor)

        element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((valor, boton)))
        element.click() 

    def buscar(self, elemento):
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, elemento))) 
        return element
