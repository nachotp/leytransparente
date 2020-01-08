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


class DashboardView(PermissionRequiredMixin,LoginRequiredMixin,TemplateView):
    template_name = "dashboard.html"
    conn = DBconnection()
    decl = conn.get_collection("estadistica")
    confl = conn.get_collection("conflictos")
    permission_required = 'auth.is_oficina'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        sorted_conflicts = self.confl.find(sort=[( 'meta.fecha', -1 )]).limit(5)
        today = datetime.now()
        for i in sorted_conflicts:
            try:
                conflict_date = i["meta"]["fecha"]
                i["meta"]["fecha"] = (today-conflict_date).days
            except:
                conflict_date = i["meta"]["Fecha"]
                i["meta"]["fecha"] = (today-conflict_date).days
        ctx["conflictos"] = sorted_conflicts

            
            
        return ctx

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

    def get_context_data(self, **kwargs):
        # Eso es get, para que sea más seguro, usar POST
        ctx = super().get_context_data()
        ctx['id'] = self.kwargs['id']

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
        cantidad = 0
        for conflicto in conflictos:
            cantidad += 1
            duplicado = self.confl.find_one({"ley": ley, "id_declaracion": conflicto[3]})

            dic = {"ley": ley,
                   "nombre_ley": ctx["nombre_ley"],
                   "id_declaracion": conflicto[3],
                   "parlamentario": conflicto[2]
                   }
            dic["razon"] = {}

            if int(conflicto[1]) <= 0:
                apellido_pat = conflicto[2].upper().split()[-2]
                apellido_mat = conflicto[2].upper().split()[-1]
                query = self.decl.find_one({"Datos_del_Declarante.Apellido_Paterno": apellido_pat, "Datos_del_Declarante.Apellido_Materno": apellido_mat})
                dic["partido"] = query["partido"]
                dic["razon"]["prov_conf"] = "indirecto"
                dic["razon"]["motivo"]={}
                dic["razon"]["motivo"]["nombre_involucrado"] = conflicto[6]

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

        ctx["indirecto"] = indirecto
        print("Conflictos encontrados: " + str(len(conflictos)))
        if(len(conflictos) > 0):
            send_email("Nuevos conflictos encontrados!", "conflict_mail", ctx, "franco.zalavari@sansano.usm.cl")
        return ctx


class ConflictoListView(LoginRequiredMixin,TemplateView):
    template_name = 'conflictos_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # query = self.confl.find()
        # data = []
        # ley_urls = dict()
        # for conf in query:
        #
        #     if conf["ley"] not in ley_urls:
        #         ley_urls[conf["ley"]] = self.leyes.find_one({"numero": conf["ley"]})
        #
        #     url_ley = ley_urls[conf["ley"]]
        #
        #     if url_ley is None:
        #         url_ley = {}
        #         url_ley["url"] = "#"
        #     if conf["partido"] is None:
        #         conf["partido"] = "Sin información"
        #
        #     dic = {
        #         "ley": conf["ley"],
        #         "nombre_ley": conf["nombre_ley"],
        #         "id_parlamentario": str(conf["id_declaracion"]),
        #         "parlamentario": conf["parlamentario"],
        #         "partido": conf["partido"],
        #         "grado": conf.get("grado", "indirecto"),
        #         "url": url_ley["url"]
        #     }
        #     if conf["razon"]["prov_conf"] == 'indirecto':
        #         conf["razon"]["prov_conf"] = 'Indirecto por ' + conf["razon"]["motivo"]["relacion_diputado"]
        #
        #         dic["nombre_involucrado"] = conf["razon"]["motivo"]["nombre_involucrado"]
        #         dic["relacion_diputado"] = conf["razon"]["motivo"]["relacion_diputado"]
        #         dic["razon_social"] = conf["razon"]["motivo"]["razon_social"]
        #         dic["tipo_conflicto"] = 'indirecto'
        #     else:
        #         dic["motivo"] = conf["razon"]["motivo"]
        #         dic["tipo_conflicto"] = 'directo'
        #
        #     dic["prov_conf"] = conf["razon"]["prov_conf"]
        #
        #     if conf["pariente"] is not None:
        #         dic["pariente"] = conf["pariente"]
        #
        #     data.append(dic)
        #
        # # print(data)
        # context["conflictos"] = json.dumps(data)
        # print(context["conflictos"])
        return context


class ClusterView(LoginRequiredMixin,TemplateView):
    template_name = "clustest.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ApiClusterView(LoginRequiredMixin,TemplateView):
    template_name = "api/patrones.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vc = VectorClustering()
        cls = vc.cluster()

        conn = DBconnection()
        clus = conn.get_collection("clusters")
        obj = clus.find_one({})

        #Se eliminan cosas con ObjectID(), ya que causan problemas, y no se usan
        for cluster in obj["clusters"]:
            for conflicto in cluster:
                del conflicto['_id']
                del conflicto['id_declaracion']
                del conflicto['meta']

        print(obj["clusters"])

        context["patrones"] = json.dumps(obj["clusters"])

        return context


class ApiConflictosView(TemplateView):
    template_name = "api/conflictos.html"
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

class ApiDereclaracionView(TemplateView):
    template_name = "api/declaraciones.html"
    conn = DBconnection()
    mycol = conn.get_collection("declaraciones")

    def get_context_data(self, **kwargs):
        # Eso es get, para que sea más seguro, usar POST
        ctx = super().get_context_data()
        ctx['id'] = self.kwargs['id']

        query = self.mycol.find_one({"_id": ObjectId(ctx['id'])})
        query.pop('_id')
        ctx['declaracion'] = json.dumps(query).encode('latin-1').decode('utf-8')

        print(ctx['declaracion'])

        return ctx

