from django.shortcuts import render
from AppBlog.models import Blog, blogImg, comments, likesBlog
from .serializers import blogSerializer, commentSerializer, FileListSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from AppUsers.models import users
from django.http import HttpResponseRedirect
from django.db import IntegrityError, transaction

from django.contrib.auth.models import User
# Create your views here.


class addBlog(viewsets.ModelViewSet):
    serializer_class = blogSerializer
    queryset = Blog.objects.all()


class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = FileListSerializer
    parser_classes = (MultiPartParser, FormParser,)
    queryset = blogImg.objects.all()


@api_view(['GET'])
def getBlog(request):
    blogs =[]
    getallBlog= Blog.objects.all().order_by('-id')
    if(getallBlog.count() > 0):
        for item in getallBlog:

            #getblogItem = Blog.objects.get(id =item.id)
            getusersBlog = users.objects.filter(id =item.userID.id).first()
            getUserDjangoBlog =User.objects.filter(id = getusersBlog.customUserID.id ).first()
            
           
            blogImgarray=[]
            getimagBlog = blogImg.objects.filter(blogID = int(item.id) ).all()
            if (getimagBlog.count() > 0):
                for itemImg in getimagBlog:
                    pic = 'http://127.0.0.1:8000/media/{}'.format(
                                            itemImg.blogimg)
                    blogImgarray.append(pic)

            allcomments = []
            getCom = comments.objects.filter(blogID = item).all()
            if(getCom.count() > 0):
                for itemCom in getCom:

                    getusers = users.objects.filter(id = itemCom.userID.id).first() 
                    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$#######################")
                    print(getusers)
                    getUserDjango = User.objects.filter(id =getusers.customUserID.id ).first()
                    picUser = 'http://127.0.0.1:8000/media/{}'.format(
                                           getusers.profilePic)
                    allcomments.append({'userName': getUserDjango.first_name , 
                                      'pic' :picUser,
                                      'userID':getusers.id ,
                                        'commentStr':itemCom.commentStr ,
                                      'published_at': itemCom.startTime})

            urlOwnerBlog = 'http://127.0.0.1:8000/media/{}'.format(
                getusersBlog.profilePic)
            blogs.append({
              'userID':getusersBlog.id,
              'first_name':getUserDjangoBlog.first_name,
              'picOwnerBlog':urlOwnerBlog,
              'imgBlog': blogImgarray,
              'title': item.title,
              'location': item.location,
              'description': item.description,
              'published_at': item.published_at,
              'blogID':item.id,
              'numLike':item.numLike,
              'comments':allcomments
            })  

        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4")
        print(blogs)    
        return Response(blogs)    
    else:
        return Response({'x':"no blog"})                                  






@api_view(['POST'])
def create(request):
    createBlog = Blog.objects.create(userID=users.objects.get(id =request.data.get('userID')), title=request.data.get(
        'title'), location=request.data.get('location'), description=request.data.get('body'), published_at=request.data.get('published_at'))
    
    try:
        filepath = request.FILES.getlist('images') if 'images' in request.FILES else False

        if filepath:
            for img in filepath:
                addImg =blogImg(blogID=createBlog, blogimg = img )
                addImg.save()
        return Response("done") 

    except IntegrityError as ex:
        transaction.rollback()
        message = ex.args
        return Response({"msg": message})           
              
    # photos = []
    # blogs = request.POST['blogID']
    # filepath = request.FILES.getlist(
    #     'blogimg') if 'blogimg' in request.FILES else False
    # for file in filepath:
    #         photo = blogImg.objects.create(
    #             blogID=Blog.objects.get(id=int(blogs)), blogimg=file)
    #         photos.append(photo)
    #     p_ser = FileListSerializer(photos, many=True)

    #     return Response(p_ser.data)


@api_view(['POST'])
def getBlog_with_related_company(request):
    blogs =[]
    allBlog = Blog.objects.filter(userID = users.objects.get(id = request.data)).all()
    if(allBlog.count() > 0):
        for item in allBlog:
           
            getusersBlog = users.objects.filter(id =item.userID.id).first()
            getUserDjangoBlog =User.objects.filter(id = getusersBlog.customUserID.id ).first()
            
           
            blogImgarray=[]
            getimagBlog = blogImg.objects.filter(blogID = int(item.id) ).all()
            if (getimagBlog.count() > 0):
                for itemImg in getimagBlog:
                    pic = 'http://127.0.0.1:8000/media/{}'.format(
                                            itemImg.blogimg)
                    blogImgarray.append(pic)

            allcomments = []
            getCom = comments.objects.filter(blogID = item).all()
            if(getCom.count() > 0):
                for itemCom in getCom:

                    getusers = users.objects.filter(id = itemCom.userID.id).first() 
        
                    getUserDjango = User.objects.filter(id = getusers.customUserID.id).first()
              
                    picUser = 'http://127.0.0.1:8000/media/{}'.format(
                                           getusers.profilePic)
                    allcomments.append({'userName': getUserDjango.first_name , 
                                      'pic' :picUser,
                                      'userID':getusers.id ,
                                      'commentStr':itemCom.commentStr ,
                                      'published_at': itemCom.startTime})

            urlOwnerBlog = 'http://127.0.0.1:8000/media/{}'.format(
                getusersBlog.profilePic)
            blogs.append({
              'blogID':item.id,  
              'userID':getusersBlog.id,
              'first_name':getUserDjangoBlog.first_name,
              'picOwnerBlog':urlOwnerBlog,
              'imgBlog': blogImgarray,
              'title': item.title,
              'location': item.location,
              'description': item.description,
              'published_at': item.published_at,
              'comments':allcomments,
               'numLike':item.numLike
            })  

        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4")
        print(blogs)    
        return Response(blogs)    
    else:
        return Response({'x':"no blog"})        

@api_view(['POST'])
def getOneBlog(request):
    blogs ={}
    oneBlog = Blog.objects.filter(id = request.data).first()
    getusersBlog = users.objects.filter(id =oneBlog.userID.id).first()
    getUserDjangoBlog =User.objects.filter(id = getusersBlog.customUserID.id ).first()
            
           
    blogImgarray=[]
    getimagBlog = blogImg.objects.filter(blogID = int(oneBlog.id) ).all()
    if (getimagBlog.count() > 0):
        for itemImg in getimagBlog:
            pic = 'http://127.0.0.1:8000/media/{}'.format(
                                            itemImg.blogimg)
            blogImgarray.append(pic)

    allcomments = []
    getCom = comments.objects.filter(blogID = oneBlog).all()
    if(getCom.count() > 0):
        for itemCom in getCom:

            getusers = users.objects.filter(id = itemCom.userID.id).first() 
        
            getUserDjango = User.objects.filter(id = getusers.customUserID.id).first()
                
            picUser = 'http://127.0.0.1:8000/media/{}'.format(
                                           getusers.profilePic)
            allcomments.append({'userName': getUserDjango.first_name , 
                                      'pic' :picUser,
                                      'userID':getusers.id ,
                                      'commentStr':itemCom.commentStr ,
                                      'published_at': itemCom.startTime})

    urlOwnerBlog = 'http://127.0.0.1:8000/media/{}'.format(
                getusersBlog.profilePic)
    blogs=({
              'blogID':oneBlog.id,  
              'userID':getusersBlog.id,
              'first_name':getUserDjangoBlog.first_name,
              'picOwnerBlog':urlOwnerBlog,
              'imgBlog': blogImgarray,
              'title': oneBlog.title,
              'location': oneBlog.location,
              'description': oneBlog.description,
              'published_at': oneBlog.published_at,
              'comments':allcomments,
               'numLike':oneBlog.numLike,
            })  

    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4")
    print(blogs)    
    return Response(blogs)    
    


@api_view(['POST']) 
def deleteBlog(request):
    try:

        deleteImg = blogImg.objects.filter(blogID =request.data ).all()
        if(deleteImg.count() > 0):
            for item in deleteImg:
                item.delete()

        deleteBlog = Blog.objects.filter(id = request.data ).all() 
        for item in deleteBlog:
            item.delete()

        return Response({"msg": "success"})
    except IntegrityError as ex:
        transaction.rollback()
        message = ex.args
        return Response({"msg": message})


@api_view(['POST']) 
def ubdateBlog(request):
    try:
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$&&&&&&&&&&&&&&&&**********8$$$$$$$$$$$$$$$$$$$$$4")
        print(request.data)
        filepath = request.FILES.getlist('images') if 'images' in request.FILES else False
        if filepath:
            updateImg = blogImg.objects.filter(blogID =request.data.get('blogID') ).first()
            for img in filepath:
                updateImg.blogimg = img
                updateImg.save()



        if(request.data.get('description') != ''):
            updateBlog = Blog.objects.filter(id =int(request.data.get('blogID'))).first() 
            updateBlog.description = request.data.get('description')
            updateBlog.save()

        return Response({"msg": "success"})
    except IntegrityError as ex:
        transaction.rollback()
        message = ex.args
        return Response({"msg": message})        


@api_view(['POST']) 
def addComment(request):

    try:
        
        comments.objects.create(blogID = Blog.objects.get(id=request.data.get('blogID')),
                                commentStr = request.data.get('commentString') ,
                                userID = users.objects.get(id = request.data.get('userID')),
                                startTime = request.data.get('published_at') ) 
      
       
        return Response('done')    
    
    except IntegrityError as ex:
        transaction.rollback()
        message = ex.args
        return Response({"msg": message})  

    
# class addComment(viewsets.ModelViewSet):
#     serializer_class = commentSerializer
#     queryset = comments.objects.all()
@api_view(['POST']) 
def Like(request):
    getBlog = Blog.objects.filter(id = request.data.get('blogID')).first()
    if(request.data.get('liked') == '0'):
        getBlog.numLike = getBlog.numLike - 1 
        getBlog.save()
        likesBlog.objects.filter(blogID = getBlog ,userID = users.objects.get(id = request.data.get('userID'))).delete()

    if(request.data.get('liked') == '1'):
        getBlog.numLike = getBlog.numLike + 1
        getBlog.save()    
        likesBlog.objects.create(blogID = getBlog ,userID = users.objects.get(id = request.data.get('userID')))

    return Response("done") 

@api_view(['POST']) 
def getlikesBlog_belongUser(request):
    getblogs =  likesBlog.objects.filter(userID = users.objects.get(id = request.data).id).all()
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print(getblogs)
    blogs=[]
    if(getblogs.count() > 0):
        for item in getblogs:
            blogs.append(item.blogID.id)

    return Response(blogs)    
