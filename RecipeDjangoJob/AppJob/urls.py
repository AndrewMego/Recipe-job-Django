from django.urls import path
from django.conf.urls import include
from AppJob import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'addJob',views.addJob)
#router.register(r'aplayJob',views.aplayJob)
#router.register(r'User/login',views.login)

urlpatterns = [
   
    path('addJob/jobDetails/',views.jobDetails , name="jobDetails" ),
    #path('addJob/addCat/',views.addCat , name="addCat" ),
    path('',include(router.urls) ),
]
