from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from lovers.forms import CustomUserCreationForm, LoginForm
from lovers.models import CustomUser

from django.conf import settings
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string

from django.contrib import messages

from datetime import datetime,timedelta
from django.utils import timezone

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# Create your views here.




# Generate token with expiration time
def generate_activation_token(user):
    expiration_time = timezone.now() + timedelta(hours=6)  # Token expires after 1 day
    token = default_token_generator.make_token(user)
    print("gen tocken : ",token)
    return token

# Check if token is valid
def token_is_valid(user, token):
    return default_token_generator.check_token(user, token)
def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print("test")
        if form.is_valid():
            # Extract form data
            username = request.POST.get('username')
            phone_number = request.POST.get('phone_number')
            email = request.POST.get('email')
            name = request.POST.get('name')
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            # status = request.POST.get('status')
            # terms_and_conditions = request.POST.get('terms_and_conditions')
            password = request.POST.get('password')
            cpassword = request.POST.get('cpassword')
            print(username)
            # cpassword = request.POST['cpassword']
            if password == cpassword:
                if CustomUser.objects.filter(username=username).exists():
                    messages.info(request, "Username already taken")
                    print(username)
                    return redirect('register:register')
                if CustomUser.objects.filter(email=email, is_active=False).exists():
                    # If the email exists and the associated account is not active
                    user = CustomUser.objects.get(email=email)
                    token = generate_activation_token(user)
                    print(token)
                    send_activation_email(user, token)
                    messages.info(request, "Activation email resent. Please check your email.")
                    return redirect('register:login')
                if CustomUser.objects.filter(email=email).exists():
                    messages.info(request, "Email already registered")
                    print(token)
                    return redirect('register:register')

                # Create new CustomUser instance
                new_user = CustomUser.objects.create_user(
                    username=username,
                    phone_number=phone_number,
                    email=email,
                    name=name,
                    age=age,
                    gender=gender,
                    terms_and_conditions=True,
                    password=password,
                    is_active = False
                )
                token = generate_activation_token(new_user)
                print(token)
                send_activation_email(new_user, token)

                messages.info(request,"Successfully Registered. Please check your email for activation.")
            
            # Redirect to login page after successful registration
                return redirect('accounts:login')
            else:
                messages.info(request, "Passwords do not match")
                return redirect('accounts:register')
            
        else:

            form = CustomUserCreationForm()
            print("test1")
            messages.info(request, "username or email id existing")
            return redirect('accounts:register')


    else:
        form = CustomUserCreationForm()
        print("test1")
        
    return render(request,"user_register.html",{'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        tokens = force_str(urlsafe_base64_decode(token))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and token_is_valid(user, tokens):
        print(user)
        print(user.is_active)
        if user.is_active == True:
            messages.info(request, 'Your account is already activated')
            return redirect('accounts:login')
        user.is_active = True
        user.save()
        messages.info(request, 'Your account has been activated successfully')
        return redirect('accounts:login')
    else:
        messages.info(request, 'Activation link is invalid')
        return redirect('accounts:login')

def send_activation_email(user, token):
    uname=user.username
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    ttoken = urlsafe_base64_encode(force_bytes(token))
    print("enc tocken : ",ttoken)
    # activation_link = f"http://127.0.0.1:8000/accounts/activate/{uid}/{ttoken}"  # Replace with your activation URL
    # message = f"Please click the following link to activate your account: {activation_link}"
    # send_mail(
    #     'Activate Your Account',
    #     message,
    #     settings.DEFAULT_FROM_EMAIL,
    #     [user.email],
    #     fail_silently=False,
    # )

    email_subject="Activate Acoount"
    message=render_to_string('account_activation_link.html',{
            
            'uname':uname,
            'uid':uid,
            'ttoken':ttoken,
            
        })
    print("mail attemptting")
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    email_message = EmailMessage(email_subject,message,email_from,recipient_list)
    print(email_message)
    email_message.content_subtype = "html"
    email_message.send()

def user_logout(request):
    logout(request)
    
    return redirect('lovers:index')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_phone = request.POST.get('username_or_phone')
            password = request.POST.get('password')
            print(username_or_phone)
            print(password)
            user = authenticate(username=username_or_phone, password=password)
            print(user)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                messages.info(request, "login success")

                return redirect('lovers:profile')  # Adjust 'home' to your home URL
            else:
                # Return an 'invalid login' error message.
                messages.info(request, "login invalid credentials")
                return render(request, 'userlogin.html', {'form': form, 'invalid_credentials': True})
    else:
        form = LoginForm()
    return render(request,"userlogin.html", {'form': form})


def user_profile(request):
    return render(render,"user_propose.html")