from rest_framework import  serializers
from .models import Blog , comments , blogImg
from django.contrib.auth.models  import User


class blogSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Blog
        fields = ['id','userID','title', 'location', 'description']

class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = blogImg
        read_only_fields = ('id','blogID', 'blogimg')
    
class FileListSerializer ( serializers.ModelSerializer ) :
    
    #blogimg = serializers.ListField(child=serializers.FileField( max_length=100000,allow_empty_file=False,use_url=False ) )
   
    class Meta:
        model = blogImg
        fields = ["id","blogID", "blogimg"]

    # def create(self, validated_data):
       
      
    #     blogs=validated_data.pop('blogID')
    #     blogimg=validated_data.pop('blogimg')

    #     for img in blogimg:
    #         print("##########################")
    #         print(img)
    #         photo=blogImg.objects.create(blogID=blogs,blogimg=img)
    #        # p_ser = FileListSerializer(photo)
    #     return photo


 



class commentSerializer(serializers.ModelSerializer):
    class Meta:
        model = comments
        fields = ['id','blogID','commentStr', 'userID', 'startTime']



        



 