from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpRequest
from django.contrib import messages
from .models import Plant
from .forms import PlantForm
from django.core.paginator import Paginator
# Create your views here.

def all_plants_view(request:HttpRequest):
    plants = Plant.objects.all()

    p=Paginator(Plant.objects.all(),6)
    page=request.GET.get('page')
    plants_list=p.get_page(page)

    return render(request, "plants/all_plants.html",{"plants":plants,'plants_list':plants_list})


def plants_details_view(request:HttpRequest,plant_id:int):
    try:
        plant=Plant.objects.get(pk=plant_id)
        related_plants=Plant.objects.filter(category=plant.category)[0:4]
        print(related_plants)
        return render(request,'plants/plants_details.html',{"plant":plant,"related_plants":related_plants})
    except Plant.DoesNotExist:
        print("error massege")
        messages.error(request, "An error occurred: The page not found")
        return redirect('main:home_view')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('main:home_view')



def search_view(request:HttpRequest):
    
    plants=Plant.objects.all()
    if "search" in request.GET and len(request.GET["search"])>=1:
        plants=Plant.objects.filter(name__contains=request.GET["search"])

    if "order_by" in request.GET:
        if request.GET["order_by"] == "created_at":
            plants = plants.order_by("-created_at")
        elif request.GET["order_by"] == "edible":
            plants = plants.filter(is_edible=True)
        elif request.GET["order_by"] == "not_edible":
            plants = plants.filter(is_edible=False)       

    p=Paginator(plants,6)
    page=request.GET.get('page')
    plants_list=p.get_page(page)

    return render(request, "plants/search_plants.html",{"plants":plants,"plants_list":plants_list})


def add_plant_view(request:HttpRequest):

    if request.method=="POST":
        plant_form=PlantForm(request.POST,request.FILES)
        if plant_form.is_valid():
              plant_form.save()
              messages.success(request, 'The plant has been added successfully!')
              return redirect("plants:add_plant_view")
        else:
            print("form is not valid")
            print(plant_form.errors)   

    return render(request, "plants/add_plant.html",{"CategoryChoices":Plant.CategoryChoices.choices})



def update_plant_view(request:HttpRequest,plant_id):

    try:
        plant=Plant.objects.get(pk=plant_id)
        if request.method=="POST":
            plant_form=PlantForm(request.POST,request.FILES,instance=plant)
            if plant_form.is_valid():
                plant_form.save()
                messages.success(request, 'The plant has been updated successfully!')
                return redirect('plants:update_plant_view',plant_id=plant.id)
            else:
                print("form is not valid")
                print(plant_form.errors)
                return redirect('main:home_view') 
        else:   
            plant_form = PlantForm(instance=plant)
        return render(request, "plants/update_plant.html",{"plant":plant, "CategoryChoices":Plant.CategoryChoices.choices})                

    except Plant.DoesNotExist:
        print("error massege")
        messages.error(request, "An error occurred: The page not found")
        return redirect('main:home_view')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('main:home_view')
    
def delete_plant_view(request:HttpRequest, plant_id):
    try:
        plant=Plant.objects.get(pk=plant_id)
        plant.delete()
        return redirect("main:home_view")
    except Plant.DoesNotExist:
        print("error massege")
        messages.error(request, "An error occurred: The page not found")
        return redirect('main:home_view')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('main:home_view')

        

