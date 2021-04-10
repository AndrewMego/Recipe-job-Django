from django.urls import path
from django.conf.urls import include
from AppUsers import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
#router.register(r'register',views.registerUser)
#router.register(r'User/register',views.registerUserCustom)
#router.register(r'User/login',views.login)

app_name="AppUser"
urlpatterns = [
   
    path('User/login/',views.login , name="login" ),
    path('register',views.registerUser , name="register" ),
    path('User/register',views.registerUserCustom , name="registerCustom" ),
    path('active/<email>/<token>',views.active,name='active'),
     path('',include(router.urls) ),
]


