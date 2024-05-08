
from xml.dom import ValidationErr
from rest_framework import serializers
from account.models import User
from django.utils.encoding import smart_str, force_bytes , DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Utill
#user registration serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    #we are writing password2 because we have to confirm the password on registration field
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta :
        model = User
        fields = ['email','password','password2','first_name','last_name','age','year_of_experience', 'skills', 'about','phone',]
        extra_kwargs={
            'password':{'write_only':True}
        }
    #validating password and confirm password are same or not 
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('password and confirm password does not match')
        return attrs 
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
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
        fields = ['id','email','first_name','last_name']

               
#passord change serializer 
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)      
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)    
    class Meta:
        fields = ['password','password2']
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
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
        fields = ['password','password2']
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
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
        fields = ['skills']      
       