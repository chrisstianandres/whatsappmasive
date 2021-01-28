import json

from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.cliente.forms import ClienteForm, FileForm
from apps.cliente.models import Cliente
import pandas as pd

opc_icono = 'fa fa-user'
opc_entidad = 'Clientes'
crud = '/cliente/nuevo'


class lista(ListView):
    model = Cliente
    template_name = "cliente_list.html"
    permission_required = 'cliente.view_cliente'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                data = []
                for c in Cliente.objects.all():
                    data.append(c.toJSON())
            elif action == 'search':
                data = []
                term = request.POST['term']
                query = Cliente.objects.filter(
                    Q(nombres__icontains=term) | Q(apellidos__icontains=term) | Q(cedula__icontains=term))[0:10]
                for a in query:
                    item = a.toJSON()
                    item['text'] = a.get_full_name()
                    data.append(item)
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nuevo Cliente'
        data['titulo'] = 'Listado de Clientes'
        data['form'] = ClienteForm
        data['form_file'] = FileForm
        data['nuevo'] = '/cliente/nuevo'
        return data


class CrudView(TemplateView):
    form_class = ClienteForm
    template_name = 'cliente_form.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']

        try:
            if action == 'add':
                f = ClienteForm(request.POST)
                data = self.save_data(f)
            if action == 'file':
                f = FileForm(request.POST, request.FILES)
                if f.is_valid():
                    var = f.save()
                    num = pd.read_excel(var.archivo.path)
                    data_dict = num.to_dict('list')
                    celulares = data_dict['celular']
                    key_to_lookup = 'nombre'
                    if key_to_lookup in data_dict:
                        nombres = data_dict['nombre']
                        combo = zip(nombres, celulares)
                        for nombre, celular in combo:
                            c = Cliente()
                            c.nombres = nombre
                            c.telefono = '+'+str(celular)
                            c.save()
                    else:
                        for numero in celulares:
                            c = Cliente()
                            c.nombres = 'Sin nombre'
                            c.telefono = '+'+str(numero)
                            c.save()
                else:
                    data['error'] = f.errors
            elif action == 'edit':
                pk = request.POST['id']
                cliente = Cliente.objects.get(pk=int(pk))
                f = ClienteForm(request.POST, instance=cliente)
                data = self.save_data(f)
            elif action == 'delete':
               pk = request.POST['id']
               cli = Cliente.objects.get(pk=pk)
               cli.delete()
               data['resp'] = True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def save_data(self, f):
        data = {}
        if f.is_valid():
            f.save()
        else:
            data['error'] = f.errors
        return data