from django.urls import path
from django.conf.urls import include
from AppBlog import views
from rest_framework.routers import DefaultRouter

#router=DefaultRouter()
#router.register(r'addBlog',views.addBlog)
#router.register(r'addComment',views.addComment)
#router.register(r'addPhoto',views.PhotcreateoViewSet)
#router.register(r'User/login',views.login)

urlpatterns = [
   
    path('create/',views.create , name="addPhoto" ),
      path('getBlog_with_related_company/',views.getBlog_with_related_company , name="addPhoto" ),
    path('getBlog',views.getBlog  ),
    path('deleteBlog',views.deleteBlog  ),
    path('ubdateBlog',views.ubdateBlog  ),
    path('getOneBlog',views.getOneBlog  ),
      path('sendComment/',views.addComment  ),
]
