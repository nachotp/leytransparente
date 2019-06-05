import json

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from pymongo import *

class HomeView(TemplateView):
    template_name = "home.html"
# Create your views here.

class EditarDeclaracion(TemplateView):
    template_name = "editar.html"


class SubirDeclaracionView(View):
    context = {}
    initial = {'key': 'value'}
    myclient = MongoClient("mongodb+srv://admin:leytransparente@leytransparente-m6y51.mongodb.net/test?retryWrites"
                           "=true&w=majority")
    mydb = myclient["leytransparente"]
    mycol = mydb["declaraciones"]
    template_name = 'declaracion_form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        
        L = ''
        contador = 0

        for chunk in request.FILES['uploaded_file']:

            if contador != 1 and contador != 2:
                L += chunk.decode(encoding='UTF-8')
                contador += 1

            else:
                contador += 1

        dic = json.loads(L)
        dic["Meta"] = True

        query = self.mycol.find_one({"Datos_del_Declarante.nombre":dic["Datos_del_Declarante"]["nombre"], 
                                    "Datos_del_Declarante.Apellido_Paterno":dic["Datos_del_Declarante"]["Apellido_Paterno"], 
                                    "Datos_del_Declarante.Apellido_Materno":dic["Datos_del_Declarante"]["Apellido_Materno"],
                                    "Meta":True})
        
        if query == None: #inserta automaticamente porque no existe nadie.
            self.mycol.insert(dic)

        else: #actualiza el registri por los datos contenidos en el JSON
            if(dic["Fecha_de_la_Declaracion"] > query["Fecha_de_la_Declaracion"]):
                self.mycol.update({"Datos_del_Declarante.nombre":dic["Datos_del_Declarante"]["nombre"], 
                                    "Datos_del_Declarante.Apellido_Paterno":dic["Datos_del_Declarante"]["Apellido_Paterno"], 
                                    "Datos_del_Declarante.Apellido_Materno":dic["Datos_del_Declarante"]["Apellido_Materno"],
                                    "Meta":True}, { "$set": {"Meta": False}})
                self.mycol.insert(dic)

        return redirect('Lista Diputados')


class DiputadosListView(TemplateView):
    myclient = MongoClient("mongodb+srv://admin:leytransparente@leytransparente-m6y51.mongodb.net/test?retryWrites"
                           "=true&w=majority")
    mydb = myclient["leytransparente"]
    mycol = mydb["declaraciones"]
    template_name = 'diputados_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.mycol.find()
        data = []
        
        for par in query:
            dic = {'nombres': par['Datos_del_Declarante']['nombre'],
                   'apellido_paterno': par['Datos_del_Declarante']['Apellido_Paterno'],
                   'apellido_materno': par['Datos_del_Declarante']['Apellido_Materno']}
            data.append(dic)

        context['diputados'] = data
        return context


class SubirLeyView(View):
    context = {}
    initial = {'key': 'value'}
    myclient = MongoClient("mongodb+srv://admin:leytransparente@leytransparente-m6y51.mongodb.net/test?retryWrites"
                           "=true&w=majority")
    mydb = myclient["leytransparente"]
    mycol = mydb["leyes"]
    template_name = 'ley_form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        print('Uploaded file: ', request.FILES['uploaded_file'])
        L = ''
        contador = 0

        for chunk in request.FILES['uploaded_file']:

            if contador != 1 and contador != 2:
                L += chunk.decode(encoding='UTF-8')
                contador += 1

            else:
                contador += 1
        """SEGMENTO AGREGADO EN BASE AL TRABAJO DE OBTENCION DE DATOS"""
        dic={}
        soup = BeautifulSoup(L, "html.parser")

        if (len(soup.findAll("tipo")) > 0):
            tipo = soup.findAll("tipo")[0].text
        elif (len(soup.findAll("Tipo")) > 0):
            tipo = soup.findAll("Tipo")[0].text
        else:
            tipo = ""

        if (tipo == "Ley"):  # condicion para filtrar decreto, codigo, ley, etc
            numero = soup.findAll("numero")[0].text  # obtener el numero de la ley
            nombre = soup.findAll("titulonorma")[0].text

            lista_tags = []

            for tag in soup.findAll("terminolibre"):
                lista_tags.append(tag.text.strip())  # almacenar los tags en una lista

            url_ley = soup.findAll("url")[0].text  # guardar la url de la ley para mostrarla en caso que sea necesario

            if (len(soup.findAll("Resumen")) > 0):
                resumen = soup.findAll("Resumen")[0].text
            else:
                resumen = ""

            dic["numero"] = numero
            dic["nombre"] = nombre
            dic["resumen"] = resumen
            dic["tags"] = lista_tags
            dic["url"] = url_ley

            try:
                x = self.mycol.insert_one(dic)
                print("ley insertada correctamente")
            except:
                print("problemas agregando la ley a la base")

        """SEGMENTO AGREGADO EN BASE AL TRABAJO DE OBTENCION DE DATOS"""

        return redirect('Lista Leyes')



class LeyesListView(TemplateView):
    myclient = MongoClient("mongodb+srv://admin:leytransparente@leytransparente-m6y51.mongodb.net/test?retryWrites"
                           "=true&w=majority")
    mydb = myclient["leytransparente"]
    mycol = mydb["leyes"]
    template_name = 'leyes_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.mycol.find()
        data = []

        for par in query:
            dic = {'numero': par['numero'],
                   'nombre': par['nombre'],
                   'resumen': par['resumen'],
                   'url' : par["url"],
                   'tags' : par["tags"]}
            data.append(dic)

        context['leyes'] = data
        return context