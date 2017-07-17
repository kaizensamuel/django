# views.py

from django.shortcuts import render, HttpResponse
import requests
import json
from django.contrib.auth.decorators import login_required

from django.shortcuts import render

from forms import ArticuloForm
from django.http import HttpResponseRedirect
from django.views.decorators import csrf
from django.shortcuts import render_to_response
from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@login_required
def index(request):
    return HttpResponse('Hello World!')

def test(request):
    return HttpResponse('My second view!')

def profile(request):
    jsonList = []
    req = requests.get('https://api.github.com/users/odrajaf')
    jsonList.append(json.loads(req.content))
    parsedData = []
    userData = {}
    for data in jsonList:
    	userData['name'] = data['name']
        userData['blog'] = data['blog']
        userData['email'] = data['email']
        userData['public_gists'] = data['public_gists']
        userData['public_repos'] = data['public_repos']
        userData['avatar_url'] = data['avatar_url']
        userData['followers'] = data['followers']
        userData['following'] = data['following']
    parsedData.append(userData)
    return HttpResponse(parsedData)


  

def home(request):
    entradas = Articulos.objects.all()[:10]
    return render_to_response('index.html', {'articulos' : entradas})

@csrf_exempt
def modificar(request):

	if request.method == 'POST':
		form = ArticuloForm(request.POST)

		if form.is_valid():
			client = MongoClient()
			client = MongoClient('mongodb://localhost:27017/')
			db = client['test']
			collection = db['restaurants']

			idResta =  form.cleaned_data['idRestaurante']
			nombreRest = form.cleaned_data['restaurante']
			cocina = form.cleaned_data['tipo']
			ciudad = form.cleaned_data['ciudad']
			direcc = form.cleaned_data['direccion']
			cpostal = form.cleaned_data['cpostal']
			coordX = form.cleaned_data['coordenadax']
			coordY = form.cleaned_data['coordenaday']

			db.restaurants.update(
			{"restaurant_id": idResta},
			   {
			      "address" : {
				 "street" : direcc,
				 "zipcode" : cpostal,
				 "building" : cpostal,
				 "coord" : [ coordX, coordY]
			      },
			      "borough" : ciudad,
			      "cuisine" : cocina,
			      "grades" : [ ],
			      "name" : nombreRest,
			      "restaurant_id" : idResta,
			      
			   })
			
			return render(request, 'restaurantes/modFinal.html', {'restaurante': nombreRest},)
		else:
			return HttpResponse('Error al validar')

def listar(request):

	if request.method == 'GET':
		restaID = request.GET.get('id', '')
		if restaID != '':
			client = MongoClient()
	    		client = MongoClient('mongodb://localhost:27017/')
			db = client['test']
			collection = db['restaurants']
			cursor = collection.find({"restaurant_id":restaID});

			form = ArticuloForm()
			form.fields['idRestaurante'].initial =cursor[0]['restaurant_id']
			form.fields['restaurante'].initial = cursor[0]['name']
			form.fields['tipo'].initial = cursor[0]['cuisine']
			form.fields['ciudad'].initial = cursor[0]['borough']
			form.fields['direccion'].initial = cursor[0]['address']['street']
			form.fields['cpostal'].initial = str(cursor[0]['address']['zipcode'])
			form.fields['coordenadax'].initial = cursor[0]['address']['coord'][0]
			form.fields['coordenaday'].initial = cursor[0]['address']['coord'][1]

			return render_to_response('restaurantes/formulario.html', {'form': form})
			
		
		else:
			client = MongoClient()
		    	client = MongoClient('mongodb://localhost:27017/')
			db = client['test']
			collection = db['restaurants']
			cursor = collection.find().skip(10).limit(10)
			arrayFilas =  []
			for fut in cursor:
				arrayFilas.append(fut)

			return render(request, 'restaurantes/listar.html', {'arrayFilas': arrayFilas},)


