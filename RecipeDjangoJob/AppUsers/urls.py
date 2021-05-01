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
    path('updateUser',views.updateUser , name="register" ),
   path('updateSkill/',views.updateSkill  ),
     path('getCompany/',views.getCompany  ),
    path('active/<email>/<token>',views.active,name='active'),
     path('',include(router.urls) ),
]


