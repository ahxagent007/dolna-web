from django.shortcuts import render

# Create your views here.

def home(request):
    request.session['current_page'] = 'Home'

    context = {

    }
    return render(request, 'home/index.html', context)

def About(request):
    request.session['current_page'] = 'About'
    context = {

    }
    return render(request, 'home/about.html', context)

def Contact(request):
    request.session['current_page'] = 'Contact'
    context = {

    }
    return render(request, 'home/contact.html', context)

