from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpRequest
from main.models import Contact
from plants.models import Plant
from django.contrib import messages
from .forms import ContactForm
from django.db.models import Q
# Create your views here.

def home_view(request:HttpRequest):
    #get all posts
    plants = Plant.objects.all()[0:3]
    return render(request,"main/home.html",{"plants":plants})


def contact_view(request:HttpRequest):
    if request.method=="POST":
        contact_form=ContactForm(request.POST)
        if contact_form.is_valid():
              contact_form.save()
              messages.success(request, 'The massege has been send successfully!')
              return redirect("main:contact_view")
        else:
            print("form is not valid")
            print(contact_form.errors)   

    return render(request,"main/contact.html")

    


def messages_view(request:HttpRequest):
    masseges=Contact.objects.all
    if "search" in request.GET and len(request.GET["search"])>=1:
        masseges = Contact.objects.filter(
        Q(first_name__icontains=request.GET["search"]) | Q(last_name__icontains=request.GET["search"]))

        if "order_by" in request.GET and request.GET["order_by"] == "created_at":
            masseges=masseges.order_by("-created_at")

    return render(request,"main/messages.html",{"masseges":masseges})



