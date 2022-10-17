import vehicles
import json
from vehicles.models import Vehicle ,HistoryTask
from django.template import loader
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from django.http import JsonResponse, Http404, HttpResponseBadRequest, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.forms.models import model_to_dict



def index(request):
    vehicles_list = Vehicle.objects.all()
    template = loader.get_template('vehicles/index.html')
    context = {
        'vehicles_list': vehicles_list,
    }
    return HttpResponse(template.render(context, request))

def list(request):
    user = request.user
    userId = user.id
    vehicles_list = [
        {
            "license_plate_number": v.license_plate_number,
            "manufacturer": v.manufacturer,
            "is_available": v.is_available,
            "id":v.id,
            "is_owned_by_me": (not v.is_available) and userId == v.owner.id,
            "owner_username":v.owner.username if v.owner else "" ,
        } for v in Vehicle.objects.all()]
    return JsonResponse(vehicles_list, safe=False)

@csrf_exempt
def occupy(request, vehicle_id):
    user = request.user
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    if not vehicle.is_available:
        return HttpResponseBadRequest("vehicle is not available")
    
    vehicle.owner = user
    vehicle.is_available = False

    vehicle.save()
    add_history_task(vehicle,user,"occupy")
    return HttpResponse("OK")

@csrf_exempt
def release(request, vehicle_id):
    user = request.user
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    if vehicle.is_available:
        return HttpResponseBadRequest("vehicle is already available")
    
    if user.id != vehicle.owner.id:
        return HttpResponseBadRequest("you are not the owner of this vehicle")

    vehicle.owner = None
    vehicle.is_available = True

    vehicle.save()
    add_history_task(vehicle,user,"release")
    return HttpResponse("OK")

def add_history_task(vehicle,user,action):
    h = HistoryTask(user = user ,vehicle = vehicle ,action = action,date = datetime.now())
    h.save()


def history(request,license_plate_number):
   history_tasks = (
        HistoryTask.objects
        .filter(vehicle__license_plate_number = license_plate_number)
        .order_by("-date")
   )

   history_tasks_list = [{
    "date": task.date,
    "user": {
        "id": task.user.id,
        "username": task.user.username,
    },
    "action": task.action,
   } for task in history_tasks]

   return JsonResponse(history_tasks_list, safe=False)

