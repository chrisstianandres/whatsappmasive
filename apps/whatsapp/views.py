import json
import socket
from time import sleep

import pandas as pd
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from apps.cliente.models import Cliente
from apps.whatsapp.forms import MensajeForm
from apps.whatsapp.models import Mensaje


class CrudView(TemplateView):
    form_class = MensajeForm
    template_name = 'mensaje_form.html'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def element_presence(self, by, xpath, time, driver):
        element_present = EC.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(driver, time).until(element_present)

    def send_whatsapp_msg(self, phone_no, text, num_vec, driver):
        driver.get("https://web.whatsapp.com/send?phone={}&source=&data=#".format(phone_no))
        try:
            driver.switch_to_alert().accept()
        except Exception as e:
            pass

        try:
            self.element_presence(
                By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]', 30, driver)
            txt_box = driver.find_element(
                By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')

            for x in range(num_vec):
                txt_box.send_keys(text)
                txt_box.send_keys("\n")

        except Exception as e:
            print("invailid phone no :" + str(phone_no))

    def is_connected(self):
        try:
            # conectarse al host: nos dice si el host es en realidad
            # accesible
            socket.create_connection(("www.google.com", 80))
            return True
        except:
            self.is_connected()

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                moblie_no_list = []
                f = self.form_class(request.POST)
                if f.is_valid():
                    pk = f.save()
                    cli = Cliente.objects.all()
                    mens = Mensaje.objects.get(id=pk.id)
                    message_text = str(mens.mensaje)
                    num_vec = int(mens.numero_veces)
                    print(message_text, num_vec)
                    driver = webdriver.Chrome(ChromeDriverManager().install())
                    driver.get("http://web.whatsapp.com")
                    sleep(10)
                    for c in cli:
                        moblie_no_list.append(c.telefono)
                    for moblie_no in moblie_no_list:
                        try:
                            self.send_whatsapp_msg(moblie_no, message_text, num_vec, driver)
                        except Exception as e:
                            sleep(10)
                            self.is_connected()
                else:
                    print(2)
                    data['error'] = f.errors
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['entidad'] = 'Mensaje'
        data['boton'] = 'Enviar'
        data['titulo'] = 'Listado de Clientes'
        data['form'] = MensajeForm()
        return data

#