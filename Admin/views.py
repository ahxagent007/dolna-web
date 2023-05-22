import hashlib
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from io import BytesIO
from PIL import Image
from django.core.files import File
import os

from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect

# Create your views here.
from django.views.decorators.csrf import csrf_protect
from User.models import *
from Rent.models import *




def Dashboard(request):
    if 'VisitorStatus' not in request.session or request.session['VisitorStatus'] != "ADMIN":
        return redirect('Admin:Login')
    admin_name = "ADMIN"
    if "AdminName" in request.session:
        name_id = UserAccount.objects.get(id = request.session["AdminID"] )
        admin_name = name_id.name

    rider = Rider.objects.all()
    driver = Driver.objects.all()

    context = {
        'admin_name': admin_name,
        'rider': rider.count(),
        'driver' : driver.count(),
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


#Image compressor and saver
def rider_image_compress_save(image, img_name):
    im = Image.open(image)  # or self.files['image'] in your form
    # destroy color pew pew
    im = im.convert('RGB')
    im_io = BytesIO()
    im.save(im_io, 'JPEG', quality=60)
    compressed_image = File(im_io, name=img_name)
    print(settings.STATIC_URL)
    print(settings.STATIC_ROOT)
    print(settings.STATICFILES_DIRS[0])
    FileSystemStorage(location=os.path.join(settings.STATICFILES_DIRS[0], 'UPLOAD', 'rider')).save(img_name,
                                                                                                    compressed_image)

@csrf_protect
def Add_Rider(request):
    if 'VisitorStatus' not in request.session or request.session['VisitorStatus'] != "ADMIN":
        return redirect('Admin:Login')

    if request.method == 'POST':
        # Login user
        data = request.POST
        if Rider.objects.filter(Phone = '+88'+data['phone']).exists():
            context = {
                'msg' : "Phone number already exist"
            }
            return render(request, 'admin/add_rider.html', context)


        rider_name = data['name'].replace(' ', '_')

        img_new_name = rider_name+'_'+'.jpg'
        rider_image_compress_save(request.FILES['picture'], img_new_name)

        new_rider = Rider(Name=data['name'], Phone='+88'+data['phone'], Email=data['email'],
                            Address=data['address'],Gender=data['gender'],DateOfBirth=data['DoB'],Photo=img_new_name,FirebaseID=data['FirebaseID'])


        new_rider.save()

        return redirect('Admin:All_Rider')

    else:
        request.session['current_page'] = 'AdminLogin'

        context = {

        }
        return render(request, 'admin/add_rider.html', context)


@csrf_protect
def Edit_Rider(request, rider_id):
    if 'VisitorStatus' not in request.session or request.session['VisitorStatus'] != "ADMIN":
        return redirect('Admin:Login')

    if request.method == 'POST':
        rider = Rider.objects.get(pk=int(rider_id))
        pic = rider.Photo
        print(rider)
        data = request.POST

        if request.FILES.get('picture') != None:
            rider_name = data['name'].replace(' ', '_')
            img_new_name = rider_name+'_'+data['phone']+'.jpg'

            try:
                os.remove('static/UPLOAD/rider/{}'.format(pic))
            except:
                pass

            rider_image_compress_save(request.FILES['picture'], img_new_name)
            print(img_new_name)


            rider.Photo = img_new_name
            rider.Name = data['name']
            rider.Phone = '+88' + data['phone']
            rider.Address = data['address']
            rider.Email = data['email']
            rider.Gender = data['gender']
            rider.DateOfBirth = data['DoB']
            rider.FirebaseID = data['FirebaseID']
            rider.save()

            return redirect('Admin:All_Rider')


        else:

            rider.Name = data['name']
            rider.Phone = '+88' + data['phone']
            rider.Address = data['address']
            rider.Email = data['email']
            rider.Gender = data['gender']
            rider.DateOfBirth = data['DoB']
            rider.FirebaseID = data['FirebaseID']
            rider.Photo = rider.Photo
            rider.save()

        context = {
            'rider_id': rider_id,
            'rider': rider,
        }
        return render(request, 'admin/edit_rider.html', context)

    else:
        # Login user
        print(rider_id)
        request.session['current_page'] = 'Edit Rider Admin'
        rider = Rider.objects.get(pk=int(rider_id))

        if rider.Phone.startswith('88'):
            rider.Phone = rider.Phone[2:]
        elif rider.Phone.startswith('+88'):
            rider.Phone = rider.Phone[3:]
        context = {
            'rider_id': rider_id,
            'rider': rider,
        }
        print(rider.Name)
        return render(request, 'admin/edit_rider.html', context)


def Delete_Rider(request, rider_id):
    if 'VisitorStatus' not in request.session or request.session['VisitorStatus'] != "ADMIN":
        return redirect('Admin:Login')


    rider = Rider.objects.get(pk=int(rider_id))

    pic = rider.Photo
    os.remove('static/UPLOAD/rider/{}'.format(pic))

    rider.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def All_Rider(request):
    if 'VisitorStatus' not in request.session or request.session['VisitorStatus'] != "ADMIN":
        return redirect('Admin:Login')


    rider = Rider.objects.all()

    context = {
        'rider' : rider,
    }
    return render(request, 'admin/all_rider.html', context)



#Image compressor and saver
def driver_image_compress_save(image, img_name,f_name):
    im = Image.open(image)  # or self.files['image'] in your form
    # destroy color pew pew
    im = im.convert('RGB')
    im_io = BytesIO()
    im.save(im_io, 'JPEG', quality=60)
    compressed_image = File(im_io, name=img_name)
    print(settings.STATIC_URL)
    print(settings.STATIC_ROOT)
    print(settings.STATICFILES_DIRS[0])
    FileSystemStorage(location=os.path.join(settings.STATICFILES_DIRS[0], 'UPLOAD', 'driver',f_name)).save(img_name,
                                                                                                    compressed_image)


@csrf_protect
def Add_Driver(request):
    if 'VisitorStatus' not in request.session or request.session['VisitorStatus'] != "ADMIN":
        return redirect('Admin:Login')

    if request.method == 'POST':
        # Login user
        data = request.POST
        if Driver.objects.filter(Phone = '+88'+data['phone']).exists():
            context = {
                'msg' : "Phone number already exist"
            }
            return render(request, 'admin/add_driver.html', context)


        driver_name = data['name'].replace(' ', '_')

        img_new_name = driver_name+'_'+'.jpg'

        new_driver = Driver(Name=data['name'], Phone='+88'+data['phone'], Email=data['email'],
                            Address=data['address'],NID=data['NID'],Photo=img_new_name,FirebaseID=data['FirebaseID'])


        new_driver.save()

        driver = Driver.objects.last()
        f_name = driver.ID

        driver_image_compress_save(request.FILES['picture'], img_new_name,str(f_name))


        return redirect('Admin:All_Driver')

    else:
        request.session['current_page'] = 'AdminLogin'

        context = {

        }
        return render(request, 'admin/add_driver.html', context)

@csrf_protect
def Edit_Driver(request, driver_id):
    if 'VisitorStatus' not in request.session or request.session['VisitorStatus'] != "ADMIN":
        return redirect('Admin:Login')

    if request.method == 'POST':
        driver = Driver.objects.get(pk=int(driver_id))
        pic = driver.Photo
        print(driver)
        data = request.POST

        if request.FILES.get('picture') != None:
            driver_name = data['name'].replace(' ', '_')
            img_new_name = driver_name+'_'+data['phone']+'.jpg'

            try:
                os.remove('static/UPLOAD/driver/{}'.format(pic))
            except:
                pass

            driver_image_compress_save(request.FILES['picture'], img_new_name)
            print(img_new_name)


            driver.Photo = img_new_name
            driver.Name = data['name']
            driver.Phone = '+88' + data['phone']
            driver.Address = data['address']
            driver.Email = data['email']
            driver.NID = data['NID']
            driver.FirebaseID = data['FirebaseID']
            driver.save()

            return redirect('Admin:All_Driver')


        else:

            driver.Name = data['name']
            driver.Phone = '+88' + data['phone']
            driver.Address = data['address']
            driver.Email = data['email']
            driver.NID = data['NID']
            driver.FirebaseID = data['FirebaseID']
            driver.Photo = driver.Photo
            driver.save()

        context = {
            'driver_id': driver_id,
            'driver': driver,
        }
        return render(request, 'admin/edit_driver.html', context)

    else:
        # Login user
        print(driver_id)
        request.session['current_page'] = 'Edit Driver Admin'
        driver = Driver.objects.get(pk=int(driver_id))

        if driver.Phone.startswith('88'):
            driver.Phone = driver.Phone[2:]
        elif driver.Phone.startswith('+88'):
            driver.Phone = driver.Phone[3:]
        context = {
            'driver_id': driver_id,
            'driver': driver,
        }
        print(driver.Name)
        return render(request, 'admin/edit_driver.html', context)


def Delete_Driver(request, driver_id):
    if 'VisitorStatus' not in request.session or request.session['VisitorStatus'] != "ADMIN":
        return redirect('Admin:Login')


    driver = Driver.objects.get(pk=int(driver_id))

    pic = driver.Photo
    os.remove('static/UPLOAD/driver/{}'.format(pic))

    driver.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def All_Driver(request):
    if 'VisitorStatus' not in request.session or request.session['VisitorStatus'] != "ADMIN":
        return redirect('Admin:Login')


    driver = Driver.objects.all()

    context = {
        'driver' : driver,
    }
    return render(request, 'admin/all_driver.html', context)


def car_image_compress_save(image, img_name,f_name):
    im = Image.open(image)  # or self.files['image'] in your form
    # destroy color pew pew
    im = im.convert('RGB')
    im_io = BytesIO()
    im.save(im_io, 'JPEG', quality=60)
    compressed_image = File(im_io, name=img_name)
    print(settings.STATIC_URL)
    print(settings.STATIC_ROOT)
    print(settings.STATICFILES_DIRS[0])
    FileSystemStorage(location=os.path.join(settings.STATICFILES_DIRS[0], 'UPLOAD', 'driver',f_name)).save(img_name,
                                                                                                    compressed_image)



@csrf_protect
def Add_Car(request,driver_id):
    if 'VisitorStatus' not in request.session or request.session['VisitorStatus'] != "ADMIN":
        return redirect('Admin:Login')

    if request.method == 'POST':

        data = request.POST

        image = request.FILES.getlist('pictures')
        n = 0
        ar = []

        for i in image:
            n = n + 1
            title_name = data['Model'].replace(' ', '_')
            image_new_name_multi = title_name + "_" + str(n) + '.jpg'
            ar.append(image_new_name_multi)
            car_image_compress_save(i, image_new_name_multi, str(driver_id))

        new_car = Car(DriverID=driver_id, Type=data['Type'], Color=data['Color'],
                            RegistrationNumber=data['RegistrationNumber'],isAC=data['isAC'],Condition=data['Condition'],Pictures=ar,Model=data['Model'])


        new_car.save()

        return redirect('Admin:All_Driver')

    else:
        request.session['current_page'] = 'EditCar'


        car = Car.objects.filter(DriverID = driver_id)

        if Car.objects.filter(DriverID = driver_id).count() == 1:
            print(2)

            return redirect('Admin:Edit_Car' , driver_id=driver_id)

        else:
            print(5)

            context = {
                'driver_id':driver_id
            }
            return render(request, 'admin/add_car.html', context)



@csrf_protect
def Edit_Car(request, driver_id):
    if 'VisitorStatus' not in request.session or request.session['VisitorStatus'] != "ADMIN":
        return redirect('Admin:Login')


    if request.method == 'POST':
        car = Car.objects.get(DriverID=int(driver_id))
        data = request.POST

        if request.FILES.get('pictures') != None:

            image = request.FILES.getlist('pictures')
            n = 50
            ar = []

            for i in image:
                n = n + 1
                title_name = data['Model'].replace(' ', '_')
                image_new_name_multi = title_name + "_" + str(n) + '.jpg'
                ar.append(image_new_name_multi)
                car_image_compress_save(i, image_new_name_multi, str(driver_id))


            car.Pictures = ar
            car.Model = data['Model']
            car.Type = data['Type']
            car.Color = data['Color']
            car.RegistrationNumber = data['RegistrationNumber']
            car.isAC = data['isAC']
            car.Condition = data['Condition']
            car.save()

            return redirect('Admin:All_Driver')


        else:

            car.Pictures = car.Pictures
            car.Model = data['Model']
            car.Type = data['Type']
            car.Color = data['Color']
            car.RegistrationNumber = data['RegistrationNumber']
            car.isAC = data['isAC']
            car.Condition = data['Condition']
            car.save()


        return redirect('Admin:All_Driver')


    else:
        request.session['current_page'] = 'Edit Car Admin'
        car = Car.objects.get(DriverID=int(driver_id))

        context = {
            'driver_id': driver_id,
            'car': car,
        }
        return render(request, 'admin/edit_car.html', context)


def Delete_Car(request, car_id):
    if 'VisitorStatus' not in request.session or request.session['VisitorStatus'] != "ADMIN":
        return redirect('Admin:Login')

    car_details = Car.objects.get(pk=int(car_id))

    car = Car.objects.values_list('Pictures',flat=True).get(pk=int(car_id))

    dict = {}


    car = car.strip('][').split(', ')


    for i in range(len(car)):
        y = car[i].replace("'", "")
        dict[i] = y

    for i in dict.values():

        os.remove('static/UPLOAD/driver/{}/{}'.format(car_details.DriverID,i))

    car_details.delete()

    return redirect('Admin:All_Driver')