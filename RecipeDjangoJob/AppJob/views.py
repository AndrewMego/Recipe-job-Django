from django.shortcuts import render
from .serializers import jobSerializer
from AppJob.models import category, jobs, locations, tags, tagsJob
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.http import request
from AppUsers.models import users
from django.contrib.auth.models import User
from  django.db import connection
# Create your views here.
# class addJob(viewsets.ModelViewSet):

# serializer_class = jobSerializer
# queryset = jobs.objects.all()


@api_view(['POST'])
def addJob(request):

    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print(request.data)

    title = request.data.get('title')
    location = request.data.get('location')
    if(request.data.get('jobType') == ' Full Time'):

        jobType ='F'

    else:
        jobType ='P' 
    userid = request.data.get('userID')    
    print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
    print(userid)
    print( users.objects.get(id=int(userid)))
    description = request.data.get('description')
    published_at = request.data.get('published_at')
    vacancy = request.data.get('vacancy')
    salary = request.data.get('salary')
    categoryID = request.data.get('categoryID')
    experience = request.data.get('experience')
    qualification = request.data.get('qualification')
    benefits = request.data.get('benefits')
    gender = request.data.get('gender')

    getJob = jobs.objects.create(userID_id=users.objects.filter(id=int(userid)).first().id,
                                 title=title,
                                 location=location,
                                 jobType=jobType,
                                 description=description,
                                 published_at=published_at,
                                 vacancy=vacancy,
                                 aplayingNum=0,
                                 salary=salary,
                                 categoryID=category.objects.filter(id = categoryID).first(),
                                 experience=experience,
                                 qualification=qualification,
                                 benefits=benefits,
                                 gender=gender)



    return Response(getJob.id)


@api_view(['POST'])
def jobDetails(request):
    print("########################")
    print(request.data)
    get_jobID = request.data.get('jobID')
    
    if request.data.get('name'):
        Tags = request.data.get('name')
        for tag in Tags:
            print(tag)
            tagsJob.objects.create(tagID=tags.objects.get(
                id=tag['id']), jobID=jobs.objects.get(id=get_jobID))

    if request.data.get('otherTags'):
        print("&&&&&&&&&&&&   true")
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
        locList.append({'id': loc.id , 'name': loc.locName})

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
        getJob = jobs.objects.filter(categoryID = loc.id ).count()
        locList.append({'id': loc.id,
                        'name': loc.name,
                        'count' : getJob
                        })
            
            #for item in getJob.all():
                 
                
               
                # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                
                # getUsers = users.objects.filter(id =item.userID.id).first()
                # getUserDjango =User.objects.filter(id = getUsers.customUserID.id ).first()
                # getCat = category.objects.filter(id = item.categoryID.id  ).first()
                # getLoc = locations.objects.filter(id = item.location.id  ).first()
                # #'profilePic':getUsers.profilePic,

                # userJob = ({
                
                #     'companyName': getUsers.companyName,
                #     'userID':getUsers.id,
                    
                #     'email': getUserDjango.email,
                #     'phone_number': getUsers.phone_number,
                # })

                # job.append({
                # 'jobID': item.id,
                # 'title': item.title,
                # 'location': getLoc.locName,
                # 'locID':getLoc.id,
                # 'jobType': item.jobType,
                # 'description': item.description,
                # 'published_at': item.published_at,
                # 'vacancy': item.vacancy,
                # 'salary': item.salary,
                # 'experience': item.experience,
                # 'catID': getCat.id,
                # 'catName': getCat.name,
                # 'userID': userJob
                # })               
        

    return Response(locList)




@api_view(['POST'])
def addCat(request):
    getCat = category.objects.create(name=request.POST.get('name'))
    return Response({"id": getCat.id})


@api_view(['POST'])
def searchJob(request):
   
    jobsList = []
    jobInfo =[]
    
    if(request.data.get('tag')):
        tag = request.data.get('tag')
        gettagId = tags.objects.filter(id=tag).first()
        getjobTag = tagsJob.objects.filter(tagID = gettagId).all()
        for job in getjobTag:
            jobsList.append(job.jobID.id)

    if(request.data.get('Ex')):
        Ex = request.data.get('Ex')
        ExJob = jobs.objects.filter(experience = Ex).all()
        for job in ExJob:
            jobsList.append(job.id)

    if(request.data.get('title')):
        title = request.data.get('title')
        getjob = jobs.objects.filter(title = title).all()
        for item in getjob:
            jobsList.append(item.id) 
        

    if(request.data.get('loc')):
        loc = request.data.get('loc')
        
        getLocID =locations.objects.filter(id =int(loc)).first() 
      
        getjob = jobs.objects.filter(location = getLocID).all()
        for item in getjob:
            jobsList.append(item.id) 

    if(request.data.get('userID')):
        getuserID = request.data.get('userID')
        getjob = jobs.objects.filter(userID =users.objects.get(id = getuserID)).all()
        for item in getjob:
            jobsList.append(item.id)

    if(request.data.get('gender')):
        getuserGender = request.data.get('gender')
        getjob = jobs.objects.filter(gender = getuserGender).all()
        for item in getjob:
            jobsList.append(item.id)        


    if(len(jobsList)>0):
        jobsList = list(dict.fromkeys(jobsList))        
        for item in jobsList:
            
            print(item)
            print(item)
            getallJob = jobs.objects.get(id =int(item))
           
            print(getallJob.userID.id)
            getUsers = users.objects.filter(id =getallJob.userID.id).first()
            getUserDjango =User.objects.filter(id = getUsers.customUserID.id ).first()
            getCat = category.objects.filter(id = getallJob.categoryID.id  ).first()
            getLoc = locations.objects.filter(id = getallJob.location.id  ).first()
            #'profilePic':getUsers.profilePic,

            userJob = ({
               
                'companyName': getUsers.companyName,
                'userID':getUsers.id,
                
                'email': getUserDjango.email,
                'phone_number': getUsers.phone_number,
            })

            jobInfo.append({
            'jobID': getallJob.id,
            'title': getallJob.title,
            'location': getLoc.locName,
            'locID':getLoc.id,
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


    return Response({"info": jobInfo} ,  status=status.HTTP_201_CREATED)        

@api_view(['GET'])
def allJobs(request):
    jobInfo=[]
    alljob = jobs.objects.all()
    if(alljob.count() > 0):
        for item in alljob:
           
            getUsers = users.objects.filter(id =item.userID.id).first()
            getUserDjango =User.objects.filter(id = getUsers.customUserID.id ).first()
            getCat = category.objects.filter(id = item.categoryID.id  ).first()
            getLoc = locations.objects.filter(id = item.location.id  ).first()
            #'profilePic':getUsers.profilePic,

            userJob = ({   
                'companyName': getUsers.companyName,
                'userID':getUsers.id,    
                'email': getUserDjango.email,
                'phone_number': getUsers.phone_number,
            })

            jobInfo.append({
            'jobID': item.id,
            'title': item.title,
            'location': getLoc.locName,
            'locID':getLoc.id,
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
def getjob_with_related_Job(request):
    jobInfo=[]
    alljob = jobs.objects.filter(categoryID = category.objects.get(id=request.data)).all()
    if(alljob.count() > 0):
        for item in alljob:
           
            getUsers = users.objects.filter(id =item.userID.id).first()
            getUserDjango =User.objects.filter(id = getUsers.customUserID.id ).first()
            getCat = category.objects.filter(id = item.categoryID.id  ).first()
            getLoc = locations.objects.filter(id = item.location.id  ).first()
            getTags = locations.objects.filter(id = item.location.id  ).first()
            #'profilePic':getUsers.profilePic,

            userJob = ({   
                'companyName': getUsers.companyName,
                'userID':getUsers.id,    
                'email': getUserDjango.email,
                'phone_number': getUsers.phone_number,
            })

            jobInfo.append({
            'jobID': item.id,
            'title': item.title,
            'location': getLoc.locName,
            'locID':getLoc.id,
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
def jobInfo(request):
    jobInfo={}
    tag = []
   
    alljob = jobs.objects.filter(id = request.data ).first()
        
    getUsers = users.objects.filter(id =alljob.userID.id).first()
    getUserDjango =User.objects.filter(id = getUsers.customUserID.id ).first()
    getCat = category.objects.filter(id = alljob.categoryID.id  ).first()
    getLoc = locations.objects.filter(id = alljob.location.id  ).first()

    gettagId = tagsJob.objects.filter(jobID=alljob).all()
    for itemtag in gettagId: 
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(itemtag.tagID.id)
        getTag = tags.objects.filter(id =itemtag.tagID.id).first()
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(getTag.tag)
        tag.append(getTag.tag)
    #'profilePic':getUsers.profilePic,

    userJob = ({   
        'companyName': getUsers.companyName,
        'userID':getUsers.id,    
        'email': getUserDjango.email,
        'phone_number': getUsers.phone_number,
    })

    jobInfo={
    'jobID': alljob.id,
    'title': alljob.title,
    'location': getLoc.locName,
    'locID':getLoc.id,
    'jobTags':tag,
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
    return Response(jobInfo)
    
# def addLoc(request):

#     locations.objects.create(locName = 'alex')
#     locations.objects.create(locName = 'assiut')
#     locations.objects.create(locName = 'aswan')
#     locations.objects.create(locName = 'luxor')
#     locations.objects.create(locName = 'cairo')
#     locations.objects.create(locName = 'giza')
#     locations.objects.create(locName = 'qena')
#     locations.objects.create(locName = 'menia')
#     locations.objects.create(locName = 'sohag')









    #     tag = tags.objects.filter( tag = request.data.get('tag') ).all()
    #     getjobTag = tagsJob.objects.filter
    # if(request.data.get('title')):
    #     title = jobs.objects.filter( title = request.data.get('title') ).all()
    # if(request.data.get('loc')):
    #     loc = jobs.objects.filter( location = request.data.get('loc') ).all()    


    # getJobs = jobs.objects.    
    
           


    # jobsList = []
    # jobSelect = ' select JOB.id as jobID , title, location, "jobType", description, published_at, JOB.vacancy, JOB.salary, JOB.experience, C.id as catID, C.name as catName , JOB."userID_id" as userID from public."AppJob_jobs" JOB join public."AppJob_category" C on C.id = JOB."categoryID_id" join public."AppJob_tagsjob" JT on JT."jobID_id" = JOB.id join public."AppJob_tags" J on J.id = JT."tagID_id" where JOB.title as like "job" or JOB.location LIKE "assiut" or J.tag LIKE "JAVA" '
    # cursor.execute(jobSelect)
    # results = cursor.fetchall()
    # for c, row in enumerate(results):

    #     userJob = {}
    #     get_mainUser = User.objects.filter(id = int(row['userID'])).first()
    #     jobSelect = "SELECT profilePic, companyName,  customUserID_id FROM AppUsers_users U where customUserID_id = {} ".format(
    #         row['userID'])
    #     cursor.execute(jobSelect)
    #     results = cursor.fetchall()
    #     for c, row in enumerate(results):
    #         userJob = ({
    #    'profilePic': row['profilePic'],
    #             'companyName': row['companyName'],
    #             'userID': row['customUserID_id'],
    #             'location' : row['location'],
    #             'email': get_mainUser.email,
    #             'phone_number': row['phone_number'],
    #         })

    #     jobsList.append({
    #         'jobID': row['jobID'],
    #         'title': row['title'],
    #         'location': row['location'],
    #         'jobType': row['jobType'],
    #         'description': row['description'],
    #         'published_at': row['published_at'],
    #         'vacancy': row['vacancy'],
    #         'salary': row['salary'],
    #         'experience': row['experience'],
    #         'catID': row['catID'],
    #         'catName': row['catName'],
    #         'userID': userJob
    #     })

    # return Response({'allJob': jobsList})    
