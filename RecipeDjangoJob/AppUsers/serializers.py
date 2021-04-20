from rest_framework import  serializers
from .models import users 
from django.contrib.auth.models  import User


class customuserSerializer(serializers.Serializer):
     customUserID = serializers.IntegerField()
     phone_number = serializers.CharField()
     typeUser = serializers.CharField()
     profilePic = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True)
    # class Meta:
        
    #     model = users
    #     fields = ['customUserID','phone_number', 'typeUser', 'profilePic']

    

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','first_name','last_name','password']

# class companySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = company
#         fields = '__all__'     


class loginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']    


class FileSerializer(serializers.ModelSerializer):
    fileUpload = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True)
# class userSerializer(serializers.ModelSerializer):

#     class customuserSerializer(serializers.ModelSerializer):

#         class Meta:
#             model = users
#             exclude = ['phone_number', 'typeUser', 'profilePic']


#     model_User = customuserSerializer()

#     class Meta:
#         model = User
#         fields = ['username','email','first_name','last_name','password1']


# class companySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = company
#         fields = '__all__'                   