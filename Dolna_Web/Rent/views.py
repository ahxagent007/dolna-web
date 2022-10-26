from django.shortcuts import render

# Create your views here.
def StartRent(request):

    request.session['current_page'] = 'Rent'
    context = {

    }
    return render(request, 'rent/start_rent.html', context)