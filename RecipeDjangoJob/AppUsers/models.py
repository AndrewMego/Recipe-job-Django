from django.db import models
from django.contrib.auth.models  import User

# Create your models here.
class users(models.Model):
    customUserID = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(null=True,max_length=15, blank=True) 
    typeUser=models.CharField(max_length=10)
    profilePic=models.ImageField(null=True,upload_to = "images/user/" , blank=True )
    creationTime= models.DateTimeField(null=True)
    isActive=models.BooleanField(default=False)
    token_used_to_active =models.CharField(null=True,max_length=30 , blank=True)
    companyID=models.ForeignKey('company' , null=True , blank=True ,on_delete=models.PROTECT)


class company(models.Model):
    name = models.CharField(max_length=20 )
    location=models.CharField(max_length=50 )
    companyField=models.CharField(max_length=50 )




