from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import users , company
from .serializers import userSerializer, companySerializer , customuserSerializer ,loginSerializer
from rest_framework import generics
from django.contrib.auth.models  import User
import json
import smtplib, ssl
import logging
from django.utils.crypto import get_random_string
from django.db import IntegrityError, transaction
from datetime  import datetime 
from rest_framework.reverse import reverse
from django.utils import timezone
# Create your views here.
# @api_view(['POST'])
# class register(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = userSerializer


SERVICE ='smtp.gmail.com:587'
USERNAME= 'job.Board.hr97@gmail.com'
PASSWORD='walaa$$123'

def send_email(fromaddr, toaddrs, msg,username):
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$ enter email")
    print(fromaddr)
    print(toaddrs)
    print(msg)
    print(username)
    print(username)
    # Create the plain-text and HTML version of your message
    message = """Subject: Your Active link

    Hi {name}, your link is {link}"""
    try:
    
      #connection = init_connection(SERVICE, USERNAME, PASSWORD)
     
      server = smtplib.SMTP(SERVICE)
      server.ehlo()
      server.starttls()
      server.login(fromaddr,PASSWORD)
      server.ehlo()
      server.sendmail(fromaddr, toaddrs, message.format(name=username,link=msg)) 
      server.quit()
    except:
        logging.critical("cant start connection")



# class registerUser(viewsets.ModelViewSet):
#     serializer_class = userSerializer
#     queryset = User.objects.all() 
   
@api_view(['POST'])
def registerUser(request):
    serializer = userSerializer(request.data)
    email = serializer.data['email']
    username = serializer.data['username']
    email_check=User.objects.filter(email = email).count()
    username_check=User.objects.filter(username = username).count()
    if email_check > 0 :
        return Response ({"msg":"this Email is exist"})

    if username_check > 0 :
        return Response ({"msg":"this username is exist"})    

    try:
        get_user_obj = User.objects.create(username=username,email=email,first_name=serializer.data['first_name'],last_name=serializer.data['last_name'] , password = serializer.data['password']  )    
        getuserSerializer = userSerializer(get_user_obj)
        obj = {"getuserSerializer":getuserSerializer}
        return Response (obj)
       
    except IntegrityError as ex:
            transaction.rollback()
            message = ex.args
            return Response ({"msg": message})

@api_view(['POST'])   
def registerUserCustom(request):
    print("####################00")
    serializer = customuserSerializer(request.data)
    userID = serializer.data['customUserID']
    print(userID)
    getUser = User.objects.filter(id = int(userID) ).first()
    print("####################1")
    username = getUser.username
    email = getUser.email

    token = get_random_string(length=30)

    try:
        print("####################2")
        filepath = request.FILES['profilePic'] if 'profilePic' in request.FILES else False
        if filepath:
            pic = request.FILES["profilePic"] 
            print(pic)
        get_user_obj = users.objects.create(customUserID= getUser,phone_number = serializer.data['phone_number'], typeUser = serializer.data['typeUser'], profilePic = pic , creationTime = timezone.now() ,isActive = False , token_used_to_active = token)    
        print("##############5")
        link="http://127.0.0.1:8000/Users/active/"+email+"/"+token
        print("##############5")
        send_email(USERNAME,email,link,username)
        getuserSerializer = customuserSerializer(get_user_obj)
        obj = {"getuserSerializer":getuserSerializer}
        return Response (getuserSerializer)
     
    except IntegrityError as ex:
            transaction.rollback()
            message = ex.args
            return Response ({"msg":message})
    

# # class registerUserCustom(viewsets.ModelViewSet):
#     serializer_class = customuserSerializer
#     queryset = users.objects.all()


def active(request,email,token):
    user=User.objects.filter(email=email).first()
    if user:
        myuser= users.objects.filter(customUserID=user).first()
        if myuser:
            datecreate =datetime(myuser.creationTime.year,myuser.creationTime.month,myuser.creationTime.day,myuser.creationTime.hour,myuser.creationTime.minute,myuser.creationTime.second)
            hour=(datetime.now()- datecreate).total_seconds()/(60*60)
            if token == myuser.token_used_to_active and hour < 24 :
                myuser.isActive=True
                myuser.save()
                user.is_active=True
                user.save()
                return render()
            return render()    
   


@api_view(['POST'])
def login(request):

    serializer = loginSerializer(request.data)
    username = serializer.data['username']
    password = serializer.data['password']
    userInfo = User.objects.filter(username= username , password=password ).first()
    print("################################################################")
    getuserSerializer = userSerializer(userInfo)
    
    userCustomInfo = users.objects.filter(customUserID = userInfo ).first()
    getuser_CustomSerializer = customuserSerializer(userCustomInfo)
    obj={"userInfo": getuserSerializer.data , "customUserInfo": getuser_CustomSerializer.data}


    return Response(obj)

    

  
## In this case lets say

    
