from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from lovers.forms import CustomUserCreationForm, LoginForm
from .models import CustomUser,UserPropose

from django.core.mail import send_mail,EmailMessage
from PIL import Image

from django.utils import timezone
from datetime import datetime



import os
GTK_FOLDER=r"C:\Program Files\GTK3-Runtime Win64\bin"
os.environ['PATH'] = GTK_FOLDER
from django.template.loader import render_to_string
from weasyprint import HTML

from django.db.models import Q

from django.conf import settings

from cryptography.fernet import Fernet


from django.contrib import messages

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        
        return redirect('lovers:profile')
    
    
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
    user=request.user.username
    propsr=UserPropose.objects.filter((Q(party_a=user) | Q(party_b=user)), accepte=True)
    proposals=UserPropose.objects.filter( (Q(party_a=user) | Q(party_b=user)))
    
    cm_propsr=propsr.count()
    print(cm_propsr)
    
    # print(count_generater)
    
    return render(request,"profile.html" ,{'proposals':proposals,'count_generater':cm_propsr,'generater':propsr})




# Generate a key for encryption and decryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Define the path to store encrypted images
encrypted_images_path = os.path.join(settings.MEDIA_ROOT, 'Id_proof')


def encrypt_file(file_path, encrypted_file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
        encrypted_data = cipher_suite.encrypt(data)
        with open(encrypted_file_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)

def decrypt_file(encrypted_file_path):
    with open(encrypted_file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        return decrypted_data

def identity(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['image']
        file_name = uploaded_file.name

        # Save the uploaded file to a temporary location
        temp_file_path = os.path.join(settings.MEDIA_ROOT, 'temp', file_name)
        with open(temp_file_path, 'wb') as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)

        # Encrypt the uploaded file
        encrypted_file_path = os.path.join(encrypted_images_path, file_name)
        encrypt_file(temp_file_path, encrypted_file_path)

        # Delete the temporary file
        os.remove(temp_file_path)

        return render(request, 'file_uploaded.html', {'file_name': file_name})
    return redirect('user_profile')

def view_encrypted_image(request, file_name):    
    encrypted_file_path = os.path.join(encrypted_images_path, file_name)
    decrypted_data = decrypt_file(encrypted_file_path)
    return HttpResponse(decrypted_data, content_type="image/jpeg")


def propose(request):
    if request.method == 'POST':
        recever = request.POST.get('username')
        sender = request.user.username
        if CustomUser.objects.filter(username=recever).exists():

            print(sender)
            print(recever)
            propose_id = sender + recever
            propose_id2 = recever + sender

            if UserPropose.objects.filter(propose_id=propose_id).exists():
                if UserPropose.objects.filter(propose_id=propose_id2).exists():
                        if UserPropose.objects.filter(propose_id=propose_id,accepet=True).exists():
                            # commited
                            messages.info(request, " You are already committed with this person")
                            return redirect('lovers:profile')

                        elif UserPropose.objects.filter(propose_id=propose_id2,accepet=None).exists():
                            messages.info(request, " You Need to Approve first")
                            return redirect('lovers:profile')
                elif UserPropose.objects.filter(propose_id=propose_id, accepte=None).exists():
                    # Proposal already sent but not accepted
                    print("1")
                    messages.info(request, "Pending for approval")
                    return redirect('lovers:profile')
                elif UserPropose.objects.filter(propose_id=propose_id, accepte=True).exists():
                    # Already committed
                    print("2")
                    messages.info(request, "You are already committed with this person")
                    return redirect('lovers:profile')
                elif UserPropose.objects.filter(propose_id=propose_id, accepte=False).exists():
                    # if UserPropose.objects.filter(propose_id=propose_id,accepte=False):
                        print("3.")
                        prepose=UserPropose.objects.get(propose_id=propose_id,accepte=False)
                        print(prepose.re_props)
                        if prepose.re_props <= 5:
                            prepose.re_props += 1
                            prepose.accepte = None
                            prepose.save()
                            print(prepose.re_props)
                            # preposes=str(prepose)
                            # propose_ids=propose_id+preposes
                            messages.info(request, "Already rejected. Re-send proposal")
                            return redirect('lovers:profile')
                            


                        else:
                            print("3")
                            messages.info(request, "You have reached the proposal limit. Contact support for reset")
                            return redirect('lovers:profile')
                
                
            elif UserPropose.objects.filter(propose_id=propose_id2).exists():
                if UserPropose.objects.filter(propose_id=propose_id).exists():
                        if UserPropose.objects.filter(propose_id=propose_id,accepet=True).exists():
                            # commited
                            messages.info(request, " You are already committed with this person")
                            return redirect('lovers:profile')

                        elif UserPropose.objects.filter(propose_id=propose_id,accepet=None).exists():
                            messages.info(request, " You Need to Approve first")
                            return redirect('lovers:profile')
                elif UserPropose.objects.filter(propose_id=propose_id2, accepte=None).exists():
                    # Proposal already sent but not accepted
                    print("1.2")
                    messages.info(request, "Pending for approval")
                    return redirect('lovers:profile')
                elif UserPropose.objects.filter(propose_id=propose_id2, accepte=True).exists():
                    # Already committed
                    print("2.2")
                    messages.info(request, "You are already committed with this person")
                    return redirect('lovers:profile')

                elif UserPropose.objects.filter(propose_id=propose_id2,accepet=False ).exists():
                    

                        print("3.2")
                        prepose=UserPropose.objects.get(propose_id=propose_id2,accepte=False)
                        if prepose.re_props <= 5:
                            prepose.re_props += 1
                            prepose.accepte = None
                            prepose.save()
                            messages.info(request, "Already rejected. Re-send proposal")
                            return redirect('lovers:profile')
                        # if UserPropose.objects.filter(propose_id=propose_id).exists():
                        #     if UserPropose.objects.filter(propose_id=propose_id,accepte=True).exists():
                        #         messages.info(request, " You are already committed with this person")
                        #         return redirect('lovers:profile')
                                    # print(prepose.re_props)
                                    # if prepose.re_props <= 5:
                                    #     prepose.re_props += 1
                                    #     prepose.accepte = None
                                    #     prepose.save()
                                    #     print(prepose.re_props)
                                        # preposes=str(prepose)
                                        # propose_ids=propose_id+preposes
                            # UserPropose.objects.filter(propose_id=propose_id).exists():
                        else:
                            print("3.4")
                            messages.info(request, "Already rejected. Re-send proposal")
                            return redirect('lovers:profile')            

                            # if UserPropose.objects.filter(propose_id=propose_id,accepte=False).exists():
                            #     if prepose.re_props <= 5:
                                    
                            #         prepose.accepte = None
                            #         prepose.save()

                                    
                            #         messages.info(request, "Already rejected. Re-send proposal")
                            #         return redirect('lovers:profile')                
                                                    
                    # elif UserPropose.objects.filter(propose_id=propose_id2,accepte=None).exists():
                    #     messages.info(request, "Pending for approval")
                    #     return redirect('lovers:profile')

                    # else:
                    #     messages.info(request, "You are already committed with this person")
                    #     return redirect('lovers:profile')
                    # elif UserPropose.objects.filter(propose_id=propose_id2,accepte=True).exists():
                    #     messages.info(request, " You are already committed with this person")
                    #     return redirect('lovers:profile')
                    #         else:
                    #             print("4")
                    #             messages.info(request, "You have reached the proposal limit. Contact support for reset")
                    #             return redirect('lovers:profile')

            else:
                print("5.4")
                UserPropose.objects.create(party_a=sender, party_b=recever, propose_id=propose_id)
                messages.info(request, "Proposal sent")
                return redirect('lovers:profile')
        else:
                print("6.5")
                messages.info(request, "username not fount")
                return redirect('lovers:profile')
        
    # return render(request,"prose.html")
        
def accepte_proposal(request,prop_id):
    prop=UserPropose.objects.get(id=prop_id)
    if prop.accepte == None:
        prop.accepte= True
        prop.save()

    return redirect('lovers:profile')

def reject_proposal(request,prop_id):
    prop=UserPropose.objects.get(id=prop_id)
    if prop.accepte == None:
        prop.accepte= False
        prop.save()

    return redirect('lovers:profile')


def pay_verify(request):
    user=request.user
    try:
        user.verify_paid = True
        messages.info(request,"payment Success")
    except:
        messages.info(request,"somthing went wrong,contact support")
    return redirect('lovers:profile')




def relationship_agreement_to_pdf(request):
    if request.method == 'POST':

        partner=request.POST.get('partner')
        partners_sig=request.FILES.get('partnersSignature')
        your_sig=request.FILES.get('yourSignature')
        users=request.user.username
        print(partner,"ids")

        props=CustomUser.objects.get(username=partner)
        part=props.username
        print(part)

        if UserPropose.objects.filter((Q(party_a=users) | Q(party_b=partner) | Q(party_a=users) | Q(party_b=partner)), accepte=True).exists():
            # partners=CustomUser.objects.get(username=partner)
            # if partners.gender == "Male":
            #     boy=partners.gender
            # elif partners.gender == "Male"
            u_props=UserPropose.objects.get((Q(party_a=partner) | Q(party_b=partner)), accepte=True)
            u_props.sing_1=your_sig
            u_props.sing_2=partners_sig
            u_props.save()
        
            boy_name= request.user.name

            # Sample data
            girl_name = props.name
            
            date = datetime.now()

            # Render HTML template with data
            html_string = render_to_string('relationship_agreement.html', {'girl_name': girl_name, 'boy_name': boy_name, 'date': date,'u_props':u_props })

            # Create PDF from HTML string
            # pdf_file = HTML(string=html_string).write_pdf()
            html = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

            # Set response type as PDF
            response = HttpResponse(html, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="love_agreement.pdf"'

            return response
    else:
        messages.info(request,"somthing went wrong")
        return redirect('lovers:profile')


def pdf(requst):
    return render(requst,"relationship_agreement.html")

def user_verify(requiest):
    user=requiest.user


    if requiest.method =='POST':
        identity=requiest.FILES.get('identity')

        uname= user.name
        u_username=user.username
        u_age=user.age
        u_gender=user.gender
        u_phone_number=user.phone_number
        u_email=user.email
        u_id=user.pk
        email_subject="Activate Acoount"
        message=render_to_string('user_verify.html',{
            
            'uname':uname,
            'u_username':u_username,
            'u_age':u_age,
            'u_gender':u_gender,
            'u_phone_number':u_phone_number,
            'u_email':u_email,
            'u_id':u_id,
            
            
        })
        print("mail attemptting")
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['akashrb763@gmail.com']

        email_message = EmailMessage(email_subject,message,email_from,recipient_list)
        
        print(email_message)
        email_message.content_subtype = "html"
        if identity:  # Check if identity file exists
            email_message.attach(identity.name, identity.read(), identity.content_type)
        email_message.send()
        
        
    messages.info(requiest,"it will take 24 hrs")


    return redirect('lovers:profile')

    
    
    