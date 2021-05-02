from django.db import models
from AppJob import models as modelJob
from AppUsers import models as modelUser


def upload_path(instance, filname):
    return '/'.join(['blog', filname])

class Blog(models.Model):
    userID=models.ForeignKey(modelUser.users,on_delete=models.CASCADE)
    title=models.CharField(max_length=50 )
    location=models.CharField(max_length=50 )
    description=models.TextField(max_length=100 )
    published_at=models.DateTimeField(null=True)
    numLike = models.IntegerField(default=0 )

class blogImg(models.Model):
    blogID =  models.ForeignKey( Blog , on_delete=models.CASCADE )
    blogimg = models.ImageField(upload_to = upload_path)


class likesBlog(models.Model):
    blogID = models.ForeignKey( Blog , on_delete=models.CASCADE)
    userID = models.ForeignKey( modelUser.users , on_delete=models.CASCADE)
    class Meta:
        unique_together = (('userID', 'blogID'))  

class comments(models.Model):
    blogID=models.ForeignKey('Blog',on_delete=models.CASCADE) 
    commentStr=models.TextField()
    userID=models.ForeignKey(modelUser.users,on_delete=models.CASCADE)
    startTime=models.DateTimeField()


class tagsBlog(models.Model):
    tagID = models.ForeignKey(modelJob.tags , on_delete=models.CASCADE)
    blogID = models.ForeignKey(Blog , on_delete=models.CASCADE)

    class Meta:
        unique_together = (('tagID', 'blogID'))    

