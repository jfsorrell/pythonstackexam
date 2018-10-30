from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Quote, Like

def index(req):
    return render(req, 'quotes/index.html')

def create(req):
    errors = User.objects.validate(req.POST)
    if len(errors) > 0:
        for error in errors:
            messages.error(req, error)
        return redirect('/')
    else:
        user = User.objects.create_user(req.POST)
        print(user)
        req.session['user_id'] = user.id
    return redirect('/allquotes')
    

def login(req):
    if req.method != 'POST':
        return redirect('quotes:index')

    valid, response = User.objects.login(req.POST)
    if valid == True:
        req.session['user_id'] = response
        return redirect("quotes:allquotes")
    else:
        messages.error(req, response)

    return redirect("quotes:index")

def logout(req):
  req.session.clear()
  return redirect('quotes:index')
    

def edit(req):
    user = User.objects.get(id=req.session['user_id'])
    user.first_name = req.POST['first_name']
    user.last_name = req.POST['last_name']
    user.email = req.POST['email']
    user.save()
    return redirect('quotes:allquotes')

def likes(req):
    pass

def delete(req, id):
    Quote.objects.get(id=id).delete()
    return redirect('quotes:allquotes')

def allquotes(req):
    context = {
        "user" : User.objects.get(id=req.session['user_id']),
        "quotes" : Quote.objects.all(),

    }
    return render(req, 'quotes/allquotes.html', context)

def addquote(req):
    errors = Quote.objects.validate(req.POST)

    if len(errors) > 0:
        for error in errors:
            messages.error(req, error)
        return redirect('/allquotes')
    else:
        user = User.objects.get(id=req.POST['user'])
        quote = Quote.objects.create(quote =req.POST['quote'], author = req.POST['author'], user = user)
        print(quote)
    return redirect('/allquotes')
    

def userquotes(req, id):
    context = {
        "username" : User.objects.filter(id=id),
        "userquotes" : Quote.objects.filter(user_id = id)
    }

    print(Quote.objects.filter(id = id))
    return render(req, 'quotes/userquotes.html', context)
    
def myaccount(req, id):
    context = {
        "user" : User.objects.get(id=req.session['user_id']),

    }
    return render(req, 'quotes/myaccount.html', context)








# Create your views here.
