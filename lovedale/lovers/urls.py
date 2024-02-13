from lovers import views
from django.urls import path

app_name="lovers"

urlpatterns = [
    path('', views.index,name="index"),
    path('profile/', views.profile,name="profile"),
    # path('propose/', views.user_propose,name="propose"),
    path('upload/', views.identity, name='upload_file'),
    path('propose/', views.propose, name='propose'),
    path('view/<str:file_name>/', views.view_encrypted_image, name='view_encrypted_image'),
    path('accepte_proposal/<int:prop_id>/', views.accepte_proposal, name='accepte_proposal'),
    path('reject_proposal/<int:prop_id>/', views.reject_proposal, name='reject_proposal'),
    path('verify_paid/', views.pay_verify, name='verify_paid'),
    path('pdf/', views.pdf, name='pdf'),
    path('relationship_agreement_to_pdf/', views.relationship_agreement_to_pdf, name='relationship_agreement_to_pdf'),
    path('user_verify/', views.user_verify, name='user_verify'),

    
    
    
]
