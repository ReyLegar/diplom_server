from django.shortcuts import render, redirect
from api.models import CustomUser, CreditApplication, Credit
from django.http import HttpResponse
import uuid

def admin_authorization_page(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        personal_code = request.POST['personal_code']

        try:
            admin_user = CustomUser.objects.get(phone_number=phone_number)
            print(admin_user)
            if admin_user.password == password and admin_user.personal_code == personal_code:
                request.session['admin_user_id'] = admin_user.id
                return redirect('admin_home')
            else:
                error_message = 'Неверный номер телефона, пароль или персональный код'
                return render(request, 'admin_authorization.html', {'error_message': error_message})
        except CustomUser.DoesNotExist:
            error_message = 'Неверный номер телефона, пароль или персональный код'
            return render(request, 'admin_authorization.html', {'error_message': error_message})

    return render(request, 'admin_authorization.html')

def admin_home(request):
    users = CustomUser.objects.all()
    return render(request, 'admin_home.html', {'users': users})

def create_user(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        patronymic = request.POST.get('patronymic')
        balance = request.POST.get('balance')
        document_image = request.FILES.get('document_image')
        password = request.POST.get('password')
        
        username = str(uuid.uuid4())
        
        user = CustomUser.objects.create(
            username=username,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            balance=balance,
            document_image=document_image,
            password=password,
        )
        
        return render(request, 'admin_home.html')
    else:
        return render(request, 'create_user.html')
    

from django.shortcuts import render, get_object_or_404
from api.models import CustomUser

def user_info(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'user_info.html', {'user': user})


def credit_applications(request):
    credit_applications = CreditApplication.objects.all()
    return render(request, 'credit_applications.html', {'credit_applications': credit_applications})




