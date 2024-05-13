
from xml.dom import ValidationErr
from rest_framework import serializers
from account.models import User,Education,WorkExperience
from django.utils.encoding import smart_str, force_bytes , DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Utill
from datetime import datetime

#user registration serializer

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id','degree', 'specialisation', 'start', 'end', 'school']
    
class WorkExperienceSerializer(serializers.ModelSerializer) :
    class Meta:
        model = WorkExperience
        fields = ['id','organisation','topSkill','current','jobPost','start', 'end']       
        extra_kwargs = {
            'end': {'allow_null': True}
        }

        
class UserRegistrationSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(style={'input_type':'password'}, write_only=True)
    education = EducationSerializer(many=True)  # Nested serializer for Education
    work = WorkExperienceSerializer(many=True,required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirmPassword', 'firstName', 'middleName', 'lastName', 'yoe','moe', 'skill', 'about','dob', 'gender', 'education','work','phone','location']
        extra_kwargs = {
            'password': {'write_only': True},
            'middleName': {'allow_blank': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        confirmPassword = attrs.get('confirmPassword')
        if password != confirmPassword:
            raise serializers.ValidationError('Password and confirm password do not match')
        # Allow an empty string for middleName field
        return attrs
    


    def create(self, validated_data):
        educations_data = validated_data.pop('education', None)  # Retrieve education data
        workexperince_data = validated_data.pop('work',None)
        user = User.objects.create_user(**validated_data)  # Create User instance
        if educations_data:
            for education_data in educations_data:
                Education.objects.create(user=user, **education_data)
        if workexperince_data:
            for workexperinces_data in workexperince_data:
                WorkExperience.objects.create(user=user, **workexperinces_data)        
        return user

    
#user login serializer 

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']    
        
#profle serializer      

class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)
    education = EducationSerializer(many=True)
    work = WorkExperienceSerializer(many=True)

    class Meta:
        model = User
        fields = ['id','email','user_age', 'firstName', 'middleName', 'lastName', 'yoe', 'moe', 'skill', 'about', 'dob', 'gender', 'education', 'work','phone','location']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_id = data['id']
        
        # Retrieve related education instances for the user
        education_instances = Education.objects.filter(user_id=user_id)
        education_serializer = EducationSerializer(education_instances, many=True)
        data['education'] = education_serializer.data

        # Retrieve related work experience instances for the user
        work_instances = WorkExperience.objects.filter(user_id=user_id)
        work_serializer = WorkExperienceSerializer(work_instances, many=True)
        data['work'] = work_serializer.data
       # Extract and format start and end years (with error handling)
        for item in data['education']:
            if item['start']:
                date_string = item['start']
                date_object = datetime.strptime(date_string, "%Y-%m-%d")
                item['start'] = date_object.year
            if item['end']:
                date_string = item['end']
                date_object = datetime.strptime(date_string, "%Y-%m-%d")
                item['end'] = date_object.year
        for item in data['work']:
            if item['start']:
                date_string = item['start']
                date_object = datetime.strptime(date_string, "%Y-%m-%d")
                item['start'] = date_object.year
            if item['end']:
                date_string = item['end']
                date_object = datetime.strptime(date_string, "%Y-%m-%d")
                item['end'] = date_object.year or None

        data['skill'] = data['skill'].split(',')
        return data  
              
#passord change serializer 
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)      
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)    
    class Meta:
        fields = ['password','confirmPassword']
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('confirmPassword')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('password and confirm password does not match')
        user.set_password(password)
        user.save()
        return attrs  
    
#email sender serializer 
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta :
        fields = ['email']    
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id)) # for encoding the user id
            #print("encode uid", uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print("password reset token", token) 
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            #print('password reset link :',link)
            #send email
            body = "click the following link to reset password  : "+link
            data ={
                'email_subject' : 'Reset Your JobChaser Password',
                'body': body,
                'to_email' : user.email
            } 
            Utill.send_email(data)
            return attrs
        else:
            raise ValidationErr("you are not a registered user")
        
        
        
class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)      
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)    
    class Meta:
        fields = ['password','confirmPassword']
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('confirmPassword')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError('password and confirm password does not match')
            id = smart_str(urlsafe_base64_decode(uid)) #usinf smart str for converting it to string
            user = User.objects.get(id=id) #get the user from user id 
            if not  PasswordResetTokenGenerator().check_token(user,token): #checking the given token and the user token is same or not 
                raise ValidationErr('token is not vailid or expired')
            user.set_password(password)
            user.save()
            return attrs      
           
    
        except DjangoUnicodeDecodeError as indentifier :
            PasswordResetTokenGenerator().check_token(user,token) 
            raise ValidationErr('token is not vailid or expired')
        
class AlgorithmViewSerializer(serializers.ModelSerializer):
       class Meta:
        model = User
        fields = ['skill','yoe']      
       
class AlgorithmInputSerializer(serializers.Serializer):
    skill = serializers.CharField()
    yoe = serializers.IntegerField()       
    
    
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True)
    work = WorkExperienceSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ['email', 'firstName', 'middleName', 'lastName', 'yoe', 'moe', 'skill', 'about', 'dob', 'gender', 'education', 'work','phone','location']

    def update(self, instance, validated_data):
        educations_data = validated_data.pop('education', None)
        workexperience_data = validated_data.pop('work', None)

        # Update User fields
        instance.email = validated_data.get('email', instance.email)
        instance.firstName = validated_data.get('firstName', instance.firstName)
        instance.middleName = validated_data.get('middleName', instance.middleName)
        instance.lastName = validated_data.get('lastName', instance.lastName)
        instance.yoe = validated_data.get('yoe', instance.yoe)
        instance.moe = validated_data.get('moe', instance.moe)
        instance.skill = validated_data.get('skill', instance.skill)
        instance.about = validated_data.get('about', instance.about)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.location = validated_data.get('location', instance.location)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()

        # Update or Create nested Education objects
        if educations_data:
            for education_data in educations_data:
                education_id = education_data.get('id', None)
                if education_id:
                    education_instance = Education.objects.filter(user=instance, id=education_id).first()
                    if education_instance:
                        EducationSerializer().update(education_instance, education_data)
                    else:
                        Education.objects.create(user=instance, **education_data)
                else:
                    Education.objects.create(user=instance, **education_data)

        # Update or Create nested WorkExperience objects
        if workexperience_data:
            for workexperience_data in workexperience_data:
                work_id = workexperience_data.get('id', None)
                if work_id:
                    work_instance = WorkExperience.objects.filter(user=instance, id=work_id).first()
                    if work_instance:
                        WorkExperienceSerializer().update(work_instance, workexperience_data)
                    else:
                        WorkExperience.objects.create(user=instance, **workexperience_data)
                else:
                    WorkExperience.objects.create(user=instance, **workexperience_data)

        return instance
