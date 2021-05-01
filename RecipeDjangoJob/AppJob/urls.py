from django.urls import path
from django.conf.urls import include
from AppJob import views
from rest_framework.routers import DefaultRouter

# router=DefaultRouter()
# router.register(r'addJob',views.addJob)
# router.register(r'aplayJob',views.aplayJob)
# router.register(r'User/login',views.login)

urlpatterns = [

    path('addJob', views.addJob, name="jobDetails"),
    path('addJob/jobDetails/', views.jobDetails, name="jobDetails"),
    path('addJob/getLoc/', views.getLoc, name="getLoc"),
    path('addJob/getTag/', views.getTag, name="getTag"),
    path('addJob/getCat/', views.getCat, name="getCat"),
    path('allJobs/', views.allJobs),
    path('search/', views.searchJob, name="search"),
    path('getInfoCat/', views.getInfoCat),
    path('getjob_with_related_Job/', views.getjob_with_related_Job),
    path('jobInfo/', views.jobInfo),
    path('deleteJob/', views.deleteJob),
    path('getjob_with_related_company/', views.getjob_with_related_company),
    path('aplayJob/', views.aplayJob),
    path('getj_ApplayingUser_with_relatedCompany/', views.getj_ApplayingUser_with_relatedCompany),
path('getjob_with_related_ApplayingUser/', views.getjob_with_related_ApplayingUser),
path('acceptUser_ForJob/', views.acceptUser_ForJob),
path('updateJob/', views.updateJob),

    #path('',include(router.urls) ),
]
