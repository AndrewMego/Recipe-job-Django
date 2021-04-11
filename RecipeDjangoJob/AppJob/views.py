from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .serializers import jobSerializer
from AppJob.models import category, jobs, tags, tagsJob
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from django.http import request

# Create your views here.
class addJob(viewsets.ModelViewSet):
    serializer_class = jobSerializer
    queryset = jobs.objects.all()



@api_view(['POST'])   
def jobDetails(request):
    print("########################")
    print(request)
    Tags =request.POST['tags']
    get_jobID =request.POST['jobID']
    for tag in Tags: 
        tagsJob.objects.create(tagID=tags.objects.get(id=int(tag)), jobID=jobs.objects.get(id=get_jobID)  )
    

    if request.POST['otherTags']:
        print("&&&&&&&&&&&&   true")
        otherTag = request.POST.getlist('otherTags') if 'otherTags' in request.POST else False
        for tag in otherTag:
              currentTag = tags.objects.create(tag= tag)
              tagsJob.objects.crea
