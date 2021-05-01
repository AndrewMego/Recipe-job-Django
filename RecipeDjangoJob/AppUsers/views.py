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
import shutil
import os
import urllib.request
import os
from urllib.parse import urlparse


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

        # connection = init_connection(SERVICE, USERNAME, PASSWORD)

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

    email = request.data.get('email')
    username = request.data.get('username')
    email_check = User.objects.filter(email=email).count()
    username_check = User.objects.filter(username=username).count()
    if email_check > 0:
        return Response({"msg": "this Email is exist"})

    if username_check > 0:
        return Response({"msg": "this username is exist"})

    try:

        if(request.data.get('typeUser') == 'Company'):

            fname = request.data.get('campanyname')
            lname = request.data.get('campanyname')
            comp = request.data.get('campanyname')
        else:
            fname = request.data.get('firstname')
            lname = request.data.get('lastname')
            comp = None

        get_user_obj = User.objects.create(
            username=username, email=email, first_name=fname, last_name=lname, password=request.data.get('password'))

        token = get_random_string(length=30)

        filepath = request.FILES['profile'] if 'profile' in request.FILES else False

        if filepath:
            pic = filepath

        get_users_obj = users.objects.create(customUserID=get_user_obj, phone_number=request.data.get('phone'), typeUser=request.data.get(
            'typeUser'), profilePic=pic, creationTime=timezone.now(), companyName=comp,  isActive=False, token_used_to_active=token, location=request.data.get('location'),
            fieldCompany=request.data.get('fieldCompany'),
            gitAccount=request.data.get('gitAccount'),
            gitInsta=request.data.get('gitInsta'),
            gitFace=request.data.get('gitFace'),
            gitLinked=request.data.get('gitLinked'))

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
                'companyName': get_users_obj.companyName,
                'profilePic': get_users_obj.profilePic})

        return Response({"msg": "success"})

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

    print(request.data)
    username = request.data.get('username')
    password = request.data.get('password')
    userssss = User.objects.all()
    userInfo = User.objects.filter(username=username, password=password)
    print("##########################################################33")
    print(userssss)
    print(userInfo)
    if userInfo.count() > 0:

        userCustomInfo = users.objects.filter(customUserID=userInfo.first())

        if userCustomInfo.count() > 0:

            url = 'http://127.0.0.1:8000/media/{}'.format(
                userCustomInfo.first().profilePic)

            obj = ({'userId': userCustomInfo.first().id,
                    'username': userInfo.first().username,
                    'email': userInfo.first().email,
                    'first_name': userInfo.first().first_name,
                    'last_name': userInfo.first().last_name,
                    'password': userInfo.first().password,
                    'phone_number': userCustomInfo.first().phone_number,
                    'profilePic':  url,
                    'location': userCustomInfo.first().location,
                    'fieldCompany': userCustomInfo.first().fieldCompany,
                    'gitAccount': userCustomInfo.first().gitAccount,
                    'gitInsta': userCustomInfo.first().gitInsta,
                    'gitFace': userCustomInfo.first().gitFace,
                    'gitLinked': userCustomInfo.first().gitLinked,
                    'skills':userCustomInfo.first().skills,
                    'typeUser': userCustomInfo.first().typeUser,
                    })

            return Response({'obj': obj})
        else:
            return Response({"msg": "notActive"})

    else:
        return Response({"msg": "no"})


@api_view(['GET'])
def getCompany(request):
    obj = []
    getcomp = users.objects.filter(typeUser="Company").all()
    if(getcomp.count() > 0):
        for item in getcomp:

            getoneCom = User.objects.filter()
            getJob = jobs.objects.filter(userID=item).count()
            obj.append({'userId': item.id,
                        'companyName': item.companyName,
                        'count': getJob
                        })

    return Response(obj)

@api_view(['POST'])
def updateUser(request):
    print('#####################################################')
    print(request.data)
    getUser = users.objects.filter( id = request.data.get('userID')).first()
    getUserDjangoInfo = User.objects.filter( id = getUser.customUserID.id ).first()

    try:
        if(request.data.get('firstname') != ''):
            getUserDjangoInfo.first_name = request.data.get('firstname')
            getUserDjangoInfo.save()
        if(request.data.get('lastname') != ''):
            getUserDjangoInfo.last_name = request.data.get('lastname') 
            getUserDjangoInfo.save()
        if(request.data.get('password') != ''):
            getUserDjangoInfo.password = request.data.get('password')
            getUserDjangoInfo.save()
        if(request.data.get('location') != ''):
            getUser.location = request.data.get('location')
            getUser.save()

        if(request.data.get('phone_number') != ''):
            getUser.phone_number = request.data.get('phone_number')
            getUser.save()
        if(request.data.get('insta') != ''):
            getUser.gitInsta = request.data.get('insta')
            getUser.save()
            
        if(request.data.get('git') != ''): 
            getUser.gitInsta = request.data.get('git')
            getUser.save()     
        if(request.data.get('face') != ''):     
            getUser.gitFace = request.data.get('face') 
            getUser.save()
        if(request.data.get('linkedin') != ''):     
            getUser.gitLinked = request.data.get('linkedin') 
            getUser.save()
        if(request.data.get('companyField') != ''): 
            getUser.fieldCompany = request.data.get('companyField')
            getUser.save()
        if(request.data.get('campanyname') != ''):
            getUser.companyName = request.data.get('campanyname')
            getUser.save()
        if(request.data.get('profile')  is not None and request.data.get('profile')  != '' ):
            getUser.profilePic = request.data.get('profile')
            getUser.save()


        url = 'http://127.0.0.1:8000/media/{}'.format(
                getUser.profilePic)

        obj = ({'userId': getUser.id,
                    'username': getUserDjangoInfo.username,
                    'email': getUserDjangoInfo.email,
                    'first_name': getUserDjangoInfo.first_name,
                    'last_name': getUserDjangoInfo.last_name,
                    'password': getUserDjangoInfo.password,
                    'phone_number': getUser.phone_number,
                    'profilePic':  url,
                    'location': getUser.location,
                    'fieldCompany': getUser.fieldCompany,
                    'gitAccount': getUser.gitAccount,
                    'gitInsta': getUser.gitInsta,
                    'gitFace': getUser.gitFace,
                    'gitLinked': getUser.gitLinked,
                    'skills':getUser.skills,
                    'typeUser': getUser.typeUser,
                    })
        return Response({"msg": "success" , "obj":obj})

    except IntegrityError as ex:
        transaction.rollback()
        message = ex.args
        return Response({"msg": message}) 


@api_view(['POST'])
def updateSkill(request):
    try:
        getUser = users.objects.filter( id = request.data.get('userID')).first() 
        getUserDjangoInfo = User.objects.filter( id = getUser.customUserID.id ).first()
    
        getUser.skills = request.data.get('skills')
        getUser.save()
        url = 'http://127.0.0.1:8000/media/{}'.format(
                    getUser.profilePic)

        obj = ({'userId': getUser.id,
                    'username': getUserDjangoInfo.username,
                    'email': getUserDjangoInfo.email,
                    'first_name': getUserDjangoInfo.first_name,
                    'last_name': getUserDjangoInfo.last_name,
                    'password': getUserDjangoInfo.password,
                    'phone_number': getUser.phone_number,
                    'profilePic':  url,
                    'location': getUser.location,
                    'fieldCompany': getUser.fieldCompany,
                    'gitAccount': getUser.gitAccount,
                    'gitInsta': getUser.gitInsta,
                    'gitFace': getUser.gitFace,
                    'gitLinked': getUser.gitLinked,
                    'skills':getUser.skills,
                    'typeUser': getUser.typeUser,
                    })
        return Response({"msg": "success" , "obj":obj})

    except IntegrityError as ex:
        transaction.rollback()
        message = ex.args
        return Response({"msg": message}) 
          
