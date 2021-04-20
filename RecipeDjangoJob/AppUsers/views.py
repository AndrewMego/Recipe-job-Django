from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import users
from .serializers import userSerializer,  customuserSerializer, loginSerializer
from rest_framework import generics
from django.contrib.auth.models import User
import json
import smtplib
import ssl
import logging
from django.utils.crypto import get_random_string
from django.db import IntegrityError, transaction
from datetime import datetime
from rest_framework.reverse import reverse
from django.utils import timezone
from multiprocessing import connection
from django.http import HttpResponse
from AppJob.models import jobs, locations
# Create your views here.
# @api_view(['POST'])
# class register(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = userSerializer


SERVICE = 'smtp.gmail.com:587'
USERNAME = 'job.Board.hr97@gmail.com'
PASSWORD = 'walaa$$123'


def send_email(fromaddr, toaddrs, msg, username):
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
        server.login(fromaddr, PASSWORD)
        server.ehlo()
        server.sendmail(fromaddr, toaddrs, message.format(
            name=username, link=msg))
        server.quit()
    except:
        logging.critical("cant start connection")


# class registerUser(viewsets.ModelViewSet):
#     serializer_class = userSerializer
#     queryset = User.objects.all()



@api_view(['POST'])
def registerUser(request):
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4")
    print(request.data)
    email = request.data.get('email')
    username = request.data.get('username')
    email_check = User.objects.filter(email=email).count()
    username_check = User.objects.filter(username=username).count()
    if email_check > 0:
        return Response({"msg": "this Email is exist"})

    if username_check > 0:
        return Response({"msg": "this username is exist"})

    try:
        print("########################")
        print(request.data.get('typeUser'))
        if(request.data.get('typeUser') == 'Company'):
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            
            fname =request.data.get('campanyname')
            print(fname)
            lname =request.data.get('campanyname')
            comp =request.data.get('campanyname')
        else:
            fname =request.data.get('first_name')
            lname =request.data.get('last_name')
            comp = None

        print(fname)
        get_user_obj = User.objects.create(
            username=username, email=email, first_name=fname, last_name=lname, password=request.data.get('password'))

        token = get_random_string(length=30)
        filepath = request.data.get('uploadImg') if 'uploadImg' in request.data else False
        if filepath:
            pic = request.data.get('uploadImg')
            print(pic)

        get_users_obj = users.objects.create(customUserID=get_user_obj, phone_number=request.data.get('phone_number'), typeUser=request.data.get(
            'typeUser'), profilePic=pic, creationTime=timezone.now(),companyName = comp ,  isActive=False, token_used_to_active=token)

        link = "http://127.0.0.1:8000/Users/active/"+email+"/"+token
        send_email(USERNAME, email, link, username)
        getuserSerializer = customuserSerializer(get_user_obj)

        obj = ({'userId': get_users_obj,
                'username': get_user_obj.username,
                'email': get_user_obj.email,
                'first_name': get_user_obj.first_name,
                'last_name': get_user_obj.last_name,
                'password': get_user_obj.password,
                'phone_number': get_users_obj.phone_number,
                'typeUser': get_users_obj.typeUser,
                'companyName':get_users_obj.companyName,
                'profilePic': get_users_obj.profilePic })

        return Response({"msg":"success"})

    except IntegrityError as ex:
        transaction.rollback()
        message = ex.args
        return Response({"msg": message})




@api_view(['POST'])
def registerUserCustom(request):

    userID = request.POST['customUserID']
    getUser = User.objects.filter(id=int(userID)).first()
    username = getUser.username
    email = getUser.email

    token = get_random_string(length=30)

    try:
        filepath = request.FILES['profilePic'] if 'profilePic' in request.FILES else False
        if filepath:
            pic = request.FILES["profilePic"]
            print(pic)
        get_user_obj = users.objects.create(customUserID=getUser, phone_number=request.POST['phone'], typeUser=request.POST[
                                            'typeUser'], profilePic=pic, creationTime=timezone.now(), isActive=False, token_used_to_active=token)
        link = "http://127.0.0.1:8000/Users/active/"+email+"/"+token
        send_email(USERNAME, email, link, username)
        getuserSerializer = customuserSerializer(get_user_obj)
        obj = {"getuserSerializer": getuserSerializer}
        return Response(getuserSerializer)

    except IntegrityError as ex:
        transaction.rollback()
        message = ex.args
        return Response({"msg": message})


# # class registerUserCustom(viewsets.ModelViewSet):
#     serializer_class = customuserSerializer
#     queryset = users.objects.all()


def active(request, email, token):
    user = User.objects.filter(email=email).first()
    if user:
        myuser = users.objects.filter(customUserID=user).first()
        if myuser:
            
            datecreate = datetime(myuser.creationTime.year, myuser.creationTime.month, myuser.creationTime.day,
                                  myuser.creationTime.hour, myuser.creationTime.minute, myuser.creationTime.second)
            hour = (datetime.now() - datecreate).total_seconds()/(60*60)
            if token == myuser.token_used_to_active and hour < 24*12:
                myuser.isActive = True
                myuser.save()
                user.is_active = True
                user.save()
                return HttpResponse("done")
            return HttpResponse("expire")


@api_view(['POST'])
def login(request):

    obj = {}

    username = request.data['username']
    password = request.data['password']
    userInfo = User.objects.filter(username=username, password=password )
    if userInfo.count() > 0:

        print("######################################")
        print(userInfo)
        userCustomInfo = users.objects.filter(customUserID=userInfo.first())
        print("######################################")
        print(userCustomInfo)

        if  userCustomInfo.count() > 0:
            obj = ({'userId' : userCustomInfo.first().id ,
                    'username' : userInfo.first().username ,
                    'email' : userInfo.first().email,
                    'first_name' : userInfo.first().first_name,
                    'last_name' : userInfo.first().last_name,
                    'password' : userInfo.first().password,
                    'phone_number' : userCustomInfo.first().phone_number,
                    'typeUser' : userCustomInfo.first().typeUser,
                    }) #'profilePic': userCustomInfo.first().profilePic 



            return Response({'obj': obj})
        else:
            return Response({"msg": "notActive"})

    else:
        return Response({"msg": "no"})

@api_view(['GET'])
def getCompany(request):
    obj = []
    getcomp = users.objects.filter(typeUser ="Company").all()
    if(getcomp.count() > 0):
        for item in getcomp:
          
            getoneCom = User.objects.filter()
            getJob = jobs.objects.filter(userID = item ).count()
            obj.append({'userId' : item.id ,
                     'companyName':item.companyName,
                     'count' : getJob
                    })

    return Response(obj)

    



