import json
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from bs4 import BeautifulSoup
from bson.objectid import ObjectId

from ltweb import conflict_detection as confd
from .conn import DBconnection
from datetime import datetime


class HomeView(TemplateView):
    template_name = "home.html"


class ViewDeclaracion(TemplateView):
    template_name = "ver.html"
    conn = DBconnection()
    mycol = conn.get_collection("declaraciones")

    def get_context_data(self, **kwargs):
        # Eso es get, para que sea más seguro, usar POST
        ctx = super().get_context_data()
        ctx['id'] = self.kwargs['id']

        query = self.mycol.find_one({"_id": ObjectId(ctx['id'])})
        query.pop('_id')
        ctx['declaracion'] = json.dumps(query)

        return ctx


class SubirDeclaracionView(View):
    context = {}
    initial = {'key': 'value'}
    conn = DBconnection()
    mycol = conn.get_collection("declaraciones")
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
        dic["meta"] = {}
        dic["meta"]["actual"] = True

        query = self.mycol.find_one({"Datos_del_Declarante.nombre": dic["Datos_del_Declarante"]["nombre"],
                                     "Datos_del_Declarante.Apellido_Paterno": dic["Datos_del_Declarante"][
                                         "Apellido_Paterno"],
                                     "Datos_del_Declarante.Apellido_Materno": dic["Datos_del_Declarante"][
                                         "Apellido_Materno"],
                                     "meta.actual": True})

        if query == None:  # inserta automaticamente porque no existe nadie.
            dic["partido"] = 'null'
            # x=self.mycol.insert(dic)

        else:  # actualiza el registri por los datos contenidos en el JSON
            if dic["Fecha_de_la_Declaracion"] >= query["Fecha_de_la_Declaracion"]:
                self.mycol.update({"Datos_del_Declarante.nombre": dic["Datos_del_Declarante"]["nombre"],
                                   "Datos_del_Declarante.Apellido_Paterno": dic["Datos_del_Declarante"][
                                       "Apellido_Paterno"],
                                   "Datos_del_Declarante.Apellido_Materno": dic["Datos_del_Declarante"][
                                       "Apellido_Materno"],
                                   "meta.actual": True}, {"$set": {"meta.actual": False}})
                dic["partido"] = query["partido"]
        x = self.mycol.insert(dic)

        return redirect('Ver Declaracion', id=x)


class DiputadosListView(TemplateView):
    conn = DBconnection()
    mycol = conn.get_collection("declaraciones")

    template_name = 'diputados_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.mycol.find({"meta.actual": True},
                                {"_id": 1, "Datos_del_Declarante.nombre": 1, "Datos_del_Declarante.Apellido_Paterno": 1,
                                 "Datos_del_Declarante.Apellido_Materno": 1, "Fecha_de_la_Declaracion": 1,
                                 "partido": 1})
        data = []

        for par in query:
            # print(par)
            dic = {'id': par["_id"],
                   'nombres': par['Datos_del_Declarante']['nombre'],
                   'apellido_paterno': par['Datos_del_Declarante']['Apellido_Paterno'],
                   'apellido_materno': par['Datos_del_Declarante']['Apellido_Materno'],
                   'fecha_declaracion': par['Fecha_de_la_Declaracion'][8:10] + "/" + par['Fecha_de_la_Declaracion'][
                                                                                     5:7] + "/" + par[
                                                                                                      'Fecha_de_la_Declaracion'][
                                                                                                  :4],
                   'partido': par['partido']}
            data.append(dic)

        context['diputados'] = data
        return context


class SubirLeyView(View):
    context = {}
    initial = {'key': 'value'}
    conn = DBconnection()
    mycol = conn.get_collection("leyes")
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
        dic = {}
        soup = BeautifulSoup(L, "html.parser")

        if len(soup.findAll("tipo")) > 0:
            tipo = soup.findAll("tipo")[0].text
        elif len(soup.findAll("Tipo")) > 0:
            tipo = soup.findAll("Tipo")[0].text
        else:
            tipo = ""

        if tipo == "Ley":  # condicion para filtrar decreto, codigo, ley, etc
            numero = soup.findAll("numero")[0].text  # obtener el numero de la ley
            nombre = soup.findAll("titulonorma")[0].text

            lista_tags = []

            materias = ""
            if len(soup.findAll("materia")) > 0:
                materias = "materia"
            elif len(soup.findAll("materias")):
                materias = "materias"
            elif len(soup.findAll("Materia")):
                materias = "Materias"
            elif len(soup.findAll("Materias")):
                materias = "Materias"
            for tag in soup.findAll(materias):
                lista_tags.append(tag.text.strip())  # almacenar los tags en una lista

            if len(soup.findAll("url")) > 0:
                url_ley = soup.findAll("url")[
                    0].text  # guardar la url de la ley para mostrarla en caso que sea necesario
            else:
                url_ley = ""

            if len(soup.findAll("resumen")) > 0:
                resumen = soup.findAll("resumen")[0].text
            elif len(soup.findAll("Resumen")) > 0:
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
        # matches = confd.conflicto_patrimonio(lista_tags)
        return redirect('Conflictos', ley=numero)


class LeyesListView(TemplateView):
    conn = DBconnection()
    mycol = conn.get_collection("leyes")

    template_name = 'leyes_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.mycol.find()
        data = []

        for par in query:
            dic = {'numero': par['numero'],
                   'nombre': par['nombre'],
                   'resumen': par['resumen'],
                   'url': par["url"],
                   'tags': par["tags"]}
            data.append(dic)

        context['leyes'] = data
        return context


class ConflictoView(TemplateView):
    template_name = "conflict_view.html"
    conn = DBconnection()
    decl = conn.get_collection("declaraciones")
    leyes = conn.get_collection("leyes")
    confl = conn.get_collection("conflictos")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ley = self.kwargs['ley']
        print(f"Buscando Ley {ley}")
        tags_ley = self.leyes.find_one({"numero": ley}, {"tags": 1, "nombre": 1, "resumen": 1})

        if tags_ley is None:
            return ctx

        print("Revisando declaraciones")
        ctx["nro_ley"] = ley
        ctx["nombre_ley"] = tags_ley["nombre"]
        ctx["desc_ley"] = tags_ley["resumen"]
        high = []
        low = []
        conflictos = confd.conflicto_embedding(list(tags_ley["tags"]))
        ctx["conflictos"] = conflictos

        # Creacion de la lista que almacena diccionarios a insertar en la collecion de conflictos
        diclist = []

        for conflicto in conflictos:
            duplicado = self.confl.find_one({"ley":ley , "id_declaracion": conflicto[3]})

            dic = {"ley": ley,
                   "nombre_ley": ctx["nombre_ley"],
                   "id_declaracion": conflicto[3],
                   "parlamentario": conflicto[2]
                   }
            query = self.decl.find_one({"_id": conflicto[3]})
            dic["partido"] = query["partido"]
            dic["pariente"] = 'null'
            dic["meta"] = {}
            dic["meta"]["Fecha"] = datetime.today()

            dic["razon"] = {}
            dic["razon"]["prov_conf"] = "acciones"
            dic["razon"]["motivo"] = conflicto[4]["Nombre_Razon_Social"]

            if conflicto[0] * conflicto[1] > 100:
                high.append(conflicto)
                dic["grado"] = "grave"
            else:
                low.append(conflicto)
                dic["grado"] = "leve"

            if duplicado != None:
                continue
            diclist.append(dic)

        if len(diclist) > 0:
            x = self.confl.insert_many(diclist)

        ctx["high"] = high
        ctx["low"] = low
        print("Conflictos encontrados: " + str(len(conflictos)))

        return ctx


class ConflictoListView(TemplateView):
    template_name = 'conflictos_list.html'
    conn = DBconnection()
    confl = conn.get_collection("conflictos")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.confl.find()
        data = []

        for conf in query:
            dic = {
                "ley": conf["ley"],
                "nombre_ley": conf["nombre_ley"],
                "id_parlamentario": str(conf["id_declaracion"]),
                "parlamentario": conf["parlamentario"],
                "partido": conf["partido"],
                "grado": conf["grado"],
                "prov_conf": conf["razon"]["prov_conf"],
                "motivo": conf["razon"]["motivo"]
            }

            if conf["pariente"] is not None:
                dic["pariente"] = conf["pariente"]

            data.append(dic)

        # print(data)
        context["conflictos"] = json.dumps(data)
        print(context["conflictos"])
        return context
