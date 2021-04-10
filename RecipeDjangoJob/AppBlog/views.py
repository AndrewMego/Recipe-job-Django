from django.shortcuts import render
from AppBlog.models import Blog , comments , blogImg
from .serializers import blogSerializer , commentSerializer , FileListSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser , FormParser

# Create your views here.


class addBlog(viewsets.ModelViewSet):
    serializer_class = blogSerializer
    queryset = Blog.objects.all()

class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = FileListSerializer
    parser_classes = (MultiPartParser, FormParser,)
    queryset=blogImg.objects.all()
      
@api_view(['POST'])
def create(request):
        photos=[]
        blogs=request.POST['blogID']
        filepath = request.FILES.getlist('blogimg') if 'blogimg' in request.FILES else False
        for file in filepath:  
            photo = blogImg.objects.create(blogID=Blog.objects.get(id=int(blogs)) , blogimg=file)
            photos.append(photo)
        p_ser = FileListSerializer(photos , many=True)
      
        return Response (p_ser.data )



class addComment(viewsets.ModelViewSet):
    serializer_class = commentSerializer
    queryset = comments.objects.all()    