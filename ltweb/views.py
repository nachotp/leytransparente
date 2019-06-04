from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views import View
from pymongo import *
import json


class HomeView(TemplateView):
    template_name = "home.html"
# Create your views here.

class SubirDeclaracionView(View):
    
    context = {}
    initial = {'key': 'value'}
    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient["LeyTransparente"]
    mycol = mydb["Declaraciones"]
    template_name = 'declaracion_form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        print('Nombre del diputado: ', request.POST.get('fname'))
        print('Uploaded file: ', request.FILES['uploaded_file'])
        L = ''
        contador = 0

        for chunk in request.FILES['uploaded_file']:

            if(contador != 1 and contador != 2):
                L += chunk.decode(encoding='UTF-8')
                contador += 1

            else:
                contador += 1

        dic = json.loads(L)
        self.mycol.insert(dic)

        return render(request, self.template_name, self.context)