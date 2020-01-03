import json
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from bs4 import BeautifulSoup
from bson.objectid import ObjectId

from ltweb import conflict_detection as confd
from .conn import DBconnection
from .clustering import VectorClustering
from .utilities import send_email
from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

"""
content_type = ContentType.objects.get_for_model(User)
permission = Permission.objects.create(
    codename='is_oficina',
    name='Oficina de Informaciones',
    content_type=content_type,
)

content_type = ContentType.objects.get_for_model(User)
permission2 = Permission.objects.create(
    codename='is_comision',
    name='Comision de Etica',
    content_type=content_type,
)

content_type = ContentType.objects.get_for_model(User)
permission3 = Permission.objects.create(
    codename='is_admin',
    name='Administrador',
    content_type=content_type,
)
"""


class HomeView(LoginRequiredMixin,TemplateView):
    template_name = "home.html"


class RegistroView(PermissionRequiredMixin,LoginRequiredMixin,View):
    template_name = "registro.html"
    context = {}
    permission_required = 'auth.is_admin'

    def get(self, request, *args, **kwargs):
        self.context['repetido'] = False
        self.context['diferente'] = False
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        try:
            self.context['repetido'] = False
            self.context['diferente'] = False
            ctx = request.POST

            if ctx['password'] != ctx['passwordConfirm']:
                self.context['diferente'] = True
                return render(request, self.template_name, self.context)

            print("Registrando...")
            user = User.objects.create_user(ctx['username'], ctx['email'], ctx['password'])
            user.first_name = ctx['name']
            user.last_name = ctx['apellido']

            print(ctx)

            for perm in ctx.getlist('roles'):
                if perm == 'Oficina de Informaciones':
                    print('oficina')
                    grupo = Group.objects.get(name=perm)
                    user.groups.add(grupo)

                elif perm == 'Comision de Etica':
                    print('comision')
                    grupo = Group.objects.get(name=perm)
                    user.groups.add(grupo)

                else:
                    print('admin')
                    grupo = Group.objects.get(name=perm)
                    user.groups.add(grupo)

            user.save()

            return redirect('Control de usuario')

        except IntegrityError:
            self.context['repetido'] = True
            print("Usuario ya existe")
            return render(request, self.template_name, self.context)


class ActualizarPassView(PermissionRequiredMixin,LoginRequiredMixin,View):
    template_name = "cambiar_pass.html"
    context = {}
    permission_required = 'auth.is_admin'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        self.context['diferente'] = False
        self.context['no_match'] = False

        user = User.objects.get(username=request.POST['username'])

        if not user.check_password(request.POST['password']):
            self.context['diferente'] = True
            dic = {}
            dic['username'] = request.POST['username']
            self.context['usuarios'] = dic
            return render(request, self.template_name, self.context)

        if request.POST['new_password'] != request.POST['new_passwordConfirm']:
            self.context['no_match'] = True
            dic = {}
            dic['username'] = request.POST['username']
            self.context['usuarios'] = dic
            return render(request, self.template_name, self.context)

        user.set_password(request.POST['new_password'])
        user.save()

        return redirect('Control de usuario')


class ActualizarPermisosView(PermissionRequiredMixin,LoginRequiredMixin,View):
    template_name = "actualizar.html"
    context = {}
    permission_required = 'auth.is_admin'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        user = User.objects.get(username=request.POST['username'])
        user.groups.clear()
        user.first_name = request.POST['name']
        user.last_name = request.POST['apellido']
        user.email = request.POST['email']

        user.save()

        user = User.objects.get(username=request.POST['username'])

        grupo = Group.objects.get(name=request.POST['roles'])
        user.groups.add(grupo)

        return redirect('Control de usuario')


class PassView(PermissionRequiredMixin,LoginRequiredMixin,TemplateView):
    template_name = "cambiar_pass.html"
    permission_required = 'auth.is_admin'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.kwargs['id'])

        dic = {}
        dic['username'] = user.username
        dic['nombre'] = user.first_name
        dic['apellido'] = user.last_name
        dic['email'] = user.email
        dic['password'] = user.password

        context['usuarios'] = dic
        return context


class ControlView(PermissionRequiredMixin,LoginRequiredMixin,TemplateView):
    template_name = "control_usuario.html"
    permission_required = 'auth.is_admin'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = []
        users = User.objects.all()

        for u in users:
            if u.is_superuser != True:
                dic = {}
                dic['username'] = u.username
                dic['nombre'] = u.first_name
                dic['apellido'] = u.last_name
                dic['email'] = u.email
                dic['password'] = u.password

                perm = u.get_all_permissions()

                if 'auth.is_oficina' in perm and 'auth.is_comision' in perm:
                    dic['permiso'] = 'Administrador'
                elif 'auth.is_oficina' in perm:
                    dic['permiso'] = 'Oficina de Informaciones'
                elif 'auth.is_comision' in perm:
                    dic['permiso'] = 'Comision de Etica'
                else:
                    dic['permiso'] = "No Tiene Grupo"

                data.append(dic)

        context['usuarios'] = data
        return context


class ActualizarView(PermissionRequiredMixin,LoginRequiredMixin,TemplateView):
    template_name = "actualizar.html"
    permission_required = 'auth.is_admin'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.kwargs['id'])

        dic = {}
        dic['username'] = user.username
        dic['nombre'] = user.first_name
        dic['apellido'] = user.last_name
        dic['email'] = user.email
        dic['password'] = user.password

        context['usuarios'] = dic
        return context


class EliminarUserView(PermissionRequiredMixin,LoginRequiredMixin,View):
    permission_required = 'auth.is_admin'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=self.kwargs['id'])
        user.delete()
        return redirect('Control de usuario')


class ViewDeclaracion(LoginRequiredMixin,TemplateView):
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


class SubirDeclaracionView(PermissionRequiredMixin,LoginRequiredMixin,View):
    context = {}
    initial = {'key': 'value'}
    conn = DBconnection()
    mycol = conn.get_collection("declaraciones")
    template_name = 'declaracion_form.html'
    permission_required = 'auth.is_oficina'

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

        if query is None:  # inserta automaticamente porque no existe nadie.
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


class DiputadosListView(LoginRequiredMixin,TemplateView):
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


class SubirLeyView(PermissionRequiredMixin,LoginRequiredMixin,View):
    context = {}
    initial = {'key': 'value'}
    conn = DBconnection()
    mycol = conn.get_collection("leyes")
    template_name = 'ley_form.html'
    permission_required = 'auth.is_oficina'

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


class LeyesListView(LoginRequiredMixin,TemplateView):
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


class ConflictoView(PermissionRequiredMixin,LoginRequiredMixin,TemplateView):
    template_name = "conflict_view.html"
    conn = DBconnection()
    decl = conn.get_collection("declaraciones")
    leyes = conn.get_collection("leyes")
    confl = conn.get_collection("conflictos")
    stats = conn.get_collection("estadistica")
    permission_required = 'auth.is_oficina'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ley = self.kwargs['ley']
        print(f"Buscando Ley {ley}")
        tags_ley = self.leyes.find_one({"numero": ley}, {"tags": 1, "nombre": 1, "resumen": 1, "url": 1})

        if tags_ley is None:
            return ctx

        print("Revisando declaraciones")
        ctx["nro_ley"] = ley
        ctx["nombre_ley"] = tags_ley["nombre"]
        ctx["desc_ley"] = tags_ley["resumen"]
        ctx["url_ley"] = tags_ley["url"]
        high = []
        low = []
        indirecto = []
        conflictos = confd.conflicto_embedding(list(tags_ley["tags"]))
        ctx["conflictos"] = conflictos
        # Creacion de la lista que almacena diccionarios a insertar en la collecion de conflictos
        diclist = []
        stat_diclist=[]
        cantidad = 0
        generos = []
        regiones = []
        for conflicto in conflictos:
            cantidad += 1
            duplicado = self.confl.find_one({"ley": ley, "id_declaracion": conflicto[3]})

            dic = {"ley": ley,
                   "nombre_ley": ctx["nombre_ley"],
                   "id_declaracion": conflicto[3],
                   "parlamentario": conflicto[2]
                   }
            dic["razon"] = {}
            stat_dic = {}
            if int(conflicto[1]) <= 0:
                apellido_pat = conflicto[2].upper().split()[-2]
                apellido_mat = conflicto[2].upper().split()[-1]
                query = self.decl.find_one({"Datos_del_Declarante.Apellido_Paterno": apellido_pat, "Datos_del_Declarante.Apellido_Materno": apellido_mat})
                dic["partido"] = query["partido"]
                dic["razon"]["prov_conf"] = "indirecto"
                dic["razon"]["motivo"]={}
                dic["razon"]["motivo"]["nombre_involucrado"] = conflicto[6]

                regiones.append(query["Region"]["nombre"])

                if conflicto[1] == 0:
                    dic["razon"]["motivo"]["relacion_diputado"] = "familiar"
                elif conflicto[1] == -1:
                    dic["razon"]["motivo"]["relacion_diputado"] = "lobby"

                dic["razon"]["motivo"]["razon_social"] = conflicto[4]["Nombre_Razon_Social"]

                dic["indirecto"] = "indirecto"
                indirecto.append(conflicto)

            else:
                query = self.decl.find_one({"_id": conflicto[3]})
                dic["partido"] = query["partido"]

                dic["razon"]["prov_conf"] = "acciones"
                dic["razon"]["motivo"] = conflicto[4]["Nombre_Razon_Social"]
                dic["razon"]["prov_conf"] = "acciones"

                regiones.append(query["Region"]["nombre"])

                if conflicto[0] * conflicto[1] > 100:
                    high.append(conflicto)
                    dic["grado"] = "grave"
                else:
                    low.append(conflicto)
                    dic["grado"] = "leve"
                dic["vector"] = conflicto[6]


            dic["pariente"] = 'null'
            dic["meta"] = {}
            dic["meta"]["Fecha"] = datetime.today()


            #dic["razon"] = {}
            #dic["razon"]["prov_conf"] = "acciones"
            #dic["razon"]["motivo"] = conflicto[4]["Nombre_Razon_Social"]
            #dic["vector"] = conflicto[6]



            if duplicado is not None:
                continue
            diclist.append(dic)

        if len(diclist) > 0:
            x = self.confl.insert_many(diclist)
        emails = [x.email for x in User.objects.filter(groups__name = "Comision de Etica")]
        ctx["high"] = high
        ctx["low"] = low

        stat_diclist = []
        for conflicto in diclist:
            stat_query = self.stats.find_one({"Partido": conflicto["partido"]})

            #revisar si el partido ya esta en la lista para actualizarlo
            flag_list = True
            i = -1
            for partido in stat_diclist:
                i += 1
                if conflicto["partido"] == partido["Partido"]:
                    indice_list = i
                    flag_list = False


            if stat_query == None: # si no esta en la BD hay que crear el partido
                if flag_list: # si el partido no esta en la stat_diclist se crea
                    stat_dic = {
                        "Partido": conflicto["partido"],
                        "total_conflictos": 0,
                        "total_graves": 0,
                        "total_leves": 0,
                        "total_directos" : 0,
                        "total_indirectos" : 0,
                        "lista_diputados" : []
                    }
                    stat_dic["total_conflictos"] += 1

                    if conflicto["grado"] == "leve":
                        stat_dic["total_leves"] += 1
                    if conflicto["grado"] == "grave":
                        stat_dic["total_graves"] += 1
                    if conflicto["razon"]["prov_conf"] == "indirecto":
                        stat_dic["total_indirectos"] += 1
                    if conflicto["razon"]["prov_conf"] != "indirecto":
                        stat_dic["total_directos"] += 1

                    # y se le crea el diputado del conflcito para agregarlo a la lista
                    dipu_datos = {
                        "Nombre_completo": conflicto["parlamentario"],
                        "region": regiones[diclist.index(conflicto)],
                        "cant_conflictos": 0,
                        "graves": 0,
                        "leves": 0,
                        "directos": 0,
                        "indirectos": 0
                    }
                    dipu_datos["cant_conflictos"] += 1

                    if conflicto["grado"] == "leve":
                        dipu_datos["leves"] += 1
                    if conflicto["grado"] == "grave":
                        dipu_datos["graves"] += 1
                    if conflicto["razon"]["prov_conf"] == "indirecto":
                        dipu_datos["indirectos"] += 1
                    if conflicto["razon"]["prov_conf"] != "indirecto":
                        dipu_datos["directos"] += 1

                    stat_dic["lista_diputados"].append(dipu_datos)

                    stat_diclist.append(stat_dic)


                else: #si el partido esta en la lista va y actualiza los datos
                    stat_diclist[indice_list]["total_conflictos"] += 1

                    if conflicto["grado"] == "leve":
                        stat_diclist[indice_list]["total_leves"] += 1
                    if conflicto["grado"] == "grave":
                        stat_diclist[indice_list]["total_graves"] += 1
                    if conflicto["razon"]["prov_conf"] == "indirecto":
                        stat_diclist[indice_list]["total_indirectos"] += 1
                    if conflicto["razon"]["prov_conf"] != "indirecto":
                        stat_diclist[indice_list]["total_directos"] += 1

                    #revisar si el diputado del conflicto ya esta en la lista del partido
                    flag = True #diputado no esta en la lista
                    j = 0
                    for diputado in stat_diclist[indice_list]["lista_diputados"]:

                        if conflicto["parlamentario"] == diputado["Nombre_completo"]:
                            indice = j
                            flag = False #diputado si esta en la lista
                        j += 1
                    if flag:#diputado no esta en la lista y hay que crearlo
                        dipu_datos = {
                            "Nombre_completo" : conflicto["parlamentario"],
                            "region" : regiones[diclist.index(conflicto)],
                            "cant_conflictos" : 0,
                            "graves" : 0,
                            "leves" : 0,
                            "directos" : 0,
                            "indirectos" : 0
                        }
                        dipu_datos["cant_conflictos"] += 1

                        if conflicto["grado"] == "leve":
                            dipu_datos["leves"] += 1
                        if conflicto["grado"] == "grave":
                            dipu_datos["graves"] += 1
                        if conflicto["razon"]["prov_conf"] == "indirecto":
                            dipu_datos["indirectos"] += 1
                        if conflicto["razon"]["prov_conf"] != "indirecto":
                            dipu_datos["directos"] += 1

                        stat_diclist[indice_list]["lista_diputados"].append(dipu_datos)

                    else: #diputado si esta en la lista y hay que actualizar
                        #indice = stat_dic["lista_diputados"].index(diputado)

                        stat_diclist[indice_list]["lista_diputados"][indice]["cant_conflictos"] += 1

                        if conflicto["grado"] == "leve":
                            stat_diclist[indice_list]["lista_diputados"][indice]["leves"] += 1
                        if conflicto["grado"] == "grave":
                            stat_diclist[indice_list]["lista_diputados"][indice]["graves"] += 1
                        if conflicto["razon"]["prov_conf"] == "indirecto":
                            stat_diclist[indice_list]["lista_diputados"][indice]["indirectos"] += 1
                        if conflicto["razon"]["prov_conf"] != "indirecto":
                            stat_diclist[indice_list]["lista_diputados"][indice]["directos"] += 1
                

            else: #condicion si el partido ya esta en el base
                id = stat_query["_id"]
                lista_d = stat_query["lista_diputados"]
                total_graves = stat_query["total_graves"]
                total_leves = stat_query["total_leves"]
                total_directos = stat_query["total_directos"]
                total_indirectos = stat_query["total_indirectos"]
                total_conflictos = stat_query["total_conflictos"]

                flag_nbd = True  # diputado no esta en la lista
                j = 0
                for diputado in lista_d:
                    if conflicto["parlamentario"] == diputado["Nombre_completo"]:
                        indice = j
                        flag_nbd = False  # diputado si esta en la lista
                    j += 1
                if flag_nbd:
                    dipu_datos = {
                        "Nombre_completo": conflicto["parlamentario"],
                        "region": regiones[diclist.index(conflicto)],
                        "cant_conflictos": 0,
                        "graves": 0,
                        "leves": 0,
                        "directos": 0,
                        "indirectos": 0
                    }
                    dipu_datos["cant_conflictos"] += 1

                    if conflicto["grado"] == "leve":
                        dipu_datos["leves"] += 1
                        total_leves += 1
                    if conflicto["grado"] == "grave":
                        dipu_datos["graves"] += 1
                        total_graves += 1
                    if conflicto["razon"]["prov_conf"] == "indirecto":
                        dipu_datos["indirectos"] += 1
                        total_indirectos += 1
                    if conflicto["razon"]["prov_conf"] != "indirecto":
                        dipu_datos["directos"] += 1
                        total_directos += 1

                    lista_d.append(dipu_datos)

                else:
                    lista_d[indice]["cant_conflictos"] += 1

                    if conflicto["grado"] == "leve":
                        lista_d[indice]["leves"] += 1
                        total_leves += 1
                    if conflicto["grado"] == "grave":
                        lista_d[indice]["graves"] += 1
                        total_graves += 1
                    if conflicto["razon"]["prov_conf"] == "indirecto":
                        lista_d[indice]["indirectos"] += 1
                        total_indirectos += 1
                    if conflicto["razon"]["prov_conf"] != "indirecto":
                        lista_d[indice]["directos"] += 1
                        total_graves += 1
                total_conflictos+=1
                self.stats.update_one({"_id": id}, {"$set" : {"lista_diputados" : lista_d ,
                                                              "total_graves" : total_graves,
                                                              "total_leves" : total_leves,
                                                              "total_directos" : total_directos,
                                                              "total_indirectos" : total_indirectos,
                                                              "total_conflictos": total_conflictos} })

        if len(stat_diclist) > 0:
            x = self.stats.insert_many(stat_diclist)

        ctx["indirecto"] = indirecto
        print("Conflictos encontrados: " + str(len(conflictos)))
        if(len(conflictos) > 0):
            send_email("Nuevos conflictos encontrados!", "conflict_mail", ctx, "franco.zalavari@sansano.usm.cl")
        return ctx


class ConflictoListView(LoginRequiredMixin,TemplateView):
    template_name = 'conflictos_list.html'
    conn = DBconnection()
    confl = conn.get_collection("conflictos")
    leyes = conn.get_collection("leyes")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.confl.find()
        data = []
        ley_urls = dict()
        for conf in query:

            if conf["ley"] not in ley_urls:
                ley_urls[conf["ley"]] = self.leyes.find_one({"numero": conf["ley"]})

            url_ley = ley_urls[conf["ley"]]

            if url_ley is None:
                url_ley = {}
                url_ley["url"] = "#"
            if conf["partido"] is None:
                conf["partido"] = "Sin información"

            dic = {
                "ley": conf["ley"],
                "nombre_ley": conf["nombre_ley"],
                "id_parlamentario": str(conf["id_declaracion"]),
                "parlamentario": conf["parlamentario"],
                "partido": conf["partido"],
                "grado": conf.get("grado", "indirecto"),
                "url": url_ley["url"]
            }
            if conf["razon"]["prov_conf"] == 'indirecto':
                conf["razon"]["prov_conf"] = 'Indirecto por ' + conf["razon"]["motivo"]["relacion_diputado"]

                dic["nombre_involucrado"] = conf["razon"]["motivo"]["nombre_involucrado"]
                dic["relacion_diputado"] = conf["razon"]["motivo"]["relacion_diputado"]
                dic["razon_social"] = conf["razon"]["motivo"]["razon_social"]
                dic["tipo_conflicto"] = 'indirecto'
            else:
                dic["motivo"] = conf["razon"]["motivo"]
                dic["tipo_conflicto"] = 'directo'

            dic["prov_conf"] = conf["razon"]["prov_conf"]

            if conf["pariente"] is not None:
                dic["pariente"] = conf["pariente"]

            data.append(dic)

        # print(data)
        context["conflictos"] = json.dumps(data)
        print(context["conflictos"])
        return context


class ClusterView(LoginRequiredMixin,TemplateView):
    template_name = "clustest.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vc = VectorClustering()
        cls = vc.cluster()

        conn = DBconnection()
        clus = conn.get_collection("clusters")
        obj = clus.find_one({})

        context["clusters"] = obj["clusters"]

        return context


class StatsView(LoginRequiredMixin,TemplateView):
    template_name = "estadisticas.html"