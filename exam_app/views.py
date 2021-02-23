from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == "POST":
        errors = User.objects.validate(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            print(pw_hash)
            new_user = User.objects.create(
                name = request.POST["name"], 
                username = request.POST["username"], 
                date_hired = request.POST["date_hired"], 
                password = pw_hash
            )
            request.session['user_id'] = new_user.id
            request.session['name'] = new_user.name
            return redirect("/dashboard")
    return redirect("/")
    

def login(request):
    if not User.objects.authenticate(request.POST['username'], request.POST['password']):
        messages.error(request, "Username or password is incorrect.")
        return redirect("/")
    existing_user = User.objects.get(username = request.POST['username'])
    request.session['user_id'] = existing_user.id
    request.session['name'] = existing_user.name
    return redirect("/dashboard")

def dashboard(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect("/")

    context = {
        'user': User.objects.get( id = request.session['user_id']),
        'products': Product.objects.all()
    } 
    return render(request, "dashboard.html", context)

def additem(request):
    if 'user_id' in request.session:
        if request.method == "POST":
            errors = Product.objects.validate(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect("/additem")
            user = User.objects.get( id = request.session['user_id'])
            new_product = Product.objects.create( item = request.POST['item'], creator = user)
            user.items.add(new_product)
            return redirect("/dashboard")
        context = {
            'user': User.objects.get( id = request.session['user_id'])
        }
        return render(request, "additem.html", context)
    messages.error(request, "You need to register or log in!")
    return redirect("/")

def wishitem(request, product_id):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect("/")

    context = {
        'user': User.objects.all(),
        'product': Product.objects.get(id = product_id)
    } 
    return render(request, "wishitem.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")

def delete(request, product_id):
    if 'user_id' in request.session:
        to_delete = Product.objects.get(id = product_id)
        if to_delete.creator_id == request.session['user_id']:
            to_delete.delete()
    return redirect("/dashboard")
    
def add(request, product_id):
    if 'user_id' in request.session:
        added_item = Product.objects.get (id = product_id)
        user =  User.objects.get(id = request.session['user_id'])
        added_item.users.add(user)
    return redirect("/dashboard")

def remove(request, product_id):
    if 'user_id' in request.session:
        added_item = Product.objects.get (id = product_id)
        user =  User.objects.get(id = request.session['user_id'])
        added_item.users.remove(user)
    return redirect("/dashboard")