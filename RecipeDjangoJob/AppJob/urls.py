from django.urls import path
from django.conf.urls import include
from AppJob import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
#router.register(r'addJob',views.addJob)
#router.register(r'aplayJob',views.aplayJob)
#router.register(r'User/login',views.login)

urlpatterns = [
   
#    path('User/login/',views.login , name="login" ),
    path('',include(router.urls) ),
]


