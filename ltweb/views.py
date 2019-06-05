from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView
from django.views import View
from pymongo import *
import json


class HomeView(TemplateView):
    template_name = "home.html"
# Create your views here.

class SubirDeclaracionView(View):
    
    context = {}
    initial = {'key': 'value'}
    myclient = MongoClient("mongodb+srv://admin:leytransparente@leytransparente-m6y51.mongodb.net/test?retryWrites=true&w=majority")
    mydb = myclient["leytransparente"]
    mycol = mydb["declaraciones"]
    template_name = 'declaracion_form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        #print('Nombre del diputado: ', request.POST.get('fname'))
        #print('Uploaded file: ', request.FILES['uploaded_file'])
        
        L = ''
        contador = 0

        for chunk in request.FILES['uploaded_file']:

            if(contador != 1 and contador != 2):
                L += chunk.decode(encoding='UTF-8')
                contador += 1

            else:
                contador += 1

        dic = json.loads(L)

        query = self.mycol.find_one({"Datos_del_Declarante.nombre":dic["Datos_del_Declarante"]["nombre"], 
                                    "Datos_del_Declarante.Apellido_Paterno":dic["Datos_del_Declarante"]["Apellido_Paterno"], 
                                    "Datos_del_Declarante.Apellido_Materno":dic["Datos_del_Declarante"]["Apellido_Materno"]})
        
        if query == None: #inserta automaticamente porque no existe nadie.
            self.mycol.insert(dic)

        else: #actualiza el registri por los datos contenidos en el JSON
            self.mycol.update({"Datos_del_Declarante.nombre":dic["Datos_del_Declarante"]["nombre"], 
                                "Datos_del_Declarante.Apellido_Paterno":dic["Datos_del_Declarante"]["Apellido_Paterno"], 
                                "Datos_del_Declarante.Apellido_Materno":dic["Datos_del_Declarante"]["Apellido_Materno"]},
                                dic)

        return redirect('Lista Diputados')

class DiputadosListView(TemplateView):
    
    myclient = MongoClient("mongodb+srv://admin:leytransparente@leytransparente-m6y51.mongodb.net/test?retryWrites=true&w=majority")
    mydb = myclient["leytransparente"]
    mycol = mydb["declaraciones"]
    template_name = 'diputados_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.mycol.find()
        data = []
        
        for par in query:
            dic = {}
            dic['nombres'] = par['Datos_del_Declarante']['nombre']
            dic['apellido_paterno'] = par['Datos_del_Declarante']['Apellido_Paterno']
            dic['apellido_materno'] = par['Datos_del_Declarante']['Apellido_Materno']
            data.append(dic)

        context['diputados'] = data
        return context