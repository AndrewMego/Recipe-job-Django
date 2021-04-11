from rest_framework import  serializers
from AppJob.models import aplayUser, category, jobs, tags

class jobSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = jobs
        fields = ['id' , 'userID' , 'title' , 'location', 'jobType' , 'description' ,'published_at' , 'vacancy' , 'salary' , 'categoryID' ,'experience']



class catSerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = ['id' , 'name']



class tagSerializer(serializers.ModelSerializer):
    class Meta:
        model = tags
        fields = ['id' , 'name']        


class aplayJobSerializer(serializers.Serializer):
    
    
    class Meta:
        model = aplayUser
        fields = ['userID','jobID','name' , 'phone_number', 'uploadCV']
