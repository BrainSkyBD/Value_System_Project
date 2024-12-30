from django.shortcuts import render, redirect
from authenticationApp.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from companyApp.models import CompanyDetailsTable
# Create your views here.

def login_func(request):
    if request.method == "POST":
        log_username = request.POST.get('email')
        log_password = request.POST.get('password')
        # this is for authenticate username and password for login
        user = authenticate(username=log_username, password=log_password)

        if user is not None:
            login(request, user)
            # messages.success(request, "Successfully Logged In !!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Credentials, Please Try Again !!")
            return render(request, "authenticationApp/login.html")

    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, "authenticationApp/login.html")


def signup_func(request):
    if request.method == "POST":
        sign_email = request.POST.get('email')
        sign_password = request.POST.get('password')
        confirm_sign_password = request.POST.get('re_password')
        sign_first_name = request.POST.get('first_name')
        sign_last_name = request.POST.get('last_name')

        # chech the error inputs

        user_username_info = User.objects.filter(username=sign_email)
        user_email_info = User.objects.filter(email=sign_email)

        messages_list = []
        erorr_message = ""

        if user_username_info:
            # messages.error(request, "Username Already Exist")
            erorr_message = "Email Already Exist as User !!"
            messages_list.append(erorr_message)

        elif user_email_info:
            # messages.error(request, "Email Already Exist")
            erorr_message = "Email Already Exist !!"
            messages_list.append(erorr_message)

        elif sign_password != confirm_sign_password:
            # messages.error(request, "Passwords are not match")
            erorr_message = "Passwords are not match !!"
            messages_list.append(erorr_message)

        elif len(sign_password) < 7:
            # messages.error(request, "Passwords Must be Al least 7 Digits")
            erorr_message = "Passwords Must be Al least 7 Digits !!"
            messages_list.append(erorr_message)

        if not erorr_message:

            # create user
            myuser = User.objects.create_user(sign_email, sign_email, sign_password)
            myuser.first_name = sign_first_name
            myuser.last_name = sign_last_name
            myuser.is_active = True
            myuser.save()
            
            var_CompanyDetails = CompanyDetailsTable(
                User=myuser,
                Subscription="Starter",
                Company_Type="Owner",
                Company_Legal_Name=f"{myuser.username}'s Company",  # Default value, can be updated later
                Email=myuser.email,  # Use the user's email as a default
            )
            var_CompanyDetails.save()
            myuser.company_details = var_CompanyDetails
            myuser.save()
            messages.success(request, 'Account Created Successfully !!!')

            return redirect('login_func')

        else:
            value_dic = {'email': sign_email,
                            'first_name': sign_first_name,
                            'last_name': sign_last_name, 'messages': messages_list}
            return render(request, 'authenticationApp/signup.html', value_dic)
    
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, "authenticationApp/signup.html")
    

def logout_func(request):
    logout(request)
    return redirect('login_func')