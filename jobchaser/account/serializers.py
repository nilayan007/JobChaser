
from xml.dom import ValidationErr
from rest_framework import serializers
from account.models import User,Education,WorkExperience
from django.utils.encoding import smart_str, force_bytes , DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Utill
#user registration serializer

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id','degree', 'specialisation', 'start', 'end', 'school']
class WorkExperienceSerializer(serializers.ModelSerializer) :
    class Meta:
        model = WorkExperience
        fields = ['id','organisation','topSkill','current','start', 'end']       
        
class UserRegistrationSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(style={'input_type':'password'}, write_only=True)
    education = EducationSerializer(many=True)  # Nested serializer for Education
    Work = WorkExperienceSerializer(many=True,required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirmPassword', 'firstName', 'middleName', 'lastName', 'yoe','moe', 'skill', 'about','dob', 'gender', 'education','Work']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        confirmPassword = attrs.get('confirmPassword')
        if password != confirmPassword:
            raise serializers.ValidationError('Password and confirm password do not match')
        return attrs

    def create(self, validated_data):
        educations_data = validated_data.pop('education', None)  # Retrieve education data
        workexperince_data = validated_data.pop('Work',None)
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
    class Meta:
        model = User
        fields = ['id','email','firstName','lastName']

               
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
       