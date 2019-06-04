from django.shortcuts import render, redirect
from django.http import HttpResponse
from pymongo import *
import json

# Create your views here.
def Home(request):
    return render(request, 'home.html')

def SubirDeclaracion(request):
    context = {}

    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient["LeyTransparente"]
    mycol = mydb["Declaraciones"]

    if request.method == 'POST':
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
        mycol.insert(dic)


    return render(request, 'declaracion_form.html', context)