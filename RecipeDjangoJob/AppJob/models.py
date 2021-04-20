from django.db import models
from AppUsers import models as modelUser
from django.core.validators import MinValueValidator

# Create your models here.


class jobs(models.Model):

    JOB_TYPE = (('P', 'Part Time'), ('F', 'Full Time'))

    userID = models.ForeignKey(modelUser.users, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    location = models.ForeignKey('locations', on_delete=models.CASCADE)
    jobType = models.CharField(max_length=1, choices=JOB_TYPE)
    description = models.TextField(max_length=100)
    published_at = models.DateTimeField()
    vacancy = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    salary = models.FloatField(null=True, blank=True)
    categoryID = models.ForeignKey('category', on_delete=models.CASCADE)
    experience = models.CharField(max_length=50)
    aplayingNum = models.IntegerField()
    qualification = models.CharField(null=True, blank=True,max_length=50)
    benefits = models.CharField(null=True, blank=True,max_length=50)
    gender = models.CharField(null=True, blank=True,max_length=50)


class category(models.Model):
    name = models.CharField(max_length=30, unique=True)


class tags(models.Model):
    tag = models.CharField(max_length=30, unique=True)


class tagsJob(models.Model):
    tagID = models.ForeignKey(tags, on_delete=models.CASCADE)
    jobID = models.ForeignKey(jobs, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('tagID', 'jobID'))


class locations(models.Model):
    locName = models.CharField(max_length=20, unique=True)
          


class aplayUser(models.Model):
    userID = models.ForeignKey(modelUser.users, on_delete=models.CASCADE)
    jobID = models.ForeignKey(jobs, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    uploadCV = models.FileField(upload_to="files/cv/")
    aplay_at = models.DateTimeField()
    isAccept = models.BooleanField(default=False)

    class Meta:
        unique_together = (('userID', 'jobID'))


class certificate(models.Model):
    uploadCer = models.FileField(upload_to="files/certificate/")


class aplayCer(models.Model):
    cerID = models.ForeignKey(certificate, on_delete=models.CASCADE)
    aplayID = models.ForeignKey(aplayUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('cerID', 'aplayID'))
