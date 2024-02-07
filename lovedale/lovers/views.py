from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from lovers.forms import CustomUserCreationForm, LoginForm
from .models import CustomUser

from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,"index.html")

# def user_register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             # Extract form data
#             username = request.POST.get('username')
#             phone_number = request.POST.get('phone_number')
#             email = request.POST.get('email')
#             name = request.POST.get('name')
#             age = request.POST.get('age')
#             # status = request.POST.get('status')
#             terms_and_conditions = request.POST.get('terms_and_conditions')
#             password = request.POST.get('password')
#             print(terms_and_conditions)

#             # Create new CustomUser instance
#             new_user = CustomUser.objects.create_user(
#                 username=username,
#                 phone_number=phone_number,
#                 email=email,
#                 name=name,
#                 age=age,
#                 # status=status,
#                 terms_and_conditions=terms_and_conditions,
#                 password=password
#             )
#             messages.info(request,"register success")
#             # Redirect to login page after successful registration
#             return redirect('lovers:login')
#     else:
#         form = CustomUserCreationForm()
#     return render(request,"user_register.html",{'form': form})

# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username_or_phone = request.POST.get('username_or_phone')
#             password = request.POST.get('password')
#             print(username_or_phone)
#             print(password)
#             user = authenticate(username=username_or_phone, password=password)
#             print(user)
#             if user is not None:
#                 login(request, user)
#                 # Redirect to a success page.
#                 messages.info(request, "login success")

#                 return redirect('lovers:profile')  # Adjust 'home' to your home URL
#             else:
#                 # Return an 'invalid login' error message.
#                 messages.info(request, "login invalid credentials")
#                 return render(request, 'userlogin.html', {'form': form, 'invalid_credentials': True})
#     else:
#         form = LoginForm()
#     return render(request,"userlogin.html", {'form': form})


def user_propose(request):
    return render(request,"account_activation_link.html")

def profile(request):
    print(request.user.username)
    
    return render(request,"profile.html")