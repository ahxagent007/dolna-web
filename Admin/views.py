import hashlib

from django.shortcuts import render,redirect

# Create your views here.
from django.views.decorators.csrf import csrf_protect
from User.models import UserAccount



def Dashboard(request):
    if 'VisitorStatus' not in request.session or request.session['VisitorStatus'] != "ADMIN":
        return redirect('Admin:Login')
    admin_name = "ADMIN"
    if "AdminName" in request.session:
        name_id = UserAccount.objects.get(id = request.session["AdminID"] )
        admin_name = name_id.name
    context = {
        'admin_name': admin_name,
        'rider': 20,
        'driver' : 50,
        'staff': 100,
    }
    return render(request, 'admin/dashboard.html',context)


@csrf_protect
def Login(request):
    if request.method == 'POST':
        # Login user
        data = request.POST
        print(data)
        email = data['username']
        password = hashlib.md5(data['password'].encode('utf-8')).hexdigest()

        exists = UserAccount.objects.filter(email=email).exists()

        if not exists:
            # show message ('This admin does not exist')
            print('This admin does not exist')
            return redirect('Admin:Login')
        admin = UserAccount.objects.get(email=email)

        if not 'ADMIN' in admin.get_role_list():
            print('Access Denied')
            return redirect('Admin:Login')
        if admin.password != password:
            # show message ('Wrong Password. Please Check Again')
            print('Wrong Password. Please Check Again')
            return redirect('Admin:Login')

        request.session['VisitorStatus'] = admin.role
        request.session["AdminID"] = admin.id
        request.session["AdminName"] = admin.name

        return redirect('Admin:Dashboard')
    else:
        request.session['current_page'] = 'AdminLogin'

        context = {

        }
        return render(request, 'admin/login.html', context)
