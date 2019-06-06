import json
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from pymongo import *
from bs4 import BeautifulSoup
from bson.objectid import ObjectId

from ltweb import conflict_detection as confd


class HomeView(TemplateView):
    template_name = "home.html"


class EditarDeclaracion(TemplateView):
    template_name = "ver.html"
    myclient = MongoClient("mongodb+srv://admin:leytransparente@leytransparente-m6y51.mongodb.net/test?retryWrites"
                           "=true&w=majority")
    mydb = myclient["leytransparente"]
    mycol = mydb["declaraciones"]

    def get_context_data(self, **kwargs):
        # Eso es get, para que sea más seguro, usar POST
        ctx = super().get_context_data()
        ctx['id'] = self.request.GET.get('id', None)
        
        query = self.mycol.find_one({"_id": ObjectId(ctx['id'])})
        query.pop('_id')
        ctx['json'] = query
        ctx['declaracion'] = json.dumps(query)
        
        return ctx


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
        
        if query == None: # inserta automaticamente porque no existe nadie.
            self.mycol.insert(dic)

        else: # actualiza el registri por los datos contenidos en el JSON
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

        query = self.mycol.find({"Meta":True}, {"_id":1, "Datos_del_Declarante.nombre":1, "Datos_del_Declarante.Apellido_Paterno":1, "Datos_del_Declarante.Apellido_Materno":1,"Fecha_de_la_Declaracion":1})
        data = []
        
        for par in query:
            dic = {'id':par["_id"],
                    'nombres': par['Datos_del_Declarante']['nombre'],
                   'apellido_paterno': par['Datos_del_Declarante']['Apellido_Paterno'],
                   'apellido_materno': par['Datos_del_Declarante']['Apellido_Materno'],
                   'fecha_declaracion': par['Fecha_de_la_Declaracion'][8:10]+"/"+par['Fecha_de_la_Declaracion'][5:7]+"/"+par['Fecha_de_la_Declaracion'][:4]}
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

            materias = ""
            if (len(soup.findAll("materia")) > 0):
                materias = "materia"
            elif (len(soup.findAll("materias"))):
                materias = "materias"
            elif (len(soup.findAll("Materia"))):
                materias = "Materias"
            elif (len(soup.findAll("Materias"))):
                materias = "Materias"
            for tag in soup.findAll(materias):
                lista_tags.append(tag.text.strip())  # almacenar los tags en una lista

            if(len(soup.findAll("url")) > 0):
                url_ley = soup.findAll("url")[0].text  # guardar la url de la ley para mostrarla en caso que sea necesario
            else:
                url_ley=""

            if (len(soup.findAll("resumen")) > 0):
                resumen = soup.findAll("resumen")[0].text
            elif (len(soup.findAll("Resumen")) > 0):
                resumen = soup.findAll("Resumen")[0].text
            else:
                resumen = "Resumen no disponible"

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
        #matches = confd.conflicto_patrimonio(lista_tags)
        return redirect('Conflictos', ley = numero)


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


class ConflictoView(TemplateView):
    template_name = "conflict_view.html"
    myclient = MongoClient("mongodb+srv://admin:leytransparente@leytransparente-m6y51.mongodb.net/test?retryWrites"
                           "=true&w=majority")
    mydb = myclient["leytransparente"]
    decl = mydb["declaraciones"]
    leyes = mydb["leyes"]
    cats = mydb["categorias"]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ley = self.kwargs['ley']
        print(f"Buscando Ley {ley}")
        tags_ley = self.leyes.find_one({"numero": ley}, {"tags": 1,"nombre": 1, "resumen": 1})
        if(tags_ley == None):
            return ctx
        print("Buscando tags:")
        tag_set = set({})
        if tags_ley is not None:
            for tag in tags_ley["tags"]:
                tags = self.cats.find_one({"tags": tag.upper()}, {"tags": 1})
                if tags is not None:
                    for cat_tag in tags["tags"]:
                        tag_set.add(cat_tag)
        print("Revisando declaraciones")
        ctx["nro_ley"] = ley
        ctx["nombre_ley"] = tags_ley["nombre"]
        ctx["desc_ley"] = tags_ley["resumen"]
        high = []
        low = []
        conflictos = confd.conflicto_patrimonio(list(tag_set))
        ctx["conflictos"] = conflictos
        for conflicto in conflictos:
            if(conflicto[0] > 109):
                high.append(conflicto)
            else:
                low.append(conflicto)
        ctx["high"] = high
        ctx["low"] = low
        print("Conflictos encontrados: "+ str(len(conflictos)))
        return ctx
