from django.shortcuts import render
from .serializers import jobSerializer
from AppJob.models import category, jobs, locations, tags, tagsJob, aplayUser, aplayCer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.http import request
from AppUsers.models import users
from django.contrib.auth.models import User
from django.db import connection
from django.db import IntegrityError, transaction
import smtplib
import ssl
import logging
# Create your views here.
# class addJob(viewsets.ModelViewSet):

# serializer_class = jobSerializer
# queryset = jobs.objects.all()


@api_view(['POST'])
def addJob(request):

    title = request.data.get('title')
    if(request.data.get('location')):
        location = request.data.get('location')
    else:
        location = None
    if(request.data.get('jobType') == ' Full Time'):

        jobType = 'F'

    else:
        jobType = 'P'
    userid = request.data.get('userID')
    description = request.data.get('description')
    published_at = request.data.get('published_at')
    vacancy = request.data.get('vacancy')
    salary = request.data.get('salary')
    if(request.data.get('categoryID')):
        categoryID = request.data.get('categoryID')
    else:
        categoryID = None
    experience = request.data.get('experience')
    qualification = request.data.get('qualification')
    benefits = request.data.get('benefits')
    gender = request.data.get('gender')
    if(request.data.get('ExEmail')):
        ExEmail = request.data.get('ExEmail')
    else:
        ExEmail = None
    getJob = jobs.objects.create(userID_id=users.objects.filter(id=int(userid)).first().id,
                                 title=title,
                                 location=location,
                                 jobType=jobType,
                                 description=description,
                                 published_at=published_at,
                                 vacancy=vacancy,
                                 aplayingNum=0,
                                 salary=salary,
                                 categoryID=category.objects.filter(
                                     id=categoryID).first(),
                                 experience=experience,
                                 qualification=qualification,
                                 benefits=benefits,
                                 gender=gender,
                                 ExEmail=ExEmail)

    return Response(getJob.id)


@api_view(['POST'])
def jobDetails(request):

    get_jobID = request.data.get('jobID')

    if request.data.get('name'):
        Tags = request.data.get('name')
     
        for tag in Tags:
            tagsJob.objects.create(tagID=tags.objects.get(
                id=tag), jobID=jobs.objects.get(id=get_jobID))

    if request.data.get('otherTags'):

        otherTag = request.data.get('otherTags')
        for tag in otherTag:
            currentTag = tags.objects.create(tag=tag)
            tagsJob.objects.create(jobID=jobs.objects.get(
                id=int(get_jobID)), tagID=currentTag)

    return Response({"msg": "success"})


@api_view(['GET'])
def getLoc(request):
    locList = []
    getLoc = locations.objects.all()
    for loc in getLoc:
        locList.append({'id': loc.id, 'name': loc.locName})

    return Response(locList)


@api_view(['GET'])
def getTag(request):
    locList = []
    getLoc = tags.objects.all().distinct()
    for loc in getLoc:
        locList.append({'id': loc.id, 'name': loc.tag})

    return Response(locList)


@api_view(['GET'])
def getCat(request):
    locList = []
    getLoc = category.objects.all().distinct()
    for loc in getLoc:
        locList.append({'id': loc.id,
                        'name': loc.name,
                        })
    return Response(locList)


@api_view(['GET'])
def getInfoCat(request):
    locList = []

    getLoc = category.objects.all()
    for loc in getLoc:
        job = []
        getJob = jobs.objects.filter(categoryID=loc.id).count()
        locList.append({'id': loc.id,
                        'name': loc.name,
                        'count': getJob
                        })

    return Response(locList)


@api_view(['POST'])
def addCat(request):
    getCat = category.objects.create(name=request.POST.get('name'))
    return Response({"id": getCat.id})


@api_view(['POST'])
def searchJob(request):

    jobsList = []
    jobInfo = []

    if(request.data.get('tag')):
        tag = request.data.get('tag')
        gettagId = tags.objects.filter(id=tag).first()
        getjobTag = tagsJob.objects.filter(tagID=gettagId).all()
        for job in getjobTag:
            jobsList.append(job.jobID.id)

    if(request.data.get('Ex')):
        Ex = request.data.get('Ex')
        ExJob = jobs.objects.filter(experience=Ex).all()
        for job in ExJob:
            jobsList.append(job.id)

    if(request.data.get('title')):
        title = request.data.get('title')
        getjob = jobs.objects.filter(title=title).all()
        for item in getjob:
            jobsList.append(item.id)

    if(request.data.get('loc')):
        loc = request.data.get('loc')

        getLocID = locations.objects.filter(id=int(loc)).first()

        getjob = jobs.objects.filter(location=getLocID).all()
        for item in getjob:
            jobsList.append(item.id)

    if(request.data.get('userID')):
        getuserID = request.data.get('userID')
        getjob = jobs.objects.filter(
            userID=users.objects.get(id=getuserID)).all()
        for item in getjob:
            jobsList.append(item.id)

    if(request.data.get('gender')):
        getuserGender = request.data.get('gender')
        getjob = jobs.objects.filter(gender=getuserGender).all()
        for item in getjob:
            jobsList.append(item.id)

    if(len(jobsList) > 0):
        jobsList = list(dict.fromkeys(jobsList))
        for item in jobsList:

          
            getallJob = jobs.objects.get(id=int(item))

          
            getUsers = users.objects.filter(id=getallJob.userID.id).first()
            getUserDjango = User.objects.filter(
                id=getUsers.customUserID.id).first()

            if(getallJob.location != None):
                getLoc = locations.objects.filter(id=getallJob.location.id).first()
            else:
                getLoc = "The location is not available"    


            if(getallJob.categoryID):
                getCat = category.objects.filter(id=getallJob.categoryID.id).first()
            else:
                getCat = 'The Category is not available'

            
            url = 'http://127.0.0.1:8000/media/{}'.format(
                getUsers.profilePic)
            userJob = ({

                'companyName': getUsers.companyName,
                'userID': getUsers.id,
                'profilePic': url,
                'email': getUserDjango.email,
                'phone_number': getUsers.phone_number,
            })

            if(getallJob.location != None):
                jobInfo.append({
                    'jobID': getallJob.id,
                    'title': getallJob.title,
                    'location': getLoc.locName,
                    'locID': getLoc.id,
                    'jobType': getallJob.jobType,
                    'description': getallJob.description,
                    'published_at': getallJob.published_at,
                    'vacancy': getallJob.vacancy,
                    'salary': getallJob.salary,
                    'experience': getallJob.experience,
                    'catID': getCat.id,
                    'catName': getCat.name,
                    'userID': userJob
                })
            else: 
                jobInfo.append({
                    'jobID': getallJob.id,
                    'title': getallJob.title,
                    'location': getLoc,
                  
                    'jobType': getallJob.jobType,
                    'description': getallJob.description,
                    'published_at': getallJob.published_at,
                    'vacancy': getallJob.vacancy,
                    'salary': getallJob.salary,
                    'experience': getallJob.experience,
                   
                    'catName': getCat,
                    'userID': userJob
                })   

    return Response({"info": jobInfo},  status=status.HTTP_201_CREATED)


@api_view(['GET'])
def allJobs(request):
    jobInfo = []
    alljob = jobs.objects.all()
    if(alljob.count() > 0):
        for item in alljob:

            getUsers = users.objects.filter(id=item.userID.id).first()
            getUserDjango = User.objects.filter(
                id=getUsers.customUserID.id).first()
            if(item.categoryID):
                getCat = category.objects.filter(id=item.categoryID.id).first()
            else:
                getCat = 'The Category is not available'

            if(item.location != None):
                getLoc = locations.objects.filter(id=item.location.id).first()
            else:
                getLoc = "The location is not available"

            #
            url = 'http://127.0.0.1:8000/media/{}'.format(
                getUsers.profilePic)
            userJob = ({
                'companyName': getUsers.companyName,
                'userID': getUsers.id,
                'email': getUserDjango.email,
                'profilePic': url,
                'phone_number': getUsers.phone_number,
            })

            if(item.location != None):
                jobInfo.append({
                    'jobID': item.id,
                    'title': item.title,
                    'location': getLoc.locName,
                    'locID': getLoc.id,
                    'jobType': item.jobType,
                    'description': item.description,
                    'published_at': item.published_at,
                    'vacancy': item.vacancy,
                    'salary': item.salary,
                    'experience': item.experience,
                    'catID': getCat.id,
                    'catName': getCat.name,
                    'userID': userJob
                })
            else:
                jobInfo.append({
                    'jobID': item.id,
                    'title': item.title,
                    'location': getLoc,
                    'jobType': item.jobType,
                    'description': item.description,
                    'published_at': item.published_at,
                    'vacancy': item.vacancy,
                    'salary': item.salary,
                    'experience': item.experience,
                   
                    'catName': getCat,
                    'userID': userJob
                })  
    return Response(jobInfo)


@api_view(['POST'])
def getjob_with_related_Job(request):
    jobInfo = []
    alljob = jobs.objects.filter(
        categoryID=category.objects.get(id=request.data)).all()
    if(alljob.count() > 0):
        for item in alljob:

            getUsers = users.objects.filter(id=item.userID.id).first()
            getUserDjango = User.objects.filter(
                id=getUsers.customUserID.id).first()
            getCat = category.objects.filter(id=item.categoryID.id).first()
            getLoc = locations.objects.filter(id=item.location.id).first()
            getTags = locations.objects.filter(id=item.location.id).first()
            #
            url = 'http://127.0.0.1:8000/media/{}'.format(
                getUsers.profilePic)
            userJob = ({
                'companyName': getUsers.companyName,
                'userID': getUsers.id,
                'email': getUserDjango.email,
                'profilePic': url,
                'phone_number': getUsers.phone_number,
            })

            jobInfo.append({
                'jobID': item.id,
                'title': item.title,
                'location': getLoc.locName,
                'locID': getLoc.id,
                'jobType': item.jobType,
                'description': item.description,
                'published_at': item.published_at,
                'vacancy': item.vacancy,
                'salary': item.salary,
                'experience': item.experience,
                'catID': getCat.id,
                'catName': getCat.name,
                'userID': userJob
            })
    return Response(jobInfo)


@api_view(['POST'])
def getjob_with_related_company(request):
    jobInfo = []
    alljob = jobs.objects.filter(
        userID=users.objects.get(id=request.data)).all()
    if(alljob.count() > 0):
        for item in alljob:

            getUsers = users.objects.filter(id=item.userID.id).first()
            getUserDjango = User.objects.filter(
                id=getUsers.customUserID.id).first()
            if(item.categoryID):
                getCat = category.objects.filter(id=item.categoryID.id).first()

            else:
                getCat = 'The Category is not available'

            if(item.location != None):
                getLoc = locations.objects.filter(id=item.location.id).first()

                #getTags = locations.objects.filter(id = item.location.id  ).first()
            else:
                getLoc = "The location is not available"

            #
            url = 'http://127.0.0.1:8000/media/{}'.format(
                getUsers.profilePic)
            userJob = ({
                'companyName': getUsers.companyName,
                'userID': getUsers.id,
                'profilePic': url,
                'email': getUserDjango.email,
                'phone_number': getUsers.phone_number,
            })

            if(item.location != None):
                jobInfo.append({
                    'jobID': item.id,
                    'title': item.title,
                    'catID': getCat.id,
                    'catName': getCat.name,
                    'jobType': item.jobType,
                    'description': item.description,
                    'published_at': item.published_at,
                    'vacancy': item.vacancy,
                    'salary': item.salary,
                    'experience': item.experience,
                    'location': getLoc.locName,
                    'locID': getLoc.id,
                    'userID': userJob
                })
            else:
                jobInfo.append({
                    'jobID': item.id,
                    'title': item.title,
                    'catName': getCat,
                    'location': getLoc,
                    'jobType': item.jobType,
                    'description': item.description,
                    'published_at': item.published_at,
                    'vacancy': item.vacancy,
                    'salary': item.salary,
                    'experience': item.experience,

                    'userID': userJob
                })
    return Response(jobInfo)


@api_view(['POST'])
def jobInfo(request):
    jobInfo = {}
    tag = []

    alljob = jobs.objects.filter(id=request.data).first()

    getUsers = users.objects.filter(id=alljob.userID.id).first()
    getUserDjango = User.objects.filter(id=getUsers.customUserID.id).first()
    
    if(alljob.categoryID):
        getCat = category.objects.filter(id=alljob.categoryID.id).first()
    else:
        getCat = 'The Category is not available'

    if(alljob.location != None):
        getLoc = locations.objects.filter(id=alljob.location.id).first()
    else:
        getLoc = "The location is not available"

    gettagId = tagsJob.objects.filter(jobID=alljob).all()
    for itemtag in gettagId:
       
        getTag = tags.objects.filter(id=itemtag.tagID.id).first()
       
        tag.append(getTag.tag)
    #
    url = 'http://127.0.0.1:8000/media/{}'.format(
        getUsers.profilePic)
    userJob = ({
        'companyName': getUsers.companyName,
        'userID': getUsers.id,
        'email': getUserDjango.email,
        'profilePic': url,
        'phone_number': getUsers.phone_number,
    })

    if(alljob.location != None):
        jobInfo = {
            'jobID': alljob.id,
            'title': alljob.title,
            'location': getLoc.locName,
            'locID': getLoc.id,
            'jobTags': tag,
            'jobType': alljob.jobType,
            'description': alljob.description,
            'published_at': alljob.published_at,
            'vacancy': alljob.vacancy,
            'salary': alljob.salary,
            'experience': alljob.experience,
            'benefits': alljob.benefits,
            'qualification': alljob.qualification,
            'catID': getCat.id,
            'catName': getCat.name,
            'gender': alljob.gender,
            'userID': userJob
        }
    else:
            
        jobInfo = {
            'jobID': alljob.id,
            'title': alljob.title,
            'location': getLoc,
            'jobTags': tag,
            'jobType': alljob.jobType,
            'description': alljob.description,
            'published_at': alljob.published_at,
            'vacancy': alljob.vacancy,
            'salary': alljob.salary,
            'experience': alljob.experience,
            'benefits': alljob.benefits,
            'qualification': alljob.qualification,
           'ExEmail':alljob.ExEmail,
            'catName': getCat,
            'gender': alljob.gender,
            'userID': userJob
        }   
    return Response(jobInfo)


@api_view(['POST'])
def deleteJob(request):
    try:
        # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$44")
        # print(request.data) 
        # tagDelete = tagsJob.objects.filter(
        #     jobID=jobs.objects.get(id=request.data)).all()
        # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$44")
        # print(tagDelete)   
        # for item in tagDelete:
        #     item.delete()    
        jobs.objects.filter(id=request.data).delete()
        return Response({"msg": "success"})
    except IntegrityError as ex:
        transaction.rollback()
        message = ex.args
        return Response({"msg": message})


@api_view(['POST'])
def aplayJob(request):

    try:
        filepath = request.FILES['uploadCv'] if 'uploadCv' in request.FILES else False

        if filepath:
            uploadCv = filepath

        apaly = aplayUser.objects.create(userID=users.objects.get(id=request.data.get('userID')),
                                         jobID=jobs.objects.get(
                                             id=request.data.get('jobID')),
                                         name=request.data.get('name'),
                                         email=request.data.get('email'),
                                         coverLitter=request.data.get(
                                             'writeSummary'),
                                         phone_number=request.data.get(
                                             'phone'),
                                         uploadCV=uploadCv,
                                         aplay_at=request.data.get(
                                             'published_at'),
                                         isAccept=False)

        fileCer = request.FILES.getlist(
            'uploadCertifi') if 'uploadCertifi' in request.FILES else False

        if fileCer:
            for Cer in fileCer:
                addCer = aplayCer(aplayID=apaly, uploadCer=Cer)
                addCer.save()

        return Response({"msg": "success"})

    except IntegrityError as ex:
        transaction.rollback()
        message = ex.args
        return Response({"msg": "exist"})


@api_view(['POST'])
def getjob_with_related_ApplayingUser(request):
    jobInfo = []
   
    aplayingJob = aplayUser.objects.filter(userID=request.data).all()
    if(aplayingJob.count() > 0):
        for item in aplayingJob:

            getjob = jobs.objects.filter(id=item.jobID.id).first()
            getUsers = users.objects.filter(id=getjob.userID.id).first()
            getUserDjango = User.objects.filter(
                id=getUsers.customUserID.id).first()
            getCat = category.objects.filter(id=getjob.categoryID.id).first()
            getLoc = locations.objects.filter(id=getjob.location.id).first()
            getTags = locations.objects.filter(id=getjob.location.id).first()
            #
            url = 'http://127.0.0.1:8000/media/{}'.format(
                getUsers.profilePic)
            userJob = ({
                'companyName': getUsers.companyName,
                'userID': getUsers.id,
                'profilePic': url,
                'email': getUserDjango.email,
                'phone_number': getUsers.phone_number,
            })

            jobInfo.append({
                'jobID': getjob.id,
                'title': getjob.title,
                'location': getLoc.locName,
                'locID': getLoc.id,
                'jobType': getjob.jobType,
                'description': getjob.description,
                'published_at': getjob.published_at,
                'vacancy': getjob.vacancy,
                'salary': getjob.salary,
                'experience': getjob.experience,
                'catID': getCat.id,
                'catName': getCat.name,
                'userID': userJob
            })
    return Response(jobInfo)


@api_view(['POST'])
def getj_ApplayingUser_with_relatedCompany(request):
    applayingInfo = []
    try:
        allJob = jobs.objects.filter(id=request.data).first()
        getapplayingJob = aplayUser.objects.filter(jobID=allJob.id).all()
        if(getapplayingJob.count() > 0):

            for aplayitem in getapplayingJob:
                getCerArr = []
                getCer = aplayCer.objects.filter(aplayID=aplayitem.id).all()
                if(getCer.count() > 0):

                    for itemCer in getCer:

                        url = 'http://127.0.0.1:8000/media/{}'.format(
                            itemCer.uploadCer)
                        getCerArr.append(url)

                urlCV = 'http://127.0.0.1:8000/media/{}'.format(
                    aplayitem.uploadCV)

                getUsers = users.objects.filter(id=aplayitem.userID.id).first()

                urlImg = 'http://127.0.0.1:8000/media/{}'.format(
                    getUsers.profilePic)

                applayingInfo.append({'applayID': aplayitem.id,
                                      'name': aplayitem.name,
                                      'phone': aplayitem.phone_number,
                                      'email': aplayitem.email,
                                      'userID': aplayitem.userID.id,
                                      'imgUser': urlImg,
                                      'CV': urlCV,
                                      'certify': getCerArr})

       
        return Response(applayingInfo)

    except IntegrityError as ex:
        transaction.rollback()
        message = ex.args
        return Response({"msg": "exist"})


@api_view(['POST'])
def acceptUser_ForJob(request):
   
    SERVICE = 'smtp.gmail.com:587'
    USERNAME = 'job.Board.hr97@gmail.com'
    PASSWORD = 'walaa$$123'
    msg = request.data.get('MsgApproval')
    toaddrs= request.data.get('mailEmp')
    fromaddrs = request.data.get('mailCom')
    userfirstName = request.data.get('userfirstName')
    nameCom = request.data.get('nameCom')
   
   
    # Create the plain-text and HTML version of your message
    message = """
    Subject: Hi {name}
    {company} Company has approved your job application and will contact you on your online account.
    approval letter:
    {aprove}
   """
    try:

        # connection = init_connection(SERVICE, USERNAME, PASSWORD)

        server = smtplib.SMTP(SERVICE)
        server.ehlo()
        server.starttls()
        server.login(USERNAME, PASSWORD)
        server.ehlo()
        server.sendmail(USERNAME, toaddrs, message.format(
            name=userfirstName, company=nameCom ,aprove=msg  ))
        server.quit()

        return Response({"msg": "success"})
    except:
        logging.critical("cant start connection")

        return Response({"msg": "no"})



@api_view(['POST'])
def updateJob(request):
    getJob = jobs.objects.filter(id = request.data.get('jobID')).first()
    if(request.data.get('title')):
        getJob.title = request.data.get('title')
        getJob.save()

    if(request.data.get('salary')):
        getJob.salary = request.data.get('salary')
        getJob.save()

    if(request.data.get('benefit')):
        getJob.benefits = request.data.get('benefit')
        getJob.save()

    if(request.data.get('vacancy')):
        getJob.vacancy = request.data.get('vacancy')
        getJob.save()    

    if(request.data.get('description')):
        getJob.description = request.data.get('description')
        getJob.save()     


    if(request.data.get('qualifi')):
        getJob.qualification = request.data.get('qualifi')
        getJob.save() 

    return Response({"msg": "success"})