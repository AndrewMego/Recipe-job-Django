from django.urls import path
from django.conf.urls import include
from AppBlog import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'addBlog',views.addBlog)
router.register(r'addComment',views.addComment)
#router.register(r'addPhoto',views.PhotcreateoViewSet)
#router.register(r'User/login',views.login)

urlpatterns = [
   
    path('addPhoto/',views.create , name="addPhoto" ),
    path('',include(router.urls) ),
]
