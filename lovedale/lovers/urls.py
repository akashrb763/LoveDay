from lovers import views
from django.urls import path

app_name="lovers"

urlpatterns = [
    path('', views.index,name="index"),
    path('profile/', views.profile,name="profile"),
    path('propose/', views.user_propose,name="propose"),
    
    
]
