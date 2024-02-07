from accounts import views
from django.urls import path

app_name="accounts"

urlpatterns = [
    
    path('register/', views.user_register,name="register"),
    path('login/', views.user_login,name="login"),
    # path('profile/', views.user_profile,name="profile"),
    path('accounts/activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('logout/',views.user_logout, name='logout'),
    
    
]
